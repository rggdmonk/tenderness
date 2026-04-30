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

import cairo
import gi
import pytest

from tenderness.bounding_boxes.bounding_boxes_schema import (
    BoundingBoxStrategy,
    BoundingBoxType,
)
from tenderness.bounding_boxes.text_bounding_box_extractor import TextBoundingBoxExtractor
from tests.tenderness.bounding_boxes.test_text_bounding_box_extractor._test_cases import (
    BBOX_ORDER_TEST_CASES,
    CHAR_BYTE_INDEX_TEST_CASES,
    CHAR_TEXT_TEST_CASES,
    CLUSTER_TEXT_TEST_CASES,
    LEVELS_TEST_CASES,
    LINE_COUNT_TEST_CASES,
    LINE_DIRECTION_TEST_CASES,
    LINE_PARAGRAPH_START_TEST_CASES,
    LINE_TEXT_TEST_CASES,
    RUN_BIDI_TEST_CASES,
    SCRIPT_LINE_DIRECTION_TEST_CASES,
    SCRIPT_RUN_COUNT_TEST_CASES,
    STRATEGY_TEST_CASES,
    TEXT_RECONSTRUCTION_TEST_CASES,
    VERTICAL_LAYOUT_TEST_CASES,
    BBoxOrderTestCase,
    CharByteIndexTestCase,
    CharTextTestCase,
    ClusterTextTestCase,
    LevelsTestCase,
    LineCountTestCase,
    LineDirectionTestCase,
    LineParagraphStartTestCase,
    LineTextTestCase,
    RunBidiTestCase,
    ScriptLineDirectionTestCase,
    ScriptRunCountTestCase,
    StrategyTestCase,
    TextReconstructionTestCase,
    VerticalLayoutTestCase,
)

gi.require_version("Pango", "1.0")
gi.require_version("PangoCairo", "1.0")
from gi.repository import Pango, PangoCairo  # noqa: E402

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_context() -> cairo.Context[cairo.Surface]:
    surface = cairo.ImageSurface(cairo.Format.RGB24, 400, 400)
    return cairo.Context(surface)


def _make_layout(text: str, width_px: float = 300.0) -> Pango.Layout:
    ctx = _make_context()
    layout = PangoCairo.create_layout(ctx)
    layout.set_text(text, -1)
    layout.set_font_description(Pango.FontDescription.from_string("Sans 14"))
    layout.set_width(Pango.units_from_double(width_px))
    return layout


def _identity() -> cairo.Matrix:
    return cairo.Matrix()


def _make_vertical_layout(
    text: str,
    gravity: Pango.Gravity = Pango.Gravity.EAST,
    width_px: float = 300.0,
) -> Pango.Layout:
    ctx = _make_context()
    layout = PangoCairo.create_layout(ctx)
    # gravity must be set on the Pango context before the layout is used
    pango_ctx = layout.get_context()
    pango_ctx.set_base_gravity(gravity)
    pango_ctx.set_gravity_hint(Pango.GravityHint.STRONG)
    layout.context_changed()
    layout.set_text(text, -1)
    layout.set_font_description(Pango.FontDescription.from_string("Sans 14"))
    layout.set_width(Pango.units_from_double(width_px))
    return layout


@pytest.fixture
def extractor() -> TextBoundingBoxExtractor:
    return TextBoundingBoxExtractor()


# ---------------------------------------------------------------------------
# Tests: levels filtering
# ---------------------------------------------------------------------------


class TestLevels:
    @pytest.mark.parametrize("test_case", LEVELS_TEST_CASES, ids=lambda c: c.test_name)
    def test_levels(self, test_case: LevelsTestCase, extractor: TextBoundingBoxExtractor) -> None:
        layout = _make_layout("Hello")
        result = extractor.extract_bounding_boxes(
            pango_layout=layout,
            matrix=_identity(),
            levels=test_case.levels,
        )
        assert (result.char_boxes is not None) is test_case.expected_char
        assert (result.cluster_boxes is not None) is test_case.expected_cluster
        assert (result.run_boxes is not None) is test_case.expected_run
        assert (result.line_boxes is not None) is test_case.expected_line
        assert (result.layout_box is not None) is test_case.expected_layout


