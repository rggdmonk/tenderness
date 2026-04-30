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

from tenderness.cairo_backend.pixel_formats import (
    ChannelOrder,
    PixelDType,
    PixelFormat,
    PixelFormatInfo,
    PixelOrder,
)
from tests._test_utils.dataclass_test import DataclassTestBase, DataclassTestConfig
from tests._test_utils.enum_test import EnumTestBase, EnumTestConfig
from tests._test_utils.str_enum_test import StrEnumTestBase, StrEnumTestConfig

# --------------------------
# Tests for PixelDType
# --------------------------
PIXEL_DTYPE_EXPECTED_MEMBERS = {"UINT8", "UINT16", "UINT32", "FLOAT32"}
PIXEL_DTYPE_EXPECTED_PROPERTIES = {"to_numpy", "to_torch", "is_torch_stable"}
PIXEL_DTYPE_TEST_STR_ENUM_CONFIG = [
    StrEnumTestConfig(
        enum_class=PixelDType,
        expected_members=PIXEL_DTYPE_EXPECTED_MEMBERS,
        expected_properties=PIXEL_DTYPE_EXPECTED_PROPERTIES,
    )
]


@pytest.mark.parametrize("config", PIXEL_DTYPE_TEST_STR_ENUM_CONFIG, ids=lambda c: c.enum_class.__name__)
class TestPixelDTypeContract(StrEnumTestBase):
    pass


# --------------------------
# Tests for ChannelOrder
# --------------------------
CHANNEL_ORDER_EXPECTED_MEMBERS = {"BGR", "BGRA", "RGB", "RGBA"}
CHANNEL_ORDER_EXPECTED_PROPERTIES = {"has_alpha", "n_channels", "is_bgr_base"}
CHANNEL_ORDER_TEST_STR_ENUM_CONFIG = [
    StrEnumTestConfig(
        enum_class=ChannelOrder,
        expected_members=CHANNEL_ORDER_EXPECTED_MEMBERS,
        expected_properties=CHANNEL_ORDER_EXPECTED_PROPERTIES,
    )
]


@pytest.mark.parametrize("config", CHANNEL_ORDER_TEST_STR_ENUM_CONFIG, ids=lambda c: c.enum_class.__name__)
class TestChannelOrderContract(StrEnumTestBase):
    pass


# --------------------------
# Tests for PixelOrder
# --------------------------
PIXEL_ORDER_EXPECTED_MEMBERS = {"BGRA", "BGRX", "RGB_PACKED_565", "RGB_PACKED_30", "ALPHA_ONLY", "RGBF", "RGBAF"}
PIXEL_ORDER_EXPECTED_PROPERTIES = {"has_alpha", "alpha_position", "native_channel_order"}
PIXEL_ORDER_TEST_STR_ENUM_CONFIG = [
    StrEnumTestConfig(
        enum_class=PixelOrder,
        expected_members=PIXEL_ORDER_EXPECTED_MEMBERS,
        expected_properties=PIXEL_ORDER_EXPECTED_PROPERTIES,
    )
]


@pytest.mark.parametrize("config", PIXEL_ORDER_TEST_STR_ENUM_CONFIG, ids=lambda c: c.enum_class.__name__)
class TestPixelOrderContract(StrEnumTestBase):
    pass


# --------------------------
# Tests for PixelFormatInfo
# --------------------------
PIXEL_FORMAT_INFO_EXPECTED_FIELDS = {
    "format_value",
    "format_name",
    "color_model",
    "pixel_order",
    "memory_dtype",
    "array_dtype",
    "n_channels",
    "is_packed",
    "description",
    "bits_per_pixel",
    "bytes_per_pixel",
}
PIXEL_FORMAT_INFO_EXPECTED_PROPERTIES = {"is_premultiplied", "has_alpha"}
PIXEL_FORMAT_INFO_TEST_DATACLASS_CONFIG = [
    DataclassTestConfig(
        dataclass_class=PixelFormatInfo,
        has_slots=True,
        is_frozen=True,
        expected_fields=PIXEL_FORMAT_INFO_EXPECTED_FIELDS,
        expected_properties=PIXEL_FORMAT_INFO_EXPECTED_PROPERTIES,
    )
]


@pytest.mark.parametrize("config", PIXEL_FORMAT_INFO_TEST_DATACLASS_CONFIG, ids=lambda c: c.dataclass_class.__name__)
class TestPixelFormatInfoContract(DataclassTestBase):
    pass


# --------------------------
# Tests for PixelFormat
# --------------------------
PIXEL_FORMAT_EXPECTED_MEMBERS = {"RGB24", "ARGB32", "A8", "RGBA128F", "RGB96F", "RGB16_565", "RGB30"}
PIXEL_FORMAT_EXPECTED_PROPERTIES = {
    "format_value",
    "format_name",
    "color_model",
    "pixel_order",
    "description",
    "is_premultiplied",
    "has_alpha",
    "array_dtype",
    "bits_per_pixel",
    "bytes_per_pixel",
    "is_packed",
    "memory_dtype",
    "n_channels",
}
PIXEL_FORMAT_EXPECTED_CLASSMETHODS = {
    "_lookup_format",
    "from_cairo_format",
    "from_format_name",
    "get_formats_with_alpha",
    "get_formats_without_alpha",
    "get_formats_by_color_model",
    "get_premultiplied_formats",
    "get_packed_formats",
    "get_formats_by_array_dtype",
    "get_formats_by_n_channels",
}
PIXEL_FORMAT_TEST_ENUM_CONFIG = [
    EnumTestConfig(
        enum_class=PixelFormat,
        expected_members=PIXEL_FORMAT_EXPECTED_MEMBERS,
        expected_properties=PIXEL_FORMAT_EXPECTED_PROPERTIES,
        expected_class_methods=PIXEL_FORMAT_EXPECTED_CLASSMETHODS,
    ),
]


@pytest.mark.parametrize("config", PIXEL_FORMAT_TEST_ENUM_CONFIG, ids=lambda c: c.enum_class.__name__)
class TestPixelFormatContract(EnumTestBase):
    pass
