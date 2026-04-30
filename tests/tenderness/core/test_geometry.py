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

import pytest

from tenderness.core.geometry import Margin, Rectangle
from tests.tenderness.core.test_cases.geometry import (
    AREA_TEST_CASES,
    ASPECT_RATIO_TEST_CASES,
    CENTER_TEST_CASES,
    CONTAINS_POINT_TEST_CASES,
    CONTAINS_RECT_TEST_CASES,
    CORNER_TEST_CASES,
    DIAGONAL_TEST_CASES,
    DISTANCE_TEST_CASES,
    INTERSECTION_TEST_CASES,
    IS_EMPTY_TEST_CASES,
    IS_NON_NEGATIVE_TEST_CASES,
    NORMALIZED_BOUNDS_TEST_CASES,
    PERIMETER_TEST_CASES,
    SIZE_TEST_CASES,
    TWO_RECT_TEST_CASES_INTERSECTS,
    TWO_RECT_TEST_CASES_TOUCHES,
    UNION_TEST_CASES,
    AreaTestCase,
    AspectRatioTestCase,
    CenterTestCase,
    ContainsPointTestCase,
    ContainsRectTestCase,
    CornersTestCase,
    DiagonalTestCase,
    DistanceTestCase,
    IntersectionTestCase,
    IsEmptyTestCase,
    IsNonNegativeTestCase,
    NormalizedBoundsTestCase,
    PerimeterTestCase,
    SizeTestCase,
    TwoRectTestCase,
    UnionTestCase,
)


# --------------------------
# Tests for Margin
# --------------------------
class TestMarginDefaults:
    def test_all_sides_default_to_zero(self) -> None:
        m = Margin()
        assert m.top == 0.0
        assert m.right == 0.0
        assert m.bottom == 0.0
        assert m.left == 0.0


class TestRectangleInset:
    def test_uniform_margin_shrinks_all_sides(self) -> None:
        r = Rectangle(x=0.0, y=0.0, width=100.0, height=60.0)
        result = r.inset(Margin(top=10.0, right=10.0, bottom=10.0, left=10.0))
        assert result == Rectangle(x=10.0, y=10.0, width=80.0, height=40.0)

    def test_zero_margin_returns_identical(self) -> None:
        r = Rectangle(x=5.0, y=5.0, width=50.0, height=30.0)
        assert r.inset(Margin()) == r

    def test_asymmetric_margin(self) -> None:
        r = Rectangle(x=0.0, y=0.0, width=100.0, height=100.0)
        result = r.inset(Margin(top=10.0, right=20.0, bottom=30.0, left=5.0))
        assert result.x == pytest.approx(5.0)
        assert result.y == pytest.approx(10.0)
        assert result.width == pytest.approx(75.0)  # 100 - 5 - 20
        assert result.height == pytest.approx(60.0)  # 100 - 10 - 30

    def test_non_zero_origin_rectangle(self) -> None:
        r = Rectangle(x=50.0, y=20.0, width=200.0, height=100.0)
        result = r.inset(Margin(top=10.0, right=15.0, bottom=10.0, left=15.0))
        assert result.x == pytest.approx(65.0)  # 50 + 15
        assert result.y == pytest.approx(30.0)  # 20 + 10
        assert result.width == pytest.approx(170.0)  # 200 - 15 - 15
        assert result.height == pytest.approx(80.0)  # 100 - 10 - 10

    def test_negative_margin_expands_rectangle(self) -> None:
        r = Rectangle(x=10.0, y=10.0, width=50.0, height=50.0)
        result = r.inset(Margin(top=-5.0, right=-5.0, bottom=-5.0, left=-5.0))
        assert result.x == pytest.approx(5.0)
        assert result.y == pytest.approx(5.0)
        assert result.width == pytest.approx(60.0)
        assert result.height == pytest.approx(60.0)

    def test_works_from_safe_bounds_for_negative_wh(self) -> None:
        # Rectangle stored with negative dimensions — inset uses _x_min/_y_min
        r = Rectangle(x=100.0, y=60.0, width=-100.0, height=-60.0)
        result = r.inset(Margin(top=10.0, right=10.0, bottom=10.0, left=10.0))
        assert result == Rectangle(x=10.0, y=10.0, width=80.0, height=40.0)

    def test_returns_new_rectangle_instance(self) -> None:
        r = Rectangle(x=0.0, y=0.0, width=100.0, height=100.0)
        result = r.inset(Margin(top=5.0, right=5.0, bottom=5.0, left=5.0))
        assert result is not r


