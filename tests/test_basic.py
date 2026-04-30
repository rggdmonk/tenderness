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

import sys

from scripts.download_test_fonts import _MANIFEST_NAME
from tenderness.font_files.manifest import FontManifestManager
from tests._test_utils.fonts_test import _TEST_FONT_SOURCES
from tests._test_utils.paths_test import TEST_FONTS_DIR, TESTS_CACHE_DIR

_DOWNLOAD_HINT = "Run 'python -m scripts.download_test_fonts' to download test fonts."


class TestDownloadTestFonts:
    def test_fonts_dir_exists(self) -> None:
        assert TEST_FONTS_DIR.is_dir(), f"Test fonts directory not found. {_DOWNLOAD_HINT}"

    def test_manifest_is_ready(self) -> None:
        manager = FontManifestManager(cache_dir=TESTS_CACHE_DIR)
        assert manager.is_manifest_ready(_MANIFEST_NAME), (
            f"Font manifest '{_MANIFEST_NAME}' not ready. {_DOWNLOAD_HINT}"
        )

    def test_all_expected_font_files_present(self) -> None:
        for source in _TEST_FONT_SOURCES:
            assert (TEST_FONTS_DIR / source.file_name).is_file(), f"Missing font: {source.file_name}. {_DOWNLOAD_HINT}"


def test_little_endian() -> None:

    # TODO: to array method can have different behavior on big-endian systems(now no check in code).
    # For now we just check that tests are run on little-endian system, but in future we can add support for big-endian if needed.
    byte_order = sys.byteorder

    assert byte_order == "little", f"Expected little-endian system, got {byte_order}"
