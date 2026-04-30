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

from tenderness.cairo_backend.matrix.context_transformer_pipeline import CairoContextTransformPipeline
from tenderness.cairo_backend.matrix.matrix_transforms import (
    FlipHorizontalParameters,
    FlipVerticalParameters,
    MatrixTransformType,
    RotateAroundPointParameters,
    RotateParameters,
    ScaleParameters,
    SkewXParameters,
    SkewYParameters,
    TranslateParameters,
)


# --------------------------
# Tests for CairoContextTransformPipeline
# --------------------------
class TestCairoContextTransformPipelineInit:
    def test_requires_matrix_argument(self) -> None:
        m = cairo.Matrix()
        p = CairoContextTransformPipeline(matrix=m)
        assert (p.matrix.xx, p.matrix.yy) == (1.0, 1.0)

    def test_stores_name(self) -> None:
        p = CairoContextTransformPipeline(matrix=cairo.Matrix(), name="test")
        assert p.name == "test"

    def test_default_name_is_empty(self) -> None:
        p = CairoContextTransformPipeline(matrix=cairo.Matrix())
        assert p.name == ""

    def test_matrix_reflects_initial_value(self) -> None:
        m = cairo.Matrix(xx=2, yx=0, xy=0, yy=3, x0=10, y0=20)
        p = CairoContextTransformPipeline(matrix=m)
        assert math.isclose(p.matrix.x0, 10.0)
        assert math.isclose(p.matrix.y0, 20.0)
        assert math.isclose(p.matrix.xx, 2.0)
        assert math.isclose(p.matrix.yy, 3.0)

    def test_cairo_matrix_transformer_is_public(self) -> None:
        p = CairoContextTransformPipeline(matrix=cairo.Matrix())
        assert hasattr(p, "cairo_matrix_transformer")


class TestCairoContextTransformPipelineFromNew:
    def test_returns_pipeline_instance(self) -> None:
        assert isinstance(CairoContextTransformPipeline.from_new(), CairoContextTransformPipeline)

    def test_starts_with_identity_matrix(self) -> None:
        p = CairoContextTransformPipeline.from_new()
        m = p.matrix
        assert (m.xx, m.yx, m.xy, m.yy, m.x0, m.y0) == (1.0, 0.0, 0.0, 1.0, 0.0, 0.0)

    def test_stores_name(self) -> None:
        p = CairoContextTransformPipeline.from_new(name="my_pipeline")
        assert p.name == "my_pipeline"

    def test_default_name_is_empty(self) -> None:
        p = CairoContextTransformPipeline.from_new()
        assert p.name == ""


class TestCairoContextTransformPipelineFromCairoContext:
    def test_returns_pipeline_instance(self, ctx: cairo.Context[cairo.Surface]) -> None:
        assert isinstance(CairoContextTransformPipeline.from_cairo_context(ctx), CairoContextTransformPipeline)

    def test_captures_identity_matrix(self, ctx: cairo.Context[cairo.Surface]) -> None:
        p = CairoContextTransformPipeline.from_cairo_context(ctx)
        m = p.matrix
        assert (m.xx, m.yx, m.xy, m.yy, m.x0, m.y0) == (1.0, 0.0, 0.0, 1.0, 0.0, 0.0)

    def test_captures_existing_translation(self, ctx: cairo.Context[cairo.Surface]) -> None:
        ctx.translate(100, 200)
        p = CairoContextTransformPipeline.from_cairo_context(ctx)
        assert math.isclose(p.matrix.x0, 100.0)
        assert math.isclose(p.matrix.y0, 200.0)

    def test_stores_name(self, ctx: cairo.Context[cairo.Surface]) -> None:
        p = CairoContextTransformPipeline.from_cairo_context(ctx, name="ctx_pipeline")
        assert p.name == "ctx_pipeline"


