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

from typing import TYPE_CHECKING, Literal

import gi

if TYPE_CHECKING:
    from collections.abc import Mapping

gi.require_version("Pango", "1.0")


from gi.repository import Pango  # noqa: E402


class PangoEnumCoerce:  # noqa: D101 TODO: docstring
    @staticmethod
    def build_map(enum_type: type, exclude: frozenset[str] = frozenset()) -> dict[str, object]:  # noqa: D102 TODO: docstring
        result = {}
        for member in enum_type.__enum_values__.values():  # type: ignore[attr-defined]
            nick = member.value_nick.lower()
            if nick not in exclude:
                result[nick] = member
        return result

    @staticmethod
    def coerce[T](mapping: Mapping[str, object], value: T | str) -> T:  # noqa: D102 TODO: docstring
        if not isinstance(value, str):
            return value

        result = mapping.get(value)
        if result is None:
            valid = list(mapping.keys())
            msg = f"Unknown value: {value!r}. Valid: {valid}"
            raise ValueError(msg)

        return result  # type: ignore[return-value]


class PangoEnumMap:  # noqa: D101 TODO: docstring
    # Pango.Layout
    WrapMode = PangoEnumCoerce.build_map(enum_type=Pango.WrapMode)
    EllipsizeMode = PangoEnumCoerce.build_map(enum_type=Pango.EllipsizeMode)
    Alignment = PangoEnumCoerce.build_map(enum_type=Pango.Alignment)

    # Pango.FontDescription
    Gravity = PangoEnumCoerce.build_map(enum_type=Pango.Gravity)
    Stretch = PangoEnumCoerce.build_map(enum_type=Pango.Stretch)
    Style = PangoEnumCoerce.build_map(enum_type=Pango.Style)
    Variant = PangoEnumCoerce.build_map(enum_type=Pango.Variant)
    Weight = PangoEnumCoerce.build_map(enum_type=Pango.Weight)
    FontColor = PangoEnumCoerce.build_map(enum_type=Pango.FontColor)  # type: ignore[attr-defined]

    # Pango.Context
    Direction = PangoEnumCoerce.build_map(
        enum_type=Pango.Direction,
        exclude=frozenset({"ttb-ltr", "ttb-rtl"}),
    )
    # Gravity (same as Pango.FontDescription)
    GravityHint = PangoEnumCoerce.build_map(enum_type=Pango.GravityHint)

    # Pango.TabAlign
    TabAlign = PangoEnumCoerce.build_map(enum_type=Pango.TabAlign)


# Pango.Layout
WrapModeStr = Literal["word", "char", "word-char", "none"]
EllipsizeModeStr = Literal["none", "start", "middle", "end"]
AlignmentStr = Literal["left", "center", "right"]

# Pango.FontDescription
GravityStr = Literal["south", "east", "north", "west", "auto"]
StretchStr = Literal[
    "ultra-condensed",
    "extra-condensed",
    "condensed",
    "semi-condensed",
    "normal",
    "semi-expanded",
    "expanded",
    "extra-expanded",
    "ultra-expanded",
]
StyleStr = Literal["normal", "oblique", "italic"]
VariantStr = Literal[
    "normal", "small-caps", "all-small-caps", "petite-caps", "all-petite-caps", "unicase", "title-caps"
]
WeightStr = Literal[
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
]
FontColorStr = Literal["forbidden", "required", "dont-care"]

# Pango.Context
DirectionStr = Literal["ltr", "rtl", "weak-ltr", "weak-rtl", "neutral"]
GravityHintStr = Literal["natural", "strong", "line"]

# Pango.TabAlign
TabAlignStr = Literal["left", "right", "center", "decimal"]
