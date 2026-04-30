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

"""Matrix transformation types, protocol, and parameter dataclasses."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import StrEnum, auto, unique
from typing import Protocol, Self, runtime_checkable


@unique
class MatrixTransformType(StrEnum):
    """Named matrix transformation operations."""

    # Basic transformations
    TRANSLATE = auto()
    SCALE = auto()
    ROTATE = auto()

    # Skew transformations
    SKEW_X = auto()
    SKEW_Y = auto()

    # Complex transformations
    ROTATE_AROUND_POINT = auto()
    FLIP_HORIZONTAL = auto()
    FLIP_VERTICAL = auto()


@runtime_checkable
class MatrixTransformerProtocol(Protocol):
    """Protocol for objects that apply matrix transformations."""

    def translate(self, tx: float, ty: float) -> Self:
        """Translate by (tx, ty)."""
        ...

    def scale(self, sx: float, sy: float) -> Self:
        """Scale by (sx, sy)."""
        ...

    def rotate(self, angle: float, *, degrees: bool = True) -> Self:
        """Rotate by angle.

        Parameters
        ----------
        angle
            Rotation angle.
        degrees
            Interpret angle as degrees when True, radians when False.
        """
        ...

    def skew_x(self, angle: float, *, degrees: bool = True) -> Self:
        """Skew along the x-axis by angle.

        Parameters
        ----------
        angle
            Skew angle.
        degrees
            Interpret angle as degrees when True, radians when False.
        """
        ...

    def skew_y(self, angle: float, *, degrees: bool = True) -> Self:
        """Skew along the y-axis by angle.

        Parameters
        ----------
        angle
            Skew angle.
        degrees
            Interpret angle as degrees when True, radians when False.
        """
        ...

    def rotate_around_point(self, angle: float, cx: float, cy: float, *, degrees: bool = True) -> Self:
        """Rotate by angle around the point (cx, cy).

        Parameters
        ----------
        angle
            Rotation angle.
        cx
            X coordinate of the pivot point.
        cy
            Y coordinate of the pivot point.
        degrees
            Interpret angle as degrees when True, radians when False.
        """
        ...

    def flip_horizontal(self, cx: float) -> Self:
        """Flip horizontally around the vertical axis at x = cx."""
        ...

    def flip_vertical(self, cy: float) -> Self:
        """Flip vertically around the horizontal axis at y = cy."""
        ...


@dataclass(slots=True)
class TransformDataclassParameter(ABC):
    """Abstract base for dataclass-style transformation parameter holders."""

    @abstractmethod
    def apply_to(self, transformer: MatrixTransformerProtocol) -> None:
        """Apply this transformation to transformer."""
        ...


# ------------------------------------------------------------------
# Basic transformation parameter classes
# ------------------------------------------------------------------
@dataclass(slots=True)
class TranslateParameters(TransformDataclassParameter):
    """Parameters for a translate transformation.

    Parameters
    ----------
    tx
        Translation along the x-axis.
    ty
        Translation along the y-axis.
    """

    tx: float = 0.0
    ty: float = 0.0

    def apply_to(self, transformer: MatrixTransformerProtocol) -> None:
        """Apply translation to transformer."""
        transformer.translate(tx=self.tx, ty=self.ty)


@dataclass(slots=True)
class ScaleParameters(TransformDataclassParameter):
    """Parameters for a scale transformation.

    Parameters
    ----------
    sx
        Scale factor along the x-axis.
    sy
        Scale factor along the y-axis.
    """

    sx: float = 1.0
    sy: float = 1.0

    def apply_to(self, transformer: MatrixTransformerProtocol) -> None:
        """Apply scaling to transformer."""
        transformer.scale(sx=self.sx, sy=self.sy)


@dataclass(slots=True)
class RotateParameters(TransformDataclassParameter):
    """Parameters for a rotate transformation.

    Parameters
    ----------
    angle
        Rotation angle.
    degrees
        Interpret angle as degrees when True, radians when False.
    """

    angle: float = 0.0
    degrees: bool = True

    def apply_to(self, transformer: MatrixTransformerProtocol) -> None:
        """Apply rotation to transformer."""
        transformer.rotate(angle=self.angle, degrees=self.degrees)


# ------------------------------------------------------------------
# Skew transformation parameter classes
# ------------------------------------------------------------------
@dataclass(slots=True)
class SkewXParameters(TransformDataclassParameter):
    """Parameters for a skew-x transformation.

    Parameters
    ----------
    angle
        Skew angle.
    degrees
        Interpret angle as degrees when True, radians when False.
    """

    angle: float = 0.0
    degrees: bool = True

    def apply_to(self, transformer: MatrixTransformerProtocol) -> None:
        """Apply x-axis skew to transformer."""
        transformer.skew_x(angle=self.angle, degrees=self.degrees)


@dataclass(slots=True)
class SkewYParameters(TransformDataclassParameter):
    """Parameters for a skew-y transformation.

    Parameters
    ----------
    angle
        Skew angle.
    degrees
        Interpret angle as degrees when True, radians when False.
    """

    angle: float = 0.0
    degrees: bool = True

    def apply_to(self, transformer: MatrixTransformerProtocol) -> None:
        """Apply y-axis skew to transformer."""
        transformer.skew_y(angle=self.angle, degrees=self.degrees)


# ------------------------------------------------------------------
# Complex transformation parameter classes
# ------------------------------------------------------------------
@dataclass(slots=True)
class RotateAroundPointParameters(TransformDataclassParameter):
    """Parameters for a rotate-around-point transformation.

    Parameters
    ----------
    angle
        Rotation angle.
    cx
        X coordinate of the pivot point.
    cy
        Y coordinate of the pivot point.
    degrees
        Interpret angle as degrees when True, radians when False.
    """

    angle: float = 0.0
    cx: float = 0.0
    cy: float = 0.0
    degrees: bool = True

    def apply_to(self, transformer: MatrixTransformerProtocol) -> None:
        """Apply rotation around point to transformer."""
        transformer.rotate_around_point(angle=self.angle, cx=self.cx, cy=self.cy, degrees=self.degrees)


@dataclass(slots=True)
class FlipHorizontalParameters(TransformDataclassParameter):
    """Parameters for a horizontal flip transformation.

    Parameters
    ----------
    cx
        X coordinate of the flip axis.
    """

    cx: float = 0.0

    def apply_to(self, transformer: MatrixTransformerProtocol) -> None:
        """Apply horizontal flip to transformer."""
        transformer.flip_horizontal(cx=self.cx)


@dataclass(slots=True)
class FlipVerticalParameters(TransformDataclassParameter):
    """Parameters for a vertical flip transformation.

    Parameters
    ----------
    cy
        Y coordinate of the flip axis.
    """

    cy: float = 0.0

    def apply_to(self, transformer: MatrixTransformerProtocol) -> None:
        """Apply vertical flip to transformer."""
        transformer.flip_vertical(cy=self.cy)
