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

import gi
import pytest

from tenderness.core.sentinel import _UNSET_PARAM
from tenderness.pango_backend.layout_context_interface import (
    LayoutContextInterfaceParameters,
)

gi.require_version("Pango", "1.0")

from gi.repository import Pango  # noqa: E402


# --------------------------
# Tests for LayoutContextInterfaceParameters
# --------------------------
class TestLayoutContextInterfaceParametersUpdateParameters:
    def test_empty_construction(self) -> None:
        params = LayoutContextInterfaceParameters()
        assert params._set_params == {}

    def test_string_coercion_at_construction(self) -> None:
        params = LayoutContextInterfaceParameters(base_dir="ltr", base_gravity="south", gravity_hint="natural")
        assert params.base_dir == Pango.Direction.LTR
        assert params.base_gravity == Pango.Gravity.SOUTH
        assert params.gravity_hint == Pango.GravityHint.NATURAL

    def test_direct_enum_accepted(self) -> None:
        params = LayoutContextInterfaceParameters(base_dir=Pango.Direction.RTL)
        assert params.base_dir == Pango.Direction.RTL

    def test_set_params_contains_only_set_fields(self) -> None:
        params = LayoutContextInterfaceParameters(base_dir="ltr", round_glyph_positions=True)
        assert set(params._set_params.keys()) == {"base_dir", "round_glyph_positions"}

    def test_update_single_field(self) -> None:
        params = LayoutContextInterfaceParameters(base_dir="ltr")
        params.update_parameters(base_dir="rtl")
        assert params.base_dir == Pango.Direction.RTL

    def test_update_multiple_fields(self) -> None:
        params = LayoutContextInterfaceParameters(base_dir="ltr")
        params.update_parameters(base_dir="rtl", base_gravity="north", round_glyph_positions=False)
        assert params.base_dir == Pango.Direction.RTL
        assert params.base_gravity == Pango.Gravity.NORTH
        assert params.round_glyph_positions is False

    def test_update_set_params_stays_consistent(self) -> None:
        params = LayoutContextInterfaceParameters(base_dir="ltr", gravity_hint="strong")
        params.update_parameters(base_dir="rtl")
        assert params._set_params["base_dir"] == Pango.Direction.RTL
        assert params._set_params["gravity_hint"] == Pango.GravityHint.STRONG

    def test_unset_field_via_update(self) -> None:
        params = LayoutContextInterfaceParameters(base_dir="ltr", gravity_hint="strong")
        params.update_parameters(gravity_hint=_UNSET_PARAM)
        assert "gravity_hint" not in params._set_params
        assert params.gravity_hint is _UNSET_PARAM

    def test_direct_assignment_blocked(self) -> None:
        params = LayoutContextInterfaceParameters(base_dir="ltr")
        with pytest.raises(AttributeError):
            params.base_dir = Pango.Direction.RTL  # type: ignore

    def test_unknown_field_raises(self) -> None:
        params = LayoutContextInterfaceParameters()
        with pytest.raises(AttributeError):
            params.update_parameters(base_diir="ltr")

    def test_loop_update_consistent(self) -> None:
        params = LayoutContextInterfaceParameters(base_gravity="south", round_glyph_positions=True)
        for hint in ["natural", "strong", "line", "natural"]:
            params.update_parameters(gravity_hint=hint)
            assert "base_gravity" in params._set_params
            assert "round_glyph_positions" in params._set_params
        assert params.gravity_hint == Pango.GravityHint.NATURAL
