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

"""MinimalFlexBox templates for document-style layouts."""

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


class MinimalFlexBoxTemplateDocuments(MinimalFlexBoxTemplateBase):
    """Layout templates for document structures with headers and sections."""

    def header_sectioned_columns(  # noqa: PLR0913
        self,
        header_height: float | None,
        section_label_height: list[float | None] | float | None,
        col_specs: list[float | None] | int,
        n_sections: int,
        *,
        section_content_height: list[float | None] | float | None = None,
        header_gap: float = 0.0,
        section_gap: float = 0.0,
        col_gap: float = 0.0,
        names: list[str] | None = None,
    ) -> MinimalFlexNode:
        """Build a layout with a fixed header and columns each containing *n_sections* label+content pairs.

        *col_specs*: ``int`` → that many equal-stretch columns;
        ``list`` where ``float`` → fixed pixel width, ``None`` → equal flex-grow share.

        ::

            ┌─────────────────────────────────┐
            │             header              │  ← header_height
            ├─────────────────────────────────┤  ↕ header_gap
            ├──────────────┬─┬────────────────┤
            │section_label │ │ section_label  │  ← section_label_height
            ├──────────────┤ ├────────────────┤  ↕ section_gap
            │   content    │ │    content     │  ← stretch
            ├──────────────┤ ├────────────────┤  ↕ section_gap
            │section_label │ │ section_label  │  ← section_label_height
            ├──────────────┤ ├────────────────┤  ↕ section_gap
            │   content    │ │    content     │  ← stretch
            └──────────────┴─┴────────────────┘
                            ↕ col_gap

        Flat name index: ``names[0]`` → header; for column *c* and section *s*:
        ``names[1 + c*n_sections*2 + s*2]`` → label,
        ``names[1 + c*n_sections*2 + s*2 + 1]`` → content.
        """
        root_props = FlexContainerProperties(direction=FlexDirection.COLUMN, row_gap=header_gap)
        body_props = FlexContainerProperties(direction=FlexDirection.ROW, col_gap=col_gap)
        col_props = FlexContainerProperties(direction=FlexDirection.COLUMN, row_gap=section_gap)

        stretch = FlexItemProperties(flex_grow=1.0, flex_shrink=1.0, flex_basis=0.0)
        header_item = FlexItemProperties(flex_grow=0.0, flex_shrink=0.0) if header_height is not None else stretch
        specs: list[float | None] = [None] * col_specs if isinstance(col_specs, int) else col_specs

        if isinstance(section_label_height, list):
            if len(section_label_height) != n_sections:
                msg = f"section_label_height list length ({len(section_label_height)}) must equal n_sections ({n_sections})."
                raise ValueError(msg)
            label_heights: list[float | None] = section_label_height
        else:
            label_heights = [section_label_height] * n_sections

        if isinstance(section_content_height, list):
            if len(section_content_height) != n_sections:
                msg = f"section_content_height list length ({len(section_content_height)}) must equal n_sections ({n_sections})."
                raise ValueError(msg)
            content_heights: list[float | None] = section_content_height
        else:
            content_heights = [section_content_height] * n_sections

        cols = []
        for c, col_spec in enumerate(specs):
            col_item = (
                FlexItemProperties(flex_grow=0.0, flex_shrink=0.0, flex_basis=col_spec)
                if col_spec is not None
                else stretch
            )
            sections = []
            for s in range(n_sections):
                label_idx = 1 + c * n_sections * 2 + s * 2
                content_idx = label_idx + 1
                label_h = label_heights[s]
                sections.append(
                    MinimalFlexNode(
                        size=(0.0, label_h) if label_h is not None else (0.0, 0.0),
                        item_props=FlexItemProperties(flex_grow=0.0, flex_shrink=0.0)
                        if label_h is not None
                        else stretch,
                        name=self._add_name(names, label_idx, f"col_{c}_section_{s}_label"),
                    )
                )
                content_h = content_heights[s]
                sections.append(
                    MinimalFlexNode(
                        size=(0.0, content_h) if content_h is not None else (0.0, 0.0),
                        item_props=FlexItemProperties(flex_grow=0.0, flex_shrink=0.0)
                        if content_h is not None
                        else stretch,
                        name=self._add_name(names, content_idx, f"col_{c}_section_{s}_content"),
                    )
                )
            cols.append(MinimalFlexNode(item_props=col_item, container_props=col_props, children=sections))

        return MinimalFlexNode(
            container_props=root_props,
            children=[
                MinimalFlexNode(
                    size=(0.0, header_height) if header_height is not None else (0.0, 0.0),
                    item_props=header_item,
                    name=self._add_name(names, 0, "header"),
                ),
                MinimalFlexNode(item_props=stretch, container_props=body_props, children=cols),
            ],
        )
