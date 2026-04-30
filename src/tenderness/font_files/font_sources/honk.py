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

"""Download sources for the Honk variable font."""

from __future__ import annotations

from tenderness.font_files.downloader_spec import FontFileDownloadSource
from tenderness.font_files.integrity import DuplicateChecker

_HONK_COMMIT = "c8e45997f999c1b23a812d4706df464c13ee8861"

_HONK = [
    FontFileDownloadSource(
        # ofl/honk/Honk[MORF,SHLN].ttf
        url=f"https://github.com/google/fonts/raw/{_HONK_COMMIT}/ofl/honk/Honk%5BMORF%2CSHLN%5D.ttf"
    ),
]


FONTS_HONK = DuplicateChecker.validate(_HONK, check_fields=["url", "file_name"])
