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

from __future__ import annotations

import pytest

from tenderness.core.geometry import Rectangle
from tenderness.layout_engines.minimal_flexbox.flex_container_properties import (
    AlignContent,
    AlignItems,
    FlexContainerProperties,
    FlexDirection,
    FlexWrap,
    JustifyContent,
)
from tenderness.layout_engines.minimal_flexbox.flex_item_properties import AlignSelf, FlexItemProperties
from tenderness.layout_engines.minimal_flexbox.minimal_flexbox import MinimalFlexBox, MinimalFlexNode

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
_CONTAINER = Rectangle(x=0, y=0, width=300, height=100)
_DEFAULT_PROPS = FlexContainerProperties()
_BOX = MinimalFlexBox()


def _item(
    w: float,
    h: float,
    *,
    grow: float = 0.0,
    shrink: float = 1.0,
    basis: float | None = None,
    order: int = 0,
    align_self: AlignSelf = AlignSelf.AUTO,
) -> tuple[FlexItemProperties, tuple[float, float]]:
    return FlexItemProperties(
        flex_grow=grow,
        flex_shrink=shrink,
        flex_basis=basis,
        order=order,
        align_self=align_self,
    ), (w, h)


def _rects(
    props: FlexContainerProperties,
    items: list[tuple[FlexItemProperties, tuple[float, float]]],
    container: Rectangle = _CONTAINER,
) -> list[Rectangle]:
    return _BOX.resolve(container, props, items)


def _leaf(w: float, h: float, **kwargs: object) -> MinimalFlexNode:
    """Shorthand for a leaf FlexNode."""
    return MinimalFlexNode(size=(w, h), item_props=FlexItemProperties(**kwargs))  # type: ignore[arg-type]


def _container_node(
    w: float,
    h: float,
    children: list[MinimalFlexNode],
    *,
    props: FlexContainerProperties | None = None,
    **kwargs: object,
) -> MinimalFlexNode:
    """Shorthand for a container FlexNode."""
    return MinimalFlexNode(
        size=(w, h),
        item_props=FlexItemProperties(**kwargs),  # type: ignore[arg-type]
        container_props=props or FlexContainerProperties(),
        children=children,
    )


