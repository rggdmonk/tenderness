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
from tenderness.layout_engines.minimal_flexbox.templates.figure_caption import MinimalFlexBoxTemplateFigureCaption

_ENGINE = MinimalFlexBox()
_C300x200 = Rectangle(x=0, y=0, width=300, height=200)
_fc = MinimalFlexBoxTemplateFigureCaption()


def _resolve(node: MinimalFlexNode, container: Rectangle = _C300x200) -> dict[str, Rectangle]:
    return {n.name: r for n, r in _ENGINE.resolve_tree(container, node) if n.name is not None}


class TestStackFigureCaption:
    def test_caption_below_by_default(self) -> None:
        rects = _resolve(_fc.stack_figure_caption(caption_height=30.0))
        assert rects["figure"].y == pytest.approx(0.0)
        assert rects["caption"].y == pytest.approx(170.0)
        assert rects["caption"].height == pytest.approx(30.0)

    def test_figure_stretches_to_fill(self) -> None:
        rects = _resolve(_fc.stack_figure_caption(caption_height=30.0))
        assert rects["figure"].height == pytest.approx(170.0)

    def test_caption_on_top(self) -> None:
        rects = _resolve(_fc.stack_figure_caption(caption_height=30.0, caption_on_top=True))
        assert rects["caption"].y == pytest.approx(0.0)
        assert rects["figure"].y == pytest.approx(30.0)

    def test_gap_between_figure_and_caption(self) -> None:
        rects = _resolve(_fc.stack_figure_caption(caption_height=30.0, gap=10.0))
        assert rects["figure"].height == pytest.approx(160.0)
        assert rects["caption"].y == pytest.approx(170.0)

    def test_gap_caption_on_top(self) -> None:
        rects = _resolve(_fc.stack_figure_caption(caption_height=30.0, gap=10.0, caption_on_top=True))
        assert rects["figure"].y == pytest.approx(40.0)
        assert rects["figure"].height == pytest.approx(160.0)

    def test_full_width(self) -> None:
        rects = _resolve(_fc.stack_figure_caption(caption_height=30.0))
        assert rects["figure"].width == pytest.approx(300.0)
        assert rects["caption"].width == pytest.approx(300.0)

    def test_custom_names(self) -> None:
        rects = _resolve(_fc.stack_figure_caption(caption_height=30.0, names=["img", "label"]))
        assert "img" in rects
        assert "label" in rects

    def test_caption_none_both_stretch_equally(self) -> None:
        rects = _resolve(_fc.stack_figure_caption(caption_height=None))
        assert rects["figure"].height == pytest.approx(100.0)
        assert rects["caption"].height == pytest.approx(100.0)

    def test_caption_none_on_top(self) -> None:
        rects = _resolve(_fc.stack_figure_caption(caption_height=None, caption_on_top=True))
        assert rects["caption"].y == pytest.approx(0.0)
        assert rects["caption"].height == pytest.approx(100.0)
        assert rects["figure"].y == pytest.approx(100.0)

    def test_caption_none_with_gap(self) -> None:
        rects = _resolve(_fc.stack_figure_caption(caption_height=None, gap=10.0))
        assert rects["figure"].height == pytest.approx(95.0)
        assert rects["caption"].height == pytest.approx(95.0)
        assert rects["caption"].y == pytest.approx(105.0)

    def test_caption_none_on_top_with_gap(self) -> None:
        # caption(stretch) then figure(stretch) with gap=10 → each (200-10)/2 = 95px
        rects = _resolve(_fc.stack_figure_caption(caption_height=None, gap=10.0, caption_on_top=True))
        assert rects["caption"].y == pytest.approx(0.0)
        assert rects["caption"].height == pytest.approx(95.0)
        assert rects["figure"].y == pytest.approx(105.0)
        assert rects["figure"].height == pytest.approx(95.0)
