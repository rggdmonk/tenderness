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

import math
from dataclasses import dataclass

from tenderness.core.geometry import Rectangle


@dataclass(frozen=True, slots=True)
class NormalizedBoundsTestCase:
    test_name: str
    x: float
    y: float
    width: float
    height: float
    x_min: float
    x_max: float
    y_min: float
    y_max: float


NORMALIZED_BOUNDS_TEST_CASES = [
    # --- basic ---
    NormalizedBoundsTestCase(
        test_name="normal",
        x=0,
        y=0,
        width=10,
        height=10,
        x_min=0,
        x_max=10,
        y_min=0,
        y_max=10,
    ),
    # --- negative dimensions ---
    NormalizedBoundsTestCase(
        test_name="negative w/h, same region",
        x=10,
        y=10,
        width=-10,
        height=-10,
        x_min=0,
        x_max=10,
        y_min=0,
        y_max=10,
    ),
    NormalizedBoundsTestCase(
        test_name="negative width only",
        x=10,
        y=0,
        width=-10,
        height=10,
        x_min=0,
        x_max=10,
        y_min=0,
        y_max=10,
    ),
    NormalizedBoundsTestCase(
        test_name="negative height only",
        x=0,
        y=10,
        width=10,
        height=-10,
        x_min=0,
        x_max=10,
        y_min=0,
        y_max=10,
    ),
    # --- negative origin ---
    NormalizedBoundsTestCase(
        test_name="negative origin positive dimensions",
        x=-4,
        y=-4,
        width=8,
        height=8,
        x_min=-4,
        x_max=4,
        y_min=-4,
        y_max=4,
    ),
    NormalizedBoundsTestCase(
        test_name="negative origin negative dimensions",
        x=4,
        y=4,
        width=-8,
        height=-8,
        x_min=-4,
        x_max=4,
        y_min=-4,
        y_max=4,
    ),
    NormalizedBoundsTestCase(
        test_name="fully negative quadrant",
        x=-10,
        y=-10,
        width=-5,
        height=-5,
        x_min=-15,
        x_max=-10,
        y_min=-15,
        y_max=-10,
    ),
    # --- zero dimensions ---
    NormalizedBoundsTestCase(
        test_name="zero width collapses x",
        x=5,
        y=5,
        width=0,
        height=10,
        x_min=5,
        x_max=5,
        y_min=5,
        y_max=15,
    ),
    NormalizedBoundsTestCase(
        test_name="zero height collapses y",
        x=5,
        y=5,
        width=10,
        height=0,
        x_min=5,
        x_max=15,
        y_min=5,
        y_max=5,
    ),
    NormalizedBoundsTestCase(
        test_name="zero width and height collapses to point",
        x=5,
        y=5,
        width=0,
        height=0,
        x_min=5,
        x_max=5,
        y_min=5,
        y_max=5,
    ),
    # --- origin at zero ---
    NormalizedBoundsTestCase(
        test_name="all zeros",
        x=0,
        y=0,
        width=0,
        height=0,
        x_min=0,
        x_max=0,
        y_min=0,
        y_max=0,
    ),
    # --- float precision ---
    NormalizedBoundsTestCase(
        test_name="float dimensions",
        x=1.5,
        y=2.5,
        width=3.5,
        height=4.5,
        x_min=1.5,
        x_max=5.0,
        y_min=2.5,
        y_max=7.0,
    ),
    NormalizedBoundsTestCase(
        test_name="float negative dimensions",
        x=5.0,
        y=7.0,
        width=-3.5,
        height=-4.5,
        x_min=1.5,
        x_max=5.0,
        y_min=2.5,
        y_max=7.0,
    ),
]


@dataclass(frozen=True, slots=True)
class AreaTestCase:
    test_name: str
    width: float
    height: float
    expected: float


AREA_TEST_CASES = [
    # --- normal ---
    AreaTestCase(test_name="normal", width=10, height=10, expected=100),
    AreaTestCase(test_name="non-square", width=4, height=5, expected=20),
    # --- negative dimensions ---
    AreaTestCase(test_name="both negative", width=-10, height=-10, expected=100),
    AreaTestCase(test_name="negative width", width=-10, height=10, expected=100),
    AreaTestCase(test_name="negative height", width=10, height=-10, expected=100),
    # --- zero ---
    AreaTestCase(test_name="zero width", width=0, height=10, expected=0),
    AreaTestCase(test_name="zero height", width=10, height=0, expected=0),
    AreaTestCase(test_name="both zero", width=0, height=0, expected=0),
    # --- float ---
    AreaTestCase(test_name="float dimensions", width=2.5, height=4.0, expected=10.0),
    AreaTestCase(test_name="float negative", width=-2.5, height=-4.0, expected=10.0),
    # --- unit ---
    AreaTestCase(test_name="unit square", width=1, height=1, expected=1),
]


@dataclass(frozen=True, slots=True)
class PerimeterTestCase:
    test_name: str
    width: float
    height: float
    expected: float


PERIMETER_TEST_CASES = [
    # --- normal ---
    PerimeterTestCase(test_name="normal", width=10, height=10, expected=40),
    PerimeterTestCase(test_name="non-square", width=10, height=5, expected=30),
    # --- negative dimensions ---
    PerimeterTestCase(test_name="both negative", width=-10, height=-10, expected=40),
    PerimeterTestCase(test_name="negative width", width=-10, height=10, expected=40),
    PerimeterTestCase(test_name="negative height", width=10, height=-10, expected=40),
    PerimeterTestCase(test_name="negative non-square", width=-10, height=-5, expected=30),
    # --- zero ---
    PerimeterTestCase(test_name="zero width", width=0, height=10, expected=20),
    PerimeterTestCase(test_name="zero height", width=10, height=0, expected=20),
    PerimeterTestCase(test_name="both zero", width=0, height=0, expected=0),
    # --- float ---
    PerimeterTestCase(test_name="float dimensions", width=2.5, height=4.0, expected=13.0),
    PerimeterTestCase(test_name="float negative", width=-2.5, height=-4.0, expected=13.0),
    # --- unit ---
    PerimeterTestCase(test_name="unit square", width=1, height=1, expected=4),
]


