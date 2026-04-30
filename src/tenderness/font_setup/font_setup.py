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

"""Fontconfig-based font setup for cairo/pango rendering."""

from __future__ import annotations

import ctypes
import logging
import os
import pathlib
import platform
import sys
from ctypes.util import find_library
from typing import ClassVar

import gi

from tenderness.core.cache_paths import TENDERNESS_FONTCONFIGS_DIR
from tenderness.core.supported_platforms import SupportedPlatforms
from tenderness.font_setup.fontconfig_managers import (
    BaseFontconfigManager,
    DarwinFontconfigManager,
    FontconfigMode,
    LinuxFontconfigManager,
)

gi.require_version("Pango", "1.0")
gi.require_version("PangoCairo", "1.0")

from gi.repository import PangoCairo  # noqa: E402

logger = logging.getLogger(__name__)


_TENDERNESS_FONTCONFIG_DARWIN_NAMES = ["libfontconfig.1.dylib", "fontconfig.dylib"]
_TENDERNESS_FONTCONFIG_LINUX_NAMES = ["libfontconfig.so.1", "libfontconfig.so"]
_TENDERNESS_FONTCONFIG_GENERIC_NAMES = ["fontconfig"]
_TENDERNESS_FONTCONFIG_SEARCH_DIRS = [
    pathlib.Path("/opt/homebrew/lib"),  # Homebrew on Apple Silicon
    pathlib.Path("/usr/local/lib"),  # Homebrew on Intel, other custom installs
    pathlib.Path("/usr/lib64"),  # Standard Linux
    pathlib.Path("/usr/lib"),  # Standard Linux
    pathlib.Path(sys.prefix) / "lib",  # Python venv/conda env
]

_TENDERNESS_PANGOCAIRO_BACKEND_ENV = "PANGOCAIRO_BACKEND"
_TENDERNESS_PANGOCAIRO_BACKEND_VALUE = "fontconfig"
_TENDERNESS_FONTCONFIG_FILE_ENV = "FONTCONFIG_FILE"