# ---------------------------------------------------------------------------
# Tests for MinimalFlexBox behaviour
# ---------------------------------------------------------------------------
class TestMinimalFlexBox:
    def test_empty_items_returns_empty(self) -> None:
        assert _rects(_DEFAULT_PROPS, []) == []

    def test_single_item_no_grow(self) -> None:
        rects = _rects(_DEFAULT_PROPS, [_item(50, 40)])
        assert len(rects) == 1
        r = rects[0]
        assert r.x == 0
        assert r.y == 0
        assert r.width == 50
        # STRETCH: cross fills container height
        assert r.height == 100

    # -----------------------------------------------------------------------
    # FlexDirection
    # -----------------------------------------------------------------------
    def test_row_places_items_left_to_right(self) -> None:
        props = FlexContainerProperties(direction=FlexDirection.ROW)
        rects = _rects(props, [_item(50, 40), _item(80, 60)])
        assert rects[0].x == 0
        assert rects[1].x == 50

    def test_column_places_items_top_to_bottom(self) -> None:
        props = FlexContainerProperties(direction=FlexDirection.COLUMN)
        rects = _rects(props, [_item(50, 30), _item(60, 40)], container=Rectangle(0, 0, 100, 200))
        assert rects[0].y == 0
        assert rects[1].y == 30

    def test_row_reverse_places_items_right_to_left(self) -> None:
        props = FlexContainerProperties(direction=FlexDirection.ROW_REVERSE)
        rects = _rects(props, [_item(50, 40), _item(80, 60)])
        # first item (50 wide) should be at x=250, second (80 wide) at x=170
        assert rects[0].x == pytest.approx(250)
        assert rects[1].x == pytest.approx(170)

    def test_column_reverse_places_items_bottom_to_top(self) -> None:
        props = FlexContainerProperties(direction=FlexDirection.COLUMN_REVERSE)
        container = Rectangle(0, 0, 100, 200)
        rects = _rects(props, [_item(50, 30), _item(60, 40)], container=container)
        # first item (30 tall) should be at y=170, second (40 tall) at y=130
        assert rects[0].y == pytest.approx(170)
        assert rects[1].y == pytest.approx(130)

    # -----------------------------------------------------------------------
    # Gap
    # -----------------------------------------------------------------------
    def test_col_gap_applied_between_row_items(self) -> None:
        props = FlexContainerProperties(col_gap=10)
        rects = _rects(props, [_item(50, 40), _item(80, 60)])
        assert rects[1].x == pytest.approx(60)  # 50 + 10 gap

    def test_row_gap_applied_between_column_items(self) -> None:
        props = FlexContainerProperties(direction=FlexDirection.COLUMN, row_gap=5)
        rects = _rects(props, [_item(50, 30), _item(60, 40)], container=Rectangle(0, 0, 100, 200))
        assert rects[1].y == pytest.approx(35)  # 30 + 5 gap

    # -----------------------------------------------------------------------
    # Flex grow / shrink
    # -----------------------------------------------------------------------
    def test_flex_grow_distributes_free_space_equally(self) -> None:
        # container=300, two items of 50 each, free=200, each gets +100
        props = FlexContainerProperties()
        rects = _rects(props, [_item(50, 40, grow=1.0), _item(50, 40, grow=1.0)])
        assert rects[0].width == pytest.approx(150)
        assert rects[1].width == pytest.approx(150)

    def test_flex_grow_proportional(self) -> None:
        # container=300, two items of 0, grow 1 and 2 → 100 and 200
        props = FlexContainerProperties()
        rects = _rects(props, [_item(0, 40, grow=1.0), _item(0, 40, grow=2.0)])
        assert rects[0].width == pytest.approx(100)
        assert rects[1].width == pytest.approx(200)

    def test_flex_shrink_reduces_oversized_items(self) -> None:
        # container=300, two items of 200 each → overflow 100, each shrinks by 50
        props = FlexContainerProperties(wrap=FlexWrap.NOWRAP)
        rects = _rects(props, [_item(200, 40, shrink=1.0), _item(200, 40, shrink=1.0)])
        assert rects[0].width == pytest.approx(150)
        assert rects[1].width == pytest.approx(150)

    def test_flex_basis_overrides_intrinsic_size(self) -> None:
        props = FlexContainerProperties()
        rects = _rects(props, [_item(50, 40, basis=20.0), _item(50, 40)])
        # first item starts at 20, not 50
        assert rects[0].width == pytest.approx(20)

    def test_flex_basis_zero_ignores_intrinsic_size(self) -> None:
        # flex_basis=0.0 is distinct from None (auto): it overrides intrinsic width.
        props = FlexContainerProperties()
        rects = _rects(props, [_item(100, 40, basis=0.0), _item(50, 40)])
        assert rects[0].width == pytest.approx(0.0)
        assert rects[1].width == pytest.approx(50.0)

    def test_flex_shrink_scaled_by_size(self) -> None:
        # Two items with equal shrink=1 but different widths: larger absorbs more.
        # container=100, item1=120, item2=60; overflow=80
        # scaled total = 1*120 + 1*60 = 180
        # item1 shrinks 80*(120/180) = 53.333 → 66.667
        # item2 shrinks 80*(60/180) = 26.667 → 33.333
        container = Rectangle(0, 0, 100, 50)
        props = FlexContainerProperties(wrap=FlexWrap.NOWRAP)
        rects = _rects(props, [_item(120, 50, shrink=1.0), _item(60, 50, shrink=1.0)], container=container)
        assert rects[0].width == pytest.approx(200 / 3)
        assert rects[1].width == pytest.approx(100 / 3)

    def test_flex_shrink_iterative_freeze(self) -> None:
        # item1=(1, shrink=10) would absorb 8.27 but only has 1px left → frozen at 0.
        # remaining deficit 90 fully absorbed by item2=(100, shrink=1) → 10.
        container = Rectangle(0, 0, 10, 50)
        props = FlexContainerProperties(wrap=FlexWrap.NOWRAP)
        rects = _rects(props, [_item(1, 50, shrink=10.0), _item(100, 50, shrink=1.0)], container=container)
        assert rects[0].width == pytest.approx(0.0)
        assert rects[1].width == pytest.approx(10.0)

    # -----------------------------------------------------------------------
    # JustifyContent
    # -----------------------------------------------------------------------
    def test_justify_content_flex_end(self) -> None:
        # container=300, one item 50 wide → starts at 250
        props = FlexContainerProperties(justify_content=JustifyContent.FLEX_END)
        rects = _rects(props, [_item(50, 40)])
        assert rects[0].x == pytest.approx(250)

    def test_justify_content_center(self) -> None:
        props = FlexContainerProperties(justify_content=JustifyContent.CENTER)
        rects = _rects(props, [_item(100, 40)])
        assert rects[0].x == pytest.approx(100)  # (300 - 100) / 2

    def test_justify_content_space_between(self) -> None:
        props = FlexContainerProperties(justify_content=JustifyContent.SPACE_BETWEEN)
        rects = _rects(props, [_item(50, 40), _item(50, 40), _item(50, 40)])
        # 300 - 150 = 150 free, 2 gaps → each gap 75
        assert rects[0].x == pytest.approx(0)
        assert rects[1].x == pytest.approx(125)
        assert rects[2].x == pytest.approx(250)

    def test_justify_content_space_around(self) -> None:
        props = FlexContainerProperties(justify_content=JustifyContent.SPACE_AROUND)
        rects = _rects(props, [_item(60, 40), _item(60, 40)])
        # 300 - 120 = 180 free, 2 items → 90 per item, 45 on each side
        assert rects[0].x == pytest.approx(45)
        assert rects[1].x == pytest.approx(195)

    def test_justify_content_space_evenly(self) -> None:
        props = FlexContainerProperties(justify_content=JustifyContent.SPACE_EVENLY)
        rects = _rects(props, [_item(50, 40), _item(50, 40)])
        # 300 - 100 = 200 free, 3 gaps → each 200/3
        spacing = 200 / 3
        assert rects[0].x == pytest.approx(spacing)
        assert rects[1].x == pytest.approx(spacing + 50 + spacing)

    # -----------------------------------------------------------------------
    # AlignItems (cross axis)
    # -----------------------------------------------------------------------
    def test_align_items_stretch_fills_cross_axis(self) -> None:
        props = FlexContainerProperties(align_items=AlignItems.STRETCH)
        rects = _rects(props, [_item(50, 30)])
        assert rects[0].height == pytest.approx(100)

    def test_align_items_flex_start_keeps_intrinsic_cross_size(self) -> None:
        props = FlexContainerProperties(align_items=AlignItems.FLEX_START)
        rects = _rects(props, [_item(50, 30)])
        assert rects[0].height == pytest.approx(30)
        assert rects[0].y == pytest.approx(0)

    def test_align_items_flex_end(self) -> None:
        props = FlexContainerProperties(align_items=AlignItems.FLEX_END)
        rects = _rects(props, [_item(50, 30)])
        assert rects[0].y == pytest.approx(70)  # 100 - 30

    def test_align_items_center(self) -> None:
        props = FlexContainerProperties(align_items=AlignItems.CENTER)
        rects = _rects(props, [_item(50, 30)])
        assert rects[0].y == pytest.approx(35)  # (100 - 30) / 2

    # -----------------------------------------------------------------------
    # AlignSelf overrides AlignItems
    # -----------------------------------------------------------------------
    def test_align_self_overrides_align_items(self) -> None:
        props = FlexContainerProperties(align_items=AlignItems.STRETCH)
        rects = _rects(props, [_item(50, 30, align_self=AlignSelf.FLEX_START)])
        assert rects[0].height == pytest.approx(30)

    def test_align_self_center_on_stretch_container(self) -> None:
        props = FlexContainerProperties(align_items=AlignItems.STRETCH)
        rects = _rects(props, [_item(50, 30, align_self=AlignSelf.CENTER)])
        assert rects[0].y == pytest.approx(35)

    # -----------------------------------------------------------------------
    # Order
    # -----------------------------------------------------------------------
    def test_order_changes_visual_position_but_not_result_index(self) -> None:
        props = FlexContainerProperties()
        # item at index 0 has order=2, item at index 1 has order=1 → index 1 renders first visually
        rects = _rects(props, [_item(50, 40, order=2), _item(80, 40, order=1)])
        # result is in SOURCE order
        assert rects[0].width == pytest.approx(50)  # original 50-wide item
        assert rects[1].width == pytest.approx(80)
        # but visually index 1 starts at x=0, index 0 starts at x=80
        assert rects[1].x == pytest.approx(0)
        assert rects[0].x == pytest.approx(80)

    # -----------------------------------------------------------------------
    # FlexWrap
    # -----------------------------------------------------------------------
    def test_nowrap_single_line_overflows(self) -> None:
        # three items of 120 in a 300-wide container → one line, shrunk
        props = FlexContainerProperties(wrap=FlexWrap.NOWRAP)
        rects = _rects(props, [_item(120, 40), _item(120, 40), _item(120, 40)])
        assert len(rects) == 3
        # all on same y
        assert all(r.y == pytest.approx(0) for r in rects)

    def test_wrap_breaks_into_multiple_lines(self) -> None:
        # two items of 200 in a 300-wide container → two lines
        container = Rectangle(0, 0, 300, 200)
        props = FlexContainerProperties(wrap=FlexWrap.WRAP, align_content=AlignContent.FLEX_START)
        rects = _rects(props, [_item(200, 40), _item(200, 50)], container=container)
        assert rects[0].y == pytest.approx(0)
        assert rects[1].y == pytest.approx(40)

    def test_wrap_reverse_first_line_at_cross_end(self) -> None:
        container = Rectangle(0, 0, 300, 200)
        props = FlexContainerProperties(wrap=FlexWrap.WRAP_REVERSE, align_content=AlignContent.FLEX_START)
        rects = _rects(props, [_item(200, 40), _item(200, 50)], container=container)
        # line 0 should be near cross-end, line 1 above it
        assert rects[0].y > rects[1].y

    def test_wrap_single_line_respects_align_content_flex_start(self) -> None:
        # A WRAP container whose items all fit on one line must still honour
        # align-content. With FLEX_START the line height equals the tallest item
        # (50), not the full container cross dimension (200).
        container = Rectangle(0, 0, 300, 200)
        props = FlexContainerProperties(
            wrap=FlexWrap.WRAP,
            align_content=AlignContent.FLEX_START,
            align_items=AlignItems.STRETCH,
        )
        rects = _rects(props, [_item(100, 50), _item(100, 50)], container=container)
        assert rects[0].height == pytest.approx(50)
        assert rects[1].height == pytest.approx(50)
        assert rects[0].y == pytest.approx(0)

    def test_wrap_reverse_flex_start_pins_to_visual_bottom_of_line(self) -> None:
        # container 300x200, wrap-reverse + FLEX_START.
        # Two items (100x30 and 100x60) share one line; line height=60.
        # Line flips to y=140 (200-60). FLEX_START inside wrap-reverse means
        # "align to visual start (cross-end)", so items pin to y = lcp+lcs-h.
        container = Rectangle(0, 0, 300, 200)
        props = FlexContainerProperties(
            wrap=FlexWrap.WRAP_REVERSE,
            align_items=AlignItems.FLEX_START,
            align_content=AlignContent.FLEX_START,
        )
        rects = _rects(props, [_item(100, 30), _item(100, 60)], container=container)
        # item1 (h=30): y = 140 + 60 - 30 = 170
        assert rects[0].y == pytest.approx(170)
        assert rects[0].height == pytest.approx(30)
        # item2 (h=60) fills its full line: y = 140
        assert rects[1].y == pytest.approx(140)

    # -----------------------------------------------------------------------
    # AlignContent (multi-line)
    # -----------------------------------------------------------------------
    def test_align_content_center_multi_line(self) -> None:
        container = Rectangle(0, 0, 300, 200)
        props = FlexContainerProperties(
            wrap=FlexWrap.WRAP,
            align_content=AlignContent.CENTER,
        )
        rects = _rects(props, [_item(200, 40), _item(200, 40)], container=container)
        # two lines of 40 → total 80; free = 120; center offset = 60
        assert rects[0].y == pytest.approx(60)
        assert rects[1].y == pytest.approx(100)

    def test_align_content_space_between_multi_line(self) -> None:
        container = Rectangle(0, 0, 300, 200)
        props = FlexContainerProperties(
            wrap=FlexWrap.WRAP,
            align_content=AlignContent.SPACE_BETWEEN,
        )
        rects = _rects(props, [_item(200, 40), _item(200, 40)], container=container)
        # lines at cross-start and cross-end
        assert rects[0].y == pytest.approx(0)
        assert rects[1].y == pytest.approx(160)  # 200 - 40

    def test_align_content_stretch_expands_lines(self) -> None:
        container = Rectangle(0, 0, 300, 200)
        props = FlexContainerProperties(
            wrap=FlexWrap.WRAP,
            align_content=AlignContent.STRETCH,
            align_items=AlignItems.STRETCH,
        )
        rects = _rects(props, [_item(200, 40), _item(200, 40)], container=container)
        # two lines stretched to fill 200 → each line 100 tall
        assert rects[0].height == pytest.approx(100)
        assert rects[1].height == pytest.approx(100)

    def test_align_content_space_around_multi_line(self) -> None:
        # Two lines (h=40, h=60); free=200-100=100; chunk=50; start=25; spacing=50
        # line0 at y=25, line1 at y=25+40+50=115; equal 25px margins top and bottom
        container = Rectangle(0, 0, 300, 200)
        props = FlexContainerProperties(
            wrap=FlexWrap.WRAP,
            align_content=AlignContent.SPACE_AROUND,
            align_items=AlignItems.FLEX_START,
        )
        rects = _rects(props, [_item(200, 40), _item(200, 60)], container=container)
        assert rects[0].y == pytest.approx(25)
        assert rects[1].y == pytest.approx(115)

    def test_align_content_space_evenly_multi_line(self) -> None:
        # Two lines (h=40, h=60); free=100; chunk=100/3; all gaps equal
        # line0 at y=chunk, line1 at y=chunk+40+chunk
        container = Rectangle(0, 0, 300, 200)
        props = FlexContainerProperties(
            wrap=FlexWrap.WRAP,
            align_content=AlignContent.SPACE_EVENLY,
            align_items=AlignItems.FLEX_START,
        )
        rects = _rects(props, [_item(200, 40), _item(200, 60)], container=container)
        chunk = 100 / 3
        assert rects[0].y == pytest.approx(chunk)
        assert rects[1].y == pytest.approx(chunk + 40 + chunk)

    # -----------------------------------------------------------------------
    # Gap + space distribution modes
    # -----------------------------------------------------------------------
    def test_space_between_with_gap(self) -> None:
        # container=300, 3x50 items, col_gap=10
        # free = 300 - 150 - 20 = 130; spacing = gap + free/(n-1) = 10 + 65 = 75
        # positions: 0, 125, 250
        props = FlexContainerProperties(justify_content=JustifyContent.SPACE_BETWEEN, col_gap=10)
        rects = _rects(props, [_item(50, 40), _item(50, 40), _item(50, 40)])
        assert rects[0].x == pytest.approx(0)
        assert rects[1].x == pytest.approx(125)
        assert rects[2].x == pytest.approx(250)

    def test_space_around_with_gap(self) -> None:
        # container=300, 2x60 items, col_gap=10
        # free = 300 - 120 - 10 = 170; chunk = 85; start = 42.5; spacing = gap+chunk = 95
        # positions: 42.5, 197.5; total = 42.5+60+95+60+42.5 = 300
        props = FlexContainerProperties(justify_content=JustifyContent.SPACE_AROUND, col_gap=10)
        rects = _rects(props, [_item(60, 40), _item(60, 40)])
        assert rects[0].x == pytest.approx(42.5)
        assert rects[1].x == pytest.approx(197.5)

    def test_space_evenly_with_gap(self) -> None:
        # container=300, 2x50 items, col_gap=10
        # free = 300 - 100 - 10 = 190; chunk = 190/3; spacing = gap+chunk
        # positions: chunk, chunk+50+gap+chunk; total = 3*chunk+100+10 = 190+110 = 300
        chunk = 190 / 3
        props = FlexContainerProperties(justify_content=JustifyContent.SPACE_EVENLY, col_gap=10)
        rects = _rects(props, [_item(50, 40), _item(50, 40)])
        assert rects[0].x == pytest.approx(chunk)
        assert rects[1].x == pytest.approx(chunk + 50 + 10 + chunk)

    # -----------------------------------------------------------------------
    # Overflow fallback (free < 0)
    # -----------------------------------------------------------------------
    def test_space_between_overflow_falls_back_to_flex_start(self) -> None:
        # container=100, 3x50 items, shrink=0 → no shrink; overflow=-50
        # SPACE_BETWEEN falls back to FLEX_START: items stacked with gap=0
        container = Rectangle(0, 0, 100, 50)
        props = FlexContainerProperties(justify_content=JustifyContent.SPACE_BETWEEN, wrap=FlexWrap.NOWRAP)
        rects = _rects(
            props,
            [_item(50, 50, shrink=0.0), _item(50, 50, shrink=0.0), _item(50, 50, shrink=0.0)],
            container=container,
        )
        assert rects[0].x == pytest.approx(0)
        assert rects[1].x == pytest.approx(50)
        assert rects[2].x == pytest.approx(100)

    # -----------------------------------------------------------------------
    # Container with non-zero origin
    # -----------------------------------------------------------------------
    def test_non_zero_container_origin(self) -> None:
        container = Rectangle(x=50, y=20, width=300, height=100)
        props = FlexContainerProperties()
        rects = _rects(props, [_item(50, 40)], container=container)
        assert rects[0].x == pytest.approx(50)
        assert rects[0].y == pytest.approx(20)

    # -----------------------------------------------------------------------
    # FlexNode / resolve_tree  (flex-inside-flex)
    # -----------------------------------------------------------------------
    def test_resolve_tree_flat_leaves_equivalent_to_resolve(self) -> None:
        """A root container with only leaf children should match the flat resolve()."""
        container = Rectangle(0, 0, 300, 100)
        root = _container_node(
            300,
            100,
            children=[_leaf(50, 40), _leaf(80, 60)],
        )
        pairs = _BOX.resolve_tree(container, root)
        leaves = [r for _, r in pairs]
        assert len(leaves) == 2
        assert leaves[0].x == pytest.approx(0)
        assert leaves[1].x == pytest.approx(50)

    def test_resolve_tree_nested_container_receives_parent_resolved_rect(self) -> None:
        """
        Root: row, 300 wide, two children each flex_grow=1 → each 150 wide.
        Right child is itself a column container with two leaves of 40 and 60 height.
        """
        container = Rectangle(0, 0, 300, 100)
        root = _container_node(
            300,
            100,
            children=[
                _leaf(0, 100, flex_grow=1.0),
                _container_node(
                    0,
                    100,
                    children=[_leaf(150, 40), _leaf(150, 60)],
                    props=FlexContainerProperties(
                        direction=FlexDirection.COLUMN,
                        align_items=AlignItems.FLEX_START,
                    ),
                    flex_grow=1.0,
                ),
            ],
        )
        pairs = _BOX.resolve_tree(container, root)
        assert len(pairs) == 3  # left leaf + two nested leaves

        _, left_rect = pairs[0]
        assert left_rect.x == pytest.approx(0)
        assert left_rect.width == pytest.approx(150)

        _, top_rect = pairs[1]
        _, bot_rect = pairs[2]

        # nested container resolved to x=150, width=150
        assert top_rect.x == pytest.approx(150)
        assert top_rect.width == pytest.approx(150)
        assert top_rect.y == pytest.approx(0)
        assert top_rect.height == pytest.approx(40)

        assert bot_rect.x == pytest.approx(150)
        assert bot_rect.y == pytest.approx(40)
        assert bot_rect.height == pytest.approx(60)

    def test_resolve_tree_three_levels_deep(self) -> None:
        """
        Root row → left leaf + right column container
                                  → top leaf + bottom row container
                                                   → two leaf cells
        """
        container = Rectangle(0, 0, 400, 200)
        root = _container_node(
            400,
            200,
            children=[
                _leaf(200, 200),
                _container_node(
                    200,
                    200,
                    children=[
                        _leaf(200, 100),
                        _container_node(
                            200,
                            100,
                            children=[_leaf(100, 100), _leaf(100, 100)],
                            props=FlexContainerProperties(direction=FlexDirection.ROW),
                        ),
                    ],
                    props=FlexContainerProperties(
                        direction=FlexDirection.COLUMN,
                        align_items=AlignItems.FLEX_START,
                    ),
                ),
            ],
        )
        pairs = _BOX.resolve_tree(container, root)
        _, rects = zip(*pairs, strict=True)
        assert len(rects) == 4

        # left leaf
        assert rects[0].x == pytest.approx(0)
        assert rects[0].width == pytest.approx(200)

        # top leaf inside right column
        assert rects[1].x == pytest.approx(200)
        assert rects[1].y == pytest.approx(0)
        assert rects[1].height == pytest.approx(100)

        # two cells inside the bottom row container
        assert rects[2].x == pytest.approx(200)
        assert rects[2].y == pytest.approx(100)
        assert rects[2].width == pytest.approx(100)

        assert rects[3].x == pytest.approx(300)
        assert rects[3].y == pytest.approx(100)
        assert rects[3].width == pytest.approx(100)

    def test_resolve_tree_returns_leaf_nodes_not_containers(self) -> None:
        """Container nodes must not appear in the result."""
        container = Rectangle(0, 0, 200, 100)
        inner_props = FlexContainerProperties()
        root = _container_node(
            200,
            100,
            children=[
                _leaf(50, 100),
                _container_node(50, 100, children=[_leaf(50, 50), _leaf(50, 50)], props=inner_props),
            ],
        )
        pairs = _BOX.resolve_tree(container, root)
        for node, _ in pairs:
            assert not node.is_container

    def test_flex_node_is_container_property(self) -> None:
        leaf = _leaf(50, 50)
        assert not leaf.is_container

        cont = _container_node(100, 100, children=[_leaf(50, 50)])
        assert cont.is_container

        no_children = MinimalFlexNode(size=(100, 100), container_props=FlexContainerProperties())
        assert not no_children.is_container

    def test_resolve_tree_empty_children_returns_empty(self) -> None:
        root = MinimalFlexNode(size=(300, 100), container_props=FlexContainerProperties(), children=[])
        result = _BOX.resolve_tree(Rectangle(0, 0, 300, 100), root)
        assert result == []