@dataclass(frozen=True, slots=True)
class CenterTestCase:
    test_name: str
    x: float
    y: float
    width: float
    height: float
    expected: tuple[float, float]


CENTER_TEST_CASES = [
    # --- normal ---
    CenterTestCase(test_name="normal", x=0, y=0, width=10, height=10, expected=(5.0, 5.0)),
    CenterTestCase(test_name="non-square", x=0, y=0, width=10, height=4, expected=(5.0, 2.0)),
    CenterTestCase(test_name="offset origin", x=5, y=5, width=10, height=10, expected=(10.0, 10.0)),
    # --- negative dimensions ---
    CenterTestCase(test_name="negative w/h same center", x=10, y=10, width=-10, height=-10, expected=(5.0, 5.0)),
    CenterTestCase(test_name="negative width only", x=10, y=0, width=-10, height=10, expected=(5.0, 5.0)),
    CenterTestCase(test_name="negative height only", x=0, y=10, width=10, height=-10, expected=(5.0, 5.0)),
    # --- negative origin ---
    CenterTestCase(test_name="negative origin", x=-4, y=-4, width=8, height=8, expected=(0.0, 0.0)),
    CenterTestCase(test_name="negative origin negative wh", x=4, y=4, width=-8, height=-8, expected=(0.0, 0.0)),
    CenterTestCase(test_name="fully negative quadrant", x=-10, y=-10, width=4, height=4, expected=(-8.0, -8.0)),
    # --- zero dimensions ---
    CenterTestCase(test_name="zero width center on edge", x=5, y=0, width=0, height=10, expected=(5.0, 5.0)),
    CenterTestCase(test_name="zero height center on edge", x=0, y=5, width=10, height=0, expected=(5.0, 5.0)),
    CenterTestCase(test_name="point collapses to origin", x=3, y=7, width=0, height=0, expected=(3.0, 7.0)),
    # --- float ---
    CenterTestCase(test_name="float dimensions", x=0.0, y=0.0, width=3.0, height=5.0, expected=(1.5, 2.5)),
    CenterTestCase(test_name="float negative dimensions", x=3.0, y=5.0, width=-3.0, height=-5.0, expected=(1.5, 2.5)),
]


@dataclass(frozen=True, slots=True)
class SizeTestCase:
    test_name: str
    width: float
    height: float


SIZE_TEST_CASES = [
    # --- normal ---
    SizeTestCase(test_name="normal", width=10, height=10),
    SizeTestCase(test_name="non-square", width=10, height=5),
    SizeTestCase(test_name="unit square", width=1, height=1),
    # --- negative dimensions ---
    SizeTestCase(test_name="both negative", width=-10, height=-10),
    SizeTestCase(test_name="negative width", width=-10, height=10),
    SizeTestCase(test_name="negative height", width=10, height=-10),
    SizeTestCase(test_name="negative non-square", width=-10, height=-5),
    # --- zero ---
    SizeTestCase(test_name="zero width", width=0, height=10),
    SizeTestCase(test_name="zero height", width=10, height=0),
    SizeTestCase(test_name="both zero", width=0, height=0),
    # --- float ---
    SizeTestCase(test_name="float dimensions", width=2.5, height=4.0),
    SizeTestCase(test_name="float negative", width=-2.5, height=-4.0),
    SizeTestCase(test_name="float mixed sign", width=-2.5, height=4.0),
]


@dataclass(frozen=True, slots=True)
class AspectRatioTestCase:
    test_name: str
    width: float
    height: float
    expected: float


ASPECT_RATIO_TEST_CASES = [
    # --- normal ---
    AspectRatioTestCase(test_name="normal wider than tall", width=20, height=10, expected=2.0),
    AspectRatioTestCase(test_name="normal taller than wide", width=10, height=20, expected=0.5),
    AspectRatioTestCase(test_name="unit square", width=1, height=1, expected=1.0),
    AspectRatioTestCase(test_name="square", width=10, height=10, expected=1.0),
    # --- negative dimensions ---
    AspectRatioTestCase(test_name="both negative", width=-20, height=-10, expected=2.0),
    AspectRatioTestCase(test_name="negative width", width=-20, height=10, expected=2.0),
    AspectRatioTestCase(test_name="negative height", width=20, height=-10, expected=2.0),
    AspectRatioTestCase(test_name="negative square", width=-10, height=-10, expected=1.0),
    AspectRatioTestCase(test_name="negative taller than wide", width=-10, height=-20, expected=0.5),
    # --- float ---
    AspectRatioTestCase(test_name="float dimensions", width=3.0, height=1.5, expected=2.0),
    AspectRatioTestCase(test_name="float negative", width=-3.0, height=-1.5, expected=2.0),
]


@dataclass(frozen=True)
class DiagonalTestCase:
    test_name: str
    width: float
    height: float
    expected: float


