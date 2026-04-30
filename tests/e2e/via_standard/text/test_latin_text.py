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

import pathlib  # noqa: TC003
from typing import TYPE_CHECKING

import pytest

from tenderness.cairo_backend.color_patterns import ImagePatternSpec  # noqa: F401
from tenderness.cairo_backend.font_options_interface import FontOptionsInterfaceParameters
from tenderness.core.geometry import Margin
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
    LINEAR_GRADIENT_BLACK_TO_WHITE_COLOR,
    MARHEY_FONT_NAME,
    NOTO_SANS_FONT_NAME,
    SOLID_BLACK_COLOR,
    SOLID_DARKMAGNETA_COLOR,
    SOLID_LAVENDER_COLOR,
    SOLID_LIGHTCYAN_COLOR,
    SOLID_RED_COLOR,
    SOLID_WHITE_COLOR,
)
from tests.e2e.via_standard._standard_render_pipeline import (
    RenderTestCase,
    _standard_render_pipeline_with_bbox_visualization,
)

if TYPE_CHECKING:
    from tenderness.cairo_backend.surface_configuration import ImageSurfaceConfig, PDFSurfaceConfig, SVGSurfaceConfig


TEXT_LATIN_TEST_CASES: list[RenderTestCase] = [
    RenderTestCase(
        test_name="single_line",
        canvas_config=CanvasConfig(
            surface_config=_DEFAULT_PLACEHOLDER_SURFACE_CONFIG,
            background_spec=SOLID_LIGHTCYAN_COLOR,
        ),
        blocks_config=BlocksConfig(
            surface_config=_DEFAULT_PLACEHOLDER_SURFACE_CONFIG,
            blocks=[
                TextBlock(
                    text="The quick brown fox jumps over the lazy dog.",
                    style=TextStyle(
                        font_description_params=FontDescriptionInterfaceParameters(
                            family=NOTO_SANS_FONT_NAME, size_device_units=32
                        ),
                        text_color_spec=SOLID_BLACK_COLOR,
                    ),
                )
            ],
        ),
    ),
    RenderTestCase(
        test_name="single_line_honk_font",
        canvas_config=CanvasConfig(
            surface_config=_DEFAULT_PLACEHOLDER_SURFACE_CONFIG,
            background_spec=SOLID_WHITE_COLOR,
        ),
        blocks_config=BlocksConfig(
            surface_config=_DEFAULT_PLACEHOLDER_SURFACE_CONFIG,
            blocks=[
                TextBlock(
                    text="Honk! The quick brown fox jumps over the lazy dog.",
                    style=TextStyle(
                        font_description_params=FontDescriptionInterfaceParameters(
                            family=HONK_FONT_NAME, size_device_units=32
                        )
                    ),
                )
            ],
        ),
    ),
    RenderTestCase(
        test_name="single_long_line",
        canvas_config=CanvasConfig(
            surface_config=_DEFAULT_PLACEHOLDER_SURFACE_CONFIG,
            background_spec=LINEAR_GRADIENT_BLACK_TO_WHITE_COLOR,
        ),
        blocks_config=BlocksConfig(
            surface_config=_DEFAULT_PLACEHOLDER_SURFACE_CONFIG,
            blocks=[
                TextBlock(
                    text=(
                        "If we all reacted the same way, we'd be predictable, and there's always more than "
                        "one way to view a situation. What's true for the group is also true for the "
                        "individual. It's simple: overspecialize, and you breed in weakness. It's slow death."
                    ),
                    style=TextStyle(
                        font_description_params=FontDescriptionInterfaceParameters(family=MARHEY_FONT_NAME, size=24),
                        text_color_spec=SOLID_DARKMAGNETA_COLOR,
                    ),
                )
            ],
        ),
    ),
    RenderTestCase(
        test_name="center_aligned_text",
        canvas_config=CanvasConfig(
            surface_config=_DEFAULT_PLACEHOLDER_SURFACE_CONFIG,
            global_margin=Margin(top=40, right=40, bottom=40, left=40),
            background_spec=SOLID_WHITE_COLOR,
        ),
        blocks_config=BlocksConfig(
            surface_config=_DEFAULT_PLACEHOLDER_SURFACE_CONFIG,
            blocks=[
                TextBlock(
                    text="11111\n2222\n333\n44\n5",
                    style=TextStyle(
                        font_options_params=FontOptionsInterfaceParameters(color_palette=6),
                        font_description_params=FontDescriptionInterfaceParameters(family=HONK_FONT_NAME, size=24),
                        layout_interface_params=LayoutInterfaceParameters(alignment="center"),
                    ),
                )
            ],
        ),
    ),
    # RenderTestCase(
    #     test_name="center_aligned_text_with_background_image",
    #     canvas_config=CanvasConfig(
    #         surface_config=_DEFAULT_PLACEHOLDER_SURFACE_CONFIG,
    #         global_margin=Margin(top=40, right=40, bottom=40, left=40),
    #         background_spec=ImagePatternSpec(path=pathlib.Path("_development/coffee_1280_853.png")),
    #     ),
    #     blocks_config=BlocksConfig(
    #         surface_config=_DEFAULT_PLACEHOLDER_SURFACE_CONFIG,
    #         blocks=[
    #             TextBlock(
    #                 text="1st line\n2nd line\n3rd line\n4th line\n5th line",
    #                 style=TextStyle(
    #                     font_options_params=FontOptionsInterfaceParameters(color_palette=4),
    #                     font_description_params=FontDescriptionInterfaceParameters(family=HONK_FONT_NAME, size=32),
    #                     layout_interface_params=LayoutInterfaceParameters(alignment="center"),
    #                 ),
    #             )
    #         ],
    #     ),
    # ),
    RenderTestCase(
        test_name="limited_background_image_not_working",
        canvas_config=CanvasConfig(
            surface_config=_DEFAULT_PLACEHOLDER_SURFACE_CONFIG,
            global_margin=Margin(top=30, right=30, bottom=30, left=30),
            background_spec=SOLID_LAVENDER_COLOR,
            # background_image_parameters=BackgroundImageParameters(
            #     path_to_image=pathlib.Path("_development/coffee_1280_853.png"),
            #     dest_rect=Rectangle(
            #         x=0, y=0, width=640, height=426
            #     ),  # only use the left half of the image as background
            # ),
        ),
        blocks_config=BlocksConfig(
            surface_config=_DEFAULT_PLACEHOLDER_SURFACE_CONFIG,
            blocks=[
                TextBlock(
                    text="The quick brown fox jumps over the lazy dog.",
                    style=TextStyle(
                        font_description_params=FontDescriptionInterfaceParameters(family=NOTO_SANS_FONT_NAME, size=32),
                        text_color_spec=SOLID_RED_COLOR,
                    ),
                )
            ],
        ),
    ),
]


@pytest.mark.e2e
@pytest.mark.parametrize("test_case", TEXT_LATIN_TEST_CASES, ids=lambda tc: tc.test_name)
def test_latin_text(
    test_case: RenderTestCase,
    surface_config: ImageSurfaceConfig | PDFSurfaceConfig | SVGSurfaceConfig,
    e2e_output_dir: pathlib.Path,
) -> None:

    _standard_render_pipeline_with_bbox_visualization(
        test_case=test_case,
        surface_config=surface_config,
        e2e_output_dir=e2e_output_dir,
    )
