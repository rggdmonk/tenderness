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

from tenderness.pipelines.document.text_block_helpers import (
    TextBlock,
    TextBlockHelpers,
    TextBlockResult,
    TextStyle,
)
from tests._test_utils.class_test import ClassTestBase, ClassTestConfig
from tests._test_utils.dataclass_test import DataclassTestBase, DataclassTestConfig

# --------------------------
# Eternal contract tests for TextStyle
# --------------------------
TEXT_STYLE_EXPECTED_FIELDS = {
    "font_options_params",
    "font_description_params",
    "text_color_spec",
    "layout_interface_params",
    "layout_context_params",
    "context_transform_params",
}
TEXT_STYLE_TEST_CONFIG = [
    DataclassTestConfig(
        dataclass_class=TextStyle,
        has_slots=True,
        expected_fields=TEXT_STYLE_EXPECTED_FIELDS,
    ),
]


@pytest.mark.parametrize("config", TEXT_STYLE_TEST_CONFIG, ids=lambda c: c.dataclass_class.__name__)
class TestTextStyleEternalContract(DataclassTestBase):
    pass


# --------------------------
# Eternal contract tests for TextBlock
# --------------------------
TEXT_BLOCK_EXPECTED_FIELDS = {"text", "text_style", "text_strategy"}
TEXT_BLOCK_TEST_CONFIG = [
    DataclassTestConfig(
        dataclass_class=TextBlock,
        has_slots=True,
        expected_fields=TEXT_BLOCK_EXPECTED_FIELDS,
    ),
]


@pytest.mark.parametrize("config", TEXT_BLOCK_TEST_CONFIG, ids=lambda c: c.dataclass_class.__name__)
class TestTextBlockEternalContract(DataclassTestBase):
    pass


# --------------------------
# Eternal contract tests for TextBlockResult
# --------------------------
TEXT_BLOCK_RESULT_EXPECTED_FIELDS = {
    "block_name",
    "block_position_name",
    "block_position_rect",
    "layout_interface",
    "ctm_cairo_matrix",
}
TEXT_BLOCK_RESULT_TEST_CONFIG = [
    DataclassTestConfig(
        dataclass_class=TextBlockResult,
        has_slots=True,
        expected_fields=TEXT_BLOCK_RESULT_EXPECTED_FIELDS,
    ),
]


@pytest.mark.parametrize("config", TEXT_BLOCK_RESULT_TEST_CONFIG, ids=lambda c: c.dataclass_class.__name__)
class TestTextBlockResultEternalContract(DataclassTestBase):
    pass


# --------------------------
# Eternal contract tests for TextBlockHelpers
# --------------------------
TEXT_BLOCK_HELPERS_EXPECTED_STATIC_METHODS = {
    "apply_pango_text_style",
    "apply_cairo_text_style",
    "create_base_text_layout_template",
    "resolve_text_for_block",
    "text_style_has_explicit_width",
    "text_style_has_explicit_height",
}
TEXT_BLOCK_HELPERS_TEST_CONFIG = [
    ClassTestConfig(
        cls=TextBlockHelpers,
        expected_static_methods=TEXT_BLOCK_HELPERS_EXPECTED_STATIC_METHODS,
    ),
]


@pytest.mark.parametrize("config", TEXT_BLOCK_HELPERS_TEST_CONFIG, ids=lambda c: c.cls.__name__)
class TestTextBlockHelpersEternalContract(ClassTestBase):
    pass
