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

from tenderness.core.color_models import AlphaPosition, ColorModel
from tests._test_utils.str_enum_test import StrEnumTestBase, StrEnumTestConfig

# --------------------------
# Tests for AlphaPosition
# --------------------------
ALPHA_POSITION_EXPECTED_MEMBERS = {"FIRST", "LAST", "NONE", "ONLY"}
ALPHA_POSITION_TEST_STR_ENUM_CONFIG = [
    StrEnumTestConfig(
        enum_class=AlphaPosition,
        expected_members=ALPHA_POSITION_EXPECTED_MEMBERS,
    )
]


@pytest.mark.parametrize("config", ALPHA_POSITION_TEST_STR_ENUM_CONFIG, ids=lambda c: c.enum_class.__name__)
class TestAlphaPositionContract(StrEnumTestBase):
    pass


# --------------------------
# Testsfor ColorModel
# --------------------------
COLOR_MODEL_EXPECTED_MEMBERS = {"RGB", "RGBA", "ALPHA"}
COLOR_MODEL_EXPECTED_PROPERTIES = {"has_alpha", "num_channels", "alpha_position"}
COLOR_MODEL_TEST_STR_ENUM_CONFIG = [
    StrEnumTestConfig(
        enum_class=ColorModel,
        expected_members=COLOR_MODEL_EXPECTED_MEMBERS,
        expected_properties=COLOR_MODEL_EXPECTED_PROPERTIES,
    )
]


@pytest.mark.parametrize("config", COLOR_MODEL_TEST_STR_ENUM_CONFIG, ids=lambda c: c.enum_class.__name__)
class TestColorModelContract(StrEnumTestBase):
    pass
