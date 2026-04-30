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


from tenderness.cairo_backend.background_selector import BackgroundSelector
from tenderness.cairo_backend.cairo_enum_coerce import (
    AntialiasStr,
    CairoEnumCoerce,
    CairoEnumMap,
    ColorModeStr,
    HintMetricsStr,
    HintStyleStr,
    OperatorStr,
    PDFVersionStr,
    SubpixelOrderStr,
    SVGUnitStr,
    SVGVersionStr,
)
from tenderness.cairo_backend.color_patterns import (
    ColorPattern,
    ColorStop,
    ImagePatternSpec,
    LinearGradientColorSpec,
    PatternColorSpec,
    RadialGradientColorSpec,
    SolidColorSpec,
    SurfacePatternSpec,
)
from tenderness.cairo_backend.font_options_interface import FontOptionsInterface, FontOptionsInterfaceParameters
from tenderness.cairo_backend.matrix.context_transformer_pipeline import (
    CairoContextTransformPipeline,
    TransformDataclassParameter,
    TransformDictParameter,
    TransformParameter,
)
from tenderness.cairo_backend.matrix.matrix_transformer import CairoMatrixTransformer
from tenderness.cairo_backend.matrix.matrix_transforms import (
    FlipHorizontalParameters,
    FlipVerticalParameters,
    MatrixTransformType,
    RotateAroundPointParameters,
    RotateParameters,
    ScaleParameters,
    SkewXParameters,
    SkewYParameters,
    TranslateParameters,
)
from tenderness.cairo_backend.pixel_formats import ChannelOrder, PixelDType, PixelFormat, PixelFormatInfo, PixelOrder
from tenderness.cairo_backend.surface_config_manager import SurfaceConfigManager
from tenderness.cairo_backend.surface_configuration import (
    ImageSurfaceConfig,
    PDFSurfaceConfig,
    SurfaceRect,
    SurfaceType,
    SVGSurfaceConfig,
)
from tenderness.cairo_backend.surface_creator import SurfaceCreator
from tenderness.cairo_backend.text_color_selector import TextColorSelector

__all__ = [
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
]
