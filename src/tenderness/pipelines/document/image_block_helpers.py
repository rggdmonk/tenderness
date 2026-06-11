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

"""Image block helpers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

import cairo

from tenderness.cairo_backend.cairo_enum_coerce import CairoEnumCoerce, CairoEnumMap, OperatorStr
from tenderness.core.image_formats import ImageFormat
from tenderness.image_backend.image_placer import ImageScaleMode
from tenderness.pipelines.document.pipeline_schema import BaseBlock

if TYPE_CHECKING:
    from tenderness.core.geometry import Rectangle


@dataclass(slots=True, kw_only=True)
class ImageBlock(BaseBlock):
    """Image block configuration.

    Attributes
    ----------
    path_to_image
        Source image file path or file-like object.
    scale_mode
        How the image is scaled to fit the block area.
    operator
        Cairo compositing operator.
    alpha
        Opacity, in ``[0.0, 1.0]``.
    image_format
        Image file format.
    """

    path_to_image: cairo._PathLike | cairo._FileLike

    scale_mode: ImageScaleMode = ImageScaleMode.STRETCH
    operator: cairo.Operator | OperatorStr = cairo.Operator.OVER
    alpha: float = 1.0
    image_format: ImageFormat = ImageFormat.PNG

    def __post_init__(self) -> None:
        """Coerce ``operator`` to a ``cairo.Operator`` enum value."""
        self.operator = CairoEnumCoerce.coerce(CairoEnumMap.Operator, self.operator)


@dataclass(slots=True)
class ImageBlockResult:
    """Positioned image block output.

    Attributes
    ----------
    block_name
        Block identifier.
    block_position_name
        Position label within the document.
    block_position_rect
        Block's bounding rectangle in document coordinates.
    """

    block_name: str | None
    block_position_name: str | None
    block_position_rect: Rectangle
