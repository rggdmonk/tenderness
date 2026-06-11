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

# ruff: noqa: PLC0415
from __future__ import annotations

_EXPECTED_BOUNDING_BOXES: frozenset[str] = frozenset(
    {
        "BoundingBox",
        "BoundingBoxType",
        "BoundingBoxWithInk",
        "CharBBox",
        "ClusterBBox",
        "ImageTextBoundingBoxDrawer",
        "LayoutBBox",
        "LineBBox",
        "Quadrilateral",
        "RunBBox",
        "SVGTextBoundingBoxDrawer",
        "TextDrawConfig",
        "TextBoundingBoxExtractor",
        "TextBoundingBoxes",
    }
)

_EXPECTED_CAIRO_BACKEND: frozenset[str] = frozenset(
    {
        "AntialiasStr",
        "BackgroundSelector",
        "CairoContextTransformPipeline",
        "CairoEnumCoerce",
        "CairoEnumMap",
        "CairoMatrixTransformer",
        "ChannelOrder",
        "ColorModeStr",
        "ColorPattern",
        "ColorStop",
        "FlipHorizontalParameters",
        "FlipVerticalParameters",
        "FontOptionsInterface",
        "FontOptionsInterfaceParameters",
        "HintMetricsStr",
        "HintStyleStr",
        "ImagePatternSpec",
        "ImageSurfaceConfig",
        "LinearGradientColorSpec",
        "MatrixTransformType",
        "OperatorStr",
        "PDFSurfaceConfig",
        "PDFVersionStr",
        "PatternColorSpec",
        "PixelDType",
        "PixelFormat",
        "PixelFormatInfo",
        "PixelOrder",
        "RadialGradientColorSpec",
        "RotateAroundPointParameters",
        "RotateParameters",
        "SVGSurfaceConfig",
        "SVGUnitStr",
        "SVGVersionStr",
        "ScaleParameters",
        "SkewXParameters",
        "SkewYParameters",
        "SolidColorSpec",
        "SubpixelOrderStr",
        "SurfaceConfigManager",
        "SurfaceCreator",
        "SurfacePatternSpec",
        "SurfaceRect",
        "SurfaceType",
        "TextColorSelector",
        "TransformDataclassParameter",
        "TransformDictParameter",
        "TransformParameter",
        "TranslateParameters",
    }
)

_EXPECTED_COLORS: frozenset[str] = frozenset(
    {
        "Color",
        "ColorGroup",
        "ColorGroupName",
        "ColorName",
        "ColorRegistry",
        "ColorSelector",
        "HexColor",
        "RGBAColor",
        "RGBColor",
    }
)

_EXPECTED_CORE: frozenset[str] = frozenset(
    {
        "_UNSET_PARAM",
        "AlphaPosition",
        "BoxSpacing",
        "ColorModel",
        "ImageFormat",
        "ImageFormatInfo",
        "Margin",
        "Padding",
        "Rectangle",
        "SupportedPlatforms",
    }
)

_EXPECTED_DRAW: frozenset[str] = frozenset(
    {
        "DashStyle",
        "MinimalDraw",
        "StrokeStyle",
    }
)

_EXPECTED_FONT_FILES: frozenset[str] = frozenset(
    {
        "FONTS_HONK",
        "FONTS_NOTO_SANS",
        "FONTS_NOTO_SANS_BW",
        "FONTS_NOTO_SANS_MINIMAL",
        "FontFileDownloadResult",
        "FontFileDownloadSource",
        "FontFileDownloader",
        "FontManifestEntry",
        "FontManifestFile",
        "FontManifestManager",
        "FontManifestStore",
        "FontManifestVerifier",
        "ManifestVerificationReport",
    }
)

_EXPECTED_FONT_SETUP: frozenset[str] = frozenset(
    {
        "FontSetup",
        "FontconfigMode",
    }
)

_EXPECTED_IMAGE_BACKEND: frozenset[str] = frozenset(
    {
        "ImageBackend",
        "ImageBackendInfo",
        "ImagePlacer",
        "ImagePlacerParameters",
        "ImageScaleMode",
        "SurfaceArrayBackend",
        "SurfaceArrayConverter",
        "SurfaceArrayConverterParameters",
        "SurfaceArrayResult",
        "SurfaceWriter",
        "SurfaceWriterParameters",
    }
)

_EXPECTED_LAYOUT_ENGINES: frozenset[str] = frozenset(
    {
        "AlignContent",
        "AlignItems",
        "AlignSelf",
        "CaptionSpec",
        "FlexContainerProperties",
        "FlexDirection",
        "FlexItemProperties",
        "FlexWrap",
        "JustifyContent",
        "MinimalFlexBox",
        "MinimalFlexBoxTemplates",
        "MinimalFlexNode",
        "PositionHelpers",
    }
)

_EXPECTED_PANGO_BACKEND: frozenset[str] = frozenset(
    {
        "AlignmentStr",
        "ClippedText",
        "DirectionStr",
        "EllipsizeModeStr",
        "ExtentsMode",
        "FitsResult",
        "FontColorStr",
        "FontDescriptionInterface",
        "FontDescriptionInterfaceParameters",
        "GravityHintStr",
        "GravityStr",
        "HeightConstraint",
        "HeightDeviceUnits",
        "HeightLineLimit",
        "HeightSingleLine",
        "LayoutContextInterface",
        "LayoutContextInterfaceParameters",
        "LayoutFitReport",
        "LayoutInterface",
        "LayoutInterfaceParameters",
        "LayoutRect",
        "PangoEnumCoerce",
        "PangoEnumMap",
        "StretchStr",
        "StyleStr",
        "TabAlignStr",
        "TextStrategy",
        "VariantStr",
        "WeightStr",
        "WidthConstraint",
        "WidthDeviceUnits",
        "WidthUnconstrained",
        "WrapModeStr",
    }
)

_SNAPSHOTS: dict[str, frozenset[str]] = {
    "bounding_boxes": _EXPECTED_BOUNDING_BOXES,
    "cairo_backend": _EXPECTED_CAIRO_BACKEND,
    "colors": _EXPECTED_COLORS,
    "core": _EXPECTED_CORE,
    "draw": _EXPECTED_DRAW,
    "font_files": _EXPECTED_FONT_FILES,
    "font_setup": _EXPECTED_FONT_SETUP,
    "image_backend": _EXPECTED_IMAGE_BACKEND,
    "layout_engines": _EXPECTED_LAYOUT_ENGINES,
    "pango_backend": _EXPECTED_PANGO_BACKEND,
}


class TestTendernessTopLevelNamespace:
    def test_sub_package_exports_match_snapshot(self) -> None:
        import importlib

        for pkg_name, expected in _SNAPSHOTS.items():
            pkg = importlib.import_module(f"tenderness.{pkg_name}")
            actual = frozenset(pkg.__all__)
            assert actual == expected, (
                f"tenderness.{pkg_name} public API changed. Added: {actual - expected}, Removed: {expected - actual}"
            )

    def test_all_sub_package_exports_at_top_level(self) -> None:
        import importlib

        import tenderness

        for pkg_name in _SNAPSHOTS:
            pkg = importlib.import_module(f"tenderness.{pkg_name}")
            for name in pkg.__all__:
                assert hasattr(tenderness, name), (
                    f"{name!r} from tenderness.{pkg_name} is in __all__ but missing from tenderness.*"
                )

    def test_pipeline_types_not_at_top_level(self) -> None:
        import tenderness
        import tenderness.pipelines.document as document_pkg

        for name in document_pkg.__all__:
            assert not hasattr(tenderness, name), f"{name!r} is a pipeline type but leaked into tenderness.*"
