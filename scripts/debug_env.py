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

import sys
from importlib.metadata import PackageNotFoundError, version


def _print_section(title: str) -> None:
    print(f"\n{'=' * 50}")
    print(f"  {title}")
    print("=" * 50)


def _info(label: str, value: object) -> None:
    print(f"  {label:<35}: {value}")


def print_python_info() -> None:
    _print_section("Python")
    _info("version", sys.version.split("\n")[0])
    _info("executable", sys.executable)
    _info("prefix", sys.prefix)
    _info("platform", sys.platform)
    _info("implementation", sys.implementation.name)
    _info("byteorder", sys.byteorder)


def print_pygobject() -> None:
    _print_section("PyGObject")
    try:
        import gi  # noqa: PLC0415

        _info("PyGObject version", gi.__version__)
        _info("PyGObject file", gi.__file__)
    except ImportError as e:
        _info("PyGObject", f"UNAVAILABLE - {e}")


def print_cairo_info() -> None:
    _print_section("Cairo (pycairo)")
    try:
        import cairo  # noqa: PLC0415

        _info("pycairo version", cairo.version)
        _info("pycairo file", cairo.__file__)
        _info("C cairo library", cairo.cairo_version_string())
        _info("C header files dir", cairo.get_include())
        features = [
            "HAS_ATSUI_FONT",
            "HAS_FT_FONT",
            "HAS_GLITZ_SURFACE",
            "HAS_IMAGE_SURFACE",
            "HAS_PDF_SURFACE",
            "HAS_PNG_FUNCTIONS",
            "HAS_PS_SURFACE",
            "HAS_RECORDING_SURFACE",
            "HAS_SVG_SURFACE",
            "HAS_USER_FONT",
            "HAS_QUARTZ_SURFACE",
            "HAS_WIN32_FONT",
            "HAS_WIN32_SURFACE",
            "HAS_XCB_SURFACE",
            "HAS_XLIB_SURFACE",
            "HAS_MIME_SURFACE",
            "HAS_SCRIPT_SURFACE",
            "HAS_TEE_SURFACE",
            "HAS_DWRITE_FONT",
        ]
        for feat in features:
            _info(feat, getattr(cairo, feat, "N/A"))
    except ImportError as e:
        _info("cairo", f"UNAVAILABLE - {e}")


def print_pango_info() -> None:
    _print_section("Pango / PangoCairo")
    try:
        import gi  # noqa: PLC0415

        gi.require_version("Pango", "1.0")
        gi.require_version("PangoCairo", "1.0")
        from gi.repository import Pango, PangoCairo  # noqa: PLC0415

        _info("Pango version string", Pango.version_string())
        _info("Pango module", Pango.__name__)
        _info("PangoCairo module", PangoCairo.__name__)
    except Exception as e:  # noqa: BLE001
        _info("Pango", f"UNAVAILABLE - {e}")


