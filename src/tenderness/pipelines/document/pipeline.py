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

"""Document render pipeline."""

from __future__ import annotations

import warnings
from typing import TYPE_CHECKING

import gi

from tenderness.bounding_boxes.bounding_boxes_schema import Quadrilateral
from tenderness.bounding_boxes.text_bounding_box_extractor import TextBoundingBoxExtractor
from tenderness.cairo_backend.pixel_formats import ChannelOrder
from tenderness.core.sentinel import _UNSET_PARAM, Settable
from tenderness.image_backend.image_placer import ImagePlacer, ImagePlacerParameters
from tenderness.image_backend.surface_array_converter import (
    SurfaceArrayBackend,
    SurfaceArrayConverterParameters,
    SurfaceArrayResult,
)
from tenderness.image_backend.surface_writer import SurfaceWriterParameters
from tenderness.layout_engines.minimal_flexbox.minimal_flexbox import MinimalFlexBox
from tenderness.pango_backend.layout_interface import LayoutInterface, TextStrategy
from tenderness.pango_backend.layout_interface_geometry import HeightDeviceUnits
from tenderness.pipelines.document.bbox_helper import (
    BlockBBox,
    BlockBBoxesResult,
    CellBBox,
    TableBlockBBoxesResult,
    TextBlockBBoxesResult,
)
from tenderness.pipelines.document.image_block_helpers import ImageBlock, ImageBlockResult
from tenderness.pipelines.document.pipeline_schema import (
    DocumentConfig,
    DocumentRenderResult,
    DocumentSetupResult,
)
from tenderness.pipelines.document.setup_helpers import BlockPosition, DocumentSetupHelpers
from tenderness.pipelines.document.table_block_helpers import (
    TableBlock,
    TableBlockHelpers,
    TableBlockResult,
    TextCell,
    TextCellResult,
)
from tenderness.pipelines.document.text_block_helpers import (
    TextBlock,
    TextBlockHelpers,
    TextBlockResult,
    TextStyle,
)
from tenderness.pipelines.renderer_configurator import RendererConfigurator

gi.require_version("Pango", "1.0")
from gi.repository import Pango  # noqa: E402

if TYPE_CHECKING:
    import io
    import pathlib

    import cairo

    from tenderness.bounding_boxes.bounding_boxes_schema import BoundingBoxType
    from tenderness.cairo_backend.surface_configuration import SurfaceConfig
    from tenderness.core.geometry import Rectangle
    from tenderness.pipelines.document.pipeline_schema import DocumentBlocksConfig


