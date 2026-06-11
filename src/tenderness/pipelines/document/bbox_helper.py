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

"""Bounding-box helpers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from tenderness.bounding_boxes.bounding_boxes_schema import Quadrilateral, TextBoundingBoxes


@dataclass(slots=True)
class TextBlockBBoxesResult:
    """Bounding-box output for a single text block.

    Attributes
    ----------
    block_name
        Block identifier.
    block_position_name
        Position label within the document.
    bboxes
        Extracted bounding boxes for the block's text.
    """

    block_name: str | None
    block_position_name: str | None
    bboxes: TextBoundingBoxes

    def to_dict(self) -> dict[str, Any]:
        """Serialize to a JSON-compatible dict.

        Returns
        -------
        dict[str, Any]
            JSON-compatible representation of this text block bounding-box result.
        """
        return {
            "block_name": self.block_name,
            "block_position_name": self.block_position_name,
            "bboxes": self.bboxes.to_dict(),
        }


@dataclass(slots=True)
class CellBBox:
    """Bounding-box output for a single table cell.

    Attributes
    ----------
    cell_name
        Cell identifier.
    cell_position_name
        Position label within the table.
    bboxes
        Extracted bounding boxes for the cell's text.
    """

    cell_name: str | None
    cell_position_name: str | None
    bboxes: TextBoundingBoxes

    def to_dict(self) -> dict[str, Any]:
        """Serialize to a JSON-compatible dict.

        Returns
        -------
        dict[str, Any]
            JSON-compatible representation of this cell bounding-box result.
        """
        return {
            "cell_name": self.cell_name,
            "cell_position_name": self.cell_position_name,
            "bboxes": self.bboxes.to_dict(),
        }


@dataclass(slots=True)
class TableBlockBBoxesResult:
    """Bounding-box output for a single table block.

    Attributes
    ----------
    block_name
        Block identifier.
    block_position_name
        Position label within the document.
    cell_bboxes
        Bounding-box results for each cell in the table.
    """

    block_name: str | None
    block_position_name: str | None
    cell_bboxes: list[CellBBox]

    def to_dict(self) -> dict[str, Any]:
        """Serialize to a JSON-compatible dict.

        Returns
        -------
        dict[str, Any]
            JSON-compatible representation of this table block bounding-box result.
        """
        return {
            "block_name": self.block_name,
            "block_position_name": self.block_position_name,
            "cell_bboxes": [cell.to_dict() for cell in self.cell_bboxes],
        }


@dataclass(slots=True)
class BlockBBox:
    """Named block with its bounding quadrilateral.

    Attributes
    ----------
    name
        Block identifier.
    bbox
        Bounding quadrilateral in user-space coordinates.
    """

    name: str | None
    bbox: Quadrilateral

    def to_dict(self) -> dict[str, Any]:
        """Serialize to a JSON-compatible dict.

        Returns
        -------
        dict[str, Any]
            JSON-compatible representation of this block bounding box.
        """
        return {
            "name": self.name,
            "bbox": self.bbox.to_dict(),
        }


@dataclass(slots=True)
class BlockBBoxesResult:
    """Bounding-box layout for a document surface.

    Attributes
    ----------
    surface_bbox
        Full surface bounding quadrilateral.
    content_bbox
        Content area bounding quadrilateral.
    block_bboxes
        Bounding boxes for each block on the surface.
    """

    surface_bbox: Quadrilateral
    content_bbox: Quadrilateral
    block_bboxes: list[BlockBBox]

    def to_dict(self) -> dict[str, Any]:
        """Serialize to a JSON-compatible dict.

        Returns
        -------
        dict[str, Any]
            JSON-compatible representation of this block bounding-box layout.
        """
        return {
            "surface_bbox": self.surface_bbox.to_dict(),
            "content_bbox": self.content_bbox.to_dict(),
            "block_bboxes": [b.to_dict() for b in self.block_bboxes],
        }