# --------------------------
# Tests for Rectangle
# --------------------------
class TestConstruction:
    def test_stores_fields(self) -> None:
        r = Rectangle(x=1, y=2, width=3, height=4)
        assert r.x == 1
        assert r.y == 2
        assert r.width == 3
        assert r.height == 4

    def test_frozen(self) -> None:
        r = Rectangle(x=0, y=0, width=10, height=10)
        with pytest.raises((AttributeError, TypeError)):
            r.x = 99  # type: ignore[misc]

    @pytest.mark.parametrize(
        "test_case",
        NORMALIZED_BOUNDS_TEST_CASES,
        ids=lambda c: c.test_name,
    )
    def test_normalized_bounds(self, test_case: NormalizedBoundsTestCase) -> None:
        r = Rectangle(x=test_case.x, y=test_case.y, width=test_case.width, height=test_case.height)
        assert r.x_min == test_case.x_min
        assert r.x_max == test_case.x_max
        assert r.y_min == test_case.y_min
        assert r.y_max == test_case.y_max

    def test_float_fields(self) -> None:
        r = Rectangle(x=1.5, y=2.5, width=3.5, height=4.5)
        assert r.x_min == pytest.approx(1.5)
        assert r.x_max == pytest.approx(5.0)


class TestEqualityAndHash:
    def test_same_fields_equal(self) -> None:
        assert Rectangle(x=0, y=0, width=10, height=10) == Rectangle(x=0, y=0, width=10, height=10)
        assert Rectangle(x=10, y=10, width=-10, height=-10) == Rectangle(x=10, y=10, width=-10, height=-10)

    def test_same_region_different_stored_fields_not_equal(self) -> None:
        """Same geometric region but different origin/sign → not equal (field-level equality)."""
        assert Rectangle(x=0, y=0, width=10, height=10) != Rectangle(x=10, y=10, width=-10, height=-10)

    def test_different_fields_different_region_not_equal(self) -> None:
        """Sanity: genuinely different rectangles are not equal."""
        assert Rectangle(x=0, y=0, width=10, height=10) != Rectangle(x=0, y=0, width=-10, height=-10)
        assert Rectangle(x=0, y=0, width=10, height=10) != Rectangle(x=10, y=10, width=10, height=10)

    def test_hash_same_fields(self) -> None:
        assert hash(Rectangle(x=0, y=0, width=10, height=10)) == hash(Rectangle(x=0, y=0, width=10, height=10))

    def test_hash_different_fields(self) -> None:
        assert hash(Rectangle(x=0, y=0, width=10, height=10)) != hash(Rectangle(x=10, y=10, width=-10, height=-10))

    def test_usable_as_dict_key(self) -> None:
        r = Rectangle(x=0, y=0, width=10, height=10)
        d = {r: "value"}
        assert d[Rectangle(x=0, y=0, width=10, height=10)] == "value"


class TestBoundsProperties:
    @pytest.mark.parametrize(
        "test_case",
        NORMALIZED_BOUNDS_TEST_CASES,
        ids=lambda c: c.test_name,
    )
    def test_extents(self, test_case: NormalizedBoundsTestCase) -> None:
        r = Rectangle(x=test_case.x, y=test_case.y, width=test_case.width, height=test_case.height)
        assert r.extents == (test_case.x_min, test_case.y_min, test_case.x_max, test_case.y_max)

    def test_bounds_alias(self) -> None:
        r = Rectangle(x=0, y=0, width=10, height=10)
        assert r.bounds == r.extents


class TestArea:
    @pytest.mark.parametrize(
        "case",
        AREA_TEST_CASES,
        ids=lambda c: c.test_name,
    )
    def test_area(self, case: AreaTestCase) -> None:
        r = Rectangle(x=0, y=0, width=case.width, height=case.height)
        assert r.area == case.expected


