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

from tenderness.bounding_boxes.bounding_boxes_schema import ClusterBBox, Quadrilateral


@dataclass(frozen=True, slots=True)
class ClusterBBoxTestCase:
    test_name: str
    text: str | None
    byte_index: int
    byte_length: int


CLUSTER_BBOX_TEST_CASES: tuple[ClusterBBoxTestCase, ...] = (
    ClusterBBoxTestCase(test_name="dummy_latin_cluster", text="Hello", byte_index=0, byte_length=5),
    ClusterBBoxTestCase(test_name="dummy_cyrillic_cluster", text="Привет", byte_index=5, byte_length=12),
    ClusterBBoxTestCase(test_name="dummy_greek_cluster", text="Γεια", byte_index=17, byte_length=8),
    ClusterBBoxTestCase(test_name="dummy_arabic_cluster", text="مرحبا", byte_index=25, byte_length=10),
    ClusterBBoxTestCase(test_name="dummy_missing_cluster_text", text=None, byte_index=35, byte_length=0),
)


class TestClusterBBox:
    @pytest.mark.parametrize(
        "test_case",
        CLUSTER_BBOX_TEST_CASES,
        ids=lambda test_case: test_case.test_name,
    )
    def test_to_dict_serializes_cluster_box(
        self,
        test_case: ClusterBBoxTestCase,
        logical_bbox: Quadrilateral,
        ink_bbox: Quadrilateral,
    ) -> None:
        box = ClusterBBox(
            logical_bbox=logical_bbox,
            ink_bbox=ink_bbox,
            text=test_case.text,
            byte_index=test_case.byte_index,
            byte_length=test_case.byte_length,
        )

        assert box.to_dict() == {
            "logical_bbox": logical_bbox.to_dict(),
            "ink_bbox": ink_bbox.to_dict(),
            "text": test_case.text,
            "byte_index": test_case.byte_index,
            "byte_length": test_case.byte_length,
        }
