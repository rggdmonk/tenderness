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

"""Layout interface."""

from __future__ import annotations

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


@unique
class TextStrategy(StrEnum):
    """Text strategy for ``add_text_to_layout``.

    Attributes
    ----------
    TEXT
        Plain text.
    MARKUP
        Pango markup.
    """

    TEXT = "text"
    MARKUP = "markup"


@dataclass(slots=True, frozen=True)
class LayoutInterfaceParameters(BaseInterfaceParameters):
    """Configuration parameters for LayoutInterface.

    Attributes
    ----------
    width_device_units
        Width in device units; exclusive with ``width``.
    height_device_units
        Height in device units or line constraint; exclusive with ``height``.
    indent_device_units
        Paragraph indent in device units; exclusive with ``indent``.
    spacing_device_units
        Inter-line spacing in device units; exclusive with ``spacing``.
    alignment
        Paragraph alignment.
    auto_dir
        Auto-detect text direction.
    ellipsize
        Ellipsis mode.
    justify
        Justify lines.
    justify_last_line
        Justify last line.
    line_spacing
        Line spacing factor.
    single_paragraph_mode
        Treat text as single paragraph.
    wrap
        Wrap mode.
    attributes
        Text attributes; ``None`` clears.
    tabs
        Tab stops; ``None`` clears.
    font_description
        Font description; ``None`` clears.
    width
        Width in Pango units; exclusive with ``width_device_units``.
    height
        Height in Pango units; exclusive with ``height_device_units``.
    indent
        Indent in Pango units; exclusive with ``indent_device_units``.
    spacing
        Inter-line spacing in Pango units; exclusive with ``spacing_device_units``.
    """

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

    def __post_init__(self) -> None:
        """Coerce values and validate parameters after initialization."""
        BaseInterfaceParameters.__post_init__(self)


