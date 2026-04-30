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

from typing import cast

import cairo
import numpy  # noqa: ICN001
import pytest

from tenderness.cairo_backend.pixel_formats import (
    ChannelOrder,
    PixelDType,
    PixelFormat,
    PixelFormatInfo,
    PixelOrder,
)
from tenderness.core.color_models import AlphaPosition
from tests.tenderness.cairo_backend.test_cases.pixel_formats import (
    ARRAY_DTYPE_FILTER_TEST_CASES,
    CAIRO_FORMAT_LOOKUP_TEST_CASES,
    CHANNEL_ORDER_TEST_CASES,
    COLOR_MODEL_FILTER_TEST_CASES,
    FORMAT_NAME_LOOKUP_TEST_CASES,
    FORMATS_WITH_ALPHA_TEST_CASES,
    FORMATS_WITHOUT_ALPHA_TEST_CASES,
    N_CHANNELS_FILTER_TEST_CASES,
    PACKED_FORMATS_TEST_CASES,
    PIXEL_FORMAT_TEST_CASES,
    PREMULTIPLIED_FORMATS_TEST_CASES,
    ArrayDTypeFilterTestCase,
    ChannelOrderTestCase,
    ColorModelFilterTestCase,
    FilterTestCase,
    LookupTestCase,
    NChannelsFilterTestCase,
    PixelFormatTestCase,
)


# --------------------------
# Tests for PixelDType
# --------------------------
class TestPixelDType:
    def test_property_return_types(self) -> None:
        for member in PixelDType:
            assert isinstance(member, PixelDType)
            assert isinstance(member.to_numpy, numpy.dtype)

            with pytest.raises(NotImplementedError):
                _ = member.to_torch

            with pytest.raises(NotImplementedError):
                _ = member.is_torch_stable

    def test_properties_raise_error_for_invalid_values(self) -> None:
        invalid_value = "unsupported_dtype_value_for_testing"

        with pytest.raises(AssertionError, match="Expected code to be unreachable"):
            PixelDType.to_numpy.fget(invalid_value)  # type: ignore

        with pytest.raises(NotImplementedError, match="Not implemented yet"):
            PixelDType.to_torch.fget(invalid_value)  # type: ignore

        with pytest.raises(NotImplementedError, match="Not implemented yet"):
            PixelDType.is_torch_stable.fget(invalid_value)  # type: ignore

    def test_to_numpy_mappings(self) -> None:
        assert PixelDType.UINT8.to_numpy == numpy.dtype(numpy.uint8)
        assert PixelDType.UINT16.to_numpy == numpy.dtype(numpy.uint16)
        assert PixelDType.UINT32.to_numpy == numpy.dtype(numpy.uint32)
        assert PixelDType.FLOAT32.to_numpy == numpy.dtype(numpy.float32)


# --------------------------
# Tests for ChannelOrder
# --------------------------
class TestChannelOrder:
    def test_property_return_types(self) -> None:
        for member in ChannelOrder:
            assert isinstance(member, ChannelOrder)
            assert isinstance(member.has_alpha, bool)
            assert isinstance(member.n_channels, int)
            assert isinstance(member.is_bgr_base, bool)

    @pytest.mark.parametrize("test_case", CHANNEL_ORDER_TEST_CASES, ids=lambda c: c.test_name)
    def test_channel_order_properties(self, test_case: ChannelOrderTestCase) -> None:
        assert test_case.order.has_alpha is test_case.has_alpha
        assert test_case.order.n_channels == test_case.n_channels
        assert test_case.order.is_bgr_base is test_case.is_bgr_base

    def test_unreachable_branches(self) -> None:
        """Force the default case in match statements for coverage."""
        invalid_order = cast("ChannelOrder", "INVALID")

        with pytest.raises(AttributeError):
            _ = invalid_order.has_alpha

        with pytest.raises(AttributeError):
            _ = invalid_order.n_channels

        with pytest.raises(AttributeError):
            _ = invalid_order.is_bgr_base


