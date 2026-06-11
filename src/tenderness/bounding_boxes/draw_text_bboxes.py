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

"""Utilities for drawing text bounding boxes (for debugging and visualization)."""

from __future__ import annotations

from dataclasses import dataclass, field

from lxml import etree
from PIL import Image, ImageDraw

from tenderness.bounding_boxes.bounding_boxes_schema import (
    BoundingBoxType,
    CharBBox,
    ClusterBBox,
    LayoutBBox,
    LineBBox,
    Quadrilateral,
    RunBBox,
    TextBoundingBoxes,
)


@dataclass
class TextDrawConfig:
    """Drawing configuration for text bounding box overlays.

    Attributes
    ----------
    char_color
        RGBA color for character bounding boxes.
    cluster_color
        RGBA color for cluster bounding boxes.
    run_color
        RGBA color for run bounding boxes.
    line_color
        RGBA color for line bounding boxes.
    layout_color
        RGBA color for layout bounding boxes.
    fill_alpha
        Alpha for the semi-transparent fill (0 = transparent, 255 = solid).
    draw_ink_bbox
        If ``True``, draw ink bounding boxes alongside logical ones.
    draw_labels
        If ``True``, annotate boxes with text content.
    line_width
        Stroke width in pixels.
    levels
        Granularity levels to draw.
    """

    char_color: tuple[int, int, int, int] = (255, 0, 0, 220)  # red
    cluster_color: tuple[int, int, int, int] = (255, 165, 0, 220)  # orange
    run_color: tuple[int, int, int, int] = (0, 200, 0, 220)  #  green
    line_color: tuple[int, int, int, int] = (0, 0, 255, 220)  # blue
    layout_color: tuple[int, int, int, int] = (128, 0, 128, 220)  # purple

    fill_alpha: int = 45  # alpha for the semi-transparent fill (0 = no fill, 255 = solid).

    draw_ink_bbox: bool = True  # draw ink_bbox in addition to logical_bbox
    draw_labels: bool = True  # annotate boxes with their text content
    line_width: int = 1
    levels: set[BoundingBoxType] = field(default_factory=lambda: set(BoundingBoxType))


@dataclass(frozen=True)
class _LevelMeta:
    boxes_attr: str
    color_attr: str
    has_ink: bool


# Maps each level to: (collection attribute, config color attribute, has_ink)
_LEVEL_META: dict[BoundingBoxType, _LevelMeta] = {
    BoundingBoxType.LAYOUT: _LevelMeta(boxes_attr="layout_bbox", color_attr="layout_color", has_ink=True),
    BoundingBoxType.LINE: _LevelMeta(boxes_attr="line_bboxes", color_attr="line_color", has_ink=True),
    BoundingBoxType.RUN: _LevelMeta(boxes_attr="run_bboxes", color_attr="run_color", has_ink=True),
    BoundingBoxType.CLUSTER: _LevelMeta(boxes_attr="cluster_bboxes", color_attr="cluster_color", has_ink=True),
    BoundingBoxType.CHAR: _LevelMeta(boxes_attr="char_bboxes", color_attr="char_color", has_ink=False),
}


class ImageTextBoundingBoxDrawer:
    """Draw text bounding boxes onto a PIL image as semi-transparent overlays."""

    def draw(
        self, image: Image.Image, text_bounding_boxes: TextBoundingBoxes, config: TextDrawConfig | None = None
    ) -> Image.Image:
        """Composite all active levels onto ``image`` and return the result.

        Parameters
        ----------
        image
            Source image to annotate.
        text_bounding_boxes
            Bounding boxes to draw.
        config
            Drawing configuration; ``None`` uses defaults.

        Returns
        -------
        Image.Image
            New RGBA image with bounding box overlays composited on top.
        """
        if config is None:
            config = TextDrawConfig()

        base = image.convert("RGBA")
        for level in _LEVEL_META:
            if level not in config.levels:
                continue
            base = self._composite_level(base, text_bounding_boxes, level, config)
        return base

    def draw_per_level(
        self, image: Image.Image, text_bounding_boxes: TextBoundingBoxes, config: TextDrawConfig | None = None
    ) -> list[tuple[BoundingBoxType, Image.Image]]:
        """Return a separate annotated image for each active granularity level.

        Parameters
        ----------
        image
            Source image to annotate.
        text_bounding_boxes
            Bounding boxes to draw.
        config
            Drawing configuration; ``None`` uses defaults.

        Returns
        -------
        list[tuple[BoundingBoxType, Image.Image]]
            One ``(level, image)`` pair per active level, in ``_LEVEL_META`` order.
        """
        if config is None:
            config = TextDrawConfig()

        base = image.convert("RGBA")
        results: list[tuple[BoundingBoxType, Image.Image]] = []

        for level in _LEVEL_META:
            if level not in config.levels:
                continue
            annotated = self._composite_level(base.copy(), text_bounding_boxes, level, config)
            results.append((level, annotated))

        return results

    def _composite_level(
        self, base: Image.Image, text_bounding_boxes: TextBoundingBoxes, level: BoundingBoxType, config: TextDrawConfig
    ) -> Image.Image:
        meta = _LEVEL_META[level]
        color: tuple[int, int, int, int] = getattr(config, meta.color_attr)

        raw = getattr(text_bounding_boxes, meta.boxes_attr)
        boxes = [raw] if level == BoundingBoxType.LAYOUT and raw is not None else raw
        if not boxes:
            return base

        # separate overlay so fill alpha doesn't stack with the outline alpha.
        overlay = Image.new("RGBA", base.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)

        for box in boxes:
            self._draw_box(draw, box.logical_bbox, color, config)
            if config.draw_ink_bbox and meta.has_ink and hasattr(box, "ink_bbox"):
                self._draw_box(draw, box.ink_bbox, self._darken(color), config)
            if config.draw_labels:
                label = self._label(box)
                if label:
                    self._draw_label(draw, box.logical_bbox, label, color)

        return Image.alpha_composite(base, overlay)

    def _draw_box(
        self,
        draw: ImageDraw.ImageDraw,
        quadrilateral: Quadrilateral,
        color: tuple[int, int, int, int],
        config: TextDrawConfig,
    ) -> None:
        pts = [
            quadrilateral.top_left,
            quadrilateral.top_right,
            quadrilateral.bottom_right,
            quadrilateral.bottom_left,
        ]
        r, g, b, _ = color
        fill = (r, g, b, config.fill_alpha)
        draw.polygon(pts, fill=fill, outline=color, width=config.line_width)

    def _draw_label(
        self, draw: ImageDraw.ImageDraw, quadrilateral: Quadrilateral, label: str, color: tuple[int, int, int, int]
    ) -> None:
        x, y = quadrilateral.top_left
        # dark background patch for legibility — PIL built-in default font, no file needed.
        text_bbox = draw.textbbox((x, y), label)
        draw.rectangle(text_bbox, fill=(0, 0, 0, 160))
        draw.text((x, y), label, fill=color)

    @staticmethod
    def _label(box: CharBBox | ClusterBBox | RunBBox | LineBBox | LayoutBBox) -> str | None:
        return box.text

    @staticmethod
    def _darken(color: tuple[int, int, int, int], factor: float = 0.6) -> tuple[int, int, int, int]:
        r, g, b, a = color
        return (int(r * factor), int(g * factor), int(b * factor), a)


