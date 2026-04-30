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
_C300x200 = Rectangle(x=0, y=0, width=300, height=200)
_flow = MinimalFlexBoxTemplateFlow()


def _resolve(node: MinimalFlexNode, container: Rectangle = _C300x200) -> dict[str, Rectangle]:
    return {n.name: r for n, r in _ENGINE.resolve_tree(container, node) if n.name is not None}


class TestFlowColumns:
    def test_int_count_produces_equal_width_columns(self) -> None:
        rects = _resolve(_flow.flow_columns(specs=3))
        assert len(rects) == 3
        for r in rects.values():
            assert r.width == pytest.approx(100.0)
            assert r.height == pytest.approx(200.0)

    def test_int_columns_packed_left_to_right(self) -> None:
        rects = _resolve(_flow.flow_columns(specs=3))
        assert rects["col_0"].x == pytest.approx(0.0)
        assert rects["col_1"].x == pytest.approx(100.0)
        assert rects["col_2"].x == pytest.approx(200.0)

    def test_int_with_gap(self) -> None:
        rects = _resolve(_flow.flow_columns(specs=2, gap=10.0))
        assert rects["col_0"].width == pytest.approx(145.0)
        assert rects["col_1"].x == pytest.approx(155.0)

    def test_list_fixed_widths(self) -> None:
        rects = _resolve(_flow.flow_columns(specs=[80.0, 120.0]))
        assert rects["col_0"].width == pytest.approx(80.0)
        assert rects["col_1"].width == pytest.approx(120.0)
        assert rects["col_1"].x == pytest.approx(80.0)

    def test_list_mixed_fixed_and_stretch(self) -> None:
        rects = _resolve(_flow.flow_columns(specs=[60.0, None, 40.0]))
        assert rects["col_0"].width == pytest.approx(60.0)
        assert rects["col_2"].width == pytest.approx(40.0)
        assert rects["col_1"].width == pytest.approx(200.0)  # 300 - 60 - 40

    def test_list_all_stretch_same_as_int(self) -> None:
        rects_list = _resolve(_flow.flow_columns(specs=[None, None, None]))
        rects_int = _resolve(_flow.flow_columns(specs=3))
        for key in rects_list:
            assert rects_list[key].width == pytest.approx(rects_int[key].width)

    def test_custom_names(self) -> None:
        rects = _resolve(_flow.flow_columns(specs=2, names=["left", "right"]))
        assert "left" in rects
        assert "right" in rects

    def test_all_columns_share_same_y_and_height(self) -> None:
        rects = _resolve(_flow.flow_columns(specs=[50.0, None, 70.0]))
        assert len({r.y for r in rects.values()}) == 1
        assert len({r.height for r in rects.values()}) == 1


class TestFlowRows:
    def test_int_count_produces_equal_height_rows(self) -> None:
        rects = _resolve(_flow.flow_rows(specs=4))
        assert len(rects) == 4
        for r in rects.values():
            assert r.height == pytest.approx(50.0)
            assert r.width == pytest.approx(300.0)

    def test_int_rows_packed_top_to_bottom(self) -> None:
        rects = _resolve(_flow.flow_rows(specs=3))
        assert rects["row_0"].y == pytest.approx(0.0)
        assert rects["row_1"].y == pytest.approx(200.0 / 3)
        assert rects["row_2"].y == pytest.approx(400.0 / 3)

    def test_int_with_gap(self) -> None:
        rects = _resolve(_flow.flow_rows(specs=2, gap=10.0))
        assert rects["row_0"].height == pytest.approx(95.0)
        assert rects["row_1"].y == pytest.approx(105.0)

    def test_list_fixed_heights(self) -> None:
        rects = _resolve(_flow.flow_rows(specs=[60.0, 80.0]))
        assert rects["row_0"].height == pytest.approx(60.0)
        assert rects["row_1"].height == pytest.approx(80.0)
        assert rects["row_1"].y == pytest.approx(60.0)

    def test_list_mixed_fixed_and_stretch(self) -> None:
        rects = _resolve(_flow.flow_rows(specs=[40.0, None, 30.0]))
        assert rects["row_0"].height == pytest.approx(40.0)
        assert rects["row_2"].height == pytest.approx(30.0)
        assert rects["row_1"].height == pytest.approx(130.0)  # 200 - 40 - 30

    def test_custom_names(self) -> None:
        rects = _resolve(_flow.flow_rows(specs=2, names=["top", "bottom"]))
        assert "top" in rects
        assert "bottom" in rects

    def test_all_rows_share_same_x_and_width(self) -> None:
        rects = _resolve(_flow.flow_rows(specs=[50.0, None, 30.0]))
        assert len({r.x for r in rects.values()}) == 1
        assert len({r.width for r in rects.values()}) == 1
