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

from tenderness.pipelines.document.bbox_helper import (
    BlockBBox,
    BlockBBoxesResult,
    CellBBox,
    TableBlockBBoxesResult,
    TextBlockBBoxesResult,
)
from tests._test_utils.dataclass_test import DataclassTestBase, DataclassTestConfig

# --------------------------
# Eternal contract tests for TextBlockBBoxesResult
# --------------------------
TEXT_BLOCK_BBOXES_RESULT_EXPECTED_FIELDS = {"block_name", "block_position_name", "bboxes"}
TEXT_BLOCK_BBOXES_RESULT_EXPECTED_METHODS = {"to_dict"}
TEXT_BLOCK_BBOXES_RESULT_TEST_CONFIG = [
    DataclassTestConfig(
        dataclass_class=TextBlockBBoxesResult,
        has_slots=True,
        expected_fields=TEXT_BLOCK_BBOXES_RESULT_EXPECTED_FIELDS,
        expected_methods=TEXT_BLOCK_BBOXES_RESULT_EXPECTED_METHODS,
    ),
]


@pytest.mark.parametrize("config", TEXT_BLOCK_BBOXES_RESULT_TEST_CONFIG, ids=lambda c: c.dataclass_class.__name__)
class TestTextBlockBBoxesResultEternalContract(DataclassTestBase):
    pass


# --------------------------
# Eternal contract tests for CellBBox
# --------------------------
CELL_BBOX_EXPECTED_FIELDS = {"cell_name", "cell_position_name", "bboxes"}
CELL_BBOX_EXPECTED_METHODS = {"to_dict"}
CELL_BBOX_TEST_CONFIG = [
    DataclassTestConfig(
        dataclass_class=CellBBox,
        has_slots=True,
        expected_fields=CELL_BBOX_EXPECTED_FIELDS,
        expected_methods=CELL_BBOX_EXPECTED_METHODS,
    ),
]


@pytest.mark.parametrize("config", CELL_BBOX_TEST_CONFIG, ids=lambda c: c.dataclass_class.__name__)
class TestCellBBoxEternalContract(DataclassTestBase):
    pass


# --------------------------
# Eternal contract tests for TableBlockBBoxesResult
# --------------------------
TABLE_BLOCK_BBOXES_RESULT_EXPECTED_FIELDS = {"block_name", "block_position_name", "cell_bboxes"}
TABLE_BLOCK_BBOXES_RESULT_EXPECTED_METHODS = {"to_dict"}
TABLE_BLOCK_BBOXES_RESULT_TEST_CONFIG = [
    DataclassTestConfig(
        dataclass_class=TableBlockBBoxesResult,
        has_slots=True,
        expected_fields=TABLE_BLOCK_BBOXES_RESULT_EXPECTED_FIELDS,
        expected_methods=TABLE_BLOCK_BBOXES_RESULT_EXPECTED_METHODS,
    ),
]


@pytest.mark.parametrize("config", TABLE_BLOCK_BBOXES_RESULT_TEST_CONFIG, ids=lambda c: c.dataclass_class.__name__)
class TestTableBlockBBoxesResultEternalContract(DataclassTestBase):
    pass


# --------------------------
# Eternal contract tests for BlockBBox
# --------------------------
BLOCK_BBOX_EXPECTED_FIELDS = {"name", "bbox"}
BLOCK_BBOX_EXPECTED_METHODS = {"to_dict"}
BLOCK_BBOX_TEST_CONFIG = [
    DataclassTestConfig(
        dataclass_class=BlockBBox,
        has_slots=True,
        expected_fields=BLOCK_BBOX_EXPECTED_FIELDS,
        expected_methods=BLOCK_BBOX_EXPECTED_METHODS,
    ),
]


@pytest.mark.parametrize("config", BLOCK_BBOX_TEST_CONFIG, ids=lambda c: c.dataclass_class.__name__)
class TestBlockBBoxEternalContract(DataclassTestBase):
    pass


# --------------------------
# Eternal contract tests for BlockBBoxesResult
# --------------------------
BLOCK_BBOXES_RESULT_EXPECTED_FIELDS = {"surface_bbox", "content_bbox", "block_bboxes"}
BLOCK_BBOXES_RESULT_EXPECTED_METHODS = {"to_dict"}
BLOCK_BBOXES_RESULT_TEST_CONFIG = [
    DataclassTestConfig(
        dataclass_class=BlockBBoxesResult,
        has_slots=True,
        expected_fields=BLOCK_BBOXES_RESULT_EXPECTED_FIELDS,
        expected_methods=BLOCK_BBOXES_RESULT_EXPECTED_METHODS,
    ),
]


@pytest.mark.parametrize("config", BLOCK_BBOXES_RESULT_TEST_CONFIG, ids=lambda c: c.dataclass_class.__name__)
class TestBlockBBoxesResultEternalContract(DataclassTestBase):
    pass
