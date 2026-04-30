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

from tenderness.pango_backend.layout_interface import (
    LayoutInterface,
    LayoutInterfaceParameters,
    TextStrategy,
)
from tests._test_utils.class_test import ClassTestBase, ClassTestConfig
from tests._test_utils.dataclass_test import DataclassTestBase, DataclassTestConfig
from tests._test_utils.str_enum_test import StrEnumTestBase, StrEnumTestConfig

# --------------------------
# Tests for TextStrategy
# --------------------------
TEXT_STRATEGY_EXPECTED_MEMBERS = {"TEXT", "MARKUP"}
TEXT_STRATEGY_TEST_STR_ENUM_CONFIG = [
    StrEnumTestConfig(
        enum_class=TextStrategy,
        expected_members=TEXT_STRATEGY_EXPECTED_MEMBERS,
    )
]


@pytest.mark.parametrize("config", TEXT_STRATEGY_TEST_STR_ENUM_CONFIG, ids=lambda c: c.enum_class.__name__)
class TestTextStrategyContract(StrEnumTestBase):
    pass


# --------------------------
# Tests for LayoutInterfaceParameters
# --------------------------
LAYOUT_INTERFACE_PARAMETERS_EXPECTED_FIELDS = {
    "_CONFLICTING_PAIRS",
    "_COERCE_DISPATCH",
    "width",
    "width_device_units",
    "height",
    "height_device_units",
    "indent",
    "indent_device_units",
    "spacing",
    "spacing_device_units",
    "alignment",
    "attributes",
    "auto_dir",
    "ellipsize",
    "font_description",
    "justify",
    "justify_last_line",
    "line_spacing",
    "single_paragraph_mode",
    "tabs",
    "wrap",
}
LAYOUT_INTERFACE_PARAMETERS_TEST_DATACLASS_CONFIG = [
    DataclassTestConfig(
        dataclass_class=LayoutInterfaceParameters,
        has_slots=True,
        is_frozen=True,
        expected_fields=LAYOUT_INTERFACE_PARAMETERS_EXPECTED_FIELDS,
        expected_methods={"__post_init__", "_validate"},
    )
]


@pytest.mark.parametrize(
    "config", LAYOUT_INTERFACE_PARAMETERS_TEST_DATACLASS_CONFIG, ids=lambda c: c.dataclass_class.__name__
)
class TestLayoutInterfaceParametersContract(DataclassTestBase):
    pass


# --------------------------
# Tests for LayoutInterface
# --------------------------
_LAYOUT_INTERFACE_PARAMETERS_PROPERTY_FIELDS = LAYOUT_INTERFACE_PARAMETERS_EXPECTED_FIELDS - {
    "_COERCE_DISPATCH",
    "_CONFLICTING_PAIRS",
}
LAYOUT_INTERFACE_EXPECTED_PROPERTIES = _LAYOUT_INTERFACE_PARAMETERS_PROPERTY_FIELDS | {
    "baseline",
    "character_count",
    "extents",
    "extents_layout_rect",
    "extents_ink_layout_rect",
    "extents_logical_layout_rect",
    "is_ellipsized",
    "is_wrapped",
    "line_count",
    "pixel_extents",
    "pixel_extents_layout_rect",
    "pixel_extents_ink_layout_rect",
    "pixel_extents_logical_layout_rect",
    "pixel_size",
    "serial",
    "size",
    "text",
    "unknown_glyphs_count",
}
LAYOUT_INTERFACE_EXPECTED_METHODS = {
    "get_caret_pos",
    "get_context",
    "get_cursor_pos",
    "get_direction",
    "get_iter",
    "get_line",
    "get_line_readonly",
    "get_lines",
    "get_lines_readonly",
    "get_log_attrs",
    "get_log_attrs_readonly",
    "set_markup",
    "set_markup_with_accel",
    "set_text",
    "serialize_layout",
    "index_to_pos",
    "index_to_line_x",
    "xy_to_index",
    "copy",
    "move_cursor_visually",
    "write_to_file",
    "serialize",
    "context_changed",
    "add_text_to_layout",
    "get_layout_fit_report",
}
LAYOUT_INTERFACE_EXPECTED_CLASS_METHODS = {"from_cairo_context"}
LAYOUT_INTERFACE_EXPECTED_CLASS_VARS = {"_SETTER_DISPATCH", "PANGO_SCALE"}
LAYOUT_INTERFACE_TEST_CLASS_CONFIG = [
    ClassTestConfig(
        cls=LayoutInterface,
        expected_class_vars=LAYOUT_INTERFACE_EXPECTED_CLASS_VARS,
        expected_properties=LAYOUT_INTERFACE_EXPECTED_PROPERTIES,
        expected_methods=LAYOUT_INTERFACE_EXPECTED_METHODS,
        expected_class_methods=LAYOUT_INTERFACE_EXPECTED_CLASS_METHODS,
    )
]


@pytest.mark.parametrize("config", LAYOUT_INTERFACE_TEST_CLASS_CONFIG, ids=lambda c: c.cls.__name__)
class TestLayoutInterfaceContract(ClassTestBase):
    pass
