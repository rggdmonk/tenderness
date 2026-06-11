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

from tenderness.bounding_boxes.bounding_boxes_schema import CharBBox, Quadrilateral


@dataclass(frozen=True, slots=True)
class CharBBoxTestCase:
    test_name: str
    text: str | None
    byte_index: int
    byte_length: int


CHAR_BBOX_TEST_CASES: tuple[CharBBoxTestCase, ...] = (
    CharBBoxTestCase(test_name="dummy_latin_char", text="A", byte_index=0, byte_length=1),
    CharBBoxTestCase(test_name="dummy_cyrillic_char", text="Ж", byte_index=1, byte_length=2),
    CharBBoxTestCase(test_name="dummy_greek_char", text="Ω", byte_index=3, byte_length=2),
    CharBBoxTestCase(test_name="dummy_arabic_char", text="م", byte_index=5, byte_length=2),
    CharBBoxTestCase(test_name="dummy_missing_char", text=None, byte_index=7, byte_length=1),
)


class TestCharBBox:
    @pytest.mark.parametrize(
        "test_case",
        CHAR_BBOX_TEST_CASES,
        ids=lambda test_case: test_case.test_name,
    )
    def test_to_dict_serializes_char_box(
        self,
        test_case: CharBBoxTestCase,
        logical_bbox: Quadrilateral,
    ) -> None:
        box = CharBBox(
            logical_bbox=logical_bbox,
            text=test_case.text,
            byte_index=test_case.byte_index,
            byte_length=test_case.byte_length,
        )

        assert box.to_dict() == {
            "logical_bbox": logical_bbox.to_dict(),
            "text": test_case.text,
            "byte_index": test_case.byte_index,
            "byte_length": test_case.byte_length,
        }
