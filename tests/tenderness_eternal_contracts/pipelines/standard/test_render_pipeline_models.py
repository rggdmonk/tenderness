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

from tenderness.pipelines.standard.render_pipeline_models import SetupRenderResult
from tests._test_utils.dataclass_test import DataclassTestBase, DataclassTestConfig

# --------------------------
# Tests for BlockPlacementResult
# --------------------------
BLOCK_PLACEMENT_RESULT_EXPECTED_FIELDS = {
    "surface_rect",
    "content_rect",
    "canvas_margin",
    "block_positions",
    "surface",
    "stream",
    "cairo_context",
}
BLOCK_PLACEMENT_RESULT_TEST_DATACLASS_CONFIG = [
    DataclassTestConfig(
        dataclass_class=SetupRenderResult,
        has_slots=True,
        expected_fields=BLOCK_PLACEMENT_RESULT_EXPECTED_FIELDS,
    ),
]


@pytest.mark.parametrize(
    "config", BLOCK_PLACEMENT_RESULT_TEST_DATACLASS_CONFIG, ids=lambda c: c.dataclass_class.__name__
)
class TestBlockPlacementResultContract(DataclassTestBase):
    pass
