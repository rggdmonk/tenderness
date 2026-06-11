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
from tenderness.layout_engines.minimal_flexbox.minimal_flexbox import MinimalFlexBox, MinimalFlexNode
from tenderness.layout_engines.minimal_flexbox.templates.flow import MinimalFlexBoxTemplateFlow

_ENGINE = MinimalFlexBox()
_C360x240 = Rectangle(x=0, y=0, width=360, height=240)  # TestFlowColumns
_C400x300 = Rectangle(x=0, y=0, width=400, height=300)  # TestFlowRows
_flow = MinimalFlexBoxTemplateFlow()


def _resolve(node: MinimalFlexNode, container: Rectangle = _C360x240) -> dict[str, Rectangle]:
    return {n.name: r for n, r in _ENGINE.resolve_tree(container, node) if n.name is not None}


class TestFlowColumns:
    # Container: 360w x 240h
    def test_int_count_produces_equal_width_columns(self) -> None:
        rects = _resolve(_flow.flow_columns(specs=3), _C360x240)
        assert len(rects) == 3
        for r in rects.values():
            assert r.width == pytest.approx(120.0)
            assert r.height == pytest.approx(240.0)

    def test_int_columns_packed_left_to_right(self) -> None:
        rects = _resolve(_flow.flow_columns(specs=3), _C360x240)
        assert rects["col_0"].x == pytest.approx(0.0)
        assert rects["col_1"].x == pytest.approx(120.0)
        assert rects["col_2"].x == pytest.approx(240.0)

    def test_int_with_gap(self) -> None:
        # 2 cols, gap=10 → each (360-10)/2=175
        rects = _resolve(_flow.flow_columns(specs=2, gap=10.0), _C360x240)
        assert rects["col_0"].width == pytest.approx(175.0)
        assert rects["col_1"].x == pytest.approx(185.0)

    def test_list_fixed_widths(self) -> None:
        rects = _resolve(_flow.flow_columns(specs=[80.0, 120.0]), _C360x240)
        assert rects["col_0"].width == pytest.approx(80.0)
        assert rects["col_1"].width == pytest.approx(120.0)
        assert rects["col_1"].x == pytest.approx(80.0)

    def test_list_mixed_fixed_and_stretch(self) -> None:
        # [60, None, 40] → stretch=360-60-40=260
        rects = _resolve(_flow.flow_columns(specs=[60.0, None, 40.0]), _C360x240)
        assert rects["col_0"].width == pytest.approx(60.0)
        assert rects["col_2"].width == pytest.approx(40.0)
        assert rects["col_1"].width == pytest.approx(260.0)

    def test_list_all_stretch_same_as_int(self) -> None:
        rects_list = _resolve(_flow.flow_columns(specs=[None, None, None]), _C360x240)
        rects_int = _resolve(_flow.flow_columns(specs=3), _C360x240)
        for key in rects_list:
            assert rects_list[key].width == pytest.approx(rects_int[key].width)

    def test_custom_names(self) -> None:
        rects = _resolve(_flow.flow_columns(specs=2, names=["left", "right"]), _C360x240)
        assert "left" in rects
        assert "right" in rects

    def test_all_columns_share_same_y_and_height(self) -> None:
        rects = _resolve(_flow.flow_columns(specs=[50.0, None, 70.0]), _C360x240)
        assert len({r.y for r in rects.values()}) == 1
        assert len({r.height for r in rects.values()}) == 1


class TestFlowRows:
    # Container: 400w x 300h
    def test_int_count_produces_equal_height_rows(self) -> None:
        rects = _resolve(_flow.flow_rows(specs=4), _C400x300)
        assert len(rects) == 4
        for r in rects.values():
            assert r.height == pytest.approx(75.0)
            assert r.width == pytest.approx(400.0)

    def test_int_rows_packed_top_to_bottom(self) -> None:
        rects = _resolve(_flow.flow_rows(specs=3), _C400x300)
        assert rects["row_0"].y == pytest.approx(0.0)
        assert rects["row_1"].y == pytest.approx(100.0)
        assert rects["row_2"].y == pytest.approx(200.0)

    def test_int_with_gap(self) -> None:
        # 2 rows, gap=10 → each (300-10)/2=145
        rects = _resolve(_flow.flow_rows(specs=2, gap=10.0), _C400x300)
        assert rects["row_0"].height == pytest.approx(145.0)
        assert rects["row_1"].y == pytest.approx(155.0)

    def test_list_fixed_heights(self) -> None:
        rects = _resolve(_flow.flow_rows(specs=[60.0, 80.0]), _C400x300)
        assert rects["row_0"].height == pytest.approx(60.0)
        assert rects["row_1"].height == pytest.approx(80.0)
        assert rects["row_1"].y == pytest.approx(60.0)

    def test_list_mixed_fixed_and_stretch(self) -> None:
        # [40, None, 30] → stretch=300-40-30=230
        rects = _resolve(_flow.flow_rows(specs=[40.0, None, 30.0]), _C400x300)
        assert rects["row_0"].height == pytest.approx(40.0)
        assert rects["row_2"].height == pytest.approx(30.0)
        assert rects["row_1"].height == pytest.approx(230.0)

    def test_custom_names(self) -> None:
        rects = _resolve(_flow.flow_rows(specs=2, names=["top", "bottom"]), _C400x300)
        assert "top" in rects
        assert "bottom" in rects

    def test_all_rows_share_same_x_and_width(self) -> None:
        rects = _resolve(_flow.flow_rows(specs=[50.0, None, 30.0]), _C400x300)
        assert len({r.x for r in rects.values()}) == 1
        assert len({r.width for r in rects.values()}) == 1
