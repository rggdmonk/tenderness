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

from tenderness.bounding_boxes.bounding_boxes_schema import Quadrilateral


@dataclass(frozen=True, slots=True)
class QuadrilateralToDictTestCase:
    test_name: str
    quadrilateral: Quadrilateral
    expected_dict: dict[str, list[float]]


QUADRILATERAL_TO_DICT_TEST_CASES: tuple[QuadrilateralToDictTestCase, ...] = (
    QuadrilateralToDictTestCase(
        test_name="origin aligned quadrilateral",
        quadrilateral=Quadrilateral(
            top_left=(0.0, 0.0),
            top_right=(10.0, 0.0),
            bottom_right=(10.0, 4.0),
            bottom_left=(0.0, 4.0),
        ),
        expected_dict={
            "top_left": [0.0, 0.0],
            "top_right": [10.0, 0.0],
            "bottom_right": [10.0, 4.0],
            "bottom_left": [0.0, 4.0],
        },
    ),
    QuadrilateralToDictTestCase(
        test_name="fractional quadrilateral",
        quadrilateral=Quadrilateral(
            top_left=(1.25, 2.5),
            top_right=(6.75, 2.5),
            bottom_right=(6.75, 7.125),
            bottom_left=(1.25, 7.125),
        ),
        expected_dict={
            "top_left": [1.25, 2.5],
            "top_right": [6.75, 2.5],
            "bottom_right": [6.75, 7.125],
            "bottom_left": [1.25, 7.125],
        },
    ),
)


class TestQuadrilateral:
    @pytest.mark.parametrize(
        "test_case",
        QUADRILATERAL_TO_DICT_TEST_CASES,
        ids=lambda test_case: test_case.test_name,
    )
    def test_to_dict_converts_corner_tuples_to_lists(self, test_case: QuadrilateralToDictTestCase) -> None:
        assert test_case.quadrilateral.to_dict() == test_case.expected_dict
