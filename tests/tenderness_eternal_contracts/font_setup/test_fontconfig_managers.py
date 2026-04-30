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

from tenderness.font_setup.fontconfig_managers import (
    BaseFontconfigManager,
    DarwinFontconfigManager,
    LinuxFontconfigManager,
)
from tests._test_utils.class_test import ClassTestBase, ClassTestConfig

# --------------------------
# Tests BaseFontconfigManager
# --------------------------
BASE_FONTCONFIG_MANAGER_EXPECTED_METHODS = {
    "_parse_xml_config_file",
    "_write_xml_config_file",
    "_validate_conf_file_existence",
    "_insert_font_dir",
    "_remove_system_fonts",
    "load_fontconfig_file_from_path",
    "copy_fontconfig_file",
    "add_font_directory",
    "add_font_directory_and_remove_system",
    "create_fontconfig_from_template",
}
BASE_FONTCONFIG_MANAGER_EXPECTED_ABSTRACT_PROPERTIES = {"remove_system_fonts_patterns", "template_map"}
BASE_FONTCONFIG_MANAGER_EXPECTED_CLASS_VARS = {"fontconfig_extension"}

BASE_FONTCONFIG_MANAGER_TEST_CLASS_CONFIG = [
    ClassTestConfig(
        cls=BaseFontconfigManager,
        is_abstract=True,
        expected_class_vars=BASE_FONTCONFIG_MANAGER_EXPECTED_CLASS_VARS,
        expected_abstract_properties=BASE_FONTCONFIG_MANAGER_EXPECTED_ABSTRACT_PROPERTIES,
        expected_methods=BASE_FONTCONFIG_MANAGER_EXPECTED_METHODS,
    ),
]


@pytest.mark.parametrize("config", BASE_FONTCONFIG_MANAGER_TEST_CLASS_CONFIG, ids=lambda c: c.cls.__name__)
class TestBaseFontconfigManagerContract(ClassTestBase):
    pass


# --------------------------
# Tests DarwinFontconfigManager
# --------------------------
DARWIN_FONTCONFIG_MANAGER_TEST_CLASS_CONFIG = [
    ClassTestConfig(
        cls=DarwinFontconfigManager,
        expected_properties=BASE_FONTCONFIG_MANAGER_EXPECTED_ABSTRACT_PROPERTIES,
    ),
]


@pytest.mark.parametrize("config", DARWIN_FONTCONFIG_MANAGER_TEST_CLASS_CONFIG, ids=lambda c: c.cls.__name__)
class TestDarwinFontconfigManagerContract(ClassTestBase):
    pass


# --------------------------
# Tests LinuxFontconfigManager
# --------------------------
LINUX_FONTCONFIG_MANAGER_TEST_CLASS_CONFIG = [
    ClassTestConfig(
        cls=LinuxFontconfigManager,
        expected_properties=BASE_FONTCONFIG_MANAGER_EXPECTED_ABSTRACT_PROPERTIES,
    ),
]


@pytest.mark.parametrize("config", LINUX_FONTCONFIG_MANAGER_TEST_CLASS_CONFIG, ids=lambda c: c.cls.__name__)
class TestLinuxFontconfigManagerContract(ClassTestBase):
    pass
