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

from tenderness.font_files.font_sources.honk import _HONK, _HONK_COMMIT, FONTS_HONK


class TestFontsHONK:
    def test_fonts_is_list(self) -> None:
        assert isinstance(FONTS_HONK, list)
        assert len(FONTS_HONK) > 0

    def test_fonts_equals_validated_source(self) -> None:
        assert FONTS_HONK == _HONK

    def test_all_urls_contain_commit(self) -> None:
        for source in FONTS_HONK:
            assert _HONK_COMMIT in source.url