# ---------------------------------------------------------------------------
# Tests: BoundingBoxStrategy
# ---------------------------------------------------------------------------


class TestStrategy:
    @pytest.mark.parametrize("test_case", STRATEGY_TEST_CASES, ids=lambda c: c.test_name)
    def test_strategy(self, test_case: StrategyTestCase, extractor: TextBoundingBoxExtractor) -> None:
        layout = _make_layout("Hello")
        result = extractor.extract_bounding_boxes(
            pango_layout=layout,
            matrix=_identity(),
            levels={test_case.level},
            text_mode=test_case.text_mode,
        )
        match test_case.level:
            case BoundingBoxType.CHAR:
                assert result.char_boxes is not None
                all_none = all(b.char is None for b in result.char_boxes)
                assert all_none is test_case.expect_text_none
            case BoundingBoxType.LINE:
                assert result.line_boxes is not None
                all_none = all(b.text is None for b in result.line_boxes)
                assert all_none is test_case.expect_text_none
            case BoundingBoxType.LAYOUT:
                assert result.layout_box is not None
                assert (result.layout_box.text is None) is test_case.expect_text_none


# ---------------------------------------------------------------------------
# Tests: CharBBox text content
# ---------------------------------------------------------------------------


class TestCharBBoxText:
    @pytest.mark.parametrize("test_case", CHAR_TEXT_TEST_CASES, ids=lambda c: c.test_name)
    def test_char_text_joined(self, test_case: CharTextTestCase, extractor: TextBoundingBoxExtractor) -> None:
        layout = _make_layout(test_case.text)
        result = extractor.extract_bounding_boxes(
            pango_layout=layout, matrix=_identity(), levels={BoundingBoxType.CHAR}
        )
        assert result.char_boxes is not None
        joined = "".join(b.char for b in result.char_boxes if b.char is not None)
        assert joined == test_case.expected_joined


# ---------------------------------------------------------------------------
# Tests: CharBBox byte indices
# ---------------------------------------------------------------------------


class TestCharBBoxByteIndex:
    @pytest.mark.parametrize("test_case", CHAR_BYTE_INDEX_TEST_CASES, ids=lambda c: c.test_name)
    def test_byte_indices(self, test_case: CharByteIndexTestCase, extractor: TextBoundingBoxExtractor) -> None:
        layout = _make_layout(test_case.text)
        result = extractor.extract_bounding_boxes(
            pango_layout=layout, matrix=_identity(), levels={BoundingBoxType.CHAR}
        )
        assert result.char_boxes is not None
        indices = [b.byte_index for b in result.char_boxes if b.char is not None]
        assert indices[0] == test_case.expected_first_index
        assert indices[1] == test_case.expected_second_index


# ---------------------------------------------------------------------------
# Tests: CharBBox schema
# ---------------------------------------------------------------------------


class TestCharBBoxSchema:
    def test_char_has_no_ink_bbox(self, extractor: TextBoundingBoxExtractor) -> None:
        layout = _make_layout("A")
        result = extractor.extract_bounding_boxes(
            pango_layout=layout, matrix=_identity(), levels={BoundingBoxType.CHAR}
        )
        assert result.char_boxes is not None
        assert not hasattr(result.char_boxes[0], "ink_bbox")

    def test_char_byte_indices_non_negative(self, extractor: TextBoundingBoxExtractor) -> None:
        layout = _make_layout("Hi")
        result = extractor.extract_bounding_boxes(
            pango_layout=layout, matrix=_identity(), levels={BoundingBoxType.CHAR}
        )
        assert result.char_boxes is not None
        assert all(b.byte_index >= 0 for b in result.char_boxes)


# ---------------------------------------------------------------------------
# Tests: ClusterBBox text content
# ---------------------------------------------------------------------------


