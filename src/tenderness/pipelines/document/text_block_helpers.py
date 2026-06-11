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

"""Text block helpers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

import gi

from tenderness.core.sentinel import _UNSET_PARAM, Settable, UnsetParam
from tenderness.pango_backend.layout_interface import LayoutInterface, TextStrategy
from tenderness.pipelines.document.pipeline_schema import BaseBlock

gi.require_version("Pango", "1.0")
from gi.repository import Pango  # noqa: E402, TC002

if TYPE_CHECKING:
    import cairo

    from tenderness.cairo_backend.color_patterns import PatternColorSpec
    from tenderness.cairo_backend.font_options_interface import FontOptionsInterfaceParameters
    from tenderness.cairo_backend.matrix.context_transformer_pipeline import TransformParameter
    from tenderness.cairo_backend.surface_configuration import SurfaceConfig
    from tenderness.core.geometry import Rectangle
    from tenderness.pango_backend.font_description_interface import FontDescriptionInterfaceParameters
    from tenderness.pango_backend.layout_context_interface import LayoutContextInterfaceParameters
    from tenderness.pango_backend.layout_interface import LayoutInterfaceParameters
    from tenderness.pipelines.renderer_configurator import RendererConfigurator


@dataclass(slots=True)
class TextStyle:
    """Text rendering style for a block or cell.

    Attributes
    ----------
    font_options_params
        Font options parameters.
    font_description_params
        Font description parameters.
    text_color_spec
        Text fill color or pattern.
    layout_interface_params
        Layout interface parameters.
    layout_context_params
        Layout context parameters.
    context_transform_params
        Context transform parameters.
    """

    font_options_params: Settable[FontOptionsInterfaceParameters] = _UNSET_PARAM
    font_description_params: Settable[FontDescriptionInterfaceParameters] = _UNSET_PARAM
    text_color_spec: Settable[PatternColorSpec] = _UNSET_PARAM
    layout_interface_params: Settable[LayoutInterfaceParameters] = _UNSET_PARAM
    layout_context_params: Settable[LayoutContextInterfaceParameters] = _UNSET_PARAM
    context_transform_params: Settable[list[TransformParameter]] = _UNSET_PARAM


@dataclass(slots=True, kw_only=True)
class TextBlock(BaseBlock):
    """Text block configuration.

    Attributes
    ----------
    text
        Text to render; ``_UNSET_PARAM`` to consume overflow from the previous block.
    text_style
        Block-level text style; overrides the base style where set.
    text_strategy
        Text rendering strategy.
    """

    text: Settable[str] = _UNSET_PARAM  # _UNSET_PARAM = receive overflow from previous text block
    text_style: Settable[TextStyle] = _UNSET_PARAM
    text_strategy: TextStrategy | str = TextStrategy.TEXT


@dataclass(slots=True)
class TextBlockResult:
    """Rendered text block output.

    Attributes
    ----------
    block_name
        Block identifier.
    block_position_name
        Position label within the document.
    block_position_rect
        Block's bounding rectangle in document coordinates.
    layout_interface
        Layout interface after rendering.
    ctm_cairo_matrix
        Current transformation matrix at render time.
    """

    block_name: str | None
    block_position_name: str | None
    block_position_rect: Rectangle
    layout_interface: LayoutInterface
    ctm_cairo_matrix: cairo.Matrix


class TextBlockHelpers:
    """Static helpers for text block rendering."""

    @staticmethod
    def apply_pango_text_style(
        renderer_configurator: RendererConfigurator,
        layout_interface: LayoutInterface,
        text_style: TextStyle,
    ) -> None:
        """Apply Pango-level style parameters from ``text_style`` to ``layout_interface``.

        Parameters
        ----------
        renderer_configurator
            Renderer used to create sub-interfaces.
        layout_interface
            Target layout interface.
        text_style
            Style to apply.
        """
        # Don't apply text_color_spec /  context_transform_params here - they are meant to be applied at the cairo context level, not the Pango layout level. The rest of the style parameters are for the Pango layout.

        if text_style.font_options_params is not _UNSET_PARAM:
            font_options_interface = renderer_configurator.create_font_options_interface()
            font_options_interface.update_with_parameters(params=text_style.font_options_params)
            font_options_interface.apply_to_layout_interface(layout_interface=layout_interface)

        if text_style.font_description_params is not _UNSET_PARAM:
            font_description_interface = renderer_configurator.create_font_description_interface()
            font_description_interface.update_with_parameters(params=text_style.font_description_params)
            font_description_interface.apply_to_layout_interface(layout_interface=layout_interface)

        if text_style.layout_context_params is not _UNSET_PARAM:
            layout_context_interface = renderer_configurator.create_layout_context_interface_from_layout_interface(
                layout_interface=layout_interface,
            )
            layout_context_interface.update_with_parameters(
                params=text_style.layout_context_params,
            )

        if text_style.layout_interface_params is not _UNSET_PARAM:
            layout_interface.update_with_parameters(
                params=text_style.layout_interface_params,
            )

    @staticmethod
    def apply_cairo_text_style(
        surface_config: SurfaceConfig,
        renderer_configurator: RendererConfigurator,
        cairo_context: cairo.Context[cairo.Surface],
        text_style: TextStyle,
    ) -> None:
        """Apply Cairo-level style parameters from ``text_style`` to ``cairo_context``.

        Parameters
        ----------
        surface_config
            Surface configuration.
        renderer_configurator
            Renderer used to apply color and transforms.
        cairo_context
            Target Cairo context.
        text_style
            Style to apply.
        """
        if text_style.text_color_spec is not _UNSET_PARAM:
            renderer_configurator.text_color_selector.add_text_color(
                cairo_context=cairo_context,
                surface_config=surface_config,
                text_color_spec=text_style.text_color_spec,
            )

        if text_style.context_transform_params is not _UNSET_PARAM:
            pipeline = renderer_configurator.create_transform_pipeline_from_cairo_context(
                cairo_context=cairo_context,
            )
            pipeline.update_with_parameters(transforms=text_style.context_transform_params)
            pipeline.apply_to_cairo_context(cairo_context=cairo_context)

    @staticmethod
    def create_base_text_layout_template(
        renderer_configurator: RendererConfigurator,
        cairo_context: cairo.Context[cairo.Surface],
        text_style: Settable[TextStyle],
    ) -> Pango.Layout | UnsetParam:
        """Build a shared layout template from ``text_style``, or return ``_UNSET_PARAM`` if unset.

        Parameters
        ----------
        renderer_configurator
            Renderer used to create the layout interface.
        cairo_context
            Cairo context for the layout.
        text_style
            Style to bake into the template.

        Returns
        -------
        Pango.Layout | UnsetParam
            Configured layout copy, or ``_UNSET_PARAM`` if ``text_style`` is unset.
        """
        if text_style is _UNSET_PARAM:
            return _UNSET_PARAM

        layout_interface = renderer_configurator.create_layout_interface_from_cairo_context(
            cairo_context=cairo_context,
        )

        TextBlockHelpers.apply_pango_text_style(
            renderer_configurator=renderer_configurator,
            layout_interface=layout_interface,
            text_style=text_style,
        )

        return layout_interface.pango_layout.copy()

    @staticmethod
    def resolve_text_for_block(
        text_block: TextBlock,
        pending_overflow_text: str | None,
    ) -> str:
        """Return the text for a block, consuming ``pending_overflow_text`` if ``text_block.text`` is unset.

        Parameters
        ----------
        text_block
            Text block to resolve text for.
        pending_overflow_text
            Overflow text from the previous block, or ``None``.

        Returns
        -------
        str
            Resolved text string.
        """
        if text_block.text is _UNSET_PARAM:
            return pending_overflow_text or ""
        return text_block.text

    @staticmethod
    def text_style_has_explicit_width(text_style: Settable[TextStyle]) -> bool:
        """Return ``True`` if ``text_style`` sets an explicit layout width.

        Parameters
        ----------
        text_style
            Style to inspect.

        Returns
        -------
        bool
            ``True`` if ``width`` or ``width_device_units`` is set in the layout interface parameters.
        """
        if text_style is _UNSET_PARAM or text_style.layout_interface_params is _UNSET_PARAM:
            return False

        p = text_style.layout_interface_params
        return p.width is not _UNSET_PARAM or p.width_device_units is not _UNSET_PARAM

    @staticmethod
    def text_style_has_explicit_height(text_style: Settable[TextStyle]) -> bool:
        """Return ``True`` if ``text_style`` sets an explicit layout height.

        Parameters
        ----------
        text_style
            Style to inspect.

        Returns
        -------
        bool
            ``True`` if ``height`` or ``height_device_units`` is set in the layout interface parameters.
        """
        if text_style is _UNSET_PARAM or text_style.layout_interface_params is _UNSET_PARAM:
            return False

        p = text_style.layout_interface_params
        return p.height is not _UNSET_PARAM or p.height_device_units is not _UNSET_PARAM