class FontSetup:
    """Manages fontconfig and PangoCairo font environment setup."""

    manager_map: ClassVar[dict[SupportedPlatforms, type[BaseFontconfigManager]]] = {
        SupportedPlatforms.DARWIN: DarwinFontconfigManager,  # macOS
        SupportedPlatforms.LINUX: LinuxFontconfigManager,  # Linux
    }

    def __init__(self) -> None:
        self.detected_system = self._detect_supported_system()
        self.font_manager = self._get_fontconfig_manager()

    # --------------------------
    # Core
    # --------------------------

    def _detect_supported_system(self) -> SupportedPlatforms:
        system = platform.system()
        logger.debug("Detected system: %s", system)

        try:
            return SupportedPlatforms(system)
        except ValueError as unsupported_system:
            msg = f"Unsupported platform: '{system}'. Supported: {[p.name for p in SupportedPlatforms]}"
            raise NotImplementedError(msg) from unsupported_system

    def _get_fontconfig_manager(self) -> BaseFontconfigManager:
        manager_class = self.manager_map.get(self.detected_system)
        if manager_class is None:
            msg = f"No fontconfig manager for platform: {self.detected_system}"
            raise NotImplementedError(msg)

        return manager_class()

    # --------------------------
    # Mode wrappers
    # --------------------------

    def _load_from_file(self, fontconfig_path: pathlib.Path) -> pathlib.Path:
        return self.font_manager.load_fontconfig_file_from_path(fontconfig_path=fontconfig_path)

    def _copy_system_fontconfig_file(
        self,
        fontconfig_source_path: pathlib.Path,
        fontconfig_destination_dir: pathlib.Path,
    ) -> pathlib.Path:
        return self.font_manager.copy_fontconfig_file(
            fontconfig_source_path=fontconfig_source_path,
            fontconfig_destination_dir=fontconfig_destination_dir,
        )

    def _add_font_directory(
        self,
        fontconfig_source_path: pathlib.Path,
        fontconfig_destination_dir: pathlib.Path,
        font_dir: pathlib.Path,
    ) -> pathlib.Path:
        copy_path = self.font_manager.copy_fontconfig_file(
            fontconfig_source_path=fontconfig_source_path, fontconfig_destination_dir=fontconfig_destination_dir
        )
        return self.font_manager.add_font_directory(fontconfig_path=copy_path, font_dir=font_dir)

    def _add_font_directory_and_remove_system(
        self,
        fontconfig_source_path: pathlib.Path,
        fontconfig_destination_dir: pathlib.Path,
        font_dir: pathlib.Path,
    ) -> pathlib.Path:
        copy_path = self.font_manager.copy_fontconfig_file(
            fontconfig_source_path=fontconfig_source_path, fontconfig_destination_dir=fontconfig_destination_dir
        )
        return self.font_manager.add_font_directory_and_remove_system(fontconfig_path=copy_path, font_dir=font_dir)

    def _create_fontconfig_from_template(
        self,
        fontconfig_destination_dir: pathlib.Path,
        font_dir: pathlib.Path,
        mode: FontconfigMode,
    ) -> pathlib.Path:
        return self.font_manager.create_fontconfig_from_template(
            font_dir=font_dir, fontconfig_output_dir=fontconfig_destination_dir, mode=mode
        )

    # --------------------------
    # Fontconfig setup
    # --------------------------

    def _ordered_lib_names(self) -> list[str]:
        if self.detected_system == SupportedPlatforms.LINUX:
            names = _TENDERNESS_FONTCONFIG_LINUX_NAMES + _TENDERNESS_FONTCONFIG_DARWIN_NAMES
        else:
            names = _TENDERNESS_FONTCONFIG_DARWIN_NAMES + _TENDERNESS_FONTCONFIG_LINUX_NAMES
        return list(dict.fromkeys(names + _TENDERNESS_FONTCONFIG_GENERIC_NAMES))

    def _try_load(self, name: str) -> ctypes.CDLL | None:
        try:
            return ctypes.CDLL(name)
        except (OSError, TypeError):
            return None

    def _strategy_find_library(self) -> tuple[ctypes.CDLL, str] | None:
        # Strategy 1: Use ctypes.util.find_library
        lib_path = find_library("fontconfig")
        if not lib_path:
            return None
        logger.debug("Strategy 1: find_library found '%s'", lib_path)
        lib = self._try_load(lib_path)
        if lib is None:
            logger.warning("find_library found '%s' but ctypes could not load it", lib_path)
            return None
        return lib, lib_path

    def _strategy_dynamic_linker(self) -> tuple[ctypes.CDLL, str] | None:
        # Strategy 2: Try common names and let the dynamic linker find them.
        logger.debug("Strategy 2: trying common names via dynamic linker")
        for name in self._ordered_lib_names():
            logger.debug("Attempting to load '%s'", name)
            lib = self._try_load(name)
            if lib is not None:
                return lib, name
            logger.debug("Dynamic linker failed for '%s'", name)
        return None

    def _strategy_manual_search(self) -> tuple[ctypes.CDLL, str] | None:
        # Strategy 3: Manually search common directories (e.g., Homebrew, venv)
        logger.debug("Strategy 3: manually searching common library paths")
        for directory in _TENDERNESS_FONTCONFIG_SEARCH_DIRS:
            if not directory.is_dir():
                continue
            logger.debug("Searching in: %s", directory)
            for name in self._ordered_lib_names():
                candidate = directory / name
                if not candidate.is_file():
                    continue
                logger.debug("Found candidate: %s", candidate)
                lib = self._try_load(str(candidate))
                if lib is not None:
                    return lib, str(candidate)
                logger.warning("Found '%s' but failed to load it", candidate)
        return None

    def _find_and_load_fontconfig(self) -> tuple[ctypes.CDLL, str]:
        for strategy in (
            self._strategy_find_library,
            self._strategy_dynamic_linker,
            self._strategy_manual_search,
        ):
            result = strategy()
            if result is not None:
                lib, path = result
                logger.debug("Successfully loaded fontconfig from: %s", path)
                return lib, path

        msg = (
            "Could not find and load the fontconfig C library. Please ensure fontconfig "
            "is installed and accessible. Searched standard paths, Homebrew paths, "
            "and Python virtual environment paths."
        )
        raise RuntimeError(msg)

    def _reinitialize_fontconfig_cache(self) -> None:
        """Force the Fontconfig C-library to re-initialize and reread its configuration from environment variables."""
        fontconfig, lib_path = self._find_and_load_fontconfig()
        logger.debug("Successfully loaded fontconfig library from: %s", lib_path)

        fontconfig.FcInitReinitialize.restype = ctypes.c_int

        try:
            result = fontconfig.FcInitReinitialize()
        except Exception as e:
            msg = f"Failed to call FcInitReinitialize on library at '{lib_path}': {e}"
            raise RuntimeError(msg) from e

        if not result:
            msg = f"FcInitReinitialize returned failure for library at '{lib_path}'"
            raise RuntimeError(msg)

        logger.debug("Successfully called FcInitReinitialize.")

    def _configure_environment(self, result_path: pathlib.Path, *, force_reinitialize: bool = True) -> None:
        os.environ[_TENDERNESS_PANGOCAIRO_BACKEND_ENV] = _TENDERNESS_PANGOCAIRO_BACKEND_VALUE
        os.environ[_TENDERNESS_FONTCONFIG_FILE_ENV] = str(result_path)
        logger.debug(
            "Set environment variables for %s: %s=%s, %s=%s",
            self.detected_system,
            _TENDERNESS_PANGOCAIRO_BACKEND_ENV,
            os.environ[_TENDERNESS_PANGOCAIRO_BACKEND_ENV],
            _TENDERNESS_FONTCONFIG_FILE_ENV,
            os.environ[_TENDERNESS_FONTCONFIG_FILE_ENV],
        )
        # after setting the environment, force the underlying C library to re-read it
        # this is crucial for applications/tests that switch font configs in a single process
        if force_reinitialize:
            self._reinitialize_fontconfig_cache()

            new_font_map = PangoCairo.FontMap.new()
            PangoCairo.FontMap.set_default(new_font_map)  # type: ignore
            logger.debug("Set new PangoCairo default FontMap to clear font cache.")

    # --------------------------
    # Public API
    # --------------------------

    def _setup_font_by_mode(  # noqa: C901
        self,
        mode: FontconfigMode,
        fontconfig_source_path: pathlib.Path | None,
        fontconfig_destination_dir: pathlib.Path,
        font_dir: pathlib.Path | None,
    ) -> pathlib.Path:
        match mode:
            case FontconfigMode.FROM_FILE:
                if fontconfig_source_path is None:
                    msg = f"{mode} requires 'fontconfig_source_path'"
                    raise ValueError(msg)
                return self._load_from_file(fontconfig_path=fontconfig_source_path)

            case FontconfigMode.SYSTEM_COPY:
                if fontconfig_source_path is None:
                    msg = f"{mode} requires 'fontconfig_source_path' and 'fontconfig_destination_dir'"
                    raise ValueError(msg)
                return self._copy_system_fontconfig_file(
                    fontconfig_source_path=fontconfig_source_path,
                    fontconfig_destination_dir=fontconfig_destination_dir,
                )

            case FontconfigMode.SYSTEM_EXTENDED:
                if fontconfig_source_path is None or font_dir is None:
                    msg = f"{mode} requires 'fontconfig_source_path', 'fontconfig_destination_dir', and 'font_dir'"
                    raise ValueError(msg)
                return self._add_font_directory(
                    fontconfig_source_path=fontconfig_source_path,
                    fontconfig_destination_dir=fontconfig_destination_dir,
                    font_dir=font_dir,
                )

            case FontconfigMode.SYSTEM_ISOLATED:
                if fontconfig_source_path is None or font_dir is None:
                    msg = f"{mode} requires 'fontconfig_source_path', 'fontconfig_destination_dir', and 'font_dir'"
                    raise ValueError(msg)
                return self._add_font_directory_and_remove_system(
                    fontconfig_source_path=fontconfig_source_path,
                    fontconfig_destination_dir=fontconfig_destination_dir,
                    font_dir=font_dir,
                )

            case FontconfigMode.TEMPLATE_MINIMAL:
                if font_dir is None:
                    msg = f"{mode} requires 'fontconfig_destination_dir' and 'font_dir'"
                    raise ValueError(msg)
                return self._create_fontconfig_from_template(
                    fontconfig_destination_dir=fontconfig_destination_dir,
                    font_dir=font_dir,
                    mode=mode,
                )

            case _:
                msg = f"Unsupported FontconfigMode: {mode}"
                raise ValueError(msg)

    def setup_font(
        self,
        mode: FontconfigMode,
        fontconfig_source_path: pathlib.Path | str | None = None,
        font_dir: pathlib.Path | str | None = None,
        fontconfig_destination_dir: pathlib.Path | str = TENDERNESS_FONTCONFIGS_DIR,
        *,
        force_reinitialize: bool = True,
    ) -> pathlib.Path:
        """Set up fontconfig and apply it to the PangoCairo environment.

        Parameters
        ----------
        mode
            Fontconfig setup strategy to use.
        fontconfig_source_path
            Path to an existing fontconfig file; required for some modes.
        font_dir
            Custom font directory to register; required for some modes.
        fontconfig_destination_dir
            Directory where generated fontconfig files are written.
        force_reinitialize
            Force the Fontconfig C-library to re-initialize after setup.

        Raises
        ------
        ValueError
            If a required parameter is missing for the selected mode.
        """
        if isinstance(fontconfig_source_path, str):
            fontconfig_source_path = pathlib.Path(fontconfig_source_path)
        if isinstance(font_dir, str):
            font_dir = pathlib.Path(font_dir)
        if isinstance(fontconfig_destination_dir, str):
            fontconfig_destination_dir = pathlib.Path(fontconfig_destination_dir)

        result_path = self._setup_font_by_mode(
            mode=mode,
            fontconfig_source_path=fontconfig_source_path,
            fontconfig_destination_dir=fontconfig_destination_dir,
            font_dir=font_dir,
        )

        # configure environment variables
        self._configure_environment(result_path=result_path, force_reinitialize=force_reinitialize)

        return result_path

    def get_all_font_families(self) -> list[str]:
        """Return all available font family names from the default PangoCairo font map."""
        font_map = PangoCairo.FontMap.get_default()
        # font_map = PangoCairo.font_map_get_default()
        # font_map = PangoCairo.FontMap.new()
        families = font_map.list_families()
        font_family_names = [family.get_name() for family in families]
        logger.debug("Total font families available: %d", len(font_family_names))
        return font_family_names

    def is_font_family_available(self, family_name: str) -> bool:
        """Return True if family_name is available in the current PangoCairo font map.

        Parameters
        ----------
        family_name
            Font family name to check.
        """
        available_families = self.get_all_font_families()
        is_available = family_name in available_families
        logger.debug("Font family '%s' availability: %s", family_name, is_available)
        return is_available
