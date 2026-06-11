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

from tenderness.bounding_boxes.draw_text_bboxes import (
    ImageTextBoundingBoxDrawer,
    SVGTextBoundingBoxDrawer,
    TextDrawConfig,
    _LevelMeta,
)
from tests._test_utils.class_test import ClassTestBase, ClassTestConfig
from tests._test_utils.dataclass_test import DataclassTestBase, DataclassTestConfig

# --------------------------
# Eternal contract tests for TextDrawConfig
# --------------------------
DRAW_CONFIG_EXPECTED_FIELDS = {
    "char_color",
    "cluster_color",
    "run_color",
    "line_color",
    "layout_color",
    "fill_alpha",
    "draw_ink_bbox",
    "draw_labels",
    "line_width",
    "levels",
}
DRAW_CONFIG_TEST_DATACLASS_CONFIG = [
    DataclassTestConfig(
        dataclass_class=TextDrawConfig,
        has_slots=False,
        is_frozen=False,
        expected_fields=DRAW_CONFIG_EXPECTED_FIELDS,
    )
]


@pytest.mark.parametrize("config", DRAW_CONFIG_TEST_DATACLASS_CONFIG, ids=lambda c: c.dataclass_class.__name__)
class TestTextDrawConfigContract(DataclassTestBase):
    pass


# --------------------------
# Eternal contract tests for _LevelMeta
# --------------------------
_LEVEL_META_EXPECTED_FIELDS = {"boxes_attr", "color_attr", "has_ink"}
_LEVEL_META_TEST_DATACLASS_CONFIG = [
    DataclassTestConfig(
        dataclass_class=_LevelMeta,
        has_slots=False,
        is_frozen=True,
        expected_fields=_LEVEL_META_EXPECTED_FIELDS,
    )
]


@pytest.mark.parametrize("config", _LEVEL_META_TEST_DATACLASS_CONFIG, ids=lambda c: c.dataclass_class.__name__)
class TestLevelMetaContract(DataclassTestBase):
    pass


# --------------------------
# Eternal contract tests for ImageTextBoundingBoxDrawer
# --------------------------
IMAGE_BOUNDING_BOX_DRAWER_EXPECTED_METHODS = {
    "draw",
    "draw_per_level",
    "_composite_level",
    "_draw_box",
    "_draw_label",
}
IMAGE_BOUNDING_BOX_DRAWER_EXPECTED_STATIC_METHODS = {"_label", "_darken"}
IMAGE_BOUNDING_BOX_DRAWER_TEST_CLASS_CONFIG = [
    ClassTestConfig(
        cls=ImageTextBoundingBoxDrawer,
        expected_methods=IMAGE_BOUNDING_BOX_DRAWER_EXPECTED_METHODS,
        expected_static_methods=IMAGE_BOUNDING_BOX_DRAWER_EXPECTED_STATIC_METHODS,
    )
]


@pytest.mark.parametrize("config", IMAGE_BOUNDING_BOX_DRAWER_TEST_CLASS_CONFIG, ids=lambda c: c.cls.__name__)
class TestImageTextBoundingBoxDrawerContract(ClassTestBase):
    pass


# --------------------------
# Eternal contract tests for SVGTextBoundingBoxDrawer
# --------------------------
SVG_BOUNDING_BOX_DRAWER_EXPECTED_METHODS = {
    "draw",
    "_draw_level",
    "_add_quadrilateral",
    "_add_label",
}
SVG_BOUNDING_BOX_DRAWER_EXPECTED_STATIC_METHODS = {"_label", "_darken"}
SVG_BOUNDING_BOX_DRAWER_EXPECTED_CLASS_VARS = {"_NS"}
SVG_BOUNDING_BOX_DRAWER_TEST_CLASS_CONFIG = [
    ClassTestConfig(
        cls=SVGTextBoundingBoxDrawer,
        expected_methods=SVG_BOUNDING_BOX_DRAWER_EXPECTED_METHODS,
        expected_static_methods=SVG_BOUNDING_BOX_DRAWER_EXPECTED_STATIC_METHODS,
        expected_class_vars=SVG_BOUNDING_BOX_DRAWER_EXPECTED_CLASS_VARS,
    )
]


@pytest.mark.parametrize("config", SVG_BOUNDING_BOX_DRAWER_TEST_CLASS_CONFIG, ids=lambda c: c.cls.__name__)
class TestSVGTextBoundingBoxDrawerContract(ClassTestBase):
    pass