class TestClusterBBoxText:
    @pytest.mark.parametrize("test_case", CLUSTER_TEXT_TEST_CASES, ids=lambda c: c.test_name)
    def test_cluster_text_combined(self, test_case: ClusterTextTestCase, extractor: TextBoundingBoxExtractor) -> None:
        layout = _make_layout(test_case.text)
        result = extractor.extract_bounding_boxes(
            pango_layout=layout, matrix=_identity(), levels={BoundingBoxType.CLUSTER}
        )
        assert result.cluster_boxes is not None
        combined = "".join(b.text for b in result.cluster_boxes if b.text)
        assert combined == test_case.expected_combined


# ---------------------------------------------------------------------------
# Tests: ClusterBBox schema
# ---------------------------------------------------------------------------


class TestClusterBBoxSchema:
    def test_cluster_has_ink_bbox(self, extractor: TextBoundingBoxExtractor) -> None:
        layout = _make_layout("A")
        result = extractor.extract_bounding_boxes(
            pango_layout=layout, matrix=_identity(), levels={BoundingBoxType.CLUSTER}
        )
        assert result.cluster_boxes is not None
        assert result.cluster_boxes[0].ink_bbox is not None

    def test_emoji_is_single_cluster(self, extractor: TextBoundingBoxExtractor) -> None:
        layout = _make_layout("👋")
        result = extractor.extract_bounding_boxes(
            pango_layout=layout, matrix=_identity(), levels={BoundingBoxType.CLUSTER}
        )
        assert result.cluster_boxes is not None
        clusters_with_text = [b for b in result.cluster_boxes if b.text]
        assert len(clusters_with_text) == 1
        assert clusters_with_text[0].text == "👋"


# ---------------------------------------------------------------------------
# Tests: RunBBox bidi
# ---------------------------------------------------------------------------


class TestRunBBoxBidi:
    @pytest.mark.parametrize("test_case", RUN_BIDI_TEST_CASES, ids=lambda c: c.test_name)
    def test_run_count(self, test_case: RunBidiTestCase, extractor: TextBoundingBoxExtractor) -> None:
        layout = _make_layout(test_case.text)
        result = extractor.extract_bounding_boxes(pango_layout=layout, matrix=_identity(), levels={BoundingBoxType.RUN})
        assert result.run_boxes is not None
        assert len(result.run_boxes) >= test_case.expected_min_runs


# ---------------------------------------------------------------------------
# Tests: RunBBox schema
# ---------------------------------------------------------------------------


class TestRunBBoxSchema:
    def test_run_has_ink_bbox(self, extractor: TextBoundingBoxExtractor) -> None:
        layout = _make_layout("Hello")
        result = extractor.extract_bounding_boxes(pango_layout=layout, matrix=_identity(), levels={BoundingBoxType.RUN})
        assert result.run_boxes is not None
        assert all(b.ink_bbox is not None for b in result.run_boxes)

    def test_run_baseline_non_negative(self, extractor: TextBoundingBoxExtractor) -> None:
        layout = _make_layout("Hello")
        result = extractor.extract_bounding_boxes(pango_layout=layout, matrix=_identity(), levels={BoundingBoxType.RUN})
        assert result.run_boxes is not None
        assert all(b.baseline >= 0 for b in result.run_boxes)

    def test_run_byte_length_non_negative(self, extractor: TextBoundingBoxExtractor) -> None:
        layout = _make_layout("Hello")
        result = extractor.extract_bounding_boxes(pango_layout=layout, matrix=_identity(), levels={BoundingBoxType.RUN})
        assert result.run_boxes is not None
        assert all(b.byte_length >= 0 for b in result.run_boxes)


# ---------------------------------------------------------------------------
# Tests: LineBBox count
# ---------------------------------------------------------------------------


class TestLineBBoxCount:
    @pytest.mark.parametrize("test_case", LINE_COUNT_TEST_CASES, ids=lambda c: c.test_name)
    def test_line_count(self, test_case: LineCountTestCase, extractor: TextBoundingBoxExtractor) -> None:
        layout = _make_layout(test_case.text)
        result = extractor.extract_bounding_boxes(
            pango_layout=layout, matrix=_identity(), levels={BoundingBoxType.LINE}
        )
        assert result.line_boxes is not None
        assert len(result.line_boxes) == test_case.expected_count


# ---------------------------------------------------------------------------
# Tests: LineBBox paragraph start
# ---------------------------------------------------------------------------


