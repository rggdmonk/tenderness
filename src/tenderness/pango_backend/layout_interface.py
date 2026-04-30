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

"""Defines `LayoutInterface` as a wrapper around `Pango.Layout` for easier access to its parameters and geometry calculations."""

from __future__ import annotations

import logging
import pathlib
from dataclasses import dataclass, field
from enum import StrEnum, unique
from typing import TYPE_CHECKING, Any, ClassVar, Self

import gi

from tenderness.core.base_interface import BaseInterface, BaseInterfaceParameters
from tenderness.core.sentinel import _UNSET_PARAM, Settable, SettableOrNone
from tenderness.pango_backend.layout_interface_geometry import (
    ClippedText,
    ExtentsMode,
    FitsResult,
    HeightConstraint,
    HeightDeviceUnits,
    HeightLineLimit,
    HeightSingleLine,
    LayoutFitReport,
    LayoutRect,
    WidthConstraint,
    WidthDeviceUnits,
    WidthUnconstrained,
)
from tenderness.pango_backend.pango_enum_coerce import (
    AlignmentStr,
    EllipsizeModeStr,
    PangoEnumCoerce,
    PangoEnumMap,
    WrapModeStr,
)

gi.require_version("Pango", "1.0")
gi.require_version("PangoCairo", "1.0")


from gi.repository import GLib, Pango, PangoCairo  # noqa: E402

if TYPE_CHECKING:
    import cairo


logger = logging.getLogger(__name__)


@unique
class TextStrategy(StrEnum):  # noqa: D101 TODO: docstring
    TEXT = "text"
    MARKUP = "markup"


@dataclass(slots=True, frozen=True)
class LayoutInterfaceParameters(BaseInterfaceParameters):  # noqa: D101 TODO: docstring
    _COERCE_DISPATCH: ClassVar[dict[str, Any]] = {
        "alignment": lambda v: PangoEnumCoerce.coerce(PangoEnumMap.Alignment, v),
        "ellipsize": lambda v: PangoEnumCoerce.coerce(PangoEnumMap.EllipsizeMode, v),
        "wrap": lambda v: PangoEnumCoerce.coerce(PangoEnumMap.WrapMode, v),
    }

    _CONFLICTING_PAIRS: ClassVar[tuple[tuple[str, str], ...]] = (
        ("width", "width_device_units"),
        ("height", "height_device_units"),
        ("indent", "indent_device_units"),
        ("spacing", "spacing_device_units"),
    )

    # --- Geometry: device units ---
    width_device_units: Settable[WidthConstraint | float] = field(default=_UNSET_PARAM)
    height_device_units: Settable[HeightConstraint | float] = field(default=_UNSET_PARAM)
    indent_device_units: Settable[float] = field(default=_UNSET_PARAM)
    spacing_device_units: Settable[float] = field(default=_UNSET_PARAM)

    alignment: Settable[Pango.Alignment | AlignmentStr] = field(default=_UNSET_PARAM)
    auto_dir: Settable[bool] = field(default=_UNSET_PARAM)
    ellipsize: Settable[Pango.EllipsizeMode | EllipsizeModeStr] = field(default=_UNSET_PARAM)
    justify: Settable[bool] = field(default=_UNSET_PARAM)
    justify_last_line: Settable[bool] = field(default=_UNSET_PARAM)
    line_spacing: Settable[float] = field(default=_UNSET_PARAM)
    single_paragraph_mode: Settable[bool] = field(default=_UNSET_PARAM)
    wrap: Settable[Pango.WrapMode | WrapModeStr] = field(default=_UNSET_PARAM)

    attributes: SettableOrNone[Pango.AttrList] = field(default=_UNSET_PARAM)
    tabs: SettableOrNone[Pango.TabArray] = field(default=_UNSET_PARAM)
    font_description: SettableOrNone[Pango.FontDescription] = field(default=_UNSET_PARAM)

    # --- Geometry: Pango units ---
    width: Settable[int] = field(default=_UNSET_PARAM)
    height: Settable[int] = field(default=_UNSET_PARAM)
    indent: Settable[int] = field(default=_UNSET_PARAM)
    spacing: Settable[int] = field(default=_UNSET_PARAM)

    def _validate(self, proposed: dict[str, Any]) -> None:
        for pango_field, device_field in self._CONFLICTING_PAIRS:
            if pango_field in proposed and device_field in proposed:
                msg = f"Cannot set both '{pango_field}' (Pango units) and '{device_field}' (device units) at the same time."
                raise ValueError(msg)

    def __post_init__(self) -> None:  # noqa: D105 TODO: docstring
        BaseInterfaceParameters.__post_init__(self)


