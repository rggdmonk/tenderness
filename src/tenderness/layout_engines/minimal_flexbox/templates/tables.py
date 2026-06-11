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

    def table_basic(
        self,
        row_specs: list[float | None] | int,
        col_specs: list[float | None] | int,
        *,
        row_gap: float = 0.0,
        col_gap: float = 0.0,
        names: list[str] | None = None,
        caption: CaptionSpec | None = None,
    ) -> MinimalFlexNode:
        """Table with fixed-size or stretching rows and columns.

        ::

            row_specs = [40.0, None, 30.0]   col_specs = [80.0, None, 60.0]

            ┌──────┬──────────┬─────┐  ← 40
            ├──────┼──────────┼─────┤  ← stretch
            └──────┴──────────┴─────┘  ← 30
               80    stretch    60

            row_specs = 2   col_specs = 3   (uniform grid)

            ┌───────┬───────┬───────┐
            │       │       │       │  ← stretch
            ├───────┼───────┼───────┤
            │       │       │       │  ← stretch
            └───────┴───────┴───────┘

        Cell names default to ``cell_{r}_{c}`` in row-major order.

        Parameters
        ----------
        row_specs
            ``int`` → that many equal-stretch rows;
            ``list`` where ``float`` → fixed height, ``None`` → equal flex-grow share.
        col_specs
            ``int`` → that many equal-stretch columns;
            ``list`` where ``float`` → fixed width, ``None`` → equal flex-grow share.
        row_gap
            Gap between rows.
        col_gap
            Gap between columns.
        names
            Flat name list in row-major order; ``None`` uses generated defaults (``cell_{r}_{c}``).
        caption
            Optional caption strip to attach above or below the table.

        Returns
        -------
        MinimalFlexNode
            Root COLUMN container (or caption wrapper) for the complete table tree.
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

    def table_header_basic(
        self,
        row_specs: list[float | None] | int,
        col_specs: list[float | None] | int,
        header_height: float | None,
        *,
        header_gap: float = 0.0,
        row_gap: float = 0.0,
        col_gap: float = 0.0,
        names: list[str] | None = None,
        caption: CaptionSpec | None = None,
    ) -> MinimalFlexNode:
        """Table with a header row above a ``table_basic`` body.

        ``header_gap`` controls the gap between header and body;
        ``row_gap`` controls gaps between body rows only.

        ::

            ┌──────┬──────────┬──────┐
            │ hc_0 │   hc_1   │ hc_2 │  ← header_height
            ├──────┴──────────┴──────┤
            │       header_gap       │
            ├──────┬──────────┬──────┤
            │ c0_0 │  c0_1    │ c0_2 │  ← row_specs
            ├──────┼──────────┼──────┤
            │ c1_0 │  c1_1    │ c1_2 │  ← row_specs
            └──────┴──────────┴──────┘
               80    stretch    60    ← col_specs

        Header cells default to ``header_cell_{c}``; body cells to ``cell_{r}_{c}``.

        Parameters
        ----------
        row_specs
            ``int`` → that many equal-stretch body rows;
            ``list`` where ``float`` → fixed height, ``None`` → equal flex-grow share.
        col_specs
            ``int`` → that many equal-stretch columns;
            ``list`` where ``float`` → fixed width, ``None`` → equal flex-grow share.
        header_height
            Fixed height of the header row; ``None`` lets it stretch equally with the body.
        header_gap
            Gap between the header row and the body.
        row_gap
            Gap between body rows.
        col_gap
            Gap between columns.
        names
            Flat name list: header cells at indices ``0…n_cols-1``, body cells in row-major order
            starting at ``n_cols``; ``None`` uses generated defaults
            (``header_cell_{c}`` and ``cell_{r}_{c}``).
        caption
            Optional caption strip to attach above or below the table.

        Returns
        -------
        MinimalFlexNode
            Root COLUMN container (or caption wrapper) for the complete table tree.
        """
        cols: list[float | None] = [None] * col_specs if isinstance(col_specs, int) else col_specs
        stretch = FlexItemProperties(flex_grow=1.0, flex_shrink=1.0, flex_basis=0.0)
        row_props = FlexContainerProperties(direction=FlexDirection.ROW, col_gap=col_gap)

        header_cells = [
            MinimalFlexNode(
                item_props=(
                    stretch
                    if col_spec is None
                    else FlexItemProperties(flex_grow=0.0, flex_shrink=0.0, flex_basis=col_spec)
                ),
                name=self._add_name(names, c, f"header_cell_{c}"),
            )
            for c, col_spec in enumerate(cols)
        ]
        header_row = MinimalFlexNode(
            size=(0.0, header_height) if header_height is not None else (0.0, 0.0),
            item_props=FlexItemProperties(flex_grow=0.0, flex_shrink=0.0) if header_height is not None else stretch,
            container_props=row_props,
            children=header_cells,
        )

        n_cols = len(cols)
        body_names = names[n_cols:] if names is not None else None
        body_node = self.table_basic(
            row_specs=row_specs, col_specs=col_specs, row_gap=row_gap, col_gap=col_gap, names=body_names
        )
        body_node.item_props = stretch

        node = MinimalFlexNode(
            container_props=FlexContainerProperties(direction=FlexDirection.COLUMN, row_gap=header_gap),
            children=[header_row, body_node],
        )
        return self._wrap_with_caption(node, caption)
