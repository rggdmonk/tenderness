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

from dataclasses import dataclass

import pytest

from tenderness.bounding_boxes.bounding_boxes_schema import LineBBox, Quadrilateral
from tenderness.pango_backend.pango_enum_coerce import PangoEnumMap


@dataclass(frozen=True, slots=True)
class LineBBoxTestCase:
    test_name: str
    text: str | None
    byte_index: int
    byte_length: int
    direction_name: str
    is_paragraph_start: bool
    baseline: float


LINE_BBOX_TEST_CASES: tuple[LineBBoxTestCase, ...] = (
    LineBBoxTestCase(
        test_name="dummy_latin_line",
        text="Hello world",
        byte_index=0,
        byte_length=11,
        direction_name="ltr",
        is_paragraph_start=True,
        baseline=12.0,
    ),
    LineBBoxTestCase(
        test_name="dummy_cyrillic_line",
        text="Привет мир",
        byte_index=11,
        byte_length=19,
        direction_name="ltr",
        is_paragraph_start=False,
        baseline=13.0,
    ),
    LineBBoxTestCase(
        test_name="dummy_greek_line",
        text="Γεια σου",  # noqa: RUF001
        byte_index=30,
        byte_length=15,
        direction_name="ltr",
        is_paragraph_start=False,
        baseline=14.0,
    ),
    LineBBoxTestCase(
        test_name="dummy_arabic_line",
        text="مرحبا بالعالم",
        byte_index=45,
        byte_length=25,
        direction_name="rtl",
        is_paragraph_start=True,
        baseline=15.0,
    ),
    LineBBoxTestCase(
        test_name="dummy_missing_line_text",
        text=None,
        byte_index=70,
        byte_length=0,
        direction_name="neutral",
        is_paragraph_start=False,
        baseline=16.0,
    ),
)


class TestLineBBox:
    @pytest.mark.parametrize(
        "test_case",
        LINE_BBOX_TEST_CASES,
        ids=lambda test_case: test_case.test_name,
    )
    def test_to_dict_serializes_line_box(
        self,
        test_case: LineBBoxTestCase,
        logical_bbox: Quadrilateral,
        ink_bbox: Quadrilateral,
    ) -> None:
        box = LineBBox(
            logical_bbox=logical_bbox,
            ink_bbox=ink_bbox,
            text=test_case.text,
            byte_index=test_case.byte_index,
            byte_length=test_case.byte_length,
            resolved_direction=PangoEnumMap.Direction[test_case.direction_name],
            is_paragraph_start=test_case.is_paragraph_start,
            baseline=test_case.baseline,
        )

        assert box.to_dict() == {
            "logical_bbox": logical_bbox.to_dict(),
            "ink_bbox": ink_bbox.to_dict(),
            "text": test_case.text,
            "byte_index": test_case.byte_index,
            "byte_length": test_case.byte_length,
            "resolved_direction": test_case.direction_name,
            "is_paragraph_start": test_case.is_paragraph_start,
            "baseline": test_case.baseline,
        }
