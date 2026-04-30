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

"""Flex item property types for MinimalFlexBox layout."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum, auto, unique


@unique
class AlignSelf(StrEnum):
    """Per-item cross-axis alignment override."""

    AUTO = auto()  # default — inherits align-items from the container
    STRETCH = auto()  # fills the line's cross size; use FLEX_START/CENTER to preserve intrinsic aspect ratio
    FLEX_START = auto()
    FLEX_END = auto()
    CENTER = auto()

    # BASELINE = auto()


@dataclass(slots=True)
class FlexItemProperties:
    """Per-item flex properties for MinimalFlexBox layout.

    Parameters
    ----------
    order
        Render order; lower values appear first.
    flex_grow
        Growth factor relative to other items; 0 disables growth.
    flex_shrink
        Shrink factor relative to other items; 0 disables shrinkage.
    flex_basis
        Override for the initial main-axis size; ``None`` uses the intrinsic size.
    align_self
        Cross-axis alignment override; ``AUTO`` inherits from the container.
    """

    order: int = field(default=0)
    flex_grow: float = field(default=0.0)  # non-negative
    flex_shrink: float = field(default=1.0)  # non-negative
    flex_basis: float | None = field(default=None)  # None = "auto" (use intrinsic size); 0.0 = ignore intrinsic
    align_self: AlignSelf = field(default=AlignSelf.AUTO)
