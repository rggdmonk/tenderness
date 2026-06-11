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
_C300x200 = Rectangle(x=0, y=0, width=300, height=200)  # TestHeaderLabeledSections
_C400x300 = Rectangle(x=0, y=0, width=400, height=300)  # TestHeaderSections
_C360x240 = Rectangle(x=0, y=0, width=360, height=240)  # TestLabeledSections
_docs = MinimalFlexBoxTemplateDocuments()


def _resolve(node: MinimalFlexNode, container: Rectangle = _C300x200) -> dict[str, Rectangle]:
    return {n.name: r for n, r in _ENGINE.resolve_tree(container, node) if n.name is not None}


class TestHeaderLabeledSections:
    def test_header_fixed_height(self) -> None:
        rects = _resolve(
            _docs.header_labeled_sections(
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
            _docs.header_labeled_sections(
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
            _docs.header_labeled_sections(
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
            _docs.header_labeled_sections(
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
            _docs.header_labeled_sections(
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
        # header=30, label=20, content=50, section_gap=5 (between sections)
        # section 0: label y=30, content y=50; section 1: label y=105, content y=125
        rects = _resolve(
            _docs.header_labeled_sections(
                header_height=30.0,
                section_label_height=20.0,
                col_specs=1,
                n_sections=2,
                section_content_height=50.0,
                section_gap=5.0,
            )
        )
        assert rects["col_0_section_0_content"].y == pytest.approx(50.0)
        assert rects["col_0_section_1_label"].y == pytest.approx(105.0)
        assert rects["col_0_section_1_content"].y == pytest.approx(125.0)

    def test_section_content_fixed_label_stretches(self) -> None:
        # label=None (stretch), content=50 fixed; body=170, 1 section → label fills remaining 120px
        rects = _resolve(
            _docs.header_labeled_sections(
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
        # body=170, 2 stretch sections each get 85; section_0: label=15 content=70; section_1: label=25 content=60
        rects = _resolve(
            _docs.header_labeled_sections(
                header_height=30.0,
                section_label_height=[15.0, 25.0],
                col_specs=1,
                n_sections=2,
            )
        )
        assert rects["col_0_section_0_label"].height == pytest.approx(15.0)
        assert rects["col_0_section_1_label"].height == pytest.approx(25.0)
        assert rects["col_0_section_0_content"].height == pytest.approx(70.0)
        assert rects["col_0_section_1_content"].height == pytest.approx(60.0)
        assert rects["col_0_section_1_label"].y == pytest.approx(115.0)

    def test_section_label_list_length_mismatch_raises(self) -> None:
        with pytest.raises(ValueError, match="section_label_height"):
            _docs.header_labeled_sections(
                header_height=30.0,
                section_label_height=[10.0, 20.0, 30.0],
                col_specs=1,
                n_sections=2,
            )

    def test_section_content_list_per_section(self) -> None:
        # 3 sections: label=10 each, contents=[40, 80, None]
        # body=170, labels=30, fixed contents=120, remaining for stretch=170-30-120=20
        rects = _resolve(
            _docs.header_labeled_sections(
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
            _docs.header_labeled_sections(
                header_height=30.0,
                section_label_height=20.0,
                col_specs=1,
                n_sections=2,
                section_content_height=[50.0, 60.0, 70.0],
            )

    def test_section_content_stretches(self) -> None:
        rects = _resolve(
            _docs.header_labeled_sections(
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
            _docs.header_labeled_sections(
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
            _docs.header_labeled_sections(
                header_height=30.0,
                section_label_height=20.0,
                col_specs=1,
                n_sections=2,
                section_gap=4.0,
            )
        )
        # section_gap applies between sections; label_1 starts 4 units after content_0 ends
        content_0 = rects["col_0_section_0_content"]
        assert rects["col_0_section_1_label"].y == pytest.approx(content_0.y + content_0.height + 4.0)

    def test_col_gap(self) -> None:
        rects = _resolve(
            _docs.header_labeled_sections(
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
            _docs.header_labeled_sections(
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
            _docs.header_labeled_sections(
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
            _docs.header_labeled_sections(
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
            _docs.header_labeled_sections(
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
            _docs.header_labeled_sections(
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
            _docs.header_labeled_sections(
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
            _docs.header_labeled_sections(
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
        # header=30 → body=170; 1 col, 2 stretch sections with section_gap=4 between them
        # each section = (170-4)/2 = 83; within section: label=content=41.5
        rects = _resolve(
            _docs.header_labeled_sections(
                header_height=30.0,
                section_label_height=None,
                col_specs=1,
                n_sections=2,
                section_gap=4.0,
            )
        )
        assert rects["col_0_section_0_label"].height == pytest.approx(41.5)
        assert rects["col_0_section_0_content"].height == pytest.approx(41.5)
        assert rects["col_0_section_1_label"].y == pytest.approx(117.0)

    def test_label_content_gap(self) -> None:
        # header=30, label=20, content=50, label_content_gap=8; content starts at 30+20+8=58
        rects = _resolve(
            _docs.header_labeled_sections(
                header_height=30.0,
                section_label_height=20.0,
                col_specs=1,
                n_sections=1,
                section_content_height=50.0,
                label_content_gap=8.0,
            )
        )
        assert rects["col_0_section_0_label"].y == pytest.approx(30.0)
        assert rects["col_0_section_0_content"].y == pytest.approx(58.0)

    def test_label_content_gap_list_per_section(self) -> None:
        # 2 sections: label=20, content=50, lc_gaps=[3, 7]
        # section_0 flex_basis=73 at y=30; section_1 flex_basis=77 at y=103
        rects = _resolve(
            _docs.header_labeled_sections(
                header_height=30.0,
                section_label_height=20.0,
                col_specs=1,
                n_sections=2,
                section_content_height=50.0,
                label_content_gap=[3.0, 7.0],
            )
        )
        assert rects["col_0_section_0_content"].y == pytest.approx(53.0)
        assert rects["col_0_section_1_label"].y == pytest.approx(103.0)
        assert rects["col_0_section_1_content"].y == pytest.approx(130.0)

    def test_label_content_gap_list_length_mismatch_raises(self) -> None:
        with pytest.raises(ValueError, match="label_content_gap"):
            _docs.header_labeled_sections(
                header_height=30.0,
                section_label_height=20.0,
                col_specs=1,
                n_sections=2,
                label_content_gap=[5.0, 6.0, 7.0],
            )

    def test_label_content_gap_and_section_gap(self) -> None:
        # header=30, label=20, content=50, lc_gap=5, section_gap=10
        # section_0 flex_basis=75 at y=30; section_1 at y=30+75+10=115
        rects = _resolve(
            _docs.header_labeled_sections(
                header_height=30.0,
                section_label_height=20.0,
                col_specs=1,
                n_sections=2,
                section_content_height=50.0,
                label_content_gap=5.0,
                section_gap=10.0,
            )
        )
        assert rects["col_0_section_0_content"].y == pytest.approx(55.0)
        assert rects["col_0_section_1_label"].y == pytest.approx(115.0)
        assert rects["col_0_section_1_content"].y == pytest.approx(140.0)

    def test_section_gap_list(self) -> None:
        # 3 sections: label=10, content=20 (fixed); section_gap=[5, 10] (non-uniform)
        # section_0 at y=10, h=30; section_1 at y=45 (10+30+5); section_2 at y=85 (45+30+10)
        rects = _resolve(
            _docs.header_labeled_sections(
                header_height=10.0,
                section_label_height=10.0,
                col_specs=1,
                n_sections=3,
                section_content_height=20.0,
                section_gap=[5.0, 10.0],
            )
        )
        assert rects["col_0_section_1_label"].y == pytest.approx(45.0)
        assert rects["col_0_section_2_label"].y == pytest.approx(85.0)

    def test_section_gap_list_length_mismatch_raises(self) -> None:
        with pytest.raises(ValueError, match="section_gap"):
            _docs.header_labeled_sections(
                header_height=30.0,
                section_label_height=20.0,
                col_specs=1,
                n_sections=3,
                section_gap=[5.0, 10.0, 15.0],
            )

    def test_header_none_with_header_gap(self) -> None:
        # header(stretch) + body(stretch) with gap=10 → available=190, each=95px
        rects = _resolve(
            _docs.header_labeled_sections(
                header_height=None,
                section_label_height=20.0,
                col_specs=1,
                n_sections=1,
                header_gap=10.0,
            )
        )
        assert rects["header"].height == pytest.approx(95.0)
        assert rects["col_0_section_0_label"].y == pytest.approx(105.0)


class TestHeaderSections:
    # Container: 400w x 300h
    def test_header_fixed_height(self) -> None:
        rects = _resolve(_docs.header_sections(header_height=30.0, col_specs=1, n_sections=2), _C400x300)
        assert rects["header"].height == pytest.approx(30.0)
        assert rects["header"].y == pytest.approx(0.0)
        assert rects["header"].width == pytest.approx(400.0)

    def test_content_strips_stretch_equally(self) -> None:
        # header=30 → body=270; 2 stretch sections → each 135
        rects = _resolve(_docs.header_sections(header_height=30.0, col_specs=1, n_sections=2), _C400x300)
        assert rects["col_0_section_0"].height == pytest.approx(135.0)
        assert rects["col_0_section_1"].height == pytest.approx(135.0)

    def test_content_fixed_height(self) -> None:
        rects = _resolve(
            _docs.header_sections(header_height=30.0, col_specs=1, n_sections=2, section_content_height=50.0),
            _C400x300,
        )
        assert rects["col_0_section_0"].height == pytest.approx(50.0)
        assert rects["col_0_section_1"].height == pytest.approx(50.0)

    def test_content_fixed_position(self) -> None:
        # header=30, content_0 at y=30, content_1 at y=80
        rects = _resolve(
            _docs.header_sections(header_height=30.0, col_specs=1, n_sections=2, section_content_height=50.0),
            _C400x300,
        )
        assert rects["col_0_section_0"].y == pytest.approx(30.0)
        assert rects["col_0_section_1"].y == pytest.approx(80.0)

    def test_header_gap(self) -> None:
        rects = _resolve(
            _docs.header_sections(header_height=30.0, col_specs=1, n_sections=1, header_gap=8.0), _C400x300
        )
        assert rects["col_0_section_0"].y == pytest.approx(38.0)

    def test_section_gap(self) -> None:
        # content_0 at y=30 h=50; gap=5; content_1 at y=85
        rects = _resolve(
            _docs.header_sections(
                header_height=30.0, col_specs=1, n_sections=2, section_content_height=50.0, section_gap=5.0
            ),
            _C400x300,
        )
        assert rects["col_0_section_0"].y == pytest.approx(30.0)
        assert rects["col_0_section_1"].y == pytest.approx(85.0)

    def test_col_gap(self) -> None:
        # 2 cols, gap=10 → each (400-10)/2=195
        rects = _resolve(_docs.header_sections(header_height=30.0, col_specs=2, n_sections=1, col_gap=10.0), _C400x300)
        assert rects["col_0_section_0"].width == pytest.approx(195.0)
        assert rects["col_1_section_0"].x == pytest.approx(205.0)

    def test_header_none_stretches_with_body(self) -> None:
        # header(stretch) + body(stretch) → each 150; 2 content strips → each 75
        rects = _resolve(_docs.header_sections(header_height=None, col_specs=1, n_sections=2), _C400x300)
        assert rects["header"].height == pytest.approx(150.0)
        assert rects["col_0_section_0"].height == pytest.approx(75.0)
        assert rects["col_0_section_1"].height == pytest.approx(75.0)

    def test_header_none_with_header_gap(self) -> None:
        # header(stretch) + body(stretch) with gap=10 → available=290, each=145
        rects = _resolve(
            _docs.header_sections(header_height=None, col_specs=1, n_sections=1, header_gap=10.0), _C400x300
        )
        assert rects["header"].height == pytest.approx(145.0)
        assert rects["col_0_section_0"].y == pytest.approx(155.0)

    def test_content_height_list_per_section(self) -> None:
        rects = _resolve(
            _docs.header_sections(header_height=30.0, col_specs=1, n_sections=2, section_content_height=[40.0, 80.0]),
            _C400x300,
        )
        assert rects["col_0_section_0"].height == pytest.approx(40.0)
        assert rects["col_0_section_1"].height == pytest.approx(80.0)
        assert rects["col_0_section_0"].y == pytest.approx(30.0)
        assert rects["col_0_section_1"].y == pytest.approx(70.0)

    def test_content_height_list_mismatch_raises(self) -> None:
        with pytest.raises(ValueError, match="section_content_height"):
            _docs.header_sections(
                header_height=30.0, col_specs=1, n_sections=2, section_content_height=[40.0, 80.0, 100.0]
            )

    def test_section_gap_list(self) -> None:
        # header=10, content=20, gaps=[5,10] → section_0 at y=10, section_1 at y=35, section_2 at y=65
        rects = _resolve(
            _docs.header_sections(
                header_height=10.0, col_specs=1, n_sections=3, section_content_height=20.0, section_gap=[5.0, 10.0]
            ),
            _C400x300,
        )
        assert rects["col_0_section_0"].y == pytest.approx(10.0)
        assert rects["col_0_section_1"].y == pytest.approx(35.0)
        assert rects["col_0_section_2"].y == pytest.approx(65.0)

    def test_section_gap_list_mismatch_raises(self) -> None:
        with pytest.raises(ValueError, match="section_gap"):
            _docs.header_sections(header_height=30.0, col_specs=1, n_sections=3, section_gap=[5.0, 10.0, 15.0])

    def test_fixed_col_specs(self) -> None:
        # col_0=80 fixed, col_1 stretch → 400-80=320
        rects = _resolve(_docs.header_sections(header_height=30.0, col_specs=[80.0, None], n_sections=1), _C400x300)
        assert rects["col_0_section_0"].width == pytest.approx(80.0)
        assert rects["col_1_section_0"].width == pytest.approx(320.0)

    def test_node_count(self) -> None:
        rects = _resolve(_docs.header_sections(header_height=30.0, col_specs=2, n_sections=3), _C400x300)
        assert len(rects) == 1 + 2 * 3  # header + 2 cols * 3 sections

    def test_name_index_formula(self) -> None:
        # names[0]=header; names[1 + c*n_sections + s]=content
        names = ["hdr", "c00", "c01", "c10", "c11"]
        rects = _resolve(_docs.header_sections(header_height=30.0, col_specs=2, n_sections=2, names=names), _C400x300)
        assert "hdr" in rects
        assert "c00" in rects  # c=0, s=0: index 1+0*2+0=1
        assert "c01" in rects  # c=0, s=1: index 1+0*2+1=2
        assert "c10" in rects  # c=1, s=0: index 1+1*2+0=3
        assert "c11" in rects  # c=1, s=1: index 1+1*2+1=4


class TestLabeledSections:
    # Container: 360w x 240h
    def test_label_fixed_height(self) -> None:
        rects = _resolve(_docs.labeled_sections(section_label_height=20.0, col_specs=2, n_sections=2), _C360x240)
        for c in range(2):
            for s in range(2):
                assert rects[f"col_{c}_section_{s}_label"].height == pytest.approx(20.0)

    def test_content_stretches(self) -> None:
        # 2 stretch sections → each 120; label=20 fixed → content fills 100 each
        rects = _resolve(_docs.labeled_sections(section_label_height=20.0, col_specs=1, n_sections=2), _C360x240)
        assert rects["col_0_section_0_label"].height == pytest.approx(20.0)
        assert rects["col_0_section_0_content"].height == pytest.approx(100.0)
        assert rects["col_0_section_1_label"].height == pytest.approx(20.0)
        assert rects["col_0_section_1_content"].height == pytest.approx(100.0)

    def test_content_fixed_height(self) -> None:
        rects = _resolve(
            _docs.labeled_sections(section_label_height=20.0, col_specs=1, n_sections=1, section_content_height=50.0),
            _C360x240,
        )
        assert rects["col_0_section_0_content"].height == pytest.approx(50.0)

    def test_no_header(self) -> None:
        rects = _resolve(_docs.labeled_sections(section_label_height=20.0, col_specs=1, n_sections=1), _C360x240)
        assert "header" not in rects

    def test_section_gap(self) -> None:
        # label=20, content=50 → section flex_basis=70; gap=5 → section_1 at y=75
        rects = _resolve(
            _docs.labeled_sections(
                section_label_height=20.0, col_specs=1, n_sections=2, section_content_height=50.0, section_gap=5.0
            ),
            _C360x240,
        )
        assert rects["col_0_section_0_label"].y == pytest.approx(0.0)
        assert rects["col_0_section_1_label"].y == pytest.approx(75.0)
        assert rects["col_0_section_1_content"].y == pytest.approx(95.0)

    def test_label_content_gap(self) -> None:
        # label=20, gap=8, content=50 → content.y = 28
        rects = _resolve(
            _docs.labeled_sections(
                section_label_height=20.0,
                col_specs=1,
                n_sections=1,
                section_content_height=50.0,
                label_content_gap=8.0,
            ),
            _C360x240,
        )
        assert rects["col_0_section_0_label"].y == pytest.approx(0.0)
        assert rects["col_0_section_0_content"].y == pytest.approx(28.0)

    def test_col_gap(self) -> None:
        # 2 cols, gap=10 → each (360-10)/2=175
        rects = _resolve(
            _docs.labeled_sections(section_label_height=20.0, col_specs=2, n_sections=1, col_gap=10.0), _C360x240
        )
        assert rects["col_0_section_0_label"].width == pytest.approx(175.0)
        assert rects["col_1_section_0_label"].x == pytest.approx(185.0)

    def test_label_none_stretches(self) -> None:
        # 2 stretch sections → each 120; label+content both stretch → each 60
        rects = _resolve(_docs.labeled_sections(section_label_height=None, col_specs=1, n_sections=2), _C360x240)
        assert rects["col_0_section_0_label"].height == pytest.approx(60.0)
        assert rects["col_0_section_0_content"].height == pytest.approx(60.0)
        assert rects["col_0_section_1_label"].height == pytest.approx(60.0)

    def test_label_height_list_per_section(self) -> None:
        rects = _resolve(
            _docs.labeled_sections(section_label_height=[15.0, 25.0], col_specs=1, n_sections=2), _C360x240
        )
        assert rects["col_0_section_0_label"].height == pytest.approx(15.0)
        assert rects["col_0_section_1_label"].height == pytest.approx(25.0)

    def test_label_height_list_mismatch_raises(self) -> None:
        with pytest.raises(ValueError, match="section_label_height"):
            _docs.labeled_sections(section_label_height=[10.0, 20.0, 30.0], col_specs=1, n_sections=2)

    def test_section_gap_list(self) -> None:
        # label=10, content=20, gaps=[5,10] → section_0 at y=0, section_1 at y=35, section_2 at y=75
        rects = _resolve(
            _docs.labeled_sections(
                section_label_height=10.0,
                col_specs=1,
                n_sections=3,
                section_content_height=20.0,
                section_gap=[5.0, 10.0],
            ),
            _C360x240,
        )
        assert rects["col_0_section_0_label"].y == pytest.approx(0.0)
        assert rects["col_0_section_1_label"].y == pytest.approx(35.0)
        assert rects["col_0_section_2_label"].y == pytest.approx(75.0)

    def test_section_gap_list_mismatch_raises(self) -> None:
        with pytest.raises(ValueError, match="section_gap"):
            _docs.labeled_sections(section_label_height=20.0, col_specs=1, n_sections=3, section_gap=[5.0, 10.0, 15.0])

    def test_label_content_gap_list(self) -> None:
        # lc_gaps=[3,7]; section_0 flex_basis=73 at y=0; section_1 flex_basis=77 at y=73
        rects = _resolve(
            _docs.labeled_sections(
                section_label_height=20.0,
                col_specs=1,
                n_sections=2,
                section_content_height=50.0,
                label_content_gap=[3.0, 7.0],
            ),
            _C360x240,
        )
        assert rects["col_0_section_0_content"].y == pytest.approx(23.0)
        assert rects["col_0_section_1_label"].y == pytest.approx(73.0)
        assert rects["col_0_section_1_content"].y == pytest.approx(100.0)

    def test_label_content_gap_list_mismatch_raises(self) -> None:
        with pytest.raises(ValueError, match="label_content_gap"):
            _docs.labeled_sections(
                section_label_height=20.0, col_specs=1, n_sections=2, label_content_gap=[5.0, 6.0, 7.0]
            )

    def test_fixed_col_specs(self) -> None:
        # col_0=80 fixed, col_1 stretch → 360-80=280
        rects = _resolve(
            _docs.labeled_sections(section_label_height=20.0, col_specs=[80.0, None], n_sections=1), _C360x240
        )
        assert rects["col_0_section_0_label"].width == pytest.approx(80.0)
        assert rects["col_1_section_0_label"].width == pytest.approx(280.0)

    def test_node_count(self) -> None:
        rects = _resolve(_docs.labeled_sections(section_label_height=20.0, col_specs=2, n_sections=3), _C360x240)
        assert len(rects) == 2 * 3 * 2  # 2 cols * 3 sections * 2 (label + content)

    def test_name_index_formula(self) -> None:
        # names[c*n_sections*2 + s*2]=label, names[...+1]=content
        names = [f"n_{i}" for i in range(8)]
        rects = _resolve(
            _docs.labeled_sections(section_label_height=20.0, col_specs=2, n_sections=2, names=names), _C360x240
        )
        assert "n_0" in rects  # c=0, s=0, label: 0*4+0*2=0
        assert "n_1" in rects  # c=0, s=0, content: index 1
        assert "n_4" in rects  # c=1, s=0, label: 1*4+0*2=4
        assert "n_7" in rects  # c=1, s=1, content: 1*4+1*2+1=7
