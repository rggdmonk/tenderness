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

"""Defines data structures for representing blocks and configurations used in the standard rendering pipeline."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

import cairo

from tenderness.cairo_backend.cairo_enum_coerce import CairoEnumCoerce, CairoEnumMap, OperatorStr
from tenderness.core.image_formats import ImageFormat
from tenderness.core.sentinel import _UNSET_PARAM, Settable
from tenderness.image_backend.image_placer import ImageScaleMode
from tenderness.layout_engines.minimal_flexbox.minimal_flexbox import MinimalFlexNode
from tenderness.pango_backend.layout_interface import TextStrategy

if TYPE_CHECKING:
    from tenderness.cairo_backend.color_patterns import PatternColorSpec
    from tenderness.cairo_backend.font_options_interface import FontOptionsInterfaceParameters
    from tenderness.cairo_backend.matrix.context_transformer_pipeline import TransformParameter
    from tenderness.cairo_backend.surface_configuration import SurfaceConfig
    from tenderness.core.geometry import Margin
    from tenderness.layout_engines.minimal_flexbox.minimal_flexbox import MinimalFlexNode
    from tenderness.pango_backend.font_description_interface import FontDescriptionInterfaceParameters
    from tenderness.pango_backend.layout_context_interface import LayoutContextInterfaceParameters
    from tenderness.pango_backend.layout_interface import LayoutInterfaceParameters


# --------------------------
# Blocks
# --------------------------
@dataclass(slots=True, kw_only=True)
class BaseBlock:
    """Base class for all blocks in the rendering pipeline."""

    block_name: str | None = None


@dataclass(slots=True)
class TextStyle:
    """Encapsulates all style parameters for text rendering."""

    font_options_params: Settable[FontOptionsInterfaceParameters] = _UNSET_PARAM
    font_description_params: Settable[FontDescriptionInterfaceParameters] = _UNSET_PARAM
    text_color_spec: Settable[PatternColorSpec] = _UNSET_PARAM
    layout_interface_params: Settable[LayoutInterfaceParameters] = _UNSET_PARAM
    layout_context_params: Settable[LayoutContextInterfaceParameters] = _UNSET_PARAM
    context_transform_params: Settable[list[TransformParameter]] = _UNSET_PARAM


@dataclass(slots=True, kw_only=True)
class TextBlock(BaseBlock):
    """Represents a block of text in the rendering pipeline."""

    text: str | None  # None = receive overflow from previous text block
    style: TextStyle | None = None
    text_strategy: TextStrategy | str = field(default=TextStrategy.TEXT)


@dataclass(slots=True, kw_only=True)
class ImageBlock(BaseBlock):
    """Represents a block of image in the rendering pipeline."""

    path_to_image: cairo._PathLike | cairo._FileLike

    scale_mode: ImageScaleMode = field(default=ImageScaleMode.STRETCH)
    operator: cairo.Operator | OperatorStr = field(default=cairo.Operator.OVER)
    alpha: float = field(default=1.0)
    image_format: ImageFormat = field(default=ImageFormat.PNG)

    def __post_init__(self) -> None:
        """Coerce operator to cairo.Operator if it's provided as a string."""
        self.operator = CairoEnumCoerce.coerce(CairoEnumMap.Operator, self.operator)


@dataclass(slots=True, kw_only=True)
class TableCell:
    """Represents a single cell in a table block."""

    content: str | object
    cell_name: str | None = None
    style: TextStyle | None = None
    text_strategy: TextStrategy | str = field(default=TextStrategy.TEXT)


@dataclass(slots=True, kw_only=True)
class TableBlock(BaseBlock):
    """Represents a block of table in the rendering pipeline."""

    cells: list[TableCell]
    table_cell_pos: MinimalFlexNode
    default_style: TextStyle | None = None


# --------------------------
# Configs
# --------------------------
@dataclass(slots=True)
class CanvasConfig:
    """Configuration for the canvas on which blocks will be rendered."""

    surface_config: SurfaceConfig
    global_margin: Settable[Margin] = _UNSET_PARAM
    block_spec: Settable[MinimalFlexNode] = _UNSET_PARAM
    background_spec: Settable[PatternColorSpec] = _UNSET_PARAM


@dataclass(slots=True)
class BlocksConfig:
    """Configuration for a collection of blocks in the rendering pipeline."""

    surface_config: SurfaceConfig
    blocks: list[TextBlock | ImageBlock | TableBlock]
    default_text_style: TextStyle | None = (
        None  # Default text style applied to all TextBlocks (can be overridden by block-level styles)
    )