DIAGONAL_TEST_CASES = [
    # --- normal ---
    DiagonalTestCase(test_name="square", width=10, height=10, expected=math.hypot(10, 10)),
    DiagonalTestCase(test_name="non-square", width=3, height=4, expected=5.0),  # 3-4-5 right triangle
    DiagonalTestCase(test_name="unit square", width=1, height=1, expected=math.sqrt(2)),
    # --- negative dimensions ---
    DiagonalTestCase(test_name="both negative", width=-10, height=-10, expected=math.hypot(10, 10)),
    DiagonalTestCase(test_name="negative width", width=-3, height=4, expected=5.0),
    DiagonalTestCase(test_name="negative height", width=3, height=-4, expected=5.0),
    DiagonalTestCase(test_name="negative non-square", width=-3, height=-4, expected=5.0),
    # --- zero ---
    DiagonalTestCase(test_name="zero width", width=0, height=10, expected=10.0),
    DiagonalTestCase(test_name="zero height", width=10, height=0, expected=10.0),
    DiagonalTestCase(test_name="both zero", width=0, height=0, expected=0.0),
    # --- float ---
    DiagonalTestCase(test_name="float dimensions", width=1.5, height=2.0, expected=math.hypot(1.5, 2.0)),
    DiagonalTestCase(test_name="float negative", width=-1.5, height=-2.0, expected=math.hypot(1.5, 2.0)),
]


@dataclass(frozen=True, slots=True)
class CornersTestCase:
    test_name: str
    x: float
    y: float
    width: float
    height: float
    expected_tl: tuple[float, float]
    expected_tr: tuple[float, float]
    expected_br: tuple[float, float]
    expected_bl: tuple[float, float]


CORNER_TEST_CASES = [
    # --- same region [0,10]x[0,10], different stored sign ---
    CornersTestCase(
        test_name="normal",
        x=0,
        y=0,
        width=10,
        height=10,
        expected_tl=(0, 0),
        expected_tr=(10, 0),
        expected_br=(10, 10),
        expected_bl=(0, 10),
    ),
    CornersTestCase(
        test_name="negative w/h",
        x=10,
        y=10,
        width=-10,
        height=-10,
        expected_tl=(0, 0),
        expected_tr=(10, 0),
        expected_br=(10, 10),
        expected_bl=(0, 10),
    ),
    CornersTestCase(
        test_name="negative width",
        x=10,
        y=0,
        width=-10,
        height=10,
        expected_tl=(0, 0),
        expected_tr=(10, 0),
        expected_br=(10, 10),
        expected_bl=(0, 10),
    ),
    CornersTestCase(
        test_name="negative height",
        x=0,
        y=10,
        width=10,
        height=-10,
        expected_tl=(0, 0),
        expected_tr=(10, 0),
        expected_br=(10, 10),
        expected_bl=(0, 10),
    ),
    # --- offset origin ---
    CornersTestCase(
        test_name="offset origin",
        x=5,
        y=3,
        width=10,
        height=7,
        expected_tl=(5, 3),
        expected_tr=(15, 3),
        expected_br=(15, 10),
        expected_bl=(5, 10),
    ),
    # --- negative origin ---
    CornersTestCase(
        test_name="negative origin",
        x=-4,
        y=-4,
        width=8,
        height=8,
        expected_tl=(-4, -4),
        expected_tr=(4, -4),
        expected_br=(4, 4),
        expected_bl=(-4, 4),
    ),
    # --- fully negative quadrant ---
    CornersTestCase(
        test_name="fully negative",
        x=-10,
        y=-10,
        width=4,
        height=4,
        expected_tl=(-10, -10),
        expected_tr=(-6, -10),
        expected_br=(-6, -6),
        expected_bl=(-10, -6),
    ),
    # --- degenerate: zero width (vertical line) ---
    CornersTestCase(
        test_name="zero width",
        x=5,
        y=0,
        width=0,
        height=10,
        expected_tl=(5, 0),
        expected_tr=(5, 0),
        expected_br=(5, 10),
        expected_bl=(5, 10),
    ),
    # --- degenerate: zero height (horizontal line) ---
    CornersTestCase(
        test_name="zero height",
        x=0,
        y=5,
        width=10,
        height=0,
        expected_tl=(0, 5),
        expected_tr=(10, 5),
        expected_br=(10, 5),
        expected_bl=(0, 5),
    ),
    # --- degenerate: point ---
    CornersTestCase(
        test_name="point",
        x=3,
        y=7,
        width=0,
        height=0,
        expected_tl=(3, 7),
        expected_tr=(3, 7),
        expected_br=(3, 7),
        expected_bl=(3, 7),
    ),
    # --- float ---
    CornersTestCase(
        test_name="float",
        x=0.5,
        y=1.5,
        width=3.0,
        height=2.0,
        expected_tl=(0.5, 1.5),
        expected_tr=(3.5, 1.5),
        expected_br=(3.5, 3.5),
        expected_bl=(0.5, 3.5),
    ),
]


@dataclass(frozen=True, slots=True)
class IsEmptyTestCase:
    test_name: str
    width: float
    height: float
    expected: bool


IS_EMPTY_TEST_CASES = [
    # --- not empty ---
    IsEmptyTestCase(test_name="normal", width=10, height=10, expected=False),
    IsEmptyTestCase(test_name="non-square", width=10, height=5, expected=False),
    IsEmptyTestCase(test_name="unit square", width=1, height=1, expected=False),
    IsEmptyTestCase(test_name="negative w/h", width=-10, height=-10, expected=False),
    IsEmptyTestCase(test_name="negative width", width=-10, height=10, expected=False),
    IsEmptyTestCase(test_name="negative height", width=10, height=-10, expected=False),
    IsEmptyTestCase(test_name="float dimensions", width=0.1, height=0.1, expected=False),
    IsEmptyTestCase(test_name="near zero not empty", width=0.001, height=0.001, expected=False),
    # --- empty ---
    IsEmptyTestCase(test_name="zero width", width=0, height=10, expected=True),
    IsEmptyTestCase(test_name="zero height", width=10, height=0, expected=True),
    IsEmptyTestCase(test_name="both zero", width=0, height=0, expected=True),
    IsEmptyTestCase(test_name="zero width negative h", width=0, height=-10, expected=True),
    IsEmptyTestCase(test_name="zero height negative w", width=-10, height=0, expected=True),
]


