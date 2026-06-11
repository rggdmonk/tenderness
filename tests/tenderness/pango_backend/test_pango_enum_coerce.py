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

if TYPE_CHECKING:
    from collections.abc import Mapping

from tenderness.pango_backend.pango_enum_coerce import (
    PangoEnumCoerce,
    PangoEnumMap,
)

gi.require_version("Pango", "1.0")
from gi.repository import Pango  # noqa: E402


class TestPangoEnumCoerce:
    # ------------------------------------------------------------------
    # build_map
    # ------------------------------------------------------------------
    def test_build_map_contains_nick(self) -> None:
        mapping = PangoEnumCoerce.build_map(Pango.WrapMode)
        assert "word" in mapping
        assert "char" in mapping
        assert "word-char" in mapping

    def test_build_map_values_are_pango_members(self) -> None:
        mapping = PangoEnumCoerce.build_map(Pango.WrapMode)
        assert mapping["word"] is Pango.WrapMode.WORD
        assert mapping["char"] is Pango.WrapMode.CHAR
        assert mapping["word-char"] is Pango.WrapMode.WORD_CHAR

    def test_build_map_exclude_removes_nicks(self) -> None:
        mapping = PangoEnumCoerce.build_map(Pango.Direction, exclude=frozenset({"ttb-ltr", "ttb-rtl"}))
        assert "ttb-ltr" not in mapping
        assert "ttb-rtl" not in mapping

    def test_build_map_exclude_keeps_non_excluded(self) -> None:
        mapping = PangoEnumCoerce.build_map(Pango.Direction, exclude=frozenset({"ttb-ltr", "ttb-rtl"}))
        assert "ltr" in mapping
        assert "rtl" in mapping
        assert "weak-ltr" in mapping
        assert "weak-rtl" in mapping
        assert "neutral" in mapping

    def test_build_map_empty_exclude_keeps_all(self) -> None:
        full = PangoEnumCoerce.build_map(Pango.Direction)
        filtered = PangoEnumCoerce.build_map(Pango.Direction, exclude=frozenset({"ttb-ltr", "ttb-rtl"}))
        assert len(filtered) == len(full) - 2

    # ------------------------------------------------------------------
    # coerce — str input
    # ------------------------------------------------------------------
    @pytest.mark.parametrize(
        ("value", "expected"),
        [
            ("word", Pango.WrapMode.WORD),
            ("char", Pango.WrapMode.CHAR),
            ("word-char", Pango.WrapMode.WORD_CHAR),
        ],
    )
    def test_coerce_str_wrap_mode(self, value: str, expected: Pango.WrapMode) -> None:
        result: Pango.WrapMode = PangoEnumCoerce.coerce(PangoEnumMap.WrapMode, value)
        assert result is expected

    @pytest.mark.parametrize(
        ("value", "expected"),
        [
            ("none", Pango.EllipsizeMode.NONE),
            ("start", Pango.EllipsizeMode.START),
            ("middle", Pango.EllipsizeMode.MIDDLE),
            ("end", Pango.EllipsizeMode.END),
        ],
    )
    def test_coerce_str_ellipsize_mode(self, value: str, expected: Pango.EllipsizeMode) -> None:
        result: Pango.EllipsizeMode = PangoEnumCoerce.coerce(PangoEnumMap.EllipsizeMode, value)
        assert result is expected

    @pytest.mark.parametrize(
        ("value", "expected"),
        [
            ("left", Pango.Alignment.LEFT),
            ("center", Pango.Alignment.CENTER),
            ("right", Pango.Alignment.RIGHT),
        ],
    )
    def test_coerce_str_alignment(self, value: str, expected: Pango.Alignment) -> None:
        result: Pango.Alignment = PangoEnumCoerce.coerce(PangoEnumMap.Alignment, value)
        assert result is expected

    @pytest.mark.parametrize(
        ("value", "expected"),
        [
            ("south", Pango.Gravity.SOUTH),
            ("east", Pango.Gravity.EAST),
            ("north", Pango.Gravity.NORTH),
            ("west", Pango.Gravity.WEST),
            ("auto", Pango.Gravity.AUTO),
        ],
    )
    def test_coerce_str_gravity(self, value: str, expected: Pango.Gravity) -> None:
        result: Pango.Gravity = PangoEnumCoerce.coerce(PangoEnumMap.Gravity, value)
        assert result is expected

    @pytest.mark.parametrize(
        ("value", "expected"),
        [
            ("ultra-condensed", Pango.Stretch.ULTRA_CONDENSED),
            ("condensed", Pango.Stretch.CONDENSED),
            ("normal", Pango.Stretch.NORMAL),
            ("expanded", Pango.Stretch.EXPANDED),
            ("ultra-expanded", Pango.Stretch.ULTRA_EXPANDED),
        ],
    )
    def test_coerce_str_stretch(self, value: str, expected: Pango.Stretch) -> None:
        result: Pango.Stretch = PangoEnumCoerce.coerce(PangoEnumMap.Stretch, value)
        assert result is expected

    @pytest.mark.parametrize(
        ("value", "expected"),
        [
            ("normal", Pango.Style.NORMAL),
            ("oblique", Pango.Style.OBLIQUE),
            ("italic", Pango.Style.ITALIC),
        ],
    )
    def test_coerce_str_style(self, value: str, expected: Pango.Style) -> None:
        result: Pango.Style = PangoEnumCoerce.coerce(PangoEnumMap.Style, value)
        assert result is expected

    @pytest.mark.parametrize(
        ("value", "expected"),
        [
            ("normal", Pango.Variant.NORMAL),
            ("small-caps", Pango.Variant.SMALL_CAPS),
        ],
    )
    def test_coerce_str_variant(self, value: str, expected: Pango.Variant) -> None:
        result: Pango.Variant = PangoEnumCoerce.coerce(PangoEnumMap.Variant, value)
        assert result is expected

    @pytest.mark.parametrize(
        ("value", "expected"),
        [
            ("thin", Pango.Weight.THIN),
            ("light", Pango.Weight.LIGHT),
            ("normal", Pango.Weight.NORMAL),
            ("bold", Pango.Weight.BOLD),
            ("ultrabold", Pango.Weight.ULTRABOLD),
            ("heavy", Pango.Weight.HEAVY),
        ],
    )
    def test_coerce_str_weight(self, value: str, expected: Pango.Weight) -> None:
        result: Pango.Weight = PangoEnumCoerce.coerce(PangoEnumMap.Weight, value)
        assert result is expected

    @pytest.mark.parametrize(
        ("value", "expected"),
        [
            ("ltr", Pango.Direction.LTR),
            ("rtl", Pango.Direction.RTL),
            ("weak-ltr", Pango.Direction.WEAK_LTR),
            ("weak-rtl", Pango.Direction.WEAK_RTL),
            ("neutral", Pango.Direction.NEUTRAL),
        ],
    )
    def test_coerce_str_direction(self, value: str, expected: Pango.Direction) -> None:
        result: Pango.Direction = PangoEnumCoerce.coerce(PangoEnumMap.Direction, value)
        assert result is expected

    @pytest.mark.parametrize(
        ("value", "expected"),
        [
            ("natural", Pango.GravityHint.NATURAL),
            ("strong", Pango.GravityHint.STRONG),
            ("line", Pango.GravityHint.LINE),
        ],
    )
    def test_coerce_str_gravity_hint(self, value: str, expected: Pango.GravityHint) -> None:
        result: Pango.GravityHint = PangoEnumCoerce.coerce(PangoEnumMap.GravityHint, value)
        assert result is expected

    @pytest.mark.parametrize(
        ("value", "expected"),
        [
            ("left", Pango.TabAlign.LEFT),
            ("right", Pango.TabAlign.RIGHT),
            ("center", Pango.TabAlign.CENTER),
            ("decimal", Pango.TabAlign.DECIMAL),
        ],
    )
    def test_coerce_str_tab_align(self, value: str, expected: Pango.TabAlign) -> None:
        result: Pango.TabAlign = PangoEnumCoerce.coerce(PangoEnumMap.TabAlign, value)
        assert result is expected

    # ------------------------------------------------------------------
    # Direction — deprecated values rejected
    # ------------------------------------------------------------------
    @pytest.mark.parametrize("deprecated", ["ttb-ltr", "ttb-rtl"])
    def test_coerce_direction_deprecated_raises(self, deprecated: str) -> None:
        with pytest.raises(ValueError, match="Unknown value"):
            PangoEnumCoerce.coerce(PangoEnumMap.Direction, deprecated)

    # ------------------------------------------------------------------
    # coerce — native input passes through
    # ------------------------------------------------------------------
    def test_coerce_native_passes_through(self) -> None:
        assert PangoEnumCoerce.coerce(PangoEnumMap.WrapMode, Pango.WrapMode.WORD) is Pango.WrapMode.WORD
        assert PangoEnumCoerce.coerce(PangoEnumMap.EllipsizeMode, Pango.EllipsizeMode.END) is Pango.EllipsizeMode.END
        assert PangoEnumCoerce.coerce(PangoEnumMap.Alignment, Pango.Alignment.CENTER) is Pango.Alignment.CENTER
        assert PangoEnumCoerce.coerce(PangoEnumMap.Gravity, Pango.Gravity.SOUTH) is Pango.Gravity.SOUTH
        assert PangoEnumCoerce.coerce(PangoEnumMap.Stretch, Pango.Stretch.NORMAL) is Pango.Stretch.NORMAL
        assert PangoEnumCoerce.coerce(PangoEnumMap.Style, Pango.Style.ITALIC) is Pango.Style.ITALIC
        assert PangoEnumCoerce.coerce(PangoEnumMap.Variant, Pango.Variant.NORMAL) is Pango.Variant.NORMAL
        assert PangoEnumCoerce.coerce(PangoEnumMap.Weight, Pango.Weight.BOLD) is Pango.Weight.BOLD
        assert PangoEnumCoerce.coerce(PangoEnumMap.Direction, Pango.Direction.LTR) is Pango.Direction.LTR
        assert PangoEnumCoerce.coerce(PangoEnumMap.GravityHint, Pango.GravityHint.STRONG) is Pango.GravityHint.STRONG
        assert PangoEnumCoerce.coerce(PangoEnumMap.TabAlign, Pango.TabAlign.LEFT) is Pango.TabAlign.LEFT

    # ------------------------------------------------------------------
    # coerce — unknown string raises
    # ------------------------------------------------------------------
    def test_coerce_unknown_str_raises(self) -> None:
        with pytest.raises(ValueError, match="Unknown value"):
            PangoEnumCoerce.coerce(PangoEnumMap.WrapMode, "invalid")

    def test_coerce_error_message_contains_valid_keys(self) -> None:
        with pytest.raises(ValueError, match="word"):
            PangoEnumCoerce.coerce(PangoEnumMap.WrapMode, "bad")


