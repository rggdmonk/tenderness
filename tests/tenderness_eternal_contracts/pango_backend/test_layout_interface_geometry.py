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

import pytest

from tenderness.pango_backend.layout_interface_geometry import (
    ClippedText,
    ExtentsMode,
    FitsResult,
    HeightDeviceUnits,
    HeightLineLimit,
    HeightSingleLine,
    LayoutFitReport,
    LayoutRect,
    WidthDeviceUnits,
    WidthUnconstrained,
)
from tests._test_utils.dataclass_test import DataclassTestBase, DataclassTestConfig
from tests._test_utils.str_enum_test import StrEnumTestBase, StrEnumTestConfig

# --------------------------
# Tests for ExtentsMode
# --------------------------
EXTENTS_MODE_EXPECTED_MEMBERS = {"INK", "LOGICAL"}
EXTENTS_MODE_TEST_STR_ENUM_CONFIG = [
    StrEnumTestConfig(
        enum_class=ExtentsMode,
        expected_members=EXTENTS_MODE_EXPECTED_MEMBERS,
    )
]


@pytest.mark.parametrize("config", EXTENTS_MODE_TEST_STR_ENUM_CONFIG, ids=lambda c: c.enum_class.__name__)
class TestExtentsModeContract(StrEnumTestBase):
    pass


# --------------------------
# Tests for LayoutRect
# --------------------------
LAYOUT_RECT_EXPECTED_CLASS_METHODS = {"from_pango_rectangle"}
LAYOUT_RECT_TEST_DATACLASS_CONFIG = [
    DataclassTestConfig(
        dataclass_class=LayoutRect,
        has_slots=False,
        is_frozen=True,
        expected_class_methods=LAYOUT_RECT_EXPECTED_CLASS_METHODS,
    )
]


@pytest.mark.parametrize("config", LAYOUT_RECT_TEST_DATACLASS_CONFIG, ids=lambda c: c.dataclass_class.__name__)
class TestLayoutRectContract(DataclassTestBase):
    pass


# --------------------------
# Tests for WidthDeviceUnits
# --------------------------
WIDTH_DEVICE_UNITS_EXPECTED_FIELDS = {"width"}
WIDTH_DEVICE_UNITS_TEST_DATACLASS_CONFIG = [
    DataclassTestConfig(
        dataclass_class=WidthDeviceUnits,
        has_slots=True,
        is_frozen=True,
        expected_fields=WIDTH_DEVICE_UNITS_EXPECTED_FIELDS,
    )
]


@pytest.mark.parametrize("config", WIDTH_DEVICE_UNITS_TEST_DATACLASS_CONFIG, ids=lambda c: c.dataclass_class.__name__)
class TestWidthDeviceUnitsContract(DataclassTestBase):
    pass


# --------------------------
# Tests for WidthUnconstrained
# --------------------------
WIDTH_UNCONSTRAINED_TEST_DATACLASS_CONFIG = [
    DataclassTestConfig(
        dataclass_class=WidthUnconstrained,
        has_slots=True,
        is_frozen=True,
    )
]


@pytest.mark.parametrize("config", WIDTH_UNCONSTRAINED_TEST_DATACLASS_CONFIG, ids=lambda c: c.dataclass_class.__name__)
class TestWidthUnconstrainedContract(DataclassTestBase):
    pass


# --------------------------
# Tests for HeightLineLimit
# --------------------------
HEIGHT_LINE_LIMIT_EXPECTED_FIELDS = {"lines"}
HEIGHT_LINE_LIMIT_TEST_DATACLASS_CONFIG = [
    DataclassTestConfig(
        dataclass_class=HeightLineLimit,
        has_slots=True,
        is_frozen=True,
        expected_fields=HEIGHT_LINE_LIMIT_EXPECTED_FIELDS,
    )
]


@pytest.mark.parametrize("config", HEIGHT_LINE_LIMIT_TEST_DATACLASS_CONFIG, ids=lambda c: c.dataclass_class.__name__)
class TestHeightLineLimitContract(DataclassTestBase):
    pass