@dataclass(frozen=True, slots=True)
class IsNonNegativeTestCase:
    test_name: str
    x: float
    y: float
    width: float
    height: float
    expected: bool


IS_NON_NEGATIVE_TEST_CASES = [
    # --- all non-negative ---
    IsNonNegativeTestCase(test_name="all zero", x=0, y=0, width=0, height=0, expected=True),
    IsNonNegativeTestCase(test_name="all non-negative", x=0, y=0, width=10, height=10, expected=True),
    IsNonNegativeTestCase(test_name="positive x/y", x=5, y=5, width=10, height=10, expected=True),
    IsNonNegativeTestCase(test_name="float non-negative", x=0.5, y=0.5, width=1.5, height=2.5, expected=True),
    # --- single negative field ---
    IsNonNegativeTestCase(test_name="negative x", x=-1, y=0, width=10, height=10, expected=False),
    IsNonNegativeTestCase(test_name="negative y", x=0, y=-1, width=10, height=10, expected=False),
    IsNonNegativeTestCase(test_name="negative width", x=0, y=0, width=-10, height=10, expected=False),
    IsNonNegativeTestCase(test_name="negative height", x=0, y=0, width=10, height=-10, expected=False),
    # --- multiple negative fields ---
    IsNonNegativeTestCase(test_name="negative x/y", x=-1, y=-1, width=10, height=10, expected=False),
    IsNonNegativeTestCase(test_name="negative w/h", x=0, y=0, width=-10, height=-10, expected=False),
    IsNonNegativeTestCase(test_name="all negative", x=-1, y=-1, width=-10, height=-10, expected=False),
    # --- near zero ---
    IsNonNegativeTestCase(test_name="near zero negative x", x=-0.001, y=0, width=10, height=10, expected=False),
    IsNonNegativeTestCase(test_name="near zero positive x", x=0.001, y=0, width=10, height=10, expected=True),
]


@dataclass(frozen=True, slots=True)
class ContainsPointTestCase:
    test_name: str
    px: float
    py: float
    expected: bool


CONTAINS_POINT_TEST_CASES = [
    # --- interior ---
    ContainsPointTestCase(test_name="interior center", px=5, py=5, expected=True),
    ContainsPointTestCase(test_name="interior off-center", px=3, py=7, expected=True),
    # --- corners (boundary) ---
    ContainsPointTestCase(test_name="corner top-left", px=0, py=0, expected=True),
    ContainsPointTestCase(test_name="corner top-right", px=10, py=0, expected=True),
    ContainsPointTestCase(test_name="corner bottom-right", px=10, py=10, expected=True),
    ContainsPointTestCase(test_name="corner bottom-left", px=0, py=10, expected=True),
    # --- edge midpoints (boundary) ---
    ContainsPointTestCase(test_name="edge top", px=5, py=0, expected=True),
    ContainsPointTestCase(test_name="edge bottom", px=5, py=10, expected=True),
    ContainsPointTestCase(test_name="edge left", px=0, py=5, expected=True),
    ContainsPointTestCase(test_name="edge right", px=10, py=5, expected=True),
    # --- just outside each edge ---
    ContainsPointTestCase(test_name="just outside top", px=5, py=-1, expected=False),
    ContainsPointTestCase(test_name="just outside bottom", px=5, py=11, expected=False),
    ContainsPointTestCase(test_name="just outside left", px=-1, py=5, expected=False),
    ContainsPointTestCase(test_name="just outside right", px=11, py=5, expected=False),
    # --- just outside corners ---
    ContainsPointTestCase(test_name="just outside corner tl", px=-1, py=-1, expected=False),
    ContainsPointTestCase(test_name="just outside corner br", px=11, py=11, expected=False),
    # --- float ---
    ContainsPointTestCase(test_name="float interior", px=5.5, py=5.5, expected=True),
    ContainsPointTestCase(test_name="float just inside edge", px=9.999, py=5, expected=True),
    ContainsPointTestCase(test_name="float just outside edge", px=10.001, py=5, expected=False),
]


@dataclass(frozen=True, slots=True)
class ContainsRectTestCase:
    test_name: str
    ix: float
    iy: float
    iw: float
    ih: float
    expected: bool


