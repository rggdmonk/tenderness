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

"""Cairo matrix transformation utilities."""

from __future__ import annotations

import math
from typing import Self

import cairo


class CairoMatrixTransformer:
    """Chainable cairo.Matrix transformer for use with cairo.Context.

    Notes
    -----
    https://pycairo.readthedocs.io/en/latest/reference/matrix.html
    https://www.cairographics.org/manual/cairo-cairo-matrix-t.html
    https://www.cairographics.org/cookbook/matrix_transform/
    """

    def __init__(self, matrix: cairo.Matrix) -> None:
        """Initialize the transformer.

        Parameters
        ----------
        matrix
            Initial transformation matrix.
        """
        self.matrix = matrix

    @classmethod
    def from_new(cls) -> CairoMatrixTransformer:
        """Construct a transformer with an identity matrix.

        Returns
        -------
        CairoMatrixTransformer
            Transformer initialized with an identity matrix.
        """
        return cls(matrix=cairo.Matrix())

    def apply_matrix_to_cairo_context(self, cairo_context: cairo.Context[cairo.Surface]) -> None:
        """Apply the current matrix to a cairo context.

        Parameters
        ----------
        cairo_context
            Cairo context to update.
        """
        cairo_context.set_matrix(self.matrix)

    def _append(self, other: cairo.Matrix) -> None:
        """Append a matrix, preserving transformation order.

        Parameters
        ----------
        other
            Matrix to append.
        """
        self.matrix = self.matrix.multiply(other)

    def get_components(self) -> tuple[float, float, float, float, float, float]:
        """Return the six matrix components as a flat tuple.

        Returns
        -------
        float
            ``xx`` component.
        float
            ``yx`` component.
        float
            ``xy`` component.
        float
            ``yy`` component.
        float
            ``x0`` component.
        float
            ``y0`` component.
        """
        m = self.matrix
        return (m.xx, m.yx, m.xy, m.yy, m.x0, m.y0)

    def transform_distance(self, dx: float, dy: float) -> tuple[float, float]:
        """Transform a distance vector by the current matrix.

        Parameters
        ----------
        dx
            Horizontal distance component.
        dy
            Vertical distance component.

        Returns
        -------
        float
            Transformed horizontal distance component.
        float
            Transformed vertical distance component.
        """
        return self.matrix.transform_distance(dx, dy)

    def transform_point(self, x: float, y: float) -> tuple[float, float]:
        """Transform a point by the current matrix.

        Parameters
        ----------
        x
            Horizontal coordinate.
        y
            Vertical coordinate.

        Returns
        -------
        float
            Transformed horizontal coordinate.
        float
            Transformed vertical coordinate.
        """
        return self.matrix.transform_point(x, y)

    def invert(self) -> Self:
        """Invert the matrix in place.

        Returns
        -------
        Self
            The transformer instance for chaining.
        """
        self.matrix.invert()
        return self

    def multiply(self, other: cairo.Matrix) -> Self:
        """Multiply the current matrix by another.

        Parameters
        ----------
        other
            Matrix to multiply by.

        Returns
        -------
        Self
            The transformer instance for chaining.
        """
        self.matrix = self.matrix.multiply(other)
        return self

    # ------------------------------------------------------------------
    # Methods (transformations)
    # ------------------------------------------------------------------
    def translate(self, tx: float, ty: float) -> Self:
        """Translate the matrix by (tx, ty).

        Parameters
        ----------
        tx
            Horizontal translation.
        ty
            Vertical translation.

        Returns
        -------
        Self
            The transformer instance for chaining.

        Notes
        -----
        Equivalent to ``ctx.translate(tx, ty)``.
        Matrix form: ``[1, 0, 0, 1, tx, ty]``
        """
        self.matrix.translate(tx, ty)
        return self

    def scale(self, sx: float, sy: float) -> Self:
        """Scale the matrix by (sx, sy).

        Parameters
        ----------
        sx
            Horizontal scale factor.
        sy
            Vertical scale factor.

        Returns
        -------
        Self
            The transformer instance for chaining.

        Notes
        -----
        Equivalent to ``ctx.scale(sx, sy)``.
        Matrix form: ``[sx, 0, 0, sy, 0, 0]``
        """
        self.matrix.scale(sx, sy)
        return self

    def rotate(self, angle: float, *, degrees: bool = True) -> Self:
        """Rotate the matrix around the current origin.

        Parameters
        ----------
        angle
            Rotation angle.
        degrees
            Interpret ``angle`` as degrees when ``True``, radians otherwise.

        Returns
        -------
        Self
            The transformer instance for chaining.

        Notes
        -----
        Equivalent to ``ctx.rotate(angle_radians)``.
        Matrix form: ``[cos(A), sin(A), -sin(A), cos(A), 0, 0]``
        """
        angle_rad = math.radians(angle) if degrees else angle
        self.matrix.rotate(angle_rad)
        return self

    def rotate_around_point(self, angle: float, cx: float, cy: float, *, degrees: bool = True) -> Self:
        """Rotate the matrix around a specific center point.

        Parameters
        ----------
        angle
            Rotation angle.
        cx
            Horizontal coordinate of the rotation center.
        cy
            Vertical coordinate of the rotation center.
        degrees
            Interpret ``angle`` as degrees when ``True``, radians otherwise.

        Returns
        -------
        Self
            The transformer instance for chaining.

        Notes
        -----
        Matrix form: ``[C, S, -S, C, cx - C*cx + S*cy, cy - S*cx - C*cy]``
        where ``C = cos(angle)``, ``S = sin(angle)``
        """
        angle_rad = math.radians(angle) if degrees else angle
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)

        rotation_matrix = cairo.Matrix(
            xx=cos_a,
            yx=sin_a,
            xy=-sin_a,
            yy=cos_a,
            x0=cx - cos_a * cx + sin_a * cy,
            y0=cy - sin_a * cx - cos_a * cy,
        )
        self._append(other=rotation_matrix)
        return self

    def skew_x(self, angle: float, *, degrees: bool = True) -> Self:
        """Skew the matrix along the x-axis.

        Parameters
        ----------
        angle
            Shear angle.
        degrees
            Interpret ``angle`` as degrees when ``True``, radians otherwise.

        Returns
        -------
        Self
            The transformer instance for chaining.

        Notes
        -----
        Matrix form: ``[1, 0, tan(A), 1, 0, 0]``
        """
        angle_rad = math.radians(angle) if degrees else angle
        shear_factor = math.tan(angle_rad)
        skew_matrix = cairo.Matrix(xx=1, yx=0, xy=shear_factor, yy=1, x0=0, y0=0)

        self._append(other=skew_matrix)
        return self

    def skew_y(self, angle: float, *, degrees: bool = True) -> Self:
        """Skew the matrix along the y-axis.

        Parameters
        ----------
        angle
            Shear angle.
        degrees
            Interpret ``angle`` as degrees when ``True``, radians otherwise.

        Returns
        -------
        Self
            The transformer instance for chaining.

        Notes
        -----
        Matrix form: ``[1, tan(A), 0, 1, 0, 0]``
        """
        angle_rad = math.radians(angle) if degrees else angle
        shear_factor = math.tan(angle_rad)
        skew_matrix = cairo.Matrix(xx=1, yx=shear_factor, xy=0, yy=1, x0=0, y0=0)

        self._append(other=skew_matrix)
        return self

    def flip_horizontal(self, cx: float = 0.0) -> Self:
        """Flip the matrix horizontally around a vertical axis at cx.

        Parameters
        ----------
        cx
            x-coordinate of the flip axis; defaults to the origin.

        Returns
        -------
        Self
            The transformer instance for chaining.

        Notes
        -----
        Equivalent to scaling by ``(-1, 1)`` around the center point.
        Matrix form: ``[-1, 0, 0, 1, 2*cx, 0]``
        """
        flip_matrix = cairo.Matrix(xx=-1, yx=0, xy=0, yy=1, x0=2 * cx, y0=0)

        self._append(other=flip_matrix)
        return self

    def flip_vertical(self, cy: float = 0.0) -> Self:
        """Flip the matrix vertically around a horizontal axis at cy.

        Parameters
        ----------
        cy
            y-coordinate of the flip axis; defaults to the origin.

        Returns
        -------
        Self
            The transformer instance for chaining.

        Notes
        -----
        Equivalent to scaling by ``(1, -1)`` around the center point.
        Matrix form: ``[1, 0, 0, -1, 0, 2*cy]``
        """
        flip_matrix = cairo.Matrix(xx=1, yx=0, xy=0, yy=-1, x0=0, y0=2 * cy)

        self._append(other=flip_matrix)
        return self
