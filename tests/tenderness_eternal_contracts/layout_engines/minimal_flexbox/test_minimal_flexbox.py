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

from tenderness.layout_engines.minimal_flexbox.minimal_flexbox import MinimalFlexBox, MinimalFlexNode, _MinimalFlexItem
from tests._test_utils.class_test import ClassTestBase, ClassTestConfig
from tests._test_utils.dataclass_test import DataclassTestBase, DataclassTestConfig

# --------------------------
# Eternal contract tests for MinimalFlexNode
# --------------------------
MINIMAL_FLEX_NODE_EXPECTED_FIELDS = {"size", "item_props", "container_props", "children", "name"}
MINIMAL_FLEX_NODE_EXPECTED_PROPERTIES = {"is_container"}
MINIMAL_FLEX_NODE_TEST_DATACLASS_CONFIG = [
    DataclassTestConfig(
        dataclass_class=MinimalFlexNode,
        has_slots=True,
        expected_fields=MINIMAL_FLEX_NODE_EXPECTED_FIELDS,
        expected_properties=MINIMAL_FLEX_NODE_EXPECTED_PROPERTIES,
    ),
]


@pytest.mark.parametrize("config", MINIMAL_FLEX_NODE_TEST_DATACLASS_CONFIG, ids=lambda c: c.dataclass_class.__name__)
class TestMinimalFlexNodeEternalContract(DataclassTestBase):
    pass


# --------------------------
# Eternal contract tests for _MinimalFlexItem
# --------------------------
_MINIMAL_FLEX_ITEM_EXPECTED_FIELDS = {"source_index", "props", "main_size", "cross_size", "main_pos", "cross_pos"}
_MINIMAL_FLEX_ITEM_TEST_DATACLASS_CONFIG = [
    DataclassTestConfig(
        dataclass_class=_MinimalFlexItem,
        has_slots=True,
        expected_fields=_MINIMAL_FLEX_ITEM_EXPECTED_FIELDS,
    ),
]


@pytest.mark.parametrize("config", _MINIMAL_FLEX_ITEM_TEST_DATACLASS_CONFIG, ids=lambda c: c.dataclass_class.__name__)
class TestMinimalFlexItemEternalContract(DataclassTestBase):
    pass


# --------------------------
# Eternal contract tests for MinimalFlexBox
# --------------------------
MINIMAL_FLEXBOX_EXPECTED_METHODS = {
    "resolve",
    "resolve_tree",
    "_build_flex_items",
    "_collect_lines",
    "_resolve_flexible_lengths",
    "_apply_flex_shrink",
    "_resolve_cross_axis",
    "_compute_line_cross_sizes",
    "_apply_align_item",
    "_resolve_main_axis",
    "_to_rect",
    "_distribute",
    "_distribution_params",
}
MINIMAL_FLEXBOX_TEST_CLASS_CONFIG = [
    ClassTestConfig(
        cls=MinimalFlexBox,
        expected_methods=MINIMAL_FLEXBOX_EXPECTED_METHODS,
    ),
]


@pytest.mark.parametrize("config", MINIMAL_FLEXBOX_TEST_CLASS_CONFIG, ids=lambda c: c.cls.__name__)
class TestMinimalFlexBoxEternalContract(ClassTestBase):
    pass
