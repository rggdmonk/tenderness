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

"""Defines the ``RendererConfigurator`` class, which provides a high-level API for configuring and aggregating renderer functionality."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

import cairo
import gi

from tenderness.cairo_backend.background_selector import (
    BackgroundSelector,
)
from tenderness.cairo_backend.font_options_interface import FontOptionsInterface
from tenderness.cairo_backend.matrix.context_transformer_pipeline import CairoContextTransformPipeline
from tenderness.cairo_backend.surface_config_manager import SurfaceConfigManager
from tenderness.cairo_backend.surface_creator import SurfaceCreator
from tenderness.cairo_backend.text_color_selector import TextColorSelector
from tenderness.image_backend.surface_array_converter import (
    SurfaceArrayConverter,
)
from tenderness.image_backend.surface_writer import SurfaceWriter
from tenderness.pango_backend.font_description_interface import FontDescriptionInterface
from tenderness.pango_backend.layout_context_interface import LayoutContextInterface
from tenderness.pango_backend.layout_interface import LayoutInterface

gi.require_version("Pango", "1.0")


if TYPE_CHECKING:
    import io

    from gi.repository import Pango

    from tenderness.cairo_backend.surface_configuration import (
        SurfaceConfig,
    )


logger = logging.getLogger(__name__)


class RendererConfigurator:
    """High-level API for configuring and aggregating renderer functionality."""

    def __init__(self) -> None:
        self.surface_config_manager = SurfaceConfigManager()
        self.surface_creator = SurfaceCreator()

        self.surface_array_converter = SurfaceArrayConverter()
        self.surface_writer = SurfaceWriter()

        self.background_selector = BackgroundSelector()
        self.text_color_selector = TextColorSelector()

    # --------------------------
    # Surface create
    # --------------------------
    def create_surface(
        self,
        surface_config: SurfaceConfig,
    ) -> tuple[cairo.Surface, io.BytesIO | None]:
        """Create a ``cairo.Surface`` based on the provided configuration.

        Parameters
        ----------
        surface_config
            Configuration for the surface to create.

        Returns
        -------
            A tuple containing the created ``cairo.Surface`` and an optional ``io.BytesIO`` buffer.
        """
        return self.surface_creator.create_surface(surface_config=surface_config)

    # --------------------------
    # Cairo context create
    # --------------------------
    def create_cairo_context(self, surface: cairo.Surface) -> cairo.Context[cairo.Surface]:
        """Create a ``cairo.Context`` for the given ``cairo.Surface``.

        Parameters
        ----------
        surface
            The ``cairo.Surface`` for which to create the context.

        Returns
        -------
            A ``cairo.Context`` associated with the given surface.
        """
        context = cairo.Context(surface)
        logger.debug("Created Cairo Context: %s", context)
        return context

    # --------------------------
    # Layout interface create (update via .update_*())
    # --------------------------
    def create_layout_interface_from_cairo_context(
        self,
        cairo_context: cairo.Context[cairo.Surface],
        name: str = "",
    ) -> LayoutInterface:
        """Create a ``LayoutInterface`` from a given ``cairo.Context``.

        Parameters
        ----------
        cairo_context
            The ``cairo.Context`` from which to create the layout interface.
        name
            An optional name for the layout interface.

        Returns
        -------
            A ``LayoutInterface`` associated with the given ``cairo.Context``.
        """
        return LayoutInterface.from_cairo_context(cairo_context=cairo_context, name=name)

    def create_layout_interface_from_existing(
        self,
        layout: Pango.Layout,
        name: str = "",
    ) -> LayoutInterface:
        """Create a ``LayoutInterface`` from an existing ``Pango.Layout``.

        Parameters
        ----------
        layout
            The existing ``Pango.Layout`` from which to create the layout interface.
        name
            An optional name for the layout interface.

        Returns
        -------
            A ``LayoutInterface`` associated with the given ``Pango.Layout``.
        """
        return LayoutInterface(pango_layout=layout, name=name)

    # --------------------------
    # FontDescription interface create (update via .update_*() , apply via .apply_to_*())
    # --------------------------
    def create_font_description_interface(
        self,
        name: str = "",
    ) -> FontDescriptionInterface:
        """Create a ``FontDescriptionInterface`` from a new ``Pango.FontDescription``.

        Parameters
        ----------
        name
            An optional name for the font description interface.

        Returns
        -------
            A ``FontDescriptionInterface`` associated with the new ``Pango.FontDescription``.
        """
        return FontDescriptionInterface.from_new(name=name)

    def create_font_description_interface_from_string(
        self,
        font_desc_str: str,
        name: str = "",
    ) -> FontDescriptionInterface:
        """Create a ``FontDescriptionInterface`` from a string representation of a ``Pango.FontDescription``.

        Parameters
        ----------
        font_desc_str
            The string representation of the ``Pango.FontDescription``.
        name
            An optional name for the font description interface.

        Returns
        -------
            A ``FontDescriptionInterface`` associated with the given string representation of a ``Pango.FontDescription``.
        """
        return FontDescriptionInterface.from_string(font_desc_str=font_desc_str, name=name)

    def create_font_description_interface_from_existing(
        self,
        font_description: Pango.FontDescription,
        name: str = "",
    ) -> FontDescriptionInterface:
        """Create a ``FontDescriptionInterface`` from an existing ``Pango.FontDescription``.

        Parameters
        ----------
        font_description
            The existing ``Pango.FontDescription`` from which to create the font description interface.
        name
            An optional name for the font description interface.

        Returns
        -------
            A ``FontDescriptionInterface`` associated with the given ``Pango.FontDescription``.
        """
        return FontDescriptionInterface(font_description=font_description, name=name)

    # --------------------------
    # LayoutContext interface create (update via .update_*())
    # --------------------------
    def create_layout_context_interface_from_layout_interface(
        self,
        layout_interface: LayoutInterface,
        name: str = "",
    ) -> LayoutContextInterface:
        """Create a ``LayoutContextInterface`` from an existing ``LayoutInterface``.

        Parameters
        ----------
        layout_interface
            The existing ``LayoutInterface`` from which to create the layout context interface.
        name
            An optional name for the layout context interface.

        Returns
        -------
            A ``LayoutContextInterface`` associated with the given ``LayoutInterface``.
        """
        return LayoutContextInterface.from_layout_interface(layout_interface=layout_interface, name=name)

    def create_layout_context_interface_from_pango_layout(
        self,
        pango_layout: Pango.Layout,
        name: str = "",
    ) -> LayoutContextInterface:
        """Create a ``LayoutContextInterface`` from an existing ``Pango.Layout``.

        Parameters
        ----------
        pango_layout
            The existing ``Pango.Layout`` from which to create the layout context interface.
        name
            An optional name for the layout context interface.

        Returns
        -------
            A ``LayoutContextInterface`` associated with the given ``Pango.Layout``.
        """
        return LayoutContextInterface.from_pango_layout(pango_layout=pango_layout, name=name)

    def create_layout_context_interface_from_existing(
        self,
        pango_context: Pango.Context,
        name: str = "",
    ) -> LayoutContextInterface:
        """Create a ``LayoutContextInterface`` from an existing ``Pango.Context``.

        Parameters
        ----------
        pango_context
            The existing ``Pango.Context`` from which to create the layout context interface.
        name
            An optional name for the layout context interface.

        Returns
        -------
            A ``LayoutContextInterface`` associated with the given ``Pango.Context``.
        """
        return LayoutContextInterface(pango_context=pango_context, name=name)

    # --------------------------
    # FontOptions interface create and update
    # --------------------------
    def create_font_options_interface(self, name: str = "") -> FontOptionsInterface:
        """Create a ``FontOptionsInterface`` from a new ``Pango.FontOptions``.

        Parameters
        ----------
        name
            An optional name for the font options interface.

        Returns
        -------
            A ``FontOptionsInterface`` associated with a new ``Pango.FontOptions``.
        """
        return FontOptionsInterface.from_new(name=name)

    # --------------------------
    # TransformPipeline create and apply
    # --------------------------
    def create_transform_pipeline_from_cairo_context(
        self,
        cairo_context: cairo.Context[cairo.Surface],
        name: str = "",
    ) -> CairoContextTransformPipeline:
        """Create a ``CairoContextTransformPipeline`` from an existing ``cairo.Context``.

        Parameters
        ----------
        cairo_context
            The existing ``cairo.Context`` from which to create the transform pipeline.
        name
            An optional name for the transform pipeline.

        Returns
        -------
            A ``CairoContextTransformPipeline`` associated with the given ``cairo.Context``.
        """
        return CairoContextTransformPipeline.from_cairo_context(cairo_context=cairo_context, name=name)

    def create_transform_pipeline_from_existing(
        self,
        matrix: cairo.Matrix,
        name: str = "",
    ) -> CairoContextTransformPipeline:
        """Create a ``CairoContextTransformPipeline`` from an existing ``cairo.Matrix``.

        Parameters
        ----------
        matrix
            The existing ``cairo.Matrix`` from which to create the transform pipeline.
        name
            An optional name for the transform pipeline.

        Returns
        -------
            A ``CairoContextTransformPipeline`` associated with the given ``cairo.Matrix``.
        """
        return CairoContextTransformPipeline(matrix=matrix, name=name)
