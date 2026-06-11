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

from tenderness.bounding_boxes.bounding_boxes_schema import Quadrilateral


def _make_quadrilateral(
    *,
    x_offset: float = 0.0,
    y_offset: float = 0.0,
    width: float = 10.0,
    height: float = 4.0,
) -> Quadrilateral:
    return Quadrilateral(
        top_left=(x_offset + 0.0, y_offset + 0.0),
        top_right=(x_offset + width, y_offset + 0.0),
        bottom_right=(x_offset + width, y_offset + height),
        bottom_left=(x_offset + 0.0, y_offset + height),
    )


@pytest.fixture
def logical_bbox() -> Quadrilateral:
    """Dummy logical bounding box for testing purposes."""
    return _make_quadrilateral(x_offset=1.0, y_offset=2.0)


@pytest.fixture
def ink_bbox() -> Quadrilateral:
    """Dummy ink bounding box for testing purposes."""
    return _make_quadrilateral(x_offset=2.0, y_offset=2.5, width=8.0, height=3.0)
