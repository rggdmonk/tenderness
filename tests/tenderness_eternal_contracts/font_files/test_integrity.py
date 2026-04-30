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

from tenderness.font_files.integrity import CheckSumUtils, DuplicateChecker
from tests._test_utils.class_test import ClassTestBase, ClassTestConfig

# --------------------------
# Tests for DuplicateChecker
# --------------------------
DUPLICATE_CHECKER_EXPECTED_STATIC_METHODS = {"find_duplicate", "raise_if_duplicates", "validate"}
DUPLICATE_CHECKER_TEST_CLASS_CONFIG = [
    ClassTestConfig(
        cls=DuplicateChecker,
        expected_static_methods=DUPLICATE_CHECKER_EXPECTED_STATIC_METHODS,
    )
]


@pytest.mark.parametrize("config", DUPLICATE_CHECKER_TEST_CLASS_CONFIG, ids=lambda c: c.cls.__name__)
class TestDuplicateCheckerContract(ClassTestBase):
    pass


# --------------------------
# Tests for CheckSumUtils
# --------------------------
CHECKSUM_UTILS_EXPECTED_STATIC_METHODS = {"compute_sha256"}
CHECKSUM_UTILS_TEST_CLASS_CONFIG = [
    ClassTestConfig(
        cls=CheckSumUtils,
        expected_static_methods=CHECKSUM_UTILS_EXPECTED_STATIC_METHODS,
    )
]


@pytest.mark.parametrize("config", CHECKSUM_UTILS_TEST_CLASS_CONFIG, ids=lambda c: c.cls.__name__)
class TestCheckSumUtilsContract(ClassTestBase):
    pass
