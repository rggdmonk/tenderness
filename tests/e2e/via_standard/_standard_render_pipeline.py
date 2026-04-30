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

from tenderness.bounding_boxes.bounding_boxes_schema import LayoutBBoxCollection
from tenderness.bounding_boxes.draw_bounding_boxes import DrawConfig, ImageBoundingBoxDrawer, SVGBoundingBoxDrawer
from tenderness.font_setup.font_setup import FontSetup
from tenderness.font_setup.fontconfig_managers import FontconfigMode
from tenderness.image_backend.surface_writer import SurfaceWriterParameters
from tenderness.pipelines.standard.render_pipeline import RenderPipeline
from tenderness.pipelines.standard.render_pipeline_models import TableBlockResult, TextBlockResult
from tests._test_utils.paths_test import TEST_FONTS_DIR

if TYPE_CHECKING:
    import io
    import pathlib

    from tenderness.cairo_backend.surface_configuration import ImageSurfaceConfig, PDFSurfaceConfig, SVGSurfaceConfig
    from tenderness.pipelines.standard.render_blocks import BlocksConfig, CanvasConfig
    from tenderness.pipelines.standard.render_pipeline_models import RenderTextResult, SetupRenderResult

logger = logging.getLogger(__name__)


type RenderPipelineOutput = tuple[
    cairo.Surface,
    io.BytesIO | None,
    cairo.Context[cairo.Surface],
    pathlib.Path,
    list[LayoutBBoxCollection | list[LayoutBBoxCollection] | None],
]


@dataclass(frozen=True)
class RenderTestCase:
    test_name: str
    canvas_config: CanvasConfig
    blocks_config: BlocksConfig


@dataclass(frozen=True)
class _PipelineRun:
    setup_render_result: SetupRenderResult
    render_text_result: RenderTextResult
    saved_file_path: pathlib.Path
    bbox_collections: list[LayoutBBoxCollection | list[LayoutBBoxCollection] | None]


def _standard_render_pipeline(
    test_case: RenderTestCase,
    surface_config: ImageSurfaceConfig | PDFSurfaceConfig | SVGSurfaceConfig,
    e2e_output_dir: pathlib.Path,
) -> _PipelineRun:

    if surface_config is not None:
        # Create a copy of the test case with the provided surface_config
        test_case = replace(
            test_case,
            canvas_config=replace(test_case.canvas_config, surface_config=surface_config),
            blocks_config=replace(test_case.blocks_config, surface_config=surface_config),
        )
    else:
        msg = "Surface configuration must be provided for the render pipeline test."
        raise ValueError(msg)

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
    # Render pipeline
    # --------------------------
    render_pipeline = RenderPipeline()

    # --------------------------
    # Setup render
    # --------------------------
    setup_render_result = render_pipeline.setup_render(canvas_config=test_case.canvas_config)

    # --------------------------
    # Render text
    # --------------------------
    render_text_result = render_pipeline.render_text(
        blocks_config=test_case.blocks_config, setup_render=setup_render_result
    )

    # --------------------------
    # Get text bounding boxes
    # --------------------------
    bbox_collections = render_pipeline.get_text_bounding_boxes(
        rendered_blocks=render_text_result.rendered_blocks,
    )

    # --------------------------
    # Save output file
    # --------------------------
    file_name = f"{test_case.test_name}{test_case.canvas_config.surface_config.image_format.extension}"
    saved_file_path = render_pipeline.save_as_file(
        surface=setup_render_result.surface,
        surface_config=test_case.canvas_config.surface_config,
        surface_writer_params=SurfaceWriterParameters(output_file_path=e2e_output_dir / file_name),
        stream=setup_render_result.stream,
    )
    assert saved_file_path.exists(), f"Expected file to be saved at {saved_file_path}, but it does not exist."
    assert saved_file_path.stat().st_size > 0, "Output file is empty"

    return _PipelineRun(
        setup_render_result=setup_render_result,
        render_text_result=render_text_result,
        saved_file_path=saved_file_path,
        bbox_collections=bbox_collections,
    )


