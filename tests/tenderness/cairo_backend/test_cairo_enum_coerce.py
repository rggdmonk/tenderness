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

import cairo
import pytest

from tenderness.cairo_backend.cairo_enum_coerce import (
    AntialiasStr,
    CairoEnumCoerce,
    CairoEnumMap,
    ColorModeStr,
    HintMetricsStr,
    HintStyleStr,
    OperatorStr,
    PDFVersionStr,
    SubpixelOrderStr,
    SVGUnitStr,
    SVGVersionStr,
)


# --------------------------
# Tests for CairoEnumCoerce
# --------------------------
class TestCairoEnumCoerce:
    # ------------------------------------------------------------------
    # build_map
    # ------------------------------------------------------------------
    def test_build_map_contains_expected_keys(self) -> None:
        mapping = CairoEnumCoerce.build_map(cairo.Antialias)
        assert "default" in mapping
        assert "none" in mapping
        assert "gray" in mapping
        assert "subpixel" in mapping

    def test_build_map_values_are_cairo_members(self) -> None:
        mapping = CairoEnumCoerce.build_map(cairo.Antialias)
        assert mapping["default"] == cairo.Antialias.DEFAULT
        assert mapping["none"] == cairo.Antialias.NONE
        assert mapping["gray"] == cairo.Antialias.GRAY
        assert mapping["subpixel"] == cairo.Antialias.SUBPIXEL

    def test_build_map_excludes_private_attrs(self) -> None:
        mapping = CairoEnumCoerce.build_map(cairo.Antialias)
        assert not any(k.startswith("_") for k in mapping)

    def test_build_map_keys_are_lowercase(self) -> None:
        mapping = CairoEnumCoerce.build_map(cairo.Antialias)
        assert all(k == k.lower() for k in mapping)

    def test_build_map_is_not_empty(self) -> None:
        assert len(CairoEnumCoerce.build_map(cairo.Antialias)) == 7
        assert len(CairoEnumCoerce.build_map(cairo.HintStyle)) == 5
        assert len(CairoEnumCoerce.build_map(cairo.SubpixelOrder)) == 5
        assert len(CairoEnumCoerce.build_map(cairo.HintMetrics)) == 3
        assert len(CairoEnumCoerce.build_map(cairo.ColorMode)) == 3
        assert len(CairoEnumCoerce.build_map(cairo.Operator)) == 29
        assert len(CairoEnumCoerce.build_map(cairo.SVGUnit)) == 10
        assert len(CairoEnumCoerce.build_map(cairo.SVGVersion)) == 2
        assert len(CairoEnumCoerce.build_map(cairo.PDFVersion)) == 4

    # ------------------------------------------------------------------
    # coerce — str input
    # ------------------------------------------------------------------
    @pytest.mark.parametrize(
        ("value", "expected"),
        [
            ("default", cairo.Antialias.DEFAULT),
            ("none", cairo.Antialias.NONE),
            ("gray", cairo.Antialias.GRAY),
            ("subpixel", cairo.Antialias.SUBPIXEL),
            ("fast", cairo.Antialias.FAST),
            ("good", cairo.Antialias.GOOD),
            ("best", cairo.Antialias.BEST),
        ],
    )
    def test_coerce_str_antialias(self, value: str, expected: cairo.Antialias) -> None:
        result: cairo.Antialias = CairoEnumCoerce.coerce(CairoEnumMap.Antialias, value)
        assert result == expected

    @pytest.mark.parametrize(
        ("value", "expected"),
        [
            ("default", cairo.HintStyle.DEFAULT),
            ("none", cairo.HintStyle.NONE),
            ("slight", cairo.HintStyle.SLIGHT),
            ("medium", cairo.HintStyle.MEDIUM),
            ("full", cairo.HintStyle.FULL),
        ],
    )
    def test_coerce_str_hint_style(self, value: str, expected: cairo.HintStyle) -> None:
        result: cairo.HintStyle = CairoEnumCoerce.coerce(CairoEnumMap.HintStyle, value)
        assert result == expected

    @pytest.mark.parametrize(
        ("value", "expected"),
        [
            ("default", cairo.SubpixelOrder.DEFAULT),
            ("rgb", cairo.SubpixelOrder.RGB),
            ("bgr", cairo.SubpixelOrder.BGR),
            ("vrgb", cairo.SubpixelOrder.VRGB),
            ("vbgr", cairo.SubpixelOrder.VBGR),
        ],
    )
    def test_coerce_str_subpixel_order(self, value: str, expected: cairo.SubpixelOrder) -> None:
        result: cairo.SubpixelOrder = CairoEnumCoerce.coerce(CairoEnumMap.SubpixelOrder, value)
        assert result == expected

    @pytest.mark.parametrize(
        ("value", "expected"),
        [
            ("default", cairo.HintMetrics.DEFAULT),
            ("off", cairo.HintMetrics.OFF),
            ("on", cairo.HintMetrics.ON),
        ],
    )
    def test_coerce_str_hint_metrics(self, value: str, expected: cairo.HintMetrics) -> None:
        result: cairo.HintMetrics = CairoEnumCoerce.coerce(CairoEnumMap.HintMetrics, value)
        assert result == expected

    @pytest.mark.parametrize(
        ("value", "expected"),
        [
            ("default", cairo.ColorMode.DEFAULT),
            ("no_color", cairo.ColorMode.NO_COLOR),
            ("color", cairo.ColorMode.COLOR),
        ],
    )
    def test_coerce_str_color_mode(self, value: str, expected: cairo.ColorMode) -> None:
        result: cairo.ColorMode = CairoEnumCoerce.coerce(CairoEnumMap.ColorMode, value)
        assert result == expected

    @pytest.mark.parametrize(
        ("value", "expected"),
        [
            ("user", cairo.SVGUnit.USER),
            ("em", cairo.SVGUnit.EM),
            ("ex", cairo.SVGUnit.EX),
            ("px", cairo.SVGUnit.PX),
            ("in", cairo.SVGUnit.IN),
            ("cm", cairo.SVGUnit.CM),
            ("mm", cairo.SVGUnit.MM),
            ("pt", cairo.SVGUnit.PT),
            ("pc", cairo.SVGUnit.PC),
            ("percent", cairo.SVGUnit.PERCENT),
        ],
    )
    def test_coerce_str_svg_unit(self, value: str, expected: cairo.SVGUnit) -> None:
        result: cairo.SVGUnit = CairoEnumCoerce.coerce(CairoEnumMap.SVGUnit, value)
        assert result == expected

    @pytest.mark.parametrize(
        ("value", "expected"),
        [
            ("version_1_1", cairo.SVGVersion.VERSION_1_1),
            ("version_1_2", cairo.SVGVersion.VERSION_1_2),
        ],
    )
    def test_coerce_str_svg_version(self, value: str, expected: cairo.SVGVersion) -> None:
        result: cairo.SVGVersion = CairoEnumCoerce.coerce(CairoEnumMap.SVGVersion, value)
        assert result == expected

    @pytest.mark.parametrize(
        ("value", "expected"),
        [
            ("over", cairo.Operator.OVER),
            ("source", cairo.Operator.SOURCE),
            ("clear", cairo.Operator.CLEAR),
            ("add", cairo.Operator.ADD),
            ("atop", cairo.Operator.ATOP),
            ("multiply", cairo.Operator.MULTIPLY),
            ("screen", cairo.Operator.SCREEN),
            ("overlay", cairo.Operator.OVERLAY),
            ("darken", cairo.Operator.DARKEN),
            ("lighten", cairo.Operator.LIGHTEN),
            ("color_dodge", cairo.Operator.COLOR_DODGE),
            ("color_burn", cairo.Operator.COLOR_BURN),
            ("hard_light", cairo.Operator.HARD_LIGHT),
            ("soft_light", cairo.Operator.SOFT_LIGHT),
            ("difference", cairo.Operator.DIFFERENCE),
            ("exclusion", cairo.Operator.EXCLUSION),
            ("hsl_hue", cairo.Operator.HSL_HUE),
            ("hsl_saturation", cairo.Operator.HSL_SATURATION),
            ("hsl_color", cairo.Operator.HSL_COLOR),
            ("hsl_luminosity", cairo.Operator.HSL_LUMINOSITY),
            ("xor", cairo.Operator.XOR),
            ("dest", cairo.Operator.DEST),
            ("dest_over", cairo.Operator.DEST_OVER),
            ("dest_in", cairo.Operator.DEST_IN),
            ("dest_out", cairo.Operator.DEST_OUT),
            ("dest_atop", cairo.Operator.DEST_ATOP),
            ("in", cairo.Operator.IN),
            ("out", cairo.Operator.OUT),
            ("saturate", cairo.Operator.SATURATE),
        ],
    )
    def test_coerce_str_operator(self, value: str, expected: cairo.Operator) -> None:
        result: cairo.Operator = CairoEnumCoerce.coerce(CairoEnumMap.Operator, value)
        assert result == expected

    @pytest.mark.parametrize(
        ("value", "expected"),
        [
            ("version_1_4", cairo.PDFVersion.VERSION_1_4),
            ("version_1_5", cairo.PDFVersion.VERSION_1_5),
            ("version_1_6", cairo.PDFVersion.VERSION_1_6),
            ("version_1_7", cairo.PDFVersion.VERSION_1_7),
        ],
    )
    def test_coerce_str_pdf_version(self, value: str, expected: cairo.PDFVersion) -> None:
        result: cairo.PDFVersion = CairoEnumCoerce.coerce(CairoEnumMap.PDFVersion, value)
        assert result == expected

    # ------------------------------------------------------------------
    # coerce — native input passes through
    # ------------------------------------------------------------------
    def test_coerce_native_passes_through(self) -> None:
        assert CairoEnumCoerce.coerce(CairoEnumMap.Antialias, cairo.Antialias.GRAY) == cairo.Antialias.GRAY
        assert CairoEnumCoerce.coerce(CairoEnumMap.HintStyle, cairo.HintStyle.FULL) == cairo.HintStyle.FULL
        assert CairoEnumCoerce.coerce(CairoEnumMap.SubpixelOrder, cairo.SubpixelOrder.RGB) == cairo.SubpixelOrder.RGB
        assert CairoEnumCoerce.coerce(CairoEnumMap.HintMetrics, cairo.HintMetrics.ON) == cairo.HintMetrics.ON
        assert CairoEnumCoerce.coerce(CairoEnumMap.ColorMode, cairo.ColorMode.COLOR) == cairo.ColorMode.COLOR
        assert CairoEnumCoerce.coerce(CairoEnumMap.Operator, cairo.Operator.OVER) == cairo.Operator.OVER
        assert CairoEnumCoerce.coerce(CairoEnumMap.Operator, cairo.Operator.MULTIPLY) == cairo.Operator.MULTIPLY
        assert CairoEnumCoerce.coerce(CairoEnumMap.SVGUnit, cairo.SVGUnit.PT) == cairo.SVGUnit.PT
        assert (
            CairoEnumCoerce.coerce(CairoEnumMap.SVGVersion, cairo.SVGVersion.VERSION_1_1)
            == cairo.SVGVersion.VERSION_1_1
        )
        assert (
            CairoEnumCoerce.coerce(CairoEnumMap.PDFVersion, cairo.PDFVersion.VERSION_1_4)
            == cairo.PDFVersion.VERSION_1_4
        )

    # ------------------------------------------------------------------
    # coerce — unknown string raises
    # ------------------------------------------------------------------
    def test_coerce_unknown_str_raises(self) -> None:
        with pytest.raises(ValueError, match="Unknown value"):
            CairoEnumCoerce.coerce(CairoEnumMap.Antialias, "invalid")

    def test_coerce_error_message_contains_valid_keys(self) -> None:
        with pytest.raises(ValueError, match="default"):
            CairoEnumCoerce.coerce(CairoEnumMap.Antialias, "bad")

    # ------------------------------------------------------------------
    # CairoEnumMap — built at import time
    # ------------------------------------------------------------------
    def test_enum_maps_are_dicts(self) -> None:
        assert isinstance(CairoEnumMap.Antialias, dict)
        assert isinstance(CairoEnumMap.HintStyle, dict)
        assert isinstance(CairoEnumMap.SubpixelOrder, dict)
        assert isinstance(CairoEnumMap.HintMetrics, dict)
        assert isinstance(CairoEnumMap.ColorMode, dict)
        assert isinstance(CairoEnumMap.Operator, dict)
        assert isinstance(CairoEnumMap.SVGUnit, dict)
        assert isinstance(CairoEnumMap.SVGVersion, dict)
        assert isinstance(CairoEnumMap.PDFVersion, dict)

    def test_enum_maps_are_not_empty(self) -> None:
        assert len(CairoEnumMap.Antialias) == 7
        assert len(CairoEnumMap.HintStyle) == 5
        assert len(CairoEnumMap.SubpixelOrder) == 5
        assert len(CairoEnumMap.HintMetrics) == 3
        assert len(CairoEnumMap.ColorMode) == 3
        assert len(CairoEnumMap.Operator) == 29
        assert len(CairoEnumMap.SVGUnit) == 10
        assert len(CairoEnumMap.SVGVersion) == 2
        assert len(CairoEnumMap.PDFVersion) == 4


