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

import cairo

from tenderness.cairo_backend.matrix.matrix_transformer import CairoMatrixTransformer


# --------------------------
# Tests for CairoMatrixTransformer
# --------------------------
class TestCairoMatrixTransformerInit:
    def test_none_matrix_defaults_to_identity(self) -> None:
        transformer = CairoMatrixTransformer(matrix=cairo.Matrix())
        assert transformer.get_components() == (1.0, 0.0, 0.0, 1.0, 0.0, 0.0)

    def test_explicit_matrix_is_used(self) -> None:
        m = cairo.Matrix(xx=2, yx=0, xy=0, yy=2, x0=10, y0=20)
        transformer = CairoMatrixTransformer(matrix=m)
        assert transformer.get_components() == (2.0, 0.0, 0.0, 2.0, 10.0, 20.0)

    def test_from_new_creates_identity_transformer(self) -> None:
        transformer = CairoMatrixTransformer.from_new()
        assert transformer.get_components() == (1.0, 0.0, 0.0, 1.0, 0.0, 0.0)


class TestCairoMatrixTransformerGetComponents:
    def test_returns_tuple(self, cairo_matrix_transformer: CairoMatrixTransformer) -> None:
        result = cairo_matrix_transformer.get_components()
        assert isinstance(result, tuple)
        assert len(result) == 6

    def test_identity_components(self, cairo_matrix_transformer: CairoMatrixTransformer) -> None:
        assert cairo_matrix_transformer.get_components() == (1.0, 0.0, 0.0, 1.0, 0.0, 0.0)


class TestCairoMatrixTransformerTranslate:
    def test_translate(self, cairo_matrix_transformer: CairoMatrixTransformer) -> None:
        cairo_matrix_transformer.translate(tx=10, ty=20)
        assert cairo_matrix_transformer.get_components() == (1.0, 0.0, 0.0, 1.0, 10.0, 20.0)

    def test_translate_returns_self(self, cairo_matrix_transformer: CairoMatrixTransformer) -> None:
        assert cairo_matrix_transformer.translate(tx=10, ty=20) is cairo_matrix_transformer

    def test_translate_chaining(self, cairo_matrix_transformer: CairoMatrixTransformer) -> None:
        cairo_matrix_transformer.translate(tx=10, ty=20).translate(tx=5, ty=5)
        assert cairo_matrix_transformer.get_components() == (1.0, 0.0, 0.0, 1.0, 15.0, 25.0)


class TestCairoMatrixTransformerScale:
    def test_scale(self, cairo_matrix_transformer: CairoMatrixTransformer) -> None:
        cairo_matrix_transformer.scale(sx=2, sy=3)
        assert cairo_matrix_transformer.get_components() == (2.0, 0.0, 0.0, 3.0, 0.0, 0.0)

    def test_scale_returns_self(self, cairo_matrix_transformer: CairoMatrixTransformer) -> None:
        assert cairo_matrix_transformer.scale(sx=2, sy=2) is cairo_matrix_transformer

    def test_scale_uniform(self, cairo_matrix_transformer: CairoMatrixTransformer) -> None:
        cairo_matrix_transformer.scale(sx=2, sy=2)
        xx, yx, xy, yy, x0, y0 = cairo_matrix_transformer.get_components()
        assert xx == yy == 2.0
        assert x0 == 0.0
        assert y0 == 0.0
        assert yx == 0.0
        assert xy == 0.0


