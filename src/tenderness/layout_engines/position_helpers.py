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

"""Rectangle inset and position helpers."""

from __future__ import annotations

from tenderness.core.geometry import Margin, Rectangle


class PositionHelpers:
    """Static helpers for rectangle positioning."""

    @staticmethod
    def inset_rect(
        rect: Rectangle,
        top: float = 0,
        right: float = 0,
        bottom: float = 0,
        left: float = 0,
        *,
        margin: Margin | None = None,
    ) -> tuple[Rectangle, Margin]:
        """Return the content rectangle and margin after insetting rect.

        Parameters
        ----------
        rect
            Source rectangle to inset.
        top
            Top margin in device units; ignored when margin is provided.
        right
            Right margin in device units; ignored when margin is provided.
        bottom
            Bottom margin in device units; ignored when margin is provided.
        left
            Left margin in device units; ignored when margin is provided.
        margin
            Explicit margin to apply; constructed from the individual values when ``None``.
        """
        if margin is None:
            margin = Margin(top=top, right=right, bottom=bottom, left=left)
        content_rect = rect.inset(spacing_box=margin)
        return content_rect, margin
