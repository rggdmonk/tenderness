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

import gi
import pytest

from tenderness.core.sentinel import _UNSET_PARAM
from tenderness.pango_backend.layout_interface import (
    LayoutInterface,
    LayoutInterfaceParameters,
)

if TYPE_CHECKING:
    import cairo

gi.require_version("Pango", "1.0")
gi.require_version("PangoCairo", "1.0")


from gi.repository import Pango  # noqa: E402


# --------------------------
# Tests for LayoutInterfaceParameters
# --------------------------
class TestLayoutInterfaceParametersUpdateParameters:
    def test_empty_construction(self) -> None:
        params = LayoutInterfaceParameters()
        assert params._set_params == {}

    def test_string_coercion_at_construction(self) -> None:
        params = LayoutInterfaceParameters(ellipsize="end", alignment="center", wrap="word")
        assert params.ellipsize == Pango.EllipsizeMode.END
        assert params.alignment == Pango.Alignment.CENTER
        assert params.wrap == Pango.WrapMode.WORD

    def test_direct_enum_accepted(self) -> None:
        params = LayoutInterfaceParameters(ellipsize=Pango.EllipsizeMode.END)
        assert params.ellipsize == Pango.EllipsizeMode.END

    def test_set_params_contains_only_set_fields(self) -> None:
        params = LayoutInterfaceParameters(ellipsize="end", justify=True)
        assert set(params._set_params.keys()) == {"ellipsize", "justify"}

    def test_update_single_field(self) -> None:
        params = LayoutInterfaceParameters(ellipsize="end")
        params.update_parameters(ellipsize="start")
        assert params.ellipsize == Pango.EllipsizeMode.START

    def test_update_multiple_fields(self) -> None:
        params = LayoutInterfaceParameters(ellipsize="end", justify=True)
        params.update_parameters(ellipsize="start", justify=False, line_spacing=1.5)
        assert params.ellipsize == Pango.EllipsizeMode.START
        assert params.justify is False
        assert params.line_spacing == 1.5

    def test_update_set_params_stays_consistent(self) -> None:
        params = LayoutInterfaceParameters(ellipsize="end", justify=True)
        params.update_parameters(ellipsize="start")
        assert params._set_params["ellipsize"] == Pango.EllipsizeMode.START
        assert params._set_params["justify"] is True

    def test_unset_field_via_update(self) -> None:
        params = LayoutInterfaceParameters(ellipsize="end", justify=True)
        params.update_parameters(justify=_UNSET_PARAM)
        assert "justify" not in params._set_params
        assert params.justify is _UNSET_PARAM

    def test_direct_assignment_blocked(self) -> None:
        params = LayoutInterfaceParameters(ellipsize="end")
        with pytest.raises(AttributeError):
            params.ellipsize = "start"  # type: ignore

    def test_unknown_field_raises(self) -> None:
        params = LayoutInterfaceParameters()
        with pytest.raises(AttributeError):
            params.update_parameters(elipsize="end")

    def test_conflicting_units_at_construction(self) -> None:
        with pytest.raises(match="Cannot set both"):
            LayoutInterfaceParameters(width=1000, width_device_units=300.0)

    def test_conflicting_units_update_is_atomic(self) -> None:
        params = LayoutInterfaceParameters(width=1000)
        with pytest.raises(match="Cannot set both"):
            params.update_parameters(width_device_units=300.0)
        assert params.width == 1000
        assert "width_device_units" not in params._set_params

    def test_loop_update_consistent(self) -> None:
        params = LayoutInterfaceParameters(width_device_units=300.0, justify=True)
        for mode in ["none", "start", "middle", "end"]:
            params.update_parameters(ellipsize=mode)
            assert "width_device_units" in params._set_params
            assert "justify" in params._set_params
        assert params.ellipsize == Pango.EllipsizeMode.END


# --------------------------
# Tests for LayoutInterface
# --------------------------
class TestLayoutInterfaceConstruction:
    def test_via_init(self, pango_layout: Pango.Layout) -> None:
        layout_interface = LayoutInterface(pango_layout=pango_layout)
        assert layout_interface.pango_layout is pango_layout
        assert isinstance(layout_interface, LayoutInterface)
        assert isinstance(layout_interface.pango_layout, Pango.Layout)
        assert layout_interface.name == ""

    def test_via_from_cairo_context(self, cairo_context: cairo.Context[cairo.Surface]) -> None:
        layout_interface = LayoutInterface.from_cairo_context(cairo_context=cairo_context)
        assert isinstance(layout_interface, LayoutInterface)
        assert isinstance(layout_interface.pango_layout, Pango.Layout)
        assert layout_interface.name == ""

    def test_pango_scale_constant(self) -> None:
        assert LayoutInterface.PANGO_SCALE == Pango.SCALE