class TestCairoMatrixTransformerRotate:
    def test_rotate_90_degrees(self, cairo_matrix_transformer: CairoMatrixTransformer) -> None:
        cairo_matrix_transformer.rotate(angle=90, degrees=True)
        xx, yx, xy, yy, x0, y0 = cairo_matrix_transformer.get_components()
        assert math.isclose(xx, 0.0, abs_tol=1e-9)
        assert math.isclose(yx, 1.0, abs_tol=1e-9)
        assert math.isclose(xy, -1.0, abs_tol=1e-9)
        assert math.isclose(yy, 0.0, abs_tol=1e-9)
        assert math.isclose(x0, 0.0, abs_tol=1e-9)
        assert math.isclose(y0, 0.0, abs_tol=1e-9)

    def test_rotate_radians(self, cairo_matrix_transformer: CairoMatrixTransformer) -> None:
        cairo_matrix_transformer.rotate(angle=math.pi / 2, degrees=False)
        xx, yx, _, _, _, _ = cairo_matrix_transformer.get_components()
        assert math.isclose(xx, 0.0, abs_tol=1e-9)
        assert math.isclose(yx, 1.0, abs_tol=1e-9)

    def test_rotate_returns_self(self, cairo_matrix_transformer: CairoMatrixTransformer) -> None:
        assert cairo_matrix_transformer.rotate(angle=45) is cairo_matrix_transformer

    def test_rotate_360_is_identity(self, cairo_matrix_transformer: CairoMatrixTransformer) -> None:
        cairo_matrix_transformer.rotate(angle=360)
        xx, yx, xy, yy, x0, y0 = cairo_matrix_transformer.get_components()
        assert math.isclose(xx, 1.0, abs_tol=1e-9)
        assert math.isclose(yy, 1.0, abs_tol=1e-9)
        assert math.isclose(yx, 0.0, abs_tol=1e-9)
        assert math.isclose(xy, 0.0, abs_tol=1e-9)
        assert math.isclose(x0, 0.0, abs_tol=1e-9)
        assert math.isclose(y0, 0.0, abs_tol=1e-9)


class TestCairoMatrixTransformerRotateAroundPoint:
    def test_rotate_around_point_returns_self(self, cairo_matrix_transformer: CairoMatrixTransformer) -> None:
        assert cairo_matrix_transformer.rotate_around_point(angle=45, cx=100, cy=100) is cairo_matrix_transformer

    def test_rotate_180_around_point(self, cairo_matrix_transformer: CairoMatrixTransformer) -> None:
        cairo_matrix_transformer.rotate_around_point(angle=180, cx=50, cy=50)
        xx, yx, xy, yy, x0, y0 = cairo_matrix_transformer.get_components()
        assert math.isclose(xx, -1.0, abs_tol=1e-9)
        assert math.isclose(yy, -1.0, abs_tol=1e-9)
        assert math.isclose(x0, 100.0, abs_tol=1e-9)
        assert math.isclose(y0, 100.0, abs_tol=1e-9)
        assert math.isclose(yx, 0.0, abs_tol=1e-9)
        assert math.isclose(xy, 0.0, abs_tol=1e-9)

    def test_rotate_0_around_point_is_identity(self, cairo_matrix_transformer: CairoMatrixTransformer) -> None:
        cairo_matrix_transformer.rotate_around_point(angle=0, cx=100, cy=200)
        xx, yx, xy, yy, x0, y0 = cairo_matrix_transformer.get_components()
        assert math.isclose(xx, 1.0, abs_tol=1e-9)
        assert math.isclose(yy, 1.0, abs_tol=1e-9)
        assert math.isclose(x0, 0.0, abs_tol=1e-9)
        assert math.isclose(y0, 0.0, abs_tol=1e-9)
        assert math.isclose(yx, 0.0, abs_tol=1e-9)
        assert math.isclose(xy, 0.0, abs_tol=1e-9)


class TestCairoMatrixTransformerSkew:
    def test_skew_x_returns_self(self, cairo_matrix_transformer: CairoMatrixTransformer) -> None:
        assert cairo_matrix_transformer.skew_x(angle=15) is cairo_matrix_transformer

    def test_skew_x_modifies_xy(self, cairo_matrix_transformer: CairoMatrixTransformer) -> None:
        cairo_matrix_transformer.skew_x(angle=45)
        _, _, xy, _, _, _ = cairo_matrix_transformer.get_components()
        assert math.isclose(xy, math.tan(math.radians(45)), abs_tol=1e-9)

    def test_skew_y_returns_self(self, cairo_matrix_transformer: CairoMatrixTransformer) -> None:
        assert cairo_matrix_transformer.skew_y(angle=15) is cairo_matrix_transformer

    def test_skew_y_modifies_yx(self, cairo_matrix_transformer: CairoMatrixTransformer) -> None:
        cairo_matrix_transformer.skew_y(angle=45)
        _, yx, _, _, _, _ = cairo_matrix_transformer.get_components()
        assert math.isclose(yx, math.tan(math.radians(45)), abs_tol=1e-9)


