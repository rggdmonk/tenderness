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
    BoundingBoxStrategy,
    BoundingBoxType,
    BoundingBoxWithInk,
    CharBBox,
    ClusterBBox,
    LayoutBBox,
    LayoutBBoxCollection,
    LineBBox,
    RunBBox,
    Tetragon,
)
from tests._test_utils.dataclass_test import DataclassTestBase, DataclassTestConfig
from tests._test_utils.enum_test import EnumTestBase, EnumTestConfig

# --------------------------
# Tests for BoundingBoxType
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
# Tests for BoundingBoxStrategy
# --------------------------
BOUNDING_BOX_STRATEGY_EXPECTED_MEMBERS = {"ONLY_BOXES", "WITH_TEXT"}
BOUNDING_BOX_STRATEGY_TEST_ENUM_CONFIG = [
    EnumTestConfig(
        enum_class=BoundingBoxStrategy,
        expected_members=BOUNDING_BOX_STRATEGY_EXPECTED_MEMBERS,
    )
]


@pytest.mark.parametrize("config", BOUNDING_BOX_STRATEGY_TEST_ENUM_CONFIG, ids=lambda c: c.enum_class.__name__)
class TestBoundingBoxStrategyContract(EnumTestBase):
    pass


# --------------------------
# Tests for Tetragon
# --------------------------
TETRAGON_EXPECTED_FIELDS = {"top_left", "top_right", "bottom_right", "bottom_left"}
TETRAGON_TEST_DATACLASS_CONFIG = [
    DataclassTestConfig(
        dataclass_class=Tetragon,
        has_slots=True,
        expected_fields=TETRAGON_EXPECTED_FIELDS,
    )
]


@pytest.mark.parametrize("config", TETRAGON_TEST_DATACLASS_CONFIG, ids=lambda c: c.dataclass_class.__name__)
class TestTetragonContract(DataclassTestBase):
    pass


# --------------------------
# Tests for BoundingBox
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
# Tests for BoundingBoxWithInk
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
# Tests for CharBBox
# --------------------------
CHAR_BBOX_EXPECTED_FIELDS = {"char", "byte_index"}
CHAR_BBOX_TEST_DATACLASS_CONFIG = [
    DataclassTestConfig(
        dataclass_class=CharBBox,
        has_slots=True,
        expected_fields=CHAR_BBOX_EXPECTED_FIELDS,
    )
]


@pytest.mark.parametrize("config", CHAR_BBOX_TEST_DATACLASS_CONFIG, ids=lambda c: c.dataclass_class.__name__)
class TestCharBBoxContract(DataclassTestBase):
    pass


# --------------------------
# Tests for ClusterBBox
# --------------------------
CLUSTER_BBOX_EXPECTED_FIELDS = {"text", "byte_index"}
CLUSTER_BBOX_TEST_DATACLASS_CONFIG = [
    DataclassTestConfig(
        dataclass_class=ClusterBBox,
        has_slots=True,
        expected_fields=CLUSTER_BBOX_EXPECTED_FIELDS,
    )
]


@pytest.mark.parametrize("config", CLUSTER_BBOX_TEST_DATACLASS_CONFIG, ids=lambda c: c.dataclass_class.__name__)
class TestClusterBBoxContract(DataclassTestBase):
    pass


# --------------------------
# Tests for RunBBox
# --------------------------
RUN_BBOX_EXPECTED_FIELDS = {"text", "byte_start", "byte_length", "baseline"}
RUN_BBOX_TEST_DATACLASS_CONFIG = [
    DataclassTestConfig(
        dataclass_class=RunBBox,
        has_slots=True,
        expected_fields=RUN_BBOX_EXPECTED_FIELDS,
    )
]


@pytest.mark.parametrize("config", RUN_BBOX_TEST_DATACLASS_CONFIG, ids=lambda c: c.dataclass_class.__name__)
class TestRunBBoxContract(DataclassTestBase):
    pass


# --------------------------
# Tests for LineBBox
# --------------------------
LINE_BBOX_EXPECTED_FIELDS = {
    "text",
    "byte_start",
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
    )
]


@pytest.mark.parametrize("config", LINE_BBOX_TEST_DATACLASS_CONFIG, ids=lambda c: c.dataclass_class.__name__)
class TestLineBBoxContract(DataclassTestBase):
    pass


# --------------------------
# Tests for LayoutBBox
# --------------------------
LAYOUT_BBOX_EXPECTED_FIELDS = {"text"}
LAYOUT_BBOX_TEST_DATACLASS_CONFIG = [
    DataclassTestConfig(
        dataclass_class=LayoutBBox,
        has_slots=True,
        expected_fields=LAYOUT_BBOX_EXPECTED_FIELDS,
    )
]


@pytest.mark.parametrize("config", LAYOUT_BBOX_TEST_DATACLASS_CONFIG, ids=lambda c: c.dataclass_class.__name__)
class TestLayoutBBoxContract(DataclassTestBase):
    pass


# --------------------------
# Tests for LayoutBBoxCollection
# --------------------------
LAYOUT_BBOX_COLLECTION_EXPECTED_FIELDS = {
    "char_boxes",
    "cluster_boxes",
    "run_boxes",
    "line_boxes",
    "layout_box",
    "position_name",
    "block_name",
    "table_name",
    "cell_name",
}
LAYOUT_BBOX_COLLECTION_TEST_DATACLASS_CONFIG = [
    DataclassTestConfig(
        dataclass_class=LayoutBBoxCollection,
        has_slots=True,
        expected_fields=LAYOUT_BBOX_COLLECTION_EXPECTED_FIELDS,
    )
]


@pytest.mark.parametrize(
    "config", LAYOUT_BBOX_COLLECTION_TEST_DATACLASS_CONFIG, ids=lambda c: c.dataclass_class.__name__
)
class TestLayoutBBoxCollectionContract(DataclassTestBase):
    pass
