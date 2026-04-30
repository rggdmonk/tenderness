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

"""Output models for the standard rendering pipeline."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import io

    import cairo

    from tenderness.bounding_boxes.bounding_boxes_schema import (
        Tetragon,
    )
    from tenderness.core.geometry import Margin, Rectangle
    from tenderness.pango_backend.layout_interface import LayoutInterface


@dataclass(slots=True)
class BlockPosition:
    """Represents the position of a block on the canvas after layout calculation."""

    name: str | None
    rect: Rectangle


@dataclass(slots=True)
class SetupRenderResult:
    """Result of the setup_render function, containing all necessary information for rendering."""

    surface_rect: Rectangle
    content_rect: Rectangle
    canvas_margin: Margin
    block_positions: list[BlockPosition]
    surface: cairo.Surface
    stream: io.BytesIO | None
    cairo_context: cairo.Context[cairo.Surface]


@dataclass(slots=True)
class BlockBoundingBoxesResult:
    """Result of the block_bounding_boxes function, containing bounding boxes for each block."""

    surface_bbox: Tetragon
    content_bbox: Tetragon
    block_boxes: list[Tetragon]


@dataclass(slots=True)
class TextBlockResult:
    """Represents the result of rendering a text block, including its position and layout information."""

    position_name: str | None
    block_name: str | None
    rect: Rectangle
    layout_interface: LayoutInterface
    matrix: cairo.Matrix


@dataclass(slots=True)
class ImageBlockResult:
    """Represents the result of rendering an image block, including its position and layout information."""

    position_name: str | None
    block_name: str | None
    rect: Rectangle


@dataclass(slots=True)
class TableBlockResult:
    """Represents the result of rendering a table block, including its position and layout information."""

    position_name: str | None
    table_name: str | None
    cell_names: list[str | None]
    cells_rects: list[Rectangle]
    cell_layouts: list[LayoutInterface]
    cell_matrices: list[cairo.Matrix]


BlockResult = TextBlockResult | ImageBlockResult | TableBlockResult


@dataclass(slots=True)
class RenderTextResult:
    """Represents the result of rendering text blocks, including their positions and layout information."""

    rendered_blocks: list[BlockResult]
