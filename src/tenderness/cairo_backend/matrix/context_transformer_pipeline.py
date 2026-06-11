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

"""Cairo context transformation pipeline."""

from __future__ import annotations

from typing import Any, ClassVar, Self

import cairo

from tenderness.cairo_backend.matrix.matrix_transformer import CairoMatrixTransformer
from tenderness.cairo_backend.matrix.matrix_transforms import (
    FlipHorizontalParameters,
    FlipVerticalParameters,
    MatrixTransformType,
    RotateAroundPointParameters,
    RotateParameters,
    ScaleParameters,
    SkewXParameters,
    SkewYParameters,
    TranslateParameters,
)

type TransformDictParameter = dict[str, Any]

type TransformDataclassParameter = (
    TranslateParameters
    | ScaleParameters
    | RotateParameters
    | SkewXParameters
    | SkewYParameters
    | RotateAroundPointParameters
    | FlipHorizontalParameters
    | FlipVerticalParameters
)

type TransformParameter = TransformDictParameter | TransformDataclassParameter


class CairoContextTransformPipeline:
    """Fluent pipeline for applying sequential matrix transformations to a cairo.Context."""

    _SUPPORTED_TRANSFORMS: ClassVar[dict[MatrixTransformType, type]] = {
        MatrixTransformType.TRANSLATE: TranslateParameters,
        MatrixTransformType.SCALE: ScaleParameters,
        MatrixTransformType.ROTATE: RotateParameters,
        MatrixTransformType.SKEW_X: SkewXParameters,
        MatrixTransformType.SKEW_Y: SkewYParameters,
        MatrixTransformType.ROTATE_AROUND_POINT: RotateAroundPointParameters,
        MatrixTransformType.FLIP_HORIZONTAL: FlipHorizontalParameters,
        MatrixTransformType.FLIP_VERTICAL: FlipVerticalParameters,
    }

    _SUPPORTED_TRANSFORMS_TYPES: ClassVar[tuple[MatrixTransformType, ...]] = tuple(_SUPPORTED_TRANSFORMS.keys())
    _SUPPORTED_TRANSFORMS_PARAMETERS_TYPES: ClassVar[tuple[type, ...]] = tuple(_SUPPORTED_TRANSFORMS.values())

    def __init__(self, matrix: cairo.Matrix, name: str = "") -> None:
        """Initialize the pipeline.

        Parameters
        ----------
        matrix
            Initial transformation matrix.
        name
            Optional label for the pipeline instance.
        """
        self.cairo_matrix_transformer = CairoMatrixTransformer(matrix=matrix)
        self.name = name

    @classmethod
    def from_new(cls, name: str = "") -> Self:
        """Construct a pipeline with an identity matrix.

        Parameters
        ----------
        name
            Optional label for the pipeline instance.

        Returns
        -------
        Self
            Pipeline initialized with an identity matrix.
        """
        return cls(matrix=cairo.Matrix(), name=name)

    @classmethod
    def from_cairo_context(cls, cairo_context: cairo.Context[cairo.Surface], name: str = "") -> Self:
        """Construct a pipeline initialized from the current matrix of a cairo context.

        Parameters
        ----------
        cairo_context
            Context whose current matrix is used as the starting state.
        name
            Optional label for the pipeline instance.

        Returns
        -------
        Self
            Pipeline initialized from the context's current matrix.
        """
        return cls(matrix=cairo_context.get_matrix(), name=name)

    def apply_to_cairo_context(self, cairo_context: cairo.Context[cairo.Surface]) -> None:
        """Apply the accumulated matrix to a cairo context.

        Parameters
        ----------
        cairo_context
            Cairo context to update.
        """
        cairo_context.set_matrix(self.cairo_matrix_transformer.matrix)

    @property
    def matrix(self) -> cairo.Matrix:
        """Current transformation matrix."""
        return self.cairo_matrix_transformer.matrix

    def reset(self) -> Self:
        """Reset the matrix to identity.

        Returns
        -------
        Self
            The pipeline instance for chaining.
        """
        self.cairo_matrix_transformer.matrix = cairo.Matrix()
        return self

    @property
    def supported_transforms_types(self) -> tuple[MatrixTransformType, ...]:
        """Supported transform types."""
        return self._SUPPORTED_TRANSFORMS_TYPES

    # ----------------------------------------------------------------
    # Fluent API
    # ----------------------------------------------------------------
    def translate(self, tx: float, ty: float) -> Self:
        """Translate the pipeline matrix by (tx, ty).

        Parameters
        ----------
        tx
            Horizontal translation.
        ty
            Vertical translation.

        Returns
        -------
        Self
            The pipeline instance for chaining.
        """
        self.cairo_matrix_transformer.translate(tx=tx, ty=ty)
        return self

    def scale(self, sx: float, sy: float) -> Self:
        """Scale the pipeline matrix by (sx, sy).

        Parameters
        ----------
        sx
            Horizontal scale factor.
        sy
            Vertical scale factor.

        Returns
        -------
        Self
            The pipeline instance for chaining.
        """
        self.cairo_matrix_transformer.scale(sx=sx, sy=sy)
        return self

    def rotate(self, angle: float, *, degrees: bool = True) -> Self:
        """Rotate the pipeline matrix around the current origin.

        Parameters
        ----------
        angle
            Rotation angle.
        degrees
            Interpret ``angle`` as degrees when ``True``, radians otherwise.

        Returns
        -------
        Self
            The pipeline instance for chaining.
        """
        self.cairo_matrix_transformer.rotate(angle=angle, degrees=degrees)
        return self

    def skew_x(self, angle: float, *, degrees: bool = True) -> Self:
        """Skew the pipeline matrix along the x-axis.

        Parameters
        ----------
        angle
            Shear angle.
        degrees
            Interpret ``angle`` as degrees when ``True``, radians otherwise.

        Returns
        -------
        Self
            The pipeline instance for chaining.
        """
        self.cairo_matrix_transformer.skew_x(angle=angle, degrees=degrees)
        return self

    def skew_y(self, angle: float, *, degrees: bool = True) -> Self:
        """Skew the pipeline matrix along the y-axis.

        Parameters
        ----------
        angle
            Shear angle.
        degrees
            Interpret ``angle`` as degrees when ``True``, radians otherwise.

        Returns
        -------
        Self
            The pipeline instance for chaining.
        """
        self.cairo_matrix_transformer.skew_y(angle=angle, degrees=degrees)
        return self

    def rotate_around_point(self, angle: float, cx: float, cy: float, *, degrees: bool = True) -> Self:
        """Rotate the pipeline matrix around a specific center point.

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
            The pipeline instance for chaining.
        """
        self.cairo_matrix_transformer.rotate_around_point(angle=angle, cx=cx, cy=cy, degrees=degrees)
        return self

    def flip_horizontal(self, cx: float = 0.0) -> Self:
        """Flip the pipeline matrix horizontally around a vertical axis at cx.

        Parameters
        ----------
        cx
            x-coordinate of the flip axis; defaults to the origin.

        Returns
        -------
        Self
            The pipeline instance for chaining.
        """
        self.cairo_matrix_transformer.flip_horizontal(cx=cx)
        return self

    def flip_vertical(self, cy: float = 0.0) -> Self:
        """Flip the pipeline matrix vertically around a horizontal axis at cy.

        Parameters
        ----------
        cy
            y-coordinate of the flip axis; defaults to the origin.

        Returns
        -------
        Self
            The pipeline instance for chaining.
        """
        self.cairo_matrix_transformer.flip_vertical(cy=cy)
        return self

    # ----------------------------------------------------------------
    # Dataclass API
    # ----------------------------------------------------------------
    def _update_from_dataclass(self, transform_dataclass: TransformDataclassParameter) -> None:
        transform_dataclass.apply_to(self.cairo_matrix_transformer)

    def _update_from_dataclasses(self, transform_dataclasses: list[TransformDataclassParameter]) -> None:
        for transform_dataclass in transform_dataclasses:
            self._update_from_dataclass(transform_dataclass)

    # ----------------------------------------------------------------
    # Dict API
    # ----------------------------------------------------------------
    def _update_from_dict(self, transform_dict: TransformDictParameter) -> None:
        transform_type = transform_dict["type"]
        kwargs = {k: v for k, v in transform_dict.items() if k != "type"}
        getattr(self, transform_type)(**kwargs)

    def _update_from_dicts(self, transform_dicts: list[TransformDictParameter]) -> None:
        for transform_dict in transform_dicts:
            self._update_from_dict(transform_dict)

    # ----------------------------------------------------------------
    # Unified API
    # ----------------------------------------------------------------
    def update_with_parameter(self, transform: TransformDataclassParameter | TransformDictParameter) -> None:
        """Apply a single transformation to the pipeline.

        Parameters
        ----------
        transform
            Transform to apply; accepted as a dataclass or a dict with a ``"type"`` key.
        """
        if isinstance(transform, dict):
            self._update_from_dict(transform)
        else:
            self._update_from_dataclass(transform)

    def update_with_parameters(self, transforms: list[TransformDataclassParameter | TransformDictParameter]) -> None:
        """Apply a sequence of transformations to the pipeline.

        Parameters
        ----------
        transforms
            Transformations to apply in order.
        """
        for transform in transforms:
            self.update_with_parameter(transform)
