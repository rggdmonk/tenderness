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

from tenderness.core.image_formats import ImageFormat, ImageFormatInfo
from tests._test_utils.dataclass_test import DataclassTestBase, DataclassTestConfig
from tests._test_utils.enum_test import EnumTestBase, EnumTestConfig

# --------------------------
# Tests for ImageFormatInfo
# --------------------------
IMAGE_FORMAT_INFO_EXPECTED_MEMBERS = {
    "extension",
    "supports_alpha",
    "supports_compression",
    "is_vector",
}
IMAGE_FORMAT_INFO_TEST_DATACLASS_CONFIG = [
    DataclassTestConfig(
        dataclass_class=ImageFormatInfo,
        has_slots=True,
        is_frozen=True,
        expected_fields=IMAGE_FORMAT_INFO_EXPECTED_MEMBERS,
    )
]


@pytest.mark.parametrize("config", IMAGE_FORMAT_INFO_TEST_DATACLASS_CONFIG, ids=lambda c: c.dataclass_class.__name__)
class TestImageFormatInfoContract(DataclassTestBase):
    pass


# --------------------------
# Tests for ImageFormat
# --------------------------
IMAGE_FORMAT_EXPECTED_MEMBERS = {"PNG", "JPEG", "SVG", "PDF"}
IMAGE_FORMAT_EXPECTED_PROPERTIES = {
    "extension",
    "supports_alpha",
    "supports_compression",
    "is_vector",
}
IMAGE_FORMAT_EXPECTED_CLASS_METHODS = {
    "_lookup_format",
    "from_extension",
    "get_formats_with_alpha",
    "get_vector_formats",
    "get_raster_formats",
}
IMAGE_FORMAT_TEST_ENUM_CONFIG = [
    EnumTestConfig(
        enum_class=ImageFormat,
        expected_members=IMAGE_FORMAT_EXPECTED_MEMBERS,
        expected_properties=IMAGE_FORMAT_EXPECTED_PROPERTIES,
        expected_class_methods=IMAGE_FORMAT_EXPECTED_CLASS_METHODS,
    )
]


@pytest.mark.parametrize("config", IMAGE_FORMAT_TEST_ENUM_CONFIG, ids=lambda c: c.enum_class.__name__)
class TestImageFormatContract(EnumTestBase):
    pass
