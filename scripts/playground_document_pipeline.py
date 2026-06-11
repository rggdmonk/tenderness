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

import json
import pathlib
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from tenderness.bounding_boxes.bounding_boxes_schema import CharBBox, ClusterBBox, LineBBox, RunBBox
    from tenderness.pipelines.document.bbox_helper import BlockBBoxesResult

from PIL import Image

from tenderness.bounding_boxes.draw_text_bboxes import ImageTextBoundingBoxDrawer
from tenderness.cairo_backend.color_patterns import SolidColorSpec
from tenderness.cairo_backend.surface_config_manager import SurfaceConfigManager
from tenderness.colors.color_selector import ColorSelector
from tenderness.core.geometry import Margin
from tenderness.font_setup.font_setup import FontSetup
from tenderness.font_setup.fontconfig_managers import FontconfigMode
from tenderness.pango_backend.font_description_interface import FontDescriptionInterfaceParameters
from tenderness.pipelines.document import (
    DocumentBlocksConfig,
    DocumentConfig,
    DocumentRenderPipeline,
    TableBlockBBoxesResult,
    TextBlock,
    TextBlockBBoxesResult,
    TextStyle,
)
from tenderness.pipelines.document.draw_block_bboxes import ImageBlockBoundingBoxDrawer

_PROJECT_ROOT = pathlib.Path(__file__).parent.parent
_OUTPUT_BASE = _PROJECT_ROOT / "tenderness_tests_output" / "document_pipeline_example"
OUTPUT_DIR = _OUTPUT_BASE
TEXT_BBOXES_DIR = _OUTPUT_BASE / "text_bboxes"
BLOCK_BBOXES_DIR = _OUTPUT_BASE / "block_bboxes"
FONTS_DIR = _PROJECT_ROOT / ".tenderness_tests_cache" / "fonts_for_tests"


def _print_char_bboxes(char_bboxes: list[CharBBox], text: str) -> None:
    print(f"\n== Char boxes == {len(char_bboxes)}")
    for idx, char_box in enumerate(char_bboxes):
        print(f"  index char box {idx}:")
        print(f"    char: {char_box.text!r}")
        print(f"    byte index: {char_box.byte_index}")
        print(f"    byte length: {char_box.byte_length}")
        if char_box.text is not None and char_box.byte_length is not None:
            assert char_box.byte_length == len(char_box.text.encode("utf-8"))
    assert len(char_bboxes) == len(text), (
        f"Expected number of char boxes to be equal to number of characters in text, "
        f"but got {len(char_bboxes)} char boxes and {len(text)} characters"
    )


def _print_cluster_bboxes(cluster_bboxes: list[ClusterBBox]) -> None:
    print(f"\n== Cluster boxes == {len(cluster_bboxes)}")
    for idx, cluster_box in enumerate(cluster_bboxes):
        print(f"  index cluster box {idx}:")
        print(f"    cluster text: {cluster_box.text!r}")
        print(f"    byte index: {cluster_box.byte_index}")
        print(f"    byte length: {cluster_box.byte_length}")
        if cluster_box.text is not None:
            assert cluster_box.byte_length == len(cluster_box.text.encode("utf-8"))


def _print_run_bboxes(run_bboxes: list[RunBBox]) -> None:
    print(f"\n== Run boxes == {len(run_bboxes)}")
    for idx, run_box in enumerate(run_bboxes):
        print(f"  index run box {idx}:")
        print(f"    run text: {run_box.text!r}")
        print(f"    byte index: {run_box.byte_index}")
        print(f"    byte length: {run_box.byte_length}")
        if run_box.text is not None:
            assert run_box.byte_length == len(run_box.text.encode("utf-8"))


def _print_line_bboxes(line_bboxes: list[LineBBox]) -> None:
    print(f"\n== Line boxes == {len(line_bboxes)}")
    for idx, line_box in enumerate(line_bboxes):
        print(f"  index line box {idx}:")
        print(f"    line text: {line_box.text!r}")
        print(f"    byte index: {line_box.byte_index}")
        print(f"    byte length: {line_box.byte_length}")
        print(f"    direction: {line_box.resolved_direction}")
        print(f"    is paragraph start: {line_box.is_paragraph_start}")
        if line_box.text is not None:
            assert line_box.byte_length == len(line_box.text.encode("utf-8"))


