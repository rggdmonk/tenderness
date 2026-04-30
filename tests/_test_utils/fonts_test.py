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

from tenderness.font_files.downloader_spec import FontFileDownloadSource

_TEST_FONTS_COMMIT = "c8e45997f999c1b23a812d4706df464c13ee8861"
_TEST_FONT_SOURCES = [
    FontFileDownloadSource(
        # ofl/honk/Honk[MORF,SHLN].ttf
        url=f"https://github.com/google/fonts/raw/{_TEST_FONTS_COMMIT}/ofl/honk/Honk%5BMORF,SHLN%5D.ttf"
    ),
    FontFileDownloadSource(
        # ofl/notocoloremoji/NotoColorEmoji-Regular.ttf
        url=f"https://github.com/google/fonts/raw/{_TEST_FONTS_COMMIT}/ofl/notocoloremoji/NotoColorEmoji-Regular.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosanscuneiform/NotoSansCuneiform-Regular.ttf
        url=f"https://github.com/google/fonts/raw/{_TEST_FONTS_COMMIT}/ofl/notosanscuneiform/NotoSansCuneiform-Regular.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosans/NotoSans[wdth,wght].ttf
        url=f"https://github.com/google/fonts/raw/{_TEST_FONTS_COMMIT}/ofl/notosans/NotoSans%5Bwdth%2Cwght%5D.ttf",
    ),
    FontFileDownloadSource(
        # ofl/longcang/LongCang-Regular.ttf
        url=f"https://github.com/google/fonts/raw/{_TEST_FONTS_COMMIT}/ofl/longcang/LongCang-Regular.ttf",
    ),
    FontFileDownloadSource(
        # ofl/marhey/Marhey[wght].ttf
        url=f"https://github.com/google/fonts/raw/{_TEST_FONTS_COMMIT}/ofl/marhey/Marhey%5Bwght%5D.ttf",
    ),
    FontFileDownloadSource(
        # ofl/rubikglitch/RubikGlitch-Regular.ttf
        url=f"https://github.com/google/fonts/raw/{_TEST_FONTS_COMMIT}/ofl/rubikglitch/RubikGlitch-Regular.ttf",
    ),
]
