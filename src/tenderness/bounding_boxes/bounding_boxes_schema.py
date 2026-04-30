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

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum, auto, unique
from typing import TYPE_CHECKING

import gi

gi.require_version("Pango", "1.0")

if TYPE_CHECKING:
    from gi.repository import Pango


@unique
class BoundingBoxType(StrEnum):  # noqa: D101 TODO: docstring
    CHAR = auto()
    CLUSTER = auto()
    LINE = auto()
    RUN = auto()
    LAYOUT = auto()


@unique
class BoundingBoxStrategy(StrEnum):  # noqa: D101 TODO: docstring
    ONLY_BOXES = auto()
    WITH_TEXT = auto()


@dataclass(slots=True)
class Tetragon:  # noqa: D101 TODO: docstring
    top_left: tuple[float, float]
    top_right: tuple[float, float]
    bottom_right: tuple[float, float]
    bottom_left: tuple[float, float]


@dataclass(slots=True, kw_only=True)
class BoundingBox:  # noqa: D101 TODO: docstring
    logical_bbox: Tetragon


@dataclass(slots=True, kw_only=True)
class BoundingBoxWithInk(BoundingBox):  # noqa: D101 TODO: docstring
    ink_bbox: Tetragon


@dataclass(slots=True, kw_only=True)
class CharBBox(BoundingBox):  # noqa: D101 TODO: docstring
    char: str | None
    byte_index: int


@dataclass(slots=True, kw_only=True)
class ClusterBBox(BoundingBoxWithInk):  # noqa: D101 TODO: docstring
    text: str | None
    byte_index: int


@dataclass(slots=True, kw_only=True)
class RunBBox(BoundingBoxWithInk):  # noqa: D101 TODO: docstring
    text: str | None
    byte_start: int
    byte_length: int
    baseline: float


@dataclass(slots=True, kw_only=True)
class LineBBox(BoundingBoxWithInk):  # noqa: D101 TODO: docstring
    text: str | None
    byte_start: int
    byte_length: int
    resolved_direction: Pango.Direction
    is_paragraph_start: bool
    baseline: float


@dataclass(slots=True, kw_only=True)
class LayoutBBox(BoundingBoxWithInk):  # noqa: D101 TODO: docstring
    text: str | None


@dataclass(slots=True)
class LayoutBBoxCollection:  # noqa: D101 TODO: docstring
    position_name: str | None = None
    block_name: str | None = None
    table_name: str | None = None
    cell_name: str | None = None
    char_boxes: list[CharBBox] | None = None
    cluster_boxes: list[ClusterBBox] | None = None
    run_boxes: list[RunBBox] | None = None
    line_boxes: list[LineBBox] | None = None
    layout_box: LayoutBBox | None = None
