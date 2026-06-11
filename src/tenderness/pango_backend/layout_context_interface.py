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

"""Layout context interface."""

from __future__ import annotations

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
gi.require_version("PangoCairo", "1.0")


from gi.repository import Pango, PangoCairo  # noqa: E402

if TYPE_CHECKING:
    from tenderness.pango_backend.layout_interface import LayoutInterface


@dataclass(slots=True, frozen=True)
class LayoutContextInterfaceParameters(BaseInterfaceParameters):
    """Configuration parameters for LayoutContextInterface.

    Attributes
    ----------
    base_dir
        Base text direction for the context.
    base_gravity
        Base gravity; resolved gravity may differ depending on the gravity hint.
    gravity_hint
        Gravity hint for disambiguating base gravity when applicable.
    round_glyph_positions
        Whether glyph positions are rounded to pixel boundaries.
    resolution
        DPI used to convert point-sized fonts to device pixels.
        ``0`` or negative inherits from the font map (default 96.0).
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
    resolution: Settable[float] = field(default=_UNSET_PARAM)

    font_description: SettableOrNone[Pango.FontDescription] = field(default=_UNSET_PARAM)
    font_map: SettableOrNone[Pango.FontMap] = field(default=_UNSET_PARAM)
    language: SettableOrNone[Pango.Language] = field(default=_UNSET_PARAM)
    matrix: SettableOrNone[Pango.Matrix] = field(default=_UNSET_PARAM)

    def __post_init__(self) -> None:
        """Coerce enum fields after initialization."""
        BaseInterfaceParameters.__post_init__(self)


class LayoutContextInterface(BaseInterface):
    """Interface for managing Pango layout context.

    Attributes
    ----------
    PANGO_SCALE
        Scale between Pango distances and device units (``Pango.SCALE``, currently 1024).

    Notes
    -----
    See https://docs.gtk.org/Pango/class.Context.html
    """

    PANGO_SCALE: int = Pango.SCALE

    def __init__(self, pango_context: Pango.Context, name: str = "") -> None:
        """Initialize LayoutContextInterface.

        Parameters
        ----------
        pango_context
            Underlying Pango context object.
        name
            Optional label for the interface instance.
        """
        super().__init__(name=name)
        self.pango_context = pango_context

    @classmethod
    def from_layout_interface(cls, layout_interface: LayoutInterface, name: str = "") -> Self:
        """Create from a LayoutInterface's Pango context.

        Parameters
        ----------
        layout_interface
            Layout interface whose context is used.
        name
            Optional label for the interface instance.

        Returns
        -------
        Self
            ``LayoutContextInterface`` backed by the given layout's context.
        """
        return cls(pango_context=layout_interface.get_context(), name=name)

    @classmethod
    def from_pango_layout(cls, pango_layout: Pango.Layout, name: str = "") -> Self:
        """Create from a Pango.Layout's context.

        Parameters
        ----------
        pango_layout
            Pango layout whose context is used.
        name
            Optional label for the interface instance.

        Returns
        -------
        Self
            ``LayoutContextInterface`` backed by the given layout's context.
        """
        return cls(pango_context=pango_layout.get_context(), name=name)

    # ------------------------------------------------------------------
    # Properties with getters and setters
    # ------------------------------------------------------------------
    @property
    def base_dir(self) -> Pango.Direction:
        """Base direction used in the Unicode bidirectional algorithm.

        Returns
        -------
        Pango.Direction
            Current base text direction.
        """
        return self.pango_context.get_base_dir()

    @base_dir.setter
    def base_dir(self, direction: Pango.Direction) -> None:
        """Set the base direction used in the Unicode bidirectional algorithm.

        Parameters
        ----------
        direction
            Direction to apply.
        """
        self.pango_context.set_base_dir(direction)

    @property
    def base_gravity(self) -> Pango.Gravity:
        """Base gravity used in laying out vertical text.

        Returns
        -------
        Pango.Gravity
            Current base gravity.

        Notes
        -----
        The resolved gravity may differ from the base gravity depending on
        the gravity hint. Use ``gravity`` to get the resolved value.
        """
        return self.pango_context.get_base_gravity()

    @base_gravity.setter
    def base_gravity(self, gravity: Pango.Gravity) -> None:
        """Set the base gravity used in laying out vertical text.

        Parameters
        ----------
        gravity
            Gravity to apply.
        """
        self.pango_context.set_base_gravity(gravity)

    @property
    def gravity_hint(self) -> Pango.GravityHint:
        """Gravity hint used when laying out vertical text.

        Returns
        -------
        Pango.GravityHint
            Current gravity hint.

        Notes
        -----
        Only relevant when ``gravity`` is ``EAST`` or ``WEST``.
        """
        return self.pango_context.get_gravity_hint()

    @gravity_hint.setter
    def gravity_hint(self, hint: Pango.GravityHint) -> None:
        """Set the gravity hint used when laying out vertical text.

        Parameters
        ----------
        hint
            Gravity hint to apply.
        """
        self.pango_context.set_gravity_hint(hint)

    @property
    def round_glyph_positions(self) -> bool:
        """``True`` when glyph positions and widths are rounded to integral device units.

        Returns
        -------
        bool
            ``True`` if glyph positions are rounded to pixel boundaries.
        """
        return self.pango_context.get_round_glyph_positions()

    @round_glyph_positions.setter
    def round_glyph_positions(self, round_positions: bool) -> None:
        """Enable or disable rounding of glyph positions to integral device units.

        Parameters
        ----------
        round_positions
            If ``True``, round glyph positions to pixel boundaries. Useful when
            the renderer cannot handle subpixel positioning. Defaults to ``True``.
        """
        self.pango_context.set_round_glyph_positions(round_positions)

    @property
    def resolution(self) -> float:
        """DPI used to convert point-sized fonts to device pixels.

        Returns
        -------
        float
            Current resolution in dots per inch.
            A negative value is returned if no resolution has been explicitly set.

        Notes
        -----
        This is the primary control for text DPI. It affects how Pango
        maps point sizes to pixels: ``pixels = points * dpi / 72``.
        Set this before measuring or rendering text to ensure consistent
        sizing across surfaces with different pixel densities.
        """
        return PangoCairo.context_get_resolution(self.pango_context)

    @resolution.setter
    def resolution(self, dpi: float) -> None:
        """Set the DPI used to convert point-sized fonts to device pixels.

        Parameters
        ----------
        dpi
            Resolution in dots per inch. Pass ``0`` or any negative value
            to inherit from the font map default (typically 96.0).
        """
        PangoCairo.context_set_resolution(self.pango_context, dpi)

    # ------------------------------------------------------------------
    # Properties with only getters
    # ------------------------------------------------------------------
    @property
    def gravity(self) -> Pango.Gravity:
        """Resolved gravity for the context (read-only).

        Returns
        -------
        Pango.Gravity
            Resolved gravity for the context.

        Notes
        -----
        Like ``base_gravity``, except when ``base_gravity`` is ``AUTO``,
        in which case the gravity is derived from the context matrix via
        ``Pango.Gravity.get_for_matrix``.
        """
        return self.pango_context.get_gravity()

    @property
    def serial(self) -> int:
        """Serial number incremented on every context or font-map change.

        Returns
        -------
        int
            Current serial number.

        Notes
        -----
        Initialized to a small positive value; never ``0``. May wrap —
        always compare with ``!=``, never ``<``.
        """
        return self.pango_context.get_serial()

    # ------------------------------------------------------------------
    # Properties with getters and setters (have separated interface)
    # ------------------------------------------------------------------
    @property
    def font_description(self) -> Pango.FontDescription | None:
        """Default font description for the context.

        Returns
        -------
        Pango.FontDescription | None
            Current font description, or ``None`` if not set.

        Notes
        -----
        The returned object is not a copy; call ``.copy()`` before modifying it.
        """
        return self.pango_context.get_font_description()

    @font_description.setter
    def font_description(self, desc: Pango.FontDescription | None) -> None:
        """Set the default font description for the context.

        Parameters
        ----------
        desc
            Font description to apply, or ``None`` to clear.
        """
        self.pango_context.set_font_description(desc)

    @property
    def font_map(self) -> Pango.FontMap | None:
        """Font map used for loading fonts.

        Returns
        -------
        Pango.FontMap | None
            Current font map, or ``None`` if not set.
        """
        return self.pango_context.get_font_map()

    @font_map.setter
    def font_map(self, font_map: Pango.FontMap | None) -> None:
        """Set the font map to be searched when fonts are looked up.

        Parameters
        ----------
        font_map
            Font map to apply, or ``None`` to use the default.

        Notes
        -----
        Intended for Pango backend use; a context obtained via
        ``FontMap.create_context()`` already has a suitable font map set.
        """
        self.pango_context.set_font_map(font_map)

    @property
    def language(self) -> Pango.Language:
        """Default language for the context.

        Returns
        -------
        Pango.Language
            Current default language.
        """
        return self.pango_context.get_language()

    @language.setter
    def language(self, language: Pango.Language | None) -> None:
        """Set the global language tag for the context.

        Parameters
        ----------
        language
            Language to apply, or ``None`` to restore the system locale
            default as returned by ``Pango.Language.get_default()``.
        """
        self.pango_context.set_language(language)

    @property
    def matrix(self) -> Pango.Matrix | None:
        """Transformation matrix applied to the context.

        Returns
        -------
        Pango.Matrix | None
            Current transformation matrix, or ``None`` if not set.
        """
        return self.pango_context.get_matrix()

    @matrix.setter
    def matrix(self, matrix: Pango.Matrix | None) -> None:
        """Set the transformation matrix applied when rendering with this context.

        Parameters
        ----------
        matrix
            Transformation matrix to apply, or ``None`` to clear.

        Notes
        -----
        Reported metrics are in user-space coordinates before the matrix is
        applied, so they do not scale with the matrix.
        """
        self.pango_context.set_matrix(matrix)

    # ------------------------------------------------------------------
    # Methods
    # ------------------------------------------------------------------
    def changed(self) -> None:
        """Force a change in the context, causing any layout using it to re-layout.

        Notes
        -----
        Intended for Pango backend implementors who attach extra data to a
        context; regular application code should not need to call this.
        """
        self.pango_context.changed()

    def get_metrics(
        self,
        desc: Pango.FontDescription | None = None,
        language: Pango.Language | None = None,
    ) -> Pango.FontMetrics:
        """Get overall metric information for a particular font description.

        Parameters
        ----------
        desc
            Font description to query; ``None`` uses the context default.
        language
            Language tag selecting which script's metrics to return;
            ``None`` uses the context default.

        Returns
        -------
        Pango.FontMetrics
            Font metrics for the given description and language.

        Notes
        -----
        Since metrics may differ substantially across scripts, providing a
        language tag ensures the correct script is measured. If the family
        name is a comma-separated list, the returned metrics are a composite
        of all loaded families.
        """
        return self.pango_context.get_metrics(desc, language)

    def list_families(self) -> list[Pango.FontFamily]:
        """Return all font families available in the current font map.

        Returns
        -------
        list[Pango.FontFamily]
            All font families in the current font map.
        """
        return self.pango_context.list_families()

    def load_font(self, desc: Pango.FontDescription) -> Pango.Font | None:
        """Load the font in one of the fontmaps in the context that is the closest match for desc.

        Parameters
        ----------
        desc
            Font description describing the font to load.

        Returns
        -------
        Pango.Font | None
            Loaded font, or ``None`` if no font matched.
        """
        return self.pango_context.load_font(desc)

    def load_fontset(
        self,
        desc: Pango.FontDescription,
        language: Pango.Language,
    ) -> Pango.Fontset | None:
        """Load a set of fonts in the context that can be used to render a font matching desc.

        Parameters
        ----------
        desc
            Font description describing the fonts to load.
        language
            Language the fonts will be used for.

        Returns
        -------
        Pango.Fontset | None
            Loaded fontset, or ``None`` if no font matched.
        """
        return self.pango_context.load_fontset(desc, language)
