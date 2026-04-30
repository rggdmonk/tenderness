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

from tenderness.core.color_models import AlphaPosition, ColorModel


# --------------------------
# Testsfor ColorModel
# --------------------------
class TestColorModels:
    def test_property_return_types(self) -> None:
        for member in ColorModel:
            assert isinstance(member, ColorModel)
            assert isinstance(member.has_alpha, bool)
            assert isinstance(member.num_channels, int)
            assert isinstance(member.alpha_position, AlphaPosition)

    def test_properties_raise_error_for_invalid_values(self) -> None:
        invalid_value = "unsupported_model_value_for_testing"

        with pytest.raises(AssertionError, match="Expected code to be unreachable"):
            ColorModel.has_alpha.fget(invalid_value)  # type: ignore

        with pytest.raises(AssertionError, match="Expected code to be unreachable"):
            ColorModel.num_channels.fget(invalid_value)  # type: ignore

        with pytest.raises(AssertionError, match="Expected code to be unreachable"):
            ColorModel.alpha_position.fget(invalid_value)  # type: ignore

    def test_rgb_model_properties(self) -> None:
        rgb = ColorModel.RGB
        assert rgb.has_alpha is False
        assert rgb.num_channels == 3
        assert rgb.alpha_position is AlphaPosition.NONE

    def test_rgba_model_properties(self) -> None:
        rgba = ColorModel.RGBA
        assert rgba.has_alpha is True
        assert rgba.num_channels == 4
        assert rgba.alpha_position is AlphaPosition.LAST

    def test_alpha_model_properties(self) -> None:
        alpha = ColorModel.ALPHA
        assert alpha.has_alpha is True
        assert alpha.num_channels == 1
        assert alpha.alpha_position is AlphaPosition.ONLY