class TestPerimeter:
    @pytest.mark.parametrize(
        "test_case",
        PERIMETER_TEST_CASES,
        ids=lambda c: c.test_name,
    )
    def test_perimeter(self, test_case: PerimeterTestCase) -> None:
        r = Rectangle(x=0, y=0, width=test_case.width, height=test_case.height)
        assert r.perimeter == test_case.expected


class TestCenter:
    @pytest.mark.parametrize(
        "test_case",
        CENTER_TEST_CASES,
        ids=lambda c: c.test_name,
    )
    def test_center(self, test_case: CenterTestCase) -> None:
        r = Rectangle(x=test_case.x, y=test_case.y, width=test_case.width, height=test_case.height)
        assert r.center == test_case.expected


class TestSize:
    @pytest.mark.parametrize(
        "test_case",
        SIZE_TEST_CASES,
        ids=lambda c: c.test_name,
    )
    def test_size_preserves_raw(self, test_case: SizeTestCase) -> None:
        r = Rectangle(x=0, y=0, width=test_case.width, height=test_case.height)
        assert r.size == (test_case.width, test_case.height)

    @pytest.mark.parametrize(
        "test_case",
        SIZE_TEST_CASES,
        ids=lambda c: c.test_name,
    )
    def test_normalized_size_always_non_negative(self, test_case: SizeTestCase) -> None:
        r = Rectangle(x=0, y=0, width=test_case.width, height=test_case.height)
        w, h = r.normalized_size
        assert w == abs(test_case.width)
        assert h == abs(test_case.height)


class TestAspectRatio:
    @pytest.mark.parametrize(
        "test_case",
        ASPECT_RATIO_TEST_CASES,
        ids=lambda c: c.test_name,
    )
    def test_aspect_ratio(self, test_case: AspectRatioTestCase) -> None:
        r = Rectangle(x=0, y=0, width=test_case.width, height=test_case.height)
        assert r.aspect_ratio == pytest.approx(test_case.expected)

    def test_zero_height_raises(self) -> None:
        r = Rectangle(x=0, y=0, width=10, height=0)
        with pytest.raises(ZeroDivisionError):
            _ = r.aspect_ratio

    def test_zero_width(self) -> None:
        r = Rectangle(x=0, y=0, width=0, height=10)
        assert r.aspect_ratio == 0.0


class TestDiagonal:
    @pytest.mark.parametrize(
        "test_case",
        DIAGONAL_TEST_CASES,
        ids=lambda c: c.test_name,
    )
    def test_diagonal(self, test_case: DiagonalTestCase) -> None:
        r = Rectangle(x=0, y=0, width=test_case.width, height=test_case.height)
        assert r.diagonal == pytest.approx(test_case.expected)


class TestCorners:
    @pytest.mark.parametrize(
        "test_case",
        CORNER_TEST_CASES,
        ids=lambda c: c.test_name,
    )
    def test_corners_order(self, test_case: CornersTestCase) -> None:
        r = Rectangle(x=test_case.x, y=test_case.y, width=test_case.width, height=test_case.height)
        tl, tr, br, bl = r.corners
        assert tl == test_case.expected_tl
        assert tr == test_case.expected_tr
        assert br == test_case.expected_br
        assert bl == test_case.expected_bl


class TestIsEmpty:
    @pytest.mark.parametrize(
        "test_case",
        IS_EMPTY_TEST_CASES,
        ids=lambda c: c.test_name,
    )
    def test_is_empty(self, test_case: IsEmptyTestCase) -> None:
        r = Rectangle(x=0, y=0, width=test_case.width, height=test_case.height)
        assert r.is_empty is test_case.expected


class TestIsNonNegative:
    @pytest.mark.parametrize(
        "test_case",
        IS_NON_NEGATIVE_TEST_CASES,
        ids=lambda c: c.test_name,
    )
    def test_is_non_negative(self, test_case: IsNonNegativeTestCase) -> None:
        r = Rectangle(x=test_case.x, y=test_case.y, width=test_case.width, height=test_case.height)
        assert r.is_non_negative is test_case.expected


