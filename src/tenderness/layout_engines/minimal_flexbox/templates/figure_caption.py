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

"""MinimalFlexBox templates for figure-caption layouts."""

from __future__ import annotations

from tenderness.layout_engines.minimal_flexbox.minimal_flexbox import MinimalFlexNode
from tenderness.layout_engines.minimal_flexbox.templates.base import (
    CaptionSpec,
    MinimalFlexBoxTemplateBase,
)


class MinimalFlexBoxTemplateFigureCaption(MinimalFlexBoxTemplateBase):
    """Layout templates for figure-with-caption arrangements."""

    def stack_figure_caption(
        self,
        caption_height: float | None,
        *,
        gap: float = 0.0,
        caption_on_top: bool = False,
        names: list[str] | None = None,
    ) -> MinimalFlexNode:
        """Stack a stretching figure and a caption strip in a COLUMN container.

        The figure always stretches; the caption is fixed-height when ``caption_height``
        is given, or stretches when ``None``.

        ::

            caption_on_top=False            caption_on_top=True
            ┌───────────┐                   ┌───────────┐
            │  figure   │ ← stretch         │  caption  │ ← caption_height
            ├───────────┤                   ├───────────┤
            │  caption  │ ← caption_height  │  figure   │ ← stretch
            └───────────┘                   └───────────┘

        Parameters
        ----------
        caption_height
            Fixed height of the caption strip; ``None`` lets it stretch.
        gap
            Gap between figure and caption.
        caption_on_top
            ``True`` places the caption above the figure; ``False`` places it below.
        names
            Two-element name list: ``names[0]`` → figure, ``names[1]`` → caption.
            ``None`` uses generated defaults.

        Returns
        -------
        MinimalFlexNode
            Root COLUMN container with figure and caption as children.
        """
        figure_node = MinimalFlexNode(name=self._add_name(names, 0, "figure"))
        return self._wrap_with_caption(
            figure_node,
            CaptionSpec(
                height=caption_height,
                gap=gap,
                on_top=caption_on_top,
                name=self._add_name(names, 1, "caption"),
            ),
        )
