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

from tenderness.cairo_backend.text_color_selector import TextColorSelector
from tests._test_utils.class_test import ClassTestBase, ClassTestConfig

# --------------------------
# Tests for TextColorSelector
# --------------------------
TEXT_COLOR_SELECTOR_EXPECTED_METHODS = {"add_text_color"}

TEXT_COLOR_SELECTOR_TEST_CLASS_CONFIG = [
    ClassTestConfig(
        cls=TextColorSelector,
        expected_methods=TEXT_COLOR_SELECTOR_EXPECTED_METHODS,
    )
]


@pytest.mark.parametrize("config", TEXT_COLOR_SELECTOR_TEST_CLASS_CONFIG, ids=lambda c: c.cls.__name__)
class TestTextColorSelectorContract(ClassTestBase):
    pass