# --------------------------
# Tests for PixelOrder
# --------------------------
class TestPixelOrder:
    def test_property_return_types(self) -> None:
        for member in PixelOrder:
            assert isinstance(member, PixelOrder)
            assert isinstance(member.has_alpha, bool)
            assert isinstance(member.alpha_position, AlphaPosition)
            assert isinstance(member.native_channel_order, ChannelOrder | None)

    def test_properties_raise_error_for_invalid_values(self) -> None:
        invalid_value = "unsupported_order_value_for_testing"

        with pytest.raises(AssertionError, match="Expected code to be unreachable"):
            PixelOrder.has_alpha.fget(invalid_value)  # type: ignore

        with pytest.raises(AssertionError, match="Expected code to be unreachable"):
            PixelOrder.alpha_position.fget(invalid_value)  # type: ignore

        with pytest.raises(AssertionError, match="Expected code to be unreachable"):
            PixelOrder.native_channel_order.fget(invalid_value)  # type: ignore

    def test_bgra_properties(self) -> None:
        bgra = PixelOrder.BGRA
        assert bgra.has_alpha is True
        assert bgra.alpha_position is AlphaPosition.LAST
        assert bgra.native_channel_order == ChannelOrder.BGRA

    def test_bgrx_properties(self) -> None:
        bgrx = PixelOrder.BGRX
        assert bgrx.has_alpha is False
        assert bgrx.alpha_position is AlphaPosition.NONE
        assert bgrx.native_channel_order == ChannelOrder.BGR

    def test_rgb_packed_565_properties(self) -> None:
        rgb565 = PixelOrder.RGB_PACKED_565
        assert rgb565.has_alpha is False
        assert rgb565.alpha_position is AlphaPosition.NONE
        assert rgb565.native_channel_order is None

    def test_rgb_packed_30_properties(self) -> None:
        rgb30 = PixelOrder.RGB_PACKED_30
        assert rgb30.has_alpha is False
        assert rgb30.alpha_position is AlphaPosition.NONE
        assert rgb30.native_channel_order is None

    def test_alpha_only_properties(self) -> None:
        alpha_only = PixelOrder.ALPHA_ONLY
        assert alpha_only.has_alpha is True
        assert alpha_only.alpha_position is AlphaPosition.ONLY
        assert alpha_only.native_channel_order is None

    def test_rgbf_properties(self) -> None:
        rgbf = PixelOrder.RGBF
        assert rgbf.has_alpha is False
        assert rgbf.alpha_position is AlphaPosition.NONE
        assert rgbf.native_channel_order is ChannelOrder.RGB

    def test_rgbaf_properties(self) -> None:
        rgbaf = PixelOrder.RGBAF
        assert rgbaf.has_alpha is True
        assert rgbaf.alpha_position is AlphaPosition.LAST
        assert rgbaf.native_channel_order is ChannelOrder.RGBA


# --------------------------
# Tests for PixelFormatInfo
# --------------------------


# --------------------------
# Tests for PixelFormat
# --------------------------
class TestPixelFormat:
    def test_members_is_expected_type(self) -> None:
        for member in PixelFormat:
            assert isinstance(member.value, PixelFormatInfo), (
                f"{member.name}.value should be {PixelFormatInfo.__name__}, got {type(member.value)}"
            )

    def test_format_values_property_uniqueness(self) -> None:
        format_values = [sf.format_value for sf in PixelFormat]
        for fv in format_values:
            assert isinstance(fv, cairo.Format), f"format_value should be {cairo.Format.__name__}, got {type(fv)}"
        assert len(format_values) == len(set(format_values)), "Duplicate format_value values found"

    def test_format_names_property_uniqueness(self) -> None:
        format_names = [sf.format_name for sf in PixelFormat]
        for fn in format_names:
            assert isinstance(fn, str), f"format_name should be str, got {type(fn)}"
        assert len(format_names) == len(set(format_names)), "Duplicate format_name values found"

    @pytest.mark.parametrize("test_case", PIXEL_FORMAT_TEST_CASES, ids=lambda c: c.test_name)
    def test_pixel_format(self, test_case: PixelFormatTestCase) -> None:
        fmt = test_case.pixel_format

        assert fmt.format_value == test_case.format_value
        assert fmt.format_name == test_case.format_name
        assert fmt.color_model == test_case.color_model
        assert fmt.pixel_order == test_case.pixel_order

        assert fmt.memory_dtype == test_case.memory_dtype
        assert fmt.array_dtype == test_case.array_dtype
        assert fmt.n_channels == test_case.n_channels
        assert fmt.is_packed is test_case.is_packed
        assert fmt.bits_per_pixel == test_case.bits_per_pixel
        assert fmt.bytes_per_pixel == test_case.bytes_per_pixel

        assert isinstance(fmt.description, str)

        assert fmt.has_alpha is test_case.has_alpha
        assert fmt.is_premultiplied is test_case.is_premultiplied


