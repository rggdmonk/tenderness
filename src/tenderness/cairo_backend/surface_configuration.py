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

"""Surface configuration dataclasses."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import StrEnum, auto, unique
from functools import cached_property
from typing import TYPE_CHECKING, Self

from tenderness.cairo_backend.cairo_enum_coerce import (
    CairoEnumCoerce,
    CairoEnumMap,
    PDFVersionStr,
    SVGUnitStr,
    SVGVersionStr,
)
from tenderness.cairo_backend.pixel_formats import PixelFormat
from tenderness.core.color_models import ColorModel
from tenderness.core.geometry import Rectangle
from tenderness.core.image_formats import ImageFormat
from tenderness.core.sentinel import _UNSET_PARAM, Settable

if TYPE_CHECKING:
    import cairo

    from tenderness.image_backend.image_backends import ImageBackend


@unique
class SurfaceType(StrEnum):
    """Supported cairo surface output types.

    Attributes
    ----------
    IMAGE
        Raster image surface.
    SVG
        SVG vector surface.
    PDF
        PDF vector surface.
    """

    IMAGE = auto()
    SVG = auto()
    PDF = auto()


class SurfaceRect(Rectangle):
    """Rectangle anchored at the origin matching a surface's dimensions."""

    @classmethod
    def from_surface_config(cls, config: SurfaceConfig) -> Self:
        """Construct a SurfaceRect from a surface configuration.

        Parameters
        ----------
        config
            Configuration whose dimensions define the rectangle.

        Returns
        -------
        Self
            Rectangle with origin at ``(0, 0)`` and the surface dimensions.

        Raises
        ------
        ValueError
            If either dimension is not positive.
        """
        if config.width <= 0 or config.height <= 0:
            msg = f"Invalid surface dimensions for SurfaceRect: width={config.width}, height={config.height}"
            raise ValueError(msg)
        return cls(x=0, y=0, width=config.width, height=config.height)


@dataclass(frozen=True)
class SurfaceConfig(ABC):
    """Abstract base configuration for a cairo rendering surface.

    Attributes
    ----------
    width
        Surface width.
    height
        Surface height.
    color_model
        Color model for pixel data.
    image_format
        Output image format.
    image_backend
        Backend used for image export.
    """

    width: float
    height: float

    color_model: ColorModel
    image_format: ImageFormat
    image_backend: ImageBackend

    def __post_init__(self) -> None:
        """Validate dimensions, backend support, and alpha compatibility."""
        self._validate_dimensions()
        self._validate_backend_support()
        self._validate_alpha_compatibility()

    # --------------------------
    # Abstract properties
    # --------------------------
    @property
    @abstractmethod
    def surface_type(self) -> SurfaceType:
        """Return the type of the surface."""
        ...

    # --------------------------
    # Properties
    # --------------------------
    @cached_property
    def rect(self) -> SurfaceRect:
        """Return a SurfaceRect representing the surface bounds, anchored at the origin.

        Returns
        -------
        SurfaceRect
            Rectangle with origin at ``(0, 0)`` and the surface dimensions.
        """
        return SurfaceRect.from_surface_config(self)

    # --------------------------
    # Methods
    # --------------------------
    def _validate_dimensions(self) -> None:
        """Validate the surface dimensions are positive.

        Raises
        ------
        ValueError
            If either dimension is not positive.
        """
        if self.width <= 0 or self.height <= 0:
            msg = f"Invalid surface dimensions: {self.width=}, {self.height=}. Both must be positive."
            raise ValueError(msg)

    def _validate_backend_support(self) -> None:
        """Validate that the chosen image backend supports the specified image format.

        Raises
        ------
        ValueError
            If the backend does not support the image format.
        """
        if not self.image_backend.is_image_format_supported(image_format=self.image_format):
            msg = (
                f"{type(self.image_backend).__name__} '{self.image_backend.name}' "
                f"(via '{self.image_backend.backend_name}') does not support "
                f"{ImageFormat.__name__} '{self.image_format.name}'."
            )
            raise ValueError(msg)

    def _validate_alpha_compatibility(self) -> None:
        """Validate that the image format can handle the alpha channel if requested.

        Raises
        ------
        ValueError
            If the color model requires alpha but the image format does not support it.
        """
        if self.color_model.has_alpha and not self.image_format.supports_alpha:
            msg = (
                f"{ColorModel.__name__} {self.color_model} requires alpha support, "
                f"but {ImageFormat.__name__} {self.image_format.name} does not support it."
            )
            raise ValueError(msg)


@dataclass(frozen=True)
class RasterSurfaceConfig(SurfaceConfig, ABC):
    """Abstract base configuration for raster (pixel-based) surfaces.

    Attributes
    ----------
    width
        Surface width in pixels.
    height
        Surface height in pixels.
    """

    width: int
    height: int

    def __post_init__(self) -> None:
        """Validate that the format is raster."""
        super().__post_init__()
        self._validate_raster_requirement()

    def _validate_raster_requirement(self) -> None:
        """Ensure the image format is raster, not vector.

        Raises
        ------
        ValueError
            If the image format is vector-based.
        """
        if self.image_format.is_vector:
            msg = f"{type(self).__name__} requires a raster format, but got {self.image_format.name}."
            raise ValueError(msg)


