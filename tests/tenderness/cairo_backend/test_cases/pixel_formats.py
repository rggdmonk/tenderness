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

from dataclasses import dataclass
from typing import Any

import cairo

from tenderness.cairo_backend.pixel_formats import (
    ChannelOrder,
    PixelDType,
    PixelFormat,
    PixelOrder,
)
from tenderness.core.color_models import ColorModel


# --------------------------
# Test cases for ChannelOrder
# --------------------------
@dataclass(frozen=True)
class ChannelOrderTestCase:
    test_name: str
    order: ChannelOrder
    has_alpha: bool
    n_channels: int
    is_bgr_base: bool


CHANNEL_ORDER_TEST_CASES = [
    ChannelOrderTestCase(
        test_name="bgr_valid",
        order=ChannelOrder.BGR,
        has_alpha=False,
        n_channels=3,
        is_bgr_base=True,
    ),
    ChannelOrderTestCase(
        test_name="rgb_valid",
        order=ChannelOrder.RGB,
        has_alpha=False,
        n_channels=3,
        is_bgr_base=False,
    ),
    ChannelOrderTestCase(
        test_name="bgra_valid",
        order=ChannelOrder.BGRA,
        has_alpha=True,
        n_channels=4,
        is_bgr_base=True,
    ),
    ChannelOrderTestCase(
        test_name="rgba_valid",
        order=ChannelOrder.RGBA,
        has_alpha=True,
        n_channels=4,
        is_bgr_base=False,
    ),
]


# --------------------------
# Test cases for PixelFormat
# --------------------------
@dataclass(frozen=True, slots=True)
class PixelFormatTestCase:
    test_name: str
    pixel_format: PixelFormat
    format_value: cairo.Format
    format_name: str
    color_model: ColorModel
    pixel_order: PixelOrder
    memory_dtype: PixelDType
    array_dtype: PixelDType
    n_channels: int
    is_packed: bool
    bits_per_pixel: int
    bytes_per_pixel: int
    has_alpha: bool
    is_premultiplied: bool


