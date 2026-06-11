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

from tenderness.font_setup.font_setup import FontSetup
from tests._test_utils.class_test import ClassTestBase, ClassTestConfig

# --------------------------
# Tests FontSetup
# --------------------------
FONT_SETUP_EXPECTED_METHODS = {
    "_detect_supported_system",
    "_get_fontconfig_manager",
    "_load_from_file",
    "_copy_system_fontconfig_file",
    "_add_font_directory",
    "_add_font_directory_and_remove_system",
    "_create_fontconfig_from_template",
    "_ordered_lib_names",
    "_try_load",
    "_strategy_find_library",
    "_strategy_dynamic_linker",
    "_strategy_manual_search",
    "_find_and_load_fontconfig",
    "_reinitialize_fontconfig_cache",
    "_configure_environment",
    "_setup_font_by_mode",
    "setup_font",
    "get_all_font_families",
    "is_font_family_available",
    "get_font_map_resolution",
    "set_font_map_resolution",
}
FONT_SETUP_EXPECTED_CLASS_VARS = {"manager_map"}
FONT_SETUP_TEST_CLASS_CONFIG = [
    ClassTestConfig(
        cls=FontSetup,
        expected_class_vars=FONT_SETUP_EXPECTED_CLASS_VARS,
        expected_methods=FONT_SETUP_EXPECTED_METHODS,
    )
]


@pytest.mark.parametrize("config", FONT_SETUP_TEST_CLASS_CONFIG, ids=lambda c: c.cls.__name__)
class TestFontSetupContract(ClassTestBase):
    pass
