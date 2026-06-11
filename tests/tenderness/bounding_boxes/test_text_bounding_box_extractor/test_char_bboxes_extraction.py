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
class CharBBoxExtractionTestCase:
    test_name: str
    input_text: str

    include_text: bool

    expected_chars: list[str]
    expected_byte_indexes: list[int]
    expected_byte_lengths: list[int | None]


CHAR_BBOX_EXTRACTION_TEST_CASES: list[CharBBoxExtractionTestCase] = [
    CharBBoxExtractionTestCase(
        test_name="latin_only",
        input_text="abc",
        include_text=True,
        expected_chars=["a", "b", "c"],
        expected_byte_indexes=[0, 1, 2],
        expected_byte_lengths=[1, 1, 1],
    ),
    CharBBoxExtractionTestCase(
        test_name="newline_multiline",
        input_text="hello\nworld",
        include_text=True,
        expected_chars=["h", "e", "l", "l", "o", "\n", "w", "o", "r", "l", "d"],
        expected_byte_indexes=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        expected_byte_lengths=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ),
    CharBBoxExtractionTestCase(
        test_name="2byte_greek",
        input_text="αβγ",
        include_text=True,
        expected_chars=["α", "β", "γ"],  # noqa: RUF001
        expected_byte_indexes=[0, 2, 4],
        expected_byte_lengths=[2, 2, 2],
    ),
    CharBBoxExtractionTestCase(
        test_name="3byte_japanese",
        input_text="日本語",
        include_text=True,
        expected_chars=["日", "本", "語"],
        expected_byte_indexes=[0, 3, 6],
        expected_byte_lengths=[3, 3, 3],
    ),
    CharBBoxExtractionTestCase(
        test_name="4byte_multi_emoji",
        input_text="😀🎉",
        include_text=True,
        expected_chars=["😀", "🎉"],
        expected_byte_indexes=[0, 4],
        expected_byte_lengths=[4, 4],
    ),
    # NFD "café": e + U+0301 combining acute = 5 code points; Pango iterates each separately
    CharBBoxExtractionTestCase(
        test_name="latin_with_accent_cafe_nfd",
        input_text="café",
        include_text=True,
        expected_chars=["c", "a", "f", "e", "́"],
        expected_byte_indexes=[0, 1, 2, 3, 4],
        expected_byte_lengths=[1, 1, 1, 1, 2],
    ),
    # 🐻‍❄️ is a ZWJ sequence: 🐻(4) + ZWJ(3) + ❄(3) + VS-16(3) = 13 bytes, 4 code points
    # Pango iterates each code point separately, not as a single grapheme cluster
    CharBBoxExtractionTestCase(
        test_name="zwj_emoji_cafe",
        input_text="🐻‍❄️ café",
        include_text=True,
        expected_chars=["🐻", "‍", "❄", "️", " ", "c", "a", "f", "é"],
        expected_byte_indexes=[0, 4, 7, 10, 13, 14, 15, 16, 17],
        expected_byte_lengths=[4, 3, 3, 3, 1, 1, 1, 1, 2],
    ),
    # Arabic is RTL (same visual iteration pattern as Hebrew):
    # "marhaba" logical order: m(0) r(2) h(4) b(6) a(8), visual left-to-right: a b h r m
    CharBBoxExtractionTestCase(
        test_name="arabic_rtl",
        input_text="مرحبا",
        include_text=True,
        expected_chars=["ا", "ب", "ح", "ر", "م"],  # noqa: RUF001
        expected_byte_indexes=[8, 6, 4, 2, 0],
        expected_byte_lengths=[2, 2, 2, 2, 2],
    ),
    # Hebrew is RTL — Pango iterates in visual order, so Hebrew chars come out reversed:
    # "shalom" visually left-to-right on screen is mem-vav-lamed-shin, hence byte_indexes go 26, 24, 22, 20
    CharBBoxExtractionTestCase(
        test_name="zwj_emoji_hebrew",
        input_text="Hello 🐻‍❄️ שלום  ",
        include_text=True,
        expected_chars=["H", "e", "l", "l", "o", " ", "🐻", "‍", "❄", "️", " ", "ם", "ו", "ל", "ש", " ", " "],  # noqa: RUF001
        expected_byte_indexes=[0, 1, 2, 3, 4, 5, 6, 10, 13, 16, 19, 26, 24, 22, 20, 28, 29],
        expected_byte_lengths=[1, 1, 1, 1, 1, 1, 4, 3, 3, 3, 1, 2, 2, 2, 2, 1, 1],
    ),
]


class TestTextBoundingBoxExtractorCharBBoxExtraction:
    _FAMILY_NAME: ClassVar[str] = "Noto Sans"
    _FAMILY_SIZE: ClassVar[int] = 24
    _HEIGHT: ClassVar[int] = 500
    _WIDTH: ClassVar[int] = 500
    _LEVELS: ClassVar[set[BoundingBoxType]] = set({BoundingBoxType.CHAR})

    @pytest.mark.usefixtures("unittests_font_setup")
    @pytest.mark.parametrize("test_case", CHAR_BBOX_EXTRACTION_TEST_CASES, ids=lambda tc: tc.test_name)
    def test_char_bbox_extraction(self, test_case: CharBBoxExtractionTestCase) -> None:

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

        assert result.char_bboxes is not None
        assert result.cluster_bboxes is None
        assert result.run_bboxes is None
        assert result.line_bboxes is None
        assert result.layout_bbox is None

        assert len(result.char_bboxes) == len(test_case.input_text)
        assert len(result.char_bboxes) == len(test_case.expected_chars)

        if test_case.include_text:
            # RTL chars come out in visual order, so sort by byte_index (logical order)
            # before joining — the result must equal the original input exactly.
            sorted_chars = sorted(result.char_bboxes, key=lambda cb: cb.byte_index)
            assert "".join(cb.text for cb in sorted_chars if cb.text is not None) == test_case.input_text

        for char_bbox, expected_char, expected_byte_index, expected_byte_length in zip(
            result.char_bboxes,
            test_case.expected_chars,
            test_case.expected_byte_indexes,
            test_case.expected_byte_lengths,
            strict=True,
        ):
            assert char_bbox.text == expected_char
            assert char_bbox.byte_index == expected_byte_index
            assert char_bbox.byte_length == expected_byte_length
