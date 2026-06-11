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

from tenderness.pipelines.document.pipeline import DocumentRenderPipeline
from tests._test_utils.class_test import ClassTestBase, ClassTestConfig

# --------------------------
# Eternal contract tests for DocumentRenderPipeline
# --------------------------
DOCUMENT_RENDER_PIPELINE_EXPECTED_METHODS = {
    "setup",
    "render",
    "_render_text_unit",
    "_render_text_block",
    "_render_table_block",
    "_render_image_block",
    "get_text_bounding_boxes",
    "get_block_bounding_boxes",
    "save_as_file",
    "to_array",
}
DOCUMENT_RENDER_PIPELINE_TEST_CONFIG = [
    ClassTestConfig(
        cls=DocumentRenderPipeline,
        expected_methods=DOCUMENT_RENDER_PIPELINE_EXPECTED_METHODS,
    ),
]


@pytest.mark.parametrize("config", DOCUMENT_RENDER_PIPELINE_TEST_CONFIG, ids=lambda c: c.cls.__name__)
class TestDocumentRenderPipelineEternalContract(ClassTestBase):
    pass
