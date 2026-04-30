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

import io
from collections.abc import Callable

import cairo
import gi
import pytest

from tenderness.cairo_backend.pixel_formats import PixelFormat
from tenderness.cairo_backend.surface_configuration import (
    ImageSurfaceConfig,
    PDFSurfaceConfig,
    SVGSurfaceConfig,
)
from tenderness.cairo_backend.surface_creator import SurfaceCreator
from tenderness.core.color_models import ColorModel
from tenderness.core.image_formats import ImageFormat
from tenderness.image_backend.image_backends import ImageBackend
from tenderness.pango_backend.layout_interface import LayoutInterface

gi.require_version("Pango", "1.0")
gi.require_version("PangoCairo", "1.0")


from gi.repository import Pango, PangoCairo  # noqa: E402


# --------------------------
# Fixtures For LayoutInterface
# --------------------------
@pytest.fixture(
    params=[
        pytest.param("native_image", id="native_image"),
        pytest.param("native_svg", id="native_svg"),
        pytest.param("native_pdf", id="native_pdf"),
        pytest.param("pipeline_image", id="pipeline_image"),
        pytest.param("pipeline_svg", id="pipeline_svg"),
        pytest.param("pipeline_pdf", id="pipeline_pdf"),
    ]
)
def cairo_surface(request: pytest.FixtureRequest) -> tuple[cairo.Surface, io.BytesIO | None]:

    surface_creator = SurfaceCreator()

    width = 128
    height = 256

    match request.param:
        case "native_image":
            return cairo.ImageSurface(cairo.Format.RGB24, width, height), None

        case "native_svg":
            stream: io.BytesIO | None = io.BytesIO()
            return cairo.SVGSurface(stream, width, height), stream

        case "native_pdf":
            stream = io.BytesIO()
            return cairo.PDFSurface(stream, width, height), stream

        case "pipeline_image":
            image_cfg = ImageSurfaceConfig(
                width=width,
                height=height,
                color_model=ColorModel.RGB,
                image_format=ImageFormat.PNG,
                image_backend=ImageBackend.CAIRO,
                pixel_format=PixelFormat.RGB24,
            )
            surface, stream = surface_creator.create_surface(surface_config=image_cfg)
            assert isinstance(surface, cairo.ImageSurface)
            assert stream is None
            return surface, stream

        case "pipeline_svg":
            svg_cfg = SVGSurfaceConfig(
                width=width,
                height=height,
                color_model=ColorModel.RGB,
                image_format=ImageFormat.SVG,
                image_backend=ImageBackend.CAIRO,
            )
            surface, stream = surface_creator.create_surface(surface_config=svg_cfg)
            assert isinstance(surface, cairo.SVGSurface)
            assert isinstance(stream, io.BytesIO)
            return surface, stream

        case "pipeline_pdf":
            pdf_cfg = PDFSurfaceConfig(
                width=width,
                height=height,
                color_model=ColorModel.RGB,
                image_format=ImageFormat.PDF,
                image_backend=ImageBackend.CAIRO,
            )
            surface, stream = surface_creator.create_surface(surface_config=pdf_cfg)
            assert isinstance(surface, cairo.PDFSurface)
            assert isinstance(stream, io.BytesIO)
            return surface, stream

        case _:
            msg = f"Unrecognized fixture parameter: {request.param!r}"
            raise ValueError(msg)


@pytest.fixture
def cairo_context(cairo_surface: tuple[cairo.Surface, io.BytesIO | None]) -> cairo.Context[cairo.Surface]:
    surface, _ = cairo_surface
    return cairo.Context(surface)


@pytest.fixture
def pango_layout(cairo_context: cairo.Context[cairo.Surface]) -> Pango.Layout:
    return PangoCairo.create_layout(cairo_context)


type LayoutFactory = Callable[
    [Pango.Layout, cairo.Context[cairo.Surface]],
    LayoutInterface,
]


def _from_init(pango_layout: Pango.Layout, _: cairo.Context[cairo.Surface]) -> LayoutInterface:
    return LayoutInterface(pango_layout=pango_layout)


def _from_context(_: Pango.Layout, cairo_context: cairo.Context[cairo.Surface]) -> LayoutInterface:
    return LayoutInterface.from_cairo_context(cairo_context=cairo_context)


@pytest.fixture(
    params=[
        pytest.param(_from_init, id="init"),
        pytest.param(_from_context, id="from_context"),
    ]
)
def layout_interface(
    request: pytest.FixtureRequest,
    pango_layout: Pango.Layout,
    cairo_context: cairo.Context[cairo.Surface],
) -> LayoutInterface:
    factory: LayoutFactory = request.param
    return factory(pango_layout, cairo_context)
