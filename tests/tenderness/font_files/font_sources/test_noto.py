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

from tenderness.font_files.font_sources.noto import (
    _BW_EMOJI_NOTO_SANS,
    _COLOR_EMOJI_NOTO_SANS,
    _COMMON_NOTO_SANS,
    _LESS_COMMON_NOTO_SANS,
    _NOTO_COMMIT,
    _RARE_NOTO_SANS,
    _SIGNWRITING_NOTO_SANS,
    _SYMBOLS_NOTO_SANS,
    FONTS_NOTO_SANS,
    FONTS_NOTO_SANS_BW,
    FONTS_NOTO_SANS_MINIMAL,
)


class TestFontsNotoSans:
    def test_all_urls_contain_commit(self) -> None:
        for source in FONTS_NOTO_SANS:
            assert _NOTO_COMMIT in source.url

    def test_color_and_bw_differ(self) -> None:
        assert FONTS_NOTO_SANS != FONTS_NOTO_SANS_BW

    def test_minimal_is_subset_of_full(self) -> None:
        full_urls = {s.url for s in FONTS_NOTO_SANS}
        minimal_urls = {s.url for s in FONTS_NOTO_SANS_MINIMAL}
        assert minimal_urls.issubset(full_urls)

    def test_minimal_smaller_than_full(self) -> None:
        assert len(FONTS_NOTO_SANS_MINIMAL) < len(FONTS_NOTO_SANS)

    def test_color_and_bw_emoji_are_mutually_exclusive(self) -> None:
        color_urls = {s.url for s in _COLOR_EMOJI_NOTO_SANS}
        bw_urls = {s.url for s in _BW_EMOJI_NOTO_SANS}
        assert color_urls.isdisjoint(bw_urls)

    def test_common_fonts_in_all_variants(self) -> None:
        common_urls = {s.url for s in _COMMON_NOTO_SANS}
        for variant in (FONTS_NOTO_SANS, FONTS_NOTO_SANS_BW, FONTS_NOTO_SANS_MINIMAL):
            variant_urls = {s.url for s in variant}
            assert common_urls.issubset(variant_urls)

    def test_less_common_in_full_not_minimal(self) -> None:
        less_common_urls = {s.url for s in _LESS_COMMON_NOTO_SANS}
        assert less_common_urls.issubset({s.url for s in FONTS_NOTO_SANS})
        assert less_common_urls.isdisjoint({s.url for s in FONTS_NOTO_SANS_MINIMAL})

    def test_rare_in_full_not_minimal(self) -> None:
        rare_urls = {s.url for s in _RARE_NOTO_SANS}
        assert rare_urls.issubset({s.url for s in FONTS_NOTO_SANS})
        assert rare_urls.isdisjoint({s.url for s in FONTS_NOTO_SANS_MINIMAL})

    def test_symbols_in_full_not_minimal(self) -> None:
        symbols_urls = {s.url for s in _SYMBOLS_NOTO_SANS}
        assert symbols_urls.issubset({s.url for s in FONTS_NOTO_SANS})
        assert symbols_urls.isdisjoint({s.url for s in FONTS_NOTO_SANS_MINIMAL})

    def test_signwriting_in_full_not_minimal(self) -> None:
        signwriting_urls = {s.url for s in _SIGNWRITING_NOTO_SANS}
        assert signwriting_urls.issubset({s.url for s in FONTS_NOTO_SANS})
        assert signwriting_urls.isdisjoint({s.url for s in FONTS_NOTO_SANS_MINIMAL})
