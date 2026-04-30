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

from tenderness.cairo_backend.matrix.matrix_transforms import MatrixTransformType
from tests._test_utils.str_enum_test import StrEnumTestBase, StrEnumTestConfig

# --------------------------
# Tests for MatrixTransformType
# --------------------------
MATRIX_TRANSFORM_TYPE_EXPECTED_MEMBERS = {
    "TRANSLATE",
    "SCALE",
    "ROTATE",
    "ROTATE_AROUND_POINT",
    "SKEW_X",
    "SKEW_Y",
    "FLIP_HORIZONTAL",
    "FLIP_VERTICAL",
}
MATRIX_TRANSFORM_TYPE_TEST_STR_ENUM_CONFIG = [
    StrEnumTestConfig(
        enum_class=MatrixTransformType,
        expected_members=MATRIX_TRANSFORM_TYPE_EXPECTED_MEMBERS,
    )
]


@pytest.mark.parametrize("config", MATRIX_TRANSFORM_TYPE_TEST_STR_ENUM_CONFIG, ids=lambda c: c.enum_class.__name__)
class TestMatrixTransformTypeContract(StrEnumTestBase):
    pass
