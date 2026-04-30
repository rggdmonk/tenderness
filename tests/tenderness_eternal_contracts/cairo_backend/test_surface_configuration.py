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

from tenderness.cairo_backend.surface_configuration import (
    ImageSurfaceConfig,
    PDFSurfaceConfig,
    RasterSurfaceConfig,
    SurfaceConfig,
    SurfaceRect,
    SurfaceType,
    SVGSurfaceConfig,
    VectorSurfaceConfig,
)
from tests._test_utils.class_test import ClassTestBase, ClassTestConfig
from tests._test_utils.dataclass_test import DataclassTestBase, DataclassTestConfig
from tests._test_utils.str_enum_test import StrEnumTestBase, StrEnumTestConfig

# --------------------------
# Tests for SurfaceType
# --------------------------
SURFACE_TYPE_EXPECTED_MEMBERS = {"IMAGE", "SVG", "PDF"}
SURFACE_TYPE_TEST_STR_ENUM_CONFIG = [
    StrEnumTestConfig(
        enum_class=SurfaceType,
        expected_members=SURFACE_TYPE_EXPECTED_MEMBERS,
    )
]


@pytest.mark.parametrize("config", SURFACE_TYPE_TEST_STR_ENUM_CONFIG, ids=lambda c: c.enum_class.__name__)
class TestSurfaceTypeContract(StrEnumTestBase):
    pass


# --------------------------
# Tests for SurfaceRect
# --------------------------
SURFACE_RECT_EXPECTED_CLASS_METHODS = {"from_surface_config"}
SURFACE_RECT_TEST_CLASS_CONFIG = [
    ClassTestConfig(
        cls=SurfaceRect,
        expected_class_methods=SURFACE_RECT_EXPECTED_CLASS_METHODS,
    )
]


@pytest.mark.parametrize("config", SURFACE_RECT_TEST_CLASS_CONFIG, ids=lambda c: c.cls.__name__)
class TestSurfaceRectContract(ClassTestBase):
    pass


# --------------------------
# Tests for SurfaceConfig
# --------------------------
SURFACE_CONFIG_EXPECTED_FIELDS = {"width", "height", "color_model", "image_format", "image_backend"}
SURFACE_CONFIG_EXPECTED_PROPERTIES = {"rect"}
SURFACE_CONFIG_EXPECTED_DATACLASS_ABSTRACT_PROPERTIES = {"surface_type"}
SURFACE_CONFIG_EXPECTED_METHODS = {
    "__post_init__",
    "_validate_dimensions",
    "_validate_backend_support",
    "_validate_alpha_compatibility",
}
SURFACE_CONFIG_TEST_DATACLASS_CONFIG = [
    DataclassTestConfig(
        dataclass_class=SurfaceConfig,
        is_abstract=True,
        is_frozen=True,
        expected_fields=SURFACE_CONFIG_EXPECTED_FIELDS,
        expected_properties=SURFACE_CONFIG_EXPECTED_PROPERTIES,
        expected_abstract_properties=SURFACE_CONFIG_EXPECTED_DATACLASS_ABSTRACT_PROPERTIES,
        expected_methods=SURFACE_CONFIG_EXPECTED_METHODS,
    )
]


@pytest.mark.parametrize("config", SURFACE_CONFIG_TEST_DATACLASS_CONFIG, ids=lambda c: c.dataclass_class.__name__)
class TestSurfaceConfigContract(DataclassTestBase):
    pass


# --------------------------
# Tests for RasterSurfaceConfig
# --------------------------
RASTER_SURFACE_CONFIG_EXPECTED_FIELDS = {"width", "height"}
RASTER_SURFACE_CONFIG_EXPECTED_METHODS = {
    "__post_init__",
    "_validate_raster_requirement",
}
RASTER_SURFACE_CONFIG_TEST_DATACLASS_CONFIG = [
    DataclassTestConfig(
        dataclass_class=RasterSurfaceConfig,
        is_abstract=True,
        is_frozen=True,
        expected_fields=RASTER_SURFACE_CONFIG_EXPECTED_FIELDS,
        expected_methods=RASTER_SURFACE_CONFIG_EXPECTED_METHODS,
    )
]


@pytest.mark.parametrize(
    "config", RASTER_SURFACE_CONFIG_TEST_DATACLASS_CONFIG, ids=lambda c: c.dataclass_class.__name__
)
class TestRasterSurfaceConfigContract(DataclassTestBase):
    pass


