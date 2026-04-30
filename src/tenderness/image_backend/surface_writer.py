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

"""Cairo surface serialization to image, SVG, and PDF files."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import TYPE_CHECKING, assert_never

import cairo

from tenderness.cairo_backend.surface_configuration import (
    ImageSurfaceConfig,
    PDFSurfaceConfig,
    SurfaceConfig,
    SVGSurfaceConfig,
)
from tenderness.image_backend.image_backends import ImageBackend

if TYPE_CHECKING:
    import io
    import pathlib

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class SurfaceWriterParameters:
    """Parameters controlling the output path and surface lifecycle."""

    output_file_path: pathlib.Path
    finish_after: bool = True


class SurfaceWriter:
    """Writes Cairo surfaces to disk in the appropriate format."""

    def save_as_file(
        self,
        surface: cairo.Surface,
        surface_config: SurfaceConfig,
        surface_writer_params: SurfaceWriterParameters,
        stream: io.BytesIO | None = None,
    ) -> pathlib.Path:
        """Save a Cairo surface to disk.

        Parameters
        ----------
        stream
            Required for SVG and PDF surfaces; unused for image surfaces.

        Returns
        -------
        pathlib.Path
            Actual output path; the suffix is replaced to match the format.

        Raises
        ------
        ValueError
            If ``stream`` is ``None`` for an SVG or PDF surface.
        TypeError
            If the surface/config combination is not supported.
        """
        match (surface, surface_config):
            case (cairo.ImageSurface(), ImageSurfaceConfig()):
                path = self._save_image(
                    surface=surface,
                    surface_config=surface_config,
                    output_file_path=surface_writer_params.output_file_path,
                )

                if surface_writer_params.finish_after:
                    surface.finish()
                return path

            case (cairo.SVGSurface(), SVGSurfaceConfig()):
                if stream is None:
                    msg = f"`{stream=}` must be provided when saving {cairo.SVGSurface.__name__}."
                    raise ValueError(msg)

                path = self._save_svg(
                    surface=surface,
                    stream=stream,
                    surface_config=surface_config,
                    output_file_path=surface_writer_params.output_file_path,
                )

                if surface_writer_params.finish_after:
                    stream.close()  # surface.finish() always called inside
                return path

            case (cairo.PDFSurface(), PDFSurfaceConfig()):
                if stream is None:
                    msg = f"`{stream=}` must be provided when saving {cairo.PDFSurface.__name__}."
                    raise ValueError(msg)

                path = self._save_pdf(
                    surface=surface,
                    stream=stream,
                    surface_config=surface_config,
                    output_file_path=surface_writer_params.output_file_path,
                )

                if surface_writer_params.finish_after:
                    stream.close()  # surface.finish() always called inside
                return path

            case _:
                msg = f"Unsupported surface/config combination: {type(surface)!r}, {type(surface_config)!r}"
                raise TypeError(msg)

    # --------------------------
    # Image
    # --------------------------
    def _save_image(
        self, surface: cairo.ImageSurface, surface_config: ImageSurfaceConfig, output_file_path: pathlib.Path
    ) -> pathlib.Path:
        match surface_config.image_backend:
            case ImageBackend.CAIRO:
                return self._save_image_via_cairo(
                    surface=surface, surface_config=surface_config, output_file_path=output_file_path
                )
            case ImageBackend.PIL:
                msg = f"Saving {cairo.ImageSurface.__name__} with {ImageBackend.PIL.backend_name} backend is not implemented yet."
                raise NotImplementedError(msg)
            case ImageBackend.CV2:
                msg = f"Saving {cairo.ImageSurface.__name__} with {ImageBackend.CV2.backend_name} backend is not implemented yet."
                raise NotImplementedError(msg)
            case _ as unreachable:
                assert_never(unreachable)

    def _save_image_via_cairo(
        self,
        surface: cairo.ImageSurface,
        surface_config: ImageSurfaceConfig,
        output_file_path: pathlib.Path,
    ) -> pathlib.Path:
        output_file_path = output_file_path.with_suffix(surface_config.image_format.extension)
        surface.write_to_png(str(output_file_path))
        logger.debug(
            "%s saved via %s backend to %s",
            cairo.ImageSurface.__name__,
            ImageBackend.CAIRO.backend_name,
            output_file_path,
        )
        return output_file_path

    # --------------------------
    # SVG
    # --------------------------
    def _save_svg(
        self,
        surface: cairo.SVGSurface,
        stream: io.BytesIO,
        surface_config: SVGSurfaceConfig,
        output_file_path: pathlib.Path,
    ) -> pathlib.Path:
        match surface_config.image_backend:
            case ImageBackend.CAIRO:
                return self._save_svg_via_cairo(
                    surface=surface, stream=stream, surface_config=surface_config, output_file_path=output_file_path
                )
            case ImageBackend.PIL:
                msg = f"Saving {cairo.SVGSurface.__name__} with {ImageBackend.PIL.backend_name} backend is not implemented yet."
                raise NotImplementedError(msg)
            case ImageBackend.CV2:
                msg = f"Saving {cairo.SVGSurface.__name__} with {ImageBackend.CV2.backend_name} backend is not implemented yet."
                raise NotImplementedError(msg)
            case _ as unreachable:
                assert_never(unreachable)

    def _save_svg_via_cairo(
        self,
        surface: cairo.SVGSurface,
        stream: io.BytesIO,
        surface_config: SVGSurfaceConfig,
        output_file_path: pathlib.Path,
    ) -> pathlib.Path:
        output_file_path = output_file_path.with_suffix(surface_config.image_format.extension)
        surface.finish()  # always required to flush SVG content to stream
        output_file_path.write_bytes(stream.getvalue())
        logger.debug(
            "%s saved via %s backend to %s",
            cairo.SVGSurface.__name__,
            ImageBackend.CAIRO.backend_name,
            output_file_path,
        )
        return output_file_path

    # --------------------------
    # PDF
    # --------------------------
    def _save_pdf(
        self,
        surface: cairo.PDFSurface,
        stream: io.BytesIO,
        surface_config: PDFSurfaceConfig,
        output_file_path: pathlib.Path,
    ) -> pathlib.Path:
        match surface_config.image_backend:
            case ImageBackend.CAIRO:
                return self._save_pdf_via_cairo(
                    surface=surface, stream=stream, surface_config=surface_config, output_file_path=output_file_path
                )
            case ImageBackend.PIL:
                msg = f"Saving {cairo.PDFSurface.__name__} with {ImageBackend.PIL.backend_name} backend is not implemented yet."
                raise NotImplementedError(msg)
            case ImageBackend.CV2:
                msg = f"Saving {cairo.PDFSurface.__name__} with {ImageBackend.CV2.backend_name} backend is not implemented yet."
                raise NotImplementedError(msg)
            case _ as unreachable:
                assert_never(unreachable)

    def _save_pdf_via_cairo(
        self,
        surface: cairo.PDFSurface,
        stream: io.BytesIO,
        surface_config: PDFSurfaceConfig,
        output_file_path: pathlib.Path,
    ) -> pathlib.Path:
        output_file_path = output_file_path.with_suffix(surface_config.image_format.extension)
        surface.finish()  # always required to flush PDF content to stream
        output_file_path.write_bytes(stream.getvalue())
        logger.debug(
            "%s saved via %s backend to %s",
            cairo.PDFSurface.__name__,
            ImageBackend.CAIRO.backend_name,
            output_file_path,
        )
        return output_file_path
