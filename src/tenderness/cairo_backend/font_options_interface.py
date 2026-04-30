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

"""Cairo font options interface."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, ClassVar

import cairo
import gi

from tenderness.cairo_backend.cairo_enum_coerce import (
    AntialiasStr,
    CairoEnumCoerce,
    CairoEnumMap,
    ColorModeStr,
    HintMetricsStr,
    HintStyleStr,
    SubpixelOrderStr,
)
from tenderness.core.base_interface import BaseInterface, BaseInterfaceParameters
from tenderness.core.sentinel import _UNSET_PARAM, Settable, SettableOrNone

gi.require_version("PangoCairo", "1.0")


from gi.repository import PangoCairo  # noqa: E402

if TYPE_CHECKING:
    from tenderness.pango_backend.layout_interface import LayoutInterface


@dataclass(slots=True, frozen=True)
class FontOptionsInterfaceParameters(BaseInterfaceParameters):
    """Parameters for configuring a FontOptionsInterface.

    Parameters
    ----------
    antialias
        Antialiasing mode.
    hint_style
        Hinting style.
    subpixel_order
        Subpixel rendering order.
    hint_metrics
        Hinting metrics mode.
    color_mode
        Color rendering mode.
    variations
        Font variations string.
    color_palette
        Active color palette index.
    """

    _COERCE_DISPATCH: ClassVar[dict[str, Any]] = {
        "antialias": lambda v: CairoEnumCoerce.coerce(CairoEnumMap.Antialias, v),
        "hint_style": lambda v: CairoEnumCoerce.coerce(CairoEnumMap.HintStyle, v),
        "subpixel_order": lambda v: CairoEnumCoerce.coerce(CairoEnumMap.SubpixelOrder, v),
        "hint_metrics": lambda v: CairoEnumCoerce.coerce(CairoEnumMap.HintMetrics, v),
        "color_mode": lambda v: CairoEnumCoerce.coerce(CairoEnumMap.ColorMode, v),
    }

    antialias: Settable[cairo.Antialias | AntialiasStr] = field(default=_UNSET_PARAM)
    hint_style: Settable[cairo.HintStyle | HintStyleStr] = field(default=_UNSET_PARAM)
    subpixel_order: Settable[cairo.SubpixelOrder | SubpixelOrderStr] = field(default=_UNSET_PARAM)
    hint_metrics: Settable[cairo.HintMetrics | HintMetricsStr] = field(default=_UNSET_PARAM)
    color_mode: Settable[cairo.ColorMode | ColorModeStr] = field(default=_UNSET_PARAM)

    variations: SettableOrNone[str] = field(default=_UNSET_PARAM)
    color_palette: SettableOrNone[int] = field(default=_UNSET_PARAM)

    def __post_init__(self) -> None:
        """Coerce string enum fields to their cairo enum equivalents."""
        BaseInterfaceParameters.__post_init__(self)


class FontOptionsInterface(BaseInterface):
    """Wrapper around cairo.FontOptions controlling font rendering quality.

    Controls antialiasing, hinting, subpixel order, and color mode —
    not which font is used.

    Parameters
    ----------
    font_options
        Font options object to wrap.
    name
        Optional label for the interface instance.

    Notes
    -----
    https://pycairo.readthedocs.io/en/latest/reference/text.html#class-fontoptions
    """

    def __init__(self, font_options: cairo.FontOptions, name: str = "") -> None:
        super().__init__(name=name)
        self.font_options = font_options

    @classmethod
    def from_new(cls, name: str = "") -> FontOptionsInterface:
        """Construct a font options interface with default cairo.FontOptions."""
        return cls(font_options=cairo.FontOptions(), name=name)

    def apply_to_layout_interface(self, layout_interface: LayoutInterface) -> None:
        """Apply the font options to a Pango layout interface."""
        PangoCairo.context_set_font_options(
            layout_interface.pango_layout.get_context(),
            self.font_options,
        )

    # ------------------------------------------------------------------
    # Properties with getters and setters
    # ------------------------------------------------------------------
    @property
    def antialias(self) -> cairo.Antialias:
        """Antialiasing mode."""
        return self.font_options.get_antialias()

    @antialias.setter
    def antialias(self, antialias: cairo.Antialias) -> None:
        self.font_options.set_antialias(antialias)

    @property
    def hint_style(self) -> cairo.HintStyle:
        """Hinting style."""
        return self.font_options.get_hint_style()

    @hint_style.setter
    def hint_style(self, hint_style: cairo.HintStyle) -> None:
        self.font_options.set_hint_style(hint_style)

    @property
    def subpixel_order(self) -> cairo.SubpixelOrder:
        """Subpixel rendering order."""
        return self.font_options.get_subpixel_order()

    @subpixel_order.setter
    def subpixel_order(self, subpixel_order: cairo.SubpixelOrder) -> None:
        self.font_options.set_subpixel_order(subpixel_order)

    @property
    def hint_metrics(self) -> cairo.HintMetrics:
        """Hinting metrics mode."""
        return self.font_options.get_hint_metrics()

    @hint_metrics.setter
    def hint_metrics(self, hint_metrics: cairo.HintMetrics) -> None:
        self.font_options.set_hint_metrics(hint_metrics)

    @property
    def variations(self) -> str:
        """Font variations string."""
        return self.font_options.get_variations()

    @variations.setter
    def variations(self, variations: str | None) -> None:
        self.font_options.set_variations(variations)

    @property
    def color_mode(self) -> cairo.ColorMode:
        """Color rendering mode."""
        return self.font_options.get_color_mode()

    @color_mode.setter
    def color_mode(self, color_mode: cairo.ColorMode) -> None:
        self.font_options.set_color_mode(color_mode)

    @property
    def color_palette(self) -> int:
        """Active color palette index."""
        return self.font_options.get_color_palette()

    @color_palette.setter
    def color_palette(self, palette_index: int) -> None:
        self.font_options.set_color_palette(palette_index)

    # ------------------------------------------------------------------
    # Properties with only getters
    # ------------------------------------------------------------------
    @property
    def hash(self) -> int:
        """Hash value of the font options."""
        return self.font_options.hash()

    # ------------------------------------------------------------------
    # Methods
    # ------------------------------------------------------------------
    def merge(self, other: cairo.FontOptions) -> None:
        """Merge another font options object into this one."""
        self.font_options.merge(other)

    def copy(self) -> cairo.FontOptions:
        """Return a copy of the underlying font options."""
        return self.font_options.copy()

    def equal(self, other: cairo.FontOptions) -> bool:
        """Return whether this font options equals another."""
        return self.font_options.equal(other)

    def get_custom_palette_color(self, index: int) -> tuple[float, float, float, float]:
        """Return the custom palette color at a given index.

        Parameters
        ----------
        index
            Palette color index.

        Returns
        -------
        tuple
            Color components as ``(red, green, blue, alpha)``.
        """
        return self.font_options.get_custom_palette_color(index)

    def set_custom_palette_color(self, index: int, red: float, green: float, blue: float, alpha: float) -> None:
        """Set a custom palette color at a given index.

        Parameters
        ----------
        index
            Palette color index.
        red
            Red component.
        green
            Green component.
        blue
            Blue component.
        alpha
            Alpha component.
        """
        self.font_options.set_custom_palette_color(index, red, green, blue, alpha)
