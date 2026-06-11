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
from tenderness.layout_engines.minimal_flexbox.templates.base import CaptionSpec
from tenderness.layout_engines.minimal_flexbox.templates.tables import MinimalFlexBoxTemplateTables

_ENGINE = MinimalFlexBox()
_C360x240 = Rectangle(x=0, y=0, width=360, height=240)  # TestTableBasic
_C400x300 = Rectangle(x=0, y=0, width=400, height=300)  # TestTableHeaderBasic
_tables = MinimalFlexBoxTemplateTables()


def _resolve(node: MinimalFlexNode, container: Rectangle = _C360x240) -> dict[str, Rectangle]:
    return {n.name: r for n, r in _ENGINE.resolve_tree(container, node) if n.name is not None}


class TestTableBasic:
    # Container: 360w x 240h
    def test_uniform_grid_int_int(self) -> None:
        rects = _resolve(_tables.table_basic(row_specs=2, col_specs=3), _C360x240)
        assert len(rects) == 6
        for r in rects.values():
            assert r.width == pytest.approx(120.0)
            assert r.height == pytest.approx(120.0)

    def test_uniform_grid_row_major_order(self) -> None:
        rects = _resolve(_tables.table_basic(row_specs=2, col_specs=3), _C360x240)
        assert rects["cell_0_0"].x == pytest.approx(0.0)
        assert rects["cell_0_1"].x == pytest.approx(120.0)
        assert rects["cell_0_2"].x == pytest.approx(240.0)
        assert rects["cell_1_0"].y == pytest.approx(120.0)

    def test_fixed_col_widths(self) -> None:
        rects = _resolve(_tables.table_basic(row_specs=2, col_specs=[80.0, None, 60.0]), _C360x240)
        assert rects["cell_0_0"].width == pytest.approx(80.0)
        assert rects["cell_0_2"].width == pytest.approx(60.0)
        assert rects["cell_0_1"].width == pytest.approx(220.0)  # 360 - 80 - 60

    def test_fixed_row_heights(self) -> None:
        rects = _resolve(_tables.table_basic(row_specs=[40.0, None, 30.0], col_specs=2), _C360x240)
        assert rects["cell_0_0"].height == pytest.approx(40.0)
        assert rects["cell_2_0"].height == pytest.approx(30.0)
        assert rects["cell_1_0"].height == pytest.approx(170.0)  # 240 - 40 - 30

    def test_fully_custom_row_and_col_specs(self) -> None:
        rects = _resolve(_tables.table_basic(row_specs=[50.0, None], col_specs=[100.0, None]), _C360x240)
        assert rects["cell_0_0"].width == pytest.approx(100.0)
        assert rects["cell_0_0"].height == pytest.approx(50.0)
        assert rects["cell_0_1"].width == pytest.approx(260.0)  # 360 - 100
        assert rects["cell_1_0"].height == pytest.approx(190.0)  # 240 - 50

    def test_row_gap(self) -> None:
        # 2 rows, gap=10 → each (240-10)/2=115
        rects = _resolve(_tables.table_basic(row_specs=2, col_specs=1, row_gap=10.0), _C360x240)
        assert rects["cell_0_0"].height == pytest.approx(115.0)
        assert rects["cell_1_0"].y == pytest.approx(125.0)

    def test_col_gap(self) -> None:
        # 2 cols, gap=10 → each (360-10)/2=175
        rects = _resolve(_tables.table_basic(row_specs=1, col_specs=2, col_gap=10.0), _C360x240)
        assert rects["cell_0_0"].width == pytest.approx(175.0)
        assert rects["cell_0_1"].x == pytest.approx(185.0)

    def test_caption_below(self) -> None:
        rects = _resolve(
            _tables.table_basic(row_specs=2, col_specs=2, caption=CaptionSpec(height=20.0, gap=4.0)), _C360x240
        )
        assert "caption" in rects
        assert rects["caption"].height == pytest.approx(20.0)
        assert rects["caption"].y == pytest.approx(220.0)  # table=216, gap=4, caption at 220

    def test_caption_above(self) -> None:
        rects = _resolve(
            _tables.table_basic(row_specs=2, col_specs=2, caption=CaptionSpec(height=20.0, gap=4.0, on_top=True)),
            _C360x240,
        )
        assert rects["caption"].y == pytest.approx(0.0)
        assert rects["cell_0_0"].y == pytest.approx(24.0)

    def test_caption_custom_name(self) -> None:
        rects = _resolve(
            _tables.table_basic(row_specs=1, col_specs=1, caption=CaptionSpec(height=10.0, name="title")), _C360x240
        )
        assert "title" in rects

    def test_custom_cell_names(self) -> None:
        rects = _resolve(_tables.table_basic(row_specs=2, col_specs=2, names=["a", "b", "c", "d"]), _C360x240)
        assert set(rects.keys()) == {"a", "b", "c", "d"}

    def test_caption_none_stretches_equally_with_table(self) -> None:
        # table and caption both flex_grow=1 → each 120 of 240 container
        rects = _resolve(_tables.table_basic(row_specs=2, col_specs=2, caption=CaptionSpec(height=None)), _C360x240)
        assert rects["caption"].height == pytest.approx(120.0)
        assert rects["cell_0_0"].height == pytest.approx(60.0)

    def test_caption_none_above(self) -> None:
        rects = _resolve(
            _tables.table_basic(row_specs=1, col_specs=1, caption=CaptionSpec(height=None, on_top=True)), _C360x240
        )
        assert rects["caption"].y == pytest.approx(0.0)
        assert rects["cell_0_0"].y == pytest.approx(120.0)

    def test_caption_none_with_gap(self) -> None:
        # table(stretch) + caption(stretch) with gap=4 → available=236, each=118
        rects = _resolve(
            _tables.table_basic(row_specs=2, col_specs=2, caption=CaptionSpec(height=None, gap=4.0)), _C360x240
        )
        assert rects["caption"].height == pytest.approx(118.0)
        assert rects["caption"].y == pytest.approx(122.0)
        assert rects["cell_0_0"].height == pytest.approx(59.0)

    def test_list_of_none_equivalent_to_int(self) -> None:
        rects_int = _resolve(_tables.table_basic(row_specs=2, col_specs=3), _C360x240)
        rects_list = _resolve(_tables.table_basic(row_specs=[None, None], col_specs=[None, None, None]), _C360x240)
        for key in rects_int:
            assert rects_int[key].width == pytest.approx(rects_list[key].width)
            assert rects_int[key].height == pytest.approx(rects_list[key].height)

    def test_single_cell(self) -> None:
        rects = _resolve(_tables.table_basic(row_specs=1, col_specs=1), _C360x240)
        assert rects["cell_0_0"].width == pytest.approx(360.0)
        assert rects["cell_0_0"].height == pytest.approx(240.0)

    def test_all_fixed_rows_and_cols(self) -> None:
        rects = _resolve(_tables.table_basic(row_specs=[50.0, 60.0], col_specs=[80.0, 100.0]), _C360x240)
        assert rects["cell_0_0"].width == pytest.approx(80.0)
        assert rects["cell_0_0"].height == pytest.approx(50.0)
        assert rects["cell_1_1"].width == pytest.approx(100.0)
        assert rects["cell_1_1"].height == pytest.approx(60.0)

    def test_row_and_col_gap_together(self) -> None:
        # 2x2, row_gap=10, col_gap=20 → each (360-20)/2=170 wide, (240-10)/2=115 tall
        rects = _resolve(_tables.table_basic(row_specs=2, col_specs=2, row_gap=10.0, col_gap=20.0), _C360x240)
        assert rects["cell_0_0"].width == pytest.approx(170.0)
        assert rects["cell_0_0"].height == pytest.approx(115.0)
        assert rects["cell_1_1"].x == pytest.approx(190.0)
        assert rects["cell_1_1"].y == pytest.approx(125.0)

    def test_four_row_y_positions(self) -> None:
        # 4 rows → each 240/4=60
        rects = _resolve(_tables.table_basic(row_specs=4, col_specs=1), _C360x240)
        assert rects["cell_0_0"].y == pytest.approx(0.0)
        assert rects["cell_1_0"].y == pytest.approx(60.0)
        assert rects["cell_2_0"].y == pytest.approx(120.0)
        assert rects["cell_3_0"].y == pytest.approx(180.0)

    def test_col_gap_with_fixed_col(self) -> None:
        # col_specs=[80, None], col_gap=10 → stretch=360-80-10=270
        rects = _resolve(_tables.table_basic(row_specs=1, col_specs=[80.0, None], col_gap=10.0), _C360x240)
        assert rects["cell_0_0"].width == pytest.approx(80.0)
        assert rects["cell_0_1"].width == pytest.approx(270.0)
        assert rects["cell_0_1"].x == pytest.approx(90.0)

    def test_row_gap_with_fixed_row(self) -> None:
        # row_specs=[40, None], row_gap=10 → stretch=240-40-10=190
        rects = _resolve(_tables.table_basic(row_specs=[40.0, None], col_specs=1, row_gap=10.0), _C360x240)
        assert rects["cell_0_0"].height == pytest.approx(40.0)
        assert rects["cell_1_0"].height == pytest.approx(190.0)
        assert rects["cell_1_0"].y == pytest.approx(50.0)


