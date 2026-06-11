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

from typing import TYPE_CHECKING

import pytest

from tests.e2e._constants import (
    _DEFAULT_IMG_SURFACE_CONFIG,
    _DEFAULT_PDF_SURFACE_CONFIG,
    _DEFAULT_SVG_SURFACE_CONFIG,
)

if TYPE_CHECKING:
    from tenderness.cairo_backend.surface_configuration import SurfaceConfig


@pytest.fixture(
    params=[
        pytest.param(_DEFAULT_IMG_SURFACE_CONFIG, id="image"),
        pytest.param(_DEFAULT_SVG_SURFACE_CONFIG, id="svg"),
        pytest.param(_DEFAULT_PDF_SURFACE_CONFIG, id="pdf"),
    ],
)
def surface_config(request: pytest.FixtureRequest) -> SurfaceConfig:
    return request.param  # type: ignore[no-any-return]
