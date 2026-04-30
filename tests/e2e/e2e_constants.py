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

from tenderness.cairo_backend.color_patterns import ColorStop, LinearGradientColorSpec, SolidColorSpec
from tenderness.cairo_backend.surface_config_manager import SurfaceConfigManager
from tenderness.colors.color_selector import ColorSelector

_DEFAULT_COLOR_SELECTOR = ColorSelector()


SOLID_WHITE_COLOR = SolidColorSpec(
    color=_DEFAULT_COLOR_SELECTOR.by_names(color_names=["white"])[0],
)

SOLID_BLACK_COLOR = SolidColorSpec(
    color=_DEFAULT_COLOR_SELECTOR.by_names(color_names=["black"])[0],
)

SOLID_RED_COLOR = SolidColorSpec(
    color=_DEFAULT_COLOR_SELECTOR.by_names(color_names=["red"])[0],
)

SOLID_LAVENDER_COLOR = SolidColorSpec(
    color=_DEFAULT_COLOR_SELECTOR.by_names(color_names=["lavender"])[0],
)
SOLID_LIGHTCYAN_COLOR = SolidColorSpec(
    color=_DEFAULT_COLOR_SELECTOR.by_names(color_names=["lightcyan"])[0],
)

SOLID_DARKMAGNETA_COLOR = SolidColorSpec(
    color=_DEFAULT_COLOR_SELECTOR.by_names(color_names=["darkmagenta"])[0],
)

LINEAR_GRADIENT_BLACK_TO_WHITE_COLOR = LinearGradientColorSpec(
    x0=0,
    y0=0,
    x1=1000,
    y1=1000,
    stops=(
        ColorStop(offset=0.0, color=_DEFAULT_COLOR_SELECTOR.by_names(color_names=["green"])[0]),
        ColorStop(offset=1.0, color=_DEFAULT_COLOR_SELECTOR.by_names(color_names=["white"])[0]),
    ),
)


# --------------------------
# FONT NAMES
# --------------------------
HONK_FONT_NAME = "Honk"
NOTO_SANS_FONT_NAME = "Noto Sans"
NOTO_SANS_CUNEIFORM_FONT_NAME = "Noto Sans Cuneiform"
NOTO_COLOR_EMOJI_FONT_NAME = "Noto Color Emoji"
LONG_CANG_FONT_NAME = "Long Cang"
MARHEY_FONT_NAME = "Marhey"
RUBIK_GLITCH_FONT_NAME = "Rubik Glitch"

# --------------------------
# SURFACE PARAMETERS
# --------------------------
_DEFAULT_SURFACE_CONFIG_MANAGER = SurfaceConfigManager()

_WIDTH_SURFACE = 1280
_HEIGHT_SURFACE = 720

_DEFAULT_PLACEHOLDER_SURFACE_CONFIG = _DEFAULT_SURFACE_CONFIG_MANAGER.create_image_surface_config(
    width=50,
    height=50,
)

_DEFAULT_IMG_SURFACE_CONFIG = _DEFAULT_SURFACE_CONFIG_MANAGER.create_image_surface_config(
    width=_WIDTH_SURFACE,
    height=_HEIGHT_SURFACE,
)


_DEFAULT_SVG_SURFACE_CONFIG = _DEFAULT_SURFACE_CONFIG_MANAGER.create_svg_surface_config(
    width=_WIDTH_SURFACE,
    height=_HEIGHT_SURFACE,
)

_DEFAULT_PDF_SURFACE_CONFIG = _DEFAULT_SURFACE_CONFIG_MANAGER.create_pdf_surface_config(
    width=_WIDTH_SURFACE,
    height=_HEIGHT_SURFACE,
)
