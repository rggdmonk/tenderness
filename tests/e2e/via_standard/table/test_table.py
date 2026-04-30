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
from tenderness.pipelines.standard.render_blocks import (
    BlocksConfig,
    CanvasConfig,
    TableBlock,
    TableCell,
    TextStyle,
)
from tests.e2e.e2e_constants import (
    _DEFAULT_PLACEHOLDER_SURFACE_CONFIG,
    HONK_FONT_NAME,
    SOLID_LAVENDER_COLOR,
)
from tests.e2e.via_standard._standard_render_pipeline import (
    RenderTestCase,
    _standard_render_pipeline_with_bbox_visualization,
)

if TYPE_CHECKING:
    import pathlib

    from tenderness.cairo_backend.surface_configuration import ImageSurfaceConfig, PDFSurfaceConfig, SVGSurfaceConfig


TABLE_TEST_CASES: list[RenderTestCase] = [
    RenderTestCase(
        test_name="simple_table",
        canvas_config=CanvasConfig(
            surface_config=_DEFAULT_PLACEHOLDER_SURFACE_CONFIG,
            global_margin=Margin(top=20, right=20, bottom=20, left=20),
            background_spec=SOLID_LAVENDER_COLOR,
        ),
        blocks_config=BlocksConfig(
            surface_config=_DEFAULT_PLACEHOLDER_SURFACE_CONFIG,
            blocks=[
                TableBlock(
                    cells=[
                        TableCell(content="1st cell"),
                        TableCell(content="2nd cell"),
                        TableCell(content="3rd cell"),
                        TableCell(content="4th cell"),
                    ],
                    table_cell_pos=MinimalFlexBoxTemplates.table_templates.table_custom(row_specs=2, col_specs=2),
                    default_style=TextStyle(
                        font_description_params=FontDescriptionInterfaceParameters(family=HONK_FONT_NAME, size=28),
                    ),
                )
            ],
        ),
    )
]


@pytest.mark.e2e
@pytest.mark.parametrize("test_case", TABLE_TEST_CASES, ids=lambda tc: tc.test_name)
def test_tables(
    test_case: RenderTestCase,
    surface_config: ImageSurfaceConfig | PDFSurfaceConfig | SVGSurfaceConfig,
    e2e_output_dir: pathlib.Path,
) -> None:

    _standard_render_pipeline_with_bbox_visualization(
        test_case=test_case,
        surface_config=surface_config,
        e2e_output_dir=e2e_output_dir,
    )