class LayoutInterface(BaseInterface):
    """Interface for layout.

    Attributes
    ----------
    PANGO_SCALE
        Scale between Pango distances and device units (``Pango.SCALE``, currently 1024).

    Notes
    -----
    See https://docs.gtk.org/Pango/class.Layout.html

    1. Create with ``from_cairo_context()``.
    2. Update with ``update_with_parameters()`` or through properties.
    """

    PANGO_SCALE: int = Pango.SCALE

    def __init__(self, pango_layout: Pango.Layout, name: str = "") -> None:
        """Initialize LayoutInterface.

        Parameters
        ----------
        pango_layout
            Underlying Pango layout object.
        name
            Optional label for the interface instance.
        """
        super().__init__(name=name)
        self.pango_layout = pango_layout

    @classmethod
    def from_cairo_context(cls, cairo_context: cairo.Context[cairo.Surface], name: str = "") -> Self:
        """Create from a Cairo context.

        Parameters
        ----------
        cairo_context
            Cairo context used to create the Pango layout.
        name
            Optional label for the interface instance.

        Returns
        -------
        Self
            ``LayoutInterface`` backed by the given Cairo context.
        """
        pango_layout = PangoCairo.create_layout(cairo_context)
        return cls(pango_layout=pango_layout, name=name)

    # ------------------------------------------------------------------
    # Serialization
    # ------------------------------------------------------------------
    def serialize_layout(
        self,
        *,
        context: bool = False,
        output: bool = False,
        filepath: pathlib.Path | None = None,
    ) -> str:
        """Serialize the layout to a UTF-8 string, optionally writing to a file.

        Parameters
        ----------
        context
            Include Pango context in output.
        output
            Include output state in output.
        filepath
            Write to this path; ``None`` skips file writing.

        Returns
        -------
        str
            Serialized layout as UTF-8.

        Raises
        ------
        RuntimeError
            On write failure, GLib error, or no data returned.
        """
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
    def add_text_to_layout(self, text: str, length: int = -1, strategy: TextStrategy | str = TextStrategy.TEXT) -> None:
        """Set layout text, replacing any previous content.

        Parameters
        ----------
        text
            Plain text or Pango markup string.
        length
            Byte length of ``text`` to use; ``-1`` for the full string.
        strategy
            ``TEXT`` for plain text, ``MARKUP`` for Pango markup.

        Raises
        ------
        ValueError
            If ``strategy`` is not a recognized ``TextStrategy`` value.
        """
        if strategy == TextStrategy.TEXT:
            self.set_text(text=text, length=length)
        elif strategy == TextStrategy.MARKUP:
            self.set_markup(markup=text, length=length)
        else:
            msg = f"Unsupported text strategy: {strategy}"
            raise ValueError(msg)

    @property
    def text(self) -> str:
        """Current plain text of the layout.

        Returns
        -------
        str
            Plain text content without any markup.
        """
        return self.pango_layout.get_text()

    def set_text(self, text: str, length: int = -1) -> None:
        """Set the layout's plain text.

        Parameters
        ----------
        text
            Plain text to set.
        length
            Byte length of ``text`` to use; ``-1`` for the full string.

        Notes
        -----
        Invalid UTF-8 bytes are rendered as placeholder glyphs. Does not clear
        attributes set by a previous markup call; call ``attributes = None`` to reset.
        """
        self.pango_layout.set_text(text, length)

    def set_markup(self, markup: str, length: int = -1) -> None:
        """Set the layout's text as Pango markup.

        Parameters
        ----------
        markup
            Pango markup string to set.
        length
            Byte length of ``markup`` to use; ``-1`` for the full string.
        """
        self.pango_layout.set_markup(markup, length)  # type: ignore

    def set_markup_with_accel(self) -> None:
        """Set Pango markup with accelerator key processing.

        Raises
        ------
        NotImplementedError
            Always; not yet implemented.
        """
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Properties with getters and setters
    # ------------------------------------------------------------------
    @property
    def alignment(self) -> Pango.Alignment:
        """Horizontal alignment of lines.

        Returns
        -------
        Pango.Alignment
            Current horizontal alignment setting.
        """
        return self.pango_layout.get_alignment()

    @alignment.setter
    def alignment(self, alignment: Pango.Alignment) -> None:
        """Set the horizontal alignment of lines.

        Parameters
        ----------
        alignment
            Alignment to apply.
        """
        self.pango_layout.set_alignment(alignment)

    @property
    def auto_dir(self) -> bool:
        """Text direction auto-detected from content.

        Returns
        -------
        bool
            ``True`` if text direction is auto-detected from content.
        """
        return self.pango_layout.get_auto_dir()

    @auto_dir.setter
    def auto_dir(self, auto_dir: bool) -> None:
        """Enable or disable auto-detection of text direction from content.

        Parameters
        ----------
        auto_dir
            If ``True``, auto-detect text direction from content.

        Notes
        -----
        When disabled, direction follows the context's base direction.
        ``ALIGN_LEFT`` and ``ALIGN_RIGHT`` swap meaning when the auto-detected
        direction differs from the context.
        """
        self.pango_layout.set_auto_dir(auto_dir)

    @property
    def ellipsize(self) -> Pango.EllipsizeMode:
        """Ellipsization mode for text that exceeds layout dimensions.

        Returns
        -------
        Pango.EllipsizeMode
            Current ellipsization mode.

        Notes
        -----
        Use ``is_ellipsized`` to query whether any paragraphs were actually ellipsized.
        """
        return self.pango_layout.get_ellipsize()

    @ellipsize.setter
    def ellipsize(self, ellipsize: Pango.EllipsizeMode) -> None:
        """Set the ellipsization mode.

        Parameters
        ----------
        ellipsize
            Ellipsization mode to apply.
        """
        self.pango_layout.set_ellipsize(ellipsize)

    @property
    def justify(self) -> bool:
        """``True`` when lines are stretched to fill the entire layout width.

        Returns
        -------
        bool
            ``True`` if lines are stretched to fill the layout width.
        """
        return self.pango_layout.get_justify()

    @justify.setter
    def justify(self, justify: bool) -> None:
        """Enable or disable line stretching to fill the layout width.

        Parameters
        ----------
        justify
            If ``True``, stretch lines to fill the layout width.

        Notes
        -----
        Tabs and justification conflict: justification moves content away from
        tab-aligned positions.
        """
        self.pango_layout.set_justify(justify)

    @property
    def justify_last_line(self) -> bool:
        """``True`` when the last line is stretched to fill the layout width.

        Returns
        -------
        bool
            ``True`` if the last line is stretched to fill the layout width.
        """
        return self.pango_layout.get_justify_last_line()

    @justify_last_line.setter
    def justify_last_line(self, justify_last_line: bool) -> None:
        """Enable or disable stretching of the last line to fill the layout width.

        Parameters
        ----------
        justify_last_line
            If ``True``, stretch the last line to fill the layout width.

        Notes
        -----
        Only has effect when ``justify`` is enabled.
        """
        self.pango_layout.set_justify_last_line(justify_last_line)

    @property
    def line_spacing(self) -> float:
        """Inter-line spacing factor.

        Returns
        -------
        float
            Current inter-line spacing factor.
        """
        return self.pango_layout.get_line_spacing()

    @line_spacing.setter
    def line_spacing(self, factor: float) -> None:
        """Set the inter-line spacing factor.

        Parameters
        ----------
        factor
            Spacing factor to apply.
        """
        self.pango_layout.set_line_spacing(factor)

    @property
    def single_paragraph_mode(self) -> bool:
        """``True`` when single-paragraph mode is active.

        Returns
        -------
        bool
            ``True`` if text is treated as a single paragraph.
        """
        return self.pango_layout.get_single_paragraph_mode()

    @single_paragraph_mode.setter
    def single_paragraph_mode(self, setting: bool) -> None:
        """Enable or disable single-paragraph mode.

        Parameters
        ----------
        setting
            If ``True``, treat all text as a single paragraph.

        Notes
        -----
        When enabled, paragraph separators are rendered as glyphs rather than
        causing line breaks.
        """
        self.pango_layout.set_single_paragraph_mode(setting)

    @property
    def wrap(self) -> Pango.WrapMode:
        """Line wrapping mode.

        Returns
        -------
        Pango.WrapMode
            Current line wrapping mode.

        Notes
        -----
        Use ``is_wrapped`` to query whether any paragraphs were actually wrapped.
        """
        return self.pango_layout.get_wrap()

    @wrap.setter
    def wrap(self, wrap: Pango.WrapMode) -> None:
        """Set the line wrapping mode.

        Parameters
        ----------
        wrap
            Wrapping mode to apply.

        Notes
        -----
        Only has effect when a width is set; set ``width`` to ``-1`` to disable wrapping.
        """
        self.pango_layout.set_wrap(wrap)

    # ------------------------------------------------------------------
    # Properties with only getters
    # ------------------------------------------------------------------
    @property
    def baseline(self) -> int:
        """First-line baseline Y offset from layout top, in Pango units.

        Returns
        -------
        int
            Y offset of the first-line baseline from the layout top, in Pango units.
        """
        return self.pango_layout.get_baseline()

    @property
    def character_count(self) -> int:
        """Number of characters in the layout.

        Returns
        -------
        int
            Number of Unicode characters in the layout text.
        """
        return self.pango_layout.get_character_count()

    @property
    def line_count(self) -> int:
        """Number of lines in the layout.

        Returns
        -------
        int
            Number of lines in the layout.
        """
        return self.pango_layout.get_line_count()

    @property
    def pixel_size(self) -> tuple[int, int]:
        """Content size in device units (logical).

        Returns
        -------
        tuple[int, int]
            ``(width, height)`` in device units.
        """
        return self.pango_layout.get_pixel_size()

    @property
    def serial(self) -> int:
        """Serial number; incremented on each layout or context change.

        Returns
        -------
        int
            Current serial number.

        Notes
        -----
        Initialized to a small positive value; never ``0``. May wrap —
        always compare with ``!=``, never ``<``.
        """
        return self.pango_layout.get_serial()

    @property
    def size(self) -> tuple[int, int]:
        """Content size in Pango units (logical).

        Returns
        -------
        tuple[int, int]
            ``(width, height)`` in Pango units.
        """
        return self.pango_layout.get_size()

    @property
    def unknown_glyphs_count(self) -> int:
        """Number of unknown glyphs in the layout.

        Returns
        -------
        int
            Number of unknown glyphs in the layout.
        """
        return self.pango_layout.get_unknown_glyphs_count()

    @property
    def is_ellipsized(self) -> bool:
        """``True`` when any paragraphs were ellipsized.

        Returns
        -------
        bool
            ``True`` if the layout has been ellipsized.
        """
        return self.pango_layout.is_ellipsized()

    @property
    def is_wrapped(self) -> bool:
        """``True`` when any paragraphs were wrapped.

        Returns
        -------
        bool
            ``True`` if the layout has been wrapped.
        """
        return self.pango_layout.is_wrapped()

    # ------------------------------------------------------------------
    # Properties with getters and setters (have separated interface)
    # ------------------------------------------------------------------
    @property
    def font_description(self) -> Pango.FontDescription | None:
        """Font description applied to the layout.

        Returns
        -------
        Pango.FontDescription | None
            Current font description, or ``None`` if inherited from the context.
        """
        return self.pango_layout.get_font_description()

    @font_description.setter
    def font_description(self, desc: Pango.FontDescription | None) -> None:
        """Set the font description.

        Parameters
        ----------
        desc
            Font description to apply, or ``None`` to clear.
        """
        self.pango_layout.set_font_description(desc)

    @property
    def attributes(self) -> Pango.AttrList | None:
        """Attribute list applied to the layout.

        Returns
        -------
        Pango.AttrList | None
            Current attribute list, or ``None`` if not set.
        """
        return self.pango_layout.get_attributes()

    @attributes.setter
    def attributes(self, attrs: Pango.AttrList | None) -> None:
        """Set the text attributes.

        Parameters
        ----------
        attrs
            Attribute list to apply, or ``None`` to clear.
        """
        self.pango_layout.set_attributes(attrs)

    @property
    def tabs(self) -> Pango.TabArray | None:
        """Tab stops used by the layout.

        Returns
        -------
        Pango.TabArray | None
            Current tab stops, or ``None`` if not set.
        """
        return self.pango_layout.get_tabs()

    @tabs.setter
    def tabs(self, tabs: Pango.TabArray | None) -> None:
        """Set the tab stops.

        Parameters
        ----------
        tabs
            Tab array to apply, or ``None`` to clear.
        """
        self.pango_layout.set_tabs(tabs)

    # ------------------------------------------------------------------
    # Methods
    # ------------------------------------------------------------------
    def context_changed(self) -> None:
        """Force recomputation of layout state that depends on the context.

        Notes
        -----
        Call after modifying the layout's associated context.
        """
        self.pango_layout.context_changed()

    def copy(self) -> Pango.Layout:
        """Return a deep copy of the layout.

        Returns
        -------
        Pango.Layout
            Independent deep copy of the underlying layout.

        Notes
        -----
        The attribute list, tab array, and text are all copied by value.
        """
        return self.pango_layout.copy()

    def get_caret_pos(self, index_: int) -> tuple[Pango.Rectangle, Pango.Rectangle]:
        """Return strong and weak caret rectangles for the given byte index.

        Parameters
        ----------
        index_
            Byte index within the layout text.

        Returns
        -------
        tuple[Pango.Rectangle, Pango.Rectangle]
            ``(strong, weak)`` caret rectangles in Pango units.
        """
        return self.pango_layout.get_caret_pos(index_)

    def get_context(self) -> Pango.Context:
        """Return the context associated with the layout.

        Returns
        -------
        Pango.Context
            Pango context used by this layout.
        """
        return self.pango_layout.get_context()

    def get_cursor_pos(self, index_: int) -> tuple[Pango.Rectangle, Pango.Rectangle]:
        """Return strong and weak cursor rectangles for the given byte index.

        Parameters
        ----------
        index_
            Byte index within the layout text.

        Returns
        -------
        tuple[Pango.Rectangle, Pango.Rectangle]
            ``(strong, weak)`` cursor rectangles in Pango units.
        """
        return self.pango_layout.get_cursor_pos(index_)

    def get_direction(self, index: int) -> Pango.Direction:
        """Return the text direction at the given byte index.

        Parameters
        ----------
        index
            Byte index within the layout text.

        Returns
        -------
        Pango.Direction
            Text direction at ``index``.
        """
        return self.pango_layout.get_direction(index)

    def get_iter(self) -> Pango.LayoutIter:
        """Return an iterator for the visual lines of the layout.

        Returns
        -------
        Pango.LayoutIter
            Iterator positioned at the start of the layout.
        """
        return self.pango_layout.get_iter()

    def get_line(self, line: int) -> Pango.LayoutLine | None:
        """Return the line at the given index, or ``None`` if out of range.

        Parameters
        ----------
        line
            Zero-based line index.

        Returns
        -------
        Pango.LayoutLine | None
            Requested line, or ``None`` if out of range.
        """
        return self.pango_layout.get_line(line)

    def get_line_readonly(self, line: int) -> Pango.LayoutLine | None:
        """Return the line at the given index (read-only), or ``None`` if out of range.

        Parameters
        ----------
        line
            Zero-based line index.

        Returns
        -------
        Pango.LayoutLine | None
            Read-only line, or ``None`` if out of range.
        """
        return self.pango_layout.get_line_readonly(line)

    def get_lines(self) -> list[Pango.LayoutLine]:
        """Return all layout lines.

        Returns
        -------
        list[Pango.LayoutLine]
            All lines in visual order.
        """
        return self.pango_layout.get_lines()

    def get_lines_readonly(self) -> list[Pango.LayoutLine]:
        """Return all layout lines (read-only).

        Returns
        -------
        list[Pango.LayoutLine]
            All lines in visual order (read-only).
        """
        return self.pango_layout.get_lines_readonly()

    def get_log_attrs(self) -> list[Pango.LogAttr]:
        """Return logical attributes for each character in the layout text.

        Returns
        -------
        list[Pango.LogAttr]
            Logical attributes per character, including a trailing sentinel.
        """
        return self.pango_layout.get_log_attrs()

    def get_log_attrs_readonly(self) -> list[Pango.LogAttr]:
        """Return logical attributes for each character in the layout text (read-only).

        Returns
        -------
        list[Pango.LogAttr]
            Logical attributes per character, including a trailing sentinel (read-only).
        """
        return self.pango_layout.get_log_attrs_readonly()

    def index_to_line_x(self, *, index_: int, trailing: bool) -> tuple[int, int]:
        """Convert a byte index to line number and X coordinate.

        Parameters
        ----------
        index_
            Byte index within the layout text.
        trailing
            If ``True``, return the position after the character at ``index_``.

        Returns
        -------
        tuple[int, int]
            ``(line, x_pos)`` where ``line`` is the zero-based line index and
            ``x_pos`` is the X coordinate in Pango units.
        """
        return self.pango_layout.index_to_line_x(index_, trailing)

    def index_to_pos(self, index_: int) -> Pango.Rectangle:
        """Return the rectangle enclosing the character at the given byte index.

        Parameters
        ----------
        index_
            Byte index within the layout text.

        Returns
        -------
        Pango.Rectangle
            Bounding rectangle of the character in Pango units.
        """
        return self.pango_layout.index_to_pos(index_)

    def move_cursor_visually(
        self, *, strong: bool, old_index: int, old_trailing: int, direction: int
    ) -> tuple[int, int]:
        """Move the cursor one visual position in the given direction.

        Parameters
        ----------
        strong
            If ``True``, move the strong cursor; otherwise the weak cursor.
        old_index
            Current byte index within the layout text.
        old_trailing
            Current trailing value (0 or 1).
        direction
            Direction to move: positive for right, negative for left.

        Returns
        -------
        tuple[int, int]
            ``(new_index, new_trailing)`` after the move.
        """
        return self.pango_layout.move_cursor_visually(strong, old_index, old_trailing, direction)

    def serialize(self, flags: Pango.LayoutSerializeFlags) -> GLib.Bytes:
        """Serialize the layout to bytes using the given flags.

        Parameters
        ----------
        flags
            Flags controlling which parts of the layout are serialized.

        Returns
        -------
        GLib.Bytes
            Serialized layout data.
        """
        return self.pango_layout.serialize(flags)

    def write_to_file(self, flags: Pango.LayoutSerializeFlags, filename: str) -> bool:
        """Serialize the layout and write it to a file.

        Parameters
        ----------
        flags
            Flags controlling which parts of the layout are serialized.
        filename
            Destination file path.

        Returns
        -------
        bool
            ``True`` on success, ``False`` on failure.
        """
        return self.pango_layout.write_to_file(flags, filename)

    def xy_to_index(self, x: int, y: int) -> tuple[bool, int, int]:
        """Convert layout coordinates to a byte index and trailing value.

        Parameters
        ----------
        x
            X coordinate in Pango units.
        y
            Y coordinate in Pango units.

        Returns
        -------
        tuple[bool, int, int]
            ``(inside, index, trailing)`` — ``inside`` is ``True`` if the point
            is within the layout, ``index`` is the byte index, ``trailing`` is 0 or 1.
        """
        return self.pango_layout.xy_to_index(x, y)

    # ------------------------------------------------------------------
    # Extents
    # ------------------------------------------------------------------
    @property
    def extents(self) -> tuple[Pango.Rectangle, Pango.Rectangle]:
        """(ink, logical) extents in Pango units.

        Returns
        -------
        tuple[Pango.Rectangle, Pango.Rectangle]
            ``(ink, logical)`` extents in Pango units.
        """
        return self.pango_layout.get_extents()

    @property
    def extents_layout_rect(self) -> tuple[LayoutRect, LayoutRect]:
        """(ink, logical) extents in Pango units as ``LayoutRect``.

        Returns
        -------
        tuple[LayoutRect, LayoutRect]
            ``(ink, logical)`` extents in Pango units as ``LayoutRect``.
        """
        ink, logical = self.extents
        return (
            LayoutRect.from_pango_rectangle(rect=ink),
            LayoutRect.from_pango_rectangle(rect=logical),
        )

    @property
    def extents_ink_layout_rect(self) -> LayoutRect:
        """Ink extents in Pango units as ``LayoutRect``.

        Returns
        -------
        LayoutRect
            Ink extents in Pango units.
        """
        ink, _ = self.extents
        return LayoutRect.from_pango_rectangle(rect=ink)

    @property
    def extents_logical_layout_rect(self) -> LayoutRect:
        """Logical extents in Pango units as ``LayoutRect``.

        Returns
        -------
        LayoutRect
            Logical extents in Pango units.
        """
        _, logical = self.extents
        return LayoutRect.from_pango_rectangle(rect=logical)

    # ------------------------------------------------------------------
    # Width (Pango units + device units)
    # ------------------------------------------------------------------
    @property
    def width(self) -> int:
        """Layout width in Pango units.

        Returns
        -------
        int
            Width value with semantics:

            - ``-1`` (default): no width set; no wrapping or ellipsization.
            - ``> 0``: maximum width in Pango units; wrapping and ellipsization apply.
            - ``= 0``: follows ``Pango.WrapMode`` and ``Pango.EllipsizeMode`` rules — avoid.

        Notes
        -----
        Any negative value is normalized to ``-1`` by Pango.
        """
        return self.pango_layout.get_width()

    @width.setter
    def width(self, width: int) -> None:
        """Set the layout width in Pango units.

        Parameters
        ----------
        width
            Width in Pango units.
        """
        self.pango_layout.set_width(width)

    @property
    def width_device_units(self) -> WidthConstraint:
        """Layout width as a ``WidthConstraint`` in device units.

        Returns
        -------
        WidthConstraint
            ``WidthUnconstrained`` if width is ``-1``, otherwise ``WidthDeviceUnits``.

        Raises
        ------
        ValueError
            If width is ``0`` (special Pango mode) or a positive value is not provided in device unit mode.
        """
        width = self.width

        if width < 0:  # any negative value is converted to -1 by Pango
            return WidthUnconstrained()

        if width == 0:
            msg = "Width is in special mode (0), not device unit mode."
            raise ValueError(msg)

        return WidthDeviceUnits(width=Pango.units_to_double(width))

    @width_device_units.setter
    def width_device_units(self, width: float | WidthConstraint) -> None:
        """Set the layout width in device units.

        Parameters
        ----------
        width
            Width as a ``WidthConstraint`` or a positive float.

        Raises
        ------
        TypeError
            If ``width`` is not a ``WidthConstraint``, ``float``, or ``int``.
        ValueError
            If ``width`` is not positive in device unit mode.
        """
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
        """Layout height in Pango units.

        Only has effect when ``width > 0`` and ``ellipsize != PANGO_ELLIPSIZE_NONE``.

        Returns
        -------
        int
            Height value with semantics:

            - ``-1`` (default): 1 line per paragraph (first line of each paragraph is shown).
            - ``> 0``: maximum height in Pango units; at least one line per paragraph is always shown.
            - ``= 0``: exactly one line for the entire layout.
            - ``< 0``: maximum lines per paragraph (absolute value).
        """
        return self.pango_layout.get_height()

    @height.setter
    def height(self, height: int) -> None:
        """Set the layout height in Pango units.

        Parameters
        ----------
        height
            Height in Pango units.
        """
        self.pango_layout.set_height(height)

    @property
    def height_device_units(self) -> HeightConstraint:
        """Layout height as a ``HeightConstraint`` in device units.

        Returns
        -------
        HeightConstraint
            ``HeightDeviceUnits`` if height ``> 0``, ``HeightSingleLine`` if ``= 0``,
            or ``HeightLineLimit`` if ``< 0``.

        """
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
        """Set the layout height in device units.

        Parameters
        ----------
        height
            Height as a ``HeightConstraint`` or a float/int.

        Raises
        ------
        ValueError
            If ``HeightDeviceUnits.height`` or ``HeightLineLimit.lines`` is not positive.
        TypeError
            If ``height`` is not a ``HeightConstraint``, ``float``, or ``int``.
        """
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
        """Paragraph indent in Pango units. Default ``0``.

        Returns
        -------
        int
            - ``>= 0``: indent applied to the first line of each paragraph.
            - ``< 0``: hanging indent; first line is full-width, subsequent lines
              are indented by the absolute value.

        Notes
        -----
        Ignored when alignment is ``Pango.Alignment.CENTER``.
        """
        return self.pango_layout.get_indent()

    @indent.setter
    def indent(self, indent: int) -> None:
        """Set the paragraph indent in Pango units.

        Parameters
        ----------
        indent
            Indent in Pango units.
        """
        self.pango_layout.set_indent(indent)

    @property
    def indent_device_units(self) -> float:
        """Paragraph indent in device units.

        Returns
        -------
        float
            Paragraph indent in device units.
        """
        return Pango.units_to_double(self.indent)

    @indent_device_units.setter
    def indent_device_units(self, indent: float) -> None:
        """Set the paragraph indent in device units.

        Parameters
        ----------
        indent
            Indent in device units.
        """
        self.indent = Pango.units_from_double(indent)

    # ------------------------------------------------------------------
    # Pixel extents
    # ------------------------------------------------------------------
    @property
    def pixel_extents(self) -> tuple[Pango.Rectangle, Pango.Rectangle]:
        """(ink, logical) extents in device units.

        Returns
        -------
        tuple[Pango.Rectangle, Pango.Rectangle]
            ``(ink, logical)`` extents in device units.
        """
        return self.pango_layout.get_pixel_extents()

    @property
    def pixel_extents_layout_rect(self) -> tuple[LayoutRect, LayoutRect]:
        """(ink, logical) extents in device units as ``LayoutRect``.

        Returns
        -------
        tuple[LayoutRect, LayoutRect]
            ``(ink, logical)`` extents in device units as ``LayoutRect``.
        """
        ink, logical = self.pixel_extents
        return (
            LayoutRect.from_pango_rectangle(rect=ink),
            LayoutRect.from_pango_rectangle(rect=logical),
        )

    @property
    def pixel_extents_ink_layout_rect(self) -> LayoutRect:
        """Ink extents in device units as ``LayoutRect``.

        Returns
        -------
        LayoutRect
            Ink extents in device units.
        """
        ink, _ = self.pixel_extents
        return LayoutRect.from_pango_rectangle(rect=ink)

    @property
    def pixel_extents_logical_layout_rect(self) -> LayoutRect:
        """Logical extents in device units as ``LayoutRect``.

        Returns
        -------
        LayoutRect
            Logical extents in device units.
        """
        _, logical = self.pixel_extents
        return LayoutRect.from_pango_rectangle(rect=logical)

    # ------------------------------------------------------------------
    # Spacing (Pango units + device units)
    # ------------------------------------------------------------------
    @property
    def spacing(self) -> int:
        """Inter-line spacing in Pango units.

        Returns
        -------
        int
            Inter-line spacing in Pango units.
        """
        return self.pango_layout.get_spacing()

    @spacing.setter
    def spacing(self, spacing: int) -> None:
        """Set the inter-line spacing in Pango units.

        Parameters
        ----------
        spacing
            Spacing in Pango units.

        Notes
        -----
        Ignored when ``line_spacing`` is non-zero.
        """
        self.pango_layout.set_spacing(spacing)

    @property
    def spacing_device_units(self) -> float:
        """Inter-line spacing in device units.

        Returns
        -------
        float
            Inter-line spacing in device units.
        """
        return Pango.units_to_double(self.spacing)

    @spacing_device_units.setter
    def spacing_device_units(self, spacing: float) -> None:
        """Set the inter-line spacing in device units.

        Parameters
        ----------
        spacing
            Spacing in device units.
        """
        self.spacing = Pango.units_from_double(spacing)

    # ------------------------------------------------------------------
    # Layout fit report (logical fits, ink fits, clipped text)
    # ------------------------------------------------------------------
    def get_layout_fit_report(self, height_override: HeightConstraint | None = None) -> LayoutFitReport:  # noqa: C901  TODO: refactor to reduce complexity
        """Compute logical fits, ink fits, and clipped text in a single pass.

        Walks the layout line iterator once to determine the last visible line
        under the active height constraint, then derives all three results from
        that single traversal.

        Parameters
        ----------
        height_override
            Use this constraint instead of the layout's current height setting.
            ``None`` uses the layout's current ``height_device_units``.

        Returns
        -------
        LayoutFitReport
            Contains ``fits_logical``, ``fits_ink``, and ``clipped_text``.

        Raises
        ------
        TypeError
            If the width constraint type is not a ``WidthConstraint``.
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
