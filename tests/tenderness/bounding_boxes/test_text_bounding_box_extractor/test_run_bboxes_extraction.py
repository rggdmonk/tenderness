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

import math
from dataclasses import dataclass
from typing import ClassVar

import pytest

from tenderness.bounding_boxes.bounding_boxes_schema import BoundingBoxType
from tenderness.bounding_boxes.text_bounding_box_extractor import TextBoundingBoxExtractor
from tests._test_utils.render_helpers import (
    _testutil_assert_no_ink_bbox_overlap,
    _testutil_assert_no_logical_bbox_overlap,
    _testutil_simple_text,
)


@dataclass(slots=True, frozen=True)
class ExpectedRunBBox:
    text: str | None
    byte_index: int
    byte_length: int
    # baseline is excluded — its value depends on font metrics and cannot be hardcoded.


@dataclass(slots=True, frozen=True)
class RunBBoxExtractionTestCase:
    test_name: str
    input_text: str
    include_text: bool
    expected_runs: list[ExpectedRunBBox]


RUN_BBOX_EXTRACTION_TEST_CASES: list[RunBBoxExtractionTestCase] = [
    # Single script, single line — one run covering the full text.
    RunBBoxExtractionTestCase(
        test_name="latin_single_run",
        input_text="dog",
        include_text=True,
        expected_runs=[
            ExpectedRunBBox(text="dog", byte_index=0, byte_length=3),
        ],
    ),
    # Two paragraphs — '\n' is excluded (NULL sentinel run), each paragraph yields one run.
    RunBBoxExtractionTestCase(
        test_name="latin_two_paragraphs",
        input_text="cat\nbat",
        include_text=True,
        expected_runs=[
            ExpectedRunBBox(text="cat", byte_index=0, byte_length=3),
            ExpectedRunBBox(text="bat", byte_index=4, byte_length=3),
        ],
    ),
    # '\r\n' excluded (both bytes are NULL sentinel run); gap is 2 bytes.
    # "jet\r\nsky": jet=0-2, \r=3(skipped), \n=4(skipped), sky starts at byte 5
    RunBBoxExtractionTestCase(
        test_name="crlf_two_paragraphs",
        input_text="jet\r\nsky",
        include_text=True,
        expected_runs=[
            ExpectedRunBBox(text="jet", byte_index=0, byte_length=3),
            ExpectedRunBBox(text="sky", byte_index=5, byte_length=3),
        ],
    ),
    # Arabic RTL single line — one RTL run covering the full text.
    # "شمس" (sun): ش(2) + م(2) + س(2) = 6 bytes
    RunBBoxExtractionTestCase(
        test_name="arabic_rtl_single_run",
        input_text="شمس",
        include_text=True,
        expected_runs=[
            ExpectedRunBBox(text="شمس", byte_index=0, byte_length=6),
        ],
    ),
    # LTR paragraph then RTL paragraph — two runs, direction changes across the '\n'.
    # "go\nشمس": go(2) + \n(1, skipped) + شمس(6) starting at byte 3
    RunBBoxExtractionTestCase(
        test_name="ltr_then_rtl_paragraphs",
        input_text="go\nشمس",
        include_text=True,
        expected_runs=[
            ExpectedRunBBox(text="go", byte_index=0, byte_length=2),
            ExpectedRunBBox(text="شمس", byte_index=3, byte_length=6),
        ],
    ),
    # Mixed Latin + CJK on one line — Pango splits by script into two LTR runs.
    # "Hello " (Latin, 6 bytes) then "你好" (Han, 6 bytes); space attaches to the Latin run.
    RunBBoxExtractionTestCase(
        test_name="latin_and_cjk",
        input_text="Hello 你好",
        include_text=True,
        expected_runs=[
            ExpectedRunBBox(text="Hello ", byte_index=0, byte_length=6),
            ExpectedRunBBox(text="你好", byte_index=6, byte_length=6),
        ],
    ),
    # '\r' is a NULL sentinel run — excluded. Gap is +1 byte.
    # "ef\rgh": "ef"=0(len 2), \r=2(skipped), "gh"=3(len 2)
    RunBBoxExtractionTestCase(
        test_name="cr_two_paragraphs",
        input_text="ef\rgh",
        include_text=True,
        expected_runs=[
            ExpectedRunBBox(text="ef", byte_index=0, byte_length=2),
            ExpectedRunBBox(text="gh", byte_index=3, byte_length=2),
        ],
    ),
    # U+2029 (PARAGRAPH SEPARATOR, 3 UTF-8 bytes) is a NULL sentinel run — excluded. Gap is +3.
    # "ef\u2029gh": "ef"=0(len 2), PS=2-4(skipped), "gh"=5(len 2)
    RunBBoxExtractionTestCase(
        test_name="ps_two_paragraphs",
        input_text="ef\u2029gh",
        include_text=True,
        expected_runs=[
            ExpectedRunBBox(text="ef", byte_index=0, byte_length=2),
            ExpectedRunBBox(text="gh", byte_index=5, byte_length=2),
        ],
    ),
    # U+2028 (LINE SEPARATOR, 3 UTF-8 bytes) is a non-NULL run — included as its own run.
    # "ef\u2028gh": "ef"=0(len 2), LS=2(len 3), "gh"=5(len 2)
    RunBBoxExtractionTestCase(
        test_name="ls_creates_run",
        input_text="ef\u2028gh",
        include_text=True,
        expected_runs=[
            ExpectedRunBBox(text="ef", byte_index=0, byte_length=2),
            ExpectedRunBBox(text="\u2028", byte_index=2, byte_length=3),
            ExpectedRunBBox(text="gh", byte_index=5, byte_length=2),
        ],
    ),
    # Arabic RTL + \n\r: both breaks are NULL sentinel runs — excluded. Gap +2 bytes.
    # "بت جح": "بت"=0(len 4), \n=4+\r=5(skipped), "جح"=6(len 4)
    RunBBoxExtractionTestCase(
        test_name="rtl_lfcr",
        input_text="بت\n\rجح",
        include_text=True,
        expected_runs=[
            ExpectedRunBBox(text="بت", byte_index=0, byte_length=4),
            ExpectedRunBBox(text="جح", byte_index=6, byte_length=4),
        ],
    ),
    # Arabic RTL + U+2029 (PS, 3 bytes): NULL run — excluded. Gap +3.
    # "قل جح": "قل"=0(len 4), PS=4-6(skipped), "جح"=7(len 4)
    RunBBoxExtractionTestCase(
        test_name="rtl_ps",
        input_text="قل\u2029جح",
        include_text=True,
        expected_runs=[
            ExpectedRunBBox(text="قل", byte_index=0, byte_length=4),
            ExpectedRunBBox(text="جح", byte_index=7, byte_length=4),
        ],
    ),
    # Arabic RTL + U+2028 (LS, 3 bytes): non-NULL run — included as its own run.
    # In RTL, LS sits at the visual left of line 0, so it iterates first.
    # "بج حخ": LS=4(len 3), "بج"=0(len 4), "حخ"=7(len 4)
    RunBBoxExtractionTestCase(
        test_name="rtl_ls",
        input_text="بج\u2028حخ",
        include_text=True,
        expected_runs=[
            ExpectedRunBBox(text="\u2028", byte_index=4, byte_length=3),
            ExpectedRunBBox(text="بج", byte_index=0, byte_length=4),
            ExpectedRunBBox(text="حخ", byte_index=7, byte_length=4),
        ],
    ),
    RunBBoxExtractionTestCase(
        test_name="include_text_false",
        input_text="dog",
        include_text=False,
        expected_runs=[
            ExpectedRunBBox(text=None, byte_index=0, byte_length=3),
        ],
    ),
]


