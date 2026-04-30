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

"""Image format enum and associated metadata."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, unique
from typing import TYPE_CHECKING, Self

if TYPE_CHECKING:
    from collections.abc import Callable


@dataclass(slots=True, frozen=True)
class ImageFormatInfo:
    """Metadata for an image format.

    Parameters
    ----------
    extension
        File extension including the leading dot (e.g. ``".png"``).
    supports_alpha
        Whether the format supports transparency.
    supports_compression
        Whether the format supports compression.
    is_vector
        Whether the format is vector-based.
    """

    extension: str
    supports_alpha: bool
    supports_compression: bool
    is_vector: bool


@unique
class ImageFormat(Enum):
    """Supported output image formats."""

    PNG = ImageFormatInfo(
        extension=".png",
        supports_alpha=True,
        supports_compression=True,
        is_vector=False,
    )

    JPEG = ImageFormatInfo(
        extension=".jpeg",
        supports_alpha=False,
        supports_compression=True,
        is_vector=False,
    )

    SVG = ImageFormatInfo(
        extension=".svg",
        supports_alpha=True,  # SVG can have transparency
        supports_compression=False,  # compression is not inherent to SVG, but can be applied externally
        is_vector=True,
    )

    PDF = ImageFormatInfo(
        extension=".pdf",
        supports_alpha=True,  # PDF supports transparency
        supports_compression=True,  # PDF has built-in compression
        is_vector=True,
    )

    # --------------------------
    # Properties (forwarded)
    # --------------------------
    @property
    def extension(self) -> str:
        """File extension including the leading dot."""
        return self.value.extension

    @property
    def supports_alpha(self) -> bool:
        """Whether this format supports transparency."""
        return self.value.supports_alpha

    @property
    def supports_compression(self) -> bool:
        """Whether this format supports compression."""
        return self.value.supports_compression

    @property
    def is_vector(self) -> bool:
        """Whether this format is vector-based."""
        return self.value.is_vector

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
    def from_extension(cls, extension: str) -> Self:
        """Return the format matching the given file extension.

        Parameters
        ----------
        extension
            File extension to look up, case-insensitive.

        Raises
        ------
        ValueError
            If no format matches the extension.
        """
        return cls._lookup_format(extension.lower(), lambda fmt: fmt.extension, "extension")

    # --------------------------
    # Filters
    # --------------------------
    @classmethod
    def get_formats_with_alpha(cls) -> list[Self]:
        """Return all formats that support transparency."""
        return [fmt for fmt in cls if fmt.supports_alpha]

    @classmethod
    def get_vector_formats(cls) -> list[Self]:
        """Return all vector formats."""
        return [fmt for fmt in cls if fmt.is_vector]

    @classmethod
    def get_raster_formats(cls) -> list[Self]:
        """Return all raster formats."""
        return [fmt for fmt in cls if not fmt.is_vector]
