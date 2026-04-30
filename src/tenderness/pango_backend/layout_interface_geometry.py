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

"""Defines data structures for LayoutInterface."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum, auto, unique
from typing import Self

import gi

from tenderness.core.geometry import Rectangle

gi.require_version("Pango", "1.0")

from gi.repository import Pango  # noqa: E402, TC002


@unique
class ExtentsMode(StrEnum):  # noqa: D101 TODO: docstring
    INK = auto()
    LOGICAL = auto()


class LayoutRect(Rectangle):  # noqa: D101 TODO: docstring
    @classmethod
    def from_pango_rectangle(cls, rect: Pango.Rectangle) -> Self:  # noqa: D102 TODO: docstring
        if rect.width < 0 or rect.height < 0:
            msg = f"Invalid Pango rectangle dimensions: width={rect.width}, height={rect.height}"
            raise ValueError(msg)
        return cls(x=rect.x, y=rect.y, width=rect.width, height=rect.height)


# ------------------------------------------------------------------
# Width device units in LayoutInterface
# ------------------------------------------------------------------
@dataclass(frozen=True, slots=True)
class WidthDeviceUnits:
    """Width expressed as device units. Maps to Pango width > 0."""

    width: float


@dataclass(frozen=True, slots=True)
class WidthUnconstrained:
    """Unconstrained width (single line). Maps to Pango width = -1."""


# ------------------------------------------------------------------
# Height device units in LayoutInterface
# ------------------------------------------------------------------
@dataclass(frozen=True, slots=True)
class HeightLineLimit:
    """
    Max lines per paragraph. Maps to Pango height `< 0`.

    Attributes
    ----------
        lines: Number of lines; stored as positive, Pango receives negated.
            Default Pango value of `-1` maps to `lines=1`.
    """

    lines: int


@dataclass(frozen=True, slots=True)
class HeightSingleLine:
    """Exactly one line regardless of content. Maps to Pango height `= 0`."""


@dataclass(frozen=True, slots=True)
class HeightDeviceUnits:
    """
    Max height in device units. Maps to Pango height `> 0`.

    Attributes
    ----------
        height: Height in device units; always positive.
    """

    height: float


type WidthConstraint = WidthDeviceUnits | WidthUnconstrained
type HeightConstraint = HeightDeviceUnits | HeightLineLimit | HeightSingleLine


@dataclass(frozen=True, slots=True)
class FitsResult:  # noqa: D101 TODO: docstring
    extents_mode: ExtentsMode
    width: bool
    height: bool
    ellipsis: Pango.EllipsizeMode
    wrap: Pango.WrapMode
    rect: LayoutRect
    width_device_units: WidthConstraint
    height_device_units: HeightConstraint
    unknown_glyphs_count: int

    @property
    def fit_both(self) -> bool:  # noqa: D102 TODO: docstring
        return self.width and self.height


@dataclass(frozen=True, slots=True)
class ClippedText:
    """
    Text that was not rendered due to layout constraints.

    Attributes
    ----------
        visible: The portion of text that was rendered.
        clipped: The portion of text that was clipped or ellipsized.
        last_visible_line: Index of the last rendered line (zero-based).
        clipped_char_index: Byte index into the full text where clipping began.
    """

    visible: str
    clipped: str
    last_visible_line: int
    clipped_char_byte_index: int

    @property
    def has_clipped(self) -> bool:
        """True if any text was not rendered."""
        return bool(self.clipped)


@dataclass(frozen=True, slots=True)
class LayoutFitReport:
    """
    Combined fitting and clipping result from a single iterator pass.

    Attributes
    ----------
        fits_logical: Fitting result based on logical extents.
        fits_ink: Fitting result based on ink extents.
        clipped_text: Visible and clipped text portions.
    """

    fits_logical: FitsResult
    fits_ink: FitsResult
    clipped_text: ClippedText
