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

import numpy  # noqa: ICN001
import pytest

from tenderness.bounding_boxes.text_bounding_box_extractor import TextBoundingBoxExtractor


class TestTextBoundingBoxExtractorByteMapping:
    # ---------------------------------------------------------------------------
    # _build_byte_to_char_map
    # ---------------------------------------------------------------------------
    @pytest.mark.parametrize(
        ("text", "expected"),
        [
            pytest.param("", [0], id="empty"),
            pytest.param("abc", [0, 1, 2, 3], id="ascii_only"),
            pytest.param("é", [0, 0, 1], id="2byte"),
            pytest.param("中", [0, 0, 0, 1], id="3byte"),
            pytest.param("😀", [0, 0, 0, 0, 1], id="4byte"),
            pytest.param("aé", [0, 1, 1, 2], id="ascii_then_2byte"),
            pytest.param("éa", [0, 0, 1, 2], id="2byte_then_ascii"),
            pytest.param("a中😀", [0, 1, 1, 1, 2, 2, 2, 2, 3], id="mixed_all_widths"),
            pytest.param("中😀", [0, 0, 0, 1, 1, 1, 1, 2], id="3byte_then_4byte"),
            pytest.param("a\nb", [0, 1, 2, 3], id="newline"),
        ],
    )
    def test_build_byte_to_char_map(self, text: str, expected: list[int]) -> None:
        text_bounding_box_extractor = TextBoundingBoxExtractor()
        encoded = numpy.frombuffer(
            text.encode(encoding="utf-8", errors="strict"),
            dtype=numpy.uint8,
        )
        result = text_bounding_box_extractor._build_byte_to_char_map(
            encoded=encoded,
            n_chars=len(text),
        )
        numpy.testing.assert_array_equal(result, expected)

    # ---------------------------------------------------------------------------
    # _build_byte_lengths
    # ---------------------------------------------------------------------------
    @pytest.mark.parametrize(
        ("raw_bytes", "expected"),
        [
            pytest.param(b"", [], id="empty"),
            pytest.param(b"abc", [1, 1, 1], id="ascii_only"),
            pytest.param("é".encode(), [2, 1], id="2byte"),
            pytest.param("中".encode(), [3, 1, 1], id="3byte"),
            pytest.param("😀".encode(), [4, 1, 1, 1], id="4byte"),
            pytest.param("a中😀".encode(), [1, 3, 1, 1, 4, 1, 1, 1], id="mixed_all_widths"),
            # boundary edges for each lead-byte threshold
            pytest.param(bytes([0xBF]), [1], id="boundary_below_2byte"),
            pytest.param(bytes([0xC0]), [2], id="boundary_lowest_2byte"),
            pytest.param(bytes([0xDF]), [2], id="boundary_highest_2byte"),
            pytest.param(bytes([0xE0]), [3], id="boundary_lowest_3byte"),
            pytest.param(bytes([0xEF]), [3], id="boundary_highest_3byte"),
            pytest.param(bytes([0xF0]), [4], id="boundary_lowest_4byte"),
        ],
    )
    def test_build_byte_lengths(self, raw_bytes: bytes, expected: list[int]) -> None:
        encoded = numpy.frombuffer(raw_bytes, dtype=numpy.uint8)
        result = TextBoundingBoxExtractor()._build_byte_lengths(encoded=encoded)
        numpy.testing.assert_array_equal(result, expected)