class TestLineBBoxParagraphStart:
    @pytest.mark.parametrize("test_case", LINE_PARAGRAPH_START_TEST_CASES, ids=lambda c: c.test_name)
    def test_first_line_paragraph_start(
        self, test_case: LineParagraphStartTestCase, extractor: TextBoundingBoxExtractor
    ) -> None:
        layout = _make_layout(test_case.text)
        result = extractor.extract_bounding_boxes(
            pango_layout=layout, matrix=_identity(), levels={BoundingBoxType.LINE}
        )
        assert result.line_boxes is not None
        assert result.line_boxes[0].is_paragraph_start is test_case.expected_first_is_paragraph_start


# ---------------------------------------------------------------------------
# Tests: LineBBox direction
# ---------------------------------------------------------------------------


class TestLineBBoxDirection:
    @pytest.mark.parametrize("test_case", LINE_DIRECTION_TEST_CASES, ids=lambda c: c.test_name)
    def test_line_direction(self, test_case: LineDirectionTestCase, extractor: TextBoundingBoxExtractor) -> None:
        layout = _make_layout(test_case.text)
        result = extractor.extract_bounding_boxes(
            pango_layout=layout, matrix=_identity(), levels={BoundingBoxType.LINE}
        )
        assert result.line_boxes is not None
        assert result.line_boxes[0].resolved_direction == test_case.expected_direction


# ---------------------------------------------------------------------------
# Tests: LineBBox text
# ---------------------------------------------------------------------------


class TestLineBBoxText:
    @pytest.mark.parametrize("test_case", LINE_TEXT_TEST_CASES, ids=lambda c: c.test_name)
    def test_line_text(self, test_case: LineTextTestCase, extractor: TextBoundingBoxExtractor) -> None:
        layout = _make_layout(test_case.text)
        result = extractor.extract_bounding_boxes(
            pango_layout=layout, matrix=_identity(), levels={BoundingBoxType.LINE}
        )
        assert result.line_boxes is not None
        texts = [b.text for b in result.line_boxes if b.text is not None]
        assert texts == test_case.expected_texts


# ---------------------------------------------------------------------------
# Tests: LineBBox schema
# ---------------------------------------------------------------------------


class TestLineBBoxSchema:
    def test_line_has_ink_bbox(self, extractor: TextBoundingBoxExtractor) -> None:
        layout = _make_layout("Hello")
        result = extractor.extract_bounding_boxes(
            pango_layout=layout, matrix=_identity(), levels={BoundingBoxType.LINE}
        )
        assert result.line_boxes is not None
        assert result.line_boxes[0].ink_bbox is not None

    def test_line_baseline_non_negative(self, extractor: TextBoundingBoxExtractor) -> None:
        layout = _make_layout("Hello")
        result = extractor.extract_bounding_boxes(
            pango_layout=layout, matrix=_identity(), levels={BoundingBoxType.LINE}
        )
        assert result.line_boxes is not None
        assert all(b.baseline >= 0 for b in result.line_boxes)


# ---------------------------------------------------------------------------
# Tests: LayoutBBox schema
# ---------------------------------------------------------------------------


class TestLayoutBBoxSchema:
    def test_layout_has_ink_bbox(self, extractor: TextBoundingBoxExtractor) -> None:
        layout = _make_layout("Hello")
        result = extractor.extract_bounding_boxes(
            pango_layout=layout, matrix=_identity(), levels={BoundingBoxType.LAYOUT}
        )
        assert result.layout_box is not None
        assert result.layout_box.ink_bbox is not None

    def test_layout_has_no_baseline(self, extractor: TextBoundingBoxExtractor) -> None:
        layout = _make_layout("Hello")
        result = extractor.extract_bounding_boxes(
            pango_layout=layout, matrix=_identity(), levels={BoundingBoxType.LAYOUT}
        )
        assert result.layout_box is not None
        assert not hasattr(result.layout_box, "baseline")

    def test_layout_text(self, extractor: TextBoundingBoxExtractor) -> None:
        layout = _make_layout("Hello")
        result = extractor.extract_bounding_boxes(
            pango_layout=layout, matrix=_identity(), levels={BoundingBoxType.LAYOUT}
        )
        assert result.layout_box is not None
        assert result.layout_box.text == "Hello"

    def test_layout_logical_encloses_all_lines(self, extractor: TextBoundingBoxExtractor) -> None:
        layout = _make_layout("Hello\nWorld")
        result = extractor.extract_bounding_boxes(
            pango_layout=layout,
            matrix=_identity(),
            levels={BoundingBoxType.LAYOUT, BoundingBoxType.LINE},
        )
        assert result.layout_box is not None
        assert result.line_boxes is not None
        layout_top = result.layout_box.logical_bbox.top_left[1]
        layout_bottom = result.layout_box.logical_bbox.bottom_left[1]
        for line in result.line_boxes:
            assert line.logical_bbox.top_left[1] >= layout_top - 1e-6
            assert line.logical_bbox.bottom_left[1] <= layout_bottom + 1e-6


