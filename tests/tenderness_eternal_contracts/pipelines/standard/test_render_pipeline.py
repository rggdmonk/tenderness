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

from tenderness.pipelines.standard.render_pipeline import RenderPipeline
from tests._test_utils.class_test import ClassTestBase, ClassTestConfig

# --------------------------
# Tests for StandardRenderPipeline
# --------------------------
STANDARD_RENDER_PIPELINE_EXPECTED_METHODS = {
    "setup_render",
    "render_text",
    "get_text_bounding_boxes",
    "get_block_bounding_boxes",
    "save_as_file",
    "to_array",
    "_apply_text_style",
    "_create_text_layout_template",
    "_render_image_block",
    "_render_table_block",
    "_render_text_block",
    "_create_cells_within_container",
    "resolve_table_cell_positions",
}

STANDARD_RENDER_PIPELINE_TEST_CLASS_CONFIG = [
    ClassTestConfig(
        cls=RenderPipeline,
        expected_methods=STANDARD_RENDER_PIPELINE_EXPECTED_METHODS,
    ),
]


@pytest.mark.parametrize(
    "config",
    STANDARD_RENDER_PIPELINE_TEST_CLASS_CONFIG,
    ids=lambda c: c.cls.__name__,
)
class TestStandardRenderPipelineContract(ClassTestBase):
    pass
