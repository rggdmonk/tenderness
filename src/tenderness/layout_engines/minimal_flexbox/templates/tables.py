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

"""MinimalFlexBox templates for table layouts."""

from __future__ import annotations

from tenderness.layout_engines.minimal_flexbox.flex_container_properties import (
    FlexContainerProperties,
    FlexDirection,
)
from tenderness.layout_engines.minimal_flexbox.flex_item_properties import FlexItemProperties
from tenderness.layout_engines.minimal_flexbox.minimal_flexbox import MinimalFlexNode
from tenderness.layout_engines.minimal_flexbox.templates.base import (
    CaptionSpec,
    MinimalFlexBoxTemplateBase,
)


class MinimalFlexBoxTemplateTables(MinimalFlexBoxTemplateBase):
    """Layout templates for grid and table structures."""

    def table_custom(
        self,
        row_specs: list[float | None] | int,
        col_specs: list[float | None] | int,
        *,
        row_gap: float = 0.0,
        col_gap: float = 0.0,
        names: list[str] | None = None,
        caption: CaptionSpec | None = None,
    ) -> MinimalFlexNode:
        """General-purpose table where each row and column is fixed-size or stretching.

        *row_specs*: ``int`` → that many equal-stretch rows;
        ``list`` where ``float`` → fixed pixel height, ``None`` → equal flex-grow share.

        *col_specs*: ``int`` → that many equal-stretch columns;
        ``list`` where ``float`` → fixed pixel width via ``flex_basis``, ``None`` → equal flex-grow share.

        ::

            row_specs = [40.0, None, 30.0]   col_specs = [80.0, None, 60.0]

            ┌──────┬──────────┬─────┐  ← 40px
            ├──────┼──────────┼─────┤  ← stretch
            └──────┴──────────┴─────┘  ← 30px
              80px   stretch    60px

            row_specs = 2   col_specs = 3   (uniform grid)

            ┌───────┬───────┬───────┐
            │       │       │       │  ← stretch
            ├───────┼───────┼───────┤
            │       │       │       │  ← stretch
            └───────┴───────┴───────┘

        Returns ``len(row_specs) * len(col_specs)`` rectangles in row-major order.
        When *caption* is set, one additional rectangle is included for the caption strip.
        """
        rows: list[float | None] = [None] * row_specs if isinstance(row_specs, int) else row_specs
        cols: list[float | None] = [None] * col_specs if isinstance(col_specs, int) else col_specs

        root_props = FlexContainerProperties(direction=FlexDirection.COLUMN, row_gap=row_gap)
        row_props = FlexContainerProperties(direction=FlexDirection.ROW, col_gap=col_gap)
        n_cols = len(cols)

        children = []
        for r, row_spec in enumerate(rows):
            cells = [
                MinimalFlexNode(
                    item_props=(
                        FlexItemProperties(flex_grow=1.0, flex_shrink=1.0, flex_basis=0.0)
                        if col_spec is None
                        else FlexItemProperties(flex_grow=0.0, flex_shrink=0.0, flex_basis=col_spec)
                    ),
                    name=self._add_name(names, r * n_cols + c, f"cell_{r}_{c}"),
                )
                for c, col_spec in enumerate(cols)
            ]
            children.append(
                MinimalFlexNode(
                    size=(0.0, row_spec) if row_spec is not None else (0.0, 0.0),
                    item_props=(
                        FlexItemProperties(flex_grow=0.0, flex_shrink=0.0)
                        if row_spec is not None
                        else FlexItemProperties(flex_grow=1.0, flex_shrink=1.0, flex_basis=0.0)
                    ),
                    container_props=row_props,
                    children=cells,
                )
            )

        node = MinimalFlexNode(container_props=root_props, children=children)
        return self._wrap_with_caption(node, caption)

    def table_header_body(
        self,
        body_rows: int,
        cols: int,
        header_height: float | None,
        *,
        row_gap: float = 0.0,
        col_gap: float = 0.0,
        names: list[str] | None = None,
        caption: CaptionSpec | None = None,
    ) -> MinimalFlexNode:
        """Fixed-height header row + N equal-stretch body rows, all with the same column count.

        ::

            ┌──────┬──────┬──────┐
            │ hdr0 │ hdr1 │ hdr2 │  ← fixed height
            ╞══════╪══════╪══════╡
            │ b0_0 │ b0_1 │ b0_2 │  ─┐
            ├──────┼──────┼──────┤   ├ equal stretch
            │ b1_0 │ b1_1 │ b1_2 │  ─┘
            └──────┴──────┴──────┘

        Names: header cells at indices 0…cols-1, body cells in row-major order at
        indices cols…(1 + body_rows) * cols - 1.
        Returns ``(1 + body_rows) * cols`` rectangles.
        When *caption* is set, one additional rectangle is included for the caption strip.
        """
        root_props = FlexContainerProperties(direction=FlexDirection.COLUMN, row_gap=row_gap)
        row_props = FlexContainerProperties(direction=FlexDirection.ROW, col_gap=col_gap)

        stretch_col = FlexItemProperties(flex_grow=1.0, flex_shrink=1.0, flex_basis=0.0)
        stretch_row = FlexItemProperties(flex_grow=1.0, flex_shrink=1.0, flex_basis=0.0)

        header_cells = [
            MinimalFlexNode(
                item_props=stretch_col,
                name=self._add_name(names, c, f"header_{c}"),
            )
            for c in range(cols)
        ]
        header_row = MinimalFlexNode(
            size=(0.0, header_height) if header_height is not None else (0.0, 0.0),
            item_props=(
                FlexItemProperties(flex_grow=0.0, flex_shrink=0.0) if header_height is not None else stretch_row
            ),
            container_props=row_props,
            children=header_cells,
        )

        body_row_nodes = []
        for r in range(body_rows):
            cells = [
                MinimalFlexNode(
                    item_props=stretch_col,
                    name=self._add_name(names, cols + r * cols + c, f"body_{r}_{c}"),
                )
                for c in range(cols)
            ]
            body_row_nodes.append(
                MinimalFlexNode(
                    item_props=stretch_row,
                    container_props=row_props,
                    children=cells,
                )
            )

        node = MinimalFlexNode(container_props=root_props, children=[header_row, *body_row_nodes])
        return self._wrap_with_caption(node, caption)
