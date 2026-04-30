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

from tenderness.colors.color_selector import Color, ColorGroup, ColorRegistry, ColorSelector
from tests.tenderness.colors.test_color_selector import TEST_GROUP_NAME, make_group, make_registry


# --------------------------
# Fixtures for test_color_selector.py
# --------------------------
@pytest.fixture
def group() -> ColorGroup:
    return make_group()


@pytest.fixture
def registry() -> ColorRegistry:
    return make_registry()


@pytest.fixture
def selector(registry: ColorRegistry) -> ColorSelector:
    return ColorSelector(color_registry=registry)


@pytest.fixture
def red_color() -> Color:
    return Color.from_hex("red", TEST_GROUP_NAME, "#ff0000")
