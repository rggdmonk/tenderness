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
from tenderness.pipelines.document.pipeline_schema import DocumentBlocksConfig, DocumentConfig
from tenderness.pipelines.document.table_block_helpers import TableBlock, TextCell
from tenderness.pipelines.document.text_block_helpers import TextStyle
from tests.e2e._constants import (
    _DEFAULT_PLACEHOLDER_SURFACE_CONFIG,
    HONK_FONT_NAME,
    SOLID_LAVENDER_COLOR,
)
from tests.e2e.pipelines.document._document_render_pipeline import (
    DocumentRenderPipelineTestCase,
    run_document_render_pipeline_with_bbox_visualization,
)

if TYPE_CHECKING:
    import pathlib

    from tenderness.cairo_backend.surface_configuration import ImageSurfaceConfig, PDFSurfaceConfig, SVGSurfaceConfig


TABLE_TEST_CASES: list[DocumentRenderPipelineTestCase] = [
    DocumentRenderPipelineTestCase(
        test_name="simple_table",
        config=DocumentConfig(
            surface_config=_DEFAULT_PLACEHOLDER_SURFACE_CONFIG,
            global_margin=Margin(top=20, right=20, bottom=20, left=20),
            background_spec=SOLID_LAVENDER_COLOR,
        ),
        blocks_config=DocumentBlocksConfig(
            surface_config=_DEFAULT_PLACEHOLDER_SURFACE_CONFIG,
            blocks=[
                TableBlock(
                    cells=[
                        TextCell(text="1st cell"),
                        TextCell(text="2nd cell"),
                        TextCell(text="3rd cell"),
                        TextCell(text="4th cell"),
                    ],
                    table_cell_pos=MinimalFlexBoxTemplates.table_templates.table_basic(row_specs=2, col_specs=2),
                    base_text_style=TextStyle(
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
    test_case: DocumentRenderPipelineTestCase,
    surface_config: ImageSurfaceConfig | PDFSurfaceConfig | SVGSurfaceConfig,
    e2e_output_dir: pathlib.Path,
) -> None:

    run_document_render_pipeline_with_bbox_visualization(
        test_case=test_case,
        surface_config=surface_config,
        e2e_output_dir=e2e_output_dir,
    )
