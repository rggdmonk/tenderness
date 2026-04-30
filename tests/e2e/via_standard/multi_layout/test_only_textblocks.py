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

from typing import TYPE_CHECKING

import pytest

from tenderness.core.geometry import Margin
from tenderness.layout_engines.minimal_flexbox.minimal_flexbox_templates import MinimalFlexBoxTemplates
from tenderness.pango_backend.font_description_interface import FontDescriptionInterfaceParameters
from tenderness.pango_backend.layout_interface import LayoutInterfaceParameters
from tenderness.pipelines.standard.render_blocks import (
    BlocksConfig,
    CanvasConfig,
    TextBlock,
    TextStyle,
)
from tests.e2e.e2e_constants import (
    _DEFAULT_PLACEHOLDER_SURFACE_CONFIG,
    HONK_FONT_NAME,
    LONG_CANG_FONT_NAME,
    # MARHEY_FONT_NAME,
    # NOTO_COLOR_EMOJI_FONT_NAME,
    # NOTO_SANS_CUNEIFORM_FONT_NAME,
    NOTO_SANS_FONT_NAME,
    RUBIK_GLITCH_FONT_NAME,
    SOLID_BLACK_COLOR,
    SOLID_LAVENDER_COLOR,
    SOLID_RED_COLOR,
    SOLID_WHITE_COLOR,
)
from tests.e2e.via_standard._standard_render_pipeline import (
    RenderTestCase,
    _standard_render_pipeline_with_bbox_visualization,
)

if TYPE_CHECKING:
    import pathlib

    from tenderness.cairo_backend.surface_configuration import ImageSurfaceConfig, PDFSurfaceConfig, SVGSurfaceConfig


