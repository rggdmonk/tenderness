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

"""Cache directory paths for the tenderness library."""

from __future__ import annotations

import os
import pathlib
import platform

from tenderness.core.supported_platforms import SupportedPlatforms


def get_cache_dir() -> pathlib.Path:
    """Get the appropriate user-specific cache directory based on OS conventions.

    Raises
    ------
    ValueError
        If the current platform is not supported.
    """
    system = platform.system()

    if system not in list(SupportedPlatforms):
        msg = f"Unsupported platform: {system}. This application only supports the following platforms: {list(SupportedPlatforms)}."
        raise ValueError(msg)

    # first check for XDG_CACHE_HOME
    if xdg_cache_home := os.getenv("XDG_CACHE_HOME"):
        return pathlib.Path(xdg_cache_home).expanduser().resolve()

    # fallback to default
    return pathlib.Path.home() / ".cache"


LIBRARY_NAME = "tenderness"

TENDERNESS_BASE_CACHE_DIR = get_cache_dir() / LIBRARY_NAME

TENDERNESS_FONTS_DIR = TENDERNESS_BASE_CACHE_DIR / "fonts"

TENDERNESS_FONTCONFIGS_DIR = TENDERNESS_BASE_CACHE_DIR / "fontconfigs"

TENDERNESS_IMAGES_DIR = TENDERNESS_BASE_CACHE_DIR / "images"
