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

"""Surface factory."""

from __future__ import annotations

import io
import logging

import cairo

from tenderness.cairo_backend.surface_configuration import (
    ImageSurfaceConfig,
    PDFSurfaceConfig,
    SurfaceConfig,
    SurfaceType,
    SVGSurfaceConfig,
)
from tenderness.core.sentinel import _UNSET_PARAM
from tenderness.image_backend.surface_array_converter import (
    SurfaceArrayConverter,
)
from tenderness.image_backend.surface_writer import SurfaceWriter

logger = logging.getLogger(__name__)


class SurfaceCreator:
    """Creates cairo surfaces from surface configurations."""

    def __init__(self) -> None:
        self._surface_array_converter = SurfaceArrayConverter()
        self._surface_writer = SurfaceWriter()

    def create_surface(
        self,
        surface_config: SurfaceConfig,
    ) -> tuple[cairo.Surface, io.BytesIO | None]:
        """Create a cairo surface from a configuration.

        Parameters
        ----------
        surface_config
            Configuration defining the surface type and properties.

        Returns
        -------
        cairo.Surface
            The created surface.
        io.BytesIO | None
            ``None`` for image surfaces; a ``BytesIO`` holding the vector data
            for SVG and PDF surfaces.

        Raises
        ------
        ValueError
            If the surface type is not supported.
        """
        match surface_config:
            case ImageSurfaceConfig():
                return self._create_image_surface(surface_config=surface_config), None
            case SVGSurfaceConfig():
                stream = io.BytesIO()
                return self._create_svg_surface(surface_config=surface_config, stream=stream), stream
            case PDFSurfaceConfig():
                stream = io.BytesIO()
                return self._create_pdf_surface(surface_config=surface_config, stream=stream), stream
            case _ as unreachable:
                msg = f"Unhandled {SurfaceType.__name__} value: {unreachable!r}"
                raise ValueError(msg)

    def _create_image_surface(self, surface_config: ImageSurfaceConfig) -> cairo.ImageSurface:
        surface = cairo.ImageSurface(
            surface_config.pixel_format.format_value,
            surface_config.width,
            surface_config.height,
        )
        logger.debug("Created Cairo ImageSurface: %s", surface)
        return surface

    def _create_svg_surface(self, surface_config: SVGSurfaceConfig, stream: io.BytesIO) -> cairo.SVGSurface:
        surface = cairo.SVGSurface(stream, surface_config.width, surface_config.height)
        if surface_config.document_unit is not _UNSET_PARAM:
            surface.set_document_unit(surface_config.document_unit)  # type: ignore[arg-type] # guranteed by SVGSurfaceConfig post-init validation
        if surface_config.fallback_resolution is not _UNSET_PARAM:
            surface.set_fallback_resolution(*surface_config.fallback_resolution)
        if surface_config.svg_version is not _UNSET_PARAM:
            surface.restrict_to_version(surface_config.svg_version)  # type: ignore[arg-type] # guranteed by SVGSurfaceConfig post-init validation
        logger.debug("Created Cairo SVGSurface: %s", surface)
        return surface

    def _create_pdf_surface(self, surface_config: PDFSurfaceConfig, stream: io.BytesIO) -> cairo.PDFSurface:
        surface = cairo.PDFSurface(stream, surface_config.width, surface_config.height)
        if surface_config.fallback_resolution is not _UNSET_PARAM:
            surface.set_fallback_resolution(*surface_config.fallback_resolution)
        if surface_config.pdf_version is not _UNSET_PARAM:
            surface.restrict_to_version(surface_config.pdf_version)  # type: ignore[arg-type] # guranteed by PDFSurfaceConfig post-init validation
        logger.debug("Created Cairo PDFSurface: %s", surface)
        return surface