class SVGTextBoundingBoxDrawer:
    """Draw text bounding boxes into an SVG document as polygon overlays."""

    _NS = "http://www.w3.org/2000/svg"

    def draw(
        self,
        svg: bytes,
        text_bounding_boxes: TextBoundingBoxes,
        config: TextDrawConfig | None = None,
    ) -> bytes:
        """Append text bounding box polygons to ``svg`` and return the result.

        Parameters
        ----------
        svg
            Source SVG bytes to annotate.
        text_bounding_boxes
            Bounding boxes to draw.
        config
            Drawing configuration; ``None`` uses defaults.

        Returns
        -------
        bytes
            SVG bytes with bounding box polygon elements appended.
        """
        if config is None:
            config = TextDrawConfig()

        root = etree.fromstring(svg)

        for level in _LEVEL_META:
            if level not in config.levels:
                continue
            self._draw_level(root, text_bounding_boxes, level, config)

        return bytes(etree.tostring(root))

    def _draw_level(
        self,
        root: etree._Element,
        text_bounding_boxes: TextBoundingBoxes,
        level: BoundingBoxType,
        config: TextDrawConfig,
    ) -> None:
        meta = _LEVEL_META[level]
        color: tuple[int, int, int, int] = getattr(config, meta.color_attr)

        raw = getattr(text_bounding_boxes, meta.boxes_attr)
        boxes = [raw] if level == BoundingBoxType.LAYOUT and raw is not None else raw
        if not boxes:
            return

        group = etree.SubElement(root, f"{{{self._NS}}}g")
        for box in boxes:
            self._add_quadrilateral(group, box.logical_bbox, color, config)
            if config.draw_ink_bbox and meta.has_ink and hasattr(box, "ink_bbox"):
                self._add_quadrilateral(group, box.ink_bbox, self._darken(color), config)
            if config.draw_labels:
                label = self._label(box)
                if label:
                    self._add_label(group, box.logical_bbox, label, color)

    def _add_quadrilateral(
        self,
        parent: etree._Element,
        quadrilateral: Quadrilateral,
        color: tuple[int, int, int, int],
        config: TextDrawConfig,
    ) -> None:
        r, g, b, a = color
        pts = " ".join(
            f"{x},{y}"
            for x, y in [
                quadrilateral.top_left,
                quadrilateral.top_right,
                quadrilateral.bottom_right,
                quadrilateral.bottom_left,
            ]
        )
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
        quadrilateral: Quadrilateral,
        label: str,
        color: tuple[int, int, int, int],
    ) -> None:
        r, g, b, a = color
        x, y = quadrilateral.top_left
        el = etree.SubElement(parent, f"{{{self._NS}}}text")
        el.set("x", str(x))
        el.set("y", str(y))
        el.set("fill", f"rgb({r},{g},{b})")
        el.set("fill-opacity", f"{a / 255:.3f}")
        el.set("font-size", "10")
        el.text = label

    @staticmethod
    def _label(box: CharBBox | ClusterBBox | RunBBox | LineBBox | LayoutBBox) -> str | None:
        return box.text

    @staticmethod
    def _darken(color: tuple[int, int, int, int], factor: float = 0.6) -> tuple[int, int, int, int]:
        r, g, b, a = color
        return (int(r * factor), int(g * factor), int(b * factor), a)
