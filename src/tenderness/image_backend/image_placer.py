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

"""Image placement with scaling modes for cairo contexts."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum, auto, unique
from typing import TYPE_CHECKING

import cairo

from tenderness.cairo_backend.cairo_enum_coerce import CairoEnumCoerce, CairoEnumMap, OperatorStr
from tenderness.core.image_formats import ImageFormat

if TYPE_CHECKING:
    from tenderness.core.geometry import Rectangle


@unique
class ImageScaleMode(StrEnum):
    """Scaling behavior when placing an image into a destination rectangle.

    Attributes
    ----------
    STRETCH
        Scale to fill the destination rectangle exactly; aspect ratio not preserved.
    FIT
        Uniform scale to fit inside the destination rectangle; may letterbox.
    FILL
        Uniform scale to fill the destination rectangle entirely; excess is cropped.
    NONE
        No scaling; placed at the destination origin at native pixel size.
    """

    STRETCH = auto()
    FIT = auto()
    FILL = auto()
    NONE = auto()


@dataclass(slots=True)
class ImagePlacerParameters:
    """Parameters for placing an image onto a cairo context.

    Attributes
    ----------
    path_to_image
        Path or file-like object for the source image.
    dest_rect
        Destination rectangle in device coordinates.
    scale_mode
        How the image is scaled to fit dest_rect.
    operator
        Cairo compositing operator.
    alpha
        Opacity applied when painting the image.
    image_format
        Format of the source image.
    """

    path_to_image: cairo._PathLike | cairo._FileLike
    dest_rect: Rectangle
    scale_mode: ImageScaleMode = field(default=ImageScaleMode.STRETCH)
    operator: cairo.Operator | OperatorStr = field(default=cairo.Operator.OVER)
    alpha: float = field(default=1.0)
    image_format: ImageFormat = field(default=ImageFormat.PNG)

    def __post_init__(self) -> None:
        """Coerce operator to a cairo.Operator enum value."""
        object.__setattr__(self, "operator", CairoEnumCoerce.coerce(CairoEnumMap.Operator, self.operator))


class ImagePlacer:
    """Places images onto a cairo context with configurable scaling."""

    def place(
        self,
        cairo_context: cairo.Context[cairo.Surface],
        params: ImagePlacerParameters,
    ) -> None:
        """Place an image onto cairo_context according to params.

        Parameters
        ----------
        cairo_context
            Cairo context to draw on.
        params
            Image placement parameters.

        Raises
        ------
        ValueError
            If params.image_format is not PNG.
        """
        if params.image_format != ImageFormat.PNG:
            msg = f"Works only with {ImageFormat.PNG.name} format, got {params.image_format.name}"
            raise ValueError(msg)

        png_surface = cairo.ImageSurface.create_from_png(params.path_to_image)
        src_w = png_surface.get_width()
        src_h = png_surface.get_height()

        dst_x = params.dest_rect.x_min
        dst_y = params.dest_rect.y_min
        dst_w, dst_h = params.dest_rect.normalized_size

        cairo_context.save()
        cairo_context.set_operator(params.operator)  # type: ignore[arg-type] # guaranteed by ImagePlacerParameters.__post_init__
        cairo_context.translate(dst_x, dst_y)

        match params.scale_mode:
            case ImageScaleMode.STRETCH:
                cairo_context.scale(dst_w / src_w, dst_h / src_h)
                cairo_context.set_source_surface(png_surface, 0, 0)

            case ImageScaleMode.FIT:
                scale = min(dst_w / src_w, dst_h / src_h)
                offset_x = (dst_w - src_w * scale) / 2
                offset_y = (dst_h - src_h * scale) / 2
                cairo_context.translate(offset_x, offset_y)
                cairo_context.scale(scale, scale)
                cairo_context.set_source_surface(png_surface, 0, 0)

            case ImageScaleMode.FILL:
                scale = max(dst_w / src_w, dst_h / src_h)
                offset_x = (dst_w - src_w * scale) / 2
                offset_y = (dst_h - src_h * scale) / 2
                cairo_context.rectangle(0, 0, dst_w, dst_h)
                cairo_context.clip()
                cairo_context.translate(offset_x, offset_y)
                cairo_context.scale(scale, scale)
                cairo_context.set_source_surface(png_surface, 0, 0)

            case ImageScaleMode.NONE:
                cairo_context.set_source_surface(png_surface, 0, 0)

            case _ as unreachable:
                msg = f"Unhandled {ImageScaleMode.__name__} value: {unreachable!r}"
                raise ValueError(msg)

        cairo_context.paint_with_alpha(params.alpha)
        cairo_context.restore()