CONTAINS_RECT_TEST_CASES = [
    # --- fully inside ---
    ContainsRectTestCase(test_name="fully inside", ix=2, iy=2, iw=6, ih=6, expected=True),
    ContainsRectTestCase(test_name="fully inside off-center", ix=1, iy=3, iw=4, ih=5, expected=True),
    # --- flush (exact boundary) ---
    ContainsRectTestCase(test_name="flush all sides", ix=0, iy=0, iw=10, ih=10, expected=True),
    ContainsRectTestCase(test_name="flush left edge", ix=0, iy=2, iw=5, ih=5, expected=True),
    ContainsRectTestCase(test_name="flush right edge", ix=5, iy=2, iw=5, ih=5, expected=True),
    ContainsRectTestCase(test_name="flush top edge", ix=2, iy=0, iw=5, ih=5, expected=True),
    ContainsRectTestCase(test_name="flush bottom edge", ix=2, iy=5, iw=5, ih=5, expected=True),
    # --- overflows one side ---
    ContainsRectTestCase(test_name="overflows right", ix=5, iy=2, iw=10, ih=5, expected=False),
    ContainsRectTestCase(test_name="overflows left", ix=-1, iy=2, iw=5, ih=5, expected=False),
    ContainsRectTestCase(test_name="overflows bottom", ix=2, iy=5, iw=5, ih=10, expected=False),
    ContainsRectTestCase(test_name="overflows top", ix=2, iy=-1, iw=5, ih=5, expected=False),
    # --- overflows multiple sides ---
    ContainsRectTestCase(test_name="overflows all sides", ix=-1, iy=-1, iw=12, ih=12, expected=False),
    ContainsRectTestCase(test_name="overflows right and bottom", ix=5, iy=5, iw=10, ih=10, expected=False),
    # --- completely outside ---
    ContainsRectTestCase(test_name="outside right", ix=11, iy=0, iw=5, ih=5, expected=False),
    ContainsRectTestCase(test_name="outside left", ix=-6, iy=0, iw=5, ih=5, expected=False),
    ContainsRectTestCase(test_name="outside top", ix=0, iy=-6, iw=5, ih=5, expected=False),
    ContainsRectTestCase(test_name="outside bottom", ix=0, iy=11, iw=5, ih=5, expected=False),
    ContainsRectTestCase(test_name="outside diagonal", ix=15, iy=15, iw=5, ih=5, expected=False),
    # --- degenerate inner ---
    ContainsRectTestCase(test_name="inner zero width", ix=5, iy=5, iw=0, ih=5, expected=True),
    ContainsRectTestCase(test_name="inner zero height", ix=5, iy=5, iw=5, ih=0, expected=True),
    ContainsRectTestCase(test_name="inner point", ix=5, iy=5, iw=0, ih=0, expected=True),
    ContainsRectTestCase(test_name="inner point on boundary", ix=10, iy=10, iw=0, ih=0, expected=True),
    ContainsRectTestCase(test_name="inner point outside", ix=11, iy=11, iw=0, ih=0, expected=False),
    # --- negative inner dimensions (same region) ---
    ContainsRectTestCase(test_name="inner negative w/h inside", ix=8, iy=8, iw=-6, ih=-6, expected=True),
    ContainsRectTestCase(test_name="inner negative w/h overflow", ix=12, iy=12, iw=-6, ih=-6, expected=False),
]


@dataclass(frozen=True, slots=True)
class TwoRectTestCase:
    test_name: str
    ax: float
    ay: float
    aw: float
    ah: float
    bx: float
    by: float
    bw: float
    bh: float
    expected: bool


TWO_RECT_TEST_CASES_INTERSECTS = [
    # --- overlapping (positive area) ---
    TwoRectTestCase(test_name="partial overlap", ax=0, ay=0, aw=10, ah=10, bx=5, by=5, bw=10, bh=10, expected=True),
    TwoRectTestCase(test_name="one contains other", ax=0, ay=0, aw=10, ah=10, bx=2, by=2, bw=6, bh=6, expected=True),
    TwoRectTestCase(test_name="identical", ax=0, ay=0, aw=10, ah=10, bx=0, by=0, bw=10, bh=10, expected=True),
    TwoRectTestCase(
        test_name="overlap horizontal strip", ax=0, ay=0, aw=10, ah=10, bx=5, by=0, bw=10, bh=10, expected=True
    ),
    TwoRectTestCase(
        test_name="overlap vertical strip", ax=0, ay=0, aw=10, ah=10, bx=0, by=5, bw=10, bh=10, expected=True
    ),
    # --- negative dimensions same region ---
    TwoRectTestCase(
        test_name="negative wh partial overlap", ax=10, ay=10, aw=-10, ah=-10, bx=5, by=5, bw=10, bh=10, expected=True
    ),
    # --- edge touch → False ---
    TwoRectTestCase(test_name="edge touch right", ax=0, ay=0, aw=10, ah=10, bx=10, by=0, bw=10, bh=10, expected=False),
    TwoRectTestCase(test_name="edge touch left", ax=10, ay=0, aw=10, ah=10, bx=0, by=0, bw=10, bh=10, expected=False),
    TwoRectTestCase(test_name="edge touch bottom", ax=0, ay=0, aw=10, ah=10, bx=0, by=10, bw=10, bh=10, expected=False),
    TwoRectTestCase(test_name="edge touch top", ax=0, ay=10, aw=10, ah=10, bx=0, by=0, bw=10, bh=10, expected=False),
    # --- corner touch → False ---
    TwoRectTestCase(test_name="corner touch top-left", ax=5, ay=5, aw=5, ah=5, bx=0, by=0, bw=5, bh=5, expected=False),
    TwoRectTestCase(test_name="corner touch top-right", ax=0, ay=5, aw=5, ah=5, bx=5, by=0, bw=5, bh=5, expected=False),
    TwoRectTestCase(
        test_name="corner touch bottom-right", ax=0, ay=0, aw=5, ah=5, bx=5, by=5, bw=5, bh=5, expected=False
    ),
    TwoRectTestCase(
        test_name="corner touch bottom-left", ax=5, ay=0, aw=5, ah=5, bx=0, by=5, bw=5, bh=5, expected=False
    ),
    # --- disjoint ---
    TwoRectTestCase(test_name="disjoint horizontal", ax=0, ay=0, aw=5, ah=5, bx=10, by=0, bw=5, bh=5, expected=False),
    TwoRectTestCase(test_name="disjoint vertical", ax=0, ay=0, aw=5, ah=5, bx=0, by=10, bw=5, bh=5, expected=False),
    TwoRectTestCase(test_name="disjoint diagonal", ax=0, ay=0, aw=5, ah=5, bx=10, by=10, bw=5, bh=5, expected=False),
]

