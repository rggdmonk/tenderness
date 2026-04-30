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

"""Pango layout context interface with typed attribute access."""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, ClassVar, Self

import gi

from tenderness.core.base_interface import BaseInterface, BaseInterfaceParameters
from tenderness.core.sentinel import _UNSET_PARAM, Settable, SettableOrNone
from tenderness.pango_backend.pango_enum_coerce import (
    DirectionStr,
    GravityHintStr,
    GravityStr,
    PangoEnumCoerce,
    PangoEnumMap,
)

gi.require_version("Pango", "1.0")


from gi.repository import Pango  # noqa: E402

if TYPE_CHECKING:
    from tenderness.pango_backend.layout_interface import LayoutInterface

logger = logging.getLogger(__name__)


@dataclass(slots=True, frozen=True)
class LayoutContextInterfaceParameters(BaseInterfaceParameters):
    """Keyword parameters for updating a LayoutContextInterface.

    Parameters
    ----------
    base_dir
        Base text direction for the context.
    base_gravity
        Base gravity; resolved gravity may differ depending on the gravity hint.
    gravity_hint
        Gravity hint for disambiguating base gravity when applicable.
    round_glyph_positions
        Whether glyph positions are rounded to pixel boundaries.
    font_description
        Default font description; ``None`` clears the setting.
    font_map
        Font map used for loading fonts; ``None`` uses the default map.
    language
        Default language for the context; ``None`` uses the system language.
    matrix
        Transformation matrix applied to the context; ``None`` clears the transform.
    """

    _COERCE_DISPATCH: ClassVar[dict[str, Any]] = {
        "base_dir": lambda v: PangoEnumCoerce.coerce(PangoEnumMap.Direction, v),
        "base_gravity": lambda v: PangoEnumCoerce.coerce(PangoEnumMap.Gravity, v),
        "gravity_hint": lambda v: PangoEnumCoerce.coerce(PangoEnumMap.GravityHint, v),
    }

    base_dir: Settable[Pango.Direction | DirectionStr] = field(default=_UNSET_PARAM)
    base_gravity: Settable[Pango.Gravity | GravityStr] = field(default=_UNSET_PARAM)
    gravity_hint: Settable[Pango.GravityHint | GravityHintStr] = field(default=_UNSET_PARAM)
    round_glyph_positions: Settable[bool] = field(default=_UNSET_PARAM)

    font_description: SettableOrNone[Pango.FontDescription] = field(default=_UNSET_PARAM)
    font_map: SettableOrNone[Pango.FontMap] = field(default=_UNSET_PARAM)
    language: SettableOrNone[Pango.Language] = field(default=_UNSET_PARAM)
    matrix: SettableOrNone[Pango.Matrix] = field(default=_UNSET_PARAM)

    def __post_init__(self) -> None:
        """Coerce enum fields after initialization."""
        BaseInterfaceParameters.__post_init__(self)