class TestCairoContextTransformPipelineSupportedTransformsTypes:
    def test_returns_tuple_of_matrix_transform_types(self, pipeline: CairoContextTransformPipeline) -> None:
        result = pipeline.supported_transforms_types
        assert isinstance(result, tuple)
        assert all(isinstance(t, MatrixTransformType) for t in result)

    def test_contains_all_expected_types(self, pipeline: CairoContextTransformPipeline) -> None:
        expected = {
            MatrixTransformType.TRANSLATE,
            MatrixTransformType.SCALE,
            MatrixTransformType.ROTATE,
            MatrixTransformType.SKEW_X,
            MatrixTransformType.SKEW_Y,
            MatrixTransformType.ROTATE_AROUND_POINT,
            MatrixTransformType.FLIP_HORIZONTAL,
            MatrixTransformType.FLIP_VERTICAL,
        }
        assert set(pipeline.supported_transforms_types) == expected


class TestCairoContextTransformPipelineFluentAPI:
    def test_translate_returns_self(self, pipeline: CairoContextTransformPipeline) -> None:
        assert pipeline.translate(tx=10, ty=20) is pipeline

    def test_translate_modifies_matrix(self, pipeline: CairoContextTransformPipeline) -> None:
        pipeline.translate(tx=100, ty=50)
        assert math.isclose(pipeline.matrix.x0, 100.0)
        assert math.isclose(pipeline.matrix.y0, 50.0)

    def test_scale_returns_self(self, pipeline: CairoContextTransformPipeline) -> None:
        assert pipeline.scale(sx=2, sy=3) is pipeline

    def test_scale_modifies_matrix(self, pipeline: CairoContextTransformPipeline) -> None:
        pipeline.scale(sx=3, sy=2)
        assert math.isclose(pipeline.matrix.xx, 3.0)
        assert math.isclose(pipeline.matrix.yy, 2.0)

    def test_rotate_returns_self(self, pipeline: CairoContextTransformPipeline) -> None:
        assert pipeline.rotate(angle=45) is pipeline

    def test_rotate_90_modifies_matrix(self, pipeline: CairoContextTransformPipeline) -> None:
        pipeline.rotate(angle=90)
        assert math.isclose(pipeline.matrix.xx, 0.0, abs_tol=1e-9)
        assert math.isclose(pipeline.matrix.yx, 1.0, abs_tol=1e-9)

    def test_rotate_radians(self, pipeline: CairoContextTransformPipeline) -> None:
        pipeline.rotate(angle=math.pi / 2, degrees=False)
        assert math.isclose(pipeline.matrix.xx, 0.0, abs_tol=1e-9)

    def test_skew_x_returns_self(self, pipeline: CairoContextTransformPipeline) -> None:
        assert pipeline.skew_x(angle=15) is pipeline

    def test_skew_x_modifies_xy(self, pipeline: CairoContextTransformPipeline) -> None:
        pipeline.skew_x(angle=45)
        assert math.isclose(pipeline.matrix.xy, math.tan(math.radians(45)), abs_tol=1e-9)

    def test_skew_y_returns_self(self, pipeline: CairoContextTransformPipeline) -> None:
        assert pipeline.skew_y(angle=15) is pipeline

    def test_skew_y_modifies_yx(self, pipeline: CairoContextTransformPipeline) -> None:
        pipeline.skew_y(angle=45)
        assert math.isclose(pipeline.matrix.yx, math.tan(math.radians(45)), abs_tol=1e-9)

    def test_rotate_around_point_returns_self(self, pipeline: CairoContextTransformPipeline) -> None:
        assert pipeline.rotate_around_point(angle=45, cx=100, cy=100) is pipeline

    def test_rotate_around_point_modifies_matrix(self, pipeline: CairoContextTransformPipeline) -> None:
        pipeline.rotate_around_point(angle=180, cx=50, cy=0)
        # 180° around (50,0): x' = 2*50 - x => translation x0 should be 100
        assert math.isclose(pipeline.matrix.x0, 100.0, abs_tol=1e-9)

    def test_flip_horizontal_returns_self(self, pipeline: CairoContextTransformPipeline) -> None:
        assert pipeline.flip_horizontal() is pipeline

    def test_flip_horizontal_negates_xx(self, pipeline: CairoContextTransformPipeline) -> None:
        pipeline.flip_horizontal()
        assert math.isclose(pipeline.matrix.xx, -1.0, abs_tol=1e-9)

    def test_flip_vertical_returns_self(self, pipeline: CairoContextTransformPipeline) -> None:
        assert pipeline.flip_vertical() is pipeline

    def test_flip_vertical_negates_yy(self, pipeline: CairoContextTransformPipeline) -> None:
        pipeline.flip_vertical()
        assert math.isclose(pipeline.matrix.yy, -1.0, abs_tol=1e-9)

    def test_chaining(self, pipeline: CairoContextTransformPipeline) -> None:
        result = pipeline.translate(tx=10, ty=20).scale(sx=2, sy=2).rotate(angle=45)
        assert result is pipeline
        assert math.isclose(result.matrix.xx, math.cos(math.radians(45)) * 2, abs_tol=1e-9)


