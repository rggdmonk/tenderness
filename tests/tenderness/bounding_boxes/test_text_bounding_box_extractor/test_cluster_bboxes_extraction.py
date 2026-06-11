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
from typing import ClassVar

import pytest

from tenderness.bounding_boxes.bounding_boxes_schema import BoundingBoxType
from tenderness.bounding_boxes.text_bounding_box_extractor import TextBoundingBoxExtractor
from tests._test_utils.render_helpers import (
    _testutil_assert_no_ink_bbox_overlap,
    _testutil_assert_no_logical_bbox_overlap,
    _testutil_simple_text,
)


@dataclass(slots=True, frozen=True)
class ExpectedClusterBBox:
    text: str | None
    byte_index: int
    byte_length: int


@dataclass(slots=True, frozen=True)
class ClusterBBoxExtractionTestCase:
    test_name: str
    input_text: str
    include_text: bool
    expected_clusters: list[ExpectedClusterBBox]
    # Connected scripts (Arabic, Devanagari, …) have ink that physically bleeds across
    # glyph boundaries, so their ink_bboxes legitimately overlap. Set False to skip the check.
    check_ink_overlap: bool = True


CLUSTER_BBOX_EXTRACTION_TEST_CASES: list[ClusterBBoxExtractionTestCase] = [
    ClusterBBoxExtractionTestCase(
        test_name="latin_only",
        input_text="pqr",
        include_text=True,
        expected_clusters=[
            ExpectedClusterBBox(text="p", byte_index=0, byte_length=1),
            ExpectedClusterBBox(text="q", byte_index=1, byte_length=1),
            ExpectedClusterBBox(text="r", byte_index=2, byte_length=1),
        ],
    ),
    # 2-byte UTF-8: θ(2) + λ(2) + ξ(2) = 6 bytes
    ClusterBBoxExtractionTestCase(
        test_name="2byte_greek",
        input_text="θλξ",
        include_text=True,
        expected_clusters=[
            ExpectedClusterBBox(text="θ", byte_index=0, byte_length=2),
            ExpectedClusterBBox(text="λ", byte_index=2, byte_length=2),
            ExpectedClusterBBox(text="ξ", byte_index=4, byte_length=2),
        ],
    ),
    # 3-byte UTF-8: 水(3) + 火(3) + 木(3) = 9 bytes
    ClusterBBoxExtractionTestCase(
        test_name="3byte_cjk",
        input_text="水火木",
        include_text=True,
        expected_clusters=[
            ExpectedClusterBBox(text="水", byte_index=0, byte_length=3),
            ExpectedClusterBBox(text="火", byte_index=3, byte_length=3),
            ExpectedClusterBBox(text="木", byte_index=6, byte_length=3),
        ],
    ),
    # 4-byte emoji — each code point is its own cluster (no ZWJ)
    ClusterBBoxExtractionTestCase(
        test_name="4byte_emoji_simple",
        input_text="🌍🌎",
        include_text=True,
        expected_clusters=[
            ExpectedClusterBBox(text="🌍", byte_index=0, byte_length=4),
            ExpectedClusterBBox(text="🌎", byte_index=4, byte_length=4),
        ],
    ),
    # ZWJ sequences — Pango groups each entire sequence as one cluster.
    # 🐻‍❄️: 🐻(4) + ZWJ(3) + ❄(3) + VS-16(3) = 13 bytes
    # 👨‍💻: 👨(4) + ZWJ(3) + 💻(4)            = 11 bytes
    ClusterBBoxExtractionTestCase(
        test_name="zwj_two_sequences",
        input_text="🐻‍❄️👨‍💻",
        include_text=True,
        expected_clusters=[
            ExpectedClusterBBox(text="🐻‍❄️", byte_index=0, byte_length=13),
            ExpectedClusterBBox(text="👨‍💻", byte_index=13, byte_length=11),
        ],
    ),
    # 🏳️‍🌈: 🏳(4) + VS-16(3) + ZWJ(3) + 🌈(4) = 14 bytes  (flag + modifier + ZWJ + object)
    ClusterBBoxExtractionTestCase(
        test_name="zwj_rainbow_flag",
        input_text="🏳️‍🌈",
        include_text=True,
        expected_clusters=[
            ExpectedClusterBBox(text="🏳️‍🌈", byte_index=0, byte_length=14),
        ],
    ),
    # ASCII text mixed with a ZWJ sequence:
    # "hi 👨‍💻 ok": h(1)+i(1)+sp(1)+👨‍💻(11)+sp(1)+o(1)+k(1) = 17 bytes total
    ClusterBBoxExtractionTestCase(
        test_name="text_and_zwj",
        input_text="hi 👨‍💻 ok",
        include_text=True,
        expected_clusters=[
            ExpectedClusterBBox(text="h", byte_index=0, byte_length=1),
            ExpectedClusterBBox(text="i", byte_index=1, byte_length=1),
            ExpectedClusterBBox(text=" ", byte_index=2, byte_length=1),
            ExpectedClusterBBox(text="👨‍💻", byte_index=3, byte_length=11),
            ExpectedClusterBBox(text=" ", byte_index=14, byte_length=1),
            ExpectedClusterBBox(text="o", byte_index=15, byte_length=1),
            ExpectedClusterBBox(text="k", byte_index=16, byte_length=1),
        ],
    ),
    # Arabic RTL — clusters come out in visual (screen left-to-right) order:
    # "نور" logical: ن(0,2) و(2,2) ر(4,2); visual: ر(4) و(2) ن(0)
    # check_ink_overlap=False: Arabic is a connected script; adjacent glyph ink strokes
    # physically join across cluster boundaries, so ink_bbox overlap is expected and correct.
    ClusterBBoxExtractionTestCase(
        test_name="arabic_rtl",
        input_text="نور",
        include_text=True,
        check_ink_overlap=False,
        expected_clusters=[
            ExpectedClusterBBox(text="ر", byte_index=4, byte_length=2),
            ExpectedClusterBBox(text="و", byte_index=2, byte_length=2),
            ExpectedClusterBBox(text="ن", byte_index=0, byte_length=2),
        ],
    ),
    # '\n' is a NULL sentinel run in Pango — excluded from cluster output entirely.
    # byte_index jumps from 1 (\n at byte 2 is absent) to 3.
    ClusterBBoxExtractionTestCase(
        test_name="newline_two_lines",
        input_text="ab\ncd",
        include_text=True,
        expected_clusters=[
            ExpectedClusterBBox(text="a", byte_index=0, byte_length=1),
            ExpectedClusterBBox(text="b", byte_index=1, byte_length=1),
            ExpectedClusterBBox(text="c", byte_index=3, byte_length=1),
            ExpectedClusterBBox(text="d", byte_index=4, byte_length=1),
        ],
    ),
    # '\t' is a regular printable whitespace — rendered in a normal run, included as a cluster.
    ClusterBBoxExtractionTestCase(
        test_name="tab_in_text",
        input_text="p\tq\tr",
        include_text=True,
        expected_clusters=[
            ExpectedClusterBBox(text="p", byte_index=0, byte_length=1),
            ExpectedClusterBBox(text="\t", byte_index=1, byte_length=1),
            ExpectedClusterBBox(text="q", byte_index=2, byte_length=1),
            ExpectedClusterBBox(text="\t", byte_index=3, byte_length=1),
            ExpectedClusterBBox(text="r", byte_index=4, byte_length=1),
        ],
    ),
    # NFD "café": c(1)+a(1)+f(1)+e(1)+U+0301(2) = 6 bytes; Pango groups e+combining_acute as one cluster
    ClusterBBoxExtractionTestCase(
        test_name="latin_with_accent_cafe_nfd",
        input_text="café",
        include_text=True,
        expected_clusters=[
            ExpectedClusterBBox(text="c", byte_index=0, byte_length=1),
            ExpectedClusterBBox(text="a", byte_index=1, byte_length=1),
            ExpectedClusterBBox(text="f", byte_index=2, byte_length=1),
            ExpectedClusterBBox(text="é", byte_index=3, byte_length=3),
        ],
    ),
    ClusterBBoxExtractionTestCase(
        test_name="include_text_false",
        input_text="pqr",
        include_text=False,
        expected_clusters=[
            ExpectedClusterBBox(text=None, byte_index=0, byte_length=1),
            ExpectedClusterBBox(text=None, byte_index=1, byte_length=1),
            ExpectedClusterBBox(text=None, byte_index=2, byte_length=1),
        ],
    ),
]


