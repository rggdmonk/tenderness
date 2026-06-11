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

import logging

from tenderness.font_files.manifest import FontManifestManager
from tests._test_utils.fonts_test import _TEST_FONT_SOURCES
from tests._test_utils.paths_test import TESTS_CACHE_DIR

logger = logging.getLogger(__name__)

_MANIFEST_NAME = "fonts_for_tests"


def download_test_fonts() -> None:
    manager = FontManifestManager(cache_dir=TESTS_CACHE_DIR, max_workers=2)
    if manager.is_manifest_ready(_MANIFEST_NAME):
        logger.info("Test fonts already ready.")
        return
    fonts_dir = manager.prepare_font_files(sources=_TEST_FONT_SOURCES, manifest_name=_MANIFEST_NAME)
    logger.info("Test fonts are ready in %s", fonts_dir)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    download_test_fonts()
