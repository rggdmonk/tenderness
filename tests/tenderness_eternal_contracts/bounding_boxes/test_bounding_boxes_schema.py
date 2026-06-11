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

import pytest

from tenderness.bounding_boxes.bounding_boxes_schema import (
    BoundingBox,
    BoundingBoxType,
    BoundingBoxWithInk,
    CharBBox,
    ClusterBBox,
    LayoutBBox,
    LineBBox,
    Quadrilateral,
    RunBBox,
    TextBoundingBoxes,
)
from tests._test_utils.dataclass_test import DataclassTestBase, DataclassTestConfig
from tests._test_utils.enum_test import EnumTestBase, EnumTestConfig

# --------------------------
# Eternal contract tests for BoundingBoxType
# --------------------------
BOUNDING_BOX_TYPE_EXPECTED_MEMBERS = {"CHAR", "CLUSTER", "LINE", "RUN", "LAYOUT"}
BOUNDING_BOX_TYPE_TEST_ENUM_CONFIG = [
    EnumTestConfig(
        enum_class=BoundingBoxType,
        expected_members=BOUNDING_BOX_TYPE_EXPECTED_MEMBERS,
    )
]


@pytest.mark.parametrize("config", BOUNDING_BOX_TYPE_TEST_ENUM_CONFIG, ids=lambda c: c.enum_class.__name__)
class TestBoundingBoxTypeContract(EnumTestBase):
    pass


# --------------------------
# Eternal contract tests for Quadrilateral
# --------------------------
QUADRILATERAL_EXPECTED_FIELDS = {"top_left", "top_right", "bottom_right", "bottom_left"}
QUADRILATERAL_TEST_DATACLASS_CONFIG = [
    DataclassTestConfig(
        dataclass_class=Quadrilateral,
        has_slots=True,
        expected_fields=QUADRILATERAL_EXPECTED_FIELDS,
        expected_methods={"to_dict"},
    )
]


@pytest.mark.parametrize("config", QUADRILATERAL_TEST_DATACLASS_CONFIG, ids=lambda c: c.dataclass_class.__name__)
class TestQuadrilateralContract(DataclassTestBase):
    pass


# --------------------------
# Eternal contract tests for BoundingBox
# --------------------------
BOUNDING_BOX_EXPECTED_FIELDS = {"logical_bbox"}
BOUNDING_BOX_TEST_DATACLASS_CONFIG = [
    DataclassTestConfig(
        dataclass_class=BoundingBox,
        has_slots=True,
        expected_fields=BOUNDING_BOX_EXPECTED_FIELDS,
    )
]


@pytest.mark.parametrize("config", BOUNDING_BOX_TEST_DATACLASS_CONFIG, ids=lambda c: c.dataclass_class.__name__)
class TestBoundingBoxContract(DataclassTestBase):
    pass


# --------------------------
# Eternal contract tests for BoundingBoxWithInk
# --------------------------
BOUNDING_BOX_WITH_INK_EXPECTED_FIELDS = {"ink_bbox"}
BOUNDING_BOX_WITH_INK_TEST_DATACLASS_CONFIG = [
    DataclassTestConfig(
        dataclass_class=BoundingBoxWithInk,
        has_slots=True,
        expected_fields=BOUNDING_BOX_WITH_INK_EXPECTED_FIELDS,
    )
]


@pytest.mark.parametrize(
    "config", BOUNDING_BOX_WITH_INK_TEST_DATACLASS_CONFIG, ids=lambda c: c.dataclass_class.__name__
)
class TestBoundingBoxWithInkContract(DataclassTestBase):
    pass


# --------------------------
# Eternal contract tests for CharBBox
# --------------------------
CHAR_BBOX_EXPECTED_FIELDS = {"text", "byte_index", "byte_length"}
CHAR_BBOX_TEST_DATACLASS_CONFIG = [
    DataclassTestConfig(
        dataclass_class=CharBBox,
        has_slots=True,
        expected_fields=CHAR_BBOX_EXPECTED_FIELDS,
        expected_methods={"to_dict"},
    )
]


