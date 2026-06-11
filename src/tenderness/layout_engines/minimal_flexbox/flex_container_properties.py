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

"""Flex container property types for MinimalFlexBox layout."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum, auto, unique


@unique
class FlexDirection(StrEnum):
    """Main-axis direction for a flex container.

    Attributes
    ----------
    ROW
        Left to right along the horizontal axis (default).
    COLUMN
        Top to bottom along the vertical axis.
    ROW_REVERSE
        Right to left along the horizontal axis.
    COLUMN_REVERSE
        Bottom to top along the vertical axis.
    """

    ROW = auto()  # default
    COLUMN = auto()
    ROW_REVERSE = auto()
    COLUMN_REVERSE = auto()


@unique
class FlexWrap(StrEnum):
    """Line-wrapping behavior for a flex container.

    Attributes
    ----------
    NOWRAP
        All items are placed on a single line (default).
    WRAP
        Items wrap onto additional lines in the cross-axis direction.
    WRAP_REVERSE
        Items wrap onto additional lines in the reverse cross-axis direction.
    """

    NOWRAP = auto()  # default
    WRAP = auto()
    WRAP_REVERSE = auto()


@unique
class JustifyContent(StrEnum):
    """Main-axis item distribution for a flex container.

    Attributes
    ----------
    FLEX_START
        Items are packed toward the main-start edge (default).
    FLEX_END
        Items are packed toward the main-end edge.
    CENTER
        Items are centered along the main axis.
    SPACE_BETWEEN
        Items are evenly distributed; first item at start, last at end.
    SPACE_AROUND
        Items are evenly distributed with equal space on both sides of each item.
    SPACE_EVENLY
        Items are evenly distributed with equal space between and around all items.
    """

    FLEX_START = auto()  # default
    FLEX_END = auto()

    CENTER = auto()

    SPACE_BETWEEN = auto()
    SPACE_AROUND = auto()
    SPACE_EVENLY = auto()


@unique
class AlignItems(StrEnum):
    """Default cross-axis item alignment for a flex container.

    Attributes
    ----------
    STRETCH
        Items are stretched to fill the line's cross size (default).
    FLEX_START
        Items are aligned to the cross-start edge of the line.
    FLEX_END
        Items are aligned to the cross-end edge of the line.
    CENTER
        Items are centered within the line's cross size.
    """

    STRETCH = auto()  # default
    FLEX_START = auto()
    FLEX_END = auto()
    CENTER = auto()

    # BASELINE = auto()


@unique
class AlignContent(StrEnum):
    """Cross-axis line distribution when wrapping is enabled.

    Attributes
    ----------
    NORMAL
        Acts like ``STRETCH`` for multi-line containers and ``FLEX_START`` for single-line (default).
    FLEX_START
        Lines are packed toward the cross-start edge.
    FLEX_END
        Lines are packed toward the cross-end edge.
    CENTER
        Lines are centered along the cross axis.
    SPACE_BETWEEN
        Lines are evenly distributed; first line at start, last at end.
    SPACE_AROUND
        Lines are evenly distributed with equal space on both sides of each line.
    SPACE_EVENLY
        Lines are evenly distributed with equal space between and around all lines.
    STRETCH
        Lines are stretched to fill the remaining cross space.
    """

    NORMAL = auto()  # default — acts like STRETCH for multi-line, FLEX_START for single-line
    FLEX_START = auto()
    FLEX_END = auto()
    CENTER = auto()
    SPACE_BETWEEN = auto()
    SPACE_AROUND = auto()
    SPACE_EVENLY = auto()
    STRETCH = auto()


@dataclass(slots=True)
class FlexContainerProperties:
    """Container-level flex layout properties for MinimalFlexBox.

    Attributes
    ----------
    direction
        Main-axis direction.
    wrap
        Line-wrapping behavior.
    justify_content
        Main-axis item distribution.
    align_items
        Default cross-axis item alignment.
    align_content
        Cross-axis line distribution; applies only when wrapping produces multiple lines.
    row_gap
        Minimum gap between rows.
    col_gap
        Minimum gap between columns.
    """

    direction: FlexDirection = field(default=FlexDirection.ROW)
    wrap: FlexWrap = field(default=FlexWrap.NOWRAP)
    justify_content: JustifyContent = field(default=JustifyContent.FLEX_START)
    align_items: AlignItems = field(default=AlignItems.STRETCH)
    align_content: AlignContent = field(default=AlignContent.NORMAL)
    row_gap: float = field(default=0.0)
    col_gap: float = field(default=0.0)
