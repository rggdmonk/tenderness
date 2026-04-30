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

from tenderness.bounding_boxes.text_bounding_box_extractor import TextBoundingBoxExtractor
from tests._test_utils.class_test import ClassTestBase, ClassTestConfig

# --------------------------
# Tests for TextBoundingBoxExtractor
# --------------------------
TEXT_BOUNDING_BOX_EXTRACTOR_EXPECTED_METHODS = {
    "extract_bounding_boxes",
    "_to_tetragon",
    "_to_baseline",
    "_extract_chars",
    "_extract_clusters",
    "_extract_runs",
    "_extract_lines",
    "_extract_layout",
}
TEXT_BOUNDING_BOX_EXTRACTOR_EXPECTED_STATIC_METHODS = {"_decode"}
TEXT_BOUNDING_BOX_EXTRACTOR_EXPECTED_CLASS_VARS = {"PANGO_SCALE"}

TEXT_BOUNDING_BOX_EXTRACTOR_TEST_CLASS_CONFIG = [
    ClassTestConfig(
        cls=TextBoundingBoxExtractor,
        expected_class_vars=TEXT_BOUNDING_BOX_EXTRACTOR_EXPECTED_CLASS_VARS,
        expected_methods=TEXT_BOUNDING_BOX_EXTRACTOR_EXPECTED_METHODS,
        expected_static_methods=TEXT_BOUNDING_BOX_EXTRACTOR_EXPECTED_STATIC_METHODS,
    )
]


@pytest.mark.parametrize("config", TEXT_BOUNDING_BOX_EXTRACTOR_TEST_CLASS_CONFIG, ids=lambda c: c.cls.__name__)
class TestTextBoundingBoxExtractorContract(ClassTestBase):
    pass
