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

"""Fontconfig operation modes and platform-specific manager classes."""

from __future__ import annotations

import logging
import shutil
from abc import ABC, abstractmethod
from enum import StrEnum, auto, unique
from typing import TYPE_CHECKING, ClassVar

from lxml import etree

from tenderness.font_setup.fontconfig_templates import (
    DARWIN_FONTCONFIG_REMOVE_SYSTEM_FONTS_PATTERNS,
    DARWIN_FONTCONFIG_TEMPLATE_CONFIG_MINIMAL,
    LINUX_FONTCONFIG_REMOVE_SYSTEM_FONTS_PATTERNS,
    LINUX_FONTCONFIG_TEMPLATE_CONFIG_MINIMAL,
)

if TYPE_CHECKING:
    import pathlib
    from string import Template


logger = logging.getLogger(__name__)


@unique
class FontconfigMode(StrEnum):
    """Fontconfig setup strategies."""

    FROM_FILE = auto()  # use existing fontconfig file without modifications
    SYSTEM_COPY = auto()  # use system fontconfig
    SYSTEM_EXTENDED = auto()  # use system fontconfig with custom font directory
    SYSTEM_ISOLATED = auto()  # use system fontconfig with custom font directory and no system fonts
    TEMPLATE_MINIMAL = auto()  # use template (minimal) fontconfig only with custom font directory


