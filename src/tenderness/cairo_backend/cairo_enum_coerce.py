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

"""Cairo enum coercion utilities and string type aliases."""

from __future__ import annotations

from typing import Literal

import cairo


class CairoEnumCoerce:
    """Utilities for building lowercase string-to-enum maps and coercing values for Cairo enums."""

    @staticmethod
    def build_map(enum_type: type) -> dict[str, object]:
        """Build a lowercase name-to-value map from a Cairo enum type.

        Parameters
        ----------
        enum_type
            Cairo enum class to introspect; non-public and non-integer attributes are excluded.

        Returns
        -------
        dict[str, object]
            Mapping of lowercase member name to enum value.
        """
        return {
            name.lower(): value
            for name, value in vars(enum_type).items()
            if not name.startswith("_") and isinstance(value, int)
        }

    @staticmethod
    def coerce[T](mapping: dict[str, object], value: T | str) -> T:
        """Coerce a string value to its enum counterpart using a mapping.

        Parameters
        ----------
        mapping
            Lowercase name-to-value map, produced by ``build_map``.
        value
            Value to coerce; returned unchanged if not a string.

        Returns
        -------
        T
            The original value if not a string, or the mapped enum value.

        Raises
        ------
        ValueError
            If ``value`` is a string not present in ``mapping``.
        """
        if not isinstance(value, str):
            return value

        result = mapping.get(value)
        if result is None:
            valid = list(mapping.keys())
            msg = f"Unknown value: {value!r}. Valid: {valid}"
            raise ValueError(msg)

        return result  # type: ignore[return-value]


class CairoEnumMap:
    """Pre-built lowercase string-to-value maps for Cairo enums.

    Attributes
    ----------
    Antialias
        Map for ``cairo.Antialias``.
    HintStyle
        Map for ``cairo.HintStyle``.
    SubpixelOrder
        Map for ``cairo.SubpixelOrder``.
    HintMetrics
        Map for ``cairo.HintMetrics``.
    ColorMode
        Map for ``cairo.ColorMode``.
    Operator
        Map for ``cairo.Operator``.
    SVGUnit
        Map for ``cairo.SVGUnit``.
    SVGVersion
        Map for ``cairo.SVGVersion``.
    PDFVersion
        Map for ``cairo.PDFVersion``.
    """

    # cairo.FontOptions
    Antialias = CairoEnumCoerce.build_map(cairo.Antialias)
    HintStyle = CairoEnumCoerce.build_map(cairo.HintStyle)
    SubpixelOrder = CairoEnumCoerce.build_map(cairo.SubpixelOrder)
    HintMetrics = CairoEnumCoerce.build_map(cairo.HintMetrics)
    ColorMode = CairoEnumCoerce.build_map(cairo.ColorMode)
    # cairo.Context
    Operator = CairoEnumCoerce.build_map(cairo.Operator)
    # cairo.Surface
    SVGUnit = CairoEnumCoerce.build_map(cairo.SVGUnit)
    SVGVersion = CairoEnumCoerce.build_map(cairo.SVGVersion)
    PDFVersion = CairoEnumCoerce.build_map(cairo.PDFVersion)


# cairo.FontOptions
AntialiasStr = Literal["default", "none", "gray", "subpixel", "fast", "good", "best"]
HintStyleStr = Literal["default", "none", "slight", "medium", "full"]
SubpixelOrderStr = Literal["default", "rgb", "bgr", "vrgb", "vbgr"]
HintMetricsStr = Literal["default", "off", "on"]
ColorModeStr = Literal["default", "no_color", "color"]
# cairo.Context
OperatorStr = Literal[
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
# cairo.Surface
SVGUnitStr = Literal["user", "em", "ex", "px", "in", "cm", "mm", "pt", "pc", "percent"]
SVGVersionStr = Literal["version_1_1", "version_1_2"]
PDFVersionStr = Literal["version_1_4", "version_1_5", "version_1_6", "version_1_7"]
