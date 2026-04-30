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
from tenderness.layout_engines.minimal_flexbox.templates.documents import MinimalFlexBoxTemplateDocuments

_ENGINE = MinimalFlexBox()
_C300x200 = Rectangle(x=0, y=0, width=300, height=200)
_docs = MinimalFlexBoxTemplateDocuments()


def _resolve(node: MinimalFlexNode, container: Rectangle = _C300x200) -> dict[str, Rectangle]:
    return {n.name: r for n, r in _ENGINE.resolve_tree(container, node) if n.name is not None}


class TestHeaderSectionedColumns:
    def test_header_fixed_height(self) -> None:
        rects = _resolve(
            _docs.header_sectioned_columns(
                header_height=30.0,
                section_label_height=20.0,
                col_specs=2,
                n_sections=2,
            )
        )
        assert rects["header"].height == pytest.approx(30.0)
        assert rects["header"].y == pytest.approx(0.0)
        assert rects["header"].width == pytest.approx(300.0)

    def test_int_col_specs_equal_width_columns(self) -> None:
        rects = _resolve(
            _docs.header_sectioned_columns(
                header_height=30.0,
                section_label_height=20.0,
                col_specs=2,
                n_sections=1,
            )
        )
        assert rects["col_0_section_0_label"].width == pytest.approx(150.0)
        assert rects["col_1_section_0_label"].width == pytest.approx(150.0)

    def test_section_labels_fixed_height(self) -> None:
        rects = _resolve(
            _docs.header_sectioned_columns(
                header_height=30.0,
                section_label_height=20.0,
                col_specs=2,
                n_sections=2,
            )
        )
        for c in range(2):
            for s in range(2):
                assert rects[f"col_{c}_section_{s}_label"].height == pytest.approx(20.0)

    def test_section_content_fixed_height(self) -> None:
        rects = _resolve(
            _docs.header_sectioned_columns(
                header_height=30.0,
                section_label_height=20.0,
                col_specs=1,
                n_sections=2,
                section_content_height=50.0,
            )
        )
        assert rects["col_0_section_0_content"].height == pytest.approx(50.0)
        assert rects["col_0_section_1_content"].height == pytest.approx(50.0)

    def test_section_content_fixed_position(self) -> None:
        # header=30, label=20, content=50, no gaps
        # section 0: label y=30, content y=50; section 1: label y=100, content y=120
        rects = _resolve(
            _docs.header_sectioned_columns(
                header_height=30.0,
                section_label_height=20.0,
                col_specs=1,
                n_sections=2,
                section_content_height=50.0,
            )
        )
        assert rects["col_0_section_0_label"].y == pytest.approx(30.0)
        assert rects["col_0_section_0_content"].y == pytest.approx(50.0)
        assert rects["col_0_section_1_label"].y == pytest.approx(100.0)
        assert rects["col_0_section_1_content"].y == pytest.approx(120.0)

    def test_section_content_fixed_with_section_gap(self) -> None:
        # header=30, label=20, content=50, gap=5
        # section 0: label y=30, content y=55; section 1: label y=110, content y=135
        rects = _resolve(
            _docs.header_sectioned_columns(
                header_height=30.0,
                section_label_height=20.0,
                col_specs=1,
                n_sections=2,
                section_content_height=50.0,
                section_gap=5.0,
            )
        )
        assert rects["col_0_section_0_content"].y == pytest.approx(55.0)
        assert rects["col_0_section_1_label"].y == pytest.approx(110.0)
        assert rects["col_0_section_1_content"].y == pytest.approx(135.0)

    def test_section_content_fixed_label_stretches(self) -> None:
        # label=None (stretch), content=50 fixed; body=170, 1 section → label fills remaining 120px
        rects = _resolve(
            _docs.header_sectioned_columns(
                header_height=30.0,
                section_label_height=None,
                col_specs=1,
                n_sections=1,
                section_content_height=50.0,
            )
        )
        assert rects["col_0_section_0_content"].height == pytest.approx(50.0)
        assert rects["col_0_section_0_label"].height == pytest.approx(120.0)

    def test_section_label_list_per_section(self) -> None:
        # label_heights=[15, 25], content stretches
        # body=170, labels=15+25=40, remaining=130 split equally: 65 each
        rects = _resolve(
            _docs.header_sectioned_columns(
                header_height=30.0,
                section_label_height=[15.0, 25.0],
                col_specs=1,
                n_sections=2,
            )
        )
        assert rects["col_0_section_0_label"].height == pytest.approx(15.0)
        assert rects["col_0_section_1_label"].height == pytest.approx(25.0)
        assert rects["col_0_section_0_content"].height == pytest.approx(65.0)
        assert rects["col_0_section_1_content"].height == pytest.approx(65.0)
        assert rects["col_0_section_1_label"].y == pytest.approx(30.0 + 15.0 + 65.0)

    def test_section_label_list_length_mismatch_raises(self) -> None:
        with pytest.raises(ValueError, match="section_label_height"):
            _docs.header_sectioned_columns(
                header_height=30.0,
                section_label_height=[10.0, 20.0, 30.0],
                col_specs=1,
                n_sections=2,
            )

    def test_section_content_list_per_section(self) -> None:
        # 3 sections: label=10 each, contents=[40, 80, None]
        # body=170, labels=30, fixed contents=120, remaining for stretch=170-30-120=20
        rects = _resolve(
            _docs.header_sectioned_columns(
                header_height=30.0,
                section_label_height=10.0,
                col_specs=1,
                n_sections=3,
                section_content_height=[40.0, 80.0, None],
            )
        )
        assert rects["col_0_section_0_content"].height == pytest.approx(40.0)
        assert rects["col_0_section_1_content"].height == pytest.approx(80.0)
        assert rects["col_0_section_2_content"].height == pytest.approx(20.0)

    def test_section_content_list_length_mismatch_raises(self) -> None:
        with pytest.raises(ValueError, match="section_content_height"):
            _docs.header_sectioned_columns(
                header_height=30.0,
                section_label_height=20.0,
                col_specs=1,
                n_sections=2,
                section_content_height=[50.0, 60.0, 70.0],
            )

    def test_section_content_stretches(self) -> None:
        rects = _resolve(
            _docs.header_sectioned_columns(
                header_height=30.0,
                section_label_height=20.0,
                col_specs=1,
                n_sections=2,
            )
        )
        # 200 - 30 (header) - 2*20 (labels) = 130 split equally across 2 contents
        assert rects["col_0_section_0_content"].height == pytest.approx(65.0)
        assert rects["col_0_section_1_content"].height == pytest.approx(65.0)

    def test_header_gap(self) -> None:
        rects = _resolve(
            _docs.header_sectioned_columns(
                header_height=30.0,
                section_label_height=20.0,
                col_specs=1,
                n_sections=1,
                header_gap=8.0,
            )
        )
        assert rects["col_0_section_0_label"].y == pytest.approx(38.0)

    def test_section_gap(self) -> None:
        rects = _resolve(
            _docs.header_sectioned_columns(
                header_height=30.0,
                section_label_height=20.0,
                col_specs=1,
                n_sections=2,
                section_gap=4.0,
            )
        )
        # label ends at 30+20=50, content starts at 50+4=54
        assert rects["col_0_section_0_content"].y == pytest.approx(54.0)

    def test_col_gap(self) -> None:
        rects = _resolve(
            _docs.header_sectioned_columns(
                header_height=30.0,
                section_label_height=20.0,
                col_specs=2,
                n_sections=1,
                col_gap=10.0,
            )
        )
        assert rects["col_0_section_0_label"].width == pytest.approx(145.0)
        assert rects["col_1_section_0_label"].x == pytest.approx(155.0)

    def test_list_col_specs_fixed_and_stretch(self) -> None:
        rects = _resolve(
            _docs.header_sectioned_columns(
                header_height=30.0,
                section_label_height=20.0,
                col_specs=[80.0, None],
                n_sections=1,
            )
        )
        assert rects["col_0_section_0_label"].width == pytest.approx(80.0)
        assert rects["col_1_section_0_label"].width == pytest.approx(220.0)

    def test_single_column(self) -> None:
        rects = _resolve(
            _docs.header_sectioned_columns(
                header_height=30.0,
                section_label_height=20.0,
                col_specs=1,
                n_sections=3,
            )
        )
        assert len(rects) == 1 + 3 * 2  # header + 3 * (label + content)
        assert rects["col_0_section_0_label"].width == pytest.approx(300.0)

    def test_name_index_formula(self) -> None:
        # 2 cols * 2 sections * 2 (label+content) + 1 header = 9 names total
        names = ["hdr"] + [f"n_{i}" for i in range(8)]
        rects = _resolve(
            _docs.header_sectioned_columns(
                header_height=30.0,
                section_label_height=20.0,
                col_specs=2,
                n_sections=2,
                names=names,
            )
        )
        assert "hdr" in rects
        # col=0, section=0, label: index 1 + 0*4 + 0*2 = 1
        assert "n_0" in rects
        # col=1, section=0, label: index 1 + 1*4 + 0*2 = 5
        assert "n_4" in rects

    def test_header_none_stretches_equally_with_body(self) -> None:
        # header and body both flex_grow=1 → each 100px of 200px container
        rects = _resolve(
            _docs.header_sectioned_columns(
                header_height=None,
                section_label_height=20.0,
                col_specs=1,
                n_sections=1,
            )
        )
        assert rects["header"].height == pytest.approx(100.0)
        assert rects["col_0_section_0_label"].height == pytest.approx(20.0)
        assert rects["col_0_section_0_content"].height == pytest.approx(80.0)

    def test_section_label_none_stretches(self) -> None:
        # header=30, body=170; 1 col, 2 sections: label+content+label+content all flex_grow=1 → each 42.5px
        rects = _resolve(
            _docs.header_sectioned_columns(
                header_height=30.0,
                section_label_height=None,
                col_specs=1,
                n_sections=2,
            )
        )
        assert rects["col_0_section_0_label"].height == pytest.approx(42.5)
        assert rects["col_0_section_0_content"].height == pytest.approx(42.5)
        assert rects["col_0_section_1_label"].height == pytest.approx(42.5)
        assert rects["col_0_section_1_content"].height == pytest.approx(42.5)

    def test_header_none_full_width(self) -> None:
        rects = _resolve(
            _docs.header_sectioned_columns(
                header_height=None,
                section_label_height=20.0,
                col_specs=1,
                n_sections=1,
            )
        )
        assert rects["header"].width == pytest.approx(300.0)

    def test_header_and_section_label_both_none(self) -> None:
        # header(stretch) + body(stretch) → each 100px; within body label(stretch) + content(stretch) → each 50px
        rects = _resolve(
            _docs.header_sectioned_columns(
                header_height=None,
                section_label_height=None,
                col_specs=1,
                n_sections=1,
            )
        )
        assert rects["header"].height == pytest.approx(100.0)
        assert rects["col_0_section_0_label"].height == pytest.approx(50.0)
        assert rects["col_0_section_0_content"].height == pytest.approx(50.0)

    def test_section_label_none_with_section_gap(self) -> None:
        # header=30 → body=170; 1 col, 2 sections, 4 stretch items with 3 gaps of 4px
        # available = 170 - 3*4 = 158, each = 39.5px
        rects = _resolve(
            _docs.header_sectioned_columns(
                header_height=30.0,
                section_label_height=None,
                col_specs=1,
                n_sections=2,
                section_gap=4.0,
            )
        )
        assert rects["col_0_section_0_label"].height == pytest.approx(39.5)
        assert rects["col_0_section_0_content"].height == pytest.approx(39.5)
        assert rects["col_0_section_1_label"].y == pytest.approx(30.0 + 39.5 + 4.0 + 39.5 + 4.0)

    def test_header_none_with_header_gap(self) -> None:
        # header(stretch) + body(stretch) with gap=10 → available=190, each=95px
        rects = _resolve(
            _docs.header_sectioned_columns(
                header_height=None,
                section_label_height=20.0,
                col_specs=1,
                n_sections=1,
                header_gap=10.0,
            )
        )
        assert rects["header"].height == pytest.approx(95.0)
        assert rects["col_0_section_0_label"].y == pytest.approx(105.0)
