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

from typing import TYPE_CHECKING

import pytest

from tenderness.font_setup.font_setup import FontSetup
from tenderness.font_setup.fontconfig_managers import FontconfigMode
from tests._test_utils.paths_test import TEST_FONTS_DIR

if TYPE_CHECKING:
    import pathlib
    from collections.abc import Iterator


# --------------------------
# Tests for get/set_font_map_resolution
# --------------------------
class TestFontSetupFontMapResolution:
    @pytest.fixture
    def font_setup(self) -> FontSetup:
        return FontSetup()

    @pytest.fixture(autouse=True)
    def restore_resolution(self, font_setup: FontSetup) -> Iterator[None]:
        original = font_setup.get_font_map_resolution()
        yield
        font_setup.set_font_map_resolution(original)

    def test_get_returns_float(self, font_setup: FontSetup) -> None:
        assert isinstance(font_setup.get_font_map_resolution(), float)

    def test_get_default_is_positive(self, font_setup: FontSetup) -> None:
        assert font_setup.get_font_map_resolution() > 0

    def test_set_and_get_roundtrip(self, font_setup: FontSetup) -> None:
        font_setup.set_font_map_resolution(72.0)
        assert font_setup.get_font_map_resolution() == 72.0

    def test_set_144_dpi(self, font_setup: FontSetup) -> None:
        font_setup.set_font_map_resolution(144.0)
        assert font_setup.get_font_map_resolution() == 144.0

    def test_two_instances_share_global_state(self) -> None:
        a = FontSetup()
        b = FontSetup()
        a.set_font_map_resolution(72.0)
        assert b.get_font_map_resolution() == 72.0


# --------------------------
# Tests for setup_font resolution= parameter
# --------------------------
class TestFontSetupResolutionParam:
    @pytest.fixture
    def font_setup(self) -> FontSetup:
        return FontSetup()

    @pytest.fixture(autouse=True)
    def restore_resolution(self, font_setup: FontSetup) -> Iterator[None]:
        original = font_setup.get_font_map_resolution()
        yield
        font_setup.set_font_map_resolution(original)

    def test_resolution_applied_to_new_font_map(self, font_setup: FontSetup, tmp_path: pathlib.Path) -> None:
        font_setup.setup_font(
            mode=FontconfigMode.TEMPLATE_MINIMAL,
            font_dir=TEST_FONTS_DIR,
            fontconfig_destination_dir=tmp_path,
            resolution=144.0,
        )
        assert font_setup.get_font_map_resolution() == 144.0

    def test_resolution_none_leaves_default_positive(self, font_setup: FontSetup, tmp_path: pathlib.Path) -> None:
        font_setup.setup_font(
            mode=FontconfigMode.TEMPLATE_MINIMAL,
            font_dir=TEST_FONTS_DIR,
            fontconfig_destination_dir=tmp_path,
        )
        assert font_setup.get_font_map_resolution() > 0

    def test_resolution_applied_without_reinitialize(self, font_setup: FontSetup, tmp_path: pathlib.Path) -> None:
        fontconfig_path = font_setup.setup_font(
            mode=FontconfigMode.TEMPLATE_MINIMAL,
            font_dir=TEST_FONTS_DIR,
            fontconfig_destination_dir=tmp_path,
        )
        font_setup.setup_font(
            mode=FontconfigMode.FROM_FILE,
            fontconfig_source_path=fontconfig_path,
            fontconfig_destination_dir=tmp_path,
            force_reinitialize=False,
            resolution=72.0,
        )
        assert font_setup.get_font_map_resolution() == 72.0
