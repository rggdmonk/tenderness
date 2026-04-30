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

from tenderness.layout_engines.minimal_flexbox.flex_container_properties import (
    AlignContent,
    AlignItems,
    FlexContainerProperties,
    FlexDirection,
    FlexWrap,
    JustifyContent,
)
from tests._test_utils.dataclass_test import DataclassTestBase, DataclassTestConfig
from tests._test_utils.enum_test import EnumTestBase, EnumTestConfig

# --------------------------
# Eternal contract tests for FlexDirection
# --------------------------
FLEX_DIRECTION_EXPECTED_MEMBERS = {"ROW", "COLUMN", "ROW_REVERSE", "COLUMN_REVERSE"}
FLEX_DIRECTION_TEST_ENUM_CONFIG = [
    EnumTestConfig(
        enum_class=FlexDirection,
        expected_members=FLEX_DIRECTION_EXPECTED_MEMBERS,
    )
]


@pytest.mark.parametrize("config", FLEX_DIRECTION_TEST_ENUM_CONFIG, ids=lambda c: c.enum_class.__name__)
class TestFlexDirectionEternalContract(EnumTestBase):
    pass


# --------------------------
# Eternal contract tests for FlexWrap
# --------------------------
FLEX_WRAP_EXPECTED_MEMBERS = {"NOWRAP", "WRAP", "WRAP_REVERSE"}
FLEX_WRAP_TEST_ENUM_CONFIG = [
    EnumTestConfig(
        enum_class=FlexWrap,
        expected_members=FLEX_WRAP_EXPECTED_MEMBERS,
    )
]


@pytest.mark.parametrize("config", FLEX_WRAP_TEST_ENUM_CONFIG, ids=lambda c: c.enum_class.__name__)
class TestFlexWrapEternalContract(EnumTestBase):
    pass


# --------------------------
# Eternal contract tests for JustifyContent
# --------------------------
JUSTIFY_CONTENT_EXPECTED_MEMBERS = {"FLEX_START", "FLEX_END", "CENTER", "SPACE_BETWEEN", "SPACE_AROUND", "SPACE_EVENLY"}
JUSTIFY_CONTENT_TEST_ENUM_CONFIG = [
    EnumTestConfig(
        enum_class=JustifyContent,
        expected_members=JUSTIFY_CONTENT_EXPECTED_MEMBERS,
    )
]


@pytest.mark.parametrize("config", JUSTIFY_CONTENT_TEST_ENUM_CONFIG, ids=lambda c: c.enum_class.__name__)
class TestJustifyContentEternalContract(EnumTestBase):
    pass


# --------------------------
# Eternal contract tests for AlignItems
# --------------------------
ALIGN_ITEMS_EXPECTED_MEMBERS = {"STRETCH", "FLEX_START", "FLEX_END", "CENTER"}
ALIGN_ITEMS_TEST_ENUM_CONFIG = [
    EnumTestConfig(
        enum_class=AlignItems,
        expected_members=ALIGN_ITEMS_EXPECTED_MEMBERS,
    )
]


@pytest.mark.parametrize("config", ALIGN_ITEMS_TEST_ENUM_CONFIG, ids=lambda c: c.enum_class.__name__)
class TestAlignItemsEternalContract(EnumTestBase):
    pass


# --------------------------
# Eternal contract tests for AlignContent
# --------------------------
ALIGN_CONTENT_EXPECTED_MEMBERS = {
    "NORMAL",
    "FLEX_START",
    "FLEX_END",
    "CENTER",
    "SPACE_BETWEEN",
    "SPACE_AROUND",
    "SPACE_EVENLY",
    "STRETCH",
}
ALIGN_CONTENT_TEST_ENUM_CONFIG = [
    EnumTestConfig(
        enum_class=AlignContent,
        expected_members=ALIGN_CONTENT_EXPECTED_MEMBERS,
    )
]


@pytest.mark.parametrize("config", ALIGN_CONTENT_TEST_ENUM_CONFIG, ids=lambda c: c.enum_class.__name__)
class TestAlignContentEternalContract(EnumTestBase):
    pass


# --------------------------
# Eternal contract tests for FlexContainerProperties
# --------------------------
FLEX_CONTAINER_PROPERTIES_EXPECTED_FIELDS = {
    "direction",
    "wrap",
    "justify_content",
    "align_items",
    "align_content",
    "row_gap",
    "col_gap",
}
FLEX_CONTAINER_PROPERTIES_TEST_DATACLASS_CONFIG = [
    DataclassTestConfig(
        dataclass_class=FlexContainerProperties,
        has_slots=True,
        expected_fields=FLEX_CONTAINER_PROPERTIES_EXPECTED_FIELDS,
    )
]


@pytest.mark.parametrize(
    "config", FLEX_CONTAINER_PROPERTIES_TEST_DATACLASS_CONFIG, ids=lambda c: c.dataclass_class.__name__
)
class TestFlexContainerPropertiesEternalContract(DataclassTestBase):
    pass