class TestCairoMatrixTransformerFlip:
    def test_flip_horizontal_returns_self(self, cairo_matrix_transformer: CairoMatrixTransformer) -> None:
        assert cairo_matrix_transformer.flip_horizontal() is cairo_matrix_transformer

    def test_flip_horizontal_negates_xx(self, cairo_matrix_transformer: CairoMatrixTransformer) -> None:
        cairo_matrix_transformer.flip_horizontal(cx=0)
        xx, _, _, _, _, _ = cairo_matrix_transformer.get_components()
        assert math.isclose(xx, -1.0, abs_tol=1e-9)

    def test_flip_horizontal_around_cx(self, cairo_matrix_transformer: CairoMatrixTransformer) -> None:
        cairo_matrix_transformer.flip_horizontal(cx=100)
        xx, _, _, _, x0, _ = cairo_matrix_transformer.get_components()
        assert math.isclose(xx, -1.0, abs_tol=1e-9)
        assert math.isclose(x0, 200.0, abs_tol=1e-9)

    def test_flip_vertical_returns_self(self, cairo_matrix_transformer: CairoMatrixTransformer) -> None:
        assert cairo_matrix_transformer.flip_vertical() is cairo_matrix_transformer

    def test_flip_vertical_negates_yy(self, cairo_matrix_transformer: CairoMatrixTransformer) -> None:
        cairo_matrix_transformer.flip_vertical(cy=0)
        _, _, _, yy, _, _ = cairo_matrix_transformer.get_components()
        assert math.isclose(yy, -1.0, abs_tol=1e-9)

    def test_flip_vertical_around_cy(self, cairo_matrix_transformer: CairoMatrixTransformer) -> None:
        cairo_matrix_transformer.flip_vertical(cy=100)
        _, _, _, yy, _, y0 = cairo_matrix_transformer.get_components()
        assert math.isclose(yy, -1.0, abs_tol=1e-9)
        assert math.isclose(y0, 200.0, abs_tol=1e-9)


class TestCairoMatrixTransformerApplyMatrixToCairoContext:
    def test_apply_matrix_to_cairo_context(self, cairo_matrix_transformer: CairoMatrixTransformer) -> None:
        cairo_matrix_transformer.translate(tx=10, ty=20)
        surface = cairo.ImageSurface(cairo.Format.RGB24, 100, 100)
        ctx = cairo.Context(surface)
        cairo_matrix_transformer.apply_matrix_to_cairo_context(cairo_context=ctx)  # type: ignore[arg-type]
        m = ctx.get_matrix()
        assert math.isclose(m.x0, 10.0, abs_tol=1e-9)
        assert math.isclose(m.y0, 20.0, abs_tol=1e-9)


class TestCairoMatrixTransformerAppend:
    def test_append_applies_matrix(self, cairo_matrix_transformer: CairoMatrixTransformer) -> None:
        other = cairo.Matrix(xx=2, yx=0, xy=0, yy=2, x0=5, y0=10)
        cairo_matrix_transformer._append(other=other)
        xx, yx, xy, yy, x0, y0 = cairo_matrix_transformer.get_components()
        assert math.isclose(xx, 2.0, abs_tol=1e-9)
        assert math.isclose(yx, 0.0, abs_tol=1e-9)
        assert math.isclose(xy, 0.0, abs_tol=1e-9)
        assert math.isclose(yy, 2.0, abs_tol=1e-9)
        assert math.isclose(x0, 5.0, abs_tol=1e-9)
        assert math.isclose(y0, 10.0, abs_tol=1e-9)

    def test_append_identity_is_noop(self, cairo_matrix_transformer: CairoMatrixTransformer) -> None:
        cairo_matrix_transformer.translate(tx=3, ty=7)
        cairo_matrix_transformer._append(other=cairo.Matrix())
        _, _, _, _, x0, y0 = cairo_matrix_transformer.get_components()
        assert math.isclose(x0, 3.0, abs_tol=1e-9)
        assert math.isclose(y0, 7.0, abs_tol=1e-9)


class TestCairoMatrixTransformerTransformPoint:
    def test_transform_point_identity(self, cairo_matrix_transformer: CairoMatrixTransformer) -> None:
        x, y = cairo_matrix_transformer.transform_point(3.0, 4.0)
        assert math.isclose(x, 3.0, abs_tol=1e-9)
        assert math.isclose(y, 4.0, abs_tol=1e-9)

    def test_transform_point_after_translate(self, cairo_matrix_transformer: CairoMatrixTransformer) -> None:
        cairo_matrix_transformer.translate(tx=10, ty=20)
        x, y = cairo_matrix_transformer.transform_point(0.0, 0.0)
        assert math.isclose(x, 10.0, abs_tol=1e-9)
        assert math.isclose(y, 20.0, abs_tol=1e-9)

    def test_transform_point_after_scale(self, cairo_matrix_transformer: CairoMatrixTransformer) -> None:
        cairo_matrix_transformer.scale(sx=2, sy=3)
        x, y = cairo_matrix_transformer.transform_point(5.0, 4.0)
        assert math.isclose(x, 10.0, abs_tol=1e-9)
        assert math.isclose(y, 12.0, abs_tol=1e-9)


