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

from tenderness.cairo_backend.font_options_interface import FontOptionsInterface, FontOptionsInterfaceParameters
from tests._test_utils.class_test import ClassTestBase, ClassTestConfig
from tests._test_utils.dataclass_test import DataclassTestBase, DataclassTestConfig

# --------------------------
# Tests for FontOptionsInterfaceParameters
# --------------------------
FONT_OPTIONS_INTERFACE_PARAMETERS_EXPECTED_FIELDS = {
    "_COERCE_DISPATCH",
    "antialias",
    "color_mode",
    "color_palette",
    "hint_metrics",
    "hint_style",
    "subpixel_order",
    "variations",
}
FONT_OPTIONS_INTERFACE_PARAMETERS_EXPECTED_METHODS = {"__post_init__"}

FONT_OPTIONS_INTERFACE_PARAMETERS_TEST_DATACLASS_CONFIG = [
    DataclassTestConfig(
        dataclass_class=FontOptionsInterfaceParameters,
        has_slots=True,
        is_frozen=True,
        expected_fields=FONT_OPTIONS_INTERFACE_PARAMETERS_EXPECTED_FIELDS,
        expected_methods=FONT_OPTIONS_INTERFACE_PARAMETERS_EXPECTED_METHODS,
    )
]


@pytest.mark.parametrize(
    "config", FONT_OPTIONS_INTERFACE_PARAMETERS_TEST_DATACLASS_CONFIG, ids=lambda c: c.dataclass_class.__name__
)
class TestFontOptionsInterfaceParametersContract(DataclassTestBase):
    pass


# --------------------------
# Tests for FontOptionsInterface
# --------------------------
FONT_OPTIONS_INTERFACE_EXPECTED_PROPERTIES = {
    "antialias",
    "hint_style",
    "hint_metrics",
    "subpixel_order",
    "variations",
    "color_mode",
    "color_palette",
    "hash",
}
FONT_OPTIONS_INTERFACE_EXPECTED_METHODS = {
    "copy",
    "equal",
    "merge",
    "get_custom_palette_color",
    "set_custom_palette_color",
    "apply_to_layout_interface",
}
FONT_OPTIONS_INTERFACE_EXPECTED_CLASS_METHODS = {
    "from_new",
}
FONT_OPTIONS_INTERFACE_EXPECTED_CLASS_VARS = {"_SETTER_DISPATCH"}

FONT_OPTIONS_INTERFACE_TEST_CLASS_CONFIG = [
    ClassTestConfig(
        cls=FontOptionsInterface,
        expected_class_vars=FONT_OPTIONS_INTERFACE_EXPECTED_CLASS_VARS,
        expected_properties=FONT_OPTIONS_INTERFACE_EXPECTED_PROPERTIES,
        expected_methods=FONT_OPTIONS_INTERFACE_EXPECTED_METHODS,
        expected_class_methods=FONT_OPTIONS_INTERFACE_EXPECTED_CLASS_METHODS,
    ),
]


@pytest.mark.parametrize("config", FONT_OPTIONS_INTERFACE_TEST_CLASS_CONFIG, ids=lambda c: c.cls.__name__)
class TestFontOptionsInterfaceContract(ClassTestBase):
    pass
