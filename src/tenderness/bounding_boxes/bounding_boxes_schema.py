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

"""Text bounding box schema types and dataclasses."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum, auto, unique
from typing import TYPE_CHECKING, Any

import gi

gi.require_version("Pango", "1.0")

from tenderness.pango_backend.pango_enum_coerce import PangoEnumMap  # noqa: E402

if TYPE_CHECKING:
    from gi.repository import Pango

_DIRECTION_TO_STR: dict[Any, str] = {v: k for k, v in PangoEnumMap.Direction.items()}


@unique
class BoundingBoxType(StrEnum):
    """Granularity level of a bounding box.

    Attributes
    ----------
    CHAR
        Single character.
    CLUSTER
        Glyph cluster.
    LINE
        Layout line.
    RUN
        Text run within a line.
    LAYOUT
        Entire layout.
    """

    CHAR = auto()
    CLUSTER = auto()
    LINE = auto()
    RUN = auto()
    LAYOUT = auto()


@dataclass(slots=True)
class Quadrilateral:
    """Four corner points of a bounding rectangle mapped to user-space coordinates.

    Attributes
    ----------
    top_left
        Top-left corner as ``(x, y)``.
    top_right
        Top-right corner as ``(x, y)``.
    bottom_right
        Bottom-right corner as ``(x, y)``.
    bottom_left
        Bottom-left corner as ``(x, y)``.
    """

    top_left: tuple[float, float]
    top_right: tuple[float, float]
    bottom_right: tuple[float, float]
    bottom_left: tuple[float, float]

    def to_dict(self) -> dict[str, list[float]]:
        """Serialize to a JSON-compatible dict.

        Returns
        -------
        dict[str, list[float]]
            Each corner as a two-element ``[x, y]`` list.
        """
        return {
            "top_left": list(self.top_left),
            "top_right": list(self.top_right),
            "bottom_right": list(self.bottom_right),
            "bottom_left": list(self.bottom_left),
        }


@dataclass(slots=True, kw_only=True)
class BoundingBox:
    """Base bounding box with a logical extent.

    Attributes
    ----------
    logical_bbox
        Logical bounding quadrilateral in user-space coordinates.
    """

    logical_bbox: Quadrilateral


@dataclass(slots=True, kw_only=True)
class BoundingBoxWithInk(BoundingBox):
    """Bounding box with both logical and ink extents.

    Attributes
    ----------
    ink_bbox
        Ink bounding quadrilateral; tightly fits the rendered glyphs.
    """

    ink_bbox: Quadrilateral


@dataclass(slots=True, kw_only=True)
class CharBBox(BoundingBox):
    """Bounding box for a single character.

    Attributes
    ----------
    text
        The character string, or ``None`` if not available.
    byte_index
        Byte offset of the character in the source string.
    byte_length
        Byte length of the character in the source string, or ``None`` if not available.
    """

    text: str | None
    byte_index: int
    byte_length: int | None = None

    def to_dict(self) -> dict[str, Any]:
        """Serialize to a JSON-compatible dict.

        Returns
        -------
        dict[str, Any]
            JSON-compatible representation of this character bounding box.
        """
        return {
            "logical_bbox": self.logical_bbox.to_dict(),
            "text": self.text,
            "byte_index": self.byte_index,
            "byte_length": self.byte_length,
        }


@dataclass(slots=True, kw_only=True)
class ClusterBBox(BoundingBoxWithInk):
    """Bounding box for a glyph cluster.

    Attributes
    ----------
    text
        Source text for the cluster, or ``None`` if not available.
    byte_index
        Byte offset of the cluster in the source string.
    byte_length
        Byte length of the cluster in the source string.
    """

    text: str | None
    byte_index: int
    byte_length: int

    def to_dict(self) -> dict[str, Any]:
        """Serialize to a JSON-compatible dict.

        Returns
        -------
        dict[str, Any]
            JSON-compatible representation of this cluster bounding box.
        """
        return {
            "logical_bbox": self.logical_bbox.to_dict(),
            "ink_bbox": self.ink_bbox.to_dict(),
            "text": self.text,
            "byte_index": self.byte_index,
            "byte_length": self.byte_length,
        }


@dataclass(slots=True, kw_only=True)
class RunBBox(BoundingBoxWithInk):
    """Bounding box for a text run within a line.

    Attributes
    ----------
    text
        Source text for the run, or ``None`` if not available.
    byte_index
        Byte offset of the run start in the source string.
    byte_length
        Byte length of the run in the source string.
    baseline
        Baseline y-coordinate in user space.
    """

    text: str | None
    byte_index: int
    byte_length: int
    baseline: float

    def to_dict(self) -> dict[str, Any]:
        """Serialize to a JSON-compatible dict.

        Returns
        -------
        dict[str, Any]
            JSON-compatible representation of this run bounding box.
        """
        return {
            "logical_bbox": self.logical_bbox.to_dict(),
            "ink_bbox": self.ink_bbox.to_dict(),
            "text": self.text,
            "byte_index": self.byte_index,
            "byte_length": self.byte_length,
            "baseline": self.baseline,
        }


@dataclass(slots=True, kw_only=True)
class LineBBox(BoundingBoxWithInk):
    """Bounding box for a layout line.

    Attributes
    ----------
    text
        Source text for the line, or ``None`` if not available.
    byte_index
        Byte offset of the line start in the source string.
    byte_length
        Byte length of the line in the source string.
    resolved_direction
        Resolved text direction for the line.
    is_paragraph_start
        ``True`` if this line starts a new paragraph.
    baseline
        Baseline y-coordinate in user space.
    """

    text: str | None
    byte_index: int
    byte_length: int
    resolved_direction: Pango.Direction
    is_paragraph_start: bool
    baseline: float

    def to_dict(self) -> dict[str, Any]:
        """Serialize to a JSON-compatible dict.

        ``resolved_direction`` is converted to its lowercase nick string
        (e.g. ``"ltr"``, ``"rtl"``) using ``PangoEnumMap.Direction``.

        Returns
        -------
        dict[str, Any]
            JSON-compatible representation of this line bounding box.
        """
        return {
            "logical_bbox": self.logical_bbox.to_dict(),
            "ink_bbox": self.ink_bbox.to_dict(),
            "text": self.text,
            "byte_index": self.byte_index,
            "byte_length": self.byte_length,
            "resolved_direction": _DIRECTION_TO_STR[self.resolved_direction],
            "is_paragraph_start": self.is_paragraph_start,
            "baseline": self.baseline,
        }


@dataclass(slots=True, kw_only=True)
class LayoutBBox(BoundingBoxWithInk):
    """Bounding box for an entire layout.

    Attributes
    ----------
    text
        Full source text of the layout, or ``None`` if not available.
    """

    text: str | None

    def to_dict(self) -> dict[str, Any]:
        """Serialize to a JSON-compatible dict.

        Returns
        -------
        dict[str, Any]
            JSON-compatible representation of this layout bounding box.
        """
        return {
            "logical_bbox": self.logical_bbox.to_dict(),
            "ink_bbox": self.ink_bbox.to_dict(),
            "text": self.text,
        }


@dataclass(slots=True)
class TextBoundingBoxes:
    """Container for all bounding box levels extracted from a layout.

    Attributes
    ----------
    char_bboxes
        Per-character bounding boxes, or ``None`` if not requested.
    cluster_bboxes
        Per-cluster bounding boxes, or ``None`` if not requested.
    run_bboxes
        Per-run bounding boxes, or ``None`` if not requested.
    line_bboxes
        Per-line bounding boxes, or ``None`` if not requested.
    layout_bbox
        Whole-layout bounding box, or ``None`` if not requested.
    """

    char_bboxes: list[CharBBox] | None = None
    cluster_bboxes: list[ClusterBBox] | None = None
    run_bboxes: list[RunBBox] | None = None
    line_bboxes: list[LineBBox] | None = None
    layout_bbox: LayoutBBox | None = None

    def to_dict(self) -> dict[str, Any]:
        """Serialize to a JSON-compatible dict.

        Returns
        -------
        dict[str, Any]
            JSON-compatible representation of all bounding box levels.
            List fields are ``None`` when the level was not requested.
        """
        return {
            "char_bboxes": [b.to_dict() for b in self.char_bboxes] if self.char_bboxes is not None else None,
            "cluster_bboxes": [b.to_dict() for b in self.cluster_bboxes] if self.cluster_bboxes is not None else None,
            "run_bboxes": [b.to_dict() for b in self.run_bboxes] if self.run_bboxes is not None else None,
            "line_bboxes": [b.to_dict() for b in self.line_bboxes] if self.line_bboxes is not None else None,
            "layout_bbox": self.layout_bbox.to_dict() if self.layout_bbox is not None else None,
        }