ONLY_TEXTBLOCKS_TEST_CASES: list[RenderTestCase] = [
    RenderTestCase(
        test_name="2_cols_short_text",
        canvas_config=CanvasConfig(
            surface_config=_DEFAULT_PLACEHOLDER_SURFACE_CONFIG,
            global_margin=Margin(top=20, right=20, bottom=20, left=20),
            block_spec=MinimalFlexBoxTemplates.flow_templates.flow_columns(specs=2, gap=50),
            background_spec=SOLID_WHITE_COLOR,
        ),
        blocks_config=BlocksConfig(
            surface_config=_DEFAULT_PLACEHOLDER_SURFACE_CONFIG,
            blocks=[
                TextBlock(
                    text="Column 1: The quick brown fox jumps over the lazy dog.",
                    style=TextStyle(
                        font_description_params=FontDescriptionInterfaceParameters(family=NOTO_SANS_FONT_NAME, size=24),
                        text_color_spec=SOLID_BLACK_COLOR,
                    ),
                ),
                TextBlock(
                    text="Column 2: The quick brown fox jumps over the lazy dog.",
                    style=TextStyle(
                        font_description_params=FontDescriptionInterfaceParameters(family=HONK_FONT_NAME, size=24),
                        text_color_spec=SOLID_BLACK_COLOR,
                    ),
                ),
            ],
        ),
    ),
    RenderTestCase(
        test_name="2_cols_short_text_rotated",
        canvas_config=CanvasConfig(
            surface_config=_DEFAULT_PLACEHOLDER_SURFACE_CONFIG,
            global_margin=Margin(top=20, right=20, bottom=20, left=20),
            block_spec=MinimalFlexBoxTemplates.flow_templates.flow_columns(specs=2, gap=50),
            background_spec=SOLID_WHITE_COLOR,
        ),
        blocks_config=BlocksConfig(
            surface_config=_DEFAULT_PLACEHOLDER_SURFACE_CONFIG,
            blocks=[
                TextBlock(
                    text="Column 1: The quick brown fox jumps over the lazy dog.",
                    style=TextStyle(
                        font_description_params=FontDescriptionInterfaceParameters(family=NOTO_SANS_FONT_NAME, size=16),
                        text_color_spec=SOLID_BLACK_COLOR,
                        context_transform_params=[{"type": "rotate", "angle": 5, "degrees": True}],
                    ),
                ),
                TextBlock(
                    text="Column 2: The quick brown fox jumps over the lazy dog.",
                    style=TextStyle(
                        font_description_params=FontDescriptionInterfaceParameters(family=NOTO_SANS_FONT_NAME, size=18),
                        text_color_spec=SOLID_BLACK_COLOR,
                        context_transform_params=[{"type": "rotate", "angle": 5, "degrees": True}],
                    ),
                ),
            ],
        ),
    ),
    RenderTestCase(
        test_name="3_cols_shared_style",
        canvas_config=CanvasConfig(
            surface_config=_DEFAULT_PLACEHOLDER_SURFACE_CONFIG,
            global_margin=Margin(top=20, right=20, bottom=20, left=20),
            block_spec=MinimalFlexBoxTemplates.flow_templates.flow_columns(specs=3, gap=50),
            background_spec=SOLID_LAVENDER_COLOR,
        ),
        blocks_config=BlocksConfig(
            surface_config=_DEFAULT_PLACEHOLDER_SURFACE_CONFIG,
            blocks=[
                TextBlock(
                    text="Column 1: The quick brown fox jumps over the lazy dog.",
                ),
                TextBlock(
                    text="Column 2: The quick brown fox jumps over the lazy dog.",
                ),
                TextBlock(
                    text="Column 3: The quick brown fox jumps over the lazy dog.",
                ),
            ],
            default_text_style=TextStyle(
                font_description_params=FontDescriptionInterfaceParameters(family=HONK_FONT_NAME, size=20),
                text_color_spec=SOLID_RED_COLOR,
                context_transform_params=[{"type": "rotate", "angle": 5, "degrees": True}],
            ),
        ),
    ),
    RenderTestCase(
        test_name="3_cols_ss_middle",
        canvas_config=CanvasConfig(
            surface_config=_DEFAULT_PLACEHOLDER_SURFACE_CONFIG,
            global_margin=Margin(top=20, right=20, bottom=20, left=20),
            block_spec=MinimalFlexBoxTemplates.flow_templates.flow_columns(specs=3, gap=50),
            background_spec=SOLID_LAVENDER_COLOR,
        ),
        blocks_config=BlocksConfig(
            surface_config=_DEFAULT_PLACEHOLDER_SURFACE_CONFIG,
            blocks=[
                TextBlock(
                    text="Column 1: The quick brown fox jumps over the lazy dog.",
                ),
                TextBlock(
                    text="Column 2: The quick brown fox jumps over the lazy dog.",
                    style=TextStyle(
                        font_description_params=FontDescriptionInterfaceParameters(family=LONG_CANG_FONT_NAME, size=40),
                        context_transform_params=[{"type": "skew_x", "angle": 5, "degrees": True}],
                    ),
                ),
                TextBlock(
                    text="Column 3: The quick brown fox jumps over the lazy dog.",
                ),
            ],
            default_text_style=TextStyle(
                font_description_params=FontDescriptionInterfaceParameters(family=HONK_FONT_NAME, size=20),
                text_color_spec=SOLID_RED_COLOR,
            ),
        ),
    ),
    RenderTestCase(
        test_name="2_cols_overflow",
        canvas_config=CanvasConfig(
            surface_config=_DEFAULT_PLACEHOLDER_SURFACE_CONFIG,
            global_margin=Margin(top=30, right=25, bottom=30, left=25),
            block_spec=MinimalFlexBoxTemplates.flow_templates.flow_columns(specs=2, gap=50),
            background_spec=SOLID_WHITE_COLOR,
        ),
        blocks_config=BlocksConfig(
            surface_config=_DEFAULT_PLACEHOLDER_SURFACE_CONFIG,
            blocks=[
                TextBlock(
                    text=(
                        "If we all reacted the same way, we'd be predictable, and there's always more than "
                        "one way to view a situation. What's true for the group is also true for the "
                        "individual. It's simple: overspecialize, and you breed in weakness. It's slow death."
                    )
                    * 5,
                ),
                TextBlock(
                    text=None,
                    style=TextStyle(layout_interface_params=LayoutInterfaceParameters(justify_last_line=False)),
                ),
            ],
            default_text_style=TextStyle(
                font_description_params=FontDescriptionInterfaceParameters(family=NOTO_SANS_FONT_NAME, size=18),
                text_color_spec=SOLID_BLACK_COLOR,
                layout_interface_params=LayoutInterfaceParameters(justify=True, wrap="word-char"),
            ),
        ),
    ),
    RenderTestCase(
        test_name="3_cols_overflow_wo_middle",
        canvas_config=CanvasConfig(
            surface_config=_DEFAULT_PLACEHOLDER_SURFACE_CONFIG,
            global_margin=Margin(top=20, right=20, bottom=20, left=20),
            block_spec=MinimalFlexBoxTemplates.flow_templates.flow_columns(specs=3, gap=50),
            background_spec=SOLID_LAVENDER_COLOR,
        ),
        blocks_config=BlocksConfig(
            surface_config=_DEFAULT_PLACEHOLDER_SURFACE_CONFIG,
            blocks=[
                TextBlock(
                    text=(
                        "If we all reacted the same way, we'd be predictable, and there's always more than "
                        "one way to view a situation. What's true for the group is also true for the "
                        "individual. It's simple: overspecialize, and you breed in weakness. It's slow death."
                    )
                    * 3,
                ),
                TextBlock(
                    text="Middle column: The quick brown fox jumps over the lazy dog. -> <b>This is bold.</b>",
                    text_strategy="markup",
                    style=TextStyle(
                        font_description_params=FontDescriptionInterfaceParameters(family=NOTO_SANS_FONT_NAME, size=20),
                    ),
                ),
                TextBlock(
                    text=None,
                ),
            ],
            default_text_style=TextStyle(
                font_description_params=FontDescriptionInterfaceParameters(family=RUBIK_GLITCH_FONT_NAME, size=20),
                text_color_spec=SOLID_RED_COLOR,
            ),
        ),
    ),
]


@pytest.mark.e2e
@pytest.mark.parametrize("test_case", ONLY_TEXTBLOCKS_TEST_CASES, ids=lambda tc: tc.test_name)
def test_only_textblocks(
    test_case: RenderTestCase,
    surface_config: ImageSurfaceConfig | PDFSurfaceConfig | SVGSurfaceConfig,
    e2e_output_dir: pathlib.Path,
) -> None:

    _standard_render_pipeline_with_bbox_visualization(
        test_case=test_case,
        surface_config=surface_config,
        e2e_output_dir=e2e_output_dir,
    )
