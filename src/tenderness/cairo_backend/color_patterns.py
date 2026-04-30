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

"""Color pattern specs and cairo pattern factory."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

import cairo

from tenderness.core.color_models import ColorModel
from tenderness.core.sentinel import _UNSET_PARAM, Settable

if TYPE_CHECKING:
    from tenderness.colors.color_selector import Color


@dataclass(frozen=True, slots=True)
class ColorStop:
    """A color at a specific offset along a gradient.

    Parameters
    ----------
    offset
        Position along the gradient, from 0.0 to 1.0.
    color
        Color at this stop.
    """

    offset: float
    color: Color


@dataclass(frozen=True, slots=True)
class SolidColorSpec:
    """Specification for a solid color fill."""

    color: Color


@dataclass(frozen=True, slots=True)
class LinearGradientColorSpec:
    """Specification for a linear gradient fill.

    Parameters
    ----------
    x0
        x-coordinate of the gradient start point.
    y0
        y-coordinate of the gradient start point.
    x1
        x-coordinate of the gradient end point.
    y1
        y-coordinate of the gradient end point.
    stops
        Color stops defining the gradient.
    """

    x0: float
    y0: float
    x1: float
    y1: float
    stops: tuple[ColorStop, ...]


@dataclass(frozen=True, slots=True)
class RadialGradientColorSpec:
    """Specification for a radial gradient fill.

    Parameters
    ----------
    cx0
        x-coordinate of the inner circle center.
    cy0
        y-coordinate of the inner circle center.
    radius0
        Radius of the inner circle.
    cx1
        x-coordinate of the outer circle center.
    cy1
        y-coordinate of the outer circle center.
    radius1
        Radius of the outer circle.
    stops
        Color stops defining the gradient.
    """

    cx0: float
    cy0: float
    radius0: float
    cx1: float
    cy1: float
    radius1: float
    stops: tuple[ColorStop, ...]


@dataclass(frozen=True, slots=True)
class SurfacePatternSpec:
    """Specification for a surface-based fill pattern.

    Parameters
    ----------
    surface
        Cairo surface to use as the pattern source.
    extend
        How the pattern is extended beyond its bounds.
    filter
        Filtering algorithm used when scaling the pattern.
    matrix
        Transformation matrix applied to the pattern.
    """

    surface: cairo.Surface
    extend: Settable[cairo.Extend] = _UNSET_PARAM
    filter: Settable[cairo.Filter] = _UNSET_PARAM
    matrix: Settable[cairo.Matrix] = _UNSET_PARAM


@dataclass(frozen=True, slots=True)
class ImagePatternSpec:
    """Specification for a PNG image fill pattern.

    Parameters
    ----------
    path
        Path or file-like object for the PNG image.
    extend
        How the pattern is extended beyond its bounds.
    filter
        Filtering algorithm used when scaling the pattern.
    matrix
        Transformation matrix applied to the pattern.
    """

    path: cairo._PathLike | cairo._FileLike
    extend: Settable[cairo.Extend] = _UNSET_PARAM
    filter: Settable[cairo.Filter] = _UNSET_PARAM
    matrix: Settable[cairo.Matrix] = _UNSET_PARAM


type PatternColorSpec = (
    SolidColorSpec | LinearGradientColorSpec | RadialGradientColorSpec | SurfacePatternSpec | ImagePatternSpec
)


class ColorPattern:
    """Factory for creating cairo patterns from pattern specifications."""

    @staticmethod
    def create_color_pattern(
        pattern_color_spec: PatternColorSpec,
        color_model: ColorModel,
    ) -> cairo.Pattern:
        """Create a cairo pattern from a pattern specification.

        Parameters
        ----------
        pattern_color_spec
            Specification describing the pattern type and parameters.
        color_model
            Color model used when constructing color patterns.

        Raises
        ------
        TypeError
            If ``pattern_color_spec`` is an unsupported type.
        """
        if isinstance(pattern_color_spec, SolidColorSpec):
            return ColorPattern.solid(pattern_color_spec, color_model)
        if isinstance(pattern_color_spec, LinearGradientColorSpec):
            return ColorPattern.linear_gradient(pattern_color_spec, color_model)
        if isinstance(pattern_color_spec, RadialGradientColorSpec):
            return ColorPattern.radial_gradient(pattern_color_spec, color_model)
        if isinstance(pattern_color_spec, SurfacePatternSpec):
            return ColorPattern.surface_pattern(pattern_color_spec)
        if isinstance(pattern_color_spec, ImagePatternSpec):
            return ColorPattern.image_pattern(pattern_color_spec)
        msg = f"Unsupported pattern type: {type(pattern_color_spec)}"
        raise TypeError(msg)

    @staticmethod
    def solid(pattern_color_spec: SolidColorSpec, color_model: ColorModel) -> cairo.SolidPattern:
        """Create a solid cairo pattern from a SolidColorSpec.

        Parameters
        ----------
        pattern_color_spec
            Solid color specification.
        color_model
            Determines whether RGB or RGBA values are used.

        Raises
        ------
        ValueError
            If ``color_model`` is not RGB or RGBA.
        """
        if color_model == ColorModel.RGB:
            return cairo.SolidPattern(*pattern_color_spec.color.rgb)
        if color_model == ColorModel.RGBA:
            return cairo.SolidPattern(*pattern_color_spec.color.rgba)
        msg = f"Unsupported {color_model=}"
        raise ValueError(msg)

    @staticmethod
    def linear_gradient(pattern_color_spec: LinearGradientColorSpec, color_model: ColorModel) -> cairo.LinearGradient:
        """Create a linear gradient cairo pattern.

        Parameters
        ----------
        pattern_color_spec
            Linear gradient specification including endpoints and stops.
        color_model
            Determines whether RGB or RGBA stop colors are used.

        Raises
        ------
        ValueError
            If ``color_model`` is not RGB or RGBA.
        """
        gradient = cairo.LinearGradient(
            pattern_color_spec.x0, pattern_color_spec.y0, pattern_color_spec.x1, pattern_color_spec.y1
        )
        for stop in pattern_color_spec.stops:
            if color_model == ColorModel.RGB:
                gradient.add_color_stop_rgb(stop.offset, *stop.color.rgb)
            elif color_model == ColorModel.RGBA:
                gradient.add_color_stop_rgba(stop.offset, *stop.color.rgba)
            else:
                msg = f"Unsupported {color_model=}"
                raise ValueError(msg)
        return gradient

    @staticmethod
    def radial_gradient(
        pattern_color_spec: RadialGradientColorSpec,
        color_model: ColorModel = ColorModel.RGBA,
    ) -> cairo.RadialGradient:
        """Create a radial gradient cairo pattern.

        Parameters
        ----------
        pattern_color_spec
            Radial gradient specification including circles and stops.
        color_model
            Determines whether RGB or RGBA stop colors are used.

        Raises
        ------
        ValueError
            If ``color_model`` is not RGB or RGBA.
        """
        gradient = cairo.RadialGradient(
            pattern_color_spec.cx0,
            pattern_color_spec.cy0,
            pattern_color_spec.radius0,
            pattern_color_spec.cx1,
            pattern_color_spec.cy1,
            pattern_color_spec.radius1,
        )
        for stop in pattern_color_spec.stops:
            if color_model == ColorModel.RGB:
                gradient.add_color_stop_rgb(stop.offset, *stop.color.rgb)
            elif color_model == ColorModel.RGBA:
                gradient.add_color_stop_rgba(stop.offset, *stop.color.rgba)
            else:
                msg = f"Unsupported {color_model=}"
                raise ValueError(msg)

        return gradient

    @staticmethod
    def surface_pattern(spec: SurfacePatternSpec) -> cairo.SurfacePattern:
        """Create a surface cairo pattern from a SurfacePatternSpec."""
        pattern = cairo.SurfacePattern(spec.surface)
        if spec.extend is not _UNSET_PARAM:
            pattern.set_extend(spec.extend)
        if spec.filter is not _UNSET_PARAM:
            pattern.set_filter(spec.filter)
        if spec.matrix is not _UNSET_PARAM:
            pattern.set_matrix(spec.matrix)
        return pattern

    @staticmethod
    def image_pattern(spec: ImagePatternSpec) -> cairo.SurfacePattern:
        """Create a surface cairo pattern from a PNG image file."""
        surface = cairo.ImageSurface.create_from_png(spec.path)
        return ColorPattern.surface_pattern(
            SurfacePatternSpec(
                surface=surface,
                extend=spec.extend,
                filter=spec.filter,
                matrix=spec.matrix,
            )
        )