class TestPixelFormatLookupMethods:
    """Tests for lookup/factory methods."""

    @pytest.mark.parametrize("test_case", CAIRO_FORMAT_LOOKUP_TEST_CASES, ids=lambda tc: tc.test_name)
    def test_from_cairo_format(self, test_case: LookupTestCase) -> None:
        if test_case.should_succeed:
            result = PixelFormat.from_cairo_format(test_case.lookup_key)
            assert result == PixelFormat[test_case.expected_format]
            assert result.format_value == test_case.lookup_key
        else:
            with pytest.raises(ValueError, match=r"No matching "):
                PixelFormat.from_cairo_format(test_case.lookup_key)

    def test_from_cairo_format_error_message_content(self) -> None:
        with pytest.raises(match="No matching "):
            PixelFormat.from_cairo_format("TEST_INVALID_CAIRO_FORMAT")  # type: ignore

    def test_from_cairo_format_roundtrip(self) -> None:
        for pixel_format in PixelFormat:
            cairo_format = pixel_format.format_value
            result = PixelFormat.from_cairo_format(cairo_format)
            assert result == pixel_format

    @pytest.mark.parametrize("test_case", FORMAT_NAME_LOOKUP_TEST_CASES, ids=lambda tc: tc.test_name)
    def test_from_format_name(self, test_case: LookupTestCase) -> None:
        if test_case.should_succeed:
            result = PixelFormat.from_format_name(test_case.lookup_key)
            assert result == PixelFormat[test_case.expected_format]
            assert result.format_name == test_case.lookup_key
        else:
            with pytest.raises(match=r"No matching "):
                PixelFormat.from_format_name(test_case.lookup_key)

    def test_from_format_name_error_message_content(self) -> None:
        with pytest.raises(match="No matching "):
            PixelFormat.from_format_name("INVALID")

    def test_from_format_name_roundtrip(self) -> None:
        for pixel_format in PixelFormat:
            format_name = pixel_format.format_name
            result = PixelFormat.from_format_name(format_name)
            assert result == pixel_format