class TestCairoMatrixTransformerTransformDistance:
    def test_transform_distance_identity(self, cairo_matrix_transformer: CairoMatrixTransformer) -> None:
        dx, dy = cairo_matrix_transformer.transform_distance(3.0, 4.0)
        assert math.isclose(dx, 3.0, abs_tol=1e-9)
        assert math.isclose(dy, 4.0, abs_tol=1e-9)

    def test_transform_distance_ignores_translation(self, cairo_matrix_transformer: CairoMatrixTransformer) -> None:
        cairo_matrix_transformer.translate(tx=100, ty=200)
        dx, dy = cairo_matrix_transformer.transform_distance(3.0, 4.0)
        assert math.isclose(dx, 3.0, abs_tol=1e-9)
        assert math.isclose(dy, 4.0, abs_tol=1e-9)

    def test_transform_distance_after_scale(self, cairo_matrix_transformer: CairoMatrixTransformer) -> None:
        cairo_matrix_transformer.scale(sx=2, sy=3)
        dx, dy = cairo_matrix_transformer.transform_distance(5.0, 4.0)
        assert math.isclose(dx, 10.0, abs_tol=1e-9)
        assert math.isclose(dy, 12.0, abs_tol=1e-9)


class TestCairoMatrixTransformerInvert:
    def test_invert_returns_self(self, cairo_matrix_transformer: CairoMatrixTransformer) -> None:
        cairo_matrix_transformer.translate(tx=10, ty=20)
        assert cairo_matrix_transformer.invert() is cairo_matrix_transformer

    def test_invert_of_translation(self, cairo_matrix_transformer: CairoMatrixTransformer) -> None:
        cairo_matrix_transformer.translate(tx=10, ty=20)
        cairo_matrix_transformer.invert()
        xx, yx, xy, yy, x0, y0 = cairo_matrix_transformer.get_components()
        assert math.isclose(xx, 1.0, abs_tol=1e-9)
        assert math.isclose(yx, 0.0, abs_tol=1e-9)
        assert math.isclose(xy, 0.0, abs_tol=1e-9)
        assert math.isclose(yy, 1.0, abs_tol=1e-9)
        assert math.isclose(x0, -10.0, abs_tol=1e-9)
        assert math.isclose(y0, -20.0, abs_tol=1e-9)

    def test_invert_identity_is_identity(self, cairo_matrix_transformer: CairoMatrixTransformer) -> None:
        cairo_matrix_transformer.invert()
        assert cairo_matrix_transformer.get_components() == (1.0, 0.0, 0.0, 1.0, 0.0, 0.0)


class TestCairoMatrixTransformerMultiply:
    def test_multiply_returns_self(self, cairo_matrix_transformer: CairoMatrixTransformer) -> None:
        assert cairo_matrix_transformer.multiply(cairo.Matrix()) is cairo_matrix_transformer

    def test_multiply_by_identity_is_noop(self, cairo_matrix_transformer: CairoMatrixTransformer) -> None:
        cairo_matrix_transformer.translate(tx=5, ty=10)
        cairo_matrix_transformer.multiply(cairo.Matrix())
        _, _, _, _, x0, y0 = cairo_matrix_transformer.get_components()
        assert math.isclose(x0, 5.0, abs_tol=1e-9)
        assert math.isclose(y0, 10.0, abs_tol=1e-9)

    def test_multiply_applies_matrix(self, cairo_matrix_transformer: CairoMatrixTransformer) -> None:
        scale = cairo.Matrix(xx=2, yx=0, xy=0, yy=2, x0=0, y0=0)
        cairo_matrix_transformer.multiply(scale)
        xx, _, _, yy, _, _ = cairo_matrix_transformer.get_components()
        assert math.isclose(xx, 2.0, abs_tol=1e-9)
        assert math.isclose(yy, 2.0, abs_tol=1e-9)
