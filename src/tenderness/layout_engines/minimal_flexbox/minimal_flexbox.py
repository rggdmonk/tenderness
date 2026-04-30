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

"""Minimal CSS Flexbox layout engine for pixel-coordinate rendering."""

from __future__ import annotations

from dataclasses import dataclass, field

from tenderness.core.geometry import Rectangle
from tenderness.layout_engines.minimal_flexbox.flex_container_properties import (
    AlignContent,
    AlignItems,
    FlexContainerProperties,
    FlexDirection,
    FlexWrap,
    JustifyContent,
)
from tenderness.layout_engines.minimal_flexbox.flex_item_properties import (
    AlignSelf,
    FlexItemProperties,
)

type _DistMode = JustifyContent | AlignContent


_FREEZE_EPSILON: float = 1e-5  # items shrunk to within this of 0.0 are frozen


@dataclass(slots=True)
class MinimalFlexNode:
    """
    A node in a flex tree — either a leaf (content) or a nested flex container.

    As a **leaf**: set ``size`` to the intrinsic pixel dimensions and leave
    ``container_props`` / ``children`` empty.

    As a **container**: set ``size``, ``container_props``, and ``children``.
    ``size`` is used by the *parent* container for flex calculations (i.e. as
    the base size before grow / shrink). Once the parent resolves the actual
    bounds for this node, those bounds become the container rect for its own
    children.

    If ``item_props.flex_basis`` is set it overrides ``size`` along the main
    axis, exactly as in the flat API.
    """

    size: tuple[float, float] = field(default=(0.0, 0.0))
    item_props: FlexItemProperties = field(default_factory=FlexItemProperties)
    container_props: FlexContainerProperties | None = field(default=None)
    children: list[MinimalFlexNode] = field(default_factory=list)
    name: str | None = field(default=None)

    @property
    def is_container(self) -> bool:
        """True when this node acts as a flex container for its children.

        Both ``container_props`` *and* at least one child are required.
        A node with ``container_props`` set but an empty ``children`` list is
        treated as a leaf — it carries no layout responsibility.
        """
        return self.container_props is not None and bool(self.children)


@dataclass(slots=True)
class _MinimalFlexItem:
    """Internal per-item state used during layout resolution."""

    source_index: int
    props: FlexItemProperties
    main_size: float  # resolved along the main axis (after flex grow/shrink)
    cross_size: float  # resolved along the cross axis (after align-items)
    main_pos: float = field(default=0.0)  # offset from main-start of the container
    cross_pos: float = field(default=0.0)  # offset from cross-start of the container