class LayoutContextInterface(BaseInterface):
    """Wrapper around Pango.Context with typed property access.

    Notes
    -----
    See https://docs.gtk.org/Pango/class.Context.html
    """

    PANGO_SCALE: int = Pango.SCALE

    def __init__(self, pango_context: Pango.Context, name: str = "") -> None:
        super().__init__(name=name)
        self.pango_context = pango_context

    @classmethod
    def from_layout_interface(cls, layout_interface: LayoutInterface, name: str = "") -> Self:
        """Create a LayoutContextInterface from a LayoutInterface's Pango context."""
        return cls(pango_context=layout_interface.get_context(), name=name)

    @classmethod
    def from_pango_layout(cls, pango_layout: Pango.Layout, name: str = "") -> Self:
        """Create a LayoutContextInterface from a Pango.Layout's context."""
        return cls(pango_context=pango_layout.get_context(), name=name)

    # ------------------------------------------------------------------
    # Properties with getters and setters
    # ------------------------------------------------------------------
    @property
    def base_dir(self) -> Pango.Direction:
        """Base text direction for the context."""
        return self.pango_context.get_base_dir()

    @base_dir.setter
    def base_dir(self, direction: Pango.Direction) -> None:
        self.pango_context.set_base_dir(direction)

    @property
    def base_gravity(self) -> Pango.Gravity:
        """Base gravity; resolved gravity may differ depending on the gravity hint."""
        return self.pango_context.get_base_gravity()

    @base_gravity.setter
    def base_gravity(self, gravity: Pango.Gravity) -> None:
        self.pango_context.set_base_gravity(gravity)

    @property
    def gravity_hint(self) -> Pango.GravityHint:
        """Gravity hint for disambiguating base gravity when applicable."""
        return self.pango_context.get_gravity_hint()

    @gravity_hint.setter
    def gravity_hint(self, hint: Pango.GravityHint) -> None:
        self.pango_context.set_gravity_hint(hint)

    @property
    def round_glyph_positions(self) -> bool:
        """True when glyph positions are rounded to pixel boundaries."""
        return self.pango_context.get_round_glyph_positions()

    @round_glyph_positions.setter
    def round_glyph_positions(self, round_positions: bool) -> None:
        self.pango_context.set_round_glyph_positions(round_positions)

    # ------------------------------------------------------------------
    # Properties with only getters
    # ------------------------------------------------------------------
    @property
    def gravity(self) -> Pango.Gravity:
        """Resolved gravity (read-only; derived from base_gravity + gravity_hint)."""
        return self.pango_context.get_gravity()

    @property
    def serial(self) -> int:
        """Current serial number; increments on each context change."""
        return self.pango_context.get_serial()

    # ------------------------------------------------------------------
    # Properties with getters and setters (have separated interface)
    # ------------------------------------------------------------------
    @property
    def font_description(self) -> Pango.FontDescription | None:
        """Read-only pointer — call `.copy()` before modifying."""
        return self.pango_context.get_font_description()

    @font_description.setter
    def font_description(self, desc: Pango.FontDescription | None) -> None:
        self.pango_context.set_font_description(desc)

    @property
    def font_map(self) -> Pango.FontMap | None:
        """Font map used for loading fonts."""
        return self.pango_context.get_font_map()

    @font_map.setter
    def font_map(self, font_map: Pango.FontMap | None) -> None:
        self.pango_context.set_font_map(font_map)

    @property
    def language(self) -> Pango.Language:
        """Default language for the context."""
        return self.pango_context.get_language()

    @language.setter
    def language(self, language: Pango.Language | None) -> None:
        self.pango_context.set_language(language)

    @property
    def matrix(self) -> Pango.Matrix | None:
        """Transformation matrix applied to the context."""
        return self.pango_context.get_matrix()

    @matrix.setter
    def matrix(self, matrix: Pango.Matrix | None) -> None:
        self.pango_context.set_matrix(matrix)

    # ------------------------------------------------------------------
    # Methods
    # ------------------------------------------------------------------
    def changed(self) -> None:
        """Force a full relayout on the next layout that uses this context."""
        self.pango_context.changed()

    def get_metrics(
        self,
        desc: Pango.FontDescription | None = None,
        language: Pango.Language | None = None,
    ) -> Pango.FontMetrics:
        """Return font metrics for the given font description and language."""
        return self.pango_context.get_metrics(desc, language)

    def list_families(self) -> list[Pango.FontFamily]:
        """Return all font families available in the current font map."""
        return self.pango_context.list_families()

    def load_font(self, desc: Pango.FontDescription) -> Pango.Font | None:
        """Load a single font matching desc from the context's font map."""
        return self.pango_context.load_font(desc)

    def load_fontset(
        self,
        desc: Pango.FontDescription,
        language: Pango.Language,
    ) -> Pango.Fontset | None:
        """Load the set of fonts matching desc for the given language."""
        return self.pango_context.load_fontset(desc, language)
