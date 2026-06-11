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

from tenderness.bounding_boxes.bounding_boxes_schema import (
    CharBBox,
    ClusterBBox,
    LayoutBBox,
    LineBBox,
    Quadrilateral,
    RunBBox,
    TextBoundingBoxes,
)
from tenderness.pango_backend.pango_enum_coerce import PangoEnumMap


class TestTextBoundingBoxes:
    def test_fields_present(
        self,
        logical_bbox: Quadrilateral,
        ink_bbox: Quadrilateral,
    ) -> None:
        char_box = CharBBox(
            logical_bbox=logical_bbox,
            text="d",
            byte_index=0,
            byte_length=1,
        )
        cluster_box = ClusterBBox(
            logical_bbox=logical_bbox,
            ink_bbox=ink_bbox,
            text="dummy_cluster",
            byte_index=0,
            byte_length=13,
        )
        run_box = RunBBox(
            logical_bbox=logical_bbox,
            ink_bbox=ink_bbox,
            text="dummy_run",
            byte_index=0,
            byte_length=9,
            baseline=21.0,
        )
        line_box = LineBBox(
            logical_bbox=logical_bbox,
            ink_bbox=ink_bbox,
            text="dummy_line",
            byte_index=0,
            byte_length=10,
            resolved_direction=PangoEnumMap.Direction["ltr"],
            is_paragraph_start=True,
            baseline=22.0,
        )
        layout_box = LayoutBBox(
            logical_bbox=logical_bbox,
            ink_bbox=ink_bbox,
            text="dummy_layout",
        )
        collection = TextBoundingBoxes(
            char_bboxes=[char_box],
            cluster_bboxes=[cluster_box],
            run_bboxes=[run_box],
            line_bboxes=[line_box],
            layout_bbox=layout_box,
        )

        assert collection.char_bboxes == [char_box]
        assert collection.cluster_bboxes == [cluster_box]
        assert collection.run_bboxes == [run_box]
        assert collection.line_bboxes == [line_box]
        assert collection.layout_bbox == layout_box

    def test_all_fields_default_to_none(self) -> None:
        collection = TextBoundingBoxes()
        assert collection.char_bboxes is None
        assert collection.cluster_bboxes is None
        assert collection.run_bboxes is None
        assert collection.line_bboxes is None
        assert collection.layout_bbox is None
