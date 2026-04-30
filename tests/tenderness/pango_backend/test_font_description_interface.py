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
from tenderness.pango_backend.font_description_interface import (
    FontDescriptionInterfaceParameters,
)

gi.require_version("Pango", "1.0")

from gi.repository import Pango  # noqa: E402


# --------------------------
# Tests for FontDescriptionInterfaceParameters
# --------------------------
class TestFontDescriptionInterfaceParametersUpdateParameters:
    def test_empty_construction(self) -> None:
        params = FontDescriptionInterfaceParameters()
        assert params._set_params == {}

    def test_string_coercion_at_construction(self) -> None:
        params = FontDescriptionInterfaceParameters(style="italic", weight="bold", stretch="condensed")
        assert params.style == Pango.Style.ITALIC
        assert params.weight == Pango.Weight.BOLD
        assert params.stretch == Pango.Stretch.CONDENSED

    def test_direct_enum_accepted(self) -> None:
        params = FontDescriptionInterfaceParameters(style=Pango.Style.ITALIC)
        assert params.style == Pango.Style.ITALIC

    def test_set_params_contains_only_set_fields(self) -> None:
        params = FontDescriptionInterfaceParameters(style="italic", family="Roboto")
        assert set(params._set_params.keys()) == {"style", "family"}

    def test_update_single_field(self) -> None:
        params = FontDescriptionInterfaceParameters(style="italic")
        params.update_parameters(style="normal")
        assert params.style == Pango.Style.NORMAL

    def test_update_multiple_fields(self) -> None:
        params = FontDescriptionInterfaceParameters(style="italic")
        params.update_parameters(style="normal", weight="light", family="Arial")
        assert params.style == Pango.Style.NORMAL
        assert params.weight == Pango.Weight.LIGHT
        assert params.family == "Arial"

    def test_update_set_params_stays_consistent(self) -> None:
        params = FontDescriptionInterfaceParameters(style="italic", weight="bold")
        params.update_parameters(style="normal")
        assert params._set_params["style"] == Pango.Style.NORMAL
        assert params._set_params["weight"] == Pango.Weight.BOLD

    def test_unset_field_via_update(self) -> None:
        params = FontDescriptionInterfaceParameters(style="italic", weight="bold")
        params.update_parameters(weight=_UNSET_PARAM)
        assert "weight" not in params._set_params
        assert params.weight is _UNSET_PARAM

    def test_direct_assignment_blocked(self) -> None:
        params = FontDescriptionInterfaceParameters(style="italic")
        with pytest.raises(AttributeError):
            params.style = "normal"  # type: ignore

    def test_unknown_field_raises(self) -> None:
        params = FontDescriptionInterfaceParameters()
        with pytest.raises(AttributeError):
            params.update_parameters(stylee="italic")

    def test_conflicting_size_fields_at_construction(self) -> None:
        with pytest.raises(match="Cannot set both"):
            FontDescriptionInterfaceParameters(size=12.0, size_device_units=12.0)

    def test_conflicting_size_fields_update_is_atomic(self) -> None:
        params = FontDescriptionInterfaceParameters(size=12.0)
        with pytest.raises(match="Cannot set both"):
            params.update_parameters(size_device_units=12.0)
        assert params.size == 12.0
        assert "size_device_units" not in params._set_params

    def test_loop_update_consistent(self) -> None:
        params = FontDescriptionInterfaceParameters(family="Roboto")
        for style in ["normal", "italic", "oblique"]:
            params.update_parameters(style=style)
            assert "family" in params._set_params
        assert params.style == Pango.Style.OBLIQUE
