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
from tenderness.font_files.downloader import FontFileDownloader
from tenderness.font_files.downloader_spec import FontFileDownloadResult, FontFileDownloadSource
from tenderness.font_files.font_sources.honk import FONTS_HONK
from tenderness.font_files.font_sources.noto import FONTS_NOTO_SANS, FONTS_NOTO_SANS_BW, FONTS_NOTO_SANS_MINIMAL
from tenderness.font_files.manifest import (
    FontManifestEntry,
    FontManifestFile,
    FontManifestManager,
    FontManifestStore,
    FontManifestVerifier,
    ManifestVerificationReport,
)

__all__ = [
    "FONTS_HONK",
    "FONTS_NOTO_SANS",
    "FONTS_NOTO_SANS_BW",
    "FONTS_NOTO_SANS_MINIMAL",
    "FontFileDownloadResult",
    "FontFileDownloadSource",
    "FontFileDownloader",
    "FontManifestEntry",
    "FontManifestFile",
    "FontManifestManager",
    "FontManifestStore",
    "FontManifestVerifier",
    "ManifestVerificationReport",
]