class TestTextBoundingBoxExtractorRunBBoxExtraction:
    _FAMILY_NAME: ClassVar[str] = "Noto Sans"
    _FAMILY_SIZE: ClassVar[int] = 24
    _HEIGHT: ClassVar[int] = 500
    _WIDTH: ClassVar[int] = 500
    _LEVELS: ClassVar[set[BoundingBoxType]] = set({BoundingBoxType.RUN})

    @pytest.mark.usefixtures("unittests_font_setup")
    @pytest.mark.parametrize("test_case", RUN_BBOX_EXTRACTION_TEST_CASES, ids=lambda tc: tc.test_name)
    def test_run_bbox_extraction(self, test_case: RunBBoxExtractionTestCase) -> None:

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
        assert result.run_bboxes is not None
        assert result.line_bboxes is None
        assert result.layout_bbox is None

        assert len(result.run_bboxes) == len(test_case.expected_runs)

        _testutil_assert_no_logical_bbox_overlap(result.run_bboxes)
        _testutil_assert_no_ink_bbox_overlap(result.run_bboxes)

        if test_case.include_text:
            # Runs skip NULL sentinel runs so '\n' is excluded.
            # Sort by byte_index to restore logical order before joining.
            sorted_runs = sorted(result.run_bboxes, key=lambda rb: rb.byte_index)
            assert "".join(rb.text for rb in sorted_runs if rb.text is not None) == test_case.input_text.replace(
                "\r\n", ""
            ).replace("\r", "").replace("\n", "").replace("\u2029", "")

        for run_bbox, expected in zip(result.run_bboxes, test_case.expected_runs, strict=True):
            assert run_bbox.text == expected.text
            assert run_bbox.byte_index == expected.byte_index
            assert run_bbox.byte_length == expected.byte_length
            assert math.isfinite(run_bbox.baseline)