class TestTableHeaderBasic:
    # Container: 400w x 300h
    def test_header_has_fixed_height(self) -> None:
        rects = _resolve(_tables.table_header_basic(row_specs=2, col_specs=3, header_height=40.0), _C400x300)
        for c in range(3):
            assert rects[f"header_cell_{c}"].height == pytest.approx(40.0)
            assert rects[f"header_cell_{c}"].y == pytest.approx(0.0)

    def test_body_rows_stretch_equally(self) -> None:
        # header=40, body=260; 2 rows → each 130
        rects = _resolve(_tables.table_header_basic(row_specs=2, col_specs=2, header_height=40.0), _C400x300)
        assert rects["cell_0_0"].height == pytest.approx(130.0)
        assert rects["cell_1_0"].height == pytest.approx(130.0)

    def test_body_starts_after_header(self) -> None:
        rects = _resolve(_tables.table_header_basic(row_specs=2, col_specs=2, header_height=40.0), _C400x300)
        assert rects["cell_0_0"].y == pytest.approx(40.0)

    def test_header_and_body_same_column_widths(self) -> None:
        rects = _resolve(_tables.table_header_basic(row_specs=1, col_specs=3, header_height=30.0), _C400x300)
        assert rects["header_cell_0"].width == pytest.approx(rects["cell_0_0"].width)

    def test_header_gap_applied(self) -> None:
        rects = _resolve(
            _tables.table_header_basic(row_specs=1, col_specs=2, header_height=40.0, header_gap=8.0), _C400x300
        )
        assert rects["cell_0_0"].y == pytest.approx(48.0)

    def test_row_gap_between_body_rows(self) -> None:
        # header=30, body=270; row_gap=10 → (270-10)/2=130 each
        rects = _resolve(
            _tables.table_header_basic(row_specs=2, col_specs=1, header_height=30.0, row_gap=10.0), _C400x300
        )
        assert rects["cell_0_0"].y == pytest.approx(30.0)
        assert rects["cell_1_0"].y == pytest.approx(170.0)

    def test_col_gap_applied(self) -> None:
        # 2 cols, gap=10 → each (400-10)/2=195
        rects = _resolve(
            _tables.table_header_basic(row_specs=1, col_specs=2, header_height=30.0, col_gap=10.0), _C400x300
        )
        assert rects["header_cell_0"].width == pytest.approx(195.0)
        assert rects["header_cell_1"].x == pytest.approx(205.0)

    def test_name_indices(self) -> None:
        rects = _resolve(
            _tables.table_header_basic(row_specs=1, col_specs=2, header_height=30.0, names=["h0", "h1", "b00", "b01"]),
            _C400x300,
        )
        assert "h0" in rects
        assert "h1" in rects
        assert "b00" in rects
        assert "b01" in rects

    def test_caption(self) -> None:
        rects = _resolve(
            _tables.table_header_basic(row_specs=2, col_specs=2, header_height=30.0, caption=CaptionSpec(height=20.0)),
            _C400x300,
        )
        assert "caption" in rects
        assert rects["caption"].height == pytest.approx(20.0)

    def test_header_none_stretches_with_body(self) -> None:
        # header(stretch) + body(stretch) → each 150; body 2 rows → each 75
        rects = _resolve(_tables.table_header_basic(row_specs=2, col_specs=2, header_height=None), _C400x300)
        assert rects["header_cell_0"].height == pytest.approx(150.0)
        assert rects["cell_0_0"].height == pytest.approx(75.0)
        assert rects["cell_1_0"].height == pytest.approx(75.0)

    def test_header_none_body_starts_after_header(self) -> None:
        rects = _resolve(_tables.table_header_basic(row_specs=1, col_specs=2, header_height=None), _C400x300)
        assert rects["cell_0_0"].y == pytest.approx(rects["header_cell_0"].height)

    def test_header_none_with_row_gap(self) -> None:
        # header(stretch) + body(stretch) → each 150; body rows with row_gap=10: (150-10)/2=70 each
        rects = _resolve(
            _tables.table_header_basic(row_specs=2, col_specs=2, header_height=None, row_gap=10.0), _C400x300
        )
        assert rects["header_cell_0"].height == pytest.approx(150.0)
        assert rects["cell_0_0"].y == pytest.approx(150.0)
        assert rects["cell_1_0"].y == pytest.approx(230.0)

    def test_fixed_col_widths(self) -> None:
        # [80, None, 60] → stretch=400-80-60=260
        rects = _resolve(
            _tables.table_header_basic(row_specs=1, col_specs=[80.0, None, 60.0], header_height=30.0), _C400x300
        )
        assert rects["header_cell_0"].width == pytest.approx(80.0)
        assert rects["header_cell_2"].width == pytest.approx(60.0)
        assert rects["header_cell_1"].width == pytest.approx(260.0)
        assert rects["cell_0_0"].width == pytest.approx(80.0)
        assert rects["cell_0_1"].width == pytest.approx(260.0)

    def test_fixed_body_row_heights(self) -> None:
        rects = _resolve(_tables.table_header_basic(row_specs=[50.0, 60.0], col_specs=2, header_height=30.0), _C400x300)
        assert rects["cell_0_0"].height == pytest.approx(50.0)
        assert rects["cell_1_0"].height == pytest.approx(60.0)

    def test_mixed_body_row_specs(self) -> None:
        # header=30, fixed body row=50, stretch body row fills 300-30-50=220
        rects = _resolve(_tables.table_header_basic(row_specs=[50.0, None], col_specs=1, header_height=30.0), _C400x300)
        assert rects["cell_0_0"].height == pytest.approx(50.0)
        assert rects["cell_1_0"].height == pytest.approx(220.0)

    def test_header_gap_and_row_gap_independent(self) -> None:
        # header=30, header_gap=10 → body=300-30-10=260; 2 rows+row_gap=6 → (260-6)/2=127 each
        rects = _resolve(
            _tables.table_header_basic(row_specs=2, col_specs=1, header_height=30.0, header_gap=10.0, row_gap=6.0),
            _C400x300,
        )
        assert rects["cell_0_0"].y == pytest.approx(40.0)
        assert rects["cell_0_0"].height == pytest.approx(127.0)
        assert rects["cell_1_0"].y == pytest.approx(173.0)

    def test_header_cells_full_width(self) -> None:
        rects = _resolve(_tables.table_header_basic(row_specs=1, col_specs=3, header_height=30.0), _C400x300)
        total = sum(rects[f"header_cell_{c}"].width for c in range(3))
        assert total == pytest.approx(400.0)

    def test_caption_above(self) -> None:
        rects = _resolve(
            _tables.table_header_basic(
                row_specs=1, col_specs=1, header_height=30.0, caption=CaptionSpec(height=20.0, on_top=True)
            ),
            _C400x300,
        )
        assert rects["caption"].y == pytest.approx(0.0)
        assert rects["header_cell_0"].y == pytest.approx(20.0)
        assert rects["cell_0_0"].y == pytest.approx(50.0)

    def test_fixed_col_widths_with_col_gap(self) -> None:
        # [80, None], col_gap=20 → stretch=400-80-20=300
        rects = _resolve(
            _tables.table_header_basic(row_specs=1, col_specs=[80.0, None], header_height=30.0, col_gap=20.0),
            _C400x300,
        )
        assert rects["header_cell_0"].width == pytest.approx(80.0)
        assert rects["header_cell_1"].width == pytest.approx(300.0)
        assert rects["cell_0_0"].width == pytest.approx(80.0)
        assert rects["cell_0_1"].width == pytest.approx(300.0)

    def test_all_fixed_col_specs(self) -> None:
        rects = _resolve(
            _tables.table_header_basic(row_specs=1, col_specs=[100.0, 80.0], header_height=30.0), _C400x300
        )
        assert rects["header_cell_0"].width == pytest.approx(100.0)
        assert rects["header_cell_1"].width == pytest.approx(80.0)
        assert rects["cell_0_0"].width == pytest.approx(100.0)
        assert rects["cell_0_1"].width == pytest.approx(80.0)
