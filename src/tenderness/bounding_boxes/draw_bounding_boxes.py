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

from dataclasses import dataclass, field

from lxml import etree
from PIL import Image, ImageDraw

from tenderness.bounding_boxes.bounding_boxes_schema import (
    BoundingBoxType,
    CharBBox,
    ClusterBBox,
    LayoutBBox,
    LayoutBBoxCollection,
    LineBBox,
    RunBBox,
    Tetragon,
)


@dataclass
class DrawConfig:  # noqa: D101 TODO: docstring
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


def _label(box: CharBBox | ClusterBBox | RunBBox | LineBBox | LayoutBBox) -> str | None:
    if isinstance(box, CharBBox):
        return box.char
    if isinstance(box, (ClusterBBox, RunBBox, LineBBox, LayoutBBox)):
        return box.text
    return None


def _darken(color: tuple[int, int, int, int], factor: float = 0.6) -> tuple[int, int, int, int]:
    r, g, b, a = color
    return (int(r * factor), int(g * factor), int(b * factor), a)


# Maps each level to: (collection attribute, config color attribute, has_ink)
_LEVEL_META: dict[BoundingBoxType, _LevelMeta] = {
    BoundingBoxType.LAYOUT: _LevelMeta(boxes_attr="layout_box", color_attr="layout_color", has_ink=True),
    BoundingBoxType.LINE: _LevelMeta(boxes_attr="line_boxes", color_attr="line_color", has_ink=True),
    BoundingBoxType.RUN: _LevelMeta(boxes_attr="run_boxes", color_attr="run_color", has_ink=True),
    BoundingBoxType.CLUSTER: _LevelMeta(boxes_attr="cluster_boxes", color_attr="cluster_color", has_ink=True),
    BoundingBoxType.CHAR: _LevelMeta(boxes_attr="char_boxes", color_attr="char_color", has_ink=False),
}


class ImageBoundingBoxDrawer:  # noqa: D101 TODO: docstring
    def draw(  # noqa: D102 TODO: docstring
        self, image: Image.Image, collection: LayoutBBoxCollection, config: DrawConfig | None = None
    ) -> Image.Image:
        if config is None:
            config = DrawConfig()

        base = image.convert("RGBA")
        for level in _LEVEL_META:
            if level not in config.levels:
                continue
            base = self._composite_level(base, collection, level, config)
        return base

    def draw_per_level(  # noqa: D102 TODO: docstring
        self, image: Image.Image, collection: LayoutBBoxCollection, config: DrawConfig | None = None
    ) -> list[tuple[BoundingBoxType, Image.Image]]:
        if config is None:
            config = DrawConfig()

        base = image.convert("RGBA")
        results: list[tuple[BoundingBoxType, Image.Image]] = []

        for level in _LEVEL_META:
            if level not in config.levels:
                continue
            annotated = self._composite_level(base.copy(), collection, level, config)
            results.append((level, annotated))

        return results

    def _composite_level(
        self, base: Image.Image, collection: LayoutBBoxCollection, level: BoundingBoxType, config: DrawConfig
    ) -> Image.Image:
        meta = _LEVEL_META[level]
        color: tuple[int, int, int, int] = getattr(config, meta.color_attr)

        raw = getattr(collection, meta.boxes_attr)
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
        self, draw: ImageDraw.ImageDraw, tetragon: Tetragon, color: tuple[int, int, int, int], config: DrawConfig
    ) -> None:
        pts = [
            tetragon.top_left,
            tetragon.top_right,
            tetragon.bottom_right,
            tetragon.bottom_left,
        ]
        r, g, b, _ = color
        fill = (r, g, b, config.fill_alpha)
        draw.polygon(pts, fill=fill, outline=color, width=config.line_width)

    def _draw_label(
        self, draw: ImageDraw.ImageDraw, tetragon: Tetragon, label: str, color: tuple[int, int, int, int]
    ) -> None:
        x, y = tetragon.top_left
        # dark background patch for legibility — PIL built-in default font, no file needed.
        text_bbox = draw.textbbox((x, y), label)
        draw.rectangle(text_bbox, fill=(0, 0, 0, 160))
        draw.text((x, y), label, fill=color)

    @staticmethod
    def _label(box: CharBBox | ClusterBBox | RunBBox | LineBBox | LayoutBBox) -> str | None:
        return _label(box)

    @staticmethod
    def _darken(color: tuple[int, int, int, int], factor: float = 0.6) -> tuple[int, int, int, int]:
        return _darken(color, factor)


class SVGBoundingBoxDrawer:  # noqa: D101 TODO: docstring
    _NS = "http://www.w3.org/2000/svg"

    def draw(  # noqa: D102 TODO: docstring
        self,
        svg: bytes,
        collection: LayoutBBoxCollection,
        config: DrawConfig | None = None,
    ) -> bytes:
        if config is None:
            config = DrawConfig()

        root = etree.fromstring(svg)

        for level in _LEVEL_META:
            if level not in config.levels:
                continue
            self._draw_level(root, collection, level, config)

        return bytes(etree.tostring(root))

    def _draw_level(
        self,
        root: etree._Element,
        collection: LayoutBBoxCollection,
        level: BoundingBoxType,
        config: DrawConfig,
    ) -> None:
        meta = _LEVEL_META[level]
        color: tuple[int, int, int, int] = getattr(config, meta.color_attr)

        raw = getattr(collection, meta.boxes_attr)
        boxes = [raw] if level == BoundingBoxType.LAYOUT and raw is not None else raw
        if not boxes:
            return

        group = etree.SubElement(root, f"{{{self._NS}}}g")
        for box in boxes:
            self._add_tetragon(group, box.logical_bbox, color, config)
            if config.draw_ink_bbox and meta.has_ink and hasattr(box, "ink_bbox"):
                self._add_tetragon(group, box.ink_bbox, _darken(color), config)
            if config.draw_labels:
                label = _label(box)
                if label:
                    self._add_label(group, box.logical_bbox, label, color)

    def _add_tetragon(
        self,
        parent: etree._Element,
        tetragon: Tetragon,
        color: tuple[int, int, int, int],
        config: DrawConfig,
    ) -> None:
        r, g, b, a = color
        pts = " ".join(
            f"{x},{y}" for x, y in [tetragon.top_left, tetragon.top_right, tetragon.bottom_right, tetragon.bottom_left]
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
        tetragon: Tetragon,
        label: str,
        color: tuple[int, int, int, int],
    ) -> None:
        r, g, b, a = color
        x, y = tetragon.top_left
        el = etree.SubElement(parent, f"{{{self._NS}}}text")
        el.set("x", str(x))
        el.set("y", str(y))
        el.set("fill", f"rgb({r},{g},{b})")
        el.set("fill-opacity", f"{a / 255:.3f}")
        el.set("font-size", "10")
        el.text = label
