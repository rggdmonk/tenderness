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


"""Utilities for drawing block bounding boxes (for debugging and visualization)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from lxml import etree
from PIL import Image, ImageDraw

if TYPE_CHECKING:
    from tenderness.bounding_boxes.bounding_boxes_schema import Quadrilateral
    from tenderness.pipelines.document.bbox_helper import BlockBBoxesResult


@dataclass
class BlockDrawConfig:
    """Drawing configuration for block bounding box overlays.

    Attributes
    ----------
    surface_color
        RGBA color for the surface bounding box.
    content_color
        RGBA color for the content area bounding box.
    block_color
        RGBA color for individual block bounding boxes.
    fill_alpha
        Alpha for the semi-transparent fill (0 = transparent, 255 = solid).
    draw_labels
        If ``True``, annotate boxes with their name.
    line_width
        Stroke width in pixels.
    """

    surface_color: tuple[int, int, int, int] = (255, 50, 180, 220)  # hot pink
    content_color: tuple[int, int, int, int] = (100, 220, 50, 220)  # lime green
    block_color: tuple[int, int, int, int] = (30, 144, 255, 220)  # dodger blue
    fill_alpha: int = 45
    draw_labels: bool = True
    line_width: int = 1


class ImageBlockBoundingBoxDrawer:
    """Draw block bounding boxes onto a PIL image as semi-transparent overlays."""

    def draw(
        self,
        image: Image.Image,
        block_bboxes_result: BlockBBoxesResult,
        config: BlockDrawConfig | None = None,
    ) -> Image.Image:
        """Draw surface, content, and all block bounding boxes onto ``image``.

        Parameters
        ----------
        image
            Source image to annotate.
        block_bboxes_result
            Block bounding boxes from ``DocumentRenderPipeline.get_block_bounding_boxes()``.
        config
            Drawing configuration; ``None`` uses defaults.

        Returns
        -------
        Image.Image
            New RGBA image with all block bounding box overlays composited on top.
        """
        if config is None:
            config = BlockDrawConfig()

        base = image.convert("RGBA")
        overlay = Image.new("RGBA", base.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)

        for name, quad, color in self._entries(block_bboxes_result, config):
            self._draw_entry(draw, name, quad, color, config)

        return Image.alpha_composite(base, overlay)

    def draw_per_block(
        self,
        image: Image.Image,
        block_bboxes_result: BlockBBoxesResult,
        config: BlockDrawConfig | None = None,
    ) -> list[tuple[str, Image.Image]]:
        """Return a separate annotated image for each block bbox entry.

        Produces one image for the surface bbox, one for the content bbox,
        and one per named block.

        Parameters
        ----------
        image
            Source image to annotate.
        block_bboxes_result
            Block bounding boxes from ``DocumentRenderPipeline.get_block_bounding_boxes()``.
        config
            Drawing configuration; ``None`` uses defaults.

        Returns
        -------
        list[tuple[str, Image.Image]]
            ``(name, image)`` pairs: ``"surface"``, ``"content"``, then each block's name.
        """
        if config is None:
            config = BlockDrawConfig()

        base = image.convert("RGBA")
        results: list[tuple[str, Image.Image]] = []

        for name, quad, color in self._entries(block_bboxes_result, config):
            overlay = Image.new("RGBA", base.size, (0, 0, 0, 0))
            draw = ImageDraw.Draw(overlay)
            self._draw_entry(draw, name, quad, color, config)
            results.append((name, Image.alpha_composite(base.copy(), overlay)))

        return results

    @staticmethod
    def _entries(
        block_bboxes_result: BlockBBoxesResult,
        config: BlockDrawConfig,
    ) -> list[tuple[str, Quadrilateral, tuple[int, int, int, int]]]:
        return [
            ("surface", block_bboxes_result.surface_bbox, config.surface_color),
            ("content", block_bboxes_result.content_bbox, config.content_color),
            *(
                (block_bbox.name or f"block_{i}", block_bbox.bbox, config.block_color)
                for i, block_bbox in enumerate(block_bboxes_result.block_bboxes)
            ),
        ]

    def _draw_entry(
        self,
        draw: ImageDraw.ImageDraw,
        name: str,
        quad: Quadrilateral,
        color: tuple[int, int, int, int],
        config: BlockDrawConfig,
    ) -> None:
        pts = [quad.top_left, quad.top_right, quad.bottom_right, quad.bottom_left]
        r, g, b, _ = color
        draw.polygon(pts, fill=(r, g, b, config.fill_alpha), outline=color, width=config.line_width)
        if config.draw_labels:
            x, y = quad.top_left
            text_bbox = draw.textbbox((x, y), name)
            draw.rectangle(text_bbox, fill=(0, 0, 0, 160))
            draw.text((x, y), name, fill=color)


class SVGBlockBoundingBoxDrawer:
    """Draw block bounding boxes into an SVG document as polygon overlays."""

    _NS = "http://www.w3.org/2000/svg"

    def draw(
        self,
        svg: bytes,
        block_bboxes_result: BlockBBoxesResult,
        config: BlockDrawConfig | None = None,
    ) -> bytes:
        """Append block bounding box polygons to ``svg`` and return the result.

        Parameters
        ----------
        svg
            Source SVG bytes to annotate.
        block_bboxes_result
            Block bounding boxes from ``DocumentRenderPipeline.get_block_bounding_boxes()``.
        config
            Drawing configuration; ``None`` uses defaults.

        Returns
        -------
        bytes
            SVG bytes with block bounding box polygon elements appended.
        """
        if config is None:
            config = BlockDrawConfig()

        root = etree.fromstring(svg)
        group = etree.SubElement(root, f"{{{self._NS}}}g")

        for name, quad, color in self._entries(block_bboxes_result, config):
            self._add_quadrilateral(group, quad, color, config)
            if config.draw_labels:
                self._add_label(group, quad, name, color)

        return bytes(etree.tostring(root))

    def draw_per_block(
        self,
        svg: bytes,
        block_bboxes_result: BlockBBoxesResult,
        config: BlockDrawConfig | None = None,
    ) -> list[tuple[str, bytes]]:
        """Return a separate annotated SVG for each block bbox entry.

        Parameters
        ----------
        svg
            Source SVG bytes to annotate.
        block_bboxes_result
            Block bounding boxes from ``DocumentRenderPipeline.get_block_bounding_boxes()``.
        config
            Drawing configuration; ``None`` uses defaults.

        Returns
        -------
        list[tuple[str, bytes]]
            ``(name, svg_bytes)`` pairs: ``"surface"``, ``"content"``, then each block's name.
        """
        if config is None:
            config = BlockDrawConfig()

        results: list[tuple[str, bytes]] = []

        for name, quad, color in self._entries(block_bboxes_result, config):
            root = etree.fromstring(svg)
            group = etree.SubElement(root, f"{{{self._NS}}}g")
            self._add_quadrilateral(group, quad, color, config)
            if config.draw_labels:
                self._add_label(group, quad, name, color)
            results.append((name, bytes(etree.tostring(root))))

        return results

    @staticmethod
    def _entries(
        block_bboxes_result: BlockBBoxesResult,
        config: BlockDrawConfig,
    ) -> list[tuple[str, Quadrilateral, tuple[int, int, int, int]]]:
        return [
            ("surface", block_bboxes_result.surface_bbox, config.surface_color),
            ("content", block_bboxes_result.content_bbox, config.content_color),
            *(
                (block_bbox.name or f"block_{i}", block_bbox.bbox, config.block_color)
                for i, block_bbox in enumerate(block_bboxes_result.block_bboxes)
            ),
        ]

    def _add_quadrilateral(
        self,
        parent: etree._Element,
        quad: Quadrilateral,
        color: tuple[int, int, int, int],
        config: BlockDrawConfig,
    ) -> None:
        r, g, b, a = color
        pts = " ".join(f"{x},{y}" for x, y in [quad.top_left, quad.top_right, quad.bottom_right, quad.bottom_left])
        el = etree.SubElement(parent, f"{{{self._NS}}}polygon")
        el.set("points", pts)
        el.set("fill", f"rgb({r},{g},{b})")
        el.set("fill-opacity", f"{config.fill_alpha / 255:.3f}")
        el.set("stroke", f"rgb({r},{g},{b})")
        el.set("stroke-opacity", f"{a / 255:.3f}")
        el.set("stroke-width", str(config.line_width))

    def _add_label(
        self,
        parent: etree._Element,
        quad: Quadrilateral,
        name: str,
        color: tuple[int, int, int, int],
    ) -> None:
        r, g, b, a = color
        x, y = quad.top_left
        el = etree.SubElement(parent, f"{{{self._NS}}}text")
        el.set("x", str(x))
        el.set("y", str(y))
        el.set("fill", f"rgb({r},{g},{b})")
        el.set("fill-opacity", f"{a / 255:.3f}")
        el.set("font-size", "10")
        el.text = name
