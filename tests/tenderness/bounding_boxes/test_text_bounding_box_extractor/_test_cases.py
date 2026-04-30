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

from dataclasses import dataclass

import gi

from tenderness.bounding_boxes.bounding_boxes_schema import (
    BoundingBoxStrategy,
    BoundingBoxType,
)

gi.require_version("Pango", "1.0")
from gi.repository import Pango  # noqa: E402


@dataclass(frozen=True)
class LevelsTestCase:
    test_name: str
    levels: set[BoundingBoxType] | None
    expected_char: bool
    expected_cluster: bool
    expected_run: bool
    expected_line: bool
    expected_layout: bool


LEVELS_TEST_CASES = [
    LevelsTestCase(
        test_name="all levels default",
        levels=None,
        expected_char=True,
        expected_cluster=True,
        expected_run=True,
        expected_line=True,
        expected_layout=True,
    ),
    LevelsTestCase(
        test_name="only line",
        levels={BoundingBoxType.LINE},
        expected_char=False,
        expected_cluster=False,
        expected_run=False,
        expected_line=True,
        expected_layout=False,
    ),
    LevelsTestCase(
        test_name="only layout",
        levels={BoundingBoxType.LAYOUT},
        expected_char=False,
        expected_cluster=False,
        expected_run=False,
        expected_line=False,
        expected_layout=True,
    ),
    LevelsTestCase(
        test_name="char and cluster",
        levels={BoundingBoxType.CHAR, BoundingBoxType.CLUSTER},
        expected_char=True,
        expected_cluster=True,
        expected_run=False,
        expected_line=False,
        expected_layout=False,
    ),
    LevelsTestCase(
        test_name="empty set",
        levels=set(),
        expected_char=False,
        expected_cluster=False,
        expected_run=False,
        expected_line=False,
        expected_layout=False,
    ),
]


@dataclass(frozen=True)
class StrategyTestCase:
    test_name: str
    text_mode: BoundingBoxStrategy
    level: BoundingBoxType
    expect_text_none: bool


STRATEGY_TEST_CASES = [
    StrategyTestCase(
        test_name="with_text char",
        text_mode=BoundingBoxStrategy.WITH_TEXT,
        level=BoundingBoxType.CHAR,
        expect_text_none=False,
    ),
    StrategyTestCase(
        test_name="only_boxes char",
        text_mode=BoundingBoxStrategy.ONLY_BOXES,
        level=BoundingBoxType.CHAR,
        expect_text_none=True,
    ),
    StrategyTestCase(
        test_name="with_text line",
        text_mode=BoundingBoxStrategy.WITH_TEXT,
        level=BoundingBoxType.LINE,
        expect_text_none=False,
    ),
    StrategyTestCase(
        test_name="only_boxes line",
        text_mode=BoundingBoxStrategy.ONLY_BOXES,
        level=BoundingBoxType.LINE,
        expect_text_none=True,
    ),
    StrategyTestCase(
        test_name="with_text layout",
        text_mode=BoundingBoxStrategy.WITH_TEXT,
        level=BoundingBoxType.LAYOUT,
        expect_text_none=False,
    ),
    StrategyTestCase(
        test_name="only_boxes layout",
        text_mode=BoundingBoxStrategy.ONLY_BOXES,
        level=BoundingBoxType.LAYOUT,
        expect_text_none=True,
    ),
]


@dataclass(frozen=True)
class CharTextTestCase:
    test_name: str
    text: str
    expected_joined: str


CHAR_TEXT_TEST_CASES = [
    CharTextTestCase(test_name="ascii", text="Hi", expected_joined="Hi"),
    CharTextTestCase(test_name="multibyte", text="αβ", expected_joined="αβ"),
    CharTextTestCase(test_name="single char", text="A", expected_joined="A"),
    CharTextTestCase(test_name="cjk", text="你好", expected_joined="你好"),
]


@dataclass(frozen=True)
class CharByteIndexTestCase:
    test_name: str
    text: str
    expected_first_index: int
    expected_second_index: int


CHAR_BYTE_INDEX_TEST_CASES = [
    CharByteIndexTestCase(test_name="ascii 1-byte", text="AB", expected_first_index=0, expected_second_index=1),
    CharByteIndexTestCase(test_name="greek 2-byte", text="αβ", expected_first_index=0, expected_second_index=2),
    CharByteIndexTestCase(test_name="cjk 3-byte", text="你好", expected_first_index=0, expected_second_index=3),
]


@dataclass(frozen=True)
class ClusterTextTestCase:
    test_name: str
    text: str
    expected_combined: str


CLUSTER_TEXT_TEST_CASES = [
    ClusterTextTestCase(test_name="ascii", text="Hi", expected_combined="Hi"),
    ClusterTextTestCase(test_name="multibyte", text="αβ", expected_combined="αβ"),
    ClusterTextTestCase(test_name="emoji", text="👋🌍", expected_combined="👋🌍"),
]


@dataclass(frozen=True)
class LineCountTestCase:
    test_name: str
    text: str
    expected_count: int


