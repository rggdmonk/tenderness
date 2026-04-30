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

from tenderness.pango_backend.layout_context_interface import (
    LayoutContextInterface,
    LayoutContextInterfaceParameters,
)
from tests._test_utils.class_test import ClassTestBase, ClassTestConfig
from tests._test_utils.dataclass_test import DataclassTestBase, DataclassTestConfig

# --------------------------
# Tests for LayoutContextInterfaceParameters
# --------------------------
LAYOUT_CONTEXT_INTERFACE_PARAMETERS_EXPECTED_FIELDS = {
    "_COERCE_DISPATCH",
    "base_dir",
    "base_gravity",
    "font_description",
    "font_map",
    "gravity_hint",
    "language",
    "matrix",
    "round_glyph_positions",
}
LAYOUT_CONTEXT_INTERFACE_PARAMETERS_TEST_DATACLASS_CONFIG = [
    DataclassTestConfig(
        dataclass_class=LayoutContextInterfaceParameters,
        has_slots=True,
        is_frozen=True,
        expected_fields=LAYOUT_CONTEXT_INTERFACE_PARAMETERS_EXPECTED_FIELDS,
        expected_methods={"__post_init__"},
    )
]


@pytest.mark.parametrize(
    "config", LAYOUT_CONTEXT_INTERFACE_PARAMETERS_TEST_DATACLASS_CONFIG, ids=lambda c: c.dataclass_class.__name__
)
class TestLayoutContextInterfaceParametersContract(DataclassTestBase):
    pass


# --------------------------
# Tests for LayoutContextInterface
# --------------------------
LAYOUT_CONTEXT_INTERFACE_EXPECTED_PROPERTIES = {
    "serial",
    "base_dir",
    "base_gravity",
    "font_description",
    "font_map",
    "gravity",
    "gravity_hint",
    "language",
    "matrix",
    "round_glyph_positions",
}
LAYOUT_CONTEXT_INTERFACE_EXPECTED_METHODS = {
    "changed",
    "get_metrics",
    "list_families",
    "load_font",
    "load_fontset",
}
LAYOUT_CONTEXT_INTERFACE_EXPECTED_CLASS_METHODS = {"from_layout_interface", "from_pango_layout"}
LAYOUT_CONTEXT_INTERFACE_EXPECTED_CLASS_CLASS_VARS = {"PANGO_SCALE", "_SETTER_DISPATCH"}

LAYOUT_CONTEXT_INTERFACE_TEST_CLASS_CONFIG = [
    ClassTestConfig(
        cls=LayoutContextInterface,
        expected_class_vars=LAYOUT_CONTEXT_INTERFACE_EXPECTED_CLASS_CLASS_VARS,
        expected_properties=LAYOUT_CONTEXT_INTERFACE_EXPECTED_PROPERTIES,
        expected_methods=LAYOUT_CONTEXT_INTERFACE_EXPECTED_METHODS,
        expected_class_methods=LAYOUT_CONTEXT_INTERFACE_EXPECTED_CLASS_METHODS,
    ),
]


@pytest.mark.parametrize("config", LAYOUT_CONTEXT_INTERFACE_TEST_CLASS_CONFIG, ids=lambda c: c.cls.__name__)
class TestLayoutContextInterfaceContract(ClassTestBase):
    pass
