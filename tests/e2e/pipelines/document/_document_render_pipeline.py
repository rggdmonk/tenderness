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

import logging
from dataclasses import dataclass, replace
from typing import TYPE_CHECKING

import cairo
from PIL import Image

from tenderness.bounding_boxes.draw_text_bboxes import (
    ImageTextBoundingBoxDrawer,
    SVGTextBoundingBoxDrawer,
    TextDrawConfig,
)
from tenderness.font_setup.font_setup import FontSetup
from tenderness.font_setup.fontconfig_managers import FontconfigMode
from tenderness.pipelines.document.bbox_helper import BlockBBoxesResult, TableBlockBBoxesResult, TextBlockBBoxesResult
from tenderness.pipelines.document.image_block_helpers import ImageBlockResult
from tenderness.pipelines.document.pipeline import DocumentRenderPipeline
from tenderness.pipelines.document.table_block_helpers import TableBlockResult
from tenderness.pipelines.document.text_block_helpers import TextBlockResult
from tests._test_utils.paths_test import TEST_FONTS_DIR

if TYPE_CHECKING:
    import pathlib

    from tenderness.cairo_backend.surface_configuration import ImageSurfaceConfig, PDFSurfaceConfig, SVGSurfaceConfig
    from tenderness.pipelines.document.pipeline_schema import DocumentBlocksConfig, DocumentConfig, DocumentSetupResult

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class DocumentRenderPipelineTestCase:
    test_name: str
    config: DocumentConfig
    blocks_config: DocumentBlocksConfig


@dataclass(frozen=True)
class _DocumentRenderPipelineRun:
    setup_result: DocumentSetupResult
    saved_file_path: pathlib.Path
    text_bbox_results: list[TextBlockBBoxesResult | TableBlockBBoxesResult | None]
    rendered_blocks: list[TextBlockResult | TableBlockResult | ImageBlockResult]
    block_bbox_results: BlockBBoxesResult


def _document_render_pipeline(
    test_case: DocumentRenderPipelineTestCase,
    surface_config: ImageSurfaceConfig | PDFSurfaceConfig | SVGSurfaceConfig,
    e2e_output_dir: pathlib.Path,
) -> _DocumentRenderPipelineRun:

    test_case = replace(
        test_case,
        config=replace(test_case.config, surface_config=surface_config),
        blocks_config=replace(test_case.blocks_config, surface_config=surface_config),
    )

    # --------------------------
    # Font setup
    # --------------------------
    font_setup = FontSetup()
    fontsconfig_path = font_setup.setup_font(
        mode=FontconfigMode.TEMPLATE_MINIMAL, font_dir=TEST_FONTS_DIR, fontconfig_destination_dir=e2e_output_dir
    )
    assert fontsconfig_path.exists(), f"Expected fonts directory at {fontsconfig_path}, but it does not exist."
    assert fontsconfig_path.is_file(), f"Expected fontsconfig path to be a file, but it is not: {fontsconfig_path}"

    # --------------------------
    # Pipeline
    # --------------------------
    pipeline = DocumentRenderPipeline()
    setup_result = pipeline.setup(config=test_case.config)
    render_result = pipeline.render(blocks_config=test_case.blocks_config, setup_result=setup_result)
    text_bbox_results = pipeline.get_text_bounding_boxes(rendered_blocks=render_result.rendered_blocks)
    block_bbox_results = pipeline.get_block_bounding_boxes(setup_result=setup_result)

    # --------------------------
    # Save output file
    # --------------------------
    file_name = f"{test_case.test_name}{surface_config.image_format.extension}"
    saved_file_path = pipeline.save_as_file(
        surface=setup_result.surface,
        surface_config=surface_config,
        output_file_path=e2e_output_dir / file_name,
        stream=setup_result.stream,
    )
    assert saved_file_path.exists(), f"Expected file to be saved at {saved_file_path}, but it does not exist."
    assert saved_file_path.stat().st_size > 0, "Output file is empty"

    return _DocumentRenderPipelineRun(
        setup_result=setup_result,
        saved_file_path=saved_file_path,
        text_bbox_results=text_bbox_results,
        rendered_blocks=render_result.rendered_blocks,
        block_bbox_results=block_bbox_results,
    )


