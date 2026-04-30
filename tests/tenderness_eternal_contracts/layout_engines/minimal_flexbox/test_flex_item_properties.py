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

from tenderness.layout_engines.minimal_flexbox.flex_item_properties import AlignSelf, FlexItemProperties
from tests._test_utils.dataclass_test import DataclassTestBase, DataclassTestConfig
from tests._test_utils.enum_test import EnumTestBase, EnumTestConfig

# --------------------------
# Eternal contract tests for AlignSelf
# --------------------------
ALIGN_SELF_EXPECTED_MEMBERS = {"AUTO", "STRETCH", "FLEX_START", "FLEX_END", "CENTER"}
ALIGN_SELF_TEST_ENUM_CONFIG = [
    EnumTestConfig(
        enum_class=AlignSelf,
        expected_members=ALIGN_SELF_EXPECTED_MEMBERS,
    )
]


@pytest.mark.parametrize("config", ALIGN_SELF_TEST_ENUM_CONFIG, ids=lambda c: c.enum_class.__name__)
class TestAlignSelfEternalContract(EnumTestBase):
    pass


# --------------------------
# Eternal contract tests for FlexItemProperties
# --------------------------
FLEX_ITEM_PROPERTIES_EXPECTED_FIELDS = {"order", "flex_grow", "flex_shrink", "flex_basis", "align_self"}
FLEX_ITEM_PROPERTIES_TEST_DATACLASS_CONFIG = [
    DataclassTestConfig(
        dataclass_class=FlexItemProperties,
        has_slots=True,
        expected_fields=FLEX_ITEM_PROPERTIES_EXPECTED_FIELDS,
    )
]


@pytest.mark.parametrize("config", FLEX_ITEM_PROPERTIES_TEST_DATACLASS_CONFIG, ids=lambda c: c.dataclass_class.__name__)
class TestFlexItemPropertiesEternalContract(DataclassTestBase):
    pass