class LayoutInterface(BaseInterface):
    """
    Wrapper for Pango.Layout for easier access to its parameters.
    See: https://docs.gtk.org/Pango/class.Layout.html
    """  # noqa: D205, D400 TODO: docstring

    PANGO_SCALE: int = Pango.SCALE

    def __init__(self, pango_layout: Pango.Layout, name: str = "") -> None:
        super().__init__(name=name)
        self.pango_layout = pango_layout

    @classmethod
    def from_cairo_context(cls, cairo_context: cairo.Context[cairo.Surface], name: str = "") -> Self:  # noqa: D102 TODO: docstring
        pango_layout = PangoCairo.create_layout(cairo_context)
        return cls(pango_layout=pango_layout, name=name)

    # ------------------------------------------------------------------
    # Serialization
    # ------------------------------------------------------------------
    def serialize_layout(  # noqa: D102 TODO: docstring
        self,
        *,
        context: bool = False,
        output: bool = False,
        filepath: pathlib.Path | None = None,
    ) -> str:
        flags = Pango.LayoutSerializeFlags.DEFAULT
        if context:
            flags |= Pango.LayoutSerializeFlags.CONTEXT
        if output:
            flags |= Pango.LayoutSerializeFlags.OUTPUT

        if filepath is not None:
            filepath = pathlib.Path(filepath)
            try:
                success = self.pango_layout.write_to_file(flags, str(filepath))
                if not success:
                    msg = f"Failed to write layout to file: {filepath}"
                    raise RuntimeError(msg)
            except GLib.Error as e:
                msg = f"Error writing layout to file: {filepath} - {e.message}"
                raise RuntimeError(msg) from e

        data = self.pango_layout.serialize(flags).get_data()

        if data is None:
            msg = "Failed to serialize layout: No data returned"
            raise RuntimeError(msg)

        return data.decode(encoding="utf-8", errors="strict")

    # ------------------------------------------------------------------
    # Text
    # ------------------------------------------------------------------
    def add_text_to_layout(self, text: str, length: int = -1, strategy: TextStrategy | str = TextStrategy.TEXT) -> None:  # noqa: D102 TODO: docstring
        if strategy == TextStrategy.TEXT:
            self.set_text(text=text, length=length)
        elif strategy == TextStrategy.MARKUP:
            self.set_markup(markup=text, length=length)
        else:
            msg = f"Unsupported text strategy: {strategy}"
            raise ValueError(msg)

    @property
    def text(self) -> str:  # noqa: D102 TODO: docstring
        return self.pango_layout.get_text()

    def set_text(self, text: str, length: int = -1) -> None:  # noqa: D102 TODO: docstring
        self.pango_layout.set_text(text, length)

    def set_markup(self, markup: str, length: int = -1) -> None:  # noqa: D102 TODO: docstring
        self.pango_layout.set_markup(markup, length)  # type: ignore

    def set_markup_with_accel(self) -> None:  # noqa: D102 TODO: docstring
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Properties with getters and setters
    # ------------------------------------------------------------------
    @property
    def alignment(self) -> Pango.Alignment:  # noqa: D102 TODO: docstring
        return self.pango_layout.get_alignment()

    @alignment.setter
    def alignment(self, alignment: Pango.Alignment) -> None:
        self.pango_layout.set_alignment(alignment)

    @property
    def auto_dir(self) -> bool:  # noqa: D102 TODO: docstring
        return self.pango_layout.get_auto_dir()

    @auto_dir.setter
    def auto_dir(self, auto_dir: bool) -> None:
        self.pango_layout.set_auto_dir(auto_dir)

    @property
    def ellipsize(self) -> Pango.EllipsizeMode:  # noqa: D102 TODO: docstring
        return self.pango_layout.get_ellipsize()

    @ellipsize.setter
    def ellipsize(self, ellipsize: Pango.EllipsizeMode) -> None:
        self.pango_layout.set_ellipsize(ellipsize)

    @property
    def justify(self) -> bool:  # noqa: D102 TODO: docstring
        return self.pango_layout.get_justify()

    @justify.setter
    def justify(self, justify: bool) -> None:
        self.pango_layout.set_justify(justify)

    @property
    def justify_last_line(self) -> bool:  # noqa: D102 TODO: docstring
        return self.pango_layout.get_justify_last_line()

    @justify_last_line.setter
    def justify_last_line(self, justify_last_line: bool) -> None:
        self.pango_layout.set_justify_last_line(justify_last_line)

    @property
    def line_spacing(self) -> float:  # noqa: D102 TODO: docstring
        return self.pango_layout.get_line_spacing()

    @line_spacing.setter
    def line_spacing(self, factor: float) -> None:
        self.pango_layout.set_line_spacing(factor)

    @property
    def single_paragraph_mode(self) -> bool:  # noqa: D102 TODO: docstring
        return self.pango_layout.get_single_paragraph_mode()

    @single_paragraph_mode.setter
    def single_paragraph_mode(self, setting: bool) -> None:
        self.pango_layout.set_single_paragraph_mode(setting)

    @property
    def wrap(self) -> Pango.WrapMode:  # noqa: D102 TODO: docstring
        return self.pango_layout.get_wrap()

    @wrap.setter
    def wrap(self, wrap: Pango.WrapMode) -> None:
        self.pango_layout.set_wrap(wrap)

    # ------------------------------------------------------------------
    # Properties with only getters
    # ------------------------------------------------------------------
    @property
    def baseline(self) -> int:  # noqa: D102 TODO: docstring
        return self.pango_layout.get_baseline()

    @property
    def character_count(self) -> int:  # noqa: D102 TODO: docstring
        return self.pango_layout.get_character_count()

    @property
    def line_count(self) -> int:  # noqa: D102 TODO: docstring
        return self.pango_layout.get_line_count()

    @property
    def pixel_size(self) -> tuple[int, int]:
        """Content size in device units (logical)."""
        return self.pango_layout.get_pixel_size()

    @property
    def serial(self) -> int:  # noqa: D102 TODO: docstring
        return self.pango_layout.get_serial()

    @property
    def size(self) -> tuple[int, int]:
        """Content size in Pango units (logical)."""
        return self.pango_layout.get_size()

    @property
    def unknown_glyphs_count(self) -> int:  # noqa: D102 TODO: docstring
        return self.pango_layout.get_unknown_glyphs_count()

    @property
    def is_ellipsized(self) -> bool:  # noqa: D102 TODO: docstring
        return self.pango_layout.is_ellipsized()

    @property
    def is_wrapped(self) -> bool:  # noqa: D102 TODO: docstring
        return self.pango_layout.is_wrapped()

    # ------------------------------------------------------------------
    # Properties with getters and setters (have separated interface)
    # ------------------------------------------------------------------
    @property
    def font_description(self) -> Pango.FontDescription | None:
        """Read-only pointer — call `.copy()` before modifying."""
        return self.pango_layout.get_font_description()

    @font_description.setter
    def font_description(self, desc: Pango.FontDescription | None) -> None:
        self.pango_layout.set_font_description(desc)

    @property
    def attributes(self) -> Pango.AttrList | None:  # noqa: D102 TODO: docstring
        return self.pango_layout.get_attributes()

    @attributes.setter
    def attributes(self, attrs: Pango.AttrList | None) -> None:
        self.pango_layout.set_attributes(attrs)

    @property
    def tabs(self) -> Pango.TabArray | None:  # noqa: D102 TODO: docstring
        return self.pango_layout.get_tabs()

    @tabs.setter
    def tabs(self, tabs: Pango.TabArray | None) -> None:
        self.pango_layout.set_tabs(tabs)

    # ------------------------------------------------------------------
    # Methods
    # ------------------------------------------------------------------
    def context_changed(self) -> None:  # noqa: D102 TODO: docstring
        self.pango_layout.context_changed()

    def copy(self) -> Pango.Layout:  # noqa: D102 TODO: docstring
        return self.pango_layout.copy()

    def get_caret_pos(self, index_: int) -> tuple[Pango.Rectangle, Pango.Rectangle]:  # noqa: D102 TODO: docstring
        return self.pango_layout.get_caret_pos(index_)

    def get_context(self) -> Pango.Context:  # noqa: D102 TODO: docstring
        return self.pango_layout.get_context()

    def get_cursor_pos(self, index_: int) -> tuple[Pango.Rectangle, Pango.Rectangle]:  # noqa: D102 TODO: docstring
        return self.pango_layout.get_cursor_pos(index_)

    def get_direction(self, index: int) -> Pango.Direction:  # noqa: D102 TODO: docstring
        return self.pango_layout.get_direction(index)

    def get_iter(self) -> Pango.LayoutIter:  # noqa: D102 TODO: docstring
        return self.pango_layout.get_iter()

    def get_line(self, line: int) -> Pango.LayoutLine | None:  # noqa: D102 TODO: docstring
        return self.pango_layout.get_line(line)

    def get_line_readonly(self, line: int) -> Pango.LayoutLine | None:  # noqa: D102 TODO: docstring
        return self.pango_layout.get_line_readonly(line)

    def get_lines(self) -> list[Pango.LayoutLine]:  # noqa: D102 TODO: docstring
        return self.pango_layout.get_lines()

    def get_lines_readonly(self) -> list[Pango.LayoutLine]:  # noqa: D102 TODO: docstring
        return self.pango_layout.get_lines_readonly()

    def get_log_attrs(self) -> list[Pango.LogAttr]:  # noqa: D102 TODO: docstring
        return self.pango_layout.get_log_attrs()

    def get_log_attrs_readonly(self) -> list[Pango.LogAttr]:  # noqa: D102 TODO: docstring
        return self.pango_layout.get_log_attrs_readonly()

    def index_to_line_x(self, *, index_: int, trailing: bool) -> tuple[int, int]:  # noqa: D102 TODO: docstring
        return self.pango_layout.index_to_line_x(index_, trailing)

    def index_to_pos(self, index_: int) -> Pango.Rectangle:  # noqa: D102 TODO: docstring
        return self.pango_layout.index_to_pos(index_)

    def move_cursor_visually(  # noqa: D102 TODO: docstring
        self, *, strong: bool, old_index: int, old_trailing: int, direction: int
    ) -> tuple[int, int]:
        return self.pango_layout.move_cursor_visually(strong, old_index, old_trailing, direction)

    def serialize(self, flags: Pango.LayoutSerializeFlags) -> GLib.Bytes:  # noqa: D102 TODO: docstring
        return self.pango_layout.serialize(flags)

    def write_to_file(self, flags: Pango.LayoutSerializeFlags, filename: str) -> bool:  # noqa: D102 TODO: docstring
        return self.pango_layout.write_to_file(flags, filename)

    def xy_to_index(self, x: int, y: int) -> tuple[bool, int, int]:  # noqa: D102 TODO: docstring
        return self.pango_layout.xy_to_index(x, y)

    # ------------------------------------------------------------------
    # Extents
    # ------------------------------------------------------------------
    @property
    def extents(self) -> tuple[Pango.Rectangle, Pango.Rectangle]:
        """(ink, logical) extents in Pango units."""
        return self.pango_layout.get_extents()

    @property
    def extents_layout_rect(self) -> tuple[LayoutRect, LayoutRect]:  # noqa: D102 TODO: docstring
        ink, logical = self.extents
        return (
            LayoutRect.from_pango_rectangle(rect=ink),
            LayoutRect.from_pango_rectangle(rect=logical),
        )

    @property
    def extents_ink_layout_rect(self) -> LayoutRect:  # noqa: D102 TODO: docstring
        ink, _ = self.extents
        return LayoutRect.from_pango_rectangle(rect=ink)

    @property
    def extents_logical_layout_rect(self) -> LayoutRect:  # noqa: D102 TODO: docstring
        _, logical = self.extents
        return LayoutRect.from_pango_rectangle(rect=logical)

    # ------------------------------------------------------------------
    # Width (Pango units + device units)
    # ------------------------------------------------------------------
    @property
    def width(self) -> int:
        """
        Width in Pango units. Default `-1`.

        Returns
        -------
            width: Width value.
        """
        return self.pango_layout.get_width()

    @width.setter
    def width(self, width: int) -> None:
        """
        Set width in Pango units.

        Note: any negative value will be converted to `-1` by Pango.

        Width semantics:
        - `-1` (default): unconstrained width (single line).
        - `> 0`: width in Pango units.
        - `= 0`: width follows `Pango.WrapMode` and `Pango.EllipsizeMode` rules (better not use this).

        Parameters
        ----------
        width
             Width value in Pango units. Negative values will be treated as `-1` (unconstrained).

        """
        self.pango_layout.set_width(width)

    @property
    def width_device_units(self) -> WidthConstraint:  # noqa: D102 TODO: docstring
        width = self.width

        if width < 0:  # any negative value is converted to -1 by Pango
            return WidthUnconstrained()

        if width == 0:
            msg = "Width is in special mode (0), not device unit mode."
            raise ValueError(msg)

        return WidthDeviceUnits(width=Pango.units_to_double(width))

    @width_device_units.setter
    def width_device_units(self, width: float | WidthConstraint) -> None:  # TODO: docstring

        if isinstance(width, WidthUnconstrained) or width == -1:
            self.width = -1
            return

        if isinstance(width, WidthDeviceUnits):
            width_value = float(width.width)
        elif isinstance(width, (float, int)):
            width_value = float(width)
        else:
            msg = f"Invalid type for width: {type(width)}. Expected {WidthConstraint.__name__} or float."
            raise TypeError(msg)

        if width_value <= 0:
            msg = "Width must be positive in device unit mode."
            raise ValueError(msg)

        self.width = Pango.units_from_double(width_value)

    # ------------------------------------------------------------------
    # Height (Pango units + device units)
    # ------------------------------------------------------------------
    @property
    def height(self) -> int:
        """
        Height in Pango units. Default `-1`.

        Returns
        -------
            height: Height value.
        """
        return self.pango_layout.get_height()

    @height.setter
    def height(self, height: int) -> None:
        """
        Set height in Pango units. Only works if `width` is `> 0`.

        Height semantics:

        - `> 0`: height in Pango units.
            Note:
                If `Pango.EllipsizeMode.None` the content will flow freely but won't be visible beyond the specified height.
                If `Pango.EllipsizeMode.START/END/MIDDLE` the content will be truncated to fit within the specified height,
                and an ellipsis will be shown at the truncation point.

        - `= 0`: exactly one line of text, regardless of how much space it takes.

        - `< 0`: maximum number of lines PER paragraph.
            Note:
                If `Pango.EllipsizeMode.None` the content will flow freely but won't be visible beyond the specified number of lines.
                If `Pango.EllipsizeMode.START/END/MIDDLE` the content will be truncated to fit within the specified number of lines,
                and an ellipsis will be shown at the truncation point.

        Parameters
        ----------
        height
            Height value in Pango units. Note that any negative value will be treated as a line limit, and zero is a special mode for exactly one line.

        """
        self.pango_layout.set_height(height)

    @property
    def height_device_units(self) -> HeightConstraint:  # noqa: D102 TODO: docstring
        height = self.height
        if height > 0:
            return HeightDeviceUnits(height=Pango.units_to_double(height))
        if height == 0:
            return HeightSingleLine()
        # height < 0: negative of max lines per paragraph
        return HeightLineLimit(lines=abs(height))

    @height_device_units.setter
    def height_device_units(
        self,
        height: float | HeightConstraint,
    ) -> None:
        if isinstance(height, HeightDeviceUnits):
            if height.height <= 0:
                msg = "HeightDeviceUnits.height must be positive."
                raise ValueError(msg)
            self.height = Pango.units_from_double(height.height)
        elif isinstance(height, HeightLineLimit):
            if height.lines <= 0:
                msg = "HeightLineLimit.lines must be positive."
                raise ValueError(msg)
            self.height = -height.lines
        elif isinstance(height, HeightSingleLine):
            self.height = 0
        elif isinstance(height, (float, int)):
            # bare numeric: positive = device units, negative = line limit, 0 = single line
            value = float(height)
            if value > 0:
                self.height = Pango.units_from_double(value)
            elif value == 0:
                self.height = 0
            else:
                self.height = int(height)
        else:
            msg = f"Invalid type for height: {type(height)}. Expected {HeightConstraint.__name__} or float, int."
            raise TypeError(msg)

    # ------------------------------------------------------------------
    # Indent (Pango units + device units)
    # ------------------------------------------------------------------
    @property
    def indent(self) -> int:
        """Paragraph indent in Pango units."""
        return self.pango_layout.get_indent()

    @indent.setter
    def indent(self, indent: int) -> None:
        self.pango_layout.set_indent(indent)

    @property
    def indent_device_units(self) -> float:  # noqa: D102 TODO: docstring
        return Pango.units_to_double(self.indent)

    @indent_device_units.setter
    def indent_device_units(self, indent: float) -> None:
        self.indent = Pango.units_from_double(indent)

    # ------------------------------------------------------------------
    # Pixel extents
    # ------------------------------------------------------------------
    @property
    def pixel_extents(self) -> tuple[Pango.Rectangle, Pango.Rectangle]:
        """(ink, logical) extents in device units."""
        return self.pango_layout.get_pixel_extents()

    @property
    def pixel_extents_layout_rect(self) -> tuple[LayoutRect, LayoutRect]:  # noqa: D102 TODO: docstring
        ink, logical = self.pixel_extents
        return (
            LayoutRect.from_pango_rectangle(rect=ink),
            LayoutRect.from_pango_rectangle(rect=logical),
        )

    @property
    def pixel_extents_ink_layout_rect(self) -> LayoutRect:  # noqa: D102 TODO: docstring
        ink, _ = self.pixel_extents
        return LayoutRect.from_pango_rectangle(rect=ink)

    @property
    def pixel_extents_logical_layout_rect(self) -> LayoutRect:  # noqa: D102 TODO: docstring
        _, logical = self.pixel_extents
        return LayoutRect.from_pango_rectangle(rect=logical)

    # ------------------------------------------------------------------
    # Spacing (Pango units + device units)
    # ------------------------------------------------------------------
    @property
    def spacing(self) -> int:
        """Inter-line spacing in Pango units."""
        return self.pango_layout.get_spacing()

    @spacing.setter
    def spacing(self, spacing: int) -> None:
        self.pango_layout.set_spacing(spacing)

    @property
    def spacing_device_units(self) -> float:  # noqa: D102 TODO: docstring
        return Pango.units_to_double(self.spacing)

    @spacing_device_units.setter
    def spacing_device_units(self, spacing: float) -> None:
        self.spacing = Pango.units_from_double(spacing)

    # ------------------------------------------------------------------
    # Layout fit report (logical fits, ink fits, clipped text)
    # ------------------------------------------------------------------
    def get_layout_fit_report(self, height_override: HeightConstraint | None = None) -> LayoutFitReport:  # noqa: C901 # TODO: refactor to reduce complexity
        """
        Compute logical fits, ink fits, and clipped text in a single pass.

        Walks the layout line iterator once to determine the last visible line
        under the active height constraint, then derives all three results from
        that single traversal.

        Returns
        -------
            `LayoutFitReport` with logical fits, ink fits, and clipped text.
        """
        full_text = self.text
        encoded = full_text.encode("utf-8")

        height_constraint = height_override if height_override is not None else self.height_device_units
        max_height_pango: int | None = None

        if isinstance(height_constraint, HeightDeviceUnits):
            max_height_pango = Pango.units_from_double(height_constraint.height)

        iter_ = self.pango_layout.get_iter()
        last_index = 0
        last_line = 0
        line_index = 0

        while True:
            line = iter_.get_line_readonly()

            if line is not None:
                if max_height_pango is not None:
                    _, y1 = iter_.get_line_yrange()
                    if y1 > max_height_pango:
                        break

                last_index = line.start_index + line.length
                last_line = line_index

            if not iter_.next_line():
                break
            line_index += 1

        # --- ClippedText ---
        visible = encoded[:last_index].decode("utf-8")
        clipped = encoded[last_index:].decode("utf-8")
        clipped_text = ClippedText(
            visible=visible,
            clipped=clipped,
            last_visible_line=last_line,
            clipped_char_byte_index=last_index,
        )

        # --- height_fits — derived from the iterator walk ---
        if isinstance(height_constraint, HeightDeviceUnits):
            height_fits = not clipped_text.has_clipped
        elif isinstance(height_constraint, HeightSingleLine):
            height_fits = True
        else:  # HeightLineLimit
            height_fits = not self.is_ellipsized

        # --- width_fits ---
        width = self.width_device_units

        ink_rect, logical_rect = self.pixel_extents_layout_rect

        if isinstance(width, WidthUnconstrained):
            logical_width_fits = True
            ink_width_fits = True
        elif isinstance(width, WidthDeviceUnits):
            logical_width_fits = logical_rect.x_min >= 0 and logical_rect.x_max <= width.width
            ink_width_fits = ink_rect.x_min >= 0 and ink_rect.x_max <= width.width
        else:
            msg = f"Invalid width type: {type(width)}. Expected {WidthConstraint.__name__}."
            raise TypeError(msg)

        ellipsize = self.ellipsize
        wrap = self.wrap
        unknown_glyphs_count = self.unknown_glyphs_count

        return LayoutFitReport(
            fits_logical=FitsResult(
                extents_mode=ExtentsMode.LOGICAL,
                width=logical_width_fits,
                height=height_fits,
                ellipsis=ellipsize,
                wrap=wrap,
                rect=logical_rect,
                width_device_units=width,
                height_device_units=height_constraint,
                unknown_glyphs_count=unknown_glyphs_count,
            ),
            fits_ink=FitsResult(
                extents_mode=ExtentsMode.INK,
                width=ink_width_fits,
                height=height_fits,
                ellipsis=ellipsize,
                wrap=wrap,
                rect=ink_rect,
                width_device_units=width,
                height_device_units=height_constraint,
                unknown_glyphs_count=unknown_glyphs_count,
            ),
            clipped_text=clipped_text,
        )
