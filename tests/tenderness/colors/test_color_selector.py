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

from tenderness.colors.color_selector import (
    Color,
    ColorGroup,
    ColorGroupName,
    ColorName,
    ColorRegistry,
    ColorSelector,
    HexColor,
)

# --------------------------
# Helpers
# --------------------------
TEST_GROUP_NAME: ColorGroupName = "TEST"
SAMPLE_COLORS: dict[ColorName, HexColor] = {
    "red": "#ff0000",
    "green": "#008000",
    "blue": "#0000ff",
    "yellow": "#ffff00",
    "purple": "#800080",
}


def make_group(source: dict[ColorName, HexColor] | None = None, name: ColorGroupName = TEST_GROUP_NAME) -> ColorGroup:
    return ColorGroup(color_group_name=name, source=source or SAMPLE_COLORS)


def make_registry(source: dict[ColorName, HexColor] | None = None) -> ColorRegistry:
    registry = ColorRegistry()
    registry._groups[TEST_GROUP_NAME] = ColorGroup(color_group_name=TEST_GROUP_NAME, source=source or SAMPLE_COLORS)
    return registry


# --------------------------
# Tests for Color
# --------------------------
class TestColor:
    def test_from_hex_sets_all_fields(self, red_color: Color) -> None:
        assert red_color.color_name == "red"
        assert red_color.color_group_name == "TEST"
        assert red_color.hex == "#ff0000"
        assert red_color.rgb == pytest.approx((1.0, 0.0, 0.0))
        assert red_color.rgba == pytest.approx((1.0, 0.0, 0.0, 1.0))

    def test_is_frozen(self, red_color: Color) -> None:
        with pytest.raises(AttributeError):
            red_color.color_name = "blue"  # type: ignore[misc]

    def test_equality_by_value(self, red_color: Color) -> None:
        other = Color.from_hex("red", "TEST", "#ff0000")
        assert red_color == other

    def test_inequality_on_different_name(self, red_color: Color) -> None:
        other = Color.from_hex("blue", "TEST", "#0000ff")
        assert red_color != other


# --------------------------
# Tests for ColorGroup
# --------------------------
class TestColorGroup:
    def test_len_matches_source(self, group: ColorGroup) -> None:
        assert len(group) == len(SAMPLE_COLORS)

    def test_contains_existing_name(self, group: ColorGroup) -> None:
        assert "red" in group

    def test_not_contains_missing_name(self, group: ColorGroup) -> None:
        assert "magenta" not in group

    def test_all_names_returns_all_keys(self, group: ColorGroup) -> None:
        assert set(group.all_names()) == set(SAMPLE_COLORS.keys())

    def test_get_color_by_name_returns_correct_color(self, group: ColorGroup) -> None:
        color = group.get_color_by_name("red")
        assert color.color_name == "red"
        assert color.hex == "#ff0000"

    def test_get_color_by_name_raises_for_unknown(self, group: ColorGroup) -> None:
        with pytest.raises(KeyError, match="color_name"):
            group.get_color_by_name("nonexistent")

    def test_colors_inherit_group_name(self) -> None:
        group = make_group(name="MYGROUP")
        color = group.get_color_by_name("red")
        assert color.color_group_name == "MYGROUP"


# --------------------------
# Tests for ColorRegistry
# --------------------------
class TestColorRegistry:
    def test_builtin_groups_present(self) -> None:
        registry = ColorRegistry()  # pristine — no TEST group injected
        assert set(registry.group_names()) == {"TABLEAU", "CSS4", "XKCD"}

    def test_get_group_returns_correct_group(self, registry: ColorRegistry) -> None:
        group = registry.get_group(TEST_GROUP_NAME)
        assert isinstance(group, ColorGroup)

    def test_get_group_raises_for_unknown(self, registry: ColorRegistry) -> None:
        with pytest.raises(KeyError, match="color_group_name"):
            registry.get_group("UNKNOWN")

    def test_get_color_delegates_correctly(self, registry: ColorRegistry) -> None:
        color = registry.get_color("red", TEST_GROUP_NAME)
        assert color.color_name == "red"
        assert color.color_group_name == TEST_GROUP_NAME

    def test_get_color_default_group_is_css4(self) -> None:
        registry = ColorRegistry()  # pristine — "red" lives in CSS4, not TEST
        color = registry.get_color("red")
        assert color.color_group_name == "CSS4"

    def test_total_colors_returns_counts_for_all_groups(self, registry: ColorRegistry) -> None:
        totals = registry.total_colors()
        assert set(totals.keys()) == set(registry.group_names())
        assert all(v > 0 for v in totals.values())


# --------------------------
# Tests for ColorSelector
# --------------------------
class TestColorSelectorInit:
    def test_default_registry_is_created(self) -> None:
        selector = ColorSelector()
        assert isinstance(selector.color_registry, ColorRegistry)

    def test_provided_registry_is_used(self, registry: ColorRegistry) -> None:
        selector = ColorSelector(color_registry=registry)
        assert selector.color_registry is registry