TWO_RECT_TEST_CASES_TOUCHES = [
    # --- overlapping → True ---
    TwoRectTestCase(test_name="partial overlap", ax=0, ay=0, aw=10, ah=10, bx=5, by=5, bw=10, bh=10, expected=True),
    TwoRectTestCase(test_name="one contains other", ax=0, ay=0, aw=10, ah=10, bx=2, by=2, bw=6, bh=6, expected=True),
    TwoRectTestCase(test_name="identical", ax=0, ay=0, aw=10, ah=10, bx=0, by=0, bw=10, bh=10, expected=True),
    # --- edge touch → True ---
    TwoRectTestCase(test_name="edge touch right", ax=0, ay=0, aw=10, ah=10, bx=10, by=0, bw=10, bh=10, expected=True),
    TwoRectTestCase(test_name="edge touch left", ax=10, ay=0, aw=10, ah=10, bx=0, by=0, bw=10, bh=10, expected=True),
    TwoRectTestCase(test_name="edge touch bottom", ax=0, ay=0, aw=10, ah=10, bx=0, by=10, bw=10, bh=10, expected=True),
    TwoRectTestCase(test_name="edge touch top", ax=0, ay=10, aw=10, ah=10, bx=0, by=0, bw=10, bh=10, expected=True),
    # --- corner touch → True ---
    TwoRectTestCase(test_name="corner touch top-left", ax=5, ay=5, aw=5, ah=5, bx=0, by=0, bw=5, bh=5, expected=True),
    TwoRectTestCase(test_name="corner touch top-right", ax=0, ay=5, aw=5, ah=5, bx=5, by=0, bw=5, bh=5, expected=True),
    TwoRectTestCase(
        test_name="corner touch bottom-right", ax=0, ay=0, aw=5, ah=5, bx=5, by=5, bw=5, bh=5, expected=True
    ),
    TwoRectTestCase(
        test_name="corner touch bottom-left", ax=5, ay=0, aw=5, ah=5, bx=0, by=5, bw=5, bh=5, expected=True
    ),
    # --- negative dimensions ---
    TwoRectTestCase(
        test_name="negative wh edge touch", ax=10, ay=10, aw=-10, ah=-10, bx=10, by=0, bw=10, bh=10, expected=True
    ),
    # --- disjoint → False ---
    TwoRectTestCase(test_name="disjoint horizontal", ax=0, ay=0, aw=5, ah=5, bx=10, by=0, bw=5, bh=5, expected=False),
    TwoRectTestCase(test_name="disjoint vertical", ax=0, ay=0, aw=5, ah=5, bx=0, by=10, bw=5, bh=5, expected=False),
    TwoRectTestCase(test_name="disjoint diagonal", ax=0, ay=0, aw=5, ah=5, bx=10, by=10, bw=5, bh=5, expected=False),
]


@dataclass(frozen=True, slots=True)
class IntersectionTestCase:
    test_name: str
    ax: float
    ay: float
    aw: float
    ah: float
    bx: float
    by: float
    bw: float
    bh: float
    expected: Rectangle | None