def _print_bboxes(text: str, block_result: TextBlockBBoxesResult | TableBlockBBoxesResult | None, i: int) -> None:
    if block_result is None:
        print(f"block {i}: image block (no text bounding boxes)")
        return
    if isinstance(block_result, TableBlockBBoxesResult):
        print(f"block {i}: table block ({len(block_result.cell_bboxes)} cells, skipping detail)")
        return
    bboxes = block_result.bboxes
    print(f"block {i}:")
    print(f"Text: {text!r}")
    print(f"Text length: {len(text)}")
    print(f"Text length in bytes: {len(text.encode('utf-8'))}")
    if bboxes.char_bboxes is not None:
        _print_char_bboxes(bboxes.char_bboxes, text)
    if bboxes.cluster_bboxes is not None:
        _print_cluster_bboxes(bboxes.cluster_bboxes)
    if bboxes.run_bboxes is not None:
        _print_run_bboxes(bboxes.run_bboxes)
    if bboxes.line_bboxes is not None:
        _print_line_bboxes(bboxes.line_bboxes)
    if bboxes.layout_bbox is not None:
        print("\n== Layout box ==")
        print(f"  layout text: {bboxes.layout_bbox.text!r}")


def _print_block_bboxes(block_bboxes_result: BlockBBoxesResult) -> None:
    print("\n== Block boxes ==")
    print(f"  surface bbox: {block_bboxes_result.surface_bbox}")
    print(f"  content bbox: {block_bboxes_result.content_bbox}")
    for block_bbox in block_bboxes_result.block_bboxes:
        print(f"  block {block_bbox.name!r}: {block_bbox.bbox}")


def playground_document_pipeline(text: str) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    TEXT_BBOXES_DIR.mkdir(parents=True, exist_ok=True)
    BLOCK_BBOXES_DIR.mkdir(parents=True, exist_ok=True)

    colors = ColorSelector()
    white = SolidColorSpec(color=colors.by_names(["white"])[0])
    black = SolidColorSpec(color=colors.by_names(["black"])[0])

    font_setup = FontSetup()
    font_setup.setup_font(
        mode=FontconfigMode.TEMPLATE_MINIMAL,
        font_dir=FONTS_DIR,
        fontconfig_destination_dir=OUTPUT_DIR,
    )

    surface_config = SurfaceConfigManager().create_image_surface_config(width=800, height=200)

    canvas_config = DocumentConfig(
        surface_config=surface_config,
        global_margin=Margin(top=5, right=5, bottom=5, left=5),
        background_spec=white,
    )

    blocks_config = DocumentBlocksConfig(
        surface_config=surface_config,
        blocks=[
            TextBlock(
                text=text,
                text_style=TextStyle(
                    font_description_params=FontDescriptionInterfaceParameters(
                        family="Noto Sans", size_device_units=48
                    ),
                    text_color_spec=black,
                ),
            ),
        ],
    )

    pipeline = DocumentRenderPipeline()
    setup = pipeline.setup(config=canvas_config)
    rendered = pipeline.render(blocks_config=blocks_config, setup_result=setup)

    output_path = OUTPUT_DIR / "output.png"
    pipeline.save_as_file(
        surface=setup.surface,
        surface_config=surface_config,
        output_file_path=output_path,
        stream=setup.stream,
    )

    block_bboxes = pipeline.get_block_bounding_boxes(setup_result=setup)
    _print_block_bboxes(block_bboxes)
    json_path = BLOCK_BBOXES_DIR / "block_bboxes.json"
    json_path.write_text(json.dumps(block_bboxes.to_dict(), indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"saved → {json_path}")

    text_bboxes = pipeline.get_text_bounding_boxes(rendered_blocks=rendered.rendered_blocks)
    for i, block_result in enumerate(text_bboxes):
        _print_bboxes(text=text, block_result=block_result, i=i)

    text_drawer = ImageTextBoundingBoxDrawer()
    block_drawer = ImageBlockBoundingBoxDrawer()
    base_image = Image.open(output_path)

    for name, annotated in block_drawer.draw_per_block(base_image, block_bboxes):
        block_bbox_path = BLOCK_BBOXES_DIR / f"block_bboxes_{name}.png"
        annotated.save(block_bbox_path)
        print(f"saved → {block_bbox_path}")
    for block_result in text_bboxes:
        if not isinstance(block_result, TextBlockBBoxesResult):
            continue
        per_level = text_drawer.draw_per_level(base_image, block_result.bboxes)
        for level, annotated in per_level:
            level_path = TEXT_BBOXES_DIR / f"bboxes_{level.value}.png"
            annotated.save(level_path)
            print(f"saved → {level_path}")
        for level_key, level_data in block_result.bboxes.to_dict().items():
            level_name = level_key.removesuffix("_bboxes").removesuffix("_bbox")
            json_path = TEXT_BBOXES_DIR / f"bboxes_{level_name}.json"
            json_path.write_text(json.dumps(level_data, indent=2, ensure_ascii=False), encoding="utf-8")
            print(f"saved → {json_path}")

    print(f"saved → {output_path}")


if __name__ == "__main__":
    # text = " A🐼 \n1"
    # text = "مرAحبا"  # noqa: RUF001, RUF003, RUF100
    # text = "café"
    text = """ Hello 你好"""
    playground_document_pipeline(text=text)