PIXEL_FORMAT_TEST_CASES = [
    PixelFormatTestCase(
        test_name="valid_rgb24_format",
        pixel_format=PixelFormat.RGB24,
        format_value=cairo.Format.RGB24,
        format_name="RGB24",
        color_model=ColorModel.RGB,
        pixel_order=PixelOrder.BGRX,
        memory_dtype=PixelDType.UINT32,
        array_dtype=PixelDType.UINT8,
        n_channels=4,
        is_packed=False,
        bits_per_pixel=32,
        bytes_per_pixel=4,
        has_alpha=False,
        is_premultiplied=False,
    ),
    PixelFormatTestCase(
        test_name="valid_argb32_format",
        pixel_format=PixelFormat.ARGB32,
        format_value=cairo.Format.ARGB32,
        format_name="ARGB32",
        color_model=ColorModel.RGBA,
        pixel_order=PixelOrder.BGRA,
        memory_dtype=PixelDType.UINT32,
        array_dtype=PixelDType.UINT8,
        n_channels=4,
        is_packed=False,
        bits_per_pixel=32,
        bytes_per_pixel=4,
        has_alpha=True,
        is_premultiplied=True,
    ),
    PixelFormatTestCase(
        test_name="valid_rgb96f_format",
        pixel_format=PixelFormat.RGB96F,
        format_value=cairo.Format.RGB96F,
        format_name="RGB96F",
        color_model=ColorModel.RGB,
        pixel_order=PixelOrder.RGBF,
        memory_dtype=PixelDType.FLOAT32,
        array_dtype=PixelDType.FLOAT32,
        n_channels=3,
        is_packed=False,
        bits_per_pixel=96,
        bytes_per_pixel=12,
        has_alpha=False,
        is_premultiplied=False,
    ),
    PixelFormatTestCase(
        test_name="valid_rgba128f_format",
        pixel_format=PixelFormat.RGBA128F,
        format_value=cairo.Format.RGBA128F,
        format_name="RGBA128F",
        color_model=ColorModel.RGBA,
        pixel_order=PixelOrder.RGBAF,
        memory_dtype=PixelDType.FLOAT32,
        array_dtype=PixelDType.FLOAT32,
        n_channels=4,
        is_packed=False,
        bits_per_pixel=128,
        bytes_per_pixel=16,
        has_alpha=True,
        is_premultiplied=True,
    ),
    PixelFormatTestCase(
        test_name="valid_a8_format",
        pixel_format=PixelFormat.A8,
        format_value=cairo.Format.A8,
        format_name="A8",
        color_model=ColorModel.ALPHA,
        pixel_order=PixelOrder.ALPHA_ONLY,
        memory_dtype=PixelDType.UINT8,
        array_dtype=PixelDType.UINT8,
        n_channels=1,
        is_packed=False,
        bits_per_pixel=8,
        bytes_per_pixel=1,
        has_alpha=True,
        is_premultiplied=False,
    ),
    PixelFormatTestCase(
        test_name="valid_rgb16_565_format",
        pixel_format=PixelFormat.RGB16_565,
        format_value=cairo.Format.RGB16_565,
        format_name="RGB16_565",
        color_model=ColorModel.RGB,
        pixel_order=PixelOrder.RGB_PACKED_565,
        memory_dtype=PixelDType.UINT16,
        array_dtype=PixelDType.UINT16,
        n_channels=3,
        is_packed=True,
        bits_per_pixel=16,
        bytes_per_pixel=2,
        has_alpha=False,
        is_premultiplied=False,
    ),
    PixelFormatTestCase(
        test_name="valid_rgb30_format",
        pixel_format=PixelFormat.RGB30,
        format_value=cairo.Format.RGB30,
        format_name="RGB30",
        color_model=ColorModel.RGB,
        pixel_order=PixelOrder.RGB_PACKED_30,
        memory_dtype=PixelDType.UINT32,
        array_dtype=PixelDType.UINT32,
        n_channels=3,
        is_packed=True,
        bits_per_pixel=32,
        bytes_per_pixel=4,
        has_alpha=False,
        is_premultiplied=False,
    ),
]


# --------------------------
# Test cases for PixelFormat lookup methods
# --------------------------
@dataclass(frozen=True, slots=True)
class LookupTestCase:
    test_name: str
    lookup_key: Any
    expected_format: str
    should_succeed: bool


CAIRO_FORMAT_LOOKUP_TEST_CASES: tuple[LookupTestCase, ...] = (
    LookupTestCase(
        test_name="rgb24_valid",
        lookup_key=cairo.Format.RGB24,
        expected_format="RGB24",
        should_succeed=True,
    ),
    LookupTestCase(
        test_name="argb32_valid",
        lookup_key=cairo.Format.ARGB32,
        expected_format="ARGB32",
        should_succeed=True,
    ),
    LookupTestCase(
        test_name="a8_valid",
        lookup_key=cairo.Format.A8,
        expected_format="A8",
        should_succeed=True,
    ),
    LookupTestCase(
        test_name="a1_invalid",
        lookup_key=cairo.Format.A1,
        expected_format="",
        should_succeed=False,
    ),
)

FORMAT_NAME_LOOKUP_TEST_CASES: tuple[LookupTestCase, ...] = (
    LookupTestCase(
        test_name="rgb24_valid",
        lookup_key="RGB24",
        expected_format="RGB24",
        should_succeed=True,
    ),
    LookupTestCase(
        test_name="argb32_valid",
        lookup_key="ARGB32",
        expected_format="ARGB32",
        should_succeed=True,
    ),
    LookupTestCase(
        test_name="invalid_format_name",
        lookup_key="INVALID_FORMAT",
        expected_format="",
        should_succeed=False,
    ),
    LookupTestCase(
        test_name="lowercase_rgb24",
        lookup_key="rgb24",
        expected_format="",
        should_succeed=False,
    ),
    LookupTestCase(
        test_name="empty_string",
        lookup_key="",
        expected_format="",
        should_succeed=False,
    ),
)