@dataclass(frozen=True)
class VectorSurfaceConfig(SurfaceConfig, ABC):
    """Abstract base configuration for vector output surfaces.

    Attributes
    ----------
    fallback_resolution
        Optional ``(x, y)`` resolution for rasterized fallback content.
    """

    fallback_resolution: Settable[tuple[float, float]] = _UNSET_PARAM

    def __post_init__(self) -> None:
        """Normalize and validate fallback resolution and vector requirements."""
        if self.fallback_resolution is not _UNSET_PARAM:
            object.__setattr__(self, "fallback_resolution", tuple(self.fallback_resolution))

        super().__post_init__()
        self._validate_vector_requirements()
        self._validate_fallback_resolution()

    def _validate_fallback_resolution(self) -> None:
        """Validate fallback resolution values are positive if provided.

        Raises
        ------
        ValueError
            If either resolution value is not positive.
        """
        if self.fallback_resolution is not _UNSET_PARAM:
            x, y = self.fallback_resolution
            if x <= 0 or y <= 0:
                msg = f"fallback_resolution values must be positive, got {self.fallback_resolution}."
                raise ValueError(msg)

    def _validate_vector_requirements(self) -> None:
        """Ensure the configuration is appropriate for vector output.

        Raises
        ------
        ValueError
            If the image format is not vector-based or the backend lacks vector support.
        """
        if not self.image_format.is_vector:
            msg = f"{type(self).__name__} requires a vector format, but got {self.image_format.name}."
            raise ValueError(msg)

        if not self.image_backend.has_vector_support():
            msg = f"{type(self.image_backend).__name__} {self.image_backend.backend_name} does not support vector exports."
            raise ValueError(msg)


@dataclass(frozen=True)
class ImageSurfaceConfig(RasterSurfaceConfig):
    """Configuration for a raster image surface.

    Attributes
    ----------
    pixel_format
        Pixel format for the image surface.
    """

    pixel_format: PixelFormat

    def __post_init__(self) -> None:
        """Validate the pixel format against the color model."""
        super().__post_init__()
        self._validate_pixel_format()

    # --------------------------
    # Properties
    # --------------------------
    @property
    def surface_type(self) -> SurfaceType:
        """Surface type identifier."""
        return SurfaceType.IMAGE

    # --------------------------
    # Methods
    # --------------------------
    def _validate_pixel_format(self) -> None:
        """Ensure the pixel format is compatible with the logical color model.

        Raises
        ------
        ValueError
            If the pixel format's color model does not match the configured color model.
        """
        if self.pixel_format.color_model != self.color_model:
            msg = (
                f"Incompatible {PixelFormat.__name__}: {self.pixel_format.name} uses {self.pixel_format.color_model}, "
                f"but config requires {self.color_model}."
            )
            raise ValueError(msg)


@dataclass(frozen=True)
class SVGSurfaceConfig(VectorSurfaceConfig):
    """Configuration for an SVG vector surface.

    Attributes
    ----------
    document_unit
        SVG document unit for coordinates.
    svg_version
        SVG specification version.
    """

    document_unit: Settable[cairo.SVGUnit | SVGUnitStr] = _UNSET_PARAM
    svg_version: Settable[cairo.SVGVersion | SVGVersionStr] = _UNSET_PARAM

    def __post_init__(self) -> None:
        """Coerce string enum fields and validate SVG requirements."""
        if self.document_unit is not _UNSET_PARAM:
            object.__setattr__(self, "document_unit", CairoEnumCoerce.coerce(CairoEnumMap.SVGUnit, self.document_unit))
        if self.svg_version is not _UNSET_PARAM:
            object.__setattr__(self, "svg_version", CairoEnumCoerce.coerce(CairoEnumMap.SVGVersion, self.svg_version))

        super().__post_init__()

    # --------------------------
    # Properties
    # --------------------------
    @property
    def surface_type(self) -> SurfaceType:
        """Surface type identifier."""
        return SurfaceType.SVG


@dataclass(frozen=True)
class PDFSurfaceConfig(VectorSurfaceConfig):
    """Configuration for a PDF vector surface.

    Attributes
    ----------
    pdf_version
        PDF specification version.
    """

    pdf_version: Settable[cairo.PDFVersion | PDFVersionStr] = _UNSET_PARAM

    def __post_init__(self) -> None:
        """Coerce string enum field and validate PDF requirements."""
        if self.pdf_version is not _UNSET_PARAM:
            object.__setattr__(self, "pdf_version", CairoEnumCoerce.coerce(CairoEnumMap.PDFVersion, self.pdf_version))

        super().__post_init__()

    # --------------------------
    # Properties
    # --------------------------
    @property
    def surface_type(self) -> SurfaceType:
        """Surface type identifier."""
        return SurfaceType.PDF
