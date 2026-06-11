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

"""Stroke-based border drawing."""

from __future__ import annotations

import math
from typing import TYPE_CHECKING

from tenderness.cairo_backend.color_patterns import ColorPattern, PatternColorSpec
from tenderness.draw.minimal_draw.draw_helpers import DEFAULT_STROKE, MinimalDrawHelpers, StrokeStyle

if TYPE_CHECKING:
    import cairo

    from tenderness.core.color_models import ColorModel
    from tenderness.core.geometry import Rectangle


class DrawBorders:
    """Stroke-based border drawing for geometric shapes."""

    def rect(
        self,
        cairo_context: cairo.Context[cairo.Surface],
        rect: Rectangle,
        color_spec: PatternColorSpec,
        color_model: ColorModel,
        stroke: StrokeStyle = DEFAULT_STROKE,
    ) -> None:
        """Stroke a rectangle border.

        Parameters
        ----------
        cairo_context
            Cairo context to draw on.
        rect
            Rectangle to stroke.
        color_spec
            Color pattern specification for the stroke.
        color_model
            Color model used when constructing the pattern.
        stroke
            Stroke style to apply.
        """
        w, h = rect.normalized_size
        pattern = ColorPattern.create_color_pattern(color_spec, color_model)
        cairo_context.save()
        cairo_context.set_source(pattern)
        MinimalDrawHelpers.apply_stroke_style(cairo_context=cairo_context, stroke=stroke)
        cairo_context.rectangle(rect.x_min, rect.y_min, w, h)
        cairo_context.stroke()
        cairo_context.restore()

    def rounded_rect(
        self,
        cairo_context: cairo.Context[cairo.Surface],
        rect: Rectangle,
        color_spec: PatternColorSpec,
        color_model: ColorModel,
        radius: float,
        stroke: StrokeStyle = DEFAULT_STROKE,
    ) -> None:
        """Stroke a rounded rectangle border.

        Parameters
        ----------
        cairo_context
            Cairo context to draw on.
        rect
            Rectangle to stroke.
        color_spec
            Color pattern specification for the stroke.
        color_model
            Color model used when constructing the pattern.
        radius
            Corner radius in device units.
        stroke
            Stroke style to apply.
        """
        pattern = ColorPattern.create_color_pattern(color_spec, color_model)
        cairo_context.save()
        cairo_context.set_source(pattern)
        MinimalDrawHelpers.apply_stroke_style(cairo_context=cairo_context, stroke=stroke)
        MinimalDrawHelpers.rounded_rect_path(cairo_context=cairo_context, rect=rect, radius=radius)
        cairo_context.stroke()
        cairo_context.restore()

    def circle(
        self,
        cairo_context: cairo.Context[cairo.Surface],
        cx: float,
        cy: float,
        radius: float,
        color_spec: PatternColorSpec,
        color_model: ColorModel,
        stroke: StrokeStyle = DEFAULT_STROKE,
    ) -> None:
        """Stroke a circle border.

        Parameters
        ----------
        cairo_context
            Cairo context to draw on.
        cx
            X coordinate of the center.
        cy
            Y coordinate of the center.
        radius
            Radius of the circle.
        color_spec
            Color pattern specification for the stroke.
        color_model
            Color model used when constructing the pattern.
        stroke
            Stroke style to apply.
        """
        pattern = ColorPattern.create_color_pattern(color_spec, color_model)
        cairo_context.save()
        cairo_context.set_source(pattern)
        MinimalDrawHelpers.apply_stroke_style(cairo_context=cairo_context, stroke=stroke)
        cairo_context.new_sub_path()
        cairo_context.arc(cx, cy, radius, 0, 2 * math.pi)
        cairo_context.stroke()
        cairo_context.restore()
