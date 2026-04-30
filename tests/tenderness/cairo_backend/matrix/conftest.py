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
import pytest

from tenderness.cairo_backend.matrix.context_transformer_pipeline import CairoContextTransformPipeline
from tenderness.cairo_backend.matrix.matrix_transformer import CairoMatrixTransformer


# --------------------------
# Fixtures For CairoMatrixTransformer
# --------------------------
@pytest.fixture
def cairo_matrix_transformer() -> CairoMatrixTransformer:
    return CairoMatrixTransformer(matrix=cairo.Matrix())


# --------------------------
# Fixtures For CairoContextTransformPipeline
# --------------------------
@pytest.fixture
def surface() -> cairo.ImageSurface:
    return cairo.ImageSurface(cairo.FORMAT_ARGB32, 1024, 512)


@pytest.fixture
def ctx(surface: cairo.ImageSurface) -> cairo.Context[cairo.Surface]:
    return cairo.Context(surface)


@pytest.fixture
def pipeline() -> CairoContextTransformPipeline:
    return CairoContextTransformPipeline.from_new()
