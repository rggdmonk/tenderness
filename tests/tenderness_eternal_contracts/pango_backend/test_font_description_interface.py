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

from tenderness.pango_backend.font_description_interface import (
    FontDescriptionInterface,
    FontDescriptionInterfaceParameters,
)
from tests._test_utils.class_test import ClassTestBase, ClassTestConfig
from tests._test_utils.dataclass_test import DataclassTestBase, DataclassTestConfig

# --------------------------
# Tests for FontDescriptionInterfaceParameters
# --------------------------
FONT_DESCRIPTION_INTERFACE_PARAMETERS_EXPECTED_FIELDS = {
    "_COERCE_DISPATCH",
    "_CONFLICTING_PAIRS",
    "color",
    "family",
    "features",
    "gravity",
    "size",
    "size_device_units",
    "stretch",
    "style",
    "variant",
    "variations",
    "weight",
}
FONT_DESCRIPTION_INTERFACE_PARAMETERS_TEST_DATACLASS_CONFIG = [
    DataclassTestConfig(
        dataclass_class=FontDescriptionInterfaceParameters,
        has_slots=True,
        is_frozen=True,
        expected_fields=FONT_DESCRIPTION_INTERFACE_PARAMETERS_EXPECTED_FIELDS,
        expected_methods={"__post_init__", "_validate"},
    )
]


@pytest.mark.parametrize(
    "config", FONT_DESCRIPTION_INTERFACE_PARAMETERS_TEST_DATACLASS_CONFIG, ids=lambda c: c.dataclass_class.__name__
)
class TestFontDescriptionInterfaceParametersContract(DataclassTestBase):
    pass


# --------------------------
# Tests for FontDescriptionInterface
# --------------------------
_FONT_DESCRIPTION_INTERFACE_PARAMETERS_PROPERTY_FIELDS = FONT_DESCRIPTION_INTERFACE_PARAMETERS_EXPECTED_FIELDS - {
    "_COERCE_DISPATCH",
    "_CONFLICTING_PAIRS",
}

FONT_DESCRIPTION_INTERFACE_EXPECTED_PROPERTIES = _FONT_DESCRIPTION_INTERFACE_PARAMETERS_PROPERTY_FIELDS | {
    "size_is_absolute",
    "hash",
    "to_filename",
    "to_string",
}
FONT_DESCRIPTION_INTERFACE_EXPECTED_METHODS = {
    "apply_to_layout_interface",
    "apply_to_layout",
    "get_set_fields",
    "unset_fields",
    "merge_static",
    "set_variations_static",
    "equal",
    "set_family_static",
    "copy_static",
    "merge",
    "copy",
    "free",
    "better_match",
    "set_features_static",
}
FONT_DESCRIPTION_INTERFACE_EXPECTED_CLASS_METHODS = {"from_new", "from_string"}
FONT_DESCRIPTION_INTERFACE_EXPECTED_CLASS_VARS = {"_SETTER_DISPATCH", "PANGO_SCALE"}

FONT_DESCRIPTION_INTERFACE_TEST_CLASS_CONFIG = [
    ClassTestConfig(
        cls=FontDescriptionInterface,
        expected_class_vars=FONT_DESCRIPTION_INTERFACE_EXPECTED_CLASS_VARS,
        expected_properties=FONT_DESCRIPTION_INTERFACE_EXPECTED_PROPERTIES,
        expected_methods=FONT_DESCRIPTION_INTERFACE_EXPECTED_METHODS,
        expected_class_methods=FONT_DESCRIPTION_INTERFACE_EXPECTED_CLASS_METHODS,
    ),
]


@pytest.mark.parametrize("config", FONT_DESCRIPTION_INTERFACE_TEST_CLASS_CONFIG, ids=lambda c: c.cls.__name__)
class TestFontDescriptionInterfaceContract(ClassTestBase):
    pass
