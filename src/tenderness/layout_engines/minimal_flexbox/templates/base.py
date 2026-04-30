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

"""Base class and shared types for MinimalFlexBox layout templates."""

from __future__ import annotations

from dataclasses import dataclass, field

from tenderness.layout_engines.minimal_flexbox.flex_container_properties import (
    FlexContainerProperties,
    FlexDirection,
)
from tenderness.layout_engines.minimal_flexbox.flex_item_properties import FlexItemProperties
from tenderness.layout_engines.minimal_flexbox.minimal_flexbox import MinimalFlexNode


@dataclass(slots=True)
class CaptionSpec:
    """Caption strip to attach above or below a layout node.

    Args:
        height:   Fixed pixel height of the caption strip.
        gap:      Gap between the layout node and the caption strip.
        on_top:   If True the caption appears above the layout; otherwise below.
        name:     Name assigned to the caption leaf node.
    """

    height: float | None
    gap: float = field(default=0.0)
    on_top: bool = field(default=False)
    name: str = field(default="caption")


class MinimalFlexBoxTemplateBase:
    """Shared helpers for MinimalFlexBox template classes."""

    def _add_name(self, names: list[str] | None, index: int, default: str) -> str:
        return names[index] if names is not None else default

    def _wrap_with_caption(self, node: MinimalFlexNode, caption: CaptionSpec | None) -> MinimalFlexNode:
        """Wrap *node* in a COLUMN container with a fixed-height caption strip.

        The wrapped node is made to stretch (flex_grow=1) so it fills the space not taken
        by the caption. When *caption* is None the original node is returned unchanged.
        """
        if caption is None:
            return node
        node.item_props = FlexItemProperties(flex_grow=1.0, flex_shrink=1.0, flex_basis=0.0)
        caption_node = MinimalFlexNode(
            size=(0.0, caption.height) if caption.height is not None else (0.0, 0.0),
            item_props=(
                FlexItemProperties(flex_grow=0.0, flex_shrink=0.0)
                if caption.height is not None
                else FlexItemProperties(flex_grow=1.0, flex_shrink=1.0, flex_basis=0.0)
            ),
            name=caption.name,
        )
        children = [caption_node, node] if caption.on_top else [node, caption_node]
        return MinimalFlexNode(
            container_props=FlexContainerProperties(direction=FlexDirection.COLUMN, row_gap=caption.gap),
            children=children,
        )
