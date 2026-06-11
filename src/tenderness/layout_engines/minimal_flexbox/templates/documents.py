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

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def header_labeled_sections(  # noqa: PLR0913
        self,
        header_height: float | None,
        section_label_height: list[float | None] | float | None,
        col_specs: list[float | None] | int,
        n_sections: int,
        *,
        section_content_height: list[float | None] | float | None = None,
        header_gap: float = 0.0,
        section_gap: list[float] | float = 0.0,
        label_content_gap: list[float] | float = 0.0,
        col_gap: float = 0.0,
        names: list[str] | None = None,
    ) -> MinimalFlexNode:
        """Build a layout with a header and columns each containing n_sections label+content pairs.

        Each section is a nested COLUMN container so ``label_content_gap`` (within a
        section) and ``section_gap`` (between sections) can differ independently.
        ``label_content_gap`` accepts a list of length ``n_sections``; ``section_gap``
        accepts a list of length ``n_sections - 1``.

        ::

            ┌─────────────────────────────────┐
            │             header              │  ← header_height
            ├─────────────────────────────────┤
            │            header_gap           │
            ├──────────────┬──┬───────────────┤
            │  label_1_1   │  │   label_2_1   │  ← section_label_height
            ├──────────────┤  ├───────────────┤
            │lbl_cont_gap  │  │ lbl_cont_gap  │
            ├──────────────┤  ├───────────────┤
            │ content_1_1  │  │  content_2_1  │  ← section_content_height
            ├──────────────┤  ├───────────────┤
            │ section_gap  │  │  section_gap  │
            ├──────────────┤  ├───────────────┤
            │  label_1_2   │  │   label_2_2   │  ← section_label_height
            ├──────────────┤  ├───────────────┤
            │lbl_cont_gap  │  │ lbl_cont_gap  │
            ├──────────────┤  ├───────────────┤
            │ content_1_2  │  │  content_2_2  │  ← section_content_height
            └──────────────┴──┴───────────────┘
                            ↔ col_gap

        Indices follow ``c_s`` (column, section): ``label_1_2`` is column 1, section 2.

        Flat name index: ``names[0]`` → header; for column *c* and section *s*:
        ``names[1 + c*n_sections*2 + s*2]`` → label,
        ``names[1 + c*n_sections*2 + s*2 + 1]`` → content.

        Parameters
        ----------
        header_height
            Fixed height of the header strip; ``None`` lets it stretch.
        section_label_height
            Fixed height(s) for section label rows; ``None`` entries stretch.
            Pass a single value to apply to all sections, or a list of length ``n_sections``.
        col_specs
            ``int`` → that many equal-stretch columns;
            ``list`` where ``float`` → fixed width, ``None`` → equal flex-grow share.
        n_sections
            Number of label+content section pairs per column.
        section_content_height
            Fixed height(s) for section content rows; ``None`` entries stretch.
            Pass a single value to apply to all sections, or a list of length ``n_sections``.
        header_gap
            Gap between the header and the body.
        section_gap
            Gap between consecutive sections (content → next label).
            Pass a single value for a uniform gap, or a list of length ``n_sections - 1``
            for per-gap control.
        label_content_gap
            Gap within each section between label and content.
            Pass a single value for a uniform gap, or a list of length ``n_sections``
            for per-section control.
        col_gap
            Gap between columns.
        names
            Flat list of node names in index order; ``None`` uses generated defaults.

        Returns
        -------
        MinimalFlexNode
            Root container node for the complete layout tree.
        """
        stretch = FlexItemProperties(flex_grow=1.0, flex_shrink=1.0, flex_basis=0.0)
        specs: list[float | None] = [None] * col_specs if isinstance(col_specs, int) else col_specs

        label_heights = self._resolve_heights(section_label_height, n_sections, "section_label_height")
        content_heights = self._resolve_heights(section_content_height, n_sections, "section_content_height")
        uniform_section_gap, section_gaps = self._resolve_section_gap(section_gap, n_sections)
        label_content_gaps = self._resolve_gap_list(label_content_gap, n_sections, "label_content_gap")

        root_props = FlexContainerProperties(direction=FlexDirection.COLUMN, row_gap=header_gap)
        body_props = FlexContainerProperties(direction=FlexDirection.ROW, col_gap=col_gap)
        col_props = FlexContainerProperties(direction=FlexDirection.COLUMN, row_gap=uniform_section_gap)

        cols = []
        for c, col_spec in enumerate(specs):
            col_item = (
                FlexItemProperties(flex_grow=0.0, flex_shrink=0.0, flex_basis=col_spec)
                if col_spec is not None
                else stretch
            )
            sections: list[MinimalFlexNode] = []
            for s in range(n_sections):
                label_idx = 1 + c * n_sections * 2 + s * 2
                label_h, content_h, lc_gap = label_heights[s], content_heights[s], label_content_gaps[s]
                label_node = self._build_leaf(
                    label_h, self._add_name(names, label_idx, f"col_{c}_section_{s}_label"), stretch
                )
                content_node = self._build_leaf(
                    content_h, self._add_name(names, label_idx + 1, f"col_{c}_section_{s}_content"), stretch
                )
                sections.append(self._build_section(label_node, content_node, label_h, content_h, lc_gap, stretch))
                if section_gaps is not None and s < n_sections - 1:
                    sections.append(
                        MinimalFlexNode(
                            size=(0.0, section_gaps[s]), item_props=FlexItemProperties(flex_grow=0.0, flex_shrink=0.0)
                        )
                    )
            cols.append(MinimalFlexNode(item_props=col_item, container_props=col_props, children=sections))

        header_node = self._build_leaf(header_height, self._add_name(names, 0, "header"), stretch)
        return MinimalFlexNode(
            container_props=root_props,
            children=[header_node, MinimalFlexNode(item_props=stretch, container_props=body_props, children=cols)],
        )

    def header_sections(
        self,
        header_height: float | None,
        col_specs: list[float | None] | int,
        n_sections: int,
        *,
        section_content_height: list[float | None] | float | None = None,
        header_gap: float = 0.0,
        section_gap: list[float] | float = 0.0,
        col_gap: float = 0.0,
        names: list[str] | None = None,
    ) -> MinimalFlexNode:
        """Build a layout with a header and columns each containing n_sections content strips.

        Like ``header_labeled_sections`` but without label rows inside each section.

        ::

            ┌─────────────────────────────────┐
            │             header              │  ← header_height
            ├─────────────────────────────────┤
            │            header_gap           │
            ├──────────────┬──┬───────────────┤
            │ content_1_1  │  │  content_2_1  │  ← section_content_height
            ├──────────────┤  ├───────────────┤
            │ section_gap  │  │  section_gap  │
            ├──────────────┤  ├───────────────┤
            │ content_1_2  │  │  content_2_2  │  ← section_content_height
            └──────────────┴──┴───────────────┘
                            ↔ col_gap

        Indices follow ``c_s`` (column, section): ``content_1_2`` is column 1, section 2.

        Flat name index: ``names[0]`` → header; for column *c* and section *s*:
        ``names[1 + c*n_sections + s]`` → content.

        Parameters
        ----------
        header_height
            Fixed height of the header strip; ``None`` lets it stretch.
        col_specs
            ``int`` → that many equal-stretch columns;
            ``list`` where ``float`` → fixed width, ``None`` → equal flex-grow share.
        n_sections
            Number of content strips per column.
        section_content_height
            Fixed height(s) for section content rows; ``None`` entries stretch.
            Pass a single value to apply to all sections, or a list of length ``n_sections``.
        header_gap
            Gap between the header and the body.
        section_gap
            Gap between consecutive sections.
            Pass a single value for a uniform gap, or a list of length ``n_sections - 1``
            for per-gap control.
        col_gap
            Gap between columns.
        names
            Flat list of node names in index order; ``None`` uses generated defaults.

        Returns
        -------
        MinimalFlexNode
            Root container node for the complete layout tree.
        """
        stretch = FlexItemProperties(flex_grow=1.0, flex_shrink=1.0, flex_basis=0.0)
        specs: list[float | None] = [None] * col_specs if isinstance(col_specs, int) else col_specs

        content_heights = self._resolve_heights(section_content_height, n_sections, "section_content_height")
        uniform_section_gap, section_gaps = self._resolve_section_gap(section_gap, n_sections)

        root_props = FlexContainerProperties(direction=FlexDirection.COLUMN, row_gap=header_gap)
        body_props = FlexContainerProperties(direction=FlexDirection.ROW, col_gap=col_gap)
        col_props = FlexContainerProperties(direction=FlexDirection.COLUMN, row_gap=uniform_section_gap)

        cols = []
        for c, col_spec in enumerate(specs):
            col_item = (
                FlexItemProperties(flex_grow=0.0, flex_shrink=0.0, flex_basis=col_spec)
                if col_spec is not None
                else stretch
            )
            sections: list[MinimalFlexNode] = []
            for s in range(n_sections):
                content_idx = 1 + c * n_sections + s
                content_node = self._build_leaf(
                    content_heights[s],
                    self._add_name(names, content_idx, f"col_{c}_section_{s}"),
                    stretch,
                )
                sections.append(content_node)
                if section_gaps is not None and s < n_sections - 1:
                    sections.append(
                        MinimalFlexNode(
                            size=(0.0, section_gaps[s]),
                            item_props=FlexItemProperties(flex_grow=0.0, flex_shrink=0.0),
                        )
                    )
            cols.append(MinimalFlexNode(item_props=col_item, container_props=col_props, children=sections))

        header_node = self._build_leaf(header_height, self._add_name(names, 0, "header"), stretch)
        return MinimalFlexNode(
            container_props=root_props,
            children=[header_node, MinimalFlexNode(item_props=stretch, container_props=body_props, children=cols)],
        )

    def labeled_sections(
        self,
        section_label_height: list[float | None] | float | None,
        col_specs: list[float | None] | int,
        n_sections: int,
        *,
        section_content_height: list[float | None] | float | None = None,
        section_gap: list[float] | float = 0.0,
        label_content_gap: list[float] | float = 0.0,
        col_gap: float = 0.0,
        names: list[str] | None = None,
    ) -> MinimalFlexNode:
        """Build a layout with columns each containing n_sections label+content pairs.

        Like ``header_labeled_sections`` but without the top header strip.

        ::

            ┌──────────────┬──┬───────────────┐
            │  label_1_1   │  │   label_2_1   │  ← section_label_height
            ├──────────────┤  ├───────────────┤
            │lbl_cont_gap  │  │ lbl_cont_gap  │
            ├──────────────┤  ├───────────────┤
            │ content_1_1  │  │  content_2_1  │  ← section_content_height
            ├──────────────┤  ├───────────────┤
            │ section_gap  │  │  section_gap  │
            ├──────────────┤  ├───────────────┤
            │  label_1_2   │  │   label_2_2   │  ← section_label_height
            ├──────────────┤  ├───────────────┤
            │lbl_cont_gap  │  │ lbl_cont_gap  │
            ├──────────────┤  ├───────────────┤
            │ content_1_2  │  │  content_2_2  │  ← section_content_height
            └──────────────┴──┴───────────────┘
                            ↔ col_gap

        Indices follow ``c_s`` (column, section): ``label_1_2`` is column 1, section 2.

        Flat name index: for column *c* and section *s*:
        ``names[c*n_sections*2 + s*2]`` → label,
        ``names[c*n_sections*2 + s*2 + 1]`` → content.

        Parameters
        ----------
        section_label_height
            Fixed height(s) for section label rows; ``None`` entries stretch.
            Pass a single value to apply to all sections, or a list of length ``n_sections``.
        col_specs
            ``int`` → that many equal-stretch columns;
            ``list`` where ``float`` → fixed width, ``None`` → equal flex-grow share.
        n_sections
            Number of label+content section pairs per column.
        section_content_height
            Fixed height(s) for section content rows; ``None`` entries stretch.
            Pass a single value to apply to all sections, or a list of length ``n_sections``.
        section_gap
            Gap between consecutive sections (content → next label).
            Pass a single value for a uniform gap, or a list of length ``n_sections - 1``
            for per-gap control.
        label_content_gap
            Gap within each section between label and content.
            Pass a single value for a uniform gap, or a list of length ``n_sections``
            for per-section control.
        col_gap
            Gap between columns.
        names
            Flat list of node names in index order; ``None`` uses generated defaults.

        Returns
        -------
        MinimalFlexNode
            Root ROW container node for the complete layout tree.
        """
        stretch = FlexItemProperties(flex_grow=1.0, flex_shrink=1.0, flex_basis=0.0)
        specs: list[float | None] = [None] * col_specs if isinstance(col_specs, int) else col_specs

        label_heights = self._resolve_heights(section_label_height, n_sections, "section_label_height")
        content_heights = self._resolve_heights(section_content_height, n_sections, "section_content_height")
        uniform_section_gap, section_gaps = self._resolve_section_gap(section_gap, n_sections)
        label_content_gaps = self._resolve_gap_list(label_content_gap, n_sections, "label_content_gap")

        body_props = FlexContainerProperties(direction=FlexDirection.ROW, col_gap=col_gap)
        col_props = FlexContainerProperties(direction=FlexDirection.COLUMN, row_gap=uniform_section_gap)

        cols = []
        for c, col_spec in enumerate(specs):
            col_item = (
                FlexItemProperties(flex_grow=0.0, flex_shrink=0.0, flex_basis=col_spec)
                if col_spec is not None
                else stretch
            )
            sections: list[MinimalFlexNode] = []
            for s in range(n_sections):
                label_idx = c * n_sections * 2 + s * 2
                label_h, content_h, lc_gap = label_heights[s], content_heights[s], label_content_gaps[s]
                label_node = self._build_leaf(
                    label_h, self._add_name(names, label_idx, f"col_{c}_section_{s}_label"), stretch
                )
                content_node = self._build_leaf(
                    content_h, self._add_name(names, label_idx + 1, f"col_{c}_section_{s}_content"), stretch
                )
                sections.append(self._build_section(label_node, content_node, label_h, content_h, lc_gap, stretch))
                if section_gaps is not None and s < n_sections - 1:
                    sections.append(
                        MinimalFlexNode(
                            size=(0.0, section_gaps[s]),
                            item_props=FlexItemProperties(flex_grow=0.0, flex_shrink=0.0),
                        )
                    )
            cols.append(MinimalFlexNode(item_props=col_item, container_props=col_props, children=sections))

        return MinimalFlexNode(container_props=body_props, children=cols)

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _resolve_heights(
        value: list[float | None] | float | None,
        n: int,
        param_name: str,
    ) -> list[float | None]:
        """Resolve a scalar or list height spec to a list of length n.

        Parameters
        ----------
        value
            Scalar applied to all sections, or a per-section list.
        n
            Expected list length.
        param_name
            Parameter name used in the error message.

        Returns
        -------
        list[float | None]
            Per-section height values.

        Raises
        ------
        ValueError
            If ``value`` is a list whose length does not equal ``n``.
        """
        if not isinstance(value, list):
            return [value] * n
        if len(value) != n:
            msg = f"{param_name} list length ({len(value)}) must equal n_sections ({n})."
            raise ValueError(msg)
        return value

    @staticmethod
    def _resolve_gap_list(value: list[float] | float, n: int, param_name: str) -> list[float]:
        """Resolve a scalar or list gap spec to a list of length n.

        Parameters
        ----------
        value
            Scalar applied uniformly, or a per-item list.
        n
            Expected list length.
        param_name
            Parameter name used in the error message.

        Returns
        -------
        list[float]
            Per-item gap values.

        Raises
        ------
        ValueError
            If ``value`` is a list whose length does not equal ``n``.
        """
        if not isinstance(value, list):
            return [value] * n
        if len(value) != n:
            msg = f"{param_name} list length ({len(value)}) must equal {n}."
            raise ValueError(msg)
        return value

    @staticmethod
    def _resolve_section_gap(
        value: list[float] | float,
        n_sections: int,
    ) -> tuple[float, list[float] | None]:
        """Resolve section_gap to a uniform float and an optional per-gap list.

        Parameters
        ----------
        value
            Scalar for uniform gaps, or a list of length ``n_sections - 1``.
        n_sections
            Total number of sections.

        Returns
        -------
        tuple[float, list[float] | None]
            ``(uniform_gap, None)`` when scalar; ``(0.0, gaps)`` when a list.

        Raises
        ------
        ValueError
            If ``value`` is a list whose length does not equal ``n_sections - 1``.
        """
        if not isinstance(value, list):
            return value, None
        expected = n_sections - 1
        if len(value) != expected:
            msg = f"section_gap list length ({len(value)}) must equal n_sections - 1 ({expected})."
            raise ValueError(msg)
        return 0.0, value

    @staticmethod
    def _build_leaf(
        height: float | None,
        name: str,
        stretch: FlexItemProperties,
    ) -> MinimalFlexNode:
        """Build a fixed-height or stretching leaf node.

        Parameters
        ----------
        height
            Fixed height; ``None`` makes the node stretch.
        name
            Node name.
        stretch
            Shared stretch item properties.

        Returns
        -------
        MinimalFlexNode
            Leaf node with appropriate size and item properties.
        """
        return MinimalFlexNode(
            size=(0.0, height) if height is not None else (0.0, 0.0),
            item_props=FlexItemProperties(flex_grow=0.0, flex_shrink=0.0) if height is not None else stretch,
            name=name,
        )

    @staticmethod
    def _build_section(
        label_node: MinimalFlexNode,
        content_node: MinimalFlexNode,
        label_h: float | None,
        content_h: float | None,
        lc_gap: float,
        stretch: FlexItemProperties,
    ) -> MinimalFlexNode:
        """Wrap label and content into a COLUMN section sub-container.

        Parameters
        ----------
        label_node
            Label leaf node.
        content_node
            Content leaf node.
        label_h
            Fixed label height; ``None`` when stretching.
        content_h
            Fixed content height; ``None`` when stretching.
        lc_gap
            Gap between label and content within the section.
        stretch
            Shared stretch item properties.

        Returns
        -------
        MinimalFlexNode
            Section container node with label and content as children.
        """
        section_props = FlexContainerProperties(direction=FlexDirection.COLUMN, row_gap=lc_gap)
        if label_h is not None and content_h is not None:
            section_item = FlexItemProperties(flex_grow=0.0, flex_shrink=0.0, flex_basis=label_h + lc_gap + content_h)
        else:
            section_item = stretch
        return MinimalFlexNode(
            size=(0.0, 0.0),
            item_props=section_item,
            container_props=section_props,
            children=[label_node, content_node],
        )