# --------------------------
# Test cases for PixelFormat filter methods
# --------------------------
@dataclass(frozen=True, slots=True)
class FilterTestCase:
    test_name: str
    expected_formats: tuple[str, ...]


FORMATS_WITH_ALPHA_TEST_CASES: tuple[FilterTestCase, ...] = (
    FilterTestCase(
        test_name="formats_with_alpha",
        expected_formats=("ARGB32", "A8", "RGBA128F"),
    ),
)

FORMATS_WITHOUT_ALPHA_TEST_CASES: tuple[FilterTestCase, ...] = (
    FilterTestCase(
        test_name="formats_without_alpha",
        expected_formats=("RGB24", "RGB96F", "RGB16_565", "RGB30"),
    ),
)

PREMULTIPLIED_FORMATS_TEST_CASES: tuple[FilterTestCase, ...] = (
    FilterTestCase(
        test_name="premultiplied_formats",
        expected_formats=("ARGB32", "RGBA128F"),
    ),
)


@dataclass(frozen=True, slots=True)
class ColorModelFilterTestCase:
    test_name: str
    color_model: ColorModel
    expected_formats: tuple[str, ...]


COLOR_MODEL_FILTER_TEST_CASES: tuple[ColorModelFilterTestCase, ...] = (
    ColorModelFilterTestCase(
        test_name="rgb_color_model",
        color_model=ColorModel.RGB,
        expected_formats=("RGB24", "RGB96F", "RGB16_565", "RGB30"),
    ),
    ColorModelFilterTestCase(
        test_name="rgba_color_model",
        color_model=ColorModel.RGBA,
        expected_formats=("ARGB32", "RGBA128F"),
    ),
)


PACKED_FORMATS_TEST_CASES: tuple[FilterTestCase, ...] = (
    FilterTestCase(
        test_name="packed_formats",
        expected_formats=("RGB16_565", "RGB30"),
    ),
)


@dataclass(frozen=True, slots=True)
class ArrayDTypeFilterTestCase:
    test_name: str
    dtype: PixelDType
    expected_formats: tuple[str, ...]


ARRAY_DTYPE_FILTER_TEST_CASES: tuple[ArrayDTypeFilterTestCase, ...] = (
    ArrayDTypeFilterTestCase(
        test_name="uint8_array_dtype",
        dtype=PixelDType.UINT8,
        expected_formats=("RGB24", "ARGB32", "A8"),
    ),
    ArrayDTypeFilterTestCase(
        test_name="uint16_array_dtype",
        dtype=PixelDType.UINT16,
        expected_formats=("RGB16_565",),
    ),
    ArrayDTypeFilterTestCase(
        test_name="uint32_array_dtype",
        dtype=PixelDType.UINT32,
        expected_formats=("RGB30",),
    ),
    ArrayDTypeFilterTestCase(
        test_name="float32_array_dtype",
        dtype=PixelDType.FLOAT32,
        expected_formats=("RGB96F", "RGBA128F"),
    ),
)


@dataclass(frozen=True, slots=True)
class NChannelsFilterTestCase:
    test_name: str
    n_channels: int
    expected_formats: tuple[str, ...]


N_CHANNELS_FILTER_TEST_CASES: tuple[NChannelsFilterTestCase, ...] = (
    NChannelsFilterTestCase(
        test_name="one_channel",
        n_channels=1,
        expected_formats=("A8",),
    ),
    NChannelsFilterTestCase(
        test_name="three_channels",
        n_channels=3,
        expected_formats=("RGB96F", "RGB16_565", "RGB30"),
    ),
    NChannelsFilterTestCase(
        test_name="four_channels",
        n_channels=4,
        expected_formats=("RGB24", "ARGB32", "RGBA128F"),
    ),
    NChannelsFilterTestCase(
        test_name="zero_channels_empty",
        n_channels=0,
        expected_formats=(),
    ),
)
