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

"""MinimalFlexBox templates for row and column flow layouts."""

from __future__ import annotations

from tenderness.layout_engines.minimal_flexbox.flex_container_properties import (
    FlexContainerProperties,
    FlexDirection,
)
from tenderness.layout_engines.minimal_flexbox.flex_item_properties import FlexItemProperties
from tenderness.layout_engines.minimal_flexbox.minimal_flexbox import MinimalFlexNode
from tenderness.layout_engines.minimal_flexbox.templates.base import (
    MinimalFlexBoxTemplateBase,
)


class MinimalFlexBoxTemplateFlow(MinimalFlexBoxTemplateBase):
    """Layout templates for horizontal column and vertical row flows."""

    def flow_columns(
        self,
        specs: list[float | None] | int,
        *,
        gap: float = 0.0,
        names: list[str] | None = None,
    ) -> MinimalFlexNode:
        """Horizontal flow of columns. Height stretches to fill the container.

        ::

            specs = [80.0, None, 60.0]      specs = 3

            ┌──────┬──────────┬─────┐       ┌───────┬───────┬───────┐
            │  80  │  stretch │  60 │       │ col_0 │ col_1 │ col_2 │
            └──────┴──────────┴─────┘       └───────┴───────┴───────┘

        Parameters
        ----------
        specs
            ``int`` → that many equal-stretch columns;
            ``list`` where ``float`` → fixed width, ``None`` → equal flex-grow share.
        gap
            Gap between columns.
        names
            Name list indexed left-to-right; ``None`` uses generated defaults (``col_0``, …).

        Returns
        -------
        MinimalFlexNode
            Root ROW container with one child node per column.
        """
        props = FlexContainerProperties(direction=FlexDirection.ROW, col_gap=gap)
        resolved: list[float | None] = [None] * specs if isinstance(specs, int) else specs

        children = [
            MinimalFlexNode(
                size=(s, 0.0) if s is not None else (0.0, 0.0),
                item_props=(
                    FlexItemProperties(flex_grow=0.0, flex_shrink=0.0)
                    if s is not None
                    else FlexItemProperties(flex_grow=1.0, flex_shrink=0.0)
                ),
                name=self._add_name(names, i, f"col_{i}"),
            )
            for i, s in enumerate(resolved)
        ]
        return MinimalFlexNode(container_props=props, children=children)

    def flow_rows(
        self,
        specs: list[float | None] | int,
        *,
        gap: float = 0.0,
        names: list[str] | None = None,
    ) -> MinimalFlexNode:
        """Vertical flow of rows. Width stretches to fill the container.

        ::

            specs = [40.0, None, 30.0]      specs = 3

            ┌───────────┐                   ┌───────────┐
            │    40     │                   │   row_0   │
            ├───────────┤                   ├───────────┤
            │  stretch  │                   │   row_1   │
            ├───────────┤                   ├───────────┤
            │    30     │                   │   row_2   │
            └───────────┘                   └───────────┘

        Parameters
        ----------
        specs
            ``int`` → that many equal-stretch rows;
            ``list`` where ``float`` → fixed height, ``None`` → equal flex-grow share.
        gap
            Gap between rows.
        names
            Name list indexed top-to-bottom; ``None`` uses generated defaults (``row_0``, …).

        Returns
        -------
        MinimalFlexNode
            Root COLUMN container with one child node per row.
        """
        props = FlexContainerProperties(direction=FlexDirection.COLUMN, row_gap=gap)
        resolved: list[float | None] = [None] * specs if isinstance(specs, int) else specs

        children = [
            MinimalFlexNode(
                size=(0.0, s) if s is not None else (0.0, 0.0),
                item_props=(
                    FlexItemProperties(flex_grow=0.0, flex_shrink=0.0)
                    if s is not None
                    else FlexItemProperties(flex_grow=1.0, flex_shrink=0.0)
                ),
                name=self._add_name(names, i, f"row_{i}"),
            )
            for i, s in enumerate(resolved)
        ]
        return MinimalFlexNode(container_props=props, children=children)
