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

from tenderness.pipelines.document.draw_block_bboxes import (
    BlockDrawConfig,
    ImageBlockBoundingBoxDrawer,
    SVGBlockBoundingBoxDrawer,
)
from tests._test_utils.class_test import ClassTestBase, ClassTestConfig
from tests._test_utils.dataclass_test import DataclassTestBase, DataclassTestConfig

# --------------------------
# Eternal contract tests for BlockDrawConfig
# --------------------------
BLOCK_DRAW_CONFIG_EXPECTED_FIELDS = {
    "surface_color",
    "content_color",
    "block_color",
    "fill_alpha",
    "draw_labels",
    "line_width",
}
BLOCK_DRAW_CONFIG_TEST_CONFIG = [
    DataclassTestConfig(
        dataclass_class=BlockDrawConfig,
        has_slots=False,
        is_frozen=False,
        expected_fields=BLOCK_DRAW_CONFIG_EXPECTED_FIELDS,
    )
]


@pytest.mark.parametrize("config", BLOCK_DRAW_CONFIG_TEST_CONFIG, ids=lambda c: c.dataclass_class.__name__)
class TestBlockDrawConfigContract(DataclassTestBase):
    pass


# --------------------------
# Eternal contract tests for ImageBlockBoundingBoxDrawer
# --------------------------
IMAGE_BLOCK_BBOX_DRAWER_EXPECTED_METHODS = {
    "draw",
    "draw_per_block",
    "_draw_entry",
}
IMAGE_BLOCK_BBOX_DRAWER_EXPECTED_STATIC_METHODS = {"_entries"}
IMAGE_BLOCK_BBOX_DRAWER_TEST_CONFIG = [
    ClassTestConfig(
        cls=ImageBlockBoundingBoxDrawer,
        expected_methods=IMAGE_BLOCK_BBOX_DRAWER_EXPECTED_METHODS,
        expected_static_methods=IMAGE_BLOCK_BBOX_DRAWER_EXPECTED_STATIC_METHODS,
    )
]


@pytest.mark.parametrize("config", IMAGE_BLOCK_BBOX_DRAWER_TEST_CONFIG, ids=lambda c: c.cls.__name__)
class TestImageBlockBoundingBoxDrawerContract(ClassTestBase):
    pass


# --------------------------
# Eternal contract tests for SVGBlockBoundingBoxDrawer
# --------------------------
SVG_BLOCK_BBOX_DRAWER_EXPECTED_METHODS = {
    "draw",
    "draw_per_block",
    "_add_quadrilateral",
    "_add_label",
}
SVG_BLOCK_BBOX_DRAWER_EXPECTED_STATIC_METHODS = {"_entries"}
SVG_BLOCK_BBOX_DRAWER_EXPECTED_CLASS_VARS = {"_NS"}
SVG_BLOCK_BBOX_DRAWER_TEST_CONFIG = [
    ClassTestConfig(
        cls=SVGBlockBoundingBoxDrawer,
        expected_methods=SVG_BLOCK_BBOX_DRAWER_EXPECTED_METHODS,
        expected_static_methods=SVG_BLOCK_BBOX_DRAWER_EXPECTED_STATIC_METHODS,
        expected_class_vars=SVG_BLOCK_BBOX_DRAWER_EXPECTED_CLASS_VARS,
    )
]


@pytest.mark.parametrize("config", SVG_BLOCK_BBOX_DRAWER_TEST_CONFIG, ids=lambda c: c.cls.__name__)
class TestSVGBlockBoundingBoxDrawerContract(ClassTestBase):
    pass
