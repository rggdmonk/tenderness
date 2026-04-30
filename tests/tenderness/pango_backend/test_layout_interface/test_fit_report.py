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

from typing import TYPE_CHECKING

import gi
import pytest

from tenderness.pango_backend.layout_interface_geometry import (
    ClippedText,
    ExtentsMode,
    FitsResult,
    HeightDeviceUnits,
    HeightLineLimit,
    HeightSingleLine,
    LayoutFitReport,
    LayoutRect,
    WidthDeviceUnits,
    WidthUnconstrained,
)

gi.require_version("Pango", "1.0")
gi.require_version("PangoCairo", "1.0")


from gi.repository import Pango  # noqa: E402

if TYPE_CHECKING:
    from tenderness.pango_backend.layout_interface import (
        LayoutInterface,
    )


def _set_up_layout_interface(
    layout_interface: LayoutInterface,
    text: str,
    width_du: float = 200.0,
    height_du: float | None = None,
) -> None:
    layout_interface.set_text(text=text)
    layout_interface.width_device_units = width_du
    if height_du is not None:
        layout_interface.height_device_units = height_du


class TestLayoutFitReport:
    def test_return_types(self, layout_interface: LayoutInterface) -> None:
        _set_up_layout_interface(layout_interface=layout_interface, text="Hello", width_du=200.0, height_du=None)
        result = layout_interface.get_layout_fit_report()
        assert isinstance(result, LayoutFitReport)
        assert isinstance(result.fits_logical, FitsResult)
        assert isinstance(result.fits_ink, FitsResult)
        assert isinstance(result.clipped_text, ClippedText)


# ---------------------------------------------------------------------------
# FitsResult fields
# ---------------------------------------------------------------------------
class TestFitsResultFields:
    def test_fields(self, layout_interface: LayoutInterface) -> None:
        _set_up_layout_interface(layout_interface=layout_interface, text="Hello", width_du=200.0, height_du=200.0)
        result = layout_interface.get_layout_fit_report()

        assert result.fits_logical.extents_mode == ExtentsMode.LOGICAL
        assert result.fits_ink.extents_mode == ExtentsMode.INK

        assert isinstance(result.fits_logical.width, bool)
        assert isinstance(result.fits_logical.height, bool)
        assert isinstance(result.fits_ink.width, bool)
        assert isinstance(result.fits_ink.height, bool)
        assert result.fits_logical.fit_both == (result.fits_logical.width and result.fits_logical.height)
        assert result.fits_ink.fit_both == (result.fits_ink.width and result.fits_ink.height)

        assert result.fits_logical.ellipsis == layout_interface.ellipsize
        assert result.fits_logical.wrap == layout_interface.wrap

        assert result.fits_ink.ellipsis == layout_interface.ellipsize
        assert result.fits_ink.wrap == layout_interface.wrap

        assert isinstance(result.fits_logical.rect, LayoutRect)
        assert isinstance(result.fits_ink.rect, LayoutRect)

        assert isinstance(result.fits_logical.width_device_units, WidthDeviceUnits)
        assert result.fits_logical.width_device_units.width == pytest.approx(200.0, abs=1 / Pango.SCALE)
        assert isinstance(result.fits_logical.height_device_units, HeightDeviceUnits)
        assert result.fits_logical.height_device_units.height == pytest.approx(200.0, abs=1 / Pango.SCALE)

        assert isinstance(result.fits_ink.width_device_units, WidthDeviceUnits)
        assert result.fits_ink.width_device_units.width == pytest.approx(200.0, abs=1 / Pango.SCALE)
        assert isinstance(result.fits_ink.height_device_units, HeightDeviceUnits)
        assert result.fits_ink.height_device_units.height == pytest.approx(200.0, abs=1 / Pango.SCALE)

        assert result.fits_ink.unknown_glyphs_count == layout_interface.unknown_glyphs_count
        assert result.fits_logical.unknown_glyphs_count == layout_interface.unknown_glyphs_count


# ---------------------------------------------------------------------------
# Height fits: HeightDeviceUnits
# ---------------------------------------------------------------------------
class TestHeightFitsDeviceUnits:
    def test_short_text_fits_height(self, layout_interface: LayoutInterface) -> None:
        _set_up_layout_interface(layout_interface=layout_interface, text="Hello", width_du=200.0, height_du=200.0)
        result = layout_interface.get_layout_fit_report()
        assert result.fits_logical.height is True
        assert result.clipped_text.has_clipped is False

    def test_long_text_does_not_fit_height(self, layout_interface: LayoutInterface) -> None:
        text = "Line one\nLine two\nLine three\nLine four\nLine five"
        _set_up_layout_interface(layout_interface=layout_interface, text=text, width_du=200.0, height_du=30.0)
        result = layout_interface.get_layout_fit_report()
        assert result.fits_logical.height is False
        assert result.clipped_text.has_clipped is True

    def test_clipped_visible_plus_clipped_equals_full(self, layout_interface: LayoutInterface) -> None:
        text = "Line one\nLine two\nLine three"
        _set_up_layout_interface(layout_interface=layout_interface, text=text, width_du=200.0, height_du=30.0)
        result = layout_interface.get_layout_fit_report()
        ct = result.clipped_text
        assert ct.visible + ct.clipped == text

    def test_clipped_char_index_is_byte_offset(self, layout_interface: LayoutInterface) -> None:
        text = "Hello\nWorld"
        _set_up_layout_interface(layout_interface=layout_interface, text=text, width_du=200.0, height_du=10.0)
        result = layout_interface.get_layout_fit_report()
        ct = result.clipped_text
        encoded = text.encode("utf-8")
        assert encoded[: ct.clipped_char_byte_index].decode("utf-8") == ct.visible

    def test_single_line_text_last_visible_line_zero(self, layout_interface: LayoutInterface) -> None:
        _set_up_layout_interface(layout_interface=layout_interface, text="Hello", width_du=200.0, height_du=200.0)
        result = layout_interface.get_layout_fit_report()
        assert result.clipped_text.last_visible_line == 0

    def test_multiline_clipped_last_visible_line(self, layout_interface: LayoutInterface) -> None:
        text = "Line one\nLine two\nLine three"
        _set_up_layout_interface(layout_interface=layout_interface, text=text, width_du=200.0, height_du=30.0)
        result = layout_interface.get_layout_fit_report()
        assert result.clipped_text.last_visible_line < 2

    def test_large_height_no_clipping(self, layout_interface: LayoutInterface) -> None:
        text = "Line one\nLine two\nLine three"
        _set_up_layout_interface(layout_interface=layout_interface, text=text, width_du=200.0, height_du=9999.0)
        result = layout_interface.get_layout_fit_report()
        assert result.fits_logical.height is True
        assert result.clipped_text.has_clipped is False
        assert result.clipped_text.visible == text
        assert result.clipped_text.clipped == ""