class TestContainsPoint:
    @pytest.mark.parametrize(
        "test_case",
        CONTAINS_POINT_TEST_CASES,
        ids=lambda c: c.test_name,
    )
    def test_contains_point(self, test_case: ContainsPointTestCase) -> None:
        r = Rectangle(x=0, y=0, width=10, height=10)
        assert r.contains_point(test_case.px, test_case.py) is test_case.expected

    @pytest.mark.parametrize(
        "test_case",
        CONTAINS_POINT_TEST_CASES,
        ids=lambda c: c.test_name,
    )
    def test_negative_wh_same_result(self, test_case: ContainsPointTestCase) -> None:
        pos = Rectangle(x=0, y=0, width=10, height=10)
        neg = Rectangle(x=10, y=10, width=-10, height=-10)
        assert pos.contains_point(test_case.px, test_case.py) == neg.contains_point(test_case.px, test_case.py)


class TestContainsRect:
    @pytest.mark.parametrize(
        "test_case",
        CONTAINS_RECT_TEST_CASES,
        ids=lambda c: c.test_name,
    )
    def test_contains_rect(self, test_case: ContainsRectTestCase) -> None:
        outer = Rectangle(x=0, y=0, width=10, height=10)
        inner = Rectangle(x=test_case.ix, y=test_case.iy, width=test_case.iw, height=test_case.ih)
        assert outer.contains_rect(inner) is test_case.expected


class TestIntersects:
    @pytest.mark.parametrize(
        "test_case",
        TWO_RECT_TEST_CASES_INTERSECTS,
        ids=lambda c: c.test_name,
    )
    def test_intersects(self, test_case: TwoRectTestCase) -> None:
        a = Rectangle(x=test_case.ax, y=test_case.ay, width=test_case.aw, height=test_case.ah)
        b = Rectangle(x=test_case.bx, y=test_case.by, width=test_case.bw, height=test_case.bh)
        assert a.intersects(b) is test_case.expected


class TestTouches:
    @pytest.mark.parametrize(
        "test_case",
        TWO_RECT_TEST_CASES_TOUCHES,
        ids=lambda c: c.test_name,
    )
    def test_touches(self, test_case: TwoRectTestCase) -> None:
        a = Rectangle(x=test_case.ax, y=test_case.ay, width=test_case.aw, height=test_case.ah)
        b = Rectangle(x=test_case.bx, y=test_case.by, width=test_case.bw, height=test_case.bh)
        assert a.touches(b) is test_case.expected


class TestIntersection:
    @pytest.mark.parametrize(
        "test_case",
        INTERSECTION_TEST_CASES,
        ids=lambda c: c.test_name,
    )
    def test_intersection(self, test_case: IntersectionTestCase) -> None:
        a = Rectangle(x=test_case.ax, y=test_case.ay, width=test_case.aw, height=test_case.ah)
        b = Rectangle(x=test_case.bx, y=test_case.by, width=test_case.bw, height=test_case.bh)
        result = a.intersection(b)
        assert result == test_case.expected
        if result is not None:
            w, h = result.normalized_size
            assert w >= 0
            assert h >= 0


class TestUnion:
    @pytest.mark.parametrize(
        "test_case",
        UNION_TEST_CASES,
        ids=lambda c: c.test_name,
    )
    def test_union(self, test_case: UnionTestCase) -> None:
        a = Rectangle(x=test_case.ax, y=test_case.ay, width=test_case.aw, height=test_case.ah)
        b = Rectangle(x=test_case.bx, y=test_case.by, width=test_case.bw, height=test_case.bh)
        result = a.union(b)
        assert result == test_case.expected
        assert result.width >= 0
        assert result.height >= 0


class TestDistanceTo:
    @pytest.mark.parametrize(
        "test_case",
        DISTANCE_TEST_CASES,
        ids=lambda c: c.test_name,
    )
    def test_distance_to(self, test_case: DistanceTestCase) -> None:
        a = Rectangle(x=test_case.ax, y=test_case.ay, width=test_case.aw, height=test_case.ah)
        b = Rectangle(x=test_case.bx, y=test_case.by, width=test_case.bw, height=test_case.bh)
        assert a.distance_to(b) == pytest.approx(test_case.expected)
        assert a.distance_to(b) == pytest.approx(b.distance_to(a))  # symmetry on every case
        assert a.distance_to(b) >= 0.0  # always non-negative
