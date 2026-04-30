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

from tenderness.font_files.downloader import FontFileDownloader
from tests._test_utils.class_test import ClassTestBase, ClassTestConfig

# --------------------------
# Tests for FontFileDownloader
# --------------------------
FONT_FILE_DOWNLOADER_EXPECTED_METHODS = {
    "download",
    "download_parallel",
    "_fetch_to_disk",
}
FONT_FILE_DOWNLOADER_EXPECTED_STATIC_METHODS = {"_build_session"}
FONT_FILE_DOWNLOADER_EXPECTED_CLASS_VARS = {
    "CHUNK_SIZE",
    "DEFAULT_BACKOFF_BASE",
    "DEFAULT_DELAY_BETWEEN",
    "DEFAULT_MAX_RETRIES",
    "DEFAULT_MAX_WORKERS",
    "DEFAULT_TIMEOUT",
}

FONT_FILE_DOWNLOADER_TEST_CLASS_CONFIG = [
    ClassTestConfig(
        cls=FontFileDownloader,
        expected_class_vars=FONT_FILE_DOWNLOADER_EXPECTED_CLASS_VARS,
        expected_methods=FONT_FILE_DOWNLOADER_EXPECTED_METHODS,
        expected_static_methods=FONT_FILE_DOWNLOADER_EXPECTED_STATIC_METHODS,
    )
]


@pytest.mark.parametrize("config", FONT_FILE_DOWNLOADER_TEST_CLASS_CONFIG, ids=lambda c: c.cls.__name__)
class TestFontFileDownloaderContract(ClassTestBase):
    pass