def run_document_render_pipeline_with_bbox_visualization(  # noqa: C901, PLR0912, PLR0915
    test_case: DocumentRenderPipelineTestCase,
    surface_config: ImageSurfaceConfig | PDFSurfaceConfig | SVGSurfaceConfig,
    e2e_output_dir: pathlib.Path,
) -> None:

    run = _document_render_pipeline(
        test_case=test_case,
        surface_config=surface_config,
        e2e_output_dir=e2e_output_dir,
    )

    setup_result = run.setup_result
    saved_file_path = run.saved_file_path
    text_bbox_results = run.text_bbox_results
    rendered_blocks = run.rendered_blocks

    # --------------------------
    # DEBUG: serialize layout after rendering
    # --------------------------
    for idx, block in enumerate(rendered_blocks):
        if isinstance(block, TextBlockResult):
            fn = f"{idx}_{test_case.test_name}_{surface_config.image_format.name}_layout_params_after_render.json"
            block.layout_interface.serialize_layout(context=True, output=True, filepath=e2e_output_dir / fn)
        elif isinstance(block, TableBlockResult):
            for sub_idx, cell_result in enumerate(block.result_cells):
                fn = f"{idx}_{sub_idx}_{test_case.test_name}_{surface_config.image_format.name}_layout_params_after_render.json"
                cell_result.layout_interface.serialize_layout(context=True, output=True, filepath=e2e_output_dir / fn)
        elif isinstance(block, ImageBlockResult):
            logger.debug("Block at index %d is an image block, skipping serialization.", idx)

        else:
            msg = f"Unexpected block type at index {idx}: {type(block).__name__}"
            raise TypeError(msg)

    # --------------------------
    # DEBUG: fit report after rendering
    # --------------------------
    for idx, block in enumerate(rendered_blocks):
        if isinstance(block, TextBlockResult):
            report = block.layout_interface.get_layout_fit_report()
            logger.info("<start> Layout %d fit report:", idx)
            if report.fits_logical.fit_both:
                logger.info("✅Logical fits!")
            else:
                logger.info("❌Logical does not fit:")
                logger.info(report.fits_logical.__repr__())
            if report.fits_ink.fit_both:
                logger.info("✅Ink fits!")
            else:
                logger.info("❌Ink does not fit:")
                logger.info(report.fits_ink.__repr__())
            if report.clipped_text.has_clipped:
                logger.info("⚠️Text that did not fit in the layout:")
                logger.info(report.clipped_text.__repr__())
            logger.info("<end> Layout %d fit report.", idx)

        elif isinstance(block, TableBlockResult):
            for cell_result in block.result_cells:
                report = cell_result.layout_interface.get_layout_fit_report()
                if report.fits_logical.fit_both:
                    logger.info("✅Logical fits!")
                else:
                    logger.info("❌Logical does not fit!")
                    logger.info(report.fits_logical.__repr__())
                if report.fits_ink.fit_both:
                    logger.info("✅Ink fits!")
                else:
                    logger.info("❌Ink does not fit!")
                    logger.info(report.fits_ink.__repr__())
                if report.clipped_text.has_clipped:
                    logger.info("⚠️Text that did not fit in the layout:")
                    logger.info(report.clipped_text.__repr__())

        elif isinstance(block, ImageBlockResult):
            logger.debug("Block at index %d is an image block, skipping fit report logging.", idx)

        else:
            msg = f"Unexpected block type at index {idx}: {type(block).__name__}"
            raise TypeError(msg)

    # --------------------------
    # DEBUG: Draw text bounding boxes on the rendered image per layout
    # --------------------------
    draw_config = TextDrawConfig(draw_labels=False)

    if isinstance(setup_result.surface, cairo.ImageSurface):
        bbox_drawer = ImageTextBoundingBoxDrawer()

        for i, bbox_result in enumerate(text_bbox_results):
            if isinstance(bbox_result, TextBlockBBoxesResult):
                source_image = Image.open(saved_file_path)
                for level, annotated_image in bbox_drawer.draw_per_level(
                    image=source_image, text_bounding_boxes=bbox_result.bboxes, config=draw_config
                ):
                    annotated_file_name = f"{i}_{test_case.test_name}_annotated_{level.name.lower()}{surface_config.image_format.extension}"
                    annotated_image.save(e2e_output_dir / annotated_file_name)
            elif isinstance(bbox_result, TableBlockBBoxesResult):
                for sub_idx, cell_bbox in enumerate(bbox_result.cell_bboxes):
                    source_image = Image.open(saved_file_path)
                    for level, annotated_image in bbox_drawer.draw_per_level(
                        image=source_image, text_bounding_boxes=cell_bbox.bboxes, config=draw_config
                    ):
                        annotated_file_name = f"{i}_{sub_idx}_{test_case.test_name}_annotated_{level.name.lower()}{surface_config.image_format.extension}"
                        annotated_image.save(e2e_output_dir / annotated_file_name)

            elif bbox_result is None:
                logger.debug("Bounding box result at index %d is None, skipping.", i)
            else:
                msg = f"Unexpected bounding box result type at index {i}: {type(bbox_result).__name__}"
                raise TypeError(msg)

    elif isinstance(setup_result.surface, cairo.SVGSurface):
        svg_drawer = SVGTextBoundingBoxDrawer()
        for i, bbox_result in enumerate(text_bbox_results):
            if isinstance(bbox_result, TextBlockBBoxesResult):
                for level in draw_config.levels:
                    level_config = replace(draw_config, levels={level})
                    annotated = svg_drawer.draw(saved_file_path.read_bytes(), bbox_result.bboxes, level_config)
                    annotated_file_name = f"{i}_{test_case.test_name}_annotated_{level.name.lower()}{surface_config.image_format.extension}"
                    (e2e_output_dir / annotated_file_name).write_bytes(annotated)
            elif isinstance(bbox_result, TableBlockBBoxesResult):
                for sub_idx, cell_bbox in enumerate(bbox_result.cell_bboxes):
                    for level in draw_config.levels:
                        level_config = replace(draw_config, levels={level})
                        annotated = svg_drawer.draw(saved_file_path.read_bytes(), cell_bbox.bboxes, level_config)
                        annotated_file_name = f"{i}_{sub_idx}_{test_case.test_name}_annotated_{level.name.lower()}{surface_config.image_format.extension}"
                        (e2e_output_dir / annotated_file_name).write_bytes(annotated)
            elif bbox_result is None:
                logger.debug("Bounding box result at index %d is None (image block), skipping.", i)
            else:
                msg = f"Unexpected bounding box result type at index {i}: {type(bbox_result).__name__}"
                raise TypeError(msg)
    else:
        logger.debug(
            "Skipping bounding box drawing for non-image surface type: %s", type(setup_result.surface).__name__
        )
