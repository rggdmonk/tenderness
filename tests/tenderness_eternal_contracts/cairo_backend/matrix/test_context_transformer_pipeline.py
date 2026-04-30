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

from tenderness.cairo_backend.matrix.context_transformer_pipeline import CairoContextTransformPipeline
from tests._test_utils.class_test import ClassTestBase, ClassTestConfig

# --------------------------
# Tests for CairoContextTransformPipeline
# --------------------------
CAIRO_CONTEXT_TRANSFORM_PIPELINE_EXPECTED_METHODS = {
    "translate",
    "scale",
    "rotate",
    "skew_x",
    "skew_y",
    "rotate_around_point",
    "flip_horizontal",
    "flip_vertical",
    "reset",
    "_update_from_dataclass",
    "_update_from_dataclasses",
    "_update_from_dict",
    "_update_from_dicts",
    "update_with_parameter",
    "update_with_parameters",
    "apply_to_cairo_context",
}
CAIRO_CONTEXT_TRANSFORM_PIPELINE_EXPECTED_CLASS_METHODS = {
    "from_new",
    "from_cairo_context",
}
CAIRO_CONTEXT_TRANSFORM_PIPELINE_EXPECTED_PROPERTIES = {
    "matrix",
    "supported_transforms_types",
}
CAIRO_CONTEXT_TRANSFORM_PIPELINE_EXPECTED_CLASS_VARS = {
    "_SUPPORTED_TRANSFORMS",
    "_SUPPORTED_TRANSFORMS_PARAMETERS_TYPES",
    "_SUPPORTED_TRANSFORMS_TYPES",
}

CAIRO_CONTEXT_TRANSFORM_PIPELINE_CLASS_CONFIG = [
    ClassTestConfig(
        cls=CairoContextTransformPipeline,
        expected_class_vars=CAIRO_CONTEXT_TRANSFORM_PIPELINE_EXPECTED_CLASS_VARS,
        expected_methods=CAIRO_CONTEXT_TRANSFORM_PIPELINE_EXPECTED_METHODS,
        expected_class_methods=CAIRO_CONTEXT_TRANSFORM_PIPELINE_EXPECTED_CLASS_METHODS,
        expected_properties=CAIRO_CONTEXT_TRANSFORM_PIPELINE_EXPECTED_PROPERTIES,
    )
]


@pytest.mark.parametrize("config", CAIRO_CONTEXT_TRANSFORM_PIPELINE_CLASS_CONFIG, ids=lambda c: c.cls.__name__)
class TestCairoContextTransformPipelineContract(ClassTestBase):
    pass
