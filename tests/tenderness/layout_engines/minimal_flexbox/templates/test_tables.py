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
_C300x200 = Rectangle(x=0, y=0, width=300, height=200)
_tables = MinimalFlexBoxTemplateTables()


def _resolve(node: MinimalFlexNode, container: Rectangle = _C300x200) -> dict[str, Rectangle]:
    return {n.name: r for n, r in _ENGINE.resolve_tree(container, node) if n.name is not None}


class TestTableCustom:
    def test_uniform_grid_int_int(self) -> None:
        rects = _resolve(_tables.table_custom(row_specs=2, col_specs=3))
        assert len(rects) == 6
        for r in rects.values():
            assert r.width == pytest.approx(100.0)
            assert r.height == pytest.approx(100.0)

    def test_uniform_grid_row_major_order(self) -> None:
        rects = _resolve(_tables.table_custom(row_specs=2, col_specs=3))
        assert rects["cell_0_0"].x == pytest.approx(0.0)
        assert rects["cell_0_1"].x == pytest.approx(100.0)
        assert rects["cell_0_2"].x == pytest.approx(200.0)
        assert rects["cell_1_0"].y == pytest.approx(100.0)

    def test_fixed_col_widths(self) -> None:
        rects = _resolve(_tables.table_custom(row_specs=2, col_specs=[80.0, None, 60.0]))
        assert rects["cell_0_0"].width == pytest.approx(80.0)
        assert rects["cell_0_2"].width == pytest.approx(60.0)
        assert rects["cell_0_1"].width == pytest.approx(160.0)  # 300 - 80 - 60

    def test_fixed_row_heights(self) -> None:
        rects = _resolve(_tables.table_custom(row_specs=[40.0, None, 30.0], col_specs=2))
        assert rects["cell_0_0"].height == pytest.approx(40.0)
        assert rects["cell_2_0"].height == pytest.approx(30.0)
        assert rects["cell_1_0"].height == pytest.approx(130.0)  # 200 - 40 - 30

    def test_fully_custom_row_and_col_specs(self) -> None:
        rects = _resolve(_tables.table_custom(row_specs=[50.0, None], col_specs=[100.0, None]))
        assert rects["cell_0_0"].width == pytest.approx(100.0)
        assert rects["cell_0_0"].height == pytest.approx(50.0)
        assert rects["cell_0_1"].width == pytest.approx(200.0)
        assert rects["cell_1_0"].height == pytest.approx(150.0)

    def test_row_gap(self) -> None:
        rects = _resolve(_tables.table_custom(row_specs=2, col_specs=1, row_gap=10.0))
        assert rects["cell_0_0"].height == pytest.approx(95.0)
        assert rects["cell_1_0"].y == pytest.approx(105.0)

    def test_col_gap(self) -> None:
        rects = _resolve(_tables.table_custom(row_specs=1, col_specs=2, col_gap=10.0))
        assert rects["cell_0_0"].width == pytest.approx(145.0)
        assert rects["cell_0_1"].x == pytest.approx(155.0)

    def test_caption_below(self) -> None:
        rects = _resolve(_tables.table_custom(row_specs=2, col_specs=2, caption=CaptionSpec(height=20.0, gap=4.0)))
        assert "caption" in rects
        assert rects["caption"].height == pytest.approx(20.0)
        assert rects["caption"].y == pytest.approx(180.0)  # table=176, gap=4, caption at 180

    def test_caption_above(self) -> None:
        rects = _resolve(
            _tables.table_custom(row_specs=2, col_specs=2, caption=CaptionSpec(height=20.0, gap=4.0, on_top=True))
        )
        assert rects["caption"].y == pytest.approx(0.0)
        assert rects["cell_0_0"].y == pytest.approx(24.0)

    def test_caption_custom_name(self) -> None:
        rects = _resolve(_tables.table_custom(row_specs=1, col_specs=1, caption=CaptionSpec(height=10.0, name="title")))
        assert "title" in rects

    def test_custom_cell_names(self) -> None:
        rects = _resolve(_tables.table_custom(row_specs=2, col_specs=2, names=["a", "b", "c", "d"]))
        assert set(rects.keys()) == {"a", "b", "c", "d"}

    def test_caption_none_stretches_equally_with_table(self) -> None:
        # table and caption both flex_grow=1 → each 100px of 200px container
        rects = _resolve(_tables.table_custom(row_specs=2, col_specs=2, caption=CaptionSpec(height=None)))
        assert rects["caption"].height == pytest.approx(100.0)
        assert rects["cell_0_0"].height == pytest.approx(50.0)

    def test_caption_none_above(self) -> None:
        rects = _resolve(_tables.table_custom(row_specs=1, col_specs=1, caption=CaptionSpec(height=None, on_top=True)))
        assert rects["caption"].y == pytest.approx(0.0)
        assert rects["cell_0_0"].y == pytest.approx(100.0)

    def test_caption_none_with_gap(self) -> None:
        # table(stretch) + caption(stretch) with gap=4 → available=196, each=98px
        rects = _resolve(_tables.table_custom(row_specs=2, col_specs=2, caption=CaptionSpec(height=None, gap=4.0)))
        assert rects["caption"].height == pytest.approx(98.0)
        assert rects["caption"].y == pytest.approx(102.0)
        assert rects["cell_0_0"].height == pytest.approx(49.0)

    def test_list_of_none_equivalent_to_int(self) -> None:
        rects_int = _resolve(_tables.table_custom(row_specs=2, col_specs=3))
        rects_list = _resolve(_tables.table_custom(row_specs=[None, None], col_specs=[None, None, None]))
        for key in rects_int:
            assert rects_int[key].width == pytest.approx(rects_list[key].width)
            assert rects_int[key].height == pytest.approx(rects_list[key].height)