class TestTextBoundingBoxExtractorClusterBBoxExtraction:
    _FAMILY_NAME: ClassVar[str] = "Noto Sans"
    _FAMILY_SIZE: ClassVar[int] = 24
    _HEIGHT: ClassVar[int] = 500
    _WIDTH: ClassVar[int] = 500
    _LEVELS: ClassVar[set[BoundingBoxType]] = set({BoundingBoxType.CLUSTER})

    @pytest.mark.usefixtures("unittests_font_setup")
    @pytest.mark.parametrize("test_case", CLUSTER_BBOX_EXTRACTION_TEST_CASES, ids=lambda tc: tc.test_name)
    def test_cluster_bbox_extraction(self, test_case: ClusterBBoxExtractionTestCase) -> None:

        _, cairo_context, layout = _testutil_simple_text(
            text=test_case.input_text,
            family_name=self._FAMILY_NAME,
            font_size=self._FAMILY_SIZE,
            height=self._HEIGHT,
            width=self._WIDTH,
        )
        text_bounding_box_extractor = TextBoundingBoxExtractor()

        result = text_bounding_box_extractor.extract_bounding_boxes(
            pango_layout=layout,
            matrix=cairo_context.get_matrix(),
            include_text=test_case.include_text,
            levels=self._LEVELS,
        )

        assert result.char_bboxes is None
        assert result.cluster_bboxes is not None
        assert result.run_bboxes is None
        assert result.line_bboxes is None
        assert result.layout_bbox is None

        assert len(result.cluster_bboxes) == len(test_case.expected_clusters)

        _testutil_assert_no_logical_bbox_overlap(result.cluster_bboxes)
        if test_case.check_ink_overlap:
            _testutil_assert_no_ink_bbox_overlap(result.cluster_bboxes)

        if test_case.include_text:
            # Clusters skip NULL sentinel runs, so '\n' is excluded from results.
            # RTL clusters come out in visual order, so sort by byte_index to restore logical order.
            sorted_clusters = sorted(result.cluster_bboxes, key=lambda cb: cb.byte_index)
            assert "".join(cb.text for cb in sorted_clusters if cb.text is not None) == test_case.input_text.replace(
                "\n", ""
            )

        for cluster_bbox, expected in zip(result.cluster_bboxes, test_case.expected_clusters, strict=True):
            assert cluster_bbox.text == expected.text
            assert cluster_bbox.byte_index == expected.byte_index
            assert cluster_bbox.byte_length == expected.byte_length
