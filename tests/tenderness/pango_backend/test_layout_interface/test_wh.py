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

from tenderness.pango_backend.layout_interface_geometry import (
    HeightDeviceUnits,
    HeightLineLimit,
    HeightSingleLine,
    WidthDeviceUnits,
    WidthUnconstrained,
)

if TYPE_CHECKING:
    from tenderness.pango_backend.layout_interface import (
        LayoutInterface,
    )

gi.require_version("Pango", "1.0")
gi.require_version("PangoCairo", "1.0")


from gi.repository import Pango  # noqa: E402


class TestLayoutInterfaceWidthProperty:
    # --- getter ---
    def test_getter_default_value(self, layout_interface: LayoutInterface) -> None:
        assert layout_interface.width == -1

    # --- setter ---
    def test_setter_zero(self, layout_interface: LayoutInterface) -> None:
        layout_interface.width = 0
        assert layout_interface.width == 0

    @pytest.mark.parametrize("positive_value", [1, 20.5, 42.1, 100])
    def test_setter_positive(self, layout_interface: LayoutInterface, positive_value: float) -> None:
        assert isinstance(positive_value, (int, float))
        assert positive_value > 0

        if isinstance(positive_value, float):
            layout_interface.width = positive_value  # type: ignore[assignment]
            assert layout_interface.width == int(positive_value)
        else:
            layout_interface.width = positive_value
            assert layout_interface.width == positive_value

    @pytest.mark.parametrize("negative_value", [-1, -12.5, -40])
    def test_setter_negative_normalises_to_minus_one(
        self, layout_interface: LayoutInterface, negative_value: float
    ) -> None:
        """Pango normalises any negative value to -1."""
        assert isinstance(negative_value, (int, float))
        assert negative_value < 0

        layout_interface.width = negative_value  # type: ignore[assignment]
        print(layout_interface.width)
        assert layout_interface.width == -1

    def test_setter_invalid_type_raise(self, layout_interface: LayoutInterface) -> None:
        with pytest.raises(TypeError):
            layout_interface.width = "100"  # type: ignore[assignment]

    @pytest.mark.parametrize("value", [100, 101.0, 150, 200.5])
    def test_setter_overwrites_previous_value(self, layout_interface: LayoutInterface, value: float) -> None:
        layout_interface.width = value  # type: ignore[assignment]
        assert layout_interface.width == int(value)
        layout_interface.width = value + 50  # type: ignore[assignment]
        assert layout_interface.width == int(value + 50)


class TestLayoutInterfaceWidthDeviceUnitsProperty:
    # --- getter ---
    def test_getter_default_returns_unconstrained(self, layout_interface: LayoutInterface) -> None:
        default_value = layout_interface.width_device_units
        assert isinstance(default_value, WidthUnconstrained)

    @pytest.mark.parametrize("negative_value", [-1, -2, -16.0, -300])
    def test_getter_negative_returns_width_unconstrained(
        self, layout_interface: LayoutInterface, negative_value: float
    ) -> None:
        assert isinstance(negative_value, (int, float))
        assert negative_value < 0

        layout_interface.width = negative_value  # type: ignore[assignment]
        result = layout_interface.width_device_units
        assert isinstance(result, WidthUnconstrained)

    def test_getter_zero_raise_error(self, layout_interface: LayoutInterface) -> None:
        layout_interface.width = 0
        with pytest.raises(ValueError, match="special mode"):
            _ = layout_interface.width_device_units

    @pytest.mark.parametrize("positive_value", [1, 20.5, 42.1, 100])
    def test_getter_positive_returns_width_device_units(
        self, layout_interface: LayoutInterface, positive_value: float
    ) -> None:
        assert isinstance(positive_value, (int, float))
        assert positive_value > 0

        layout_interface.width = Pango.units_from_double(positive_value)
        result = layout_interface.width_device_units
        assert isinstance(result, WidthDeviceUnits)
        assert result.width == pytest.approx(positive_value, abs=1 / Pango.SCALE)

    # --- setter ---
    def test_setter_unconstrained_instance(self, layout_interface: LayoutInterface) -> None:
        layout_interface.width_device_units = WidthUnconstrained()
        assert layout_interface.width == -1

    def test_setter_minus_one(self, layout_interface: LayoutInterface) -> None:
        layout_interface.width_device_units = -1
        assert layout_interface.width == -1

    def test_setter_zero_raise_error(self, layout_interface: LayoutInterface) -> None:
        with pytest.raises(ValueError, match="positive"):
            layout_interface.width_device_units = 0

    @pytest.mark.parametrize("negative_value", [-2, -20.5, -42.1, -100])
    def test_setter_negative_raise_error(self, layout_interface: LayoutInterface, negative_value: float) -> None:
        assert isinstance(negative_value, (int, float))
        assert negative_value < 0

        with pytest.raises(ValueError, match="positive"):
            layout_interface.width_device_units = negative_value

    @pytest.mark.parametrize("negative_value_du", [-1.5, -10.0, -100.0])
    def test_setter_negative_width_device_units_raise_error(
        self, layout_interface: LayoutInterface, negative_value_du: float
    ) -> None:
        assert isinstance(negative_value_du, (int, float))
        assert negative_value_du < 0

        with pytest.raises(ValueError, match="positive"):
            layout_interface.width_device_units = WidthDeviceUnits(width=negative_value_du)

    @pytest.mark.parametrize("positive_value", [1, 20.5, 42.1, 100])
    def test_setter_positive(self, layout_interface: LayoutInterface, positive_value: float) -> None:
        assert isinstance(positive_value, (int, float))
        assert positive_value > 0

        layout_interface.width_device_units = positive_value
        result = layout_interface.width_device_units
        assert isinstance(result, WidthDeviceUnits)
        assert result.width == pytest.approx(positive_value, abs=1 / Pango.SCALE)
        assert layout_interface.width == Pango.units_from_double(positive_value)

    @pytest.mark.parametrize("positive_value_du", [1, 18.3, 72.8, 100])
    def test_setter_positive_du(self, layout_interface: LayoutInterface, positive_value_du: float) -> None:
        assert isinstance(positive_value_du, (int, float))
        assert positive_value_du > 0

        width_device_units_instance = WidthDeviceUnits(width=positive_value_du)
        layout_interface.width_device_units = width_device_units_instance
        result = layout_interface.width_device_units
        assert isinstance(result, WidthDeviceUnits)
        assert result.width == pytest.approx(positive_value_du, abs=1 / Pango.SCALE)
        assert layout_interface.width == Pango.units_from_double(positive_value_du)

    def test_setter_invalid_type_raise(self, layout_interface: LayoutInterface) -> None:
        with pytest.raises(TypeError):
            layout_interface.width_device_units = "100"  # type: ignore[assignment]