class TestTableHeaderBody:
    def test_header_has_fixed_height(self) -> None:
        rects = _resolve(_tables.table_header_body(body_rows=2, cols=3, header_height=40.0))
        for c in range(3):
            assert rects[f"header_{c}"].height == pytest.approx(40.0)
            assert rects[f"header_{c}"].y == pytest.approx(0.0)

    def test_body_rows_stretch_equally(self) -> None:
        rects = _resolve(_tables.table_header_body(body_rows=2, cols=2, header_height=40.0))
        assert rects["body_0_0"].height == pytest.approx(80.0)
        assert rects["body_1_0"].height == pytest.approx(80.0)

    def test_body_starts_after_header(self) -> None:
        rects = _resolve(_tables.table_header_body(body_rows=2, cols=2, header_height=40.0))
        assert rects["body_0_0"].y == pytest.approx(40.0)

    def test_header_and_body_same_column_widths(self) -> None:
        rects = _resolve(_tables.table_header_body(body_rows=1, cols=3, header_height=30.0))
        assert rects["header_0"].width == pytest.approx(rects["body_0_0"].width)

    def test_row_gap_applied(self) -> None:
        rects = _resolve(_tables.table_header_body(body_rows=1, cols=2, header_height=40.0, row_gap=8.0))
        assert rects["body_0_0"].y == pytest.approx(48.0)

    def test_col_gap_applied(self) -> None:
        rects = _resolve(_tables.table_header_body(body_rows=1, cols=2, header_height=30.0, col_gap=10.0))
        assert rects["header_0"].width == pytest.approx(145.0)
        assert rects["header_1"].x == pytest.approx(155.0)

    def test_name_indices(self) -> None:
        rects = _resolve(
            _tables.table_header_body(body_rows=1, cols=2, header_height=30.0, names=["h0", "h1", "b00", "b01"])
        )
        assert "h0" in rects
        assert "h1" in rects
        assert "b00" in rects
        assert "b01" in rects

    def test_caption(self) -> None:
        rects = _resolve(
            _tables.table_header_body(body_rows=2, cols=2, header_height=30.0, caption=CaptionSpec(height=20.0))
        )
        assert "caption" in rects
        assert rects["caption"].height == pytest.approx(20.0)

    def test_header_none_stretches_equally_with_body_rows(self) -> None:
        # header and 2 body rows all flex_grow=1 → each 200/3 ≈ 66.666px
        rects = _resolve(_tables.table_header_body(body_rows=2, cols=2, header_height=None))
        expected = pytest.approx(200.0 / 3)
        assert rects["header_0"].height == expected
        assert rects["body_0_0"].height == expected
        assert rects["body_1_0"].height == expected

    def test_header_none_body_starts_after_header(self) -> None:
        rects = _resolve(_tables.table_header_body(body_rows=1, cols=2, header_height=None))
        assert rects["body_0_0"].y == pytest.approx(rects["header_0"].height)

    def test_header_none_with_row_gap(self) -> None:
        # header + 2 body rows, all stretch, 2 gaps of 10px → available=180, each=60px
        rects = _resolve(_tables.table_header_body(body_rows=2, cols=2, header_height=None, row_gap=10.0))
        assert rects["header_0"].height == pytest.approx(60.0)
        assert rects["body_0_0"].y == pytest.approx(70.0)
        assert rects["body_1_0"].y == pytest.approx(140.0)