# ---------------------------------------------------------------------------
# Tests: script line direction
# ---------------------------------------------------------------------------


class TestScriptLineDirection:
    @pytest.mark.parametrize("test_case", SCRIPT_LINE_DIRECTION_TEST_CASES, ids=lambda c: c.test_name)
    def test_line_direction(self, test_case: ScriptLineDirectionTestCase, extractor: TextBoundingBoxExtractor) -> None:
        layout = _make_layout(test_case.text)
        result = extractor.extract_bounding_boxes(
            pango_layout=layout, matrix=_identity(), levels={BoundingBoxType.LINE}
        )
        assert result.line_boxes is not None
        assert result.line_boxes[0].resolved_direction == test_case.expected_direction


# ---------------------------------------------------------------------------
# Tests: script run count
# ---------------------------------------------------------------------------


class TestScriptRunCount:
    @pytest.mark.parametrize("test_case", SCRIPT_RUN_COUNT_TEST_CASES, ids=lambda c: c.test_name)
    def test_run_count(self, test_case: ScriptRunCountTestCase, extractor: TextBoundingBoxExtractor) -> None:
        layout = _make_layout(test_case.text)
        result = extractor.extract_bounding_boxes(pango_layout=layout, matrix=_identity(), levels={BoundingBoxType.RUN})
        assert result.run_boxes is not None
        assert len(result.run_boxes) >= test_case.expected_min_runs


# ---------------------------------------------------------------------------
# Tests: bounding box order
#
# Line boxes: always top-to-bottom in y-down space regardless of script
# direction — Pango's iterator walks layout lines top-to-bottom.
#
# Line byte_start: always monotonically increasing in logical (storage)
# order, because Pango stores text in logical order regardless of visual
# direction.
#
# LTR clusters: x positions increase left-to-right within a line.
# RTL clusters: x positions decrease (visual right-to-left) within a line,
# because the iterator walks in visual order.
# ---------------------------------------------------------------------------