class TestCairoContextTransformPipelineReset:
    def test_reset_returns_self(self, pipeline: CairoContextTransformPipeline) -> None:
        assert pipeline.reset() is pipeline

    def test_reset_restores_identity_matrix(self, pipeline: CairoContextTransformPipeline) -> None:
        pipeline.translate(tx=100, ty=200).reset()
        m = pipeline.matrix
        assert (m.xx, m.yx, m.xy, m.yy, m.x0, m.y0) == (1.0, 0.0, 0.0, 1.0, 0.0, 0.0)

    def test_reset_after_scale(self, pipeline: CairoContextTransformPipeline) -> None:
        pipeline.scale(sx=5, sy=5).reset()
        assert math.isclose(pipeline.matrix.xx, 1.0)
        assert math.isclose(pipeline.matrix.yy, 1.0)


class TestCairoContextTransformPipelineDictAPI:
    def test_update_from_dict_translate(self, pipeline: CairoContextTransformPipeline) -> None:
        pipeline._update_from_dict({"type": "translate", "tx": 10.0, "ty": 20.0})
        assert math.isclose(pipeline.matrix.x0, 10.0)
        assert math.isclose(pipeline.matrix.y0, 20.0)

    def test_update_from_dict_scale(self, pipeline: CairoContextTransformPipeline) -> None:
        pipeline._update_from_dict({"type": "scale", "sx": 3.0, "sy": 2.0})
        assert math.isclose(pipeline.matrix.xx, 3.0)
        assert math.isclose(pipeline.matrix.yy, 2.0)

    def test_update_from_dict_rotate(self, pipeline: CairoContextTransformPipeline) -> None:
        pipeline._update_from_dict({"type": "rotate", "angle": 90.0})
        assert math.isclose(pipeline.matrix.xx, 0.0, abs_tol=1e-9)

    def test_update_from_dict_skew_x(self, pipeline: CairoContextTransformPipeline) -> None:
        pipeline._update_from_dict({"type": "skew_x", "angle": 45.0})
        assert math.isclose(pipeline.matrix.xy, math.tan(math.radians(45)), abs_tol=1e-9)

    def test_update_from_dict_skew_y(self, pipeline: CairoContextTransformPipeline) -> None:
        pipeline._update_from_dict({"type": "skew_y", "angle": 45.0})
        assert math.isclose(pipeline.matrix.yx, math.tan(math.radians(45)), abs_tol=1e-9)

    def test_update_from_dict_flip_horizontal(self, pipeline: CairoContextTransformPipeline) -> None:
        pipeline._update_from_dict({"type": "flip_horizontal"})
        assert math.isclose(pipeline.matrix.xx, -1.0, abs_tol=1e-9)

    def test_update_from_dict_flip_vertical(self, pipeline: CairoContextTransformPipeline) -> None:
        pipeline._update_from_dict({"type": "flip_vertical"})
        assert math.isclose(pipeline.matrix.yy, -1.0, abs_tol=1e-9)

    def test_update_from_dict_rotate_around_point(self, pipeline: CairoContextTransformPipeline) -> None:
        pipeline._update_from_dict({"type": "rotate_around_point", "angle": 180.0, "cx": 50.0, "cy": 0.0})
        assert math.isclose(pipeline.matrix.x0, 100.0, abs_tol=1e-9)

    def test_update_from_dict_with_matrix_transform_type_key(self, pipeline: CairoContextTransformPipeline) -> None:
        pipeline._update_from_dict({"type": MatrixTransformType.TRANSLATE, "tx": 7.0, "ty": 3.0})
        assert math.isclose(pipeline.matrix.x0, 7.0)

    def test_update_from_dicts_applies_all(self, pipeline: CairoContextTransformPipeline) -> None:
        pipeline._update_from_dicts(
            [
                {"type": "translate", "tx": 10.0, "ty": 0.0},
                {"type": "translate", "tx": 5.0, "ty": 0.0},
            ]
        )
        assert math.isclose(pipeline.matrix.x0, 15.0)

    def test_update_from_dicts_empty_list(self, pipeline: CairoContextTransformPipeline) -> None:
        pipeline._update_from_dicts([])
        m = pipeline.matrix
        assert (m.xx, m.yx, m.xy, m.yy, m.x0, m.y0) == (1.0, 0.0, 0.0, 1.0, 0.0, 0.0)


