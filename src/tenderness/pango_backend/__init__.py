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

from tenderness.pango_backend.font_description_interface import (
    FontDescriptionInterface,
    FontDescriptionInterfaceParameters,
)
from tenderness.pango_backend.layout_context_interface import LayoutContextInterface, LayoutContextInterfaceParameters
from tenderness.pango_backend.layout_interface import LayoutInterface, LayoutInterfaceParameters, TextStrategy
from tenderness.pango_backend.layout_interface_geometry import (
    ClippedText,
    ExtentsMode,
    FitsResult,
    HeightConstraint,
    HeightDeviceUnits,
    HeightLineLimit,
    HeightSingleLine,
    LayoutFitReport,
    LayoutRect,
    WidthConstraint,
    WidthDeviceUnits,
    WidthUnconstrained,
)
from tenderness.pango_backend.pango_enum_coerce import (
    AlignmentStr,
    DirectionStr,
    EllipsizeModeStr,
    FontColorStr,
    GravityHintStr,
    GravityStr,
    PangoEnumCoerce,
    PangoEnumMap,
    StretchStr,
    StyleStr,
    TabAlignStr,
    VariantStr,
    WeightStr,
    WrapModeStr,
)

__all__ = [
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
]