class TestCairoEnumLiterals:
    def test_antialias_literals_in_map(self) -> None:
        valid: list[AntialiasStr] = ["default", "none", "gray", "subpixel", "fast", "good", "best"]
        for value in valid:
            assert value in CairoEnumMap.Antialias, f"{value!r} missing from Antialias map"
        assert len(CairoEnumMap.Antialias) == len(valid)

    def test_hint_style_literals_in_map(self) -> None:
        valid: list[HintStyleStr] = ["default", "none", "slight", "medium", "full"]
        for value in valid:
            assert value in CairoEnumMap.HintStyle, f"{value!r} missing from HintStyle map"
        assert len(CairoEnumMap.HintStyle) == len(valid)

    def test_subpixel_order_literals_in_map(self) -> None:
        valid: list[SubpixelOrderStr] = ["default", "rgb", "bgr", "vrgb", "vbgr"]
        for value in valid:
            assert value in CairoEnumMap.SubpixelOrder, f"{value!r} missing from SubpixelOrder map"
        assert len(CairoEnumMap.SubpixelOrder) == len(valid)

    def test_hint_metrics_literals_in_map(self) -> None:
        valid: list[HintMetricsStr] = ["default", "off", "on"]
        for value in valid:
            assert value in CairoEnumMap.HintMetrics, f"{value!r} missing from HintMetrics map"
        assert len(CairoEnumMap.HintMetrics) == len(valid)

    def test_color_mode_literals_in_map(self) -> None:
        valid: list[ColorModeStr] = ["default", "no_color", "color"]
        for value in valid:
            assert value in CairoEnumMap.ColorMode, f"{value!r} missing from ColorMode map"
        assert len(CairoEnumMap.ColorMode) == len(valid)

    def test_svg_unit_literals_in_map(self) -> None:
        valid: list[SVGUnitStr] = ["user", "em", "ex", "px", "in", "cm", "mm", "pt", "pc", "percent"]
        for value in valid:
            assert value in CairoEnumMap.SVGUnit, f"{value!r} missing from SVGUnit map"
        assert len(CairoEnumMap.SVGUnit) == len(valid)

    def test_svg_version_literals_in_map(self) -> None:
        valid: list[SVGVersionStr] = ["version_1_1", "version_1_2"]
        for value in valid:
            assert value in CairoEnumMap.SVGVersion, f"{value!r} missing from SVGVersion map"
        assert len(CairoEnumMap.SVGVersion) == len(valid)

    def test_pdf_version_literals_in_map(self) -> None:
        valid: list[PDFVersionStr] = ["version_1_4", "version_1_5", "version_1_6", "version_1_7"]
        for value in valid:
            assert value in CairoEnumMap.PDFVersion, f"{value!r} missing from PDFVersion map"
        assert len(CairoEnumMap.PDFVersion) == len(valid)

    def test_operator_literals_in_map(self) -> None:
        valid: list[OperatorStr] = [
            "add",
            "atop",
            "clear",
            "color_burn",
            "color_dodge",
            "darken",
            "dest",
            "dest_atop",
            "dest_in",
            "dest_out",
            "dest_over",
            "difference",
            "exclusion",
            "hard_light",
            "hsl_color",
            "hsl_hue",
            "hsl_luminosity",
            "hsl_saturation",
            "in",
            "lighten",
            "multiply",
            "out",
            "over",
            "overlay",
            "saturate",
            "screen",
            "soft_light",
            "source",
            "xor",
        ]
        for value in valid:
            assert value in CairoEnumMap.Operator, f"{value!r} missing from Operator map"
        assert len(CairoEnumMap.Operator) == len(valid)
