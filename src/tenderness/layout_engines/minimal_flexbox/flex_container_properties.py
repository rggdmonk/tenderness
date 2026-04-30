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
    """Main-axis direction for a flex container."""

    ROW = auto()  # default
    COLUMN = auto()
    ROW_REVERSE = auto()
    COLUMN_REVERSE = auto()


@unique
class FlexWrap(StrEnum):
    """Line-wrapping behavior for a flex container."""

    NOWRAP = auto()  # default
    WRAP = auto()
    WRAP_REVERSE = auto()


@unique
class JustifyContent(StrEnum):
    """Main-axis item distribution for a flex container."""

    FLEX_START = auto()  # default
    FLEX_END = auto()

    CENTER = auto()

    SPACE_BETWEEN = auto()
    SPACE_AROUND = auto()
    SPACE_EVENLY = auto()


@unique
class AlignItems(StrEnum):
    """Default cross-axis item alignment for a flex container."""

    STRETCH = auto()  # default
    FLEX_START = auto()
    FLEX_END = auto()
    CENTER = auto()

    # BASELINE = auto()


@unique
class AlignContent(StrEnum):
    """Cross-axis line distribution when wrapping is enabled."""

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

    Parameters
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
        Minimum gap between rows in device units.
    col_gap
        Minimum gap between columns in device units.
    """

    direction: FlexDirection = field(default=FlexDirection.ROW)
    wrap: FlexWrap = field(default=FlexWrap.NOWRAP)
    justify_content: JustifyContent = field(default=JustifyContent.FLEX_START)
    align_items: AlignItems = field(default=AlignItems.STRETCH)
    align_content: AlignContent = field(default=AlignContent.NORMAL)
    row_gap: float = field(default=0.0)
    col_gap: float = field(default=0.0)
