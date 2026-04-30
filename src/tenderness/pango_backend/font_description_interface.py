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

"""Pango font description interface with typed attribute access."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, ClassVar, Self

import gi

from tenderness.core.base_interface import BaseInterface, BaseInterfaceParameters
from tenderness.core.sentinel import _UNSET_PARAM, Settable, SettableOrNone
from tenderness.pango_backend.pango_enum_coerce import (
    FontColorStr,
    GravityStr,
    PangoEnumCoerce,
    PangoEnumMap,
    StretchStr,
    StyleStr,
    VariantStr,
    WeightStr,
)

gi.require_version("Pango", "1.0")


from gi.repository import Pango  # noqa: E402

if TYPE_CHECKING:
    from tenderness.pango_backend.layout_interface import LayoutInterface


@dataclass(slots=True, frozen=True)
class FontDescriptionInterfaceParameters(BaseInterfaceParameters):
    """Keyword parameters for updating a FontDescriptionInterface.

    Parameters
    ----------
    family
        Font family name.
    features
        OpenType feature string; ``None`` clears the setting.
    gravity
        Glyph gravity.
    stretch
        Font stretch width.
    style
        Font style (normal, italic, or oblique).
    variant
        Font variant (normal or small caps).
    variations
        OpenType variations string; ``None`` clears the setting.
    weight
        Font weight.
    size_device_units
        Font size in device units; mutually exclusive with ``size``.
    size
        Font size in Pango units; mutually exclusive with ``size_device_units``.
    color
        Font color.
    """

    _COERCE_DISPATCH: ClassVar[dict[str, Any]] = {
        "gravity": lambda v: PangoEnumCoerce.coerce(PangoEnumMap.Gravity, v),
        "stretch": lambda v: PangoEnumCoerce.coerce(PangoEnumMap.Stretch, v),
        "style": lambda v: PangoEnumCoerce.coerce(PangoEnumMap.Style, v),
        "variant": lambda v: PangoEnumCoerce.coerce(PangoEnumMap.Variant, v),
        "weight": lambda v: PangoEnumCoerce.coerce(PangoEnumMap.Weight, v),
        "color": lambda v: PangoEnumCoerce.coerce(PangoEnumMap.FontColor, v),
    }

    _CONFLICTING_PAIRS: ClassVar[tuple[tuple[str, str], ...]] = (("size", "size_device_units"),)

    family: Settable[str] = field(default=_UNSET_PARAM)
    features: SettableOrNone[str] = field(default=_UNSET_PARAM)
    gravity: Settable[Pango.Gravity | GravityStr] = field(default=_UNSET_PARAM)
    stretch: Settable[Pango.Stretch | StretchStr] = field(default=_UNSET_PARAM)
    style: Settable[Pango.Style | StyleStr] = field(default=_UNSET_PARAM)
    variant: Settable[Pango.Variant | VariantStr] = field(default=_UNSET_PARAM)
    variations: SettableOrNone[str] = field(default=_UNSET_PARAM)
    weight: Settable[Pango.Weight | WeightStr] = field(default=_UNSET_PARAM)

    size_device_units: Settable[float] = field(default=_UNSET_PARAM)
    size: Settable[float] = field(default=_UNSET_PARAM)

    color: Settable[Pango.FontColor | FontColorStr] = field(default=_UNSET_PARAM)  # type: ignore[name-defined]

    def _validate(self, proposed: dict[str, Any]) -> None:
        for pango_field, device_field in self._CONFLICTING_PAIRS:
            if pango_field in proposed and device_field in proposed:
                msg = f"Cannot set both '{pango_field}' (Pango units) and '{device_field}' (device units) at the same time."
                raise ValueError(msg)

    def __post_init__(self) -> None:
        """Coerce enum fields and validate after initialization."""
        BaseInterfaceParameters.__post_init__(self)


class FontDescriptionInterface(BaseInterface):
    """Wrapper around Pango.FontDescription with typed property access.

    Notes
    -----
    See https://docs.gtk.org/Pango/struct.FontDescription.html

    1) Create — ``FontDescriptionInterface.from_new`` / ``FontDescriptionInterface.from_string``
    2) Update — ``FontDescriptionInterface.update_*()``
    3) Apply  — ``FontDescriptionInterface.apply_to_layout`` / ``FontDescriptionInterface.apply_to_layout_interface``
    """

    PANGO_SCALE: int = Pango.SCALE

    def __init__(self, font_description: Pango.FontDescription, name: str = "") -> None:
        super().__init__(name=name)
        self.font_description = font_description

    @classmethod
    def from_new(cls, name: str = "") -> Self:
        """Create a FontDescriptionInterface with a new empty font description."""
        return cls(font_description=Pango.FontDescription(), name=name)

    @classmethod
    def from_string(cls, font_desc_str: str, name: str = "") -> Self:
        """Create a FontDescriptionInterface from a Pango font description string.

        Notes
        -----
        See https://docs.gtk.org/Pango/type_func.FontDescription.from_string.html
        """
        return cls(font_description=Pango.FontDescription.from_string(font_desc_str), name=name)

    def apply_to_layout(self, layout: Pango.Layout) -> None:
        """Apply the font description to a Pango layout."""
        layout.set_font_description(self.font_description)

    def apply_to_layout_interface(self, layout_interface: LayoutInterface) -> None:
        """Apply the font description to a LayoutInterface."""
        layout_interface.font_description = self.font_description

    # ------------------------------------------------------------------
    # Properties with getters and setters
    # ------------------------------------------------------------------
    @property
    def color(self) -> Pango.FontColor:  # type: ignore[name-defined]
        """Font color."""
        return self.font_description.get_color()  # type: ignore[attr-defined]

    @color.setter
    def color(self, color: Pango.FontColor) -> None:  # type: ignore[name-defined]
        self.font_description.set_color(color)  # type: ignore[attr-defined]

    @property
    def family(self) -> str | None:
        """Font family name."""
        return self.font_description.get_family()

    @family.setter
    def family(self, family: str) -> None:
        self.font_description.set_family(family)

    @property
    def features(self) -> str | None:
        """OpenType feature string."""
        return self.font_description.get_features()

    @features.setter
    def features(self, features: str | None) -> None:
        self.font_description.set_features(features)

    @property
    def gravity(self) -> Pango.Gravity:
        """Glyph gravity."""
        return self.font_description.get_gravity()

    @gravity.setter
    def gravity(self, gravity: Pango.Gravity) -> None:
        self.font_description.set_gravity(gravity)

    @property
    def stretch(self) -> Pango.Stretch:
        """Font stretch width."""
        return self.font_description.get_stretch()

    @stretch.setter
    def stretch(self, stretch: Pango.Stretch) -> None:
        self.font_description.set_stretch(stretch)

    @property
    def style(self) -> Pango.Style:
        """Font style (normal, italic, or oblique)."""
        return self.font_description.get_style()

    @style.setter
    def style(self, style: Pango.Style) -> None:
        self.font_description.set_style(style)

    @property
    def variant(self) -> Pango.Variant:
        """Font variant (normal or small caps)."""
        return self.font_description.get_variant()

    @variant.setter
    def variant(self, variant: Pango.Variant) -> None:
        self.font_description.set_variant(variant)

    @property
    def variations(self) -> str | None:
        """OpenType variations string."""
        return self.font_description.get_variations()

    @variations.setter
    def variations(self, variations: str | None) -> None:
        self.font_description.set_variations(variations)

    @property
    def weight(self) -> Pango.Weight:
        """Font weight."""
        return self.font_description.get_weight()

    @weight.setter
    def weight(self, weight: Pango.Weight) -> None:
        self.font_description.set_weight(weight)

    # ------------------------------------------------------------------
    # Properties with only getters
    # ------------------------------------------------------------------
    @property
    def size_is_absolute(self) -> bool:
        """True when the font size was set as an absolute device-unit value."""
        return self.font_description.get_size_is_absolute()

    @property
    def hash(self) -> int:
        """Hash value for the font description."""
        return self.font_description.hash()

    @property
    def to_filename(self) -> str | None:
        """Font description as a filename-compatible string."""
        return self.font_description.to_filename()

    @property
    def to_string(self) -> str:
        """Font description as a Pango string representation."""
        return self.font_description.to_string()

    # ------------------------------------------------------------------
    # Methods
    # ------------------------------------------------------------------
    def better_match(self, old_match: Pango.FontDescription | None, new_match: Pango.FontDescription) -> bool:
        """Return True if new_match is a closer match to this description than old_match."""
        return self.font_description.better_match(old_match, new_match)

    def copy(self) -> Pango.FontDescription | None:
        """Return a copy of the underlying Pango.FontDescription."""
        return self.font_description.copy()

    def copy_static(self) -> Pango.FontDescription | None:
        """Return a copy suitable for stack allocation."""
        return self.font_description.copy_static()

    def equal(self, desc2: Pango.FontDescription) -> bool:
        """Return True if desc2 has the same attributes as this description."""
        return self.font_description.equal(desc2)

    def free(self) -> None:
        """Free the underlying Pango.FontDescription."""
        self.font_description.free()

    def get_set_fields(self) -> Pango.FontMask:
        """Return a bitmask of the fields that have been explicitly set."""
        return self.font_description.get_set_fields()

    def merge(self, desc_to_merge: Pango.FontDescription | None, *, replace_existing: bool) -> None:
        """Merge desc_to_merge into this description.

        Parameters
        ----------
        desc_to_merge
            Description to merge in; ``None`` is a no-op.
        replace_existing
            When ``True``, fields already set in this description are overwritten.
        """
        self.font_description.merge(desc_to_merge, replace_existing)

    def merge_static(self, desc_to_merge: Pango.FontDescription, *, replace_existing: bool) -> None:
        """Merge desc_to_merge without copying; the caller must keep it alive.

        Parameters
        ----------
        desc_to_merge
            Description to merge in; must outlive this description.
        replace_existing
            When ``True``, fields already set in this description are overwritten.
        """
        self.font_description.merge_static(desc_to_merge, replace_existing)

    def set_family_static(self, family: str) -> None:
        """Set the family without copying the string; the caller must keep it alive."""
        self.font_description.set_family_static(family)

    def set_features_static(self, features: str) -> None:
        """Set features without copying the string; the caller must keep it alive."""
        self.font_description.set_features_static(features)

    def set_variations_static(self, variations: str) -> None:
        """Set variations without copying the string; the caller must keep it alive."""
        self.font_description.set_variations_static(variations)

    def unset_fields(self, fields: Pango.FontMask) -> None:
        """Unset the specified fields, reverting them to their default values."""
        self.font_description.unset_fields(fields)

    # ------------------------------------------------------------------
    # Size
    # ------------------------------------------------------------------
    @property
    def size(self) -> float | None:
        """Font size in Pango units; ``None`` when an absolute device size is set."""
        if self.size_is_absolute:
            return None
        return Pango.units_to_double(self.font_description.get_size())

    @size.setter
    def size(self, size: int) -> None:
        self.font_description.set_size(Pango.units_from_double(size))

    @property
    def size_device_units(self) -> float | None:
        """Font size in device units; ``None`` when a Pango-unit size is set."""
        if not self.size_is_absolute:
            return None
        return Pango.units_to_double(self.font_description.get_size())

    @size_device_units.setter
    def size_device_units(self, size: float) -> None:
        self.font_description.set_absolute_size(Pango.units_from_double(size))
