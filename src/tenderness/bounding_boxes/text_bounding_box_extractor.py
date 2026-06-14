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

"""Text bounding box extractor."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import TYPE_CHECKING

import gi
import numpy  # noqa: ICN001

from tenderness.bounding_boxes.bounding_boxes_schema import (
    BoundingBoxType,
    CharBBox,
    ClusterBBox,
    LayoutBBox,
    LineBBox,
    Quadrilateral,
    RunBBox,
    TextBoundingBoxes,
)

if TYPE_CHECKING:
    import cairo

gi.require_version("Pango", "1.0")


from gi.repository import Pango  # noqa: E402


@dataclass(slots=True)
class _RawCluster:
    byte_index: int
    run_end: int
    ink_rect: Pango.Rectangle
    logical_rect: Pango.Rectangle


@dataclass(slots=True)
class _TextData:
    text: str
    byte_to_char: numpy.ndarray
    byte_lengths: numpy.ndarray


_ALL_LEVELS: set[BoundingBoxType] = set(BoundingBoxType)


class TextBoundingBoxExtractor:
    """Extract text bounding boxes at character, cluster, run, line, and layout granularity."""

    def extract_bounding_boxes(
        self,
        pango_layout: Pango.Layout,
        matrix: cairo.Matrix,
        *,
        include_text: bool = True,
        levels: set[BoundingBoxType] | None = None,
    ) -> TextBoundingBoxes:
        """Extract bounding boxes at the requested granularity levels.

        Parameters
        ----------
        pango_layout
            Layout to extract bounding boxes from.
        matrix
            Cairo transformation matrix applied to all coordinates.
        include_text
            If ``True``, populate the ``text`` field of each bounding box.
        levels
            Granularity levels to extract; ``None`` extracts all levels.

        Returns
        -------
        TextBoundingBoxes
            Empty when the layout contains no characters.
        """
        if levels is None:
            levels = _ALL_LEVELS

        if pango_layout.get_character_count() == 0:
            return TextBoundingBoxes()

        if include_text:
            layout_text = pango_layout.get_text()
            text_length = len(layout_text)
            encoded = numpy.frombuffer(layout_text.encode(encoding="utf-8", errors="strict"), dtype=numpy.uint8)
            text_data: _TextData | None = _TextData(
                text=layout_text,
                byte_to_char=self._build_byte_to_char_map(encoded=encoded, n_chars=text_length),
                byte_lengths=self._build_byte_lengths(encoded=encoded),
            )
        else:
            text_data = None

        text_bboxes = TextBoundingBoxes()

        if BoundingBoxType.CHAR in levels:
            text_bboxes.char_bboxes = self._extract_chars(
                pango_layout=pango_layout,
                matrix=matrix,
                text_data=text_data,
            )

        if BoundingBoxType.CLUSTER in levels:
            text_bboxes.cluster_bboxes = self._extract_clusters(
                pango_layout=pango_layout,
                matrix=matrix,
                text_data=text_data,
            )

        if BoundingBoxType.RUN in levels:
            text_bboxes.run_bboxes = self._extract_runs(
                pango_layout=pango_layout,
                matrix=matrix,
                text_data=text_data,
            )

        if BoundingBoxType.LINE in levels:
            text_bboxes.line_bboxes = self._extract_lines(
                pango_layout=pango_layout,
                matrix=matrix,
                text_data=text_data,
            )

        if BoundingBoxType.LAYOUT in levels:
            text_bboxes.layout_bbox = self._extract_layout(
                pango_layout=pango_layout,
                matrix=matrix,
                layout_text=text_data.text if text_data is not None else None,
            )

        return text_bboxes

    def _build_byte_to_char_map(self, encoded: numpy.ndarray, n_chars: int) -> numpy.ndarray:
        """Return byte_to_char[byte_index] -> char_index for a UTF-8 encoded string.

        Parameters
        ----------
        encoded
            UTF-8 encoded bytes as a numpy array.
        n_chars
            Number of Unicode characters in the original string.

        Returns
        -------
        numpy.ndarray
            Array of shape ``(len(encoded) + 1,)`` where each entry maps a byte
            index to its corresponding character index.
        """
        byte_to_char = numpy.empty(len(encoded) + 1, dtype=numpy.intp)
        if len(encoded) == 0:
            byte_to_char[0] = 0
            return byte_to_char
        is_char_start = (encoded & 0xC0) != 0x80  # noqa: PLR2004

        # Note: Cumsum outputs 1-based indices (e.g., [1, 2, 2]).
        # By setting the first byte to False, we force it to output
        # 0-based indices (e.g., [0, 1, 1]) matching Python string indices.
        # This is safe because `encoded` is strictly verified UTF-8.
        is_char_start[0] = False
        byte_to_char[:-1] = numpy.cumsum(is_char_start, dtype=numpy.intp)
        byte_to_char[-1] = n_chars
        return byte_to_char

    def _build_byte_lengths(self, encoded: numpy.ndarray) -> numpy.ndarray:
        """Return byte_lengths[byte_index] -> UTF-8 byte length of the char starting at byte_index.

        Parameters
        ----------
        encoded
            UTF-8 encoded bytes as a numpy array.

        Returns
        -------
        numpy.ndarray
            Array of shape ``(len(encoded),)`` where each entry is the byte
            length of the UTF-8 character starting at that byte index.
        """
        char_byte_lengths = numpy.ones(len(encoded), dtype=numpy.uint8)
        char_byte_lengths[encoded >= 0xF0] = 4  # noqa: PLR2004
        char_byte_lengths[(encoded >= 0xE0) & (encoded < 0xF0)] = 3  # noqa: PLR2004
        char_byte_lengths[(encoded >= 0xC0) & (encoded < 0xE0)] = 2  # noqa: PLR2004
        return char_byte_lengths

    def _pango_rect_to_quadrilateral(self, matrix: cairo.Matrix, rect: Pango.Rectangle) -> Quadrilateral:
        u2d = Pango.units_to_double
        x = u2d(rect.x)
        y = u2d(rect.y)
        w = u2d(rect.width)
        h = u2d(rect.height)
        tp = matrix.transform_point
        return Quadrilateral(
            top_left=tp(x, y),
            top_right=tp(x + w, y),
            bottom_right=tp(x + w, y + h),
            bottom_left=tp(x, y + h),
        )

    def _extract_chars(
        self,
        pango_layout: Pango.Layout,
        matrix: cairo.Matrix,
        *,
        text_data: _TextData | None,
    ) -> list[CharBBox]:
        it = pango_layout.get_iter()
        char_bboxes: list[CharBBox] = []
        prev_byte_index = -1
        while True:
            char = it.get_char_extents()
            byte_index = it.get_index()
            if text_data is not None:
                # Pango visits \r\n as two chars but reports \r's byte_index for both.
                if byte_index == prev_byte_index:
                    actual_byte_index = byte_index + int(text_data.byte_lengths[byte_index])
                else:
                    actual_byte_index = byte_index
                char_text: str | None = text_data.text[int(text_data.byte_to_char[actual_byte_index])]
                byte_length: int | None = int(text_data.byte_lengths[actual_byte_index])
            else:
                actual_byte_index = byte_index
                char_text = None
                byte_length = None
            char_bboxes.append(
                CharBBox(
                    text=char_text,
                    byte_index=actual_byte_index,
                    byte_length=byte_length,
                    logical_bbox=self._pango_rect_to_quadrilateral(matrix=matrix, rect=char),
                )
            )
            prev_byte_index = byte_index
            if not it.next_char():
                break
        return char_bboxes

    def _extract_clusters(
        self,
        pango_layout: Pango.Layout,
        matrix: cairo.Matrix,
        *,
        text_data: _TextData | None,
    ) -> list[ClusterBBox]:
        it = pango_layout.get_iter()

        # Pass 1: collect raw data in visual order; skip between-run gaps where run is None.
        raw_clusters: list[_RawCluster] = []
        while True:
            run = it.get_run_readonly()
            if run is not None:
                ink_rect, logical_rect = it.get_cluster_extents()
                raw_clusters.append(
                    _RawCluster(
                        byte_index=it.get_index(),
                        run_end=run.item.offset + run.item.length,
                        ink_rect=ink_rect,
                        logical_rect=logical_rect,
                    )
                )
            if not it.next_cluster():
                break

        # Pass 2: group byte_indexes by run (run_end is unique per run), sort ascending
        # (logical order), compute byte_end.
        run_groups: dict[int, list[int]] = defaultdict(list)
        for cluster in raw_clusters:
            run_groups[cluster.run_end].append(cluster.byte_index)

        cluster_byte_ends: dict[int, int] = {}
        for run_end, indices in run_groups.items():
            indices.sort()
            for i, idx in enumerate(indices):
                cluster_byte_ends[idx] = indices[i + 1] if i + 1 < len(indices) else run_end

        # Pass 3: build result in original visual order.
        # byte_to_char is padded to len(text_bytes)+1 with a sentinel, so byte_end==len(text_bytes) is a safe index.
        cluster_bboxes: list[ClusterBBox] = []
        for cluster in raw_clusters:
            byte_end = cluster_byte_ends[cluster.byte_index]
            cluster_text: str | None = (
                text_data.text[text_data.byte_to_char[cluster.byte_index] : text_data.byte_to_char[byte_end]]
                if text_data is not None
                else None
            )
            cluster_bboxes.append(
                ClusterBBox(
                    text=cluster_text,
                    byte_index=cluster.byte_index,
                    byte_length=byte_end - cluster.byte_index,
                    logical_bbox=self._pango_rect_to_quadrilateral(matrix=matrix, rect=cluster.logical_rect),
                    ink_bbox=self._pango_rect_to_quadrilateral(matrix=matrix, rect=cluster.ink_rect),
                )
            )

        return cluster_bboxes

    def _extract_runs(
        self,
        pango_layout: Pango.Layout,
        matrix: cairo.Matrix,
        *,
        text_data: _TextData | None,
    ) -> list[RunBBox]:
        it = pango_layout.get_iter()
        run_bboxes: list[RunBBox] = []
        while True:
            run = it.get_run_readonly()
            # Pango inserts a NULL sentinel run at the end of every line
            # (guarantees every line has ≥1 run, even newline-only lines).
            # There are no extents to record for these gaps, so skip them.
            if run is not None:
                ink_rect, logical_rect = it.get_run_extents()
                # run is a PangoGlyphItem; run.item is the underlying PangoItem.
                byte_index = run.item.offset  # byte offset from layout text start
                byte_length = run.item.length  # byte length of this run
                if text_data is not None:
                    char_start = int(text_data.byte_to_char[byte_index])
                    char_end = int(text_data.byte_to_char[byte_index + byte_length])
                    run_text: str | None = text_data.text[char_start:char_end]
                else:
                    run_text = None
                run_bboxes.append(
                    RunBBox(
                        text=run_text,
                        byte_index=byte_index,
                        byte_length=byte_length,
                        baseline=Pango.units_to_double(it.get_run_baseline()),
                        ink_bbox=self._pango_rect_to_quadrilateral(matrix=matrix, rect=ink_rect),
                        logical_bbox=self._pango_rect_to_quadrilateral(matrix=matrix, rect=logical_rect),
                    )
                )
            if not it.next_run():
                break
        return run_bboxes

    def _extract_lines(
        self,
        pango_layout: Pango.Layout,
        matrix: cairo.Matrix,
        *,
        text_data: _TextData | None,
    ) -> list[LineBBox]:
        it = pango_layout.get_iter()
        line_bboxes: list[LineBBox] = []
        while True:
            line = it.get_line_readonly()
            if line is not None:
                ink_rect, logical_rect = it.get_line_extents()
                byte_index = line.get_start_index()
                byte_length = line.get_length()
                if text_data is not None:
                    char_start = int(text_data.byte_to_char[byte_index])
                    char_end = int(text_data.byte_to_char[byte_index + byte_length])
                    line_text: str | None = text_data.text[char_start:char_end]
                else:
                    line_text = None
                line_bboxes.append(
                    LineBBox(
                        text=line_text,
                        byte_index=byte_index,
                        byte_length=byte_length,
                        resolved_direction=line.get_resolved_direction(),
                        is_paragraph_start=bool(line.is_paragraph_start),
                        baseline=Pango.units_to_double(it.get_baseline()),
                        ink_bbox=self._pango_rect_to_quadrilateral(matrix=matrix, rect=ink_rect),
                        logical_bbox=self._pango_rect_to_quadrilateral(matrix=matrix, rect=logical_rect),
                    )
                )
            if not it.next_line():
                break
        return line_bboxes

    def _extract_layout(
        self,
        pango_layout: Pango.Layout,
        matrix: cairo.Matrix,
        layout_text: str | None,
    ) -> LayoutBBox:
        it = pango_layout.get_iter()
        ink_rect, logical_rect = it.get_layout_extents()

        return LayoutBBox(
            logical_bbox=self._pango_rect_to_quadrilateral(matrix=matrix, rect=logical_rect),
            ink_bbox=self._pango_rect_to_quadrilateral(matrix=matrix, rect=ink_rect),
            text=layout_text,
        )