class DocumentRenderPipeline:
    """Two-phase document rendering pipeline.

    Notes
    -----
    1. Call ``setup()`` with a ``DocumentConfig`` to create the surface and resolve block positions.
    2. Call ``render()`` with a ``DocumentBlocksConfig`` and the setup result to render all blocks.
    """

    def __init__(self) -> None:
        self.renderer_configurator = RendererConfigurator()
        self.image_placer = ImagePlacer()
        self.minimal_flexbox_engine = MinimalFlexBox()
        self.text_bounding_box_extractor = TextBoundingBoxExtractor()

    def setup(self, config: DocumentConfig) -> DocumentSetupResult:
        """Run the document setup phase.

        Parameters
        ----------
        config
            Document configuration.

        Returns
        -------
        DocumentSetupResult
            Result of the setup phase.
        """
        # 1. Create surface
        surface, stream = self.renderer_configurator.create_surface(
            surface_config=config.surface_config,
        )

        # 2. Create cairo context
        cairo_context = self.renderer_configurator.create_cairo_context(
            surface=surface,
        )

        # 3. Apply background color
        DocumentSetupHelpers.apply_background_color(
            renderer_configurator=self.renderer_configurator,
            config=config,
            cairo_context=cairo_context,
        )

        # 4. Get surface rect
        surface_rect = config.surface_config.rect

        # 5. Apply global margin -> content rect and document margin
        content_rect, document_margin = DocumentSetupHelpers.apply_global_margin(
            config=config,
            surface_rect=surface_rect,
        )

        # 6. Resolve block positions
        block_positions = DocumentSetupHelpers.resolve_block_positions(
            minimal_flexbox_engine=self.minimal_flexbox_engine,
            config=config,
            content_rect=content_rect,
        )

        return DocumentSetupResult(
            surface_rect=surface_rect,
            content_rect=content_rect,
            document_margin=document_margin,
            block_positions=block_positions,
            surface=surface,
            stream=stream,
            cairo_context=cairo_context,
            surface_config=config.surface_config,
        )

    def render(
        self,
        blocks_config: DocumentBlocksConfig,
        setup_result: DocumentSetupResult,
    ) -> DocumentRenderResult:
        """Run the document render phase.

        Parameters
        ----------
        blocks_config
            Blocks configuration for rendering.
        setup_result
            Output from the setup phase.

        Returns
        -------
        DocumentRenderResult
            Result of the render phase.

        Raises
        ------
        TypeError
            If a block type is not supported.
        """
        # 1. Create base text layout template if base_text_style is set (can be overridden by block-level styles)
        base_text_layout_template = TextBlockHelpers.create_base_text_layout_template(
            renderer_configurator=self.renderer_configurator,
            cairo_context=setup_result.cairo_context,
            text_style=blocks_config.base_text_style,
        )

        # 2. Render blocks in order, passing overflow text from one TextBlock to the next
        pending_overflow_text: str | None = None

        rendered_blocks: list[TextBlockResult | ImageBlockResult | TableBlockResult] = []

        for block, block_position in zip(
            blocks_config.blocks,
            setup_result.block_positions,
            strict=True,
        ):
            if isinstance(block, TextBlock):
                (
                    layout_interface,
                    ctm_cairo_matrix,
                    block_text_overflow,
                ) = self._render_text_block(
                    setup_result=setup_result,
                    text_block=block,
                    text_block_position=block_position,
                    pending_overflow_text=pending_overflow_text,
                    base_text_layout_template=base_text_layout_template,
                    base_text_style=blocks_config.base_text_style,
                )
                if block.text is _UNSET_PARAM:
                    # Receiver consumed pending_overflow_text; store whatever still didn't fit
                    pending_overflow_text = block_text_overflow
                elif block_text_overflow is not None:
                    # Source block produced overflow; store it for the next receiver
                    pending_overflow_text = block_text_overflow
                # else: source block fit cleanly — leave pending_overflow_text untouched

                rendered_blocks.append(
                    TextBlockResult(
                        block_name=block.block_name,
                        block_position_name=block_position.name,
                        block_position_rect=block_position.rect,
                        layout_interface=layout_interface,
                        ctm_cairo_matrix=ctm_cairo_matrix,
                    )
                )

            elif isinstance(block, ImageBlock):
                self._render_image_block(
                    setup_result=setup_result,
                    image_block=block,
                    image_block_position=block_position,
                )
                rendered_blocks.append(
                    ImageBlockResult(
                        block_name=block.block_name,
                        block_position_name=block_position.name,
                        block_position_rect=block_position.rect,
                    )
                )

            elif isinstance(block, TableBlock):
                cell_results = self._render_table_block(
                    setup_result=setup_result,
                    table_block=block,
                    table_block_position=block_position,
                )
                rendered_blocks.append(
                    TableBlockResult(
                        block_name=block.block_name,
                        block_position_name=block_position.name,
                        block_position_rect=block_position.rect,
                        result_cells=cell_results,
                    )
                )

            else:
                msg = f"Unsupported block type: {type(block)!r}"
                raise TypeError(msg)

        return DocumentRenderResult(
            rendered_blocks=rendered_blocks,
        )

    def _render_text_unit(  # noqa: C901
        self,
        text: str,
        text_style: Settable[TextStyle],
        text_strategy: TextStrategy | str,
        base_text_layout_template: Settable[Pango.Layout],
        base_text_style: Settable[TextStyle],
        rect: Rectangle,
        surface_config: SurfaceConfig,
        cairo_context: cairo.Context[cairo.Surface],
    ) -> tuple[LayoutInterface, cairo.Matrix, str | None]:

        if base_text_layout_template is not _UNSET_PARAM:
            # 1.1 Create layout interface -> copy the template so each block gets an isolated snapshot;
            # without copying, every block wraps the same Pango.Layout object and later renders would
            # overwrite earlier blocks' layouts, corrupting stored TextBlockResult.layout_interface refs.
            layout_interface = self.renderer_configurator.create_layout_interface_from_existing(
                layout=base_text_layout_template.copy()
            )
        else:
            # 1.2 Create layout interface from cairo context -> no shared parameters to apply
            layout_interface = self.renderer_configurator.create_layout_interface_from_cairo_context(
                cairo_context=cairo_context,
            )

        # 2. Add text to layout
        layout_interface.add_text_to_layout(text=text, strategy=text_strategy)

        # 3. Apply unit-level pango text styles (if any) - overriding base layout template styles where applicable
        if text_style is not _UNSET_PARAM:
            TextBlockHelpers.apply_pango_text_style(
                renderer_configurator=self.renderer_configurator,
                layout_interface=layout_interface,
                text_style=text_style,
            )

        # 4. Save cairo context state and translate to block position
        cairo_context.save()
        cairo_context.translate(rect.x, rect.y)
        # cairo transforms are cumulative - need to capture only needed translation (block OR template)
        post_translate_matrix = cairo_context.get_matrix()

        # 5. Apply base cairo styles (if any)
        if base_text_style is not _UNSET_PARAM:
            TextBlockHelpers.apply_cairo_text_style(
                surface_config=surface_config,
                renderer_configurator=self.renderer_configurator,
                cairo_context=cairo_context,
                text_style=base_text_style,
            )

        # 6. Apply unit-level cairo styles (if any)
        if text_style is not _UNSET_PARAM:
            if text_style.context_transform_params is not _UNSET_PARAM:
                cairo_context.set_matrix(
                    post_translate_matrix
                )  # discard base style transforms to prevent them from affecting block-level transforms
            TextBlockHelpers.apply_cairo_text_style(
                surface_config=surface_config,
                renderer_configurator=self.renderer_configurator,
                cairo_context=cairo_context,
                text_style=text_style,
            )

        # 7. Constrain layout to rect (unless explicitly overridden by style)
        if not TextBlockHelpers.text_style_has_explicit_width(
            text_style
        ) and not TextBlockHelpers.text_style_has_explicit_width(base_text_style):
            layout_interface.width_device_units = rect.width
        if not TextBlockHelpers.text_style_has_explicit_height(  # noqa: SIM102
            text_style
        ) and not TextBlockHelpers.text_style_has_explicit_height(base_text_style):
            # set_height with ELLIPSIZE_NONE and a positive value is undefined behaviour per
            # Pango docs and causes multi-column layout where the second column is rendered
            # outside the Cairo clip, making overflow content invisible. Only apply it when
            # ellipsization is active; Cairo's clip rect handles the visual boundary otherwise.
            if layout_interface.ellipsize != Pango.EllipsizeMode.NONE:
                layout_interface.height_device_units = rect.height

        # 8. Capture layout overflow
        intended_height = HeightDeviceUnits(height=rect.height)
        fit_report = layout_interface.get_layout_fit_report(height_override=intended_height)
        overflow_text = fit_report.clipped_text.clipped or None

        # Trim layout to visible for TEXT strategy (MARKUP can't be trimmed safely)
        if overflow_text is not None:
            if text_strategy is TextStrategy.TEXT:
                layout_interface.set_text(text=fit_report.clipped_text.visible)
            else:
                warnings.warn(
                    f"Text overflow with {text_strategy!r} strategy cannot be trimmed — only {TextStrategy.TEXT!r} supports trimming. Overflow will be clipped by Cairo.",
                    category=UserWarning,
                    stacklevel=3,
                )

        # 9. Clip layout to rect
        cairo_context.new_path()
        cairo_context.rectangle(0, 0, rect.width, rect.height)
        cairo_context.clip()
        cairo_context.move_to(0, 0)

        # 10. Render layout
        self.renderer_configurator.show_layout(
            cairo_context=cairo_context,
            pango_layout=layout_interface.pango_layout,
        )
        ctm_cairo_matrix = cairo_context.get_matrix()
        cairo_context.restore()  # restore to undo block translation and styles

        return layout_interface, ctm_cairo_matrix, overflow_text

    # ------------------------------------------------------------------
    # Block logic
    # ------------------------------------------------------------------
    def _render_text_block(
        self,
        setup_result: DocumentSetupResult,
        text_block: TextBlock,
        text_block_position: BlockPosition,
        pending_overflow_text: str | None,
        base_text_layout_template: Settable[Pango.Layout],
        base_text_style: Settable[TextStyle],
    ) -> tuple[LayoutInterface, cairo.Matrix, str | None]:

        # 1. Resolve text for this block (handle overflow from previous block if text is _UNSET_PARAM)
        resolved_text = TextBlockHelpers.resolve_text_for_block(
            text_block=text_block,
            pending_overflow_text=pending_overflow_text,
        )

        return self._render_text_unit(
            text=resolved_text,
            text_style=text_block.text_style,
            text_strategy=text_block.text_strategy,
            base_text_layout_template=base_text_layout_template,
            base_text_style=base_text_style,
            rect=text_block_position.rect,
            surface_config=setup_result.surface_config,
            cairo_context=setup_result.cairo_context,
        )

    def _render_table_block(
        self,
        setup_result: DocumentSetupResult,
        table_block: TableBlock,
        table_block_position: BlockPosition,
    ) -> list[TextCellResult]:

        # 1. Resolve cell rectangles
        cells_rects = TableBlockHelpers.create_cells_within_container(
            minimal_flexbox_engine=self.minimal_flexbox_engine,
            container_rect=table_block_position.rect,
            node=table_block.table_cell_pos,
        )

        if len(table_block.cells) != len(cells_rects):
            msg = f"Number of table cells ({len(table_block.cells)}) does not match number of cell rectangles ({len(cells_rects)})."
            raise ValueError(msg)

        # 2. Create base text layout template for cells (if base_text_style is set) — can be overridden by cell-level styles
        base_cell_layout_template = TextBlockHelpers.create_base_text_layout_template(
            renderer_configurator=self.renderer_configurator,
            cairo_context=setup_result.cairo_context,
            text_style=table_block.base_text_style,
        )

        rendered_cells: list[TextCellResult] = []

        for cell, cell_position in zip(table_block.cells, cells_rects, strict=True):
            if isinstance(cell, TextCell):
                layout_interface, ctm_matrix, _ = self._render_text_unit(
                    text=cell.text,
                    text_style=cell.text_style,
                    text_strategy=cell.text_strategy,
                    base_text_layout_template=base_cell_layout_template,
                    base_text_style=table_block.base_text_style,
                    rect=cell_position.rect,
                    surface_config=setup_result.surface_config,
                    cairo_context=setup_result.cairo_context,
                )
                rendered_cells.append(
                    TextCellResult(
                        cell_name=cell.cell_name,
                        cell_position_name=cell_position.name,
                        cell_position_rect=cell_position.rect,
                        layout_interface=layout_interface,
                        ctm_cairo_matrix=ctm_matrix,
                    )
                )
            else:
                msg = f"Unsupported cell type: {type(cell)!r}"
                raise TypeError(msg)

        return rendered_cells

    def _render_image_block(
        self,
        setup_result: DocumentSetupResult,
        image_block: ImageBlock,
        image_block_position: BlockPosition,
    ) -> None:
        img_palacer_params = ImagePlacerParameters(
            path_to_image=image_block.path_to_image,
            dest_rect=image_block_position.rect,
            scale_mode=image_block.scale_mode,
            operator=image_block.operator,
            alpha=image_block.alpha,
            image_format=image_block.image_format,
        )

        self.image_placer.place(
            cairo_context=setup_result.cairo_context,
            params=img_palacer_params,
        )

    # --------------------------
    # Bounding boxes
    # --------------------------
    def get_text_bounding_boxes(
        self,
        rendered_blocks: list[TextBlockResult | ImageBlockResult | TableBlockResult],
        levels: set[BoundingBoxType] | None = None,
        *,
        include_text: bool = True,
    ) -> list[TextBlockBBoxesResult | TableBlockBBoxesResult | None]:
        """Extract text bounding boxes from rendered blocks.

        Parameters
        ----------
        rendered_blocks
            Rendered block results from ``render()``.
        levels
            Bounding box granularity levels to extract; ``None`` uses defaults.
        include_text
            Whether to include source text in each bounding box.

        Returns
        -------
        list[TextBlockBBoxesResult | TableBlockBBoxesResult | None]
            One entry per block; ``None`` for image blocks.

        Raises
        ------
        TypeError
            If a block type is not supported.
        """
        bbox_collections: list[TextBlockBBoxesResult | TableBlockBBoxesResult | None] = []

        for block in rendered_blocks:
            if isinstance(block, TextBlockResult):
                bboxes = self.text_bounding_box_extractor.extract_bounding_boxes(
                    pango_layout=block.layout_interface.pango_layout,
                    matrix=block.ctm_cairo_matrix,
                    levels=levels,
                    include_text=include_text,
                )
                bbox_collections.append(
                    TextBlockBBoxesResult(
                        block_name=block.block_name,
                        block_position_name=block.block_position_name,
                        bboxes=bboxes,
                    )
                )
            elif isinstance(block, TableBlockResult):
                cell_bboxes = [
                    CellBBox(
                        cell_name=cell.cell_name,
                        cell_position_name=cell.cell_position_name,
                        bboxes=self.text_bounding_box_extractor.extract_bounding_boxes(
                            pango_layout=cell.layout_interface.pango_layout,
                            matrix=cell.ctm_cairo_matrix,
                            levels=levels,
                            include_text=include_text,
                        ),
                    )
                    for cell in block.result_cells
                ]
                bbox_collections.append(
                    TableBlockBBoxesResult(
                        block_name=block.block_name,
                        block_position_name=block.block_position_name,
                        cell_bboxes=cell_bboxes,
                    )
                )
            elif isinstance(block, ImageBlockResult):
                bbox_collections.append(None)  # ImageBlocks don't have text bounding boxes

            else:
                msg = f"Unsupported block type: {type(block)!r}"
                raise TypeError(msg)

        return bbox_collections

    def get_block_bounding_boxes(self, setup_result: DocumentSetupResult) -> BlockBBoxesResult:
        """Extract block bounding boxes from the setup result.

        Parameters
        ----------
        setup_result
            Output from the setup phase.

        Returns
        -------
        BlockBBoxesResult
            Block bounding boxes.
        """
        surface_bbox = Quadrilateral(*setup_result.surface_rect.corners)
        content_bbox = Quadrilateral(*setup_result.content_rect.corners)
        block_bboxes = [
            BlockBBox(name=bp.name, bbox=Quadrilateral(*bp.rect.corners)) for bp in setup_result.block_positions
        ]

        return BlockBBoxesResult(
            surface_bbox=surface_bbox,
            content_bbox=content_bbox,
            block_bboxes=block_bboxes,
        )

    # --------------------------
    # Save as file
    # --------------------------
    def save_as_file(
        self,
        surface: cairo.Surface,
        surface_config: SurfaceConfig,
        output_file_path: pathlib.Path,
        stream: io.BytesIO | None = None,
        *,
        finish_after: bool = True,
    ) -> pathlib.Path:
        """Save the rendered surface to a file.

        Parameters
        ----------
        surface
            Cairo surface to save.
        surface_config
            Surface configuration.
        output_file_path
            Destination file path.
        stream
            Byte stream for in-memory surfaces, or ``None``.
        finish_after
            Whether to finish the surface after writing.

        Returns
        -------
        pathlib.Path
            Path to the written file.
        """
        return self.renderer_configurator.surface_writer.save_as_file(
            surface=surface,
            surface_config=surface_config,
            surface_writer_params=SurfaceWriterParameters(
                output_file_path=output_file_path,
                finish_after=finish_after,
            ),
            stream=stream,
        )

    # --------------------------
    # As array
    # --------------------------
    def to_array(
        self,
        surface: cairo.Surface,
        surface_config: SurfaceConfig,
        *,
        channel_order: ChannelOrder | None = ChannelOrder.RGB,
        copy: bool = True,
        backend: SurfaceArrayBackend = SurfaceArrayBackend.NUMPY,
        finish_after: bool = True,
    ) -> SurfaceArrayResult:
        """Convert the rendered surface to an array.

        Parameters
        ----------
        surface
            Cairo surface to convert.
        surface_config
            Surface configuration.
        channel_order
            Output channel order, or ``None`` to keep the native order.
        copy
            Whether to copy the surface data.
        backend
            Array backend to use.
        finish_after
            Whether to finish the surface after conversion.

        Returns
        -------
        SurfaceArrayResult
            Array representation of the surface.
        """
        return self.renderer_configurator.surface_array_converter.surface_to_array(
            surface=surface,
            surface_config=surface_config,
            surface_array_converter_params=SurfaceArrayConverterParameters(
                channel_order=channel_order,
                copy=copy,
                backend=backend,
                finish_after=finish_after,
            ),
        )
