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

from tenderness.bounding_boxes.text_bounding_box_extractor import TextBoundingBoxExtractor, _RawCluster
from tests._test_utils.class_test import ClassTestBase, ClassTestConfig
from tests._test_utils.dataclass_test import DataclassTestBase, DataclassTestConfig

# --------------------------
# Eternal contract tests for _RawCluster
# --------------------------
_RAW_CLUSTER_EXPECTED_FIELDS = {"byte_index", "run_end", "ink_rect", "logical_rect"}
_RAW_CLUSTER_TEST_CLASS_CONFIG = [
    DataclassTestConfig(
        dataclass_class=_RawCluster,
        has_slots=True,
        expected_fields=_RAW_CLUSTER_EXPECTED_FIELDS,
    )
]


@pytest.mark.parametrize("config", _RAW_CLUSTER_TEST_CLASS_CONFIG, ids=lambda c: c.dataclass_class.__name__)
class TestRawClusterContract(DataclassTestBase):
    pass


# --------------------------
# Eternal contract tests for TextBoundingBoxExtractor
# --------------------------
TEXT_BOUNDING_BOX_EXTRACTOR_EXPECTED_METHODS = {
    "extract_bounding_boxes",
    "_pango_rect_to_quadrilateral",
    "_build_byte_to_char_map",
    "_build_byte_lengths",
    "_extract_chars",
    "_extract_clusters",
    "_extract_runs",
    "_extract_lines",
    "_extract_layout",
}
TEXT_BOUNDING_BOX_EXTRACTOR_EXPECTED_STATIC_METHODS: set[str] = set()
TEXT_BOUNDING_BOX_EXTRACTOR_EXPECTED_CLASS_VARS: set[str] = set()

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