INTERSECTION_TEST_CASES = [
    # --- overlapping (positive area) ---
    IntersectionTestCase(
        test_name="partial overlap diagonal",
        ax=0,
        ay=0,
        aw=10,
        ah=10,
        bx=5,
        by=5,
        bw=10,
        bh=10,
        expected=Rectangle(x=5, y=5, width=5, height=5),
    ),
    IntersectionTestCase(
        test_name="partial overlap horizontal strip",
        ax=0,
        ay=0,
        aw=10,
        ah=10,
        bx=5,
        by=0,
        bw=10,
        bh=10,
        expected=Rectangle(x=5, y=0, width=5, height=10),
    ),
    IntersectionTestCase(
        test_name="partial overlap vertical strip",
        ax=0,
        ay=0,
        aw=10,
        ah=10,
        bx=0,
        by=5,
        bw=10,
        bh=10,
        expected=Rectangle(x=0, y=5, width=10, height=5),
    ),
    IntersectionTestCase(
        test_name="one contains other",
        ax=0,
        ay=0,
        aw=10,
        ah=10,
        bx=2,
        by=2,
        bw=6,
        bh=6,
        expected=Rectangle(x=2, y=2, width=6, height=6),
    ),
    IntersectionTestCase(
        test_name="identical",
        ax=0,
        ay=0,
        aw=10,
        ah=10,
        bx=0,
        by=0,
        bw=10,
        bh=10,
        expected=Rectangle(x=0, y=0, width=10, height=10),
    ),
    # --- negative dimensions (same region) ---
    IntersectionTestCase(
        test_name="negative wh partial overlap",
        ax=10,
        ay=10,
        aw=-10,
        ah=-10,
        bx=5,
        by=5,
        bw=10,
        bh=10,
        expected=Rectangle(x=5, y=5, width=5, height=5),
    ),
    IntersectionTestCase(
        test_name="both negative wh identical region",
        ax=10,
        ay=10,
        aw=-10,
        ah=-10,
        bx=0,
        by=0,
        bw=10,
        bh=10,
        expected=Rectangle(x=0, y=0, width=10, height=10),
    ),
    # --- edge touch → None ---
    IntersectionTestCase(
        test_name="edge touch right",
        ax=0,
        ay=0,
        aw=10,
        ah=10,
        bx=10,
        by=0,
        bw=10,
        bh=10,
        expected=None,
    ),
    IntersectionTestCase(
        test_name="edge touch left",
        ax=10,
        ay=0,
        aw=10,
        ah=10,
        bx=0,
        by=0,
        bw=10,
        bh=10,
        expected=None,
    ),
    IntersectionTestCase(
        test_name="edge touch bottom",
        ax=0,
        ay=0,
        aw=10,
        ah=10,
        bx=0,
        by=10,
        bw=10,
        bh=10,
        expected=None,
    ),
    IntersectionTestCase(
        test_name="edge touch top",
        ax=0,
        ay=10,
        aw=10,
        ah=10,
        bx=0,
        by=0,
        bw=10,
        bh=10,
        expected=None,
    ),
    # --- corner touch → None ---
    IntersectionTestCase(
        test_name="corner touch bottom-right",
        ax=0,
        ay=0,
        aw=5,
        ah=5,
        bx=5,
        by=5,
        bw=5,
        bh=5,
        expected=None,
    ),
    IntersectionTestCase(
        test_name="corner touch bottom-left",
        ax=5,
        ay=0,
        aw=5,
        ah=5,
        bx=0,
        by=5,
        bw=5,
        bh=5,
        expected=None,
    ),
    IntersectionTestCase(
        test_name="corner touch top-right",
        ax=0,
        ay=5,
        aw=5,
        ah=5,
        bx=5,
        by=0,
        bw=5,
        bh=5,
        expected=None,
    ),
    IntersectionTestCase(
        test_name="corner touch top-left",
        ax=5,
        ay=5,
        aw=5,
        ah=5,
        bx=0,
        by=0,
        bw=5,
        bh=5,
        expected=None,
    ),
    # --- disjoint → None ---
    IntersectionTestCase(
        test_name="disjoint horizontal",
        ax=0,
        ay=0,
        aw=5,
        ah=5,
        bx=10,
        by=0,
        bw=5,
        bh=5,
        expected=None,
    ),
    IntersectionTestCase(
        test_name="disjoint vertical",
        ax=0,
        ay=0,
        aw=5,
        ah=5,
        bx=0,
        by=10,
        bw=5,
        bh=5,
        expected=None,
    ),
    IntersectionTestCase(
        test_name="disjoint diagonal",
        ax=0,
        ay=0,
        aw=5,
        ah=5,
        bx=10,
        by=10,
        bw=5,
        bh=5,
        expected=None,
    ),
]


@dataclass(frozen=True, slots=True)
class UnionTestCase:
    test_name: str
    ax: float
    ay: float
    aw: float
    ah: float
    bx: float
    by: float
    bw: float
    bh: float
    expected: Rectangle


UNION_TEST_CASES = [
    # --- overlapping ---
    UnionTestCase(
        test_name="partial overlap diagonal",
        ax=0,
        ay=0,
        aw=10,
        ah=10,
        bx=5,
        by=5,
        bw=10,
        bh=10,
        expected=Rectangle(x=0, y=0, width=15, height=15),
    ),
    UnionTestCase(
        test_name="partial overlap horizontal strip",
        ax=0,
        ay=0,
        aw=10,
        ah=10,
        bx=5,
        by=0,
        bw=10,
        bh=10,
        expected=Rectangle(x=0, y=0, width=15, height=10),
    ),
    UnionTestCase(
        test_name="partial overlap vertical strip",
        ax=0,
        ay=0,
        aw=10,
        ah=10,
        bx=0,
        by=5,
        bw=10,
        bh=10,
        expected=Rectangle(x=0, y=0, width=10, height=15),
    ),
    # --- containment ---
    UnionTestCase(
        test_name="one contains other",
        ax=0,
        ay=0,
        aw=10,
        ah=10,
        bx=2,
        by=2,
        bw=6,
        bh=6,
        expected=Rectangle(x=0, y=0, width=10, height=10),
    ),
    UnionTestCase(
        test_name="identical",
        ax=0,
        ay=0,
        aw=10,
        ah=10,
        bx=0,
        by=0,
        bw=10,
        bh=10,
        expected=Rectangle(x=0, y=0, width=10, height=10),
    ),
    # --- touching ---
    UnionTestCase(
        test_name="edge touch right",
        ax=0,
        ay=0,
        aw=10,
        ah=10,
        bx=10,
        by=0,
        bw=10,
        bh=10,
        expected=Rectangle(x=0, y=0, width=20, height=10),
    ),
    UnionTestCase(
        test_name="edge touch bottom",
        ax=0,
        ay=0,
        aw=10,
        ah=10,
        bx=0,
        by=10,
        bw=10,
        bh=10,
        expected=Rectangle(x=0, y=0, width=10, height=20),
    ),
    UnionTestCase(
        test_name="corner touch",
        ax=0,
        ay=0,
        aw=5,
        ah=5,
        bx=5,
        by=5,
        bw=5,
        bh=5,
        expected=Rectangle(x=0, y=0, width=10, height=10),
    ),
    # --- disjoint ---
    UnionTestCase(
        test_name="disjoint diagonal",
        ax=0,
        ay=0,
        aw=5,
        ah=5,
        bx=10,
        by=10,
        bw=5,
        bh=5,
        expected=Rectangle(x=0, y=0, width=15, height=15),
    ),
    UnionTestCase(
        test_name="disjoint horizontal",
        ax=0,
        ay=0,
        aw=5,
        ah=5,
        bx=10,
        by=0,
        bw=5,
        bh=5,
        expected=Rectangle(x=0, y=0, width=15, height=5),
    ),
    UnionTestCase(
        test_name="disjoint vertical",
        ax=0,
        ay=0,
        aw=5,
        ah=5,
        bx=0,
        by=10,
        bw=5,
        bh=5,
        expected=Rectangle(x=0, y=0, width=5, height=15),
    ),
    # --- negative origin ---
    UnionTestCase(
        test_name="negative origin",
        ax=-5,
        ay=-5,
        aw=5,
        ah=5,
        bx=0,
        by=0,
        bw=5,
        bh=5,
        expected=Rectangle(x=-5, y=-5, width=10, height=10),
    ),
    # --- negative dimensions ---
    UnionTestCase(
        test_name="negative wh same region as positive",
        ax=0,
        ay=0,
        aw=10,
        ah=10,
        bx=10,
        by=10,
        bw=-10,
        bh=-10,
        expected=Rectangle(x=0, y=0, width=10, height=10),
    ),
    UnionTestCase(
        test_name="both negative wh disjoint regions",
        ax=10,
        ay=10,
        aw=-10,
        ah=-10,
        bx=15,
        by=15,
        bw=5,
        bh=5,
        expected=Rectangle(x=0, y=0, width=20, height=20),
    ),
    # --- float ---
    UnionTestCase(
        test_name="float dimensions",
        ax=0.0,
        ay=0.0,
        aw=5.5,
        ah=5.5,
        bx=3.0,
        by=3.0,
        bw=5.5,
        bh=5.5,
        expected=Rectangle(x=0.0, y=0.0, width=8.5, height=8.5),
    ),
]


