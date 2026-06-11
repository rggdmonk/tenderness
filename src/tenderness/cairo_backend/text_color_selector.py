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

"""Text color source utilities."""

from __future__ import annotations

from typing import TYPE_CHECKING

from tenderness.cairo_backend.color_patterns import ColorPattern, PatternColorSpec

if TYPE_CHECKING:
    import cairo

    from tenderness.cairo_backend.surface_configuration import SurfaceConfig


class TextColorSelector:
    """Sets a color pattern as the text source on a cairo context."""

    def add_text_color(
        self,
        cairo_context: cairo.Context[cairo.Surface],
        surface_config: SurfaceConfig,
        text_color_spec: PatternColorSpec,
    ) -> None:
        """Set a color pattern as the text source on a cairo context.

        Parameters
        ----------
        cairo_context
            Context to configure.
        surface_config
            Provides the color model used to resolve the color spec.
        text_color_spec
            Color specification for the text.
        """
        pattern = ColorPattern.create_color_pattern(text_color_spec, surface_config.color_model)
        cairo_context.set_source(pattern)
