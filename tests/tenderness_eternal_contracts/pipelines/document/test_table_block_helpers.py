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

from tenderness.pipelines.document.table_block_helpers import (
    CellPosition,
    TableBlock,
    TableBlockHelpers,
    TableBlockResult,
    TextCell,
    TextCellResult,
)
from tests._test_utils.class_test import ClassTestBase, ClassTestConfig
from tests._test_utils.dataclass_test import DataclassTestBase, DataclassTestConfig

# --------------------------
# Eternal contract tests for TextCell
# --------------------------
TEXT_CELL_EXPECTED_FIELDS = {"cell_name", "text", "text_style", "text_strategy"}
TEXT_CELL_TEST_CONFIG = [
    DataclassTestConfig(
        dataclass_class=TextCell,
        has_slots=True,
        expected_fields=TEXT_CELL_EXPECTED_FIELDS,
    ),
]


@pytest.mark.parametrize("config", TEXT_CELL_TEST_CONFIG, ids=lambda c: c.dataclass_class.__name__)
class TestTextCellEternalContract(DataclassTestBase):
    pass


# --------------------------
# Eternal contract tests for TableBlock
# --------------------------
TABLE_BLOCK_EXPECTED_FIELDS = {"cells", "table_cell_pos", "base_text_style"}
TABLE_BLOCK_TEST_CONFIG = [
    DataclassTestConfig(
        dataclass_class=TableBlock,
        has_slots=True,
        expected_fields=TABLE_BLOCK_EXPECTED_FIELDS,
    ),
]


@pytest.mark.parametrize("config", TABLE_BLOCK_TEST_CONFIG, ids=lambda c: c.dataclass_class.__name__)
class TestTableBlockEternalContract(DataclassTestBase):
    pass


# --------------------------
# Eternal contract tests for TextCellResult
# --------------------------
TEXT_CELL_RESULT_EXPECTED_FIELDS = {
    "cell_name",
    "cell_position_name",
    "cell_position_rect",
    "layout_interface",
    "ctm_cairo_matrix",
}
TEXT_CELL_RESULT_TEST_CONFIG = [
    DataclassTestConfig(
        dataclass_class=TextCellResult,
        has_slots=True,
        expected_fields=TEXT_CELL_RESULT_EXPECTED_FIELDS,
    ),
]


@pytest.mark.parametrize("config", TEXT_CELL_RESULT_TEST_CONFIG, ids=lambda c: c.dataclass_class.__name__)
class TestTextCellResultEternalContract(DataclassTestBase):
    pass


# --------------------------
# Eternal contract tests for TableBlockResult
# --------------------------
TABLE_BLOCK_RESULT_EXPECTED_FIELDS = {
    "block_name",
    "block_position_name",
    "block_position_rect",
    "result_cells",
}
TABLE_BLOCK_RESULT_TEST_CONFIG = [
    DataclassTestConfig(
        dataclass_class=TableBlockResult,
        has_slots=True,
        expected_fields=TABLE_BLOCK_RESULT_EXPECTED_FIELDS,
    ),
]


@pytest.mark.parametrize("config", TABLE_BLOCK_RESULT_TEST_CONFIG, ids=lambda c: c.dataclass_class.__name__)
class TestTableBlockResultEternalContract(DataclassTestBase):
    pass


# --------------------------
# Eternal contract tests for CellPosition
# --------------------------
CELL_POSITION_EXPECTED_FIELDS = {"name", "rect"}
CELL_POSITION_TEST_CONFIG = [
    DataclassTestConfig(
        dataclass_class=CellPosition,
        has_slots=True,
        expected_fields=CELL_POSITION_EXPECTED_FIELDS,
    ),
]


@pytest.mark.parametrize("config", CELL_POSITION_TEST_CONFIG, ids=lambda c: c.dataclass_class.__name__)
class TestCellPositionEternalContract(DataclassTestBase):
    pass


# --------------------------
# Eternal contract tests for TableBlockHelpers
# --------------------------
TABLE_BLOCK_HELPERS_EXPECTED_STATIC_METHODS = {"create_cells_within_container"}
TABLE_BLOCK_HELPERS_TEST_CONFIG = [
    ClassTestConfig(
        cls=TableBlockHelpers,
        expected_static_methods=TABLE_BLOCK_HELPERS_EXPECTED_STATIC_METHODS,
    ),
]


@pytest.mark.parametrize("config", TABLE_BLOCK_HELPERS_TEST_CONFIG, ids=lambda c: c.cls.__name__)
class TestTableBlockHelpersEternalContract(ClassTestBase):
    pass
