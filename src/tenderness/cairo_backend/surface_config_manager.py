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

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from tenderness.cairo_backend.pixel_formats import PixelFormat
from tenderness.cairo_backend.surface_configuration import ImageSurfaceConfig, PDFSurfaceConfig, SVGSurfaceConfig
from tenderness.core.color_models import ColorModel
from tenderness.core.image_formats import ImageFormat
from tenderness.core.sentinel import _UNSET_PARAM, Settable
from tenderness.image_backend.image_backends import ImageBackend

if TYPE_CHECKING:
    import cairo

    from tenderness.cairo_backend.cairo_enum_coerce import PDFVersionStr, SVGUnitStr, SVGVersionStr

logger = logging.getLogger(__name__)


class SurfaceConfigManager:
    """Factory for creating validated surface configuration instances."""

    def create_image_surface_config(
        self,
        *,
        width: int,
        height: int,
        color_model: ColorModel = ColorModel.RGB,
        image_format: ImageFormat = ImageFormat.PNG,
        image_backend: ImageBackend = ImageBackend.CAIRO,
        pixel_format: PixelFormat = PixelFormat.RGB24,
    ) -> ImageSurfaceConfig:
        """Create a validated ImageSurfaceConfig.

        Parameters
        ----------
        width
            Surface width in pixels.
        height
            Surface height in pixels.
        color_model
            Color model for pixel data.
        image_format
            Output image format.
        image_backend
            Backend for image export.
        pixel_format
            Pixel format for the cairo image surface.

        Raises
        ------
        TypeError
            If ``pixel_format`` is not a PixelFormat instance.
        ValueError
            If the configuration is invalid.
        """
        if not isinstance(pixel_format, PixelFormat):
            msg = f"pixel_format must be an instance of {PixelFormat.__name__}, got {type(pixel_format).__name__}."
            raise TypeError(msg)
        img_cfg = ImageSurfaceConfig(
            width=width,
            height=height,
            color_model=color_model,
            image_format=image_format,
            image_backend=image_backend,
            pixel_format=pixel_format,
        )
        logger.debug("Created %s: %s", ImageSurfaceConfig.__name__, img_cfg)
        return img_cfg

    def create_svg_surface_config(
        self,
        *,
        width: float,
        height: float,
        color_model: ColorModel = ColorModel.RGB,
        image_format: ImageFormat = ImageFormat.SVG,
        image_backend: ImageBackend = ImageBackend.CAIRO,
        document_unit: Settable[cairo.SVGUnit | SVGUnitStr] = _UNSET_PARAM,
        svg_version: Settable[cairo.SVGVersion | SVGVersionStr] = _UNSET_PARAM,
        fallback_resolution: Settable[tuple[float, float]] = _UNSET_PARAM,
    ) -> SVGSurfaceConfig:
        """Create a validated SVGSurfaceConfig.

        Parameters
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
            Backend for image export.
        document_unit
            SVG document unit for coordinates.
        svg_version
            SVG specification version.
        fallback_resolution
            Optional (x, y) resolution for rasterized fallback content.

        Raises
        ------
        ValueError
            If the configuration is invalid.
        """
        svg_cfg = SVGSurfaceConfig(
            width=width,
            height=height,
            color_model=color_model,
            image_format=image_format,
            image_backend=image_backend,
            fallback_resolution=fallback_resolution,
            document_unit=document_unit,
            svg_version=svg_version,
        )
        logger.debug("Created %s: %s", SVGSurfaceConfig.__name__, svg_cfg)
        return svg_cfg

    def create_pdf_surface_config(
        self,
        *,
        width: float,
        height: float,
        color_model: ColorModel = ColorModel.RGB,
        image_format: ImageFormat = ImageFormat.PDF,
        image_backend: ImageBackend = ImageBackend.CAIRO,
        fallback_resolution: Settable[tuple[float, float]] = _UNSET_PARAM,
        pdf_version: Settable[cairo.PDFVersion | PDFVersionStr] = _UNSET_PARAM,
    ) -> PDFSurfaceConfig:
        """Create a validated PDFSurfaceConfig.

        Parameters
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
            Backend for image export.
        fallback_resolution
            Optional (x, y) resolution for rasterized fallback content.
        pdf_version
            PDF specification version.

        Raises
        ------
        ValueError
            If the configuration is invalid.
        """
        pdf_cfg = PDFSurfaceConfig(
            width=width,
            height=height,
            color_model=color_model,
            image_format=image_format,
            image_backend=image_backend,
            fallback_resolution=fallback_resolution,
            pdf_version=pdf_version,
        )
        logger.debug("Created %s: %s", PDFSurfaceConfig.__name__, pdf_cfg)
        return pdf_cfg