class BaseFontconfigManager(ABC):
    """Base class for fontconfig file operations."""

    fontconfig_extension: ClassVar[str] = ".conf"

    @property
    @abstractmethod
    def remove_system_fonts_patterns(self) -> tuple[str, ...]:
        """Directory path prefixes used to identify and remove system fonts."""
        ...

    @property
    @abstractmethod
    def template_map(self) -> dict[FontconfigMode, Template]:
        """Mapping from FontconfigMode to the corresponding config template."""
        ...

    def _parse_xml_config_file(self, fontconfig_path: pathlib.Path) -> etree._ElementTree:
        logger.debug("Parsing XML fontconfig file: %s", fontconfig_path)
        return etree.parse(str(fontconfig_path))

    def _write_xml_config_file(self, fontconfig_path: pathlib.Path, tree: etree._ElementTree) -> None:
        logger.debug("Writing XML fontconfig file to: %s", fontconfig_path)
        etree.indent(tree, space="\t")
        tree.write(str(fontconfig_path), encoding="utf-8", xml_declaration=True, pretty_print=True)

    def _validate_conf_file_existence(self, file_path: pathlib.Path) -> None:
        if not file_path.is_file() or file_path.suffix != self.fontconfig_extension:
            msg_no_conf_file = f"No {self.fontconfig_extension} file found at {file_path}"
            raise FileNotFoundError(msg_no_conf_file)

    def _insert_font_dir(self, tree: etree._ElementTree, font_dir: pathlib.Path) -> etree._ElementTree:
        root = tree.getroot()

        dir_element = etree.Element("dir")
        dir_element.text = str(font_dir)

        # attempt #1: insert after <description></description>
        description_element = root.find("description")
        if description_element is not None:
            description_element.addnext(dir_element)
        # attempt #2: insert at the beginning if root tag is <fontconfig>
        elif root.tag == "fontconfig":
            root.insert(0, dir_element)
        else:
            msg_fail = "Failed to insert <dir> element: 1) <description> not found, 2) root tag is not <fontconfig>"
            raise ValueError(msg_fail)
        return tree

    def _remove_system_fonts(self, tree: etree._ElementTree) -> etree._ElementTree:
        root = tree.getroot()

        dirs_to_remove = []
        for dir_element in root.xpath("//dir"):
            dir_text = dir_element.text.strip() if dir_element.text else ""

            # check text patterns or xdg prefix attribute (like <dir prefix="xdg">fonts</dir>)
            if (
                any(dir_text.startswith(pattern) for pattern in self.remove_system_fonts_patterns)
                or dir_element.get("prefix") == "xdg"
            ):
                dirs_to_remove.append(dir_element)

        for dir_element in dirs_to_remove:
            parent = dir_element.getparent()
            if parent is not None:
                parent.remove(dir_element)

        return tree

    def load_fontconfig_file_from_path(self, fontconfig_path: pathlib.Path) -> pathlib.Path:
        """Load existing fontconfig file from the specified path."""
        result_path = fontconfig_path.resolve()
        self._validate_conf_file_existence(file_path=result_path)

        try:
            tree = self._parse_xml_config_file(fontconfig_path=result_path)
            if tree.getroot().tag != "fontconfig":
                msg_invalid_root = f"Invalid root element in fontconfig file: {tree.getroot().tag}"
                raise ValueError(msg_invalid_root)
        except (etree.XMLSyntaxError, etree.ParseError) as e:
            msg_invalid_xml = f"Invalid XML in fontconfig file: {e}"
            raise ValueError(msg_invalid_xml) from e

        logger.debug("Loading fontconfig from path: %s", result_path)
        return result_path

    def copy_fontconfig_file(
        self, fontconfig_source_path: pathlib.Path, fontconfig_destination_dir: pathlib.Path
    ) -> pathlib.Path:
        """Copy fontconfig file from source to output directory."""
        logger.debug("Copying fontconfig file from %s to %s", fontconfig_source_path, fontconfig_destination_dir)

        fontconfig_source_path = fontconfig_source_path.resolve()
        self._validate_conf_file_existence(file_path=fontconfig_source_path)

        fontconfig_destination_dir.mkdir(parents=True, exist_ok=True)
        result_path = (
            fontconfig_destination_dir.joinpath(FontconfigMode.SYSTEM_COPY)
            .with_suffix(self.fontconfig_extension)
            .resolve()
        )
        shutil.copy(fontconfig_source_path, result_path)
        logger.debug("Fontconfig copied to: %s", result_path)
        return result_path

    def add_font_directory(self, fontconfig_path: pathlib.Path, font_dir: pathlib.Path) -> pathlib.Path:
        """Add custom font directory to the fontconfig file."""
        fontconfig_path = fontconfig_path.resolve()
        self._validate_conf_file_existence(file_path=fontconfig_path)
        font_dir = font_dir.resolve()

        logger.debug("Adding font directory %s to config %s", font_dir, fontconfig_path)

        tree = self._parse_xml_config_file(fontconfig_path=fontconfig_path)
        tree = self._insert_font_dir(tree=tree, font_dir=font_dir)
        result_path = (
            fontconfig_path.parent.joinpath(FontconfigMode.SYSTEM_EXTENDED)
            .with_suffix(self.fontconfig_extension)
            .resolve()
        )
        self._write_xml_config_file(fontconfig_path=result_path, tree=tree)
        logger.debug("New fontconfig created at: %s", result_path)
        return result_path

    def add_font_directory_and_remove_system(
        self, fontconfig_path: pathlib.Path, font_dir: pathlib.Path
    ) -> pathlib.Path:
        """Add custom font directory and remove system fonts."""
        fontconfig_path = fontconfig_path.resolve()
        self._validate_conf_file_existence(file_path=fontconfig_path)
        font_dir = font_dir.resolve()

        logger.debug("Adding font directory %s and removing system fonts from %s", font_dir, fontconfig_path)

        tree = self._parse_xml_config_file(fontconfig_path=fontconfig_path)
        tree = self._remove_system_fonts(tree=tree)
        tree = self._insert_font_dir(tree=tree, font_dir=font_dir)

        result_path = (
            fontconfig_path.parent.joinpath(FontconfigMode.SYSTEM_ISOLATED)
            .with_suffix(self.fontconfig_extension)
            .resolve()
        )
        self._write_xml_config_file(fontconfig_path=result_path, tree=tree)
        logger.debug("New fontconfig created at: %s", result_path)
        return result_path

    def create_fontconfig_from_template(
        self, font_dir: pathlib.Path, fontconfig_output_dir: pathlib.Path, mode: FontconfigMode
    ) -> pathlib.Path:
        """Create fontconfig file from a predefined template."""
        font_dir = font_dir.resolve()
        fontconfig_output_dir = fontconfig_output_dir.resolve()

        if mode not in self.template_map:
            msg_error_mode = f"Unsupported template mode: {mode}"
            raise ValueError(msg_error_mode)

        logger.debug("Creating fontconfig with mode %s and font directory %s", mode, font_dir)

        template = self.template_map[mode]
        config_content = template.substitute(font_dir=str(font_dir))

        root = etree.fromstring(config_content.encode("utf-8"))
        tree = etree.ElementTree(root)

        fontconfig_output_dir.mkdir(parents=True, exist_ok=True)
        result_path = fontconfig_output_dir.joinpath(mode).with_suffix(self.fontconfig_extension).resolve()
        self._write_xml_config_file(fontconfig_path=result_path, tree=tree)
        logger.debug("Fontconfig created at: %s", result_path)
        return result_path


class DarwinFontconfigManager(BaseFontconfigManager):
    """Darwin-specific fontconfig manager."""

    @property
    def remove_system_fonts_patterns(self) -> tuple[str, ...]:
        """Directory path prefixes used to identify and remove macOS system fonts."""
        return DARWIN_FONTCONFIG_REMOVE_SYSTEM_FONTS_PATTERNS

    @property
    def template_map(self) -> dict[FontconfigMode, Template]:
        """Mapping from FontconfigMode to the macOS config template."""
        return {FontconfigMode.TEMPLATE_MINIMAL: DARWIN_FONTCONFIG_TEMPLATE_CONFIG_MINIMAL}


class LinuxFontconfigManager(BaseFontconfigManager):
    """Linux-specific fontconfig manager."""

    @property
    def remove_system_fonts_patterns(self) -> tuple[str, ...]:
        """Directory path prefixes used to identify and remove Linux system fonts."""
        return LINUX_FONTCONFIG_REMOVE_SYSTEM_FONTS_PATTERNS

    @property
    def template_map(self) -> dict[FontconfigMode, Template]:
        """Mapping from FontconfigMode to the Linux config template."""
        return {FontconfigMode.TEMPLATE_MINIMAL: LINUX_FONTCONFIG_TEMPLATE_CONFIG_MINIMAL}
