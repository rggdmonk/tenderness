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

from tenderness.cairo_backend.cairo_enum_coerce import (
    CairoEnumCoerce,
    CairoEnumMap,
)
from tests._test_utils.class_test import ClassTestBase, ClassTestConfig

# --------------------------
# Tests for CairoEnumCoerce
# --------------------------
CAIRO_ENUM_COERCE_EXPECTED_STATIC_METHODS = {"build_map", "coerce"}
CAIRO_ENUM_COERCE_TEST_CLASS_CONFIG = [
    ClassTestConfig(
        cls=CairoEnumCoerce,
        expected_static_methods=CAIRO_ENUM_COERCE_EXPECTED_STATIC_METHODS,
    )
]


@pytest.mark.parametrize("config", CAIRO_ENUM_COERCE_TEST_CLASS_CONFIG, ids=lambda c: c.cls.__name__)
class TestCairoEnumCoerceContract(ClassTestBase):
    pass


# --------------------------
# Tests for CairoEnumMap
# --------------------------
CAIRO_ENUM_MAP_EXPECTED_CLASS_VARS = {
    "Antialias",
    "HintStyle",
    "SubpixelOrder",
    "HintMetrics",
    "ColorMode",
    "Operator",
    "SVGUnit",
    "SVGVersion",
    "PDFVersion",
}
CAIRO_ENUM_MAP_TEST_CLASS_CONFIG = [
    ClassTestConfig(
        cls=CairoEnumMap,
        expected_class_vars=CAIRO_ENUM_MAP_EXPECTED_CLASS_VARS,
    )
]


@pytest.mark.parametrize("config", CAIRO_ENUM_MAP_TEST_CLASS_CONFIG, ids=lambda c: c.cls.__name__)
class TestCairoEnumMapContract(ClassTestBase):
    pass