class MinimalFlexBox:
    """
    A minimal CSS Flexbox layout engine operating on concrete pixel coordinates.

    Implements the core Flexbox algorithm:
    - Single-direction layout on a main axis with a perpendicular cross axis
    - Line wrapping (nowrap / wrap / wrap-reverse)
    - Flex grow and shrink
    - justify-content, align-items, align-self, align-content
    - row-gap / column-gap

    Not implemented (out of scope for a pixel-coordinate renderer):
    - Writing-mode / directionality (ltr / rtl)
    - Percentage sizes or auto margins
    - Baseline alignment
    - min-width / max-width constraints

    Args:
        container: The rectangle acting as the flex container.
        props:     Container-level properties (direction, wrap, alignment, gaps).
        items:     Sequence of ``(FlexItemProperties, (width, height))`` in source order.

    Returns
    -------
        ``list[Rectangle]`` with one entry per input item, in **source order**.
    """

    def resolve(
        self,
        container: Rectangle,
        props: FlexContainerProperties,
        items: list[tuple[FlexItemProperties, tuple[float, float]]],
    ) -> list[Rectangle]:
        """Resolve flex layout and return one Rectangle per item in source order.

        Parameters
        ----------
        container
            Rectangle acting as the flex container.
        props
            Container-level properties (direction, wrap, alignment, gaps).
        items
            Sequence of ``(FlexItemProperties, (width, height))`` in source order.
        """
        if not items:
            return []

        # ── 1. Order items: stable sort preserves source order for ties ───
        indexed = sorted(enumerate(items), key=lambda x: x[1][0].order)

        # ── 2. Axis configuration ─────────────────────────────────────────
        is_row = props.direction in (FlexDirection.ROW, FlexDirection.ROW_REVERSE)
        is_reverse_main = props.direction in (FlexDirection.ROW_REVERSE, FlexDirection.COLUMN_REVERSE)
        is_wrap_reverse = props.wrap == FlexWrap.WRAP_REVERSE

        container_main = container.width if is_row else container.height
        container_cross = container.height if is_row else container.width
        main_gap = props.col_gap if is_row else props.row_gap
        cross_gap = props.row_gap if is_row else props.col_gap

        # ── 3. Build internal items; flex-basis overrides intrinsic main size
        flex_items = self._build_flex_items(indexed=indexed, is_row=is_row)

        # ── 4. Collect into lines ─────────────────────────────────────────
        lines = self._collect_lines(items=flex_items, container_main=container_main, main_gap=main_gap, wrap=props.wrap)

        # ── 5. Resolve flex grow / shrink within each line ────────────────
        for line in lines:
            self._resolve_flexible_lengths(line=line, container_main=container_main, main_gap=main_gap)

        # ── 6-8. Cross axis: line sizes, line positions, item alignment ───
        self._resolve_cross_axis(
            lines=lines,
            container_cross=container_cross,
            cross_gap=cross_gap,
            props=props,
            is_wrap_reverse=is_wrap_reverse,
        )

        # ── 9. Main axis: justify-content ─────────────────────────────────
        self._resolve_main_axis(
            lines=lines, container_main=container_main, main_gap=main_gap, justify_mode=props.justify_content
        )

        # ── 10. Convert to absolute Rectangles in source order ────────────
        result: list[Rectangle] = [Rectangle(0.0, 0.0, 0.0, 0.0)] * len(items)
        for line in lines:
            for item in line:
                result[item.source_index] = self._to_rect(
                    item=item, container=container, is_row=is_row, is_reverse_main=is_reverse_main
                )

        return result

    def resolve_tree(
        self,
        container: Rectangle,
        node: MinimalFlexNode,
    ) -> list[tuple[MinimalFlexNode, Rectangle]]:
        """Recursively resolve a flex tree rooted at node within container.

        node must be a container (``is_container`` is True). Container nodes do
        not appear in the result — only their leaf descendants do.

        Parameters
        ----------
        container
            Absolute bounds to lay out node's children within.
        node
            A :class:`MinimalFlexNode` with ``container_props`` and ``children``.

        Returns
        -------
        list[tuple[MinimalFlexNode, Rectangle]]
            Flat list of ``(leaf_node, rect)`` pairs in depth-first tree order.
            Leaf rects are absolute pixel Rectangles.
        """
        if node.container_props is None:
            msg = "resolve_tree requires a container node (container_props must be set)"
            raise ValueError(msg)
        if not node.children:
            return []
        items = [(child.item_props, child.size) for child in node.children]
        rects = self.resolve(container, node.container_props, items)

        result: list[tuple[MinimalFlexNode, Rectangle]] = []
        for child, rect in zip(node.children, rects, strict=True):
            if child.is_container:
                result.extend(self.resolve_tree(rect, child))
            else:
                result.append((child, rect))
        return result

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _build_flex_items(
        self,
        indexed: list[tuple[int, tuple[FlexItemProperties, tuple[float, float]]]],
        *,
        is_row: bool,
    ) -> list[_MinimalFlexItem]:
        """Construct :class:`_FlexItem` instances with flex-basis and intrinsic sizes."""
        result = []
        for src_idx, (item_props, size) in indexed:
            intrinsic_main = size[0] if is_row else size[1]
            cross_size = size[1] if is_row else size[0]
            main_size = item_props.flex_basis if item_props.flex_basis is not None else intrinsic_main
            result.append(
                _MinimalFlexItem(source_index=src_idx, props=item_props, main_size=main_size, cross_size=cross_size)
            )
        return result

    def _collect_lines(
        self,
        items: list[_MinimalFlexItem],
        container_main: float,
        main_gap: float,
        wrap: FlexWrap,
    ) -> list[list[_MinimalFlexItem]]:
        """Split *items* into flex lines according to *wrap* and *container_main*."""
        if wrap == FlexWrap.NOWRAP:
            return [list(items)]

        lines: list[list[_MinimalFlexItem]] = []
        current_line: list[_MinimalFlexItem] = []
        current_size = 0.0

        for item in items:
            gap = main_gap if current_line else 0.0
            if current_line and current_size + gap + item.main_size > container_main + 1e-9:
                lines.append(current_line)
                current_line = [item]
                current_size = item.main_size
            else:
                current_line.append(item)
                current_size += gap + item.main_size

        if current_line:
            lines.append(current_line)

        return lines

    def _resolve_flexible_lengths(
        self,
        line: list[_MinimalFlexItem],
        container_main: float,
        main_gap: float,
    ) -> None:
        """Apply flex-grow / flex-shrink to items in *line*, mutating ``main_size`` in-place."""
        if not line:
            return

        total_gap = main_gap * (len(line) - 1)
        free = container_main - total_gap - sum(item.main_size for item in line)

        if free > 0:
            total_grow = sum(item.props.flex_grow for item in line)
            if total_grow > 0:
                for item in line:
                    item.main_size += free * (item.props.flex_grow / total_grow)
        elif free < 0:
            self._apply_flex_shrink(line=line, deficit=-free)

    def _apply_flex_shrink(self, line: list[_MinimalFlexItem], deficit: float) -> None:
        """CSS iterative-freeze flex-shrink algorithm.

        Items that would shrink below 0.0 are frozen at 0.0 and their unabsorbed
        deficit is redistributed to the remaining unfrozen items.
        """
        unfrozen = list(line)
        while unfrozen and deficit > _FREEZE_EPSILON:
            total_scaled_shrink = sum(item.props.flex_shrink * item.main_size for item in unfrozen)
            if total_scaled_shrink <= 0:
                break
            freeze_happened = False
            next_unfrozen: list[_MinimalFlexItem] = []
            for item in unfrozen:
                shrink_ratio = (item.props.flex_shrink * item.main_size) / total_scaled_shrink
                shrink_amount = deficit * shrink_ratio
                if item.main_size - shrink_amount <= _FREEZE_EPSILON:
                    deficit -= item.main_size
                    item.main_size = 0.0
                    freeze_happened = True
                else:
                    next_unfrozen.append(item)
            if freeze_happened:
                unfrozen = next_unfrozen
            else:
                for item in unfrozen:
                    shrink_ratio = (item.props.flex_shrink * item.main_size) / total_scaled_shrink
                    item.main_size -= deficit * shrink_ratio
                break

    def _resolve_cross_axis(
        self,
        lines: list[list[_MinimalFlexItem]],
        container_cross: float,
        cross_gap: float,
        props: FlexContainerProperties,
        *,
        is_wrap_reverse: bool,
    ) -> None:
        """Compute line cross sizes, distribute them, then align items within each line."""
        is_single_line = props.wrap == FlexWrap.NOWRAP
        # align-content: normal acts like stretch for multi-line containers
        effective_ac = AlignContent.STRETCH if props.align_content == AlignContent.NORMAL else props.align_content

        line_cross_sizes = self._compute_line_cross_sizes(
            lines=lines,
            container_cross=container_cross,
            cross_gap=cross_gap,
            align_content=effective_ac,
            is_single_line=is_single_line,
        )

        # STRETCH already inflated sizes → pack from start
        dist_mode = AlignContent.FLEX_START if effective_ac == AlignContent.STRETCH else effective_ac
        line_cross_positions = self._distribute(
            sizes=line_cross_sizes, container=container_cross, gap=cross_gap, mode=dist_mode
        )

        if is_wrap_reverse:
            # flip each line's cross position so line[0] lands at cross-end
            line_cross_positions = [
                container_cross - p - s for p, s in zip(line_cross_positions, line_cross_sizes, strict=True)
            ]

        for line_idx, line in enumerate(lines):
            lcs = line_cross_sizes[line_idx]
            lcp = line_cross_positions[line_idx]
            for item in line:
                self._apply_align_item(
                    item=item,
                    line_cross_size=lcs,
                    line_cross_pos=lcp,
                    align_items=props.align_items,
                    is_wrap_reverse=is_wrap_reverse,
                )

    def _compute_line_cross_sizes(
        self,
        lines: list[list[_MinimalFlexItem]],
        container_cross: float,
        cross_gap: float,
        align_content: AlignContent,
        *,
        is_single_line: bool,
    ) -> list[float]:
        """Return the cross-axis size for each flex line."""
        n = len(lines)

        # nowrap containers always occupy the full cross dimension; wrapping containers
        # that happen to produce one line still respect align-content.
        if is_single_line:
            return [container_cross]

        intrinsic = [max(item.cross_size for item in line) if line else 0.0 for line in lines]

        if align_content == AlignContent.STRETCH:
            total = sum(intrinsic) + cross_gap * (n - 1)
            free = container_cross - total
            if free > 0:
                extra = free / n
                return [s + extra for s in intrinsic]

        return intrinsic

    def _apply_align_item(
        self,
        item: _MinimalFlexItem,
        line_cross_size: float,
        line_cross_pos: float,
        align_items: AlignItems,
        *,
        is_wrap_reverse: bool,
    ) -> None:
        """Set ``item.cross_pos`` (and optionally ``cross_size``) within its line.

        When *is_wrap_reverse* is True the container's cross-start and cross-end are
        swapped, so FLEX_START/FLEX_END positions within each line are also swapped.
        """
        align = item.props.align_self
        effective: AlignItems | AlignSelf = align_items if align == AlignSelf.AUTO else align

        if effective == AlignItems.STRETCH:
            item.cross_size = line_cross_size
            item.cross_pos = line_cross_pos
        elif effective == AlignItems.FLEX_START:
            # wrap-reverse swaps cross-start to the visual end of the line
            item.cross_pos = line_cross_pos + line_cross_size - item.cross_size if is_wrap_reverse else line_cross_pos
        elif effective == AlignItems.FLEX_END:
            # wrap-reverse swaps cross-end to the visual start of the line
            item.cross_pos = line_cross_pos if is_wrap_reverse else line_cross_pos + line_cross_size - item.cross_size
        elif effective == AlignItems.CENTER:
            item.cross_pos = line_cross_pos + (line_cross_size - item.cross_size) / 2.0
        else:
            # BASELINE not supported — fall back to flex_start (respecting wrap-reverse)
            item.cross_pos = line_cross_pos + line_cross_size - item.cross_size if is_wrap_reverse else line_cross_pos

    def _resolve_main_axis(
        self,
        lines: list[list[_MinimalFlexItem]],
        container_main: float,
        main_gap: float,
        justify_mode: JustifyContent,
    ) -> None:
        """Distribute items along the main axis (justify-content), mutating ``main_pos``."""
        for line in lines:
            positions = self._distribute(
                sizes=[item.main_size for item in line], container=container_main, gap=main_gap, mode=justify_mode
            )
            for item, pos in zip(line, positions, strict=True):
                item.main_pos = pos

    def _to_rect(
        self,
        item: _MinimalFlexItem,
        container: Rectangle,
        *,
        is_row: bool,
        is_reverse_main: bool,
    ) -> Rectangle:
        """Convert an item's main/cross offsets into an absolute ``Rectangle``."""
        if is_row:
            x = container.x_max - item.main_pos - item.main_size if is_reverse_main else container.x_min + item.main_pos
            return Rectangle(x=x, y=container.y_min + item.cross_pos, width=item.main_size, height=item.cross_size)
        y = container.y_max - item.main_pos - item.main_size if is_reverse_main else container.y_min + item.main_pos
        return Rectangle(x=container.x_min + item.cross_pos, y=y, width=item.cross_size, height=item.main_size)

    def _distribute(self, sizes: list[float], container: float, gap: float, mode: _DistMode) -> list[float]:
        """
        Return start positions for *sizes* distributed across *container*.

        Positions are relative to the start of the container on the relevant axis.
        The caller converts to absolute pixel coordinates in ``_to_rect``.

        Supports all ``JustifyContent`` and ``AlignContent`` string values.
        """
        n = len(sizes)
        if n == 0:
            return []

        free = container - sum(sizes) - gap * (n - 1)
        start, spacing = self._distribution_params(n=n, free=free, gap=gap, mode=mode)

        pos, positions = start, []
        for s in sizes:
            positions.append(pos)
            pos += s + spacing
        return positions

    def _distribution_params(self, n: int, free: float, gap: float, mode: _DistMode) -> tuple[float, float]:
        """Return ``(start_pos, inter-item spacing)`` for the given distribution *mode*.

        When *free* < 0 (overflow), space-distribution modes fall back to safe modes
        per the CSS Box Alignment spec: SPACE_BETWEEN → FLEX_START,
        SPACE_AROUND / SPACE_EVENLY → CENTER.

        *gap* is the minimum baseline spacing; space-distribution modes add their
        computed chunk on top of it.
        """
        # Overflow fallback: space modes are undefined for negative free space.
        if free < 0:
            if mode in (JustifyContent.SPACE_BETWEEN, AlignContent.SPACE_BETWEEN):
                mode = JustifyContent.FLEX_START
            elif mode in (
                JustifyContent.SPACE_AROUND,
                AlignContent.SPACE_AROUND,
                JustifyContent.SPACE_EVENLY,
                AlignContent.SPACE_EVENLY,
            ):
                mode = JustifyContent.CENTER

        if mode in (JustifyContent.SPACE_AROUND, AlignContent.SPACE_AROUND):
            chunk = free / n
            return chunk / 2.0, gap + chunk
        if mode in (JustifyContent.SPACE_EVENLY, AlignContent.SPACE_EVENLY):
            chunk = free / (n + 1)
            return chunk, gap + chunk
        # All remaining modes use *gap* as the inter-item spacing; only start differs.
        start_by_mode: dict[_DistMode, float] = {
            JustifyContent.FLEX_START: 0.0,
            AlignContent.FLEX_START: 0.0,
            AlignContent.STRETCH: 0.0,
            JustifyContent.FLEX_END: free,
            AlignContent.FLEX_END: free,
            JustifyContent.CENTER: free / 2.0,
            AlignContent.CENTER: free / 2.0,
            JustifyContent.SPACE_BETWEEN: 0.0,
            AlignContent.SPACE_BETWEEN: 0.0,
        }
        is_space_between = mode in (JustifyContent.SPACE_BETWEEN, AlignContent.SPACE_BETWEEN)
        spacing = gap + free / (n - 1) if (is_space_between and n > 1) else gap
        return start_by_mode.get(mode, 0.0), spacing
