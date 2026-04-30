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

from tenderness.image_backend.image_placer import (
    ImagePlacer,
    ImagePlacerParameters,
    ImageScaleMode,
)
from tests._test_utils.class_test import ClassTestBase, ClassTestConfig
from tests._test_utils.dataclass_test import DataclassTestBase, DataclassTestConfig
from tests._test_utils.str_enum_test import StrEnumTestBase, StrEnumTestConfig

# --------------------------
# Tests for ImageScaleMode
# --------------------------
IMAGE_SCALE_MODE_EXPECTED_MEMBERS = {"STRETCH", "FIT", "FILL", "NONE"}
IMAGE_SCALE_MODE_TEST_STR_ENUM_CONFIG = [
    StrEnumTestConfig(
        enum_class=ImageScaleMode,
        expected_members=IMAGE_SCALE_MODE_EXPECTED_MEMBERS,
    )
]


@pytest.mark.parametrize("config", IMAGE_SCALE_MODE_TEST_STR_ENUM_CONFIG, ids=lambda c: c.enum_class.__name__)
class TestImageScaleModeContract(StrEnumTestBase):
    pass


# --------------------------
# Tests for ImagePlacerParameters
# --------------------------
IMAGE_PLACER_PARAMETERS_EXPECTED_FIELDS = {
    "path_to_image",
    "dest_rect",
    "scale_mode",
    "operator",
    "alpha",
    "image_format",
}
IMAGE_PLACER_PARAMETERS_EXPECTED_METHODS = {"__post_init__"}
IMAGE_PLACER_PARAMETERS_TEST_DATACLASS_CONFIG = [
    DataclassTestConfig(
        dataclass_class=ImagePlacerParameters,
        has_slots=True,
        expected_fields=IMAGE_PLACER_PARAMETERS_EXPECTED_FIELDS,
        expected_methods=IMAGE_PLACER_PARAMETERS_EXPECTED_METHODS,
    )
]


@pytest.mark.parametrize(
    "config", IMAGE_PLACER_PARAMETERS_TEST_DATACLASS_CONFIG, ids=lambda c: c.dataclass_class.__name__
)
class TestImagePlacerParametersContract(DataclassTestBase):
    pass


# --------------------------
# Tests for ImagePlacer
# --------------------------
IMAGE_PLACER_EXPECTED_METHODS = {
    "place",
}
IMAGE_PLACER_TEST_CLASS_CONFIG = [
    ClassTestConfig(
        cls=ImagePlacer,
        expected_methods=IMAGE_PLACER_EXPECTED_METHODS,
    )
]


@pytest.mark.parametrize("config", IMAGE_PLACER_TEST_CLASS_CONFIG, ids=lambda c: c.cls.__name__)
class TestImagePlacerContract(ClassTestBase):
    pass
