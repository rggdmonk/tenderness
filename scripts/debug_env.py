from __future__ import annotations

import sys
from importlib.metadata import PackageNotFoundError, version

import cairo
import gi

gi.require_version("Pango", "1.0")
gi.require_version("PangoCairo", "1.0")
from gi.repository import Pango, PangoCairo  # noqa: E402


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


def print_cairo_info() -> None:
    _print_section("Cairo (pycairo)")
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


def print_pango_info() -> None:
    _print_section("Pango / PangoCairo")
    _info("Pango version string", Pango.version_string())
    _info("Pango version", Pango.__name__)
    _info("PangoCairo module", PangoCairo.__name__)


def print_pygobject() -> None:
    _print_section("PyGObject")
    _info("PyGObject version", gi.__version__)
    _info("PyGObject file", gi.__file__)


def print_other_packages() -> None:
    _print_section("Other packages")
    packages = [
        "Pillow",
        "fonttools",
        "torch",
    ]
    for pkg in packages:
        try:
            _info(pkg, version(pkg))
        except PackageNotFoundError:
            _info(pkg, "NOT INSTALLED")


def print_simple_test() -> None:
    _print_section("Simple Cairo Test")
    try:
        surface = cairo.ImageSurface(cairo.Format.RGB24, 100, 100)
        ctx = cairo.Context(surface)
        ctx.set_source_rgb(1, 0, 0)
        ctx.rectangle(10, 10, 80, 80)
        ctx.fill()
        _info("Cairo test", "SUCCESS")
    except Exception as e:  # noqa: BLE001
        _info("Cairo test", f"FAILED - {e}")


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
    packages = [
        "numpy",
        "matplotlib",
        "lxml",
        "requests",
        "tqdm",
    ]
    for pkg in packages:
        try:
            _info(pkg, version(pkg))
        except PackageNotFoundError:
            _info(pkg, "NOT INSTALLED")


def main() -> None:
    # System
    print_python_info()

    # Core dependencies
    print_pygobject()
    print_cairo_info()
    print_pango_info()

    # tenderness
    print_tenderness_info()
    print_tenderness_dependencies()

    # Optional / extra packages
    print_other_packages()

    # Tests
    print_simple_test()
    print()


if __name__ == "__main__":
    main()
