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

from tenderness.pipelines.standard.render_blocks import (
    BaseBlock,
    BlocksConfig,
    CanvasConfig,
    ImageBlock,
    TableBlock,
    TableCell,
    TextBlock,
    TextStyle,
)
from tests._test_utils.dataclass_test import DataclassTestBase, DataclassTestConfig

# --------------------------
# Tests for BaseBlock
# --------------------------
BASE_BLOCK_EXPECTED_FIELDS = {"block_name"}
BASE_BLOCK_TEST_DATACLASS_CONFIG = [
    DataclassTestConfig(
        dataclass_class=BaseBlock,
        has_slots=True,
        expected_fields=BASE_BLOCK_EXPECTED_FIELDS,
    ),
]


@pytest.mark.parametrize("config", BASE_BLOCK_TEST_DATACLASS_CONFIG, ids=lambda c: c.dataclass_class.__name__)
class TestBaseBlockContract(DataclassTestBase):
    pass


# --------------------------
# Tests for TextBlock
# --------------------------
TEXT_BLOCK_EXPECTED_FIELDS = {
    "text",
    "style",
    "text_strategy",
}
TEXT_BLOCK_TEST_DATACLASS_CONFIG = [
    DataclassTestConfig(
        dataclass_class=TextBlock,
        has_slots=True,
        expected_fields=TEXT_BLOCK_EXPECTED_FIELDS,
    ),
]


@pytest.mark.parametrize("config", TEXT_BLOCK_TEST_DATACLASS_CONFIG, ids=lambda c: c.dataclass_class.__name__)
class TestTextBlockContract(DataclassTestBase):
    pass


# --------------------------
# Tests for ImageBlock
# --------------------------
IMAGE_BLOCK_EXPECTED_FIELDS = {
    "path_to_image",
    "scale_mode",
    "operator",
    "alpha",
    "image_format",
}
IMAGE_BLOCK_EXPECTED_METHODS = {"__post_init__"}
IMAGE_BLOCK_TEST_DATACLASS_CONFIG = [
    DataclassTestConfig(
        dataclass_class=ImageBlock,
        has_slots=True,
        expected_fields=IMAGE_BLOCK_EXPECTED_FIELDS,
        expected_methods=IMAGE_BLOCK_EXPECTED_METHODS,
    ),
]


@pytest.mark.parametrize("config", IMAGE_BLOCK_TEST_DATACLASS_CONFIG, ids=lambda c: c.dataclass_class.__name__)
class TestImageBlockContract(DataclassTestBase):
    pass


# --------------------------
# Tests for TableCell
# --------------------------
TABLE_CELL_EXPECTED_FIELDS = {
    "cell_name",
    "content",
    "style",
    "text_strategy",
}
TABLE_CELL_TEST_DATACLASS_CONFIG = [
    DataclassTestConfig(
        dataclass_class=TableCell,
        has_slots=True,
        expected_fields=TABLE_CELL_EXPECTED_FIELDS,
    ),
]


@pytest.mark.parametrize("config", TABLE_CELL_TEST_DATACLASS_CONFIG, ids=lambda c: c.dataclass_class.__name__)
class TestTableCellContract(DataclassTestBase):
    pass


# --------------------------
# Tests for TableBlock
# --------------------------
TABLE_BLOCK_EXPECTED_FIELDS = {
    "cells",
    "table_cell_pos",
    "default_style",
}
TABLE_BLOCK_TEST_DATACLASS_CONFIG = [
    DataclassTestConfig(
        dataclass_class=TableBlock,
        has_slots=True,
        expected_fields=TABLE_BLOCK_EXPECTED_FIELDS,
    ),
]


@pytest.mark.parametrize("config", TABLE_BLOCK_TEST_DATACLASS_CONFIG, ids=lambda c: c.dataclass_class.__name__)
class TestTableBlockContract(DataclassTestBase):
    pass


# --------------------------
# Tests for TextStyle
# --------------------------
TEXT_STYLE_EXPECTED_FIELDS = {
    "font_options_params",
    "font_description_params",
    "text_color_spec",
    "layout_interface_params",
    "layout_context_params",
    "context_transform_params",
}
TEXT_STYLE_TEST_DATACLASS_CONFIG = [
    DataclassTestConfig(
        dataclass_class=TextStyle,
        has_slots=True,
        expected_fields=TEXT_STYLE_EXPECTED_FIELDS,
    ),
]


@pytest.mark.parametrize("config", TEXT_STYLE_TEST_DATACLASS_CONFIG, ids=lambda c: c.dataclass_class.__name__)
class TestTextStyleContract(DataclassTestBase):
    pass


# --------------------------
# Tests for PlacementConfig
# --------------------------
PLACEMENT_CONFIG_EXPECTED_FIELDS = {
    "surface_config",
    "global_margin",
    "block_spec",
    "background_spec",
}
PLACEMENT_CONFIG_TEST_DATACLASS_CONFIG = [
    DataclassTestConfig(
        dataclass_class=CanvasConfig,
        has_slots=True,
        expected_fields=PLACEMENT_CONFIG_EXPECTED_FIELDS,
    ),
]


@pytest.mark.parametrize(
    "config",
    PLACEMENT_CONFIG_TEST_DATACLASS_CONFIG,
    ids=lambda c: c.dataclass_class.__name__,
)
class TestPlacementConfigContract(DataclassTestBase):
    pass


# --------------------------
# Tests for BlocksConfig
# --------------------------
BLOCKS_CONFIG_EXPECTED_FIELDS = {
    "surface_config",
    "blocks",
    "default_text_style",
}
BLOCKS_CONFIG_TEST_DATACLASS_CONFIG = [
    DataclassTestConfig(
        dataclass_class=BlocksConfig,
        has_slots=True,
        expected_fields=BLOCKS_CONFIG_EXPECTED_FIELDS,
    ),
]


@pytest.mark.parametrize(
    "config",
    BLOCKS_CONFIG_TEST_DATACLASS_CONFIG,
    ids=lambda c: c.dataclass_class.__name__,
)
class TestBlocksConfigContract(DataclassTestBase):
    pass
