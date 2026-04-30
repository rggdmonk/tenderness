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

from tenderness.colors.color_selector import (
    Color,
    ColorGroup,
    ColorRegistry,
    ColorSelector,
)
from tests._test_utils.class_test import ClassTestBase, ClassTestConfig
from tests._test_utils.dataclass_test import DataclassTestBase, DataclassTestConfig

# --------------------------
# Tests for Color
# --------------------------
COLOR_EXPECTED_FIELDS = {"color_name", "color_group_name", "hex", "rgb", "rgba"}
COLOR_EXPECTED_CLASS_METHODS = {"from_hex"}
COLOR_TEST_DATACLASS_CONFIG = [
    DataclassTestConfig(
        dataclass_class=Color,
        has_slots=True,
        is_frozen=True,
        expected_fields=COLOR_EXPECTED_FIELDS,
        expected_class_methods=COLOR_EXPECTED_CLASS_METHODS,
    )
]


@pytest.mark.parametrize("config", COLOR_TEST_DATACLASS_CONFIG, ids=lambda c: c.dataclass_class.__name__)
class TestColorContract(DataclassTestBase):
    pass


# --------------------------
# Tests for ColorGroup
# --------------------------
COLOR_GROUP_EXPECTED_METHODS = {"get_color_by_name", "all_names"}
COLOR_GROUP_TEST_CLASS_CONFIG = [
    ClassTestConfig(
        cls=ColorGroup,
        expected_methods=COLOR_GROUP_EXPECTED_METHODS,
    )
]


@pytest.mark.parametrize("config", COLOR_GROUP_TEST_CLASS_CONFIG, ids=lambda c: c.cls.__name__)
class TestColorGroupContract(ClassTestBase):
    pass


# --------------------------
# Tests for ColorRegistry
# --------------------------
COLOR_REGISTRY_EXPECTED_METHODS = {"group_names", "get_group", "get_color", "total_colors"}
COLOR_REGISTRY_EXPECTED_CLASS_VARS = {"_BUILTIN_SOURCES"}  # no class vars expected on ColorRegistry
COLOR_REGISTRY_TEST_CLASS_CONFIG = [
    ClassTestConfig(
        cls=ColorRegistry,
        expected_class_vars=COLOR_REGISTRY_EXPECTED_CLASS_VARS,
        expected_methods=COLOR_REGISTRY_EXPECTED_METHODS,
    )
]


@pytest.mark.parametrize("config", COLOR_REGISTRY_TEST_CLASS_CONFIG, ids=lambda c: c.cls.__name__)
class TestColorRegistryContract(ClassTestBase):
    pass


# --------------------------
# Tests for ColorSelector
# --------------------------
COLOR_SELECTOR_EXPECTED_METHODS = {"by_names", "randomly"}
COLOR_SELECTOR_TEST_CLASS_CONFIG = [
    ClassTestConfig(
        cls=ColorSelector,
        expected_methods=COLOR_SELECTOR_EXPECTED_METHODS,
    )
]


@pytest.mark.parametrize("config", COLOR_SELECTOR_TEST_CLASS_CONFIG, ids=lambda c: c.cls.__name__)
class TestColorSelectorContract(ClassTestBase):
    pass