class TestColorSelectorByNames:
    def test_returns_colors_in_order(self, selector: ColorSelector) -> None:
        result = selector.by_names(["blue", "red", "green"], TEST_GROUP_NAME)
        assert [c.color_name for c in result] == ["blue", "red", "green"]

    def test_empty_input_returns_empty_list(self, selector: ColorSelector) -> None:
        assert selector.by_names([]) == []

    def test_default_group_is_css4(self) -> None:
        selector = ColorSelector()  # pristine
        result = selector.by_names(["red"])
        assert result[0].color_group_name == "CSS4"

    def test_custom_group_is_used(self, selector: ColorSelector) -> None:
        result = selector.by_names(["red"], color_group_name=TEST_GROUP_NAME)
        assert result[0].color_group_name == TEST_GROUP_NAME

    def test_duplicate_names_return_duplicate_colors(self, selector: ColorSelector) -> None:
        result = selector.by_names(["red", "red"], TEST_GROUP_NAME)
        assert len(result) == 2
        assert all(c.color_name == "red" for c in result)

    def test_unknown_name_raises(self, selector: ColorSelector) -> None:
        with pytest.raises(KeyError):
            selector.by_names(["nonexistent"], TEST_GROUP_NAME)


class TestColorSelectorRandomly:
    def test_returns_correct_count(self, selector: ColorSelector) -> None:
        assert len(selector.randomly(3, TEST_GROUP_NAME)) == 3

    def test_returns_color_objects(self, selector: ColorSelector) -> None:
        assert all(isinstance(c, Color) for c in selector.randomly(2, TEST_GROUP_NAME))

    def test_no_duplicates(self, selector: ColorSelector) -> None:
        names = [c.color_name for c in selector.randomly(5, TEST_GROUP_NAME)]
        assert len(names) == len(set(names))

    def test_zero_raises(self, selector: ColorSelector) -> None:
        with pytest.raises(ValueError, match="num_colors=0 must be > 0"):
            selector.randomly(0, TEST_GROUP_NAME)

    def test_negative_raises(self, selector: ColorSelector) -> None:
        with pytest.raises(ValueError, match="must be > 0"):
            selector.randomly(-1, TEST_GROUP_NAME)

    def test_exceeding_available_raises(self, selector: ColorSelector) -> None:
        with pytest.raises(ValueError, match=f"only {len(SAMPLE_COLORS)} available"):
            selector.randomly(len(SAMPLE_COLORS) + 1, TEST_GROUP_NAME)

    def test_exact_available_count_succeeds(self, selector: ColorSelector) -> None:
        assert len(selector.randomly(len(SAMPLE_COLORS), TEST_GROUP_NAME)) == len(SAMPLE_COLORS)

    def test_exclusion_removes_colors(self, selector: ColorSelector) -> None:
        names = {c.color_name for c in selector.randomly(3, TEST_GROUP_NAME, excluded=["red", "blue"])}
        assert "red" not in names
        assert "blue" not in names

    def test_exclusion_is_case_insensitive(self, selector: ColorSelector) -> None:
        names = {c.color_name for c in selector.randomly(3, TEST_GROUP_NAME, excluded=["RED", "BLUE"])}
        assert "red" not in names
        assert "blue" not in names

    def test_exclusion_reduces_pool_triggering_error(self, selector: ColorSelector) -> None:
        exclude_all_but_one = list(SAMPLE_COLORS.keys())[:-1]
        with pytest.raises(ValueError, match="only 1 available"):
            selector.randomly(2, TEST_GROUP_NAME, excluded=exclude_all_but_one)

    def test_none_excluded_uses_full_pool(self, selector: ColorSelector) -> None:
        assert len(selector.randomly(len(SAMPLE_COLORS), TEST_GROUP_NAME, excluded=None)) == len(SAMPLE_COLORS)

    def test_empty_excluded_uses_full_pool(self, selector: ColorSelector) -> None:
        assert len(selector.randomly(len(SAMPLE_COLORS), TEST_GROUP_NAME, excluded=[])) == len(SAMPLE_COLORS)

    def test_same_seed_is_deterministic(self, selector: ColorSelector) -> None:
        a = [c.color_name for c in selector.randomly(3, TEST_GROUP_NAME, seed=42)]
        b = [c.color_name for c in selector.randomly(3, TEST_GROUP_NAME, seed=42)]
        assert a == b

    def test_different_seeds_differ(self, selector: ColorSelector) -> None:
        a = [c.color_name for c in selector.randomly(3, TEST_GROUP_NAME, seed=1)]
        b = [c.color_name for c in selector.randomly(3, TEST_GROUP_NAME, seed=9999)]
        assert a != b

    def test_default_group_is_css4(self) -> None:
        selector = ColorSelector()  # pristine
        assert all(c.color_group_name == "CSS4" for c in selector.randomly(3))

    def test_custom_group_is_used(self, selector: ColorSelector) -> None:
        assert all(c.color_group_name == TEST_GROUP_NAME for c in selector.randomly(3, TEST_GROUP_NAME))

    def test_unknown_group_raises(self, selector: ColorSelector) -> None:
        with pytest.raises(KeyError, match="color_group_name"):
            selector.randomly(1, color_group_name="UNKNOWN")
