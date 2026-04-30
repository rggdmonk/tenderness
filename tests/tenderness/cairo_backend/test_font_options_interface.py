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

import cairo
import pytest

from tenderness.cairo_backend.font_options_interface import FontOptionsInterfaceParameters
from tenderness.core.sentinel import _UNSET_PARAM


# --------------------------
# Tests for FontOptionsInterfaceParameters
# --------------------------
class TestFontOptionsInterfaceParametersUpdateParameters:
    def test_empty_construction(self) -> None:
        params = FontOptionsInterfaceParameters()
        assert params._set_params == {}

    def test_string_coercion_at_construction(self) -> None:
        params = FontOptionsInterfaceParameters(antialias="gray", hint_style="slight", hint_metrics="on")
        assert params.antialias == cairo.Antialias.GRAY
        assert params.hint_style == cairo.HintStyle.SLIGHT
        assert params.hint_metrics == cairo.HintMetrics.ON

    def test_direct_enum_accepted(self) -> None:
        params = FontOptionsInterfaceParameters(antialias=cairo.Antialias.GRAY)
        assert params.antialias == cairo.Antialias.GRAY

    def test_set_params_contains_only_set_fields(self) -> None:
        params = FontOptionsInterfaceParameters(antialias="gray", hint_metrics="on")
        assert set(params._set_params.keys()) == {"antialias", "hint_metrics"}

    def test_update_single_field(self) -> None:
        params = FontOptionsInterfaceParameters(antialias="gray")
        params.update_parameters(antialias="none")
        assert params.antialias == cairo.Antialias.NONE

    def test_update_multiple_fields(self) -> None:
        params = FontOptionsInterfaceParameters(antialias="gray")
        params.update_parameters(antialias="none", hint_style="full", hint_metrics="off")
        assert params.antialias == cairo.Antialias.NONE
        assert params.hint_style == cairo.HintStyle.FULL
        assert params.hint_metrics == cairo.HintMetrics.OFF

    def test_update_set_params_stays_consistent(self) -> None:
        params = FontOptionsInterfaceParameters(antialias="gray", hint_style="slight")
        params.update_parameters(antialias="none")
        assert params._set_params["antialias"] == cairo.Antialias.NONE
        assert params._set_params["hint_style"] == cairo.HintStyle.SLIGHT

    def test_unset_field_via_update(self) -> None:
        params = FontOptionsInterfaceParameters(antialias="gray", hint_style="slight")
        params.update_parameters(hint_style=_UNSET_PARAM)
        assert "hint_style" not in params._set_params
        assert params.hint_style is _UNSET_PARAM

    def test_direct_assignment_blocked(self) -> None:
        params = FontOptionsInterfaceParameters(antialias="gray")
        with pytest.raises(AttributeError):
            params.antialias = "none"  # type: ignore

    def test_unknown_field_raises(self) -> None:
        params = FontOptionsInterfaceParameters()
        with pytest.raises(AttributeError):
            params.update_parameters(antialiass="gray")

    def test_loop_update_consistent(self) -> None:
        params = FontOptionsInterfaceParameters(hint_style="slight")
        for mode in ["none", "gray", "subpixel", "fast"]:
            params.update_parameters(antialias=mode)
            assert "hint_style" in params._set_params
        assert params.antialias == cairo.Antialias.FAST
