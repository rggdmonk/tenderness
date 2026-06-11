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

"""Drawing operations entry point."""

from __future__ import annotations

from tenderness.draw.minimal_draw.draw_borders import DrawBorders
from tenderness.draw.minimal_draw.draw_shapes import DrawShapes


# ---------------------------------------------------------------------------
# MinimalDraw
# ---------------------------------------------------------------------------
class MinimalDraw:
    """Entry point for drawing operations.

    Attributes
    ----------
    shapes
        Shape fill drawing operations.
    borders
        Border drawing operations.
    """

    shapes = DrawShapes()
    borders = DrawBorders()
