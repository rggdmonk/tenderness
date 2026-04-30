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

from tenderness.pango_backend.pango_enum_coerce import (
    PangoEnumCoerce,
    PangoEnumMap,
)
from tests._test_utils.class_test import ClassTestBase, ClassTestConfig

# --------------------------
# Tests for PangoEnumCoerce
# --------------------------
PANGO_ENUM_COERCE_EXPECTED_STATIC_METHODS = {"build_map", "coerce"}
PANGO_ENUM_COERCE_TEST_CLASS_CONFIG = [
    ClassTestConfig(
        cls=PangoEnumCoerce,
        expected_static_methods=PANGO_ENUM_COERCE_EXPECTED_STATIC_METHODS,
    )
]


@pytest.mark.parametrize("config", PANGO_ENUM_COERCE_TEST_CLASS_CONFIG, ids=lambda c: c.cls.__name__)
class TestPangoEnumCoerceContract(ClassTestBase):
    pass


# --------------------------
# Tests for PangoEnumMap
# --------------------------
PANGO_ENUM_MAP_EXPECTED_CLASS_VARS = {
    "WrapMode",
    "EllipsizeMode",
    "Alignment",
    "Gravity",
    "Stretch",
    "Style",
    "Variant",
    "Weight",
    "FontColor",
    "Direction",
    "GravityHint",
    "TabAlign",
}
PANGO_ENUM_MAP_TEST_CLASS_CONFIG = [
    ClassTestConfig(
        cls=PangoEnumMap,
        expected_class_vars=PANGO_ENUM_MAP_EXPECTED_CLASS_VARS,
    )
]


@pytest.mark.parametrize("config", PANGO_ENUM_MAP_TEST_CLASS_CONFIG, ids=lambda c: c.cls.__name__)
class TestPangoEnumMapContract(ClassTestBase):
    pass