# ---------------------------------------------------------------------------
# Height fits: HeightSingleLine
# ---------------------------------------------------------------------------
class TestHeightFitsSingleLine:
    def test_single_line_mode_always_fits_height(self, layout_interface: LayoutInterface) -> None:
        layout_interface.set_text("Hello\nWorld\nThird line")
        layout_interface.width_device_units = 200.0
        layout_interface.height_device_units = HeightSingleLine()
        result = layout_interface.get_layout_fit_report()
        assert result.fits_logical.height is True


# ---------------------------------------------------------------------------
# Height fits: HeightLineLimit
# ---------------------------------------------------------------------------
class TestHeightFitsLineLimit:
    def test_fits_when_not_ellipsized(self, layout_interface: LayoutInterface) -> None:
        layout_interface.set_text("Short")
        layout_interface.width_device_units = 200.0
        layout_interface.height_device_units = HeightLineLimit(lines=3)
        result = layout_interface.get_layout_fit_report()
        assert result.fits_logical.height is True

    def test_does_not_fit_when_ellipsized(self, layout_interface: LayoutInterface) -> None:
        layout_interface.set_text("Line one\nLine two\nLine three\nLine four")
        layout_interface.width_device_units = 200.0
        layout_interface.height_device_units = HeightLineLimit(lines=2)
        layout_interface.ellipsize = Pango.EllipsizeMode.END
        result = layout_interface.get_layout_fit_report()
        if layout_interface.is_ellipsized:
            assert result.fits_logical.height is False


# ---------------------------------------------------------------------------
# Width fits
# ---------------------------------------------------------------------------
class TestWidthFits:
    def test_unconstrained_width_always_fits(self, layout_interface: LayoutInterface) -> None:
        layout_interface.set_text("Hello world")
        layout_interface.width_device_units = WidthUnconstrained()
        result = layout_interface.get_layout_fit_report()
        assert result.fits_logical.width is True
        assert result.fits_ink.width is True

    def test_wide_enough_fits(self, layout_interface: LayoutInterface) -> None:
        layout_interface.set_text("Hi")
        layout_interface.width_device_units = 500.0
        layout_interface.height_device_units = HeightSingleLine()
        result = layout_interface.get_layout_fit_report()
        assert result.fits_logical.width is True


# ---------------------------------------------------------------------------
# ClippedText: multibyte scripts
# ---------------------------------------------------------------------------
class TestClippedTextMultibyte:
    def test_arabic_byte_boundary(self, layout_interface: LayoutInterface) -> None:
        text = "مرحبا\nكيف حالك\nأتمنى لك"
        _set_up_layout_interface(layout_interface=layout_interface, text=text, width_du=200.0, height_du=20.0)
        result = layout_interface.get_layout_fit_report()
        ct = result.clipped_text
        assert ct.visible.encode("utf-8") + ct.clipped.encode("utf-8") == text.encode("utf-8")

    def test_cjk_byte_boundary(self, layout_interface: LayoutInterface) -> None:
        text = "こんにちは\n世界です\nよろしく"
        _set_up_layout_interface(layout_interface=layout_interface, text=text, width_du=200.0, height_du=20.0)
        result = layout_interface.get_layout_fit_report()
        ct = result.clipped_text
        assert ct.visible.encode("utf-8") + ct.clipped.encode("utf-8") == text.encode("utf-8")

    def test_emoji_byte_boundary(self, layout_interface: LayoutInterface) -> None:
        text = "👋🌍\n🔥💧\n🎉🎊"
        _set_up_layout_interface(layout_interface=layout_interface, text=text, width_du=200.0, height_du=20.0)
        result = layout_interface.get_layout_fit_report()
        ct = result.clipped_text
        assert ct.visible.encode("utf-8") + ct.clipped.encode("utf-8") == text.encode("utf-8")

    def test_no_clipping_empty_clipped_string(self, layout_interface: LayoutInterface) -> None:
        _set_up_layout_interface(layout_interface=layout_interface, text="Hello", width_du=200.0, height_du=999.0)
        result = layout_interface.get_layout_fit_report()
        assert result.clipped_text.clipped == ""
        assert result.clipped_text.has_clipped is False

    def test_clipping_non_empty_clipped_string(self, layout_interface: LayoutInterface) -> None:
        text = "Line one\nLine two\nLine three"
        _set_up_layout_interface(layout_interface=layout_interface, text=text, width_du=200.0, height_du=10.0)
        result = layout_interface.get_layout_fit_report()
        assert result.clipped_text.has_clipped is True
        assert result.clipped_text.clipped != ""