_LITERAL_MAP_CASES: list[tuple[list[str], Mapping[str, object], str]] = [
    (["word", "char", "word-char", "none"], PangoEnumMap.WrapMode, "WrapMode"),
    (["none", "start", "middle", "end"], PangoEnumMap.EllipsizeMode, "EllipsizeMode"),
    (["left", "center", "right"], PangoEnumMap.Alignment, "Alignment"),
    (["south", "east", "north", "west", "auto"], PangoEnumMap.Gravity, "Gravity"),
    (
        [
            "ultra-condensed",
            "extra-condensed",
            "condensed",
            "semi-condensed",
            "normal",
            "semi-expanded",
            "expanded",
            "extra-expanded",
            "ultra-expanded",
        ],
        PangoEnumMap.Stretch,
        "Stretch",
    ),
    (["normal", "oblique", "italic"], PangoEnumMap.Style, "Style"),
    (
        ["normal", "small-caps", "all-small-caps", "petite-caps", "all-petite-caps", "unicase", "title-caps"],
        PangoEnumMap.Variant,
        "Variant",
    ),
    (
        [
            "thin",
            "ultralight",
            "light",
            "semilight",
            "book",
            "normal",
            "medium",
            "semibold",
            "bold",
            "ultrabold",
            "heavy",
            "ultraheavy",
        ],
        PangoEnumMap.Weight,
        "Weight",
    ),
    (["forbidden", "required", "dont-care"], PangoEnumMap.FontColor, "FontColor"),
    (["ltr", "rtl", "weak-ltr", "weak-rtl", "neutral"], PangoEnumMap.Direction, "Direction"),
    (["natural", "strong", "line"], PangoEnumMap.GravityHint, "GravityHint"),
    (["left", "right", "center", "decimal"], PangoEnumMap.TabAlign, "TabAlign"),
]


class TestPangoEnumLiterals:
    @pytest.mark.parametrize(
        ("values", "mapping", "map_name"), _LITERAL_MAP_CASES, ids=lambda x: x if isinstance(x, str) else ""
    )
    def test_literals_in_map(self, values: list[str], mapping: Mapping[str, object], map_name: str) -> None:
        for value in values:
            assert value in mapping, f"{value!r} missing from {map_name} map"
        assert len(mapping) == len(values), f"{map_name} map has unexpected extra keys"

    def test_direction_deprecated_not_in_map(self) -> None:
        for deprecated in ("ttb-ltr", "ttb-rtl"):
            assert deprecated not in PangoEnumMap.Direction, f"{deprecated!r} should be excluded from Direction map"
