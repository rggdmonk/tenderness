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

"""Color selection utilities backed by matplotlib."""

from __future__ import annotations

import logging
import random
from dataclasses import dataclass
from typing import ClassVar, Self

import matplotlib.colors as mcolors

logger = logging.getLogger(__name__)

type ColorName = str
type ColorGroupName = str
type HexColor = str
type RGBColor = tuple[float, float, float]
type RGBAColor = tuple[float, float, float, float]


@dataclass(frozen=True, slots=True)
class Color:
    """Color value with hex, RGB, and RGBA representations."""

    color_name: ColorName
    color_group_name: ColorGroupName
    hex: HexColor
    rgb: RGBColor
    rgba: RGBAColor

    @classmethod
    def from_hex(cls, color_name: ColorName, color_group_name: ColorGroupName, hex_color: HexColor) -> Self:
        """Construct a Color from a hex string, deriving RGB and RGBA automatically.

        Parameters
        ----------
        color_name
            Name of the color.
        color_group_name
            Name of the palette group.
        hex_color
            Hex color string, e.g. ``"#1f77b4"``.

        Returns
        -------
        Color
            Fully populated Color instance.
        """
        return cls(
            color_name=color_name,
            color_group_name=color_group_name,
            hex=hex_color,
            rgb=mcolors.to_rgb(hex_color),
            rgba=mcolors.to_rgba(hex_color),
        )


class ColorGroup:
    """A named collection of colors loaded from a name-to-hex mapping."""

    def __init__(self, color_group_name: ColorGroupName, source: dict[ColorName, HexColor]) -> None:
        self.color_group_name = color_group_name
        self._colors: dict[ColorName, Color] = {
            color_name: Color.from_hex(
                color_name=color_name, color_group_name=self.color_group_name, hex_color=hex_color
            )
            for color_name, hex_color in source.items()
        }

    def __len__(self) -> int:
        """Return the number of colors in the group."""
        return len(self._colors)

    def __contains__(self, color_name: ColorName) -> bool:
        """Check whether a color name exists in the group."""
        return color_name in self._colors

    def get_color_by_name(self, color_name: ColorName) -> Color:
        """Retrieve a color by name.

        Parameters
        ----------
        color_name
            Name of the color to look up.

        Returns
        -------
        Color
            The matching Color.

        Raises
        ------
        KeyError
            If ``color_name`` is not present in this group.
        """
        if color_name not in self._colors:
            msg = f"'{color_name=}' not found in '{self.color_group_name=}'!"
            raise KeyError(msg)
        return self._colors[color_name]

    def all_names(self) -> list[ColorName]:
        """Return all color names in the group."""
        return list(self._colors.keys())


class ColorRegistry:
    """Registry of built-in color groups sourced from matplotlib palettes."""

    # ignore types because from matplotlib.typing import ColorType is wide type
    _BUILTIN_SOURCES: ClassVar[dict[ColorGroupName, dict[ColorName, HexColor]]] = {
        "TABLEAU": mcolors.TABLEAU_COLORS,  # type: ignore[dict-item]
        "CSS4": mcolors.CSS4_COLORS,  # type: ignore[dict-item]
        "XKCD": mcolors.XKCD_COLORS,  # type: ignore[dict-item]
    }

    def __init__(self) -> None:
        self._groups: dict[ColorGroupName, ColorGroup] = {
            name: ColorGroup(color_group_name=name, source=source) for name, source in self._BUILTIN_SOURCES.items()
        }

    def group_names(self) -> list[ColorGroupName]:
        """Return the names of all registered groups."""
        return list(self._groups.keys())

    def get_group(self, color_group_name: ColorGroupName) -> ColorGroup:
        """Retrieve a color group by name.

        Parameters
        ----------
        color_group_name
            Name of the group.

        Returns
        -------
        ColorGroup
            The requested group.

        Raises
        ------
        KeyError
            If ``color_group_name`` is not registered.
        """
        if color_group_name not in self._groups:
            msg = f"Unknown '{color_group_name=}'! Valid options: {self.group_names()}"
            raise KeyError(msg)
        return self._groups[color_group_name]

    def get_color(self, color_name: ColorName, color_group_name: ColorGroupName = "CSS4") -> Color:
        """Retrieve a color by name from the specified group.

        Parameters
        ----------
        color_name
            Name of the color.
        color_group_name
            Group to search; defaults to ``"CSS4"``.

        Returns
        -------
        Color
            The matching Color.
        """
        return self.get_group(color_group_name=color_group_name).get_color_by_name(color_name=color_name)

    def total_colors(self) -> dict[ColorGroupName, int]:
        """Return the color count per group."""
        return {name: len(group) for name, group in self._groups.items()}


class ColorSelector:
    """High-level interface for selecting colors from the registry."""

    def __init__(self, color_registry: ColorRegistry | None = None) -> None:
        self.color_registry = color_registry or ColorRegistry()

    def by_names(self, color_names: list[ColorName], color_group_name: ColorGroupName = "CSS4") -> list[Color]:
        """Select colors by name, preserving input order.

        Parameters
        ----------
        color_names
            Names of colors to retrieve.
        color_group_name
            Group to look up names in; defaults to ``"CSS4"``.

        Returns
        -------
        list
            Colors in the same order as ``color_names``.
        """
        logger.debug("Selecting colors %s from group '%s'", color_names, color_group_name)
        return [self.color_registry.get_color(name, color_group_name) for name in color_names]

    def randomly(
        self,
        num_colors: int,
        color_group_name: ColorGroupName = "CSS4",
        excluded: list[ColorName] | None = None,
        seed: int = 1234542,
    ) -> list[Color]:
        """Select a reproducible random sample of colors from a group.

        Parameters
        ----------
        num_colors
            Number of colors to sample; must be > 0.
        color_group_name
            Group to sample from; defaults to ``"CSS4"``.
        excluded
            Names to exclude from the pool.
        seed
            Random seed for reproducibility.

        Returns
        -------
        list
            Randomly sampled colors.

        Raises
        ------
        ValueError
            If ``num_colors`` is not positive or exceeds the available pool.
        """
        logger.debug("Selecting %d random colors from group '%s'", num_colors, color_group_name)

        if num_colors <= 0:
            msg = f"{num_colors=} must be > 0!"
            raise ValueError(msg)

        excluded_set = set(excluded or [])
        available = [n for n in self.color_registry.get_group(color_group_name).all_names() if n not in excluded_set]
        logger.debug("Available colors after exclusion: %d (excluded: %s)", len(available), excluded_set)

        if num_colors > len(available):
            msg = f"Requested {num_colors=} but only {len(available)} available!"
            raise ValueError(msg)

        random.seed(seed)
        return [self.color_registry.get_color(name, color_group_name) for name in random.sample(available, num_colors)]