class TestLayoutInterfaceHeightProperty:
    # --- getter ---
    def test_getter_default_value(self, layout_interface: LayoutInterface) -> None:
        assert layout_interface.height == -1

    # --- setter ---
    def test_setter_zero(self, layout_interface: LayoutInterface) -> None:
        layout_interface.height = 0
        assert layout_interface.height == 0

    @pytest.mark.parametrize("positive_value", [1, 20.5, 42.1, 100])
    def test_setter_positive(self, layout_interface: LayoutInterface, positive_value: float) -> None:
        assert isinstance(positive_value, (int, float))
        assert positive_value > 0

        if isinstance(positive_value, float):
            layout_interface.height = positive_value  # type: ignore[assignment]
            assert layout_interface.height == int(positive_value)
        else:
            layout_interface.height = positive_value
            assert layout_interface.height == positive_value

    @pytest.mark.parametrize("negative_value", [-1, -13.5, -40])
    def test_setter_negative(self, layout_interface: LayoutInterface, negative_value: float) -> None:
        assert isinstance(negative_value, (int, float))
        assert negative_value < 0

        if isinstance(negative_value, float):
            layout_interface.height = negative_value  # type: ignore[assignment]
            assert layout_interface.height == int(negative_value)
        else:
            layout_interface.height = negative_value
            assert layout_interface.height == negative_value

    @pytest.mark.parametrize("value", [100, 101.0, 150, 200.5])
    def test_setter_overwrites_previous_value(self, layout_interface: LayoutInterface, value: float) -> None:
        layout_interface.height = value  # type: ignore[assignment]
        assert layout_interface.height == int(value)
        layout_interface.height = value + 50  # type: ignore[assignment]
        assert layout_interface.height == int(value + 50)


