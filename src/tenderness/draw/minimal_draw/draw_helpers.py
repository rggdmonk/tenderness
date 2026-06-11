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

"""Stroke style definitions and low-level drawing helpers for cairo contexts."""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from enum import StrEnum, auto, unique
from typing import TYPE_CHECKING

import cairo

if TYPE_CHECKING:
    from tenderness.core.geometry import Rectangle


@unique
class DashStyle(StrEnum):
    """Dash pattern for stroked lines.

    Attributes
    ----------
    SOLID
        Continuous unbroken line.
    DASHED
        Alternating long dashes and gaps.
    DOTTED
        Closely spaced round dots.
    DASH_DOT
        Alternating dash and dot pattern.
    """

    SOLID = auto()
    DASHED = auto()
    DOTTED = auto()
    DASH_DOT = auto()


@dataclass(frozen=True, slots=True)
class StrokeStyle:
    """Stroke style parameters for a path.

    Attributes
    ----------
    line_width
        Width of the stroke in device units.
    line_cap
        Line cap style; uses the context default when ``None``.
    line_join
        Line join style; uses the context default when ``None``.
    dash_style
        Dash pattern style for the stroke.
    """

    line_width: float = 1.0
    line_cap: cairo.LineCap | None = None
    line_join: cairo.LineJoin | None = None
    dash_style: DashStyle = field(default=DashStyle.SOLID)


DEFAULT_STROKE = StrokeStyle()


class MinimalDrawHelpers:
    """Low-level cairo drawing helper methods."""

    @staticmethod
    def rounded_rect_path(cairo_context: cairo.Context[cairo.Surface], rect: Rectangle, radius: float) -> None:
        """Trace a rounded rectangle path without stroking or filling.

        Parameters
        ----------
        cairo_context
            Cairo context to trace on.
        rect
            Bounding rectangle.
        radius
            Corner radius; clamped to half the shorter dimension.
        """
        x, y = rect.x_min, rect.y_min
        w, h = rect.normalized_size
        r = min(radius, w / 2, h / 2)
        cairo_context.new_sub_path()
        cairo_context.arc(x + w - r, y + r, r, -math.pi / 2, 0)
        cairo_context.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
        cairo_context.arc(x + r, y + h - r, r, math.pi / 2, math.pi)
        cairo_context.arc(x + r, y + r, r, math.pi, -math.pi / 2)
        cairo_context.close_path()

    @staticmethod
    def apply_stroke_style(cairo_context: cairo.Context[cairo.Surface], stroke: StrokeStyle) -> None:
        """Apply stroke style settings to cairo_context.

        Parameters
        ----------
        cairo_context
            Cairo context to configure.
        stroke
            Stroke style to apply.
        """
        cairo_context.set_line_width(stroke.line_width)
        if stroke.line_cap is not None:
            cairo_context.set_line_cap(stroke.line_cap)
        if stroke.line_join is not None:
            cairo_context.set_line_join(stroke.line_join)
        match stroke.dash_style:
            case DashStyle.SOLID:
                cairo_context.set_dash([])
            case DashStyle.DASHED:
                cairo_context.set_dash([stroke.line_width * 4, stroke.line_width * 2])
            case DashStyle.DOTTED:
                cairo_context.set_line_cap(cairo.LineCap.ROUND)
                cairo_context.set_dash([0, stroke.line_width * 2.5])
            case DashStyle.DASH_DOT:
                cairo_context.set_line_cap(cairo.LineCap.ROUND)
                cairo_context.set_dash([stroke.line_width * 4, stroke.line_width * 2, 0, stroke.line_width * 2])
