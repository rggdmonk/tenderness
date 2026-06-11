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
from typing import ClassVar

import gi
import pytest

from tenderness.bounding_boxes.bounding_boxes_schema import BoundingBoxType
from tenderness.bounding_boxes.text_bounding_box_extractor import TextBoundingBoxExtractor
from tests._test_utils.render_helpers import (
    _testutil_assert_no_ink_bbox_overlap,
    _testutil_assert_no_logical_bbox_overlap,
    _testutil_simple_text,
)

gi.require_version("Pango", "1.0")
from gi.repository import Pango  # noqa: E402


@dataclass(slots=True, frozen=True)
class ExpectedLineBBox:
    text: str | None
    byte_index: int
    byte_length: int
    resolved_direction: Pango.Direction
    is_paragraph_start: bool


@dataclass(slots=True, frozen=True)
class LineBBoxExtractionTestCase:
    test_name: str
    input_text: str
    include_text: bool
    expected_lines: list[ExpectedLineBBox]


LINE_BBOX_EXTRACTION_TEST_CASES: list[LineBBoxExtractionTestCase] = [
    LineBBoxExtractionTestCase(
        test_name="latin_single_line",
        input_text="xyz",
        include_text=True,
        expected_lines=[
            ExpectedLineBBox(
                text="xyz",
                byte_index=0,
                byte_length=3,
                resolved_direction=Pango.Direction.LTR,
                is_paragraph_start=True,
            ),
        ],
    ),
    LineBBoxExtractionTestCase(
        test_name="latin_two_lines",
        input_text="foo\nbar",
        include_text=True,
        expected_lines=[
            ExpectedLineBBox(
                text="foo",
                byte_index=0,
                byte_length=3,
                resolved_direction=Pango.Direction.LTR,
                is_paragraph_start=True,
            ),
            ExpectedLineBBox(
                text="bar",
                byte_index=4,
                byte_length=3,
                resolved_direction=Pango.Direction.LTR,
                is_paragraph_start=True,
            ),
        ],
    ),
    LineBBoxExtractionTestCase(
        test_name="2byte_greek_single_line",
        input_text="δεζ",
        include_text=True,
        expected_lines=[
            ExpectedLineBBox(
                text="δεζ",
                byte_index=0,
                byte_length=6,
                resolved_direction=Pango.Direction.LTR,
                is_paragraph_start=True,
            ),
        ],
    ),
    LineBBoxExtractionTestCase(
        test_name="3byte_japanese_single_line",
        input_text="東京都",
        include_text=True,
        expected_lines=[
            ExpectedLineBBox(
                text="東京都",
                byte_index=0,
                byte_length=9,
                resolved_direction=Pango.Direction.LTR,
                is_paragraph_start=True,
            ),
        ],
    ),
    # Arabic is RTL — resolved_direction should be RTL for the line
    # "كتب" (books): ك(2) + ت(2) + ب(2) = 6 bytes, 3 chars
    LineBBoxExtractionTestCase(
        test_name="arabic_rtl_single_line",
        input_text="كتب",
        include_text=True,
        expected_lines=[
            ExpectedLineBBox(
                text="كتب",
                byte_index=0,
                byte_length=6,
                resolved_direction=Pango.Direction.RTL,
                is_paragraph_start=True,
            ),
        ],
    ),
    # Mixed LTR then RTL paragraphs — each newline starts a new paragraph
    # "world\nكتب": line1=5 bytes (world), \n at byte 5, line2=6 bytes (كتب) at byte 6
    LineBBoxExtractionTestCase(
        test_name="ltr_then_rtl_paragraphs",
        input_text="world\nكتب",
        include_text=True,
        expected_lines=[
            ExpectedLineBBox(
                text="world",
                byte_index=0,
                byte_length=5,
                resolved_direction=Pango.Direction.LTR,
                is_paragraph_start=True,
            ),
            ExpectedLineBBox(
                text="كتب",
                byte_index=6,
                byte_length=6,
                resolved_direction=Pango.Direction.RTL,
                is_paragraph_start=True,
            ),
        ],
    ),
    LineBBoxExtractionTestCase(
        test_name="numbers_three_lines",
        input_text="123\n456\n7890",
        include_text=True,
        expected_lines=[
            ExpectedLineBBox(
                text="123",
                byte_index=0,
                byte_length=3,
                resolved_direction=Pango.Direction.LTR,
                is_paragraph_start=True,
            ),
            ExpectedLineBBox(
                text="456",
                byte_index=4,
                byte_length=3,
                resolved_direction=Pango.Direction.LTR,
                is_paragraph_start=True,
            ),
            ExpectedLineBBox(
                text="7890",
                byte_index=8,
                byte_length=4,
                resolved_direction=Pango.Direction.LTR,
                is_paragraph_start=True,
            ),
        ],
    ),
]


class TestTextBoundingBoxExtractorLineBBoxExtraction:
    _FAMILY_NAME: ClassVar[str] = "Noto Sans"
    _FAMILY_SIZE: ClassVar[int] = 24
    _HEIGHT: ClassVar[int] = 500
    _WIDTH: ClassVar[int] = 500
    _LEVELS: ClassVar[set[BoundingBoxType]] = set({BoundingBoxType.LINE})

    @pytest.mark.usefixtures("unittests_font_setup")
    @pytest.mark.parametrize("test_case", LINE_BBOX_EXTRACTION_TEST_CASES, ids=lambda tc: tc.test_name)
    def test_line_bbox_extraction(self, test_case: LineBBoxExtractionTestCase) -> None:

        _, cairo_context, layout = _testutil_simple_text(
            text=test_case.input_text,
            family_name=self._FAMILY_NAME,
            font_size=self._FAMILY_SIZE,
            height=self._HEIGHT,
            width=self._WIDTH,
        )
        text_bounding_box_extractor = TextBoundingBoxExtractor()

        result = text_bounding_box_extractor.extract_bounding_boxes(
            pango_layout=layout,
            matrix=cairo_context.get_matrix(),
            include_text=test_case.include_text,
            levels=self._LEVELS,
        )

        assert result.char_bboxes is None
        assert result.cluster_bboxes is None
        assert result.run_bboxes is None
        assert result.line_bboxes is not None
        assert result.layout_bbox is None

        assert len(result.line_bboxes) == len(test_case.expected_lines)

        _testutil_assert_no_logical_bbox_overlap(result.line_bboxes)
        _testutil_assert_no_ink_bbox_overlap(result.line_bboxes)

        if test_case.include_text:
            # Pango excludes '\n' bytes from each line's text and byte_length,
            # so joining all lines reconstructs the input without newlines.
            assert "".join(lb.text for lb in result.line_bboxes if lb.text is not None) == test_case.input_text.replace(
                "\n", ""
            )

        for line_bbox, expected in zip(result.line_bboxes, test_case.expected_lines, strict=True):
            assert line_bbox.text == expected.text
            assert line_bbox.byte_index == expected.byte_index
            assert line_bbox.byte_length == expected.byte_length
            assert line_bbox.resolved_direction == expected.resolved_direction
            assert line_bbox.is_paragraph_start == expected.is_paragraph_start