LINE_COUNT_TEST_CASES = [
    LineCountTestCase(test_name="single line", text="Hello", expected_count=1),
    LineCountTestCase(test_name="explicit newline", text="Hello\nWorld", expected_count=2),
    LineCountTestCase(test_name="two newlines", text="A\nB\nC", expected_count=3),
]


@dataclass(frozen=True)
class LineParagraphStartTestCase:
    test_name: str
    text: str
    expected_first_is_paragraph_start: bool


LINE_PARAGRAPH_START_TEST_CASES = [
    LineParagraphStartTestCase(
        test_name="single line",
        text="Hello",
        expected_first_is_paragraph_start=True,
    ),
    LineParagraphStartTestCase(
        test_name="two paragraphs",
        text="Hello\nWorld",
        expected_first_is_paragraph_start=True,
    ),
]


@dataclass(frozen=True)
class LineDirectionTestCase:
    test_name: str
    text: str
    expected_direction: Pango.Direction


LINE_DIRECTION_TEST_CASES = [
    LineDirectionTestCase(test_name="ltr english", text="Hello", expected_direction=Pango.Direction.LTR),
    LineDirectionTestCase(test_name="rtl arabic", text="مرحبا", expected_direction=Pango.Direction.RTL),
    LineDirectionTestCase(test_name="rtl hebrew", text="שלום", expected_direction=Pango.Direction.RTL),
]


@dataclass(frozen=True)
class LineTextTestCase:
    test_name: str
    text: str
    expected_texts: list[str]


LINE_TEXT_TEST_CASES = [
    LineTextTestCase(test_name="single line", text="Hello", expected_texts=["Hello"]),
    LineTextTestCase(test_name="two lines", text="Hello\nWorld", expected_texts=["Hello", "World"]),
    LineTextTestCase(test_name="three lines", text="A\nB\nC", expected_texts=["A", "B", "C"]),
]


@dataclass(frozen=True)
class RunBidiTestCase:
    test_name: str
    text: str
    expected_min_runs: int


RUN_BIDI_TEST_CASES = [
    RunBidiTestCase(test_name="pure ltr", text="Hello", expected_min_runs=1),
    RunBidiTestCase(test_name="rtl arabic", text="مرحبا", expected_min_runs=1),
    RunBidiTestCase(test_name="ltr + rtl", text="Hello مرحبا", expected_min_runs=2),
    RunBidiTestCase(test_name="ltr + rtl + ltr", text="Hi مرحبا world", expected_min_runs=2),
]


@dataclass(frozen=True)
class ScriptLineDirectionTestCase:
    test_name: str
    text: str
    expected_direction: Pango.Direction


SCRIPT_LINE_DIRECTION_TEST_CASES = [
    # --- LTR ---
    ScriptLineDirectionTestCase(test_name="ltr_english", text="Hello world", expected_direction=Pango.Direction.LTR),
    ScriptLineDirectionTestCase(test_name="ltr_spanish", text="¡Hola mundo!", expected_direction=Pango.Direction.LTR),
    ScriptLineDirectionTestCase(test_name="ltr_hindi", text="नमस्ते दुनिया", expected_direction=Pango.Direction.LTR),
    ScriptLineDirectionTestCase(test_name="ltr_thai", text="สวัสดีชาวโลก", expected_direction=Pango.Direction.LTR),
    ScriptLineDirectionTestCase(
        test_name="ltr_japanese", text="こんにちは世界", expected_direction=Pango.Direction.LTR
    ),
    ScriptLineDirectionTestCase(test_name="ltr_chinese", text="你好，世界", expected_direction=Pango.Direction.LTR),  # noqa: RUF001
    # --- RTL ---
    ScriptLineDirectionTestCase(test_name="rtl_arabic", text="مرحبا بالعالم", expected_direction=Pango.Direction.RTL),
    ScriptLineDirectionTestCase(test_name="rtl_hebrew", text="שלום עולם", expected_direction=Pango.Direction.RTL),
    # --- Vertical (gravity EAST) ---
    # Vertical CJK — gravity EAST or WEST does not change resolved_direction
    # (direction is still LTR for CJK), but confirms the layout processes correctly
    ScriptLineDirectionTestCase(
        test_name="vertical_japanese_east", text="こんにちは世界", expected_direction=Pango.Direction.LTR
    ),
    ScriptLineDirectionTestCase(
        test_name="vertical_chinese_east",
        text="你好，世界",  # noqa: RUF001
        expected_direction=Pango.Direction.LTR,
    ),
]


@dataclass(frozen=True)
class ScriptRunCountTestCase:
    test_name: str
    text: str
    expected_min_runs: int