class TestLayoutInterfaceHeightDeviceUnitsProperty:
    # --- getter: HeightDeviceUnits (height > 0) ---

    @pytest.mark.parametrize("positive_value", [1, 20.5, 47.3, 100])
    def test_getter_positive_returns_height_device_units(
        self, layout_interface: LayoutInterface, positive_value: float
    ) -> None:
        assert isinstance(positive_value, (int, float))
        assert positive_value > 0

        layout_interface.height = Pango.units_from_double(positive_value)
        result = layout_interface.height_device_units
        assert isinstance(result, HeightDeviceUnits)
        assert result.height == pytest.approx(positive_value, abs=1 / Pango.SCALE)

    # --- getter: HeightSingleLine (height == 0) ---

    def test_getter_zero_returns_height_single_line(self, layout_interface: LayoutInterface) -> None:
        layout_interface.height = 0
        result = layout_interface.height_device_units
        assert isinstance(result, HeightSingleLine)

    # --- getter: HeightLineLimit (height < 0) ---

    def test_getter_default_returns_height_line_limit(self, layout_interface: LayoutInterface) -> None:
        """Default height is -1 → HeightLineLimit(lines=1)."""
        result = layout_interface.height_device_units
        assert isinstance(result, HeightLineLimit)
        assert result.lines == 1

    @pytest.mark.parametrize(
        ("pango_height", "expected_lines"),
        [
            (-1, 1),
            (-2, 2),
            (-5, 5),
            (-10, 10),
        ],
    )
    def test_getter_negative_returns_height_line_limit(
        self,
        layout_interface: LayoutInterface,
        pango_height: int,
        expected_lines: int,
    ) -> None:
        assert pango_height < 0
        layout_interface.height = pango_height
        result = layout_interface.height_device_units
        assert isinstance(result, HeightLineLimit)
        assert result.lines == expected_lines

    # --- setter: HeightDeviceUnits ---

    @pytest.mark.parametrize("positive_value", [1, 20.5, 47.3, 100])
    def test_setter_positive_float_sets_device_units(
        self, layout_interface: LayoutInterface, positive_value: float
    ) -> None:
        assert positive_value > 0

        layout_interface.height_device_units = positive_value
        result = layout_interface.height_device_units
        assert isinstance(result, HeightDeviceUnits)
        assert result.height == pytest.approx(positive_value, abs=1 / Pango.SCALE)
        assert layout_interface.height == Pango.units_from_double(positive_value)

    @pytest.mark.parametrize("positive_value_du", [1, 18.3, 72.8, 100])
    def test_setter_height_device_units_instance(
        self, layout_interface: LayoutInterface, positive_value_du: float
    ) -> None:
        assert positive_value_du > 0

        layout_interface.height_device_units = HeightDeviceUnits(height=positive_value_du)
        result = layout_interface.height_device_units
        assert isinstance(result, HeightDeviceUnits)
        assert result.height == pytest.approx(positive_value_du, abs=1 / Pango.SCALE)
        assert layout_interface.height == Pango.units_from_double(positive_value_du)

    @pytest.mark.parametrize("negative_value_du", [-1.5, -10.0, -100.0])
    def test_setter_height_device_units_negative_raises(
        self, layout_interface: LayoutInterface, negative_value_du: float
    ) -> None:
        assert negative_value_du < 0
        with pytest.raises(ValueError, match="positive"):
            layout_interface.height_device_units = HeightDeviceUnits(height=negative_value_du)

    # --- setter: HeightSingleLine ---

    def test_setter_height_single_line_instance(self, layout_interface: LayoutInterface) -> None:
        layout_interface.height_device_units = HeightSingleLine()
        assert layout_interface.height == 0
        assert isinstance(layout_interface.height_device_units, HeightSingleLine)

    def test_setter_zero_sets_single_line(self, layout_interface: LayoutInterface) -> None:
        layout_interface.height_device_units = 0
        assert layout_interface.height == 0
        assert isinstance(layout_interface.height_device_units, HeightSingleLine)

    # --- setter: HeightLineLimit ---

    @pytest.mark.parametrize("lines", [1, 2, 5, 10])
    def test_setter_height_line_limit_instance(self, layout_interface: LayoutInterface, lines: int) -> None:
        assert lines > 0
        layout_interface.height_device_units = HeightLineLimit(lines=lines)
        assert layout_interface.height == -lines
        result = layout_interface.height_device_units
        assert isinstance(result, HeightLineLimit)
        assert result.lines == lines

    @pytest.mark.parametrize("negative_value", [-1, -2, -5, -10])
    def test_setter_negative_int_sets_line_limit(self, layout_interface: LayoutInterface, negative_value: int) -> None:
        assert negative_value < 0
        layout_interface.height_device_units = negative_value
        assert layout_interface.height == negative_value
        result = layout_interface.height_device_units
        assert isinstance(result, HeightLineLimit)
        assert result.lines == abs(negative_value)

    @pytest.mark.parametrize("invalid_lines", [0, -1, -5])
    def test_setter_height_line_limit_non_positive_raises(
        self, layout_interface: LayoutInterface, invalid_lines: int
    ) -> None:
        with pytest.raises(ValueError, match="positive"):
            layout_interface.height_device_units = HeightLineLimit(lines=invalid_lines)

    # --- setter: invalid type ---

    def test_setter_invalid_type_raises(self, layout_interface: LayoutInterface) -> None:
        with pytest.raises(TypeError):
            layout_interface.height_device_units = "1010"  # type: ignore[assignment]