class TestCairoContextTransformPipelineDataclassAPI:
    def test_update_from_dataclass_translate(self, pipeline: CairoContextTransformPipeline) -> None:
        pipeline._update_from_dataclass(TranslateParameters(tx=10.0, ty=20.0))
        assert math.isclose(pipeline.matrix.x0, 10.0)
        assert math.isclose(pipeline.matrix.y0, 20.0)

    def test_update_from_dataclass_scale(self, pipeline: CairoContextTransformPipeline) -> None:
        pipeline._update_from_dataclass(ScaleParameters(sx=4.0, sy=2.0))
        assert math.isclose(pipeline.matrix.xx, 4.0)
        assert math.isclose(pipeline.matrix.yy, 2.0)

    def test_update_from_dataclass_rotate(self, pipeline: CairoContextTransformPipeline) -> None:
        pipeline._update_from_dataclass(RotateParameters(angle=90.0))
        assert math.isclose(pipeline.matrix.xx, 0.0, abs_tol=1e-9)

    def test_update_from_dataclass_skew_x(self, pipeline: CairoContextTransformPipeline) -> None:
        pipeline._update_from_dataclass(SkewXParameters(angle=45.0))
        assert math.isclose(pipeline.matrix.xy, math.tan(math.radians(45)), abs_tol=1e-9)

    def test_update_from_dataclass_skew_y(self, pipeline: CairoContextTransformPipeline) -> None:
        pipeline._update_from_dataclass(SkewYParameters(angle=45.0))
        assert math.isclose(pipeline.matrix.yx, math.tan(math.radians(45)), abs_tol=1e-9)

    def test_update_from_dataclass_flip_horizontal(self, pipeline: CairoContextTransformPipeline) -> None:
        pipeline._update_from_dataclass(FlipHorizontalParameters())
        assert math.isclose(pipeline.matrix.xx, -1.0, abs_tol=1e-9)

    def test_update_from_dataclass_flip_vertical(self, pipeline: CairoContextTransformPipeline) -> None:
        pipeline._update_from_dataclass(FlipVerticalParameters())
        assert math.isclose(pipeline.matrix.yy, -1.0, abs_tol=1e-9)

    def test_update_from_dataclass_rotate_around_point(self, pipeline: CairoContextTransformPipeline) -> None:
        pipeline._update_from_dataclass(RotateAroundPointParameters(angle=180.0, cx=50.0, cy=0.0))
        assert math.isclose(pipeline.matrix.x0, 100.0, abs_tol=1e-9)

    def test_update_from_dataclasses_applies_all(self, pipeline: CairoContextTransformPipeline) -> None:
        pipeline._update_from_dataclasses(
            [
                TranslateParameters(tx=10.0, ty=0.0),
                TranslateParameters(tx=5.0, ty=0.0),
            ]
        )
        assert math.isclose(pipeline.matrix.x0, 15.0)

    def test_update_from_dataclasses_empty_list(self, pipeline: CairoContextTransformPipeline) -> None:
        pipeline._update_from_dataclasses([])
        m = pipeline.matrix
        assert (m.xx, m.yx, m.xy, m.yy, m.x0, m.y0) == (1.0, 0.0, 0.0, 1.0, 0.0, 0.0)


