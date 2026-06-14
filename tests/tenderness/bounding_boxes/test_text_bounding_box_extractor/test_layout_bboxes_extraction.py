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

import pytest

from tenderness.bounding_boxes.bounding_boxes_schema import BoundingBoxType
from tenderness.bounding_boxes.text_bounding_box_extractor import TextBoundingBoxExtractor
from tests._test_utils.render_helpers import _testutil_simple_text


@dataclass(slots=True, frozen=True)
class LayoutBBoxExtractionTestCase:
    test_name: str
    input_text: str
    include_text: bool
    expected_text: str | None


LAYOUT_BBOX_EXTRACTION_TEST_CASES: list[LayoutBBoxExtractionTestCase] = [
    LayoutBBoxExtractionTestCase(
        test_name="latin_single_line",
        input_text="sphinx",
        include_text=True,
        expected_text="sphinx",
    ),
    LayoutBBoxExtractionTestCase(
        test_name="latin_multiline",
        input_text="one\ntwo\nthree",
        include_text=True,
        expected_text="one\ntwo\nthree",
    ),
    # 2-byte UTF-8: à(2) + é(2) + î(2) = 6 bytes
    LayoutBBoxExtractionTestCase(
        test_name="2byte_accented",
        input_text="àéî",
        include_text=True,
        expected_text="àéî",
    ),
    # 3-byte UTF-8: 한(3) + 국(3) + 어(3) = 9 bytes
    LayoutBBoxExtractionTestCase(
        test_name="3byte_korean",
        input_text="한국어",
        include_text=True,
        expected_text="한국어",
    ),
    # 4-byte UTF-8 emoji
    LayoutBBoxExtractionTestCase(
        test_name="4byte_emoji",
        input_text="🎸🎵",
        include_text=True,
        expected_text="🎸🎵",
    ),
    # '\r\n' is preserved verbatim — layout text is the full unmodified source string
    LayoutBBoxExtractionTestCase(
        test_name="crlf_multiline",
        input_text="red\r\nblue",
        include_text=True,
        expected_text="red\r\nblue",
    ),
    # '\r' is preserved verbatim — layout text is the full unmodified source string
    LayoutBBoxExtractionTestCase(
        test_name="cr_multiline",
        input_text="ef\rgh",
        include_text=True,
        expected_text="ef\rgh",
    ),
    # U+2029 (PARAGRAPH SEPARATOR) is preserved verbatim
    LayoutBBoxExtractionTestCase(
        test_name="ps_multiline",
        input_text="ef\u2029gh",
        include_text=True,
        expected_text="ef\u2029gh",
    ),
    # U+2028 (LINE SEPARATOR) is preserved verbatim
    LayoutBBoxExtractionTestCase(
        test_name="ls_multiline",
        input_text="ef\u2028gh",
        include_text=True,
        expected_text="ef\u2028gh",
    ),
    # Hebrew RTL — layout text is preserved in logical order regardless of direction
    LayoutBBoxExtractionTestCase(
        test_name="rtl_hebrew",
        input_text="שלום",
        include_text=True,
        expected_text="שלום",
    ),
    # include_text=False — text must be None
    LayoutBBoxExtractionTestCase(
        test_name="include_text_false",
        input_text="sphinx",
        include_text=False,
        expected_text=None,
    ),
]


class TestTextBoundingBoxExtractorLayoutBBoxExtraction:
    _FAMILY_NAME: ClassVar[str] = "Noto Sans"
    _FAMILY_SIZE: ClassVar[int] = 24
    _HEIGHT: ClassVar[int] = 500
    _WIDTH: ClassVar[int] = 500
    _LEVELS: ClassVar[set[BoundingBoxType]] = set({BoundingBoxType.LAYOUT})

    @pytest.mark.usefixtures("unittests_font_setup")
    @pytest.mark.parametrize("test_case", LAYOUT_BBOX_EXTRACTION_TEST_CASES, ids=lambda tc: tc.test_name)
    def test_layout_bbox_extraction(self, test_case: LayoutBBoxExtractionTestCase) -> None:

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
        assert result.line_bboxes is None
        assert result.layout_bbox is not None

        if test_case.include_text:
            # Layout text is the full source string unchanged — newlines and RTL included.
            assert result.layout_bbox.text == test_case.input_text

        assert result.layout_bbox.text == test_case.expected_text
