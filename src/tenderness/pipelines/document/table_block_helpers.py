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

"""Table block helpers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from tenderness.core.sentinel import _UNSET_PARAM, Settable
from tenderness.layout_engines.minimal_flexbox.minimal_flexbox import MinimalFlexNode
from tenderness.pango_backend.layout_interface import LayoutInterface, TextStrategy
from tenderness.pipelines.document.pipeline_schema import BaseBlock

if TYPE_CHECKING:
    import cairo

    from tenderness.core.geometry import Rectangle
    from tenderness.layout_engines.minimal_flexbox.minimal_flexbox import MinimalFlexBox, MinimalFlexNode
    from tenderness.pipelines.document.text_block_helpers import TextStyle


@dataclass(slots=True, kw_only=True)
class TextCell:
    """Text cell configuration.

    Attributes
    ----------
    cell_name
        Cell identifier, or ``None`` if unnamed.
    text
        Text to render.
    text_style
        Cell-level text style; overrides the base style where set.
    text_strategy
        Text rendering strategy.
    """

    cell_name: str | None = None
    text: str
    text_style: Settable[TextStyle] = _UNSET_PARAM
    text_strategy: TextStrategy | str = TextStrategy.TEXT


@dataclass(slots=True, kw_only=True)
class TableBlock(BaseBlock):
    """Table block configuration.

    Attributes
    ----------
    cells
        Cells to render.
    table_cell_pos
        Cell arrangement specification.
    base_text_style
        Default text style applied to all cells.
    """

    cells: list[TextCell]
    table_cell_pos: MinimalFlexNode
    base_text_style: Settable[TextStyle] = _UNSET_PARAM


@dataclass(slots=True, kw_only=True)
class TextCellResult:
    """Rendered text cell output.

    Attributes
    ----------
    cell_name
        Cell identifier.
    cell_position_name
        Position label within the table.
    cell_position_rect
        Cell's bounding rectangle in document coordinates.
    layout_interface
        Layout interface after rendering.
    ctm_cairo_matrix
        Current transformation matrix at render time.
    """

    cell_name: str | None
    cell_position_name: str | None
    cell_position_rect: Rectangle
    layout_interface: LayoutInterface
    ctm_cairo_matrix: cairo.Matrix


@dataclass(slots=True, kw_only=True)
class TableBlockResult:
    """Rendered table block output.

    Attributes
    ----------
    block_name
        Block identifier.
    block_position_name
        Position label within the document.
    block_position_rect
        Block's bounding rectangle in document coordinates.
    result_cells
        Results for each rendered cell.
    """

    block_name: str | None
    block_position_name: str | None
    block_position_rect: Rectangle
    result_cells: list[TextCellResult]


@dataclass(slots=True)
class CellPosition:
    """Named cell with its resolved rectangle.

    Attributes
    ----------
    name
        Cell identifier, or ``None`` if unnamed.
    rect
        Cell's bounding rectangle in document coordinates.
    """

    name: str | None
    rect: Rectangle


class TableBlockHelpers:
    """Static helpers for table block rendering."""

    @staticmethod
    def create_cells_within_container(
        minimal_flexbox_engine: MinimalFlexBox,
        container_rect: Rectangle,
        node: MinimalFlexNode,
    ) -> list[CellPosition]:
        """Resolve cell positions from ``node`` within ``container_rect``.

        Parameters
        ----------
        minimal_flexbox_engine
            Engine used to resolve the layout tree.
        container_rect
            Available area for the table.
        node
            Cell arrangement specification.

        Returns
        -------
        list[CellPosition]
            Computed positions for each cell.
        """
        result_tree = minimal_flexbox_engine.resolve_tree(container=container_rect, node=node)
        cell_positions = [CellPosition(name=node.name, rect=rect) for node, rect in result_tree]

        return cell_positions  # noqa: RET504