class TestCairoContextTransformPipelineUnifiedAPI:
    def test_update_with_parameter_dispatches_dict(self, pipeline: CairoContextTransformPipeline) -> None:
        pipeline.update_with_parameter({"type": "translate", "tx": 50.0, "ty": 0.0})
        assert math.isclose(pipeline.matrix.x0, 50.0)

    def test_update_with_parameter_dispatches_dataclass(self, pipeline: CairoContextTransformPipeline) -> None:
        pipeline.update_with_parameter(TranslateParameters(tx=50.0, ty=0.0))
        assert math.isclose(pipeline.matrix.x0, 50.0)

    def test_update_with_parameter_dict_and_dataclass_equivalent(self, pipeline: CairoContextTransformPipeline) -> None:
        p2 = CairoContextTransformPipeline.from_new()
        pipeline.update_with_parameter({"type": "scale", "sx": 3.0, "sy": 2.0})
        p2.update_with_parameter(ScaleParameters(sx=3.0, sy=2.0))
        assert math.isclose(pipeline.matrix.xx, p2.matrix.xx)
        assert math.isclose(pipeline.matrix.yy, p2.matrix.yy)

    def test_update_with_parameters_mixed_list(self, pipeline: CairoContextTransformPipeline) -> None:
        pipeline.update_with_parameters(
            [
                {"type": "translate", "tx": 10.0, "ty": 0.0},
                ScaleParameters(sx=2.0, sy=2.0),
            ]
        )
        assert math.isclose(pipeline.matrix.xx, 2.0)
        assert math.isclose(pipeline.matrix.x0, 10.0)

    def test_update_with_parameters_empty_list(self, pipeline: CairoContextTransformPipeline) -> None:
        pipeline.update_with_parameters([])
        m = pipeline.matrix
        assert (m.xx, m.yx, m.xy, m.yy, m.x0, m.y0) == (1.0, 0.0, 0.0, 1.0, 0.0, 0.0)

    def test_update_with_parameters_dataclass_only(self, pipeline: CairoContextTransformPipeline) -> None:
        pipeline.update_with_parameters(
            [
                TranslateParameters(tx=5.0, ty=0.0),
                TranslateParameters(tx=5.0, ty=0.0),
            ]
        )
        assert math.isclose(pipeline.matrix.x0, 10.0)

    def test_update_with_parameters_dict_only(self, pipeline: CairoContextTransformPipeline) -> None:
        pipeline.update_with_parameters(
            [
                {"type": "translate", "tx": 5.0, "ty": 0.0},
                {"type": "translate", "tx": 5.0, "ty": 0.0},
            ]
        )
        assert math.isclose(pipeline.matrix.x0, 10.0)


class TestCairoContextTransformPipelineApplyToCairoContext:
    def test_sets_matrix_on_context(
        self, pipeline: CairoContextTransformPipeline, ctx: cairo.Context[cairo.Surface]
    ) -> None:
        pipeline.translate(tx=100, ty=50)
        pipeline.apply_to_cairo_context(ctx)
        m = ctx.get_matrix()
        assert math.isclose(m.x0, 100.0)
        assert math.isclose(m.y0, 50.0)

    def test_applies_identity_when_no_transforms(
        self, pipeline: CairoContextTransformPipeline, ctx: cairo.Context[cairo.Surface]
    ) -> None:
        ctx.translate(999, 999)
        pipeline.apply_to_cairo_context(ctx)
        m = ctx.get_matrix()
        assert (m.xx, m.yx, m.xy, m.yy, m.x0, m.y0) == (1.0, 0.0, 0.0, 1.0, 0.0, 0.0)

    def test_from_context_chain(self, ctx: cairo.Context[cairo.Surface]) -> None:
        ctx.translate(50, 50)
        CairoContextTransformPipeline.from_cairo_context(ctx).translate(tx=50, ty=50).apply_to_cairo_context(ctx)
        m = ctx.get_matrix()
        assert math.isclose(m.x0, 100.0)
        assert math.isclose(m.y0, 100.0)