# --------------------------
# Tests for VectorSurfaceConfig
# --------------------------
VECTOR_SURFACE_CONFIG_EXPECTED_FIELDS = {"fallback_resolution"}
VECTOR_SURFACE_CONFIG_EXPECTED_METHODS = {
    "__post_init__",
    "_validate_fallback_resolution",
    "_validate_vector_requirements",
}
VECTOR_SURFACE_CONFIG_TEST_DATACLASS_CONFIG = [
    DataclassTestConfig(
        dataclass_class=VectorSurfaceConfig,
        is_abstract=True,
        is_frozen=True,
        expected_fields=VECTOR_SURFACE_CONFIG_EXPECTED_FIELDS,
        expected_methods=VECTOR_SURFACE_CONFIG_EXPECTED_METHODS,
    )
]


@pytest.mark.parametrize(
    "config", VECTOR_SURFACE_CONFIG_TEST_DATACLASS_CONFIG, ids=lambda c: c.dataclass_class.__name__
)
class TestVectorSurfaceConfigContract(DataclassTestBase):
    pass


# --------------------------
# Tests for ImageSurfaceConfig
# --------------------------
IMAGE_SURFACE_CONFIG_EXPECTED_FIELDS = {"pixel_format"}
IMAGE_SURFACE_CONFIG_EXPECTED_PROPERTIES = {"surface_type"}
IMAGE_SURFACE_CONFIG_EXPECTED_METHODS = {
    "__post_init__",
    "_validate_pixel_format",
}
IMAGE_SURFACE_TEST_DATACLASS_CONFIG = [
    DataclassTestConfig(
        dataclass_class=ImageSurfaceConfig,
        is_frozen=True,
        expected_fields=IMAGE_SURFACE_CONFIG_EXPECTED_FIELDS,
        expected_properties=IMAGE_SURFACE_CONFIG_EXPECTED_PROPERTIES,
        expected_methods=IMAGE_SURFACE_CONFIG_EXPECTED_METHODS,
    )
]


@pytest.mark.parametrize("config", IMAGE_SURFACE_TEST_DATACLASS_CONFIG, ids=lambda c: c.dataclass_class.__name__)
class TestImageSurfaceConfigContract(DataclassTestBase):
    pass


# --------------------------
# Tests for SVGSurfaceConfig
# --------------------------
SVG_SURFACE_CONFIG_EXPECTED_FIELDS = {"document_unit", "svg_version"}
SVG_SURFACE_CONFIG_EXPECTED_PROPERTIES = {"surface_type"}
SVG_SURFACE_CONFIG_EXPECTED_METHODS: set[str] = {"__post_init__"}
SVG_SURFACE_TEST_DATACLASS_CONFIG = [
    DataclassTestConfig(
        dataclass_class=SVGSurfaceConfig,
        is_frozen=True,
        expected_fields=SVG_SURFACE_CONFIG_EXPECTED_FIELDS,
        expected_properties=SVG_SURFACE_CONFIG_EXPECTED_PROPERTIES,
        expected_methods=SVG_SURFACE_CONFIG_EXPECTED_METHODS,
    )
]


@pytest.mark.parametrize("config", SVG_SURFACE_TEST_DATACLASS_CONFIG, ids=lambda c: c.dataclass_class.__name__)
class TestSVGSurfaceConfigContract(DataclassTestBase):
    pass


# --------------------------
# Tests for PDFSurfaceConfig
# --------------------------
PDF_SURFACE_CONFIG_EXPECTED_FIELDS = {"pdf_version"}
PDF_SURFACE_CONFIG_EXPECTED_PROPERTIES = {"surface_type"}
PDF_SURFACE_CONFIG_EXPECTED_METHODS: set[str] = {"__post_init__"}
PDF_SURFACE_CONFIG_TEST_DATACLASS_CONFIG = [
    DataclassTestConfig(
        dataclass_class=PDFSurfaceConfig,
        is_frozen=True,
        expected_fields=PDF_SURFACE_CONFIG_EXPECTED_FIELDS,
        expected_properties=PDF_SURFACE_CONFIG_EXPECTED_PROPERTIES,
        expected_methods=PDF_SURFACE_CONFIG_EXPECTED_METHODS,
    )
]


@pytest.mark.parametrize("config", PDF_SURFACE_CONFIG_TEST_DATACLASS_CONFIG, ids=lambda c: c.dataclass_class.__name__)
class TestPDFSurfaceConfigContract(DataclassTestBase):
    pass
