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

from tenderness.bounding_boxes.bounding_boxes_schema import LayoutBBox, Quadrilateral


@dataclass(frozen=True, slots=True)
class LayoutBBoxTestCase:
    test_name: str
    text: str | None


LAYOUT_BBOX_TEST_CASES: tuple[LayoutBBoxTestCase, ...] = (
    LayoutBBoxTestCase(test_name="dummy_latin_layout", text="Hello world"),
    LayoutBBoxTestCase(test_name="dummy_cyrillic_layout", text="Привет мир"),
    LayoutBBoxTestCase(test_name="dummy_greek_layout", text="Γεια σου κόσμε"),  # noqa: RUF001
    LayoutBBoxTestCase(test_name="dummy_arabic_layout", text="مرحبا بالعالم"),
    LayoutBBoxTestCase(test_name="dummy_mixed_layout", text="Hello Привет Γεια مرحبا"),
    LayoutBBoxTestCase(test_name="dummy_missing_layout_text", text=None),
)


class TestLayoutBBox:
    @pytest.mark.parametrize(
        "test_case",
        LAYOUT_BBOX_TEST_CASES,
        ids=lambda test_case: test_case.test_name,
    )
    def test_to_dict_serializes_layout_box(
        self,
        test_case: LayoutBBoxTestCase,
        logical_bbox: Quadrilateral,
        ink_bbox: Quadrilateral,
    ) -> None:
        box = LayoutBBox(logical_bbox=logical_bbox, ink_bbox=ink_bbox, text=test_case.text)

        assert box.to_dict() == {
            "logical_bbox": logical_bbox.to_dict(),
            "ink_bbox": ink_bbox.to_dict(),
            "text": test_case.text,
        }