class TestBBoxOrder:
    @pytest.mark.parametrize("test_case", BBOX_ORDER_TEST_CASES, ids=lambda c: c.test_name)
    def test_line_byte_start_monotone(self, test_case: BBoxOrderTestCase, extractor: TextBoundingBoxExtractor) -> None:
        layout = _make_layout(test_case.text)
        result = extractor.extract_bounding_boxes(
            pango_layout=layout, matrix=_identity(), levels={BoundingBoxType.LINE}
        )
        assert result.line_boxes is not None
        byte_starts = [b.byte_start for b in result.line_boxes]
        assert byte_starts == sorted(byte_starts), (
            f"Line byte_start values are not monotonically increasing: {byte_starts}"
        )

    def test_ltr_lines_top_to_bottom(self, extractor: TextBoundingBoxExtractor) -> None:
        layout = _make_layout("First\nSecond\nThird")
        result = extractor.extract_bounding_boxes(
            pango_layout=layout, matrix=_identity(), levels={BoundingBoxType.LINE}
        )
        assert result.line_boxes is not None
        ys = [b.logical_bbox.top_left[1] for b in result.line_boxes]
        assert ys == sorted(ys), f"LTR lines not top-to-bottom: {ys}"

    def test_rtl_lines_top_to_bottom(self, extractor: TextBoundingBoxExtractor) -> None:
        layout = _make_layout("مرحبا\nكيف حالك\nأتمنى لك")
        result = extractor.extract_bounding_boxes(
            pango_layout=layout, matrix=_identity(), levels={BoundingBoxType.LINE}
        )
        assert result.line_boxes is not None
        ys = [b.logical_bbox.top_left[1] for b in result.line_boxes]
        assert ys == sorted(ys), f"RTL lines not top-to-bottom: {ys}"

    def test_rtl_clusters_visual_order(self, extractor: TextBoundingBoxExtractor) -> None:
        """RTL clusters are yielded in visual order — byte indices are
        monotonically decreasing because RTL reads right-to-left visually,
        which is reverse logical order.
        """
        layout = _make_layout("مرحبا")
        result = extractor.extract_bounding_boxes(
            pango_layout=layout, matrix=_identity(), levels={BoundingBoxType.CLUSTER}
        )
        assert result.cluster_boxes is not None
        byte_indices = [b.byte_index for b in result.cluster_boxes]
        assert byte_indices == sorted(byte_indices, reverse=True), (
            f"RTL cluster byte indices not in visual order: {byte_indices}"
        )

    def test_ltr_clusters_visual_order(self, extractor: TextBoundingBoxExtractor) -> None:
        """LTR clusters are yielded in visual order — byte indices are
        monotonically increasing because LTR reads left-to-right visually,
        which matches logical order.
        """
        layout = _make_layout("ABC")
        result = extractor.extract_bounding_boxes(
            pango_layout=layout, matrix=_identity(), levels={BoundingBoxType.CLUSTER}
        )
        assert result.cluster_boxes is not None
        byte_indices = [b.byte_index for b in result.cluster_boxes]
        assert byte_indices == sorted(byte_indices), f"LTR cluster byte indices not in visual order: {byte_indices}"


# ---------------------------------------------------------------------------
# Tests: text reconstruction
#
# Text from bboxes, sorted by byte offset and joined, must equal the
# original layout text.
#
# RTL and bidi: bbox iteration order is visual, not logical.
# Sorting by byte_start / byte_index restores logical order, which when
# joined must match the original input string.
# ---------------------------------------------------------------------------


class TestTextReconstruction:
    @pytest.mark.parametrize("test_case", TEXT_RECONSTRUCTION_TEST_CASES, ids=lambda c: c.test_name)
    def test_text_reconstruction(
        self, test_case: TextReconstructionTestCase, extractor: TextBoundingBoxExtractor
    ) -> None:
        layout = _make_layout(test_case.text)
        result = extractor.extract_bounding_boxes(
            pango_layout=layout,
            matrix=_identity(),
            levels={test_case.level},
            text_mode=BoundingBoxStrategy.WITH_TEXT,
        )

        match test_case.level:
            case BoundingBoxType.CLUSTER:
                assert result.cluster_boxes is not None
                # RTL clusters are in visual order — sort by byte_index for logical order
                sorted_clusters = sorted(result.cluster_boxes, key=lambda b: b.byte_index)
                reconstructed = "".join(b.text for b in sorted_clusters if b.text)

            case BoundingBoxType.RUN:
                assert result.run_boxes is not None
                sorted_runs = sorted(result.run_boxes, key=lambda b: b.byte_start)
                reconstructed = "".join(b.text for b in sorted_runs if b.text)

            case BoundingBoxType.LINE:
                assert result.line_boxes is not None
                # lines are already in logical order (monotone byte_start)
                reconstructed = "\n".join(b.text for b in result.line_boxes if b.text)

            case _:
                pytest.fail(f"Unhandled level: {test_case.level}")
                return

        assert reconstructed == test_case.text, f"Reconstructed {reconstructed!r} != original {test_case.text!r}"