@dataclass(frozen=True, slots=True)
class DistanceTestCase:
    test_name: str
    ax: float
    ay: float
    aw: float
    ah: float
    bx: float
    by: float
    bw: float
    bh: float
    expected: float


DISTANCE_TEST_CASES = [
    # --- zero distance: overlapping ---
    DistanceTestCase(test_name="overlapping partial", ax=0, ay=0, aw=10, ah=10, bx=5, by=5, bw=10, bh=10, expected=0.0),
    DistanceTestCase(test_name="one contains other", ax=0, ay=0, aw=10, ah=10, bx=2, by=2, bw=6, bh=6, expected=0.0),
    DistanceTestCase(test_name="identical", ax=0, ay=0, aw=10, ah=10, bx=0, by=0, bw=10, bh=10, expected=0.0),
    # --- zero distance: touching ---
    DistanceTestCase(test_name="touch edge right", ax=0, ay=0, aw=10, ah=10, bx=10, by=0, bw=10, bh=10, expected=0.0),
    DistanceTestCase(test_name="touch edge left", ax=10, ay=0, aw=10, ah=10, bx=0, by=0, bw=10, bh=10, expected=0.0),
    DistanceTestCase(test_name="touch edge bottom", ax=0, ay=0, aw=10, ah=10, bx=0, by=10, bw=10, bh=10, expected=0.0),
    DistanceTestCase(test_name="touch edge top", ax=0, ay=10, aw=10, ah=10, bx=0, by=0, bw=10, bh=10, expected=0.0),
    DistanceTestCase(test_name="touch corner", ax=0, ay=0, aw=5, ah=5, bx=5, by=5, bw=5, bh=5, expected=0.0),
    # --- axis-aligned gaps ---
    DistanceTestCase(test_name="horizontal gap", ax=0, ay=0, aw=5, ah=5, bx=10, by=0, bw=5, bh=5, expected=5.0),
    DistanceTestCase(test_name="horizontal gap left", ax=10, ay=0, aw=5, ah=5, bx=0, by=0, bw=5, bh=5, expected=5.0),
    DistanceTestCase(test_name="vertical gap", ax=0, ay=0, aw=5, ah=5, bx=0, by=10, bw=5, bh=5, expected=5.0),
    DistanceTestCase(test_name="vertical gap above", ax=0, ay=10, aw=5, ah=5, bx=0, by=0, bw=5, bh=5, expected=5.0),
    # --- diagonal gaps ---
    DistanceTestCase(
        test_name="diagonal gap", ax=0, ay=0, aw=5, ah=5, bx=8, by=8, bw=5, bh=5, expected=math.hypot(3, 3)
    ),
    DistanceTestCase(
        test_name="diagonal gap top-left", ax=8, ay=8, aw=5, ah=5, bx=0, by=0, bw=5, bh=5, expected=math.hypot(3, 3)
    ),
    DistanceTestCase(
        test_name="diagonal gap top-right", ax=0, ay=8, aw=5, ah=5, bx=8, by=0, bw=5, bh=5, expected=math.hypot(3, 3)
    ),
    DistanceTestCase(
        test_name="diagonal gap bottom-left", ax=8, ay=0, aw=5, ah=5, bx=0, by=8, bw=5, bh=5, expected=math.hypot(3, 3)
    ),
    # --- negative dimensions ---
    DistanceTestCase(
        test_name="negative wh horizontal gap", ax=5, ay=5, aw=-5, ah=-5, bx=10, by=0, bw=5, bh=5, expected=5.0
    ),
    DistanceTestCase(
        test_name="negative wh touching", ax=10, ay=10, aw=-10, ah=-10, bx=10, by=0, bw=10, bh=10, expected=0.0
    ),
    # --- float ---
    DistanceTestCase(
        test_name="float gap", ax=0.0, ay=0.0, aw=5.0, ah=5.0, bx=7.5, by=0.0, bw=5.0, bh=5.0, expected=2.5
    ),
]
