# Copyright 2026 Pavel Stepachev
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations

import logging
from collections import defaultdict
from dataclasses import dataclass
from typing import TYPE_CHECKING

import gi

from tenderness.bounding_boxes.bounding_boxes_schema import (
    BoundingBoxStrategy,
    BoundingBoxType,
    CharBBox,
    ClusterBBox,
    LayoutBBox,
    LayoutBBoxCollection,
    LineBBox,
    RunBBox,
    Tetragon,
)

if TYPE_CHECKING:
    import cairo

gi.require_version("Pango", "1.0")


from gi.repository import Pango  # noqa: E402

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class _RawCluster:
    byte_index: int
    ink_rect: Pango.Rectangle
    logical_rect: Pango.Rectangle
    run_byte_start: int
    run_byte_end: int


class TextBoundingBoxExtractor:  # noqa: D101 TODO: docstring
    PANGO_SCALE: int = Pango.SCALE

    # --------------------------
    # Public API
    # --------------------------
    def extract_bounding_boxes(  # noqa: D102 TODO: docstring
        self,
        pango_layout: Pango.Layout,
        matrix: cairo.Matrix,
        origin: tuple[float, float] | None = None,
        levels: set[BoundingBoxType] | None = None,
        text_mode: BoundingBoxStrategy = BoundingBoxStrategy.WITH_TEXT,
    ) -> LayoutBBoxCollection:
        # `matrix` is a copy of the CTM (user→device). Pango layout coords are relative to (0,0).
        # `PangoCairo.show_layout` renders them offset by the current point set via move_to.
        # That current point is NOT part of the CTM, so it must be applied to the matrix copy
        # here so bbox coordinates end up in the correct device-space position.
        if origin is not None:
            matrix.translate(origin[0], origin[1])

        if levels is None:
            levels = set(BoundingBoxType)

        layout_text = pango_layout.get_text()
        text_bytes = layout_text.encode("utf-8") if text_mode != BoundingBoxStrategy.ONLY_BOXES else b""

        result = LayoutBBoxCollection()

        if BoundingBoxType.CHAR in levels:
            result.char_boxes = self._extract_chars(
                pango_layout=pango_layout, matrix=matrix, text_bytes=text_bytes, text_mode=text_mode
            )
        if BoundingBoxType.CLUSTER in levels:
            result.cluster_boxes = self._extract_clusters(
                pango_layout=pango_layout, matrix=matrix, text_bytes=text_bytes, text_mode=text_mode
            )
        if BoundingBoxType.RUN in levels:
            result.run_boxes = self._extract_runs(
                pango_layout=pango_layout, matrix=matrix, text_bytes=text_bytes, text_mode=text_mode
            )
        if BoundingBoxType.LINE in levels:
            result.line_boxes = self._extract_lines(
                pango_layout=pango_layout, matrix=matrix, text_bytes=text_bytes, text_mode=text_mode
            )
        if BoundingBoxType.LAYOUT in levels:
            result.layout_box = self._extract_layout(
                pango_layout=pango_layout,
                matrix=matrix,
                layout_text=layout_text if text_mode != BoundingBoxStrategy.ONLY_BOXES else None,
            )

        return result

    # --------------------------
    # Helpers
    # --------------------------
    def _to_tetragon(self, matrix: cairo.Matrix, rect: Pango.Rectangle) -> Tetragon:
        x = rect.x / self.PANGO_SCALE
        y = rect.y / self.PANGO_SCALE
        w = rect.width / self.PANGO_SCALE
        h = rect.height / self.PANGO_SCALE
        return Tetragon(
            top_left=matrix.transform_point(x, y),
            top_right=matrix.transform_point(x + w, y),
            bottom_right=matrix.transform_point(x + w, y + h),
            bottom_left=matrix.transform_point(x, y + h),
        )

    def _to_baseline(self, raw: int) -> float:
        return raw / self.PANGO_SCALE

    @staticmethod
    def _decode(text_bytes: bytes, start: int, end: int) -> str:
        return text_bytes[start:end].decode("utf-8", errors="strict")

    # --------------------------
    # Per-level extraction methods
    # --------------------------
    def _extract_chars(
        self,
        pango_layout: Pango.Layout,
        matrix: cairo.Matrix,
        text_bytes: bytes,
        text_mode: BoundingBoxStrategy,
    ) -> list[CharBBox]:

        # build byte_offset → char mapping once — O(n) total
        char_at_byte: dict[int, str] = {}
        if text_mode != BoundingBoxStrategy.ONLY_BOXES:
            byte_offset = 0
            for ch in text_bytes.decode("utf-8", errors="strict"):
                char_at_byte[byte_offset] = ch
                byte_offset += len(ch.encode("utf-8"))

        it = pango_layout.get_iter()
        boxes: list[CharBBox] = []

        while True:
            byte_index = it.get_index()
            logical_rect = it.get_char_extents()

            boxes.append(
                CharBBox(
                    logical_bbox=self._to_tetragon(matrix=matrix, rect=logical_rect),
                    char=char_at_byte.get(byte_index),
                    byte_index=byte_index,
                )
            )
            if not it.next_char():
                break

        return boxes

    def _extract_clusters(
        self,
        pango_layout: Pango.Layout,
        matrix: cairo.Matrix,
        text_bytes: bytes,
        text_mode: BoundingBoxStrategy,
    ) -> list[ClusterBBox]:

        it = pango_layout.get_iter()
        raw: list[_RawCluster] = []

        while True:
            byte_index = it.get_index()
            ink_rect, logical_rect = it.get_cluster_extents()
            run = it.get_run_readonly()

            run_start, run_end = 0, 0
            if run is not None:
                try:
                    run_start = run.item.offset
                    run_end = run_start + run.item.length
                except AttributeError:
                    run_start = run_end = byte_index

            raw.append(
                _RawCluster(
                    byte_index=byte_index,
                    ink_rect=ink_rect,
                    logical_rect=logical_rect,
                    run_byte_start=run_start,
                    run_byte_end=run_end,
                )
            )
            if not it.next_cluster():
                break

        # Pre-compute byte_end for each cluster.
        # Group by run span once (O(n)), sort byte indices within each run,
        # then use the next sorted index (or run_end) as the cluster's byte end.
        run_groups: dict[tuple[int, int], list[int]] = defaultdict(list)
        for entry in raw:
            run_groups[(entry.run_byte_start, entry.run_byte_end)].append(entry.byte_index)
        for indices in run_groups.values():
            indices.sort()

        byte_ends: list[int] = []
        for entry in raw:
            run_indices = run_groups[(entry.run_byte_start, entry.run_byte_end)]
            pos = run_indices.index(entry.byte_index)
            byte_end = run_indices[pos + 1] if pos + 1 < len(run_indices) else entry.run_byte_end
            byte_ends.append(byte_end)

        boxes: list[ClusterBBox] = []
        for i, entry in enumerate(raw):
            cluster_text: str | None = None
            if text_mode != BoundingBoxStrategy.ONLY_BOXES:
                cluster_text = self._decode(text_bytes, entry.byte_index, byte_ends[i])
            boxes.append(
                ClusterBBox(
                    logical_bbox=self._to_tetragon(matrix=matrix, rect=entry.logical_rect),
                    ink_bbox=self._to_tetragon(matrix=matrix, rect=entry.ink_rect),
                    text=cluster_text,
                    byte_index=entry.byte_index,
                )
            )
        return boxes

    def _extract_runs(
        self,
        pango_layout: Pango.Layout,
        matrix: cairo.Matrix,
        text_bytes: bytes,
        text_mode: BoundingBoxStrategy,
    ) -> list[RunBBox]:

        it = pango_layout.get_iter()
        boxes: list[RunBBox] = []

        while True:
            ink_rect, logical_rect = it.get_run_extents()
            baseline = it.get_run_baseline()
            run = it.get_run_readonly()

            byte_start = byte_length = 0
            if run is not None:
                try:
                    byte_start = run.item.offset
                    byte_length = run.item.length
                except AttributeError:
                    byte_start = it.get_index()
                    byte_length = 0

            run_text: str | None = None
            if text_mode != BoundingBoxStrategy.ONLY_BOXES:
                run_text = self._decode(text_bytes, byte_start, byte_start + byte_length)

            boxes.append(
                RunBBox(
                    logical_bbox=self._to_tetragon(matrix=matrix, rect=logical_rect),
                    baseline=self._to_baseline(raw=baseline),
                    ink_bbox=self._to_tetragon(matrix=matrix, rect=ink_rect),
                    text=run_text,
                    byte_start=byte_start,
                    byte_length=byte_length,
                )
            )
            if not it.next_run():
                break

        return boxes

    def _extract_lines(
        self,
        pango_layout: Pango.Layout,
        matrix: cairo.Matrix,
        text_bytes: bytes,
        text_mode: BoundingBoxStrategy,
    ) -> list[LineBBox]:
        it = pango_layout.get_iter()
        boxes: list[LineBBox] = []

        while True:
            ink_rect, logical_rect = it.get_line_extents()
            baseline = it.get_baseline()
            line = it.get_line_readonly()

            byte_start: int = line.start_index  # type: ignore[union-attr]
            byte_length: int = line.length  # type: ignore[union-attr]
            resolved_direction: Pango.Direction = line.get_resolved_direction()  # type: ignore
            is_paragraph_start: bool = line.is_paragraph_start()  # type: ignore

            line_text: str | None = None
            if text_mode != BoundingBoxStrategy.ONLY_BOXES:
                line_text = self._decode(text_bytes, byte_start, byte_start + byte_length)

            boxes.append(
                LineBBox(
                    logical_bbox=self._to_tetragon(matrix=matrix, rect=logical_rect),
                    baseline=self._to_baseline(raw=baseline),
                    ink_bbox=self._to_tetragon(matrix=matrix, rect=ink_rect),
                    text=line_text,
                    byte_start=byte_start,
                    byte_length=byte_length,
                    resolved_direction=resolved_direction,
                    is_paragraph_start=is_paragraph_start,
                )
            )
            if not it.next_line():
                break

        return boxes

    def _extract_layout(
        self,
        pango_layout: Pango.Layout,
        matrix: cairo.Matrix,
        layout_text: str | None,
    ) -> LayoutBBox:
        it = pango_layout.get_iter()
        ink_rect, logical_rect = it.get_layout_extents()

        return LayoutBBox(
            logical_bbox=self._to_tetragon(matrix=matrix, rect=logical_rect),
            ink_bbox=self._to_tetragon(matrix=matrix, rect=ink_rect),
            text=layout_text,
        )
