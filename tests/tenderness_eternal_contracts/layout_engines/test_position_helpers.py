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

from tenderness.layout_engines.position_helpers import PositionHelpers
from tests._test_utils.class_test import ClassTestBase, ClassTestConfig

# --------------------------
# Eternal contract tests for PositionHelpers
# --------------------------
POSITION_HELPERS_EXPECTED_STATIC_METHODS = {"inset_rect"}
POSITION_HELPERS_TEST_CLASS_CONFIG = [
    ClassTestConfig(
        cls=PositionHelpers,
        expected_static_methods=POSITION_HELPERS_EXPECTED_STATIC_METHODS,
    )
]


@pytest.mark.parametrize("config", POSITION_HELPERS_TEST_CLASS_CONFIG, ids=lambda c: c.cls.__name__)
class TestPositionHelpersEternalContract(ClassTestBase):
    pass