# --------------------------
# Tests for HeightSingleLine
# --------------------------
HEIGHT_SINGLE_LINE_TEST_DATACLASS_CONFIG = [
    DataclassTestConfig(
        dataclass_class=HeightSingleLine,
        has_slots=True,
        is_frozen=True,
    )
]


@pytest.mark.parametrize("config", HEIGHT_SINGLE_LINE_TEST_DATACLASS_CONFIG, ids=lambda c: c.dataclass_class.__name__)
class TestHeightSingleLineContract(DataclassTestBase):
    pass


# --------------------------
# Tests for HeightDeviceUnits
# --------------------------
HEIGHT_DEVICE_UNITS_EXPECTED_FIELDS = {"height"}
HEIGHT_DEVICE_UNITS_TEST_DATACLASS_CONFIG = [
    DataclassTestConfig(
        dataclass_class=HeightDeviceUnits,
        has_slots=True,
        is_frozen=True,
        expected_fields=HEIGHT_DEVICE_UNITS_EXPECTED_FIELDS,
    )
]


@pytest.mark.parametrize("config", HEIGHT_DEVICE_UNITS_TEST_DATACLASS_CONFIG, ids=lambda c: c.dataclass_class.__name__)
class TestHeightDeviceUnitsContract(DataclassTestBase):
    pass


# --------------------------
# Tests for FitsResult
# --------------------------
FITS_RESULT_EXPECTED_FIELDS = {
    "extents_mode",
    "width",
    "height",
    "ellipsis",
    "wrap",
    "rect",
    "width_device_units",
    "height_device_units",
    "unknown_glyphs_count",
}
FITS_RESULT_EXPECTED_PROPERTIES = {"fit_both"}
FITS_RESULT_TEST_DATACLASS_CONFIG = [
    DataclassTestConfig(
        dataclass_class=FitsResult,
        has_slots=True,
        is_frozen=True,
        expected_fields=FITS_RESULT_EXPECTED_FIELDS,
        expected_properties=FITS_RESULT_EXPECTED_PROPERTIES,
    )
]


@pytest.mark.parametrize("config", FITS_RESULT_TEST_DATACLASS_CONFIG, ids=lambda c: c.dataclass_class.__name__)
class TestFitsResultContract(DataclassTestBase):
    pass


# --------------------------
# Tests for ClippedText
# --------------------------
CLIPPED_TEXT_EXPECTED_FIELDS = {"visible", "clipped", "last_visible_line", "clipped_char_byte_index"}
CLIPPED_TEXT_EXPECTED_PROPERTIES = {"has_clipped"}
CLIPPED_TEXT_TEST_DATACLASS_CONFIG = [
    DataclassTestConfig(
        dataclass_class=ClippedText,
        has_slots=True,
        is_frozen=True,
        expected_fields=CLIPPED_TEXT_EXPECTED_FIELDS,
        expected_properties=CLIPPED_TEXT_EXPECTED_PROPERTIES,
    )
]


@pytest.mark.parametrize("config", CLIPPED_TEXT_TEST_DATACLASS_CONFIG, ids=lambda c: c.dataclass_class.__name__)
class TestClippedTextContract(DataclassTestBase):
    pass


# --------------------------
# Tests for LayoutFitReport
# --------------------------
LAYOUT_FIT_REPORT_EXPECTED_FIELDS = {
    "fits_logical",
    "fits_ink",
    "clipped_text",
}
LAYOUT_FIT_REPORT_TEST_DATACLASS_CONFIG = [
    DataclassTestConfig(
        dataclass_class=LayoutFitReport,
        has_slots=True,
        is_frozen=True,
        expected_fields=LAYOUT_FIT_REPORT_EXPECTED_FIELDS,
    )
]


@pytest.mark.parametrize("config", LAYOUT_FIT_REPORT_TEST_DATACLASS_CONFIG, ids=lambda c: c.dataclass_class.__name__)
class TestLayoutFitReportContract(DataclassTestBase):
    pass