@pytest.mark.parametrize("config", CHAR_BBOX_TEST_DATACLASS_CONFIG, ids=lambda c: c.dataclass_class.__name__)
class TestCharBBoxContract(DataclassTestBase):
    pass


# --------------------------
# Eternal contract tests for ClusterBBox
# --------------------------
CLUSTER_BBOX_EXPECTED_FIELDS = {"text", "byte_index", "byte_length"}
CLUSTER_BBOX_TEST_DATACLASS_CONFIG = [
    DataclassTestConfig(
        dataclass_class=ClusterBBox,
        has_slots=True,
        expected_fields=CLUSTER_BBOX_EXPECTED_FIELDS,
        expected_methods={"to_dict"},
    )
]


@pytest.mark.parametrize("config", CLUSTER_BBOX_TEST_DATACLASS_CONFIG, ids=lambda c: c.dataclass_class.__name__)
class TestClusterBBoxContract(DataclassTestBase):
    pass


# --------------------------
# Eternal contract tests for RunBBox
# --------------------------
RUN_BBOX_EXPECTED_FIELDS = {"text", "byte_index", "byte_length", "baseline"}
RUN_BBOX_TEST_DATACLASS_CONFIG = [
    DataclassTestConfig(
        dataclass_class=RunBBox,
        has_slots=True,
        expected_fields=RUN_BBOX_EXPECTED_FIELDS,
        expected_methods={"to_dict"},
    )
]


@pytest.mark.parametrize("config", RUN_BBOX_TEST_DATACLASS_CONFIG, ids=lambda c: c.dataclass_class.__name__)
class TestRunBBoxContract(DataclassTestBase):
    pass


# --------------------------
# Eternal contract tests for LineBBox
# --------------------------
LINE_BBOX_EXPECTED_FIELDS = {
    "text",
    "byte_index",
    "byte_length",
    "resolved_direction",
    "is_paragraph_start",
    "baseline",
}
LINE_BBOX_TEST_DATACLASS_CONFIG = [
    DataclassTestConfig(
        dataclass_class=LineBBox,
        has_slots=True,
        expected_fields=LINE_BBOX_EXPECTED_FIELDS,
        expected_methods={"to_dict"},
    )
]


@pytest.mark.parametrize("config", LINE_BBOX_TEST_DATACLASS_CONFIG, ids=lambda c: c.dataclass_class.__name__)
class TestLineBBoxContract(DataclassTestBase):
    pass


# --------------------------
# Eternal contract tests for LayoutBBox
# --------------------------
LAYOUT_BBOX_EXPECTED_FIELDS = {"text"}
LAYOUT_BBOX_TEST_DATACLASS_CONFIG = [
    DataclassTestConfig(
        dataclass_class=LayoutBBox,
        has_slots=True,
        expected_fields=LAYOUT_BBOX_EXPECTED_FIELDS,
        expected_methods={"to_dict"},
    )
]


@pytest.mark.parametrize("config", LAYOUT_BBOX_TEST_DATACLASS_CONFIG, ids=lambda c: c.dataclass_class.__name__)
class TestLayoutBBoxContract(DataclassTestBase):
    pass


# --------------------------
# Eternal contract tests for TextBoundingBoxes
# --------------------------
TEXT_BOUNDING_BOXES_EXPECTED_FIELDS = {"char_bboxes", "cluster_bboxes", "run_bboxes", "line_bboxes", "layout_bbox"}
TEXT_BOUNDING_BOXES_TEST_DATACLASS_CONFIG = [
    DataclassTestConfig(
        dataclass_class=TextBoundingBoxes,
        has_slots=True,
        expected_fields=TEXT_BOUNDING_BOXES_EXPECTED_FIELDS,
        expected_methods={"to_dict"},
    )
]


@pytest.mark.parametrize("config", TEXT_BOUNDING_BOXES_TEST_DATACLASS_CONFIG, ids=lambda c: c.dataclass_class.__name__)
class TestTextBoundingBoxesContract(DataclassTestBase):
    pass
