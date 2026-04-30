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

from tenderness.image_backend.image_backends import ImageBackend, ImageBackendInfo
from tests._test_utils.dataclass_test import DataclassTestBase, DataclassTestConfig
from tests._test_utils.enum_test import EnumTestBase, EnumTestConfig

# --------------------------
# Tests for ImageBackendInfo
# --------------------------
IMAGE_BACKEND_INFO_EXPECTED_FIELDS = {"backend_name", "supported_formats"}
IMAGE_BACKEND_INFO_TEST_DATACLASS_CONFIG = [
    DataclassTestConfig(
        dataclass_class=ImageBackendInfo,
        has_slots=True,
        is_frozen=True,
        expected_fields=IMAGE_BACKEND_INFO_EXPECTED_FIELDS,
    )
]


@pytest.mark.parametrize("config", IMAGE_BACKEND_INFO_TEST_DATACLASS_CONFIG, ids=lambda c: c.dataclass_class.__name__)
class TestImageBackendInfoContract(DataclassTestBase):
    pass


# --------------------------
# Test cases for ImageBackend
# --------------------------
IMAGE_BACKEND_EXPECTED_MEMBERS = {"CAIRO", "PIL", "CV2"}
IMAGE_BACKEND_EXPECTED_PROPERTIES = {"backend_name", "supported_formats"}
IMAGE_BACKEND_EXPECTED_METHODS = {"is_image_format_supported", "has_alpha_support", "has_vector_support"}
IMAGE_BACKEND_EXPECTED_CLASS_METHODS = {"backends_supporting_format", "backends_supporting_all_formats"}
IMAGE_BACKEND_TEST_ENUM_CONFIG = [
    EnumTestConfig(
        enum_class=ImageBackend,
        expected_members=IMAGE_BACKEND_EXPECTED_MEMBERS,
        expected_properties=IMAGE_BACKEND_EXPECTED_PROPERTIES,
        expected_methods=IMAGE_BACKEND_EXPECTED_METHODS,
        expected_class_methods=IMAGE_BACKEND_EXPECTED_CLASS_METHODS,
    )
]


@pytest.mark.parametrize("config", IMAGE_BACKEND_TEST_ENUM_CONFIG, ids=lambda c: c.enum_class.__name__)
class TestImageBackendContract(EnumTestBase):
    pass