class TestPixelFormatFilterMethods:
    """Tests for filter methods that return lists of formats."""

    @pytest.mark.parametrize("test_case", FORMATS_WITH_ALPHA_TEST_CASES, ids=lambda tc: tc.test_name)
    def test_get_formats_with_alpha(self, test_case: FilterTestCase) -> None:
        formats = PixelFormat.get_formats_with_alpha()

        assert isinstance(formats, list)
        assert all(fmt.has_alpha for fmt in formats)

        expected = [PixelFormat[name] for name in test_case.expected_formats]
        assert set(formats) == set(expected)

    @pytest.mark.parametrize("test_case", FORMATS_WITHOUT_ALPHA_TEST_CASES, ids=lambda tc: tc.test_name)
    def test_get_formats_without_alpha(self, test_case: FilterTestCase) -> None:
        formats = PixelFormat.get_formats_without_alpha()

        assert isinstance(formats, list)
        assert all(not fmt.has_alpha for fmt in formats)

        expected = [PixelFormat[name] for name in test_case.expected_formats]
        assert set(formats) == set(expected)

    def test_formats_with_and_without_alpha_are_complementary(self) -> None:
        with_alpha = set(PixelFormat.get_formats_with_alpha())
        without_alpha = set(PixelFormat.get_formats_without_alpha())
        all_formats = set(PixelFormat)

        # should be disjoint (no overlap)
        assert with_alpha.isdisjoint(without_alpha)
        # should cover all formats exactly
        assert with_alpha | without_alpha == all_formats

    @pytest.mark.parametrize("test_case", COLOR_MODEL_FILTER_TEST_CASES, ids=lambda tc: tc.test_name)
    def test_get_formats_by_color_model(self, test_case: ColorModelFilterTestCase) -> None:
        formats = PixelFormat.get_formats_by_color_model(test_case.color_model)

        assert isinstance(formats, list)
        assert all(fmt.color_model == test_case.color_model for fmt in formats)

        expected = [PixelFormat[name] for name in test_case.expected_formats]
        assert formats == expected

    def test_get_formats_by_color_model_covers_all_formats(self) -> None:
        # get all unique color models from the enum
        color_models = {fmt.color_model for fmt in PixelFormat}

        all_found_formats = set()
        for color_model in color_models:
            formats = PixelFormat.get_formats_by_color_model(color_model)
            all_found_formats.update(formats)

        # should cover all formats exactly
        assert all_found_formats == set(PixelFormat)

    @pytest.mark.parametrize("test_case", PREMULTIPLIED_FORMATS_TEST_CASES, ids=lambda tc: tc.test_name)
    def test_get_premultiplied_formats(self, test_case: FilterTestCase) -> None:
        formats = PixelFormat.get_premultiplied_formats()

        assert isinstance(formats, list)
        assert all(fmt.is_premultiplied for fmt in formats)

        expected = [PixelFormat[name] for name in test_case.expected_formats]
        assert formats == expected

    def test_premultiplied_formats_have_alpha(self) -> None:
        premultiplied = PixelFormat.get_premultiplied_formats()
        assert all(fmt.has_alpha for fmt in premultiplied)

    @pytest.mark.parametrize("test_case", PACKED_FORMATS_TEST_CASES, ids=lambda tc: tc.test_name)
    def test_get_packed_formats(self, test_case: FilterTestCase) -> None:
        formats = PixelFormat.get_packed_formats()

        assert isinstance(formats, list)
        assert all(fmt.is_packed for fmt in formats)

        expected = [PixelFormat[name] for name in test_case.expected_formats]
        assert set(formats) == set(expected)

    def test_packed_and_unpacked_formats_are_complementary(self) -> None:
        packed = set(PixelFormat.get_packed_formats())
        unpacked = {fmt for fmt in PixelFormat if not fmt.is_packed}

        assert packed.isdisjoint(unpacked)
        assert packed | unpacked == set(PixelFormat)

    @pytest.mark.parametrize("test_case", ARRAY_DTYPE_FILTER_TEST_CASES, ids=lambda tc: tc.test_name)
    def test_get_formats_by_array_dtype(self, test_case: ArrayDTypeFilterTestCase) -> None:
        formats = PixelFormat.get_formats_by_array_dtype(test_case.dtype)

        assert isinstance(formats, list)
        assert all(fmt.array_dtype == test_case.dtype for fmt in formats)

        expected = [PixelFormat[name] for name in test_case.expected_formats]
        assert set(formats) == set(expected)

    def test_get_formats_by_array_dtype_covers_all_formats(self) -> None:
        dtypes = {fmt.array_dtype for fmt in PixelFormat}

        all_found_formats = set()
        for dtype in dtypes:
            formats = PixelFormat.get_formats_by_array_dtype(dtype)
            all_found_formats.update(formats)

        assert all_found_formats == set(PixelFormat)

    @pytest.mark.parametrize("test_case", N_CHANNELS_FILTER_TEST_CASES, ids=lambda tc: tc.test_name)
    def test_get_formats_by_n_channels(self, test_case: NChannelsFilterTestCase) -> None:
        formats = PixelFormat.get_formats_by_n_channels(test_case.n_channels)

        assert isinstance(formats, list)
        assert all(fmt.n_channels == test_case.n_channels for fmt in formats)

        expected = [PixelFormat[name] for name in test_case.expected_formats]
        assert set(formats) == set(expected)

    def test_get_formats_by_n_channels_covers_all_formats(self) -> None:
        all_n_channels = {fmt.n_channels for fmt in PixelFormat}

        all_found_formats = set()
        for n in all_n_channels:
            formats = PixelFormat.get_formats_by_n_channels(n)
            all_found_formats.update(formats)

        assert all_found_formats == set(PixelFormat)
