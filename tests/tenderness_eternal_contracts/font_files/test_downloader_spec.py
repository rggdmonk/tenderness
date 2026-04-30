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

from tenderness.font_files.downloader_spec import FontFileDownloadResult, FontFileDownloadSource
from tests._test_utils.dataclass_test import DataclassTestBase, DataclassTestConfig

# --------------------------
# Tests for FontFileDownloadSource
# --------------------------
FONT_FILE_DOWNLOAD_SOURCE_EXPECTED_FIELDS = {"url", "file_name"}
FONT_FILE_DOWNLOAD_SOURCE_EXPECTED_METHODS = {"__post_init__", "__str__", "extract_file_name", "to_dict"}

FONT_FILE_DOWNLOAD_SOURCE_TEST_DATACLASS_CONFIG = [
    DataclassTestConfig(
        dataclass_class=FontFileDownloadSource,
        has_slots=True,
        expected_fields=FONT_FILE_DOWNLOAD_SOURCE_EXPECTED_FIELDS,
        expected_methods=FONT_FILE_DOWNLOAD_SOURCE_EXPECTED_METHODS,
    )
]


@pytest.mark.parametrize(
    "config", FONT_FILE_DOWNLOAD_SOURCE_TEST_DATACLASS_CONFIG, ids=lambda c: c.dataclass_class.__name__
)
class TestFontFileDownloadSourceContract(DataclassTestBase):
    pass


# --------------------------
# Tests for FontFileDownloadResult
# --------------------------
FONT_FILE_DOWNLOAD_RESULT_EXPECTED_FIELDS = {"url", "output_file_path", "success", "sha256"}
FONT_FILE_DOWNLOAD_RESULT_EXPECTED_METHODS = {"to_dict"}

FONT_FILE_DOWNLOAD_RESULT_TEST_DATACLASS_CONFIG = [
    DataclassTestConfig(
        dataclass_class=FontFileDownloadResult,
        has_slots=True,
        expected_fields=FONT_FILE_DOWNLOAD_RESULT_EXPECTED_FIELDS,
        expected_methods=FONT_FILE_DOWNLOAD_RESULT_EXPECTED_METHODS,
    )
]


@pytest.mark.parametrize(
    "config", FONT_FILE_DOWNLOAD_RESULT_TEST_DATACLASS_CONFIG, ids=lambda c: c.dataclass_class.__name__
)
class TestFontFileDownloadResultContract(DataclassTestBase):
    pass
