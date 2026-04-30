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

from tenderness.image_backend.surface_array_converter import (
    SurfaceArrayBackend,
    SurfaceArrayConverter,
    SurfaceArrayConverterParameters,
    SurfaceArrayResult,
)
from tests._test_utils.class_test import ClassTestBase, ClassTestConfig
from tests._test_utils.dataclass_test import DataclassTestBase, DataclassTestConfig
from tests._test_utils.str_enum_test import StrEnumTestBase, StrEnumTestConfig

# --------------------------
# Tests for SurfaceArrayBackend
# --------------------------
SURFACE_ARRAY_BACKEND_EXPECTED_MEMBERS = {"NUMPY", "TORCH"}
SURFACE_ARRAY_BACKEND_TEST_STR_ENUM_CONFIG = [
    StrEnumTestConfig(
        enum_class=SurfaceArrayBackend,
        expected_members=SURFACE_ARRAY_BACKEND_EXPECTED_MEMBERS,
    )
]


@pytest.mark.parametrize("config", SURFACE_ARRAY_BACKEND_TEST_STR_ENUM_CONFIG, ids=lambda c: c.enum_class.__name__)
class TestSurfaceArrayBackendContract(StrEnumTestBase):
    pass


# --------------------------
# Tests for SurfaceArrayResult
# --------------------------
SURFACE_ARRAY_RESULT_EXPECTED_FIELDS = {"backend", "image_array", "channel_order", "pixel_format", "is_copy"}
SURFACE_ARRAY_RESULT_EXPECTED_PROPERTIES = {"shape", "dtype", "is_premultiplied", "has_alpha"}
SURFACE_ARRAY_RESULT_TEST_DATACLASS_CONFIG = [
    DataclassTestConfig(
        dataclass_class=SurfaceArrayResult,
        has_slots=True,
        expected_fields=SURFACE_ARRAY_RESULT_EXPECTED_FIELDS,
        expected_properties=SURFACE_ARRAY_RESULT_EXPECTED_PROPERTIES,
    )
]


@pytest.mark.parametrize("config", SURFACE_ARRAY_RESULT_TEST_DATACLASS_CONFIG, ids=lambda c: c.dataclass_class.__name__)
class TestSurfaceArrayResultContract(DataclassTestBase):
    pass


# --------------------------
# Tests for SurfaceArrayConverterParameters
# --------------------------
SURFACE_ARRAY_CONVERTER_PARAMETERS_EXPECTED_FIELDS = {"channel_order", "copy", "backend", "finish_after"}
SURFACE_ARRAY_CONVERTER_PARAMETERS_TEST_DATACLASS_CONFIG = [
    DataclassTestConfig(
        dataclass_class=SurfaceArrayConverterParameters,
        has_slots=True,
        expected_fields=SURFACE_ARRAY_CONVERTER_PARAMETERS_EXPECTED_FIELDS,
    )
]


@pytest.mark.parametrize(
    "config", SURFACE_ARRAY_CONVERTER_PARAMETERS_TEST_DATACLASS_CONFIG, ids=lambda c: c.dataclass_class.__name__
)
class TestSurfaceArrayConverterParametersContract(DataclassTestBase):
    pass


# --------------------------
# Tests for SurfaceArrayConverter
# --------------------------
SURFACE_ARRAY_CONVERTER_EXPECTED_METHODS = {
    "surface_to_array",
    "_image_surface_to_array",
    "to_numpy",
    "_reorder_channels_numpy",
}
SURFACE_ARRAY_CONVERTER_TEST_CLASS_CONFIG = [
    ClassTestConfig(
        cls=SurfaceArrayConverter,
        expected_methods=SURFACE_ARRAY_CONVERTER_EXPECTED_METHODS,
    )
]


@pytest.mark.parametrize("config", SURFACE_ARRAY_CONVERTER_TEST_CLASS_CONFIG, ids=lambda c: c.cls.__name__)
class TestSurfaceArrayConverterContract(ClassTestBase):
    pass