class TestVerticalLayout:
    @pytest.mark.parametrize("test_case", VERTICAL_LAYOUT_TEST_CASES, ids=lambda c: c.test_name)
    def test_line_count(self, test_case: VerticalLayoutTestCase, extractor: TextBoundingBoxExtractor) -> None:
        layout = _make_vertical_layout(test_case.text, gravity=test_case.gravity)
        result = extractor.extract_bounding_boxes(
            pango_layout=layout, matrix=_identity(), levels={BoundingBoxType.LINE}
        )
        assert result.line_boxes is not None
        assert len(result.line_boxes) == test_case.expected_line_count

    @pytest.mark.parametrize("test_case", VERTICAL_LAYOUT_TEST_CASES, ids=lambda c: c.test_name)
    def test_line_byte_start_monotone(
        self, test_case: VerticalLayoutTestCase, extractor: TextBoundingBoxExtractor
    ) -> None:
        layout = _make_vertical_layout(test_case.text, gravity=test_case.gravity)
        result = extractor.extract_bounding_boxes(
            pango_layout=layout, matrix=_identity(), levels={BoundingBoxType.LINE}
        )
        assert result.line_boxes is not None
        byte_starts = [b.byte_start for b in result.line_boxes]
        assert byte_starts == sorted(byte_starts), f"Vertical line byte_start not monotone: {byte_starts}"

    @pytest.mark.parametrize(
        "test_case",
        [c for c in VERTICAL_LAYOUT_TEST_CASES if "\n" not in c.text],
        ids=lambda c: c.test_name,
    )
    def test_cluster_text_reconstruction(
        self, test_case: VerticalLayoutTestCase, extractor: TextBoundingBoxExtractor
    ) -> None:
        # Pango's cluster iterator does not yield paragraph separators (\n),
        # so multiline reconstruction at cluster level is not possible.
        # Multiline cases are covered by test_line_byte_start_monotone instead.

        layout = _make_vertical_layout(test_case.text, gravity=test_case.gravity)
        result = extractor.extract_bounding_boxes(
            pango_layout=layout,
            matrix=_identity(),
            levels={BoundingBoxType.CLUSTER},
            text_mode=BoundingBoxStrategy.WITH_TEXT,
        )
        assert result.cluster_boxes is not None
        sorted_clusters = sorted(result.cluster_boxes, key=lambda b: b.byte_index)
        reconstructed = "".join(b.text for b in sorted_clusters if b.text)
        assert reconstructed == test_case.text, (
            f"Vertical cluster reconstruction {reconstructed!r} != {test_case.text!r}"
        )

    @pytest.mark.parametrize("test_case", VERTICAL_LAYOUT_TEST_CASES, ids=lambda c: c.test_name)
    def test_has_ink_and_logical_bboxes(
        self, test_case: VerticalLayoutTestCase, extractor: TextBoundingBoxExtractor
    ) -> None:
        layout = _make_vertical_layout(test_case.text, gravity=test_case.gravity)
        result = extractor.extract_bounding_boxes(
            pango_layout=layout,
            matrix=_identity(),
            levels={BoundingBoxType.LINE, BoundingBoxType.LAYOUT},
        )
        assert result.line_boxes is not None
        assert result.layout_box is not None
        assert result.layout_box.ink_bbox is not None
        assert result.layout_box.logical_bbox is not None
        for line in result.line_boxes:
            assert line.ink_bbox is not None
            assert line.logical_bbox is not None

    def test_east_vs_west_gravity_different_boxes(self, extractor: TextBoundingBoxExtractor) -> None:
        """EAST and WEST gravity should produce different logical bounding boxes."""
        text = "こんにちは"
        layout_east = _make_vertical_layout(text, gravity=Pango.Gravity.EAST)
        layout_west = _make_vertical_layout(text, gravity=Pango.Gravity.WEST)

        result_east = extractor.extract_bounding_boxes(
            pango_layout=layout_east, matrix=_identity(), levels={BoundingBoxType.LAYOUT}
        )
        result_west = extractor.extract_bounding_boxes(
            pango_layout=layout_west, matrix=_identity(), levels={BoundingBoxType.LAYOUT}
        )

        assert result_east.layout_box is not None
        assert result_west.layout_box is not None

        east_tl = result_east.layout_box.logical_bbox.top_left
        west_tl = result_west.layout_box.logical_bbox.top_left
        assert east_tl != west_tl
