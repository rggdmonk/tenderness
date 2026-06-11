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

from tenderness.pipelines.document.pipeline_schema import (
    BaseBlock,
    DocumentBlocksConfig,
    DocumentConfig,
    DocumentRenderResult,
    DocumentSetupResult,
)
from tests._test_utils.dataclass_test import DataclassTestBase, DataclassTestConfig

# --------------------------
# Eternal contract tests for BaseBlock
# --------------------------
BASE_BLOCK_EXPECTED_FIELDS = {"block_name"}
BASE_BLOCK_TEST_CONFIG = [
    DataclassTestConfig(
        dataclass_class=BaseBlock,
        has_slots=True,
        expected_fields=BASE_BLOCK_EXPECTED_FIELDS,
    ),
]


@pytest.mark.parametrize("config", BASE_BLOCK_TEST_CONFIG, ids=lambda c: c.dataclass_class.__name__)
class TestBaseBlockEternalContract(DataclassTestBase):
    pass


# --------------------------
# Eternal contract tests for DocumentConfig
# --------------------------
DOCUMENT_CONFIG_EXPECTED_FIELDS = {"surface_config", "global_margin", "block_spec", "background_spec"}
DOCUMENT_CONFIG_TEST_CONFIG = [
    DataclassTestConfig(
        dataclass_class=DocumentConfig,
        has_slots=True,
        expected_fields=DOCUMENT_CONFIG_EXPECTED_FIELDS,
    ),
]


@pytest.mark.parametrize("config", DOCUMENT_CONFIG_TEST_CONFIG, ids=lambda c: c.dataclass_class.__name__)
class TestDocumentConfigEternalContract(DataclassTestBase):
    pass


# --------------------------
# Eternal contract tests for DocumentBlocksConfig
# --------------------------
DOCUMENT_BLOCKS_CONFIG_EXPECTED_FIELDS = {"surface_config", "blocks", "base_text_style"}
DOCUMENT_BLOCKS_CONFIG_TEST_CONFIG = [
    DataclassTestConfig(
        dataclass_class=DocumentBlocksConfig,
        has_slots=True,
        expected_fields=DOCUMENT_BLOCKS_CONFIG_EXPECTED_FIELDS,
    ),
]


@pytest.mark.parametrize("config", DOCUMENT_BLOCKS_CONFIG_TEST_CONFIG, ids=lambda c: c.dataclass_class.__name__)
class TestDocumentBlocksConfigEternalContract(DataclassTestBase):
    pass


# --------------------------
# Eternal contract tests for DocumentSetupResult
# --------------------------
DOCUMENT_SETUP_RESULT_EXPECTED_FIELDS = {
    "surface_rect",
    "content_rect",
    "document_margin",
    "block_positions",
    "surface",
    "stream",
    "cairo_context",
    "surface_config",
}
DOCUMENT_SETUP_RESULT_TEST_CONFIG = [
    DataclassTestConfig(
        dataclass_class=DocumentSetupResult,
        has_slots=True,
        expected_fields=DOCUMENT_SETUP_RESULT_EXPECTED_FIELDS,
    ),
]


@pytest.mark.parametrize("config", DOCUMENT_SETUP_RESULT_TEST_CONFIG, ids=lambda c: c.dataclass_class.__name__)
class TestDocumentSetupResultEternalContract(DataclassTestBase):
    pass


# --------------------------
# Eternal contract tests for DocumentRenderResult
# --------------------------
DOCUMENT_RENDER_RESULT_EXPECTED_FIELDS = {"rendered_blocks"}
DOCUMENT_RENDER_RESULT_TEST_CONFIG = [
    DataclassTestConfig(
        dataclass_class=DocumentRenderResult,
        has_slots=True,
        expected_fields=DOCUMENT_RENDER_RESULT_EXPECTED_FIELDS,
    ),
]


@pytest.mark.parametrize("config", DOCUMENT_RENDER_RESULT_TEST_CONFIG, ids=lambda c: c.dataclass_class.__name__)
class TestDocumentRenderResultEternalContract(DataclassTestBase):
    pass
