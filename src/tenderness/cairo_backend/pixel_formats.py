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

"""Cairo pixel format definitions and metadata."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, StrEnum, auto, unique
from typing import TYPE_CHECKING, Self, assert_never

import cairo
import numpy  # noqa: ICN001

from tenderness.core.color_models import AlphaPosition, ColorModel

if TYPE_CHECKING:
    from collections.abc import Callable


@unique
class PixelDType(StrEnum):
    """Numeric dtype of a pixel memory unit or output array element."""

    UINT8 = auto()
    UINT16 = auto()
    UINT32 = auto()
    FLOAT32 = auto()

    @property
    def to_numpy(self) -> numpy.dtype:
        """Corresponding numpy dtype."""
        match self:
            case PixelDType.UINT8:
                return numpy.dtype(numpy.uint8)
            case PixelDType.UINT16:
                return numpy.dtype(numpy.uint16)
            case PixelDType.UINT32:
                return numpy.dtype(numpy.uint32)
            case PixelDType.FLOAT32:
                return numpy.dtype(numpy.float32)
            case _ as unreachable:
                assert_never(unreachable)

    @property
    def to_torch(self) -> None:
        """Corresponding torch dtype.

        Raises
        ------
        NotImplementedError
            Not yet implemented.
        """
        msg = "Not implemented yet"
        raise NotImplementedError(msg)

    @property
    def is_torch_stable(self) -> None:
        """Whether this dtype is stable for torch operations.

        Raises
        ------
        NotImplementedError
            Not yet implemented.
        """
        msg = "Not implemented yet"
        raise NotImplementedError(msg)


@unique
class ChannelOrder(StrEnum):
    """Requested channel order of the output array (user-facing)."""

    BGR = auto()
    BGRA = auto()
    RGB = auto()
    RGBA = auto()

    @property
    def has_alpha(self) -> bool:
        """True if this channel order includes an alpha channel."""
        match self:
            case ChannelOrder.BGR | ChannelOrder.RGB:
                return False
            case ChannelOrder.BGRA | ChannelOrder.RGBA:
                return True
            case _ as unreachable:
                assert_never(unreachable)

    @property
    def n_channels(self) -> int:
        """Number of channels in this order."""
        match self:
            case ChannelOrder.BGR | ChannelOrder.RGB:
                return 3
            case ChannelOrder.BGRA | ChannelOrder.RGBA:
                return 4
            case _ as unreachable:
                assert_never(unreachable)

    @property
    def is_bgr_base(self) -> bool:
        """True if the channel base order is BGR (OpenCV convention)."""
        match self:
            case ChannelOrder.BGR | ChannelOrder.BGRA:
                return True
            case ChannelOrder.RGB | ChannelOrder.RGBA:
                return False
            case _ as unreachable:
                assert_never(unreachable)


@unique
class PixelOrder(StrEnum):
    """Order of color components within an interleaved pixel."""

    BGRA = auto()
    BGRX = auto()
    RGB_PACKED_565 = auto()  # RGB 5-6-5 packed into uint16
    RGB_PACKED_30 = auto()  # RGB 10-10-10 packed into uint32 (2 bits unused)
    ALPHA_ONLY = auto()  # single alpha channel
    RGBF = auto()  # float RGB, R-G-B order
    RGBAF = auto()  # float RGBA, R-G-B-A order

    @property
    def has_alpha(self) -> bool:  # noqa: PLR0911
        """True if this pixel order includes an alpha channel."""
        match self:
            case PixelOrder.BGRX:
                return False
            case PixelOrder.BGRA:
                return True
            case PixelOrder.RGB_PACKED_565:
                return False
            case PixelOrder.RGB_PACKED_30:
                return False
            case PixelOrder.ALPHA_ONLY:
                return True
            case PixelOrder.RGBF:
                return False
            case PixelOrder.RGBAF:
                return True
            case _ as unreachable:
                assert_never(unreachable)

    @property
    def alpha_position(self) -> AlphaPosition:  # noqa: PLR0911
        """Position of the alpha channel within the pixel."""
        match self:
            case PixelOrder.BGRX:
                return AlphaPosition.NONE
            case PixelOrder.BGRA:
                return AlphaPosition.LAST
            case PixelOrder.RGB_PACKED_565:
                return AlphaPosition.NONE
            case PixelOrder.RGB_PACKED_30:
                return AlphaPosition.NONE
            case PixelOrder.ALPHA_ONLY:
                return AlphaPosition.ONLY
            case PixelOrder.RGBF:
                return AlphaPosition.NONE
            case PixelOrder.RGBAF:
                return AlphaPosition.LAST
            case _ as unreachable:
                assert_never(unreachable)

    @property
    def native_channel_order(self) -> ChannelOrder | None:
        """Natural ChannelOrder for this pixel layout, or ``None`` for packed and alpha-only formats."""
        match self:
            case PixelOrder.BGRA:
                return ChannelOrder.BGRA
            case PixelOrder.BGRX:
                return ChannelOrder.BGR
            case PixelOrder.RGBF:
                return ChannelOrder.RGB
            case PixelOrder.RGBAF:
                return ChannelOrder.RGBA
            case PixelOrder.ALPHA_ONLY | PixelOrder.RGB_PACKED_565 | PixelOrder.RGB_PACKED_30:
                return None  # no meaningful ChannelOrder applies
            case _ as unreachable:
                assert_never(unreachable)


@dataclass(slots=True, frozen=True)
class PixelFormatInfo:
    """Metadata record for a single cairo pixel format."""

    format_value: cairo.Format
    format_name: str
    color_model: ColorModel
    pixel_order: PixelOrder
    memory_dtype: PixelDType  # dtype of the raw memory unit
    array_dtype: PixelDType  # dtype of the unpacked/output array
    n_channels: int  # number of meaningful color/alpha channels
    is_packed: bool  # True if channels are bit-packed into a single memory unit
    bits_per_pixel: int
    bytes_per_pixel: int
    description: str

    @property
    def is_premultiplied(self) -> bool:
        """True if alpha values are premultiplied into color channels."""
        match self.format_value:
            case cairo.Format.ARGB32 | cairo.Format.RGBA128F:
                return True
            case _:
                return False

    @property
    def has_alpha(self) -> bool:
        """True if the format includes an alpha channel."""
        return self.color_model.has_alpha


@unique
class PixelFormat(Enum):
    """Enumeration of supported cairo pixel formats with associated metadata."""

    RGB24 = PixelFormatInfo(
        format_value=cairo.Format.RGB24,
        format_name="RGB24",
        color_model=ColorModel.RGB,
        pixel_order=PixelOrder.BGRX,
        memory_dtype=PixelDType.UINT32,
        array_dtype=PixelDType.UINT8,
        n_channels=4,  # 4 bytes in memory, X byte unused
        is_packed=False,
        bits_per_pixel=32,
        bytes_per_pixel=4,
        description=(
            "Each pixel is a 32-bit quantity, with the upper 8 bits unused. "
            "Red, Green, and Blue are stored in the remaining 24 bits in that order."
        ),
    )

    ARGB32 = PixelFormatInfo(
        format_value=cairo.Format.ARGB32,
        format_name="ARGB32",
        color_model=ColorModel.RGBA,
        pixel_order=PixelOrder.BGRA,
        memory_dtype=PixelDType.UINT32,
        array_dtype=PixelDType.UINT8,
        n_channels=4,
        is_packed=False,
        bits_per_pixel=32,
        bytes_per_pixel=4,
        description="Each pixel is a 32-bit quantity, with alpha in the upper 8 bits, then red, then green, then blue. "
        "The 32-bit quantities are stored native-endian. Pre-multiplied alpha is used. (That is, 50% transparent red is 0x80800000, not 0x80ff0000.)",
    )

    RGB96F = PixelFormatInfo(
        format_value=cairo.Format.RGB96F,
        format_name="RGB96F",
        color_model=ColorModel.RGB,
        pixel_order=PixelOrder.RGBF,
        memory_dtype=PixelDType.FLOAT32,
        array_dtype=PixelDType.FLOAT32,
        n_channels=3,
        is_packed=False,
        bits_per_pixel=96,
        bytes_per_pixel=12,
        description="3 floats, R, G, B.",
    )

    RGBA128F = PixelFormatInfo(
        format_value=cairo.Format.RGBA128F,
        format_name="RGBA128F",
        color_model=ColorModel.RGBA,
        pixel_order=PixelOrder.RGBAF,
        memory_dtype=PixelDType.FLOAT32,
        array_dtype=PixelDType.FLOAT32,
        n_channels=4,
        is_packed=False,
        bits_per_pixel=128,
        bytes_per_pixel=16,
        description="4 floats, R, G, B, A.",
    )

    A8 = PixelFormatInfo(
        format_value=cairo.Format.A8,
        format_name="A8",
        color_model=ColorModel.ALPHA,
        pixel_order=PixelOrder.ALPHA_ONLY,
        memory_dtype=PixelDType.UINT8,
        array_dtype=PixelDType.UINT8,
        n_channels=1,
        is_packed=False,
        bits_per_pixel=8,
        bytes_per_pixel=1,
        description="Each pixel is a 8-bit quantity holding an alpha value.",
    )

    RGB16_565 = PixelFormatInfo(
        format_value=cairo.Format.RGB16_565,
        format_name="RGB16_565",
        color_model=ColorModel.RGB,
        pixel_order=PixelOrder.RGB_PACKED_565,
        memory_dtype=PixelDType.UINT16,
        array_dtype=PixelDType.UINT16,
        n_channels=3,
        is_packed=True,
        bits_per_pixel=16,
        bytes_per_pixel=2,
        description="Each pixel is a 16-bit quantity with red in the upper 5 bits, then green in the middle 6 bits, and blue in the lower 5 bits.",
    )

    RGB30 = PixelFormatInfo(
        format_value=cairo.Format.RGB30,
        format_name="RGB30",
        color_model=ColorModel.RGB,
        pixel_order=PixelOrder.RGB_PACKED_30,
        memory_dtype=PixelDType.UINT32,
        array_dtype=PixelDType.UINT32,
        n_channels=3,
        is_packed=True,
        bits_per_pixel=32,  # 30 bits used, 2 bits unused
        bytes_per_pixel=4,
        description="Like RGB24 but with 10bpc.",
    )

    # --------------------------
    # Properties (forwarded)
    # --------------------------
    @property
    def format_value(self) -> cairo.Format:
        """cairo.Format enum value."""
        return self.value.format_value

    @property
    def format_name(self) -> str:
        """String name of the format."""
        return self.value.format_name

    @property
    def color_model(self) -> ColorModel:
        """Color model of this format."""
        return self.value.color_model

    @property
    def pixel_order(self) -> PixelOrder:
        """Pixel component order."""
        return self.value.pixel_order

    @property
    def description(self) -> str:
        """Human-readable format description."""
        return self.value.description

    @property
    def has_alpha(self) -> bool:
        """True if the format includes an alpha channel."""
        return self.value.has_alpha

    @property
    def is_premultiplied(self) -> bool:
        """True if alpha is premultiplied."""
        return self.value.is_premultiplied

    @property
    def memory_dtype(self) -> PixelDType:
        """Dtype of the raw memory unit."""
        return self.value.memory_dtype

    @property
    def array_dtype(self) -> PixelDType:
        """Dtype of the unpacked output array."""
        return self.value.array_dtype

    @property
    def n_channels(self) -> int:
        """Number of meaningful color/alpha channels."""
        return self.value.n_channels

    @property
    def is_packed(self) -> bool:
        """True if channels are bit-packed into a single memory unit."""
        return self.value.is_packed

    @property
    def bits_per_pixel(self) -> int:
        """Number of bits per pixel."""
        return self.value.bits_per_pixel

    @property
    def bytes_per_pixel(self) -> int:
        """Number of bytes per pixel."""
        return self.value.bytes_per_pixel

    # --------------------------
    # Lookup helpers
    # --------------------------
    @classmethod
    def _lookup_format(
        cls,
        key: object,
        mapping_func: Callable[[Self], object],
        key_name: str,
    ) -> Self:
        format_map = {mapping_func(fmt): fmt for fmt in cls}
        try:
            return format_map[key]
        except KeyError:
            available = list(format_map.keys())
            msg = f"No matching {key_name}: {key!r}. Available: {available}"
            raise ValueError(msg) from None

    @classmethod
    def from_cairo_format(cls, format_value: cairo.Format) -> Self:
        """Look up a PixelFormat by cairo.Format value.

        Parameters
        ----------
        format_value
            cairo.Format enum value to look up.

        Raises
        ------
        ValueError
            If no format matches ``format_value``.
        """
        return cls._lookup_format(format_value, lambda fmt: fmt.format_value, "cairo.Format")

    @classmethod
    def from_format_name(cls, format_name: str) -> Self:
        """Look up a PixelFormat by its string name.

        Parameters
        ----------
        format_name
            Format name string to look up.

        Raises
        ------
        ValueError
            If no format matches ``format_name``.
        """
        return cls._lookup_format(format_name, lambda fmt: fmt.format_name, "format_name")

    # --------------------------
    # Filters
    # --------------------------
    @classmethod
    def get_formats_with_alpha(cls) -> list[Self]:
        """Return all formats that include an alpha channel."""
        return [fmt for fmt in cls if fmt.has_alpha]

    @classmethod
    def get_formats_without_alpha(cls) -> list[Self]:
        """Return all formats without an alpha channel."""
        return [fmt for fmt in cls if not fmt.has_alpha]

    @classmethod
    def get_formats_by_color_model(cls, color_model: ColorModel) -> list[Self]:
        """Return all formats matching a given color model.

        Parameters
        ----------
        color_model
            Color model to filter by.
        """
        return [fmt for fmt in cls if fmt.color_model == color_model]

    @classmethod
    def get_premultiplied_formats(cls) -> list[Self]:
        """Return all formats with premultiplied alpha."""
        return [fmt for fmt in cls if fmt.is_premultiplied]

    @classmethod
    def get_packed_formats(cls) -> list[Self]:
        """Return all bit-packed pixel formats."""
        return [fmt for fmt in cls if fmt.is_packed]

    @classmethod
    def get_formats_by_array_dtype(cls, dtype: PixelDType) -> list[Self]:
        """Return all formats whose output array uses a given dtype.

        Parameters
        ----------
        dtype
            Array dtype to filter by.
        """
        return [fmt for fmt in cls if fmt.array_dtype == dtype]

    @classmethod
    def get_formats_by_n_channels(cls, n: int) -> list[Self]:
        """Return all formats with a given number of channels.

        Parameters
        ----------
        n
            Number of channels to filter by.
        """
        return [fmt for fmt in cls if fmt.n_channels == n]