SCRIPT_RUN_COUNT_TEST_CASES = [
    ScriptRunCountTestCase(test_name="ltr_english", text="Hello", expected_min_runs=1),
    ScriptRunCountTestCase(test_name="rtl_arabic", text="مرحبا", expected_min_runs=1),
    ScriptRunCountTestCase(test_name="rtl_hebrew", text="שלום", expected_min_runs=1),
    ScriptRunCountTestCase(test_name="bidi_en_ar", text="Hello مرحبا", expected_min_runs=2),
    ScriptRunCountTestCase(test_name="bidi_en_he", text="Hello שלום", expected_min_runs=2),
    ScriptRunCountTestCase(test_name="bidi_en_ar_en", text="Hi مرحبا world", expected_min_runs=2),
    ScriptRunCountTestCase(test_name="bidi_en_he_numeric", text="ABC אבג 123", expected_min_runs=2),
]


@dataclass(frozen=True)
class BBoxOrderTestCase:
    test_name: str
    text: str
    lines_monotone_byte_start: bool


BBOX_ORDER_TEST_CASES = [
    BBoxOrderTestCase(
        test_name="ltr_multiline",
        text="First line\nSecond line\nThird line",
        lines_monotone_byte_start=True,
    ),
    BBoxOrderTestCase(
        test_name="rtl_multiline",
        text="مرحبا\nكيف حالك\nأتمنى لك",
        lines_monotone_byte_start=True,
    ),
    BBoxOrderTestCase(
        test_name="bidi_multiline",
        text="Hello مرحبا\nשלום world",  # noqa: RUF001
        lines_monotone_byte_start=True,
    ),
]


@dataclass(frozen=True)
class TextReconstructionTestCase:
    test_name: str
    text: str
    level: BoundingBoxType


TEXT_RECONSTRUCTION_TEST_CASES = [
    # --- LTR ---
    TextReconstructionTestCase(test_name="ltr_cluster", text="Hello", level=BoundingBoxType.CLUSTER),
    TextReconstructionTestCase(test_name="ltr_run", text="Hello", level=BoundingBoxType.RUN),
    TextReconstructionTestCase(test_name="ltr_line", text="Hello\nWorld", level=BoundingBoxType.LINE),
    # --- RTL ---
    TextReconstructionTestCase(test_name="rtl_cluster", text="مرحبا", level=BoundingBoxType.CLUSTER),
    TextReconstructionTestCase(test_name="rtl_run", text="مرحبا", level=BoundingBoxType.RUN),
    TextReconstructionTestCase(test_name="rtl_line", text="مرحبا\nשלום", level=BoundingBoxType.LINE),  # noqa: RUF001
    # --- Bidi ---
    TextReconstructionTestCase(test_name="bidi_cluster", text="Hello مرحبا", level=BoundingBoxType.CLUSTER),
    TextReconstructionTestCase(test_name="bidi_run", text="Hello مرحبا", level=BoundingBoxType.RUN),
    TextReconstructionTestCase(test_name="bidi_line", text="Hello\nمرحبا", level=BoundingBoxType.LINE),  # noqa: RUF001
    # --- Multibyte / complex scripts ---
    TextReconstructionTestCase(test_name="hindi_cluster", text="नमस्ते", level=BoundingBoxType.CLUSTER),
    TextReconstructionTestCase(test_name="emoji_cluster", text="👋🌍", level=BoundingBoxType.CLUSTER),
    TextReconstructionTestCase(test_name="cjk_cluster", text="你好世界", level=BoundingBoxType.CLUSTER),
    TextReconstructionTestCase(test_name="thai_cluster", text="สวัสดี", level=BoundingBoxType.CLUSTER),
    # --- Vertical ---
    TextReconstructionTestCase(test_name="vertical_japanese_cluster", text="こんにちは", level=BoundingBoxType.CLUSTER),
    TextReconstructionTestCase(test_name="vertical_chinese_cluster", text="你好世界", level=BoundingBoxType.CLUSTER),
    TextReconstructionTestCase(
        test_name="vertical_japanese_line", text="こんにちは\n世界です", level=BoundingBoxType.LINE
    ),
]


@dataclass(frozen=True)
class VerticalLayoutTestCase:
    test_name: str
    text: str
    gravity: Pango.Gravity
    expected_line_count: int


VERTICAL_LAYOUT_TEST_CASES = [
    VerticalLayoutTestCase(
        test_name="japanese_east_single_line",
        text="こんにちは世界",
        gravity=Pango.Gravity.EAST,
        expected_line_count=1,
    ),
    VerticalLayoutTestCase(
        test_name="japanese_east_multiline",
        text="こんにちは\n世界です",
        gravity=Pango.Gravity.EAST,
        expected_line_count=2,
    ),
    VerticalLayoutTestCase(
        test_name="chinese_east_single_line",
        text="你好世界",
        gravity=Pango.Gravity.EAST,
        expected_line_count=1,
    ),
    VerticalLayoutTestCase(
        test_name="japanese_west_single_line",
        text="こんにちは世界",
        gravity=Pango.Gravity.WEST,
        expected_line_count=1,
    ),
    VerticalLayoutTestCase(
        test_name="chinese_west_multiline",
        text="你好\n世界",
        gravity=Pango.Gravity.WEST,
        expected_line_count=2,
    ),
]
