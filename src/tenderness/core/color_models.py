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

"""Color model enums and cairo color source helpers."""

from __future__ import annotations

from enum import StrEnum, auto, unique
from typing import TYPE_CHECKING, assert_never

if TYPE_CHECKING:
    import cairo

    from tenderness.colors.color_selector import Color


@unique
class AlphaPosition(StrEnum):
    """Position of the alpha channel within a pixel."""

    FIRST = auto()
    LAST = auto()
    NONE = auto()
    ONLY = auto()


@unique
class ColorModel(StrEnum):
    """Logical color model from user perspective."""

    RGB = auto()
    RGBA = auto()
    ALPHA = auto()  # alpha-only channel (e.g. A8 mask format)

    @property
    def has_alpha(self) -> bool:
        """True if this model includes an alpha channel."""
        match self:
            case ColorModel.RGB:
                return False
            case ColorModel.RGBA:
                return True
            case ColorModel.ALPHA:
                return True
            case _:
                assert_never(self)

    @property
    def alpha_position(self) -> AlphaPosition:
        """Alpha channel position for this model."""
        match self:
            case ColorModel.RGB:
                return AlphaPosition.NONE
            case ColorModel.RGBA:
                return AlphaPosition.LAST
            case ColorModel.ALPHA:
                return AlphaPosition.ONLY
            case _:
                assert_never(self)

    @property
    def num_channels(self) -> int:
        """Number of color/alpha channels."""
        match self:
            case ColorModel.RGB:
                return 3
            case ColorModel.RGBA:
                return 4
            case ColorModel.ALPHA:
                return 1
            case _:
                assert_never(self)


class ColorModelHelpers:
    """Cairo color source helpers."""

    @staticmethod
    def set_source_color(
        cairo_context: cairo.Context[cairo.Surface],
        color_model: ColorModel,
        color: Color,
    ) -> None:
        """Set the cairo source color from a Color, using the appropriate model.

        Parameters
        ----------
        cairo_context
            Context whose source is set.
        color_model
            Determines whether RGB or RGBA values are used.
        color
            Color to apply.

        Raises
        ------
        ValueError
            If ``color_model`` is not RGB or RGBA.
        """
        match color_model:
            case ColorModel.RGB:
                cairo_context.set_source_rgb(*color.rgb)
            case ColorModel.RGBA:
                cairo_context.set_source_rgba(*color.rgba)
            case _:
                msg = f"Unsupported {color_model=}"
                raise ValueError(msg)
