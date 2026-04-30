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

"""Image backend definitions and capability queries."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, unique
from typing import Self

from tenderness.core.image_formats import ImageFormat


@dataclass(slots=True, frozen=True)
class ImageBackendInfo:
    """Backend metadata: name and supported formats."""

    backend_name: str
    supported_formats: frozenset[ImageFormat]


@unique
class ImageBackend(Enum):
    """Available image rendering backends with their format capabilities."""

    CAIRO = ImageBackendInfo(
        backend_name="pycairo",
        supported_formats=frozenset({ImageFormat.PNG, ImageFormat.SVG, ImageFormat.PDF}),
    )
    PIL = ImageBackendInfo(
        backend_name="pillow",
        supported_formats=frozenset({ImageFormat.PNG, ImageFormat.JPEG}),
    )
    CV2 = ImageBackendInfo(
        backend_name="opencv-python",
        supported_formats=frozenset({ImageFormat.PNG, ImageFormat.JPEG}),
    )

    # --------------------------
    # Properties (forwarded)
    # --------------------------
    @property
    def backend_name(self) -> str:
        """Backend package name."""
        return self.value.backend_name

    @property
    def supported_formats(self) -> frozenset[ImageFormat]:
        """Set of formats this backend can produce."""
        return self.value.supported_formats

    # --------------------------
    # Methods
    # --------------------------
    def is_image_format_supported(self, image_format: ImageFormat) -> bool:
        """Return whether ``image_format`` is supported by this backend."""
        return image_format in self.supported_formats

    def has_alpha_support(self) -> bool:
        """Return whether any supported format handles alpha."""
        return any(fmt.supports_alpha for fmt in self.supported_formats)

    def has_vector_support(self) -> bool:
        """Return whether any supported format is vector-based."""
        return any(fmt.is_vector for fmt in self.supported_formats)

    # --------------------------
    # Class Methods
    # --------------------------
    @classmethod
    def backends_supporting_format(cls, image_format: ImageFormat) -> list[Self]:
        """Return all backends that support ``image_format``."""
        return [backend for backend in cls if backend.is_image_format_supported(image_format)]

    @classmethod
    def backends_supporting_all_formats(cls, *formats: ImageFormat) -> list[Self]:
        """Return backends that support all given formats.

        Parameters
        ----------
        *formats
            Formats that must all be supported; returns all backends if empty.
        """
        if not formats:
            return list(cls)

        format_set = set(formats)
        return [backend for backend in cls if format_set.issubset(backend.supported_formats)]
