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

from tenderness.pipelines.document.setup_helpers import BlockPosition, DocumentSetupHelpers
from tests._test_utils.class_test import ClassTestBase, ClassTestConfig
from tests._test_utils.dataclass_test import DataclassTestBase, DataclassTestConfig

# --------------------------
# Eternal contract tests for BlockPosition
# --------------------------
BLOCK_POSITION_EXPECTED_FIELDS = {"name", "rect"}
BLOCK_POSITION_TEST_CONFIG = [
    DataclassTestConfig(
        dataclass_class=BlockPosition,
        has_slots=True,
        expected_fields=BLOCK_POSITION_EXPECTED_FIELDS,
    ),
]


@pytest.mark.parametrize("config", BLOCK_POSITION_TEST_CONFIG, ids=lambda c: c.dataclass_class.__name__)
class TestBlockPositionEternalContract(DataclassTestBase):
    pass


# --------------------------
# Eternal contract tests for DocumentSetupHelpers
# --------------------------
DOCUMENT_SETUP_HELPERS_EXPECTED_STATIC_METHODS = {
    "apply_background_color",
    "apply_global_margin",
    "resolve_block_positions",
}
DOCUMENT_SETUP_HELPERS_TEST_CONFIG = [
    ClassTestConfig(
        cls=DocumentSetupHelpers,
        expected_static_methods=DOCUMENT_SETUP_HELPERS_EXPECTED_STATIC_METHODS,
    ),
]


@pytest.mark.parametrize("config", DOCUMENT_SETUP_HELPERS_TEST_CONFIG, ids=lambda c: c.cls.__name__)
class TestDocumentSetupHelpersEternalContract(ClassTestBase):
    pass