def print_smoke_tests() -> None:
    _print_section("Smoke Tests")

    # Cairo: draw a rectangle on an image surface
    try:
        import cairo  # noqa: PLC0415

        surface = cairo.ImageSurface(cairo.Format.RGB24, 100, 100)
        ctx = cairo.Context(surface)
        ctx.set_source_rgb(1, 0, 0)
        ctx.rectangle(10, 10, 80, 80)
        ctx.fill()
        _info("Cairo", "SUCCESS")
    except Exception as e:  # noqa: BLE001
        _info("Cairo", f"FAILED - {e}")

    # Pango: create a layout and set text
    try:
        import gi  # noqa: PLC0415

        gi.require_version("Pango", "1.0")
        gi.require_version("PangoCairo", "1.0")
        from gi.repository import Pango, PangoCairo  # noqa: PLC0415

        font_map = PangoCairo.font_map_get_default()
        pango_ctx = font_map.create_context()
        layout = Pango.Layout(pango_ctx)  # type: ignore[call-arg]
        layout.set_text("Hello")
        _info("Pango (layout)", f"SUCCESS — char count: {layout.get_character_count()}")
    except Exception as e:  # noqa: BLE001
        _info("Pango (layout)", f"FAILED - {e}")

    # PangoCairo: render a layout onto a Cairo surface
    try:
        import cairo  # noqa: PLC0415
        import gi  # noqa: PLC0415

        gi.require_version("Pango", "1.0")
        gi.require_version("PangoCairo", "1.0")
        from gi.repository import Pango, PangoCairo  # noqa: PLC0415

        surface = cairo.ImageSurface(cairo.Format.RGB24, 200, 50)
        ctx = cairo.Context(surface)
        layout = PangoCairo.create_layout(ctx)
        layout.set_text("Hello")
        font_desc = Pango.FontDescription.from_string("Sans 12")
        layout.set_font_description(font_desc)
        PangoCairo.show_layout(ctx, layout)
        _info("PangoCairo (render)", "SUCCESS")
    except Exception as e:  # noqa: BLE001
        _info("PangoCairo (render)", f"FAILED - {e}")


def print_dpi_info() -> None:
    _print_section("DPI / Resolution")
    try:
        import gi  # noqa: PLC0415

        gi.require_version("Pango", "1.0")
        gi.require_version("PangoCairo", "1.0")
        from gi.repository import Pango, PangoCairo  # noqa: PLC0415

        # Font-map DPI: the process-wide default
        font_map = PangoCairo.font_map_get_default()
        font_map_dpi = font_map.get_resolution()  # type: ignore[attr-defined]
        _info("Font map DPI", font_map_dpi)

        # Context DPI: pango_cairo_context_set_resolution default
        # A value <= 0 means "inherit from font map" (Pango docs, since 1.10)
        ctx = font_map.create_context()
        context_dpi = PangoCairo.context_get_resolution(ctx)
        _info("Context DPI (raw, -1 = inherit)", context_dpi)
        effective_dpi = font_map_dpi if context_dpi <= 0 else context_dpi
        _info("Effective DPI", effective_dpi)

        _info("1 pt in device pixels", f"{effective_dpi / 72:.4f} px")
        _info("Pango SCALE", Pango.SCALE)
        _info("1 Pango unit in points", f"{1 / Pango.SCALE:.6f} pt")
        _info("1 Pango unit in pixels", f"{effective_dpi / 72 / Pango.SCALE:.6f} px")
        _info("Example: 10 pt → px (Pango docs)", f"{10 * effective_dpi / 72:.2f} px")
    except Exception as e:  # noqa: BLE001
        _info("DPI", f"UNAVAILABLE - {e}")


def print_tenderness_info() -> None:
    _print_section("tenderness package")
    try:
        _info("tenderness version", version("tenderness"))
        mod = __import__("tenderness")
        _info("tenderness file", mod.__file__)
    except (ImportError, PackageNotFoundError):
        _info("tenderness", "NOT INSTALLED")


def print_tenderness_dependencies() -> None:
    _print_section("Other `tenderness` dependencies")
    packages = ["numpy", "matplotlib", "lxml", "requests", "tqdm"]
    for pkg in packages:
        try:
            _info(pkg, version(pkg))
        except PackageNotFoundError:
            _info(pkg, "NOT INSTALLED")


def print_other_packages() -> None:
    _print_section("Other packages")
    packages = ["Pillow", "fonttools", "torch"]
    for pkg in packages:
        try:
            _info(pkg, version(pkg))
        except PackageNotFoundError:
            _info(pkg, "NOT INSTALLED")


def main() -> None:
    print_python_info()
    print_pygobject()
    print_cairo_info()
    print_pango_info()
    print_smoke_tests()
    print_dpi_info()
    print_tenderness_info()
    print_tenderness_dependencies()
    print_other_packages()
    print()


if __name__ == "__main__":
    main()
