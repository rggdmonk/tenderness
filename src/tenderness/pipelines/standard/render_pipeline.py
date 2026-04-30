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

"""Standard rendering pipeline."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

import gi

from tenderness.bounding_boxes.bounding_boxes_schema import (
    BoundingBoxStrategy,
    Tetragon,
)
from tenderness.bounding_boxes.text_bounding_box_extractor import TextBoundingBoxExtractor
from tenderness.core.sentinel import _UNSET_PARAM
from tenderness.image_backend.image_placer import ImagePlacer, ImagePlacerParameters
from tenderness.layout_engines.minimal_flexbox.minimal_flexbox import MinimalFlexBox, MinimalFlexNode
from tenderness.layout_engines.position_helpers import PositionHelpers
from tenderness.pango_backend.layout_interface import TextStrategy
from tenderness.pango_backend.layout_interface_geometry import HeightDeviceUnits, WidthDeviceUnits
from tenderness.pipelines.renderer_configurator import RendererConfigurator
from tenderness.pipelines.standard.render_blocks import (
    BlocksConfig,
    ImageBlock,
    TableBlock,
    TextBlock,
    TextStyle,
)
from tenderness.pipelines.standard.render_pipeline_models import (
    BlockBoundingBoxesResult,
    BlockPosition,
    BlockResult,
    ImageBlockResult,
    RenderTextResult,
    SetupRenderResult,
    TableBlockResult,
    TextBlockResult,
)

gi.require_version("PangoCairo", "1.0")

from gi.repository import Pango, PangoCairo  # noqa: E402

if TYPE_CHECKING:
    import io
    import pathlib

    import cairo

    from tenderness.bounding_boxes.bounding_boxes_schema import (
        BoundingBoxType,
        LayoutBBoxCollection,
    )
    from tenderness.cairo_backend.surface_configuration import SurfaceConfig
    from tenderness.core.geometry import Rectangle
    from tenderness.image_backend.surface_array_converter import (
        SurfaceArrayConverterParameters,
        SurfaceArrayResult,
    )
    from tenderness.image_backend.surface_writer import SurfaceWriterParameters
    from tenderness.pango_backend.layout_interface import LayoutInterface
    from tenderness.pipelines.standard.render_blocks import CanvasConfig


def _style_has_explicit_width(style: TextStyle | None) -> bool:
    return (
        style is not None
        and style.layout_interface_params is not _UNSET_PARAM
        and (
            style.layout_interface_params.width_device_units is not _UNSET_PARAM
            or style.layout_interface_params.width is not _UNSET_PARAM
        )
    )


def _style_has_explicit_height(style: TextStyle | None) -> bool:
    return (
        style is not None
        and style.layout_interface_params is not _UNSET_PARAM
        and (
            style.layout_interface_params.height_device_units is not _UNSET_PARAM
            or style.layout_interface_params.height is not _UNSET_PARAM
        )
    )


def _apply_height_constraint(
    layout_interface: LayoutInterface,
    height: float,
) -> None:
    """
    Apply height constraint only when ellipsization is active.

    set_height with ELLIPSIZE_NONE and a value other than -1 is undefined
    behavior per Pango docs. With ELLIPSIZE_NONE, height clipping is handled
    by get_layout_fit_report instead.
    """
    if layout_interface.ellipsize != Pango.EllipsizeMode.NONE:
        layout_interface.height_device_units = HeightDeviceUnits(height=height)


@dataclass(slots=True)
class _PreparedTextStyle:
    """Bundles the default TextStyle with its pre-built Pango template.

    The template carries Pango-level formatting (font, wrapping, etc.) that can be shared
    across TextBlocks via copy(). Cairo state (transforms, colors) cannot be baked into a
    Pango template — it must be applied per-block at render time — so those are read from
    ``style`` separately in ``_render_text_block``.
    """

    style: TextStyle
    template: Pango.Layout


class RenderPipeline:
    """Implements the standard rendering pipeline, orchestrating the setup, rendering, and bounding box extraction processes."""

    def __init__(self) -> None:
        self.renderer_configurator = RendererConfigurator()
        self.text_bounding_box_extractor = TextBoundingBoxExtractor()
        self.image_placer = ImagePlacer()

        self.minimal_flexbox_engine = MinimalFlexBox()
        self.position_helpers = PositionHelpers()

    # --------------------------
    # Setup render
    # --------------------------
    def setup_render(  # noqa: D102 TODO: docstring
        self,
        canvas_config: CanvasConfig,
    ) -> SetupRenderResult:

        # 1. Create surface
        surface, stream = self.renderer_configurator.create_surface(surface_config=canvas_config.surface_config)

        # 2. Create cairo context
        cairo_context = self.renderer_configurator.create_cairo_context(surface=surface)

        # 3. Apply background color
        if canvas_config.background_spec is not _UNSET_PARAM:
            self.renderer_configurator.background_selector.add_background_color(
                cairo_context=cairo_context,
                surface_config=canvas_config.surface_config,
                background_color_spec=canvas_config.background_spec,
            )

        surface_rect = canvas_config.surface_config.rect

        # 4. Apply global margin -> content rect and canvas margin
        if canvas_config.global_margin is not _UNSET_PARAM:
            content_rect, canvas_margin = self.position_helpers.inset_rect(
                rect=surface_rect, margin=canvas_config.global_margin
            )
        else:
            content_rect, canvas_margin = self.position_helpers.inset_rect(rect=surface_rect)

        # 5. Resolve block positions -> block rects
        if canvas_config.block_spec is not _UNSET_PARAM:
            result_tree = self.minimal_flexbox_engine.resolve_tree(
                container=content_rect, node=canvas_config.block_spec
            )
            block_positions = [BlockPosition(name=node.name, rect=rect) for node, rect in result_tree]
        else:
            block_positions = [BlockPosition(name="main", rect=content_rect)]

        return SetupRenderResult(
            surface_rect=surface_rect,
            content_rect=content_rect,
            canvas_margin=canvas_margin,
            block_positions=block_positions,
            surface=surface,
            stream=stream,
            cairo_context=cairo_context,
        )

    # --------------------------
    # Render
    # --------------------------
    def render_text(self, blocks_config: BlocksConfig, setup_render: SetupRenderResult) -> RenderTextResult:  # noqa: D102 TODO: docstring

        cairo_context = setup_render.cairo_context
        block_positions = setup_render.block_positions

        # 4. Build shared text layout template from default style (if any)
        prepared_text_style: _PreparedTextStyle | None = None
        if blocks_config.default_text_style is not None:
            template = self._create_text_layout_template(
                cairo_context=cairo_context,
                text_style=blocks_config.default_text_style,
            )
            prepared_text_style = _PreparedTextStyle(style=blocks_config.default_text_style, template=template)

        # Render blocks with overflow tracking
        pending_overflow: str | None = None

        rendered_blocks: list[BlockResult] = []

        for block, block_pos in zip(blocks_config.blocks, block_positions, strict=True):
            if isinstance(block, TextBlock):
                layout_interface, block_overflow, rendering_matrix = self._render_text_block(
                    cairo_context=cairo_context,
                    surface_config=blocks_config.surface_config,
                    block=block,
                    rect=block_pos.rect,
                    pending_overflow=pending_overflow,
                    prepared_text_style=prepared_text_style,
                )
                if block.text is None:
                    # Receiver consumed pending_overflow; store whatever still didn't fit.
                    pending_overflow = block_overflow
                elif block_overflow is not None:
                    # Source block produced overflow; store it for the next receiver.
                    pending_overflow = block_overflow
                # else: non-receiver block that fit cleanly — leave pending_overflow untouched.
                rendered_blocks.append(
                    TextBlockResult(
                        position_name=block_pos.name,
                        block_name=block.block_name,
                        rect=block_pos.rect,
                        layout_interface=layout_interface,
                        matrix=rendering_matrix,
                    )
                )

            elif isinstance(block, ImageBlock):
                self._render_image_block(block=block, rect=block_pos.rect, cairo_context=cairo_context)
                rendered_blocks.append(
                    ImageBlockResult(position_name=block_pos.name, block_name=block.block_name, rect=block_pos.rect)
                )

            elif isinstance(block, TableBlock):
                cell_layouts, cells_rects, cell_matrices = self._render_table_block(
                    block=block,
                    rect=block_pos.rect,
                    surface_config=blocks_config.surface_config,
                    cairo_context=cairo_context,
                )
                rendered_blocks.append(
                    TableBlockResult(
                        position_name=block_pos.name,
                        table_name=block.block_name,
                        cell_names=[cell.cell_name for cell in block.cells],
                        cells_rects=cells_rects,
                        cell_layouts=cell_layouts,
                        cell_matrices=cell_matrices,
                    )
                )

            else:
                msg = f"Unsupported block type: {type(block)!r}"
                raise TypeError(msg)

        return RenderTextResult(rendered_blocks=rendered_blocks)

    # --------------------------
    # Bounding box for text
    # --------------------------
    def get_text_bounding_boxes(  # noqa: D102 TODO: docstring
        self,
        rendered_blocks: list[BlockResult],
        levels: set[BoundingBoxType] | None = None,
        text_mode: BoundingBoxStrategy = BoundingBoxStrategy.WITH_TEXT,
    ) -> list[LayoutBBoxCollection | list[LayoutBBoxCollection] | None]:

        bbox_collections: list[LayoutBBoxCollection | list[LayoutBBoxCollection] | None] = []

        for block in rendered_blocks:
            if isinstance(block, TextBlockResult):
                bbox_collection = self.text_bounding_box_extractor.extract_bounding_boxes(
                    pango_layout=block.layout_interface.pango_layout,
                    matrix=block.matrix,
                    origin=(0.0, 0.0),
                    levels=levels,
                    text_mode=text_mode,
                )
                bbox_collection.position_name = block.position_name
                bbox_collection.block_name = block.block_name
                bbox_collections.append(bbox_collection)
            elif isinstance(block, TableBlockResult):
                cell_bbox_collections = []
                for cell_name, cell_layout, cell_matrix in zip(
                    block.cell_names, block.cell_layouts, block.cell_matrices, strict=True
                ):
                    coll = self.text_bounding_box_extractor.extract_bounding_boxes(
                        pango_layout=cell_layout.pango_layout,
                        matrix=cell_matrix,
                        origin=(0.0, 0.0),
                        levels=levels,
                        text_mode=text_mode,
                    )
                    coll.position_name = block.position_name
                    coll.table_name = block.table_name
                    coll.cell_name = cell_name
                    cell_bbox_collections.append(coll)
                bbox_collections.append(cell_bbox_collections)
            else:
                bbox_collections.append(None)

        return bbox_collections

    def get_block_bounding_boxes(self, setup_render: SetupRenderResult) -> BlockBoundingBoxesResult:  # noqa: D102 TODO: docstring

        surface_bbox = Tetragon(*setup_render.surface_rect.corners)
        content_bbox = Tetragon(*setup_render.content_rect.corners)
        block_boxes = [Tetragon(*block_pos.rect.corners) for block_pos in setup_render.block_positions]

        return BlockBoundingBoxesResult(
            surface_bbox=surface_bbox,
            content_bbox=content_bbox,
            block_boxes=block_boxes,
        )

    # --------------------------
    # Save as file
    # --------------------------
    def save_as_file(  # noqa: D102 TODO: docstring
        self,
        surface: cairo.Surface,
        surface_config: SurfaceConfig,
        surface_writer_params: SurfaceWriterParameters,
        stream: io.BytesIO | None = None,
    ) -> pathlib.Path:

        return self.renderer_configurator.surface_writer.save_as_file(
            surface=surface,
            surface_config=surface_config,
            surface_writer_params=surface_writer_params,
            stream=stream,
        )

    # --------------------------
    # As array
    # --------------------------
    def to_array(  # noqa: D102 TODO: docstring
        self,
        surface: cairo.Surface,
        surface_config: SurfaceConfig,
        surface_array_converter_params: SurfaceArrayConverterParameters | None = None,
    ) -> SurfaceArrayResult:

        return self.renderer_configurator.surface_array_converter.surface_to_array(
            surface=surface,
            surface_config=surface_config,
            surface_array_converter_params=surface_array_converter_params,
        )

    # --------------------------
    # Text operations
    # --------------------------
    def _apply_text_style(
        self,
        cairo_context: cairo.Context[cairo.Surface],
        layout_interface: LayoutInterface,
        style: TextStyle,
    ) -> None:
        if style.font_options_params is not _UNSET_PARAM:
            font_options_interface = self.renderer_configurator.create_font_options_interface()
            font_options_interface.update_with_parameters(params=style.font_options_params)
            font_options_interface.apply_to_layout_interface(layout_interface=layout_interface)

        if style.font_description_params is not _UNSET_PARAM:
            font_description_interface = self.renderer_configurator.create_font_description_interface()
            font_description_interface.update_with_parameters(params=style.font_description_params)
            font_description_interface.apply_to_layout_interface(layout_interface=layout_interface)

        if style.layout_context_params is not _UNSET_PARAM:
            layout_context_interface = self.renderer_configurator.create_layout_context_interface_from_layout_interface(
                layout_interface=layout_interface,
            )
            layout_context_interface.update_with_parameters(params=style.layout_context_params)

        if style.layout_interface_params is not _UNSET_PARAM:
            layout_interface.update_with_parameters(params=style.layout_interface_params)

        if style.context_transform_params is not _UNSET_PARAM:
            pipeline = self.renderer_configurator.create_transform_pipeline_from_cairo_context(
                cairo_context=cairo_context
            )
            pipeline.update_with_parameters(transforms=style.context_transform_params)
            pipeline.apply_to_cairo_context(cairo_context=cairo_context)

    def _create_text_layout_template(
        self,
        cairo_context: cairo.Context[cairo.Surface],
        text_style: TextStyle,
    ) -> Pango.Layout:

        template_interface = self.renderer_configurator.create_layout_interface_from_cairo_context(
            cairo_context=cairo_context
        )
        cairo_context.save()
        self._apply_text_style(
            cairo_context=cairo_context,
            layout_interface=template_interface,
            style=text_style,
        )
        cairo_context.restore()

        return template_interface.pango_layout.copy()

    # --------------------------
    # Text block
    # --------------------------
    def _render_text_block(
        self,
        cairo_context: cairo.Context[cairo.Surface],
        surface_config: SurfaceConfig,
        block: TextBlock,
        rect: Rectangle,
        pending_overflow: str | None,
        prepared_text_style: _PreparedTextStyle | None,
    ) -> tuple[LayoutInterface, str | None, cairo.Matrix]:

        # 1. If block text is None, use pending overflow from previous block in flow (if any)
        text = block.text if block.text is not None else pending_overflow or ""

        if prepared_text_style is not None:
            # 2.1 Create layout interface from template copy (shared formatting already applied)
            layout_interface = self.renderer_configurator.create_layout_interface_from_existing(
                layout=prepared_text_style.template.copy()
            )
        else:
            # 2.2 Create layout interface from cairo context (no shared formatting)
            layout_interface = self.renderer_configurator.create_layout_interface_from_cairo_context(
                cairo_context=cairo_context
            )
        # 3. Add text
        if text:
            layout_interface.add_text_to_layout(text=text, strategy=block.text_strategy)

        cairo_context.save()
        cairo_context.translate(rect.x, rect.y)  # All transforms pivot at the block's own origin

        # 4. Apply default text style context transform (if any) — block-level transform composes on top
        if prepared_text_style is not None and prepared_text_style.style.context_transform_params is not _UNSET_PARAM:
            pipeline = self.renderer_configurator.create_transform_pipeline_from_cairo_context(
                cairo_context=cairo_context
            )
            pipeline.update_with_parameters(transforms=prepared_text_style.style.context_transform_params)
            pipeline.apply_to_cairo_context(cairo_context=cairo_context)

        # 5. Apply block-level style (overrides template defaults)
        if block.style is not None:
            self._apply_text_style(
                layout_interface=layout_interface,
                style=block.style,
                cairo_context=cairo_context,
            )

        # 6. Add text color (from default text style)
        if prepared_text_style is not None and prepared_text_style.style.text_color_spec is not _UNSET_PARAM:
            self.renderer_configurator.text_color_selector.add_text_color(
                cairo_context=cairo_context,
                surface_config=surface_config,
                text_color_spec=prepared_text_style.style.text_color_spec,
            )

        # 7. Add text color (from block-level style)
        if block.style is not None and block.style.text_color_spec is not _UNSET_PARAM:
            self.renderer_configurator.text_color_selector.add_text_color(
                cairo_context=cairo_context,
                surface_config=surface_config,
                text_color_spec=block.style.text_color_spec,
            )

        # Constrain to rectangle unless explicit width/height was set via layout_interface_params
        default_style = prepared_text_style.style if prepared_text_style is not None else None
        if not _style_has_explicit_width(block.style) and not _style_has_explicit_width(default_style):
            layout_interface.width_device_units = WidthDeviceUnits(width=rect.width)

        intended_height = HeightDeviceUnits(height=rect.height)

        if not _style_has_explicit_height(block.style) and not _style_has_explicit_height(default_style):
            _apply_height_constraint(layout_interface, rect.height)

        # Capture overflow before rendering. For TEXT strategy, also trim the layout to
        # the visible portion so PangoCairo.show_layout never paints overflow lines
        # (which would bleed through the Cairo clip as a partial first line).
        # MARKUP strategy cannot be trimmed this way — clipped_text.visible is plain text
        # and re-applying it would destroy the markup tags; Cairo clip handles the boundary.
        report = layout_interface.get_layout_fit_report(height_override=intended_height)

        overflow = report.clipped_text.clipped if report.clipped_text.has_clipped else None
        if overflow is not None and block.text_strategy is TextStrategy.TEXT:
            layout_interface.set_text(report.clipped_text.visible)

        cairo_context.new_path()
        cairo_context.rectangle(0, 0, rect.width, rect.height)
        cairo_context.clip()
        cairo_context.move_to(0, 0)

        # TODO: alias in renderer configurator for this function
        PangoCairo.show_layout(cairo_context, layout_interface.pango_layout)
        rendering_matrix = cairo_context.get_matrix()
        cairo_context.restore()

        return layout_interface, overflow, rendering_matrix

    # --------------------------
    # Image block
    # --------------------------
    def _render_image_block(
        self, block: ImageBlock, rect: Rectangle, cairo_context: cairo.Context[cairo.Surface]
    ) -> None:
        self.image_placer.place(
            cairo_context=cairo_context,
            params=ImagePlacerParameters(
                path_to_image=block.path_to_image,
                dest_rect=rect,
                scale_mode=block.scale_mode,
                operator=block.operator,
                alpha=block.alpha,
                image_format=block.image_format,
            ),
        )

    # --------------------------
    # Table block
    # --------------------------
    def _render_table_block(
        self,
        block: TableBlock,
        rect: Rectangle,
        surface_config: SurfaceConfig,
        cairo_context: cairo.Context[cairo.Surface],
    ) -> tuple[list[LayoutInterface], list[Rectangle], list[cairo.Matrix]]:

        # 1. Resolve cell rectangles from flexbox layout
        cells_rects, _ = self._create_cells_within_container(container_rect=rect, node=block.table_cell_pos)

        # 2. Validate cell count matches layout
        if len(block.cells) != len(cells_rects):
            msg = f"Number of table cells ({len(block.cells)}) does not match number of cell rectangles ({len(cells_rects)})."
            raise ValueError(msg)

        cell_layouts: list[LayoutInterface] = []
        cell_matrices: list[cairo.Matrix] = []

        # 3. Render each cell with independent styling
        for cell, cell_rect in zip(block.cells, cells_rects, strict=True):
            # Create fresh layout interface for this cell
            layout_interface = self.renderer_configurator.create_layout_interface_from_cairo_context(
                cairo_context=cairo_context
            )

            cell_text = str(cell.content)
            layout_interface.add_text_to_layout(text=cell_text, strategy=cell.text_strategy)

            cairo_context.save()
            cairo_context.translate(cell_rect.x, cell_rect.y)  # All transforms pivot at the cell's own origin

            # 4. Apply block-level defaults first
            if block.default_style is not None:
                self._apply_text_style(
                    layout_interface=layout_interface,
                    style=block.default_style,
                    cairo_context=cairo_context,
                )

            # 5. Then apply per-cell overrides (if any)
            if cell.style is not None:
                self._apply_text_style(
                    layout_interface=layout_interface,
                    style=cell.style,
                    cairo_context=cairo_context,
                )

            # 6. Text color (block-level)
            if block.default_style is not None and block.default_style.text_color_spec is not _UNSET_PARAM:
                self.renderer_configurator.text_color_selector.add_text_color(
                    cairo_context=cairo_context,
                    surface_config=surface_config,
                    text_color_spec=block.default_style.text_color_spec,
                )

            # 7. Text color (cell-level)
            if cell.style is not None and cell.style.text_color_spec is not _UNSET_PARAM:
                self.renderer_configurator.text_color_selector.add_text_color(
                    cairo_context=cairo_context,
                    surface_config=surface_config,
                    text_color_spec=cell.style.text_color_spec,
                )

            # 8. Constrain to cell rectangle unless explicit width/height was set via layout_interface_params
            if not _style_has_explicit_width(cell.style) and not _style_has_explicit_width(block.default_style):
                layout_interface.width_device_units = WidthDeviceUnits(width=cell_rect.width)

            if not _style_has_explicit_height(cell.style) and not _style_has_explicit_height(block.default_style):
                _apply_height_constraint(layout_interface, cell_rect.height)

            cairo_context.new_path()
            cairo_context.rectangle(0, 0, cell_rect.width, cell_rect.height)
            cairo_context.clip()
            cairo_context.move_to(0, 0)
            PangoCairo.show_layout(cairo_context, layout_interface.pango_layout)
            cell_matrices.append(cairo_context.get_matrix())
            cairo_context.restore()
            cell_layouts.append(layout_interface)

        return cell_layouts, cells_rects, cell_matrices

    def resolve_table_cell_positions(
        self,
        blocks_config: BlocksConfig,
        setup_render: SetupRenderResult,
    ) -> dict[str | None, list[tuple[str | None, Rectangle]]]:
        """Return cell positions for all TableBlocks, keyed by block_name, without rendering.

        Call this after setup_render but before render_text to get cell rects for
        drawing backgrounds/borders underneath the text.
        """
        result: dict[str | None, list[tuple[str | None, Rectangle]]] = {}
        for block, block_pos in zip(blocks_config.blocks, setup_render.block_positions, strict=True):
            if not isinstance(block, TableBlock):
                continue
            cells_rects, _ = self._create_cells_within_container(
                container_rect=block_pos.rect, node=block.table_cell_pos
            )
            if len(block.cells) != len(cells_rects):
                msg = f"Number of table cells ({len(block.cells)}) does not match number of cell rectangles ({len(cells_rects)})."
                raise ValueError(msg)
            result[block.block_name] = [
                (cell.cell_name, cell_rect) for cell, cell_rect in zip(block.cells, cells_rects, strict=True)
            ]
        return result

    def _create_cells_within_container(
        self, container_rect: Rectangle, node: MinimalFlexNode
    ) -> tuple[list[Rectangle], list[tuple[MinimalFlexNode, Rectangle]]]:

        result_tree = self.minimal_flexbox_engine.resolve_tree(container=container_rect, node=node)
        only_cell_rects = [rect for node, rect in result_tree]
        return only_cell_rects, result_tree