def _standard_render_pipeline_with_bbox_visualization(  # noqa: C901, PLR0912, PLR0915
    test_case: RenderTestCase,
    surface_config: ImageSurfaceConfig | PDFSurfaceConfig | SVGSurfaceConfig,
    e2e_output_dir: pathlib.Path,
) -> RenderPipelineOutput:

    run = _standard_render_pipeline(
        test_case=test_case,
        surface_config=surface_config,
        e2e_output_dir=e2e_output_dir,
    )

    setup_render_result = run.setup_render_result
    render_text_result = run.render_text_result
    saved_file_path = run.saved_file_path
    bbox_collections = run.bbox_collections

    # --------------------------
    # DEBUG: serialize layout after rendering
    # --------------------------
    for idx, block in enumerate(render_text_result.rendered_blocks):
        if isinstance(block, TextBlockResult):
            fn_layout_after_render = (
                f"{idx}_{test_case.test_name}_{surface_config.image_format.name}_layout_params_after_render.json"
            )
            block.layout_interface.serialize_layout(
                context=True, output=True, filepath=e2e_output_dir / fn_layout_after_render
            )
        elif isinstance(block, TableBlockResult):
            for sub_idx, cell_layout in enumerate(block.cell_layouts):
                fn_layout_after_render = f"{idx}_{sub_idx}_{test_case.test_name}_{surface_config.image_format.name}_layout_params_after_render.json"
                cell_layout.serialize_layout(
                    context=True, output=True, filepath=e2e_output_dir / fn_layout_after_render
                )
        else:
            logger.debug("Block at index %d is an image block, skipping serialization.", idx)

    # --------------------------
    # DEBUG: fit report after rendering
    # --------------------------
    for idx, block in enumerate(render_text_result.rendered_blocks):
        if isinstance(block, TextBlockResult):
            report = block.layout_interface.get_layout_fit_report()

            logger.info("<start> Layout %d fit report:", idx)

            if report.fits_logical.fit_both:
                logger.info("Logical fits!")
            else:
                logger.info("Logical does not fit:")
                logger.info(report.fits_logical.__repr__())

            if report.fits_ink.fit_both:
                logger.info("Ink fits!")
            else:
                logger.info("Ink does not fit:")
                logger.info(report.fits_ink.__repr__())

            if report.clipped_text.has_clipped:
                logger.info("Text that did not fit in the layout:")
                logger.info(report.clipped_text.__repr__())

            logger.info("<end> Layout %d fit report.", idx)

        elif isinstance(block, TableBlockResult):
            for cell_layout in block.cell_layouts:
                report = cell_layout.get_layout_fit_report()

                if report.fits_logical.fit_both:
                    logger.info("Logical fits!")
                else:
                    logger.info("Logical does not fit!")
                    logger.info(report.fits_logical.__repr__())

                if report.fits_ink.fit_both:
                    logger.info("Ink fits!")
                else:
                    logger.info("Ink does not fit!")
                    logger.info(report.fits_ink.__repr__())

                if report.clipped_text.has_clipped:
                    logger.info("Text that did not fit in the layout:")
                    logger.info(report.clipped_text.__repr__())

        else:
            logger.debug("Block at index %d is an image block, skipping fit report logging.", idx)

    # --------------------------
    # DEBUG: Draw bounding boxes on the rendered image per layout
    # --------------------------

    draw_config = DrawConfig(draw_labels=False)

    if isinstance(setup_render_result.surface, cairo.ImageSurface):
        bbox_drawer = ImageBoundingBoxDrawer()
        for i, bbox_collection in enumerate(bbox_collections):
            if isinstance(bbox_collection, LayoutBBoxCollection):
                source_image = Image.open(saved_file_path)
                for level, annotated_image in bbox_drawer.draw_per_level(
                    image=source_image, collection=bbox_collection, config=draw_config
                ):
                    annotated_file_name = f"{i}_{test_case.test_name}_annotated_{level.name.lower()}{surface_config.image_format.extension}"
                    annotated_image.save(e2e_output_dir.joinpath(annotated_file_name))
            elif isinstance(bbox_collection, list):
                for sub_idx, sub_bbox_collection in enumerate(bbox_collection):
                    if isinstance(sub_bbox_collection, LayoutBBoxCollection):
                        source_image = Image.open(saved_file_path)
                        for level, annotated_image in bbox_drawer.draw_per_level(
                            image=source_image, collection=sub_bbox_collection, config=draw_config
                        ):
                            annotated_file_name = f"{i}_{sub_idx}_{test_case.test_name}_annotated_{level.name.lower()}{surface_config.image_format.extension}"
                            annotated_image.save(e2e_output_dir.joinpath(annotated_file_name))
                    else:
                        logger.debug(
                            "Sub bounding box collection at index %d in bbox_collections is not of type LayoutBBoxCollection, skipping.",
                            sub_idx,
                        )
            else:
                logger.debug(
                    "Bounding box collection at index %d in bbox_collections is not of type LayoutBBoxCollection or list, skipping.",
                    i,
                )
    elif isinstance(setup_render_result.surface, cairo.SVGSurface):
        svg_drawer = SVGBoundingBoxDrawer()
        for i, bbox_collection in enumerate(bbox_collections):
            if isinstance(bbox_collection, LayoutBBoxCollection):
                for level in draw_config.levels:
                    level_config = replace(draw_config, levels={level})
                    annotated = svg_drawer.draw(saved_file_path.read_bytes(), bbox_collection, level_config)
                    annotated_file_name = f"{i}_{test_case.test_name}_annotated_{level.name.lower()}{surface_config.image_format.extension}"
                    (e2e_output_dir / annotated_file_name).write_bytes(annotated)
            elif isinstance(bbox_collection, list):
                for sub_idx, sub_bbox_collection in enumerate(bbox_collection):
                    if isinstance(sub_bbox_collection, LayoutBBoxCollection):
                        for level in draw_config.levels:
                            level_config = replace(draw_config, levels={level})
                            annotated = svg_drawer.draw(saved_file_path.read_bytes(), sub_bbox_collection, level_config)
                            annotated_file_name = f"{i}_{sub_idx}_{test_case.test_name}_annotated_{level.name.lower()}{surface_config.image_format.extension}"
                            (e2e_output_dir / annotated_file_name).write_bytes(annotated)
                    else:
                        logger.debug(
                            "Sub bounding box collection at index %d in bbox_collections is not of type LayoutBBoxCollection, skipping.",
                            sub_idx,
                        )
            else:
                logger.debug(
                    "Bounding box collection at index %d in bbox_collections is not of type LayoutBBoxCollection or list, skipping.",
                    i,
                )
    else:
        logger.debug(
            "Skipping bounding box drawing for non-image surface type: %s", type(setup_render_result.surface).__name__
        )

    return (
        setup_render_result.surface,
        setup_render_result.stream,
        setup_render_result.cairo_context,
        saved_file_path,
        bbox_collections,
    )
