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

"""Conversion of cairo surfaces to numpy arrays."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from enum import StrEnum, auto, unique
from typing import assert_never

import cairo
import numpy  # noqa: ICN001

from tenderness.cairo_backend.pixel_formats import ChannelOrder, PixelDType, PixelFormat, PixelOrder
from tenderness.cairo_backend.surface_configuration import (
    ImageSurfaceConfig,
    PDFSurfaceConfig,
    SurfaceConfig,
    SVGSurfaceConfig,
)

logger = logging.getLogger(__name__)


@unique
class SurfaceArrayBackend(StrEnum):
    """Backend for surface-to-array conversion."""

    NUMPY = auto()
    TORCH = auto()


@dataclass(slots=True)
class SurfaceArrayResult:
    """Array result from a cairo surface conversion.

    Notes
    -----
    ``channel_order`` is ``None`` for formats where the concept does not apply
    (packed formats: RGB16_565, RGB30; and A8).

    ``image_array`` is a mutable numpy array. When ``is_copy=False``, the array
    is a view into Cairo's surface buffer — the surface must remain alive and
    unmodified for as long as the array is in use.
    """

    backend: SurfaceArrayBackend
    image_array: numpy.ndarray
    channel_order: ChannelOrder | None
    pixel_format: PixelFormat
    is_copy: bool

    @property
    def shape(self) -> tuple[int, ...]:
        """Shape of the image array."""
        return self.image_array.shape

    @property
    def dtype(self) -> numpy.dtype:
        """Dtype of the image array."""
        return self.image_array.dtype

    @property
    def is_premultiplied(self) -> bool:
        """True when pixel values use premultiplied alpha."""
        return self.pixel_format.is_premultiplied

    @property
    def has_alpha(self) -> bool:
        """True when the array includes an alpha channel."""
        if self.channel_order is None:
            return self.pixel_format.has_alpha
        return self.channel_order.has_alpha


@dataclass(slots=True)
class SurfaceArrayConverterParameters:
    """Parameters for surface-to-array conversion.

    Parameters
    ----------
    channel_order
        Desired channel ordering in the output array; format-dependent.
    copy
        Return a copy of the data when ``True``, a zero-copy view when ``False``.
    backend
        Array backend to produce.
    finish_after
        Call ``surface.finish()`` after conversion when ``True``.
    """

    channel_order: ChannelOrder | None = ChannelOrder.RGB
    copy: bool = True
    backend: SurfaceArrayBackend = SurfaceArrayBackend.NUMPY
    finish_after: bool = True


class SurfaceArrayConverter:
    """Converts cairo surfaces to numpy arrays."""

    def surface_to_array(
        self,
        surface: cairo.Surface,
        surface_config: SurfaceConfig,
        surface_array_converter_params: SurfaceArrayConverterParameters | None = None,
    ) -> SurfaceArrayResult:
        """Convert a cairo surface to an array result.

        Parameters
        ----------
        surface
            Cairo surface to convert.
        surface_config
            Configuration describing the surface format.
        surface_array_converter_params
            Conversion parameters; uses defaults when ``None``.

        Raises
        ------
        NotImplementedError
            If surface is an SVGSurface or PDFSurface.
        TypeError
            If the surface/config combination is unsupported.
        """
        if surface_array_converter_params is None:
            surface_array_converter_params = SurfaceArrayConverterParameters()

        match (surface, surface_config):
            case (cairo.ImageSurface(), ImageSurfaceConfig()):
                surface_arr_result = self._image_surface_to_array(
                    surface=surface,
                    surface_config=surface_config,
                    channel_order=surface_array_converter_params.channel_order,
                    copy=surface_array_converter_params.copy,
                    backend=surface_array_converter_params.backend,
                )
                if surface_array_converter_params.finish_after:
                    surface.finish()
                return surface_arr_result
            case (cairo.SVGSurface(), SVGSurfaceConfig()):
                msg = "Conversion from SVGSurface to array is not supported."
                raise NotImplementedError(msg)
            case (cairo.PDFSurface(), PDFSurfaceConfig()):
                msg = "Conversion from PDFSurface to array is not supported."
                raise NotImplementedError(msg)
            case _:
                msg = f"Unsupported surface/config combination: {type(surface)!r}, {type(surface_config)!r}"
                raise TypeError(msg)

    def _image_surface_to_array(
        self,
        surface: cairo.ImageSurface,
        surface_config: ImageSurfaceConfig,
        channel_order: ChannelOrder | None,
        *,
        copy: bool,
        backend: SurfaceArrayBackend,
    ) -> SurfaceArrayResult:

        match backend:
            case SurfaceArrayBackend.NUMPY:
                return self.to_numpy(
                    surface=surface,
                    surface_config=surface_config,
                    channel_order=channel_order,
                    copy=copy,
                )
            case SurfaceArrayBackend.TORCH:
                msg = "Conversion to PyTorch tensors is not implemented yet."
                raise NotImplementedError(msg)
            case _ as unreachable:
                assert_never(unreachable)

    def to_numpy(
        self,
        surface: cairo.ImageSurface,
        surface_config: ImageSurfaceConfig,
        channel_order: ChannelOrder | None = None,
        *,
        copy: bool = True,
    ) -> SurfaceArrayResult:
        """Convert a cairo ImageSurface to a numpy-backed SurfaceArrayResult.

        Parameters
        ----------
        surface
            Cairo ImageSurface to convert.
        surface_config
            Configuration describing the surface format.
        channel_order
            Desired channel ordering; uses the format's native order when ``None``.
        copy
            Return a copy when ``True``, a zero-copy view when ``False``.
        """
        surface.flush()

        # trust surface_config
        width = surface_config.width
        height = surface_config.height

        stride = surface.get_stride()
        buffer = surface.get_data()

        mem_dtype = surface_config.pixel_format.memory_dtype.to_numpy

        bytes_per_pixel = surface_config.pixel_format.bytes_per_pixel
        cols = stride // bytes_per_pixel

        if surface_config.pixel_format.is_packed:
            raw = numpy.ndarray(shape=(height, cols), dtype=mem_dtype, buffer=buffer)
            raw = raw[:, :width]
            array = raw.copy() if copy else raw
            resolved_order = None

        elif surface_config.pixel_format.memory_dtype == PixelDType.FLOAT32:
            # RGB96F (c=3), RGBA128F (c=4): returned in Cairo's native order
            c = surface_config.pixel_format.n_channels
            raw = numpy.ndarray(shape=(height, cols, c), dtype=mem_dtype, buffer=buffer)
            raw = raw[:, :width, :]
            array = raw.copy() if copy else raw
            # Resolve from pixel_order: RGBF → RGB, RGBAF → RGBA
            resolved_order = surface_config.pixel_format.pixel_order.native_channel_order

        elif surface_config.pixel_format.pixel_order == PixelOrder.ALPHA_ONLY:
            # A8: single byte per pixel, stride already in bytes
            raw = numpy.ndarray(shape=(height, stride), dtype=mem_dtype, buffer=buffer)
            raw = raw[:, :width]
            array = raw.copy() if copy else raw
            resolved_order = None
        else:
            # Interleaved uint8: ARGB32 (BGRA layout) and RGB24 (BGRX layout)
            # Resolve None to the format's native channel order
            resolved_order = channel_order or surface_config.pixel_format.pixel_order.native_channel_order
            assert resolved_order is not None, (
                f"pixel_order {surface_config.pixel_format.pixel_order} has no native_channel_order; "
                "cannot use it with interleaved uint8 format."
            )

            raw = numpy.ndarray(shape=(height, cols), dtype=mem_dtype, buffer=buffer)
            byte_view = raw[:, :width].view(numpy.uint8).reshape(height, width, 4)
            array = self._reorder_channels_numpy(
                byte_view=byte_view,
                pixel_order=surface_config.pixel_format.pixel_order,
                channel_order=resolved_order,
                height=height,
                width=width,
                copy=copy,
            )

        return SurfaceArrayResult(
            backend=SurfaceArrayBackend.NUMPY,
            image_array=array,
            channel_order=resolved_order,
            pixel_format=surface_config.pixel_format,
            is_copy=copy,
        )

    def _reorder_channels_numpy(
        self,
        byte_view: numpy.ndarray,  # (h, w, 4), layout: [B, G, R, A|X]
        pixel_order: PixelOrder,
        channel_order: ChannelOrder,
        height: int,
        width: int,
        *,
        copy: bool,
    ) -> numpy.ndarray:

        if channel_order.has_alpha and pixel_order == PixelOrder.BGRX:
            msg = f"Requested channel order {channel_order} has alpha, but pixel format {pixel_order} has no alpha channel."
            raise ValueError(msg)

        b = byte_view[..., 0]
        g = byte_view[..., 1]
        r = byte_view[..., 2]

        match channel_order:
            case ChannelOrder.BGRA if pixel_order == PixelOrder.BGRA:
                # Native layout — zero-copy possible
                return byte_view.copy() if copy else byte_view

            case ChannelOrder.BGR if pixel_order == PixelOrder.BGRX:
                # Native layout for RGB24 — zero-copy possible
                bgr = byte_view[..., :3]
                return bgr.copy() if copy else bgr

            case ChannelOrder.BGR:
                out = numpy.empty((height, width, 3), dtype=numpy.uint8)
                out[..., 0] = b
                out[..., 1] = g
                out[..., 2] = r
                return out

            case ChannelOrder.RGB:
                out = numpy.empty((height, width, 3), dtype=numpy.uint8)
                out[..., 0] = r
                out[..., 1] = g
                out[..., 2] = b
                return out

            case ChannelOrder.BGRA:
                a = byte_view[..., 3]
                out = numpy.empty((height, width, 4), dtype=numpy.uint8)
                out[..., 0] = b
                out[..., 1] = g
                out[..., 2] = r
                out[..., 3] = a
                return out

            case ChannelOrder.RGBA:
                a = byte_view[..., 3]
                out = numpy.empty((height, width, 4), dtype=numpy.uint8)
                out[..., 0] = r
                out[..., 1] = g
                out[..., 2] = b
                out[..., 3] = a
                return out
            case _:
                msg = f"Unsupported channel order: {channel_order!r}"
                raise ValueError(msg)
