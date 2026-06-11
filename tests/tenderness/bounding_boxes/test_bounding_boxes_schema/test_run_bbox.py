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

from tenderness.bounding_boxes.bounding_boxes_schema import Quadrilateral, RunBBox


@dataclass(frozen=True, slots=True)
class RunBBoxTestCase:
    test_name: str
    text: str | None
    byte_index: int
    byte_length: int
    baseline: float


RUN_BBOX_TEST_CASES: tuple[RunBBoxTestCase, ...] = (
    RunBBoxTestCase(test_name="dummy_latin_run", text="Hello", byte_index=0, byte_length=5, baseline=11.5),
    RunBBoxTestCase(test_name="dummy_cyrillic_run", text="Привет", byte_index=5, byte_length=12, baseline=14.0),
    RunBBoxTestCase(test_name="dummy_greek_run", text="Γεια", byte_index=17, byte_length=8, baseline=16.25),
    RunBBoxTestCase(test_name="dummy_arabic_run", text="مرحبا", byte_index=25, byte_length=10, baseline=18.75),
    RunBBoxTestCase(test_name="dummy_missing_run_text", text=None, byte_index=35, byte_length=0, baseline=20.0),
)


class TestRunBBox:
    @pytest.mark.parametrize(
        "test_case",
        RUN_BBOX_TEST_CASES,
        ids=lambda test_case: test_case.test_name,
    )
    def test_to_dict_serializes_run_box(
        self,
        test_case: RunBBoxTestCase,
        logical_bbox: Quadrilateral,
        ink_bbox: Quadrilateral,
    ) -> None:
        box = RunBBox(
            logical_bbox=logical_bbox,
            ink_bbox=ink_bbox,
            text=test_case.text,
            byte_index=test_case.byte_index,
            byte_length=test_case.byte_length,
            baseline=test_case.baseline,
        )

        assert box.to_dict() == {
            "logical_bbox": logical_bbox.to_dict(),
            "ink_bbox": ink_bbox.to_dict(),
            "text": test_case.text,
            "byte_index": test_case.byte_index,
            "byte_length": test_case.byte_length,
            "baseline": test_case.baseline,
        }
