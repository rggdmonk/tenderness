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

from tenderness.core.geometry import Margin, Rectangle
from tests._test_utils.dataclass_test import DataclassTestBase, DataclassTestConfig

# --------------------------
# Tests for Margin
# --------------------------
MARGIN_TEST_DATACLASS_CONFIG = [
    DataclassTestConfig(
        dataclass_class=Margin,
        has_slots=True,
        is_frozen=True,
    )
]


@pytest.mark.parametrize("config", MARGIN_TEST_DATACLASS_CONFIG, ids=lambda c: c.dataclass_class.__name__)
class TestMarginContract(DataclassTestBase):
    pass


# --------------------------
# Tests for Rectangle
# --------------------------
RECTANGLE_EXPECTED_FIELDS = {
    "x",
    "y",
    "width",
    "height",
    "_x_min",
    "_x_max",
    "_y_min",
    "_y_max",
}

RECTANGLE_EXPECTED_PROPERTIES = {
    "area",
    "aspect_ratio",
    "bounds",
    "center",
    "corners",
    "diagonal",
    "extents",
    "is_empty",
    "is_non_negative",
    "normalized_size",
    "perimeter",
    "size",
    "x_max",
    "x_min",
    "y_max",
    "y_min",
}

RECTANGLE_EXPECTED_METHODS = {
    "__post_init__",
    "contains_point",
    "union",
    "distance_to",
    "contains_rect",
    "intersects",
    "intersection",
    "touches",
    "transform",
    "inset",
}
RECTANGLE_TEST_DATACLASS_CONFIG = [
    DataclassTestConfig(
        dataclass_class=Rectangle,
        has_slots=True,
        is_frozen=True,
        expected_fields=RECTANGLE_EXPECTED_FIELDS,
        expected_properties=RECTANGLE_EXPECTED_PROPERTIES,
        expected_methods=RECTANGLE_EXPECTED_METHODS,
    )
]


@pytest.mark.parametrize("config", RECTANGLE_TEST_DATACLASS_CONFIG, ids=lambda c: c.dataclass_class.__name__)
class TestRectangleContract(DataclassTestBase):
    pass
