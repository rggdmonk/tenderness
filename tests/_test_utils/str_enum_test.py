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

from dataclasses import dataclass, field
from enum import StrEnum

import pytest

from tests._test_utils.helpers import _is_property_defined_on


@dataclass(slots=True, frozen=True)
class StrEnumTestConfig:
    enum_class: type[StrEnum]
    expected_members: set[str] = field(default_factory=set)
    expected_properties: set[str] = field(default_factory=set)


class StrEnumTestBase:
    pytestmark = pytest.mark.eternal_contract

    # ------------------------------------------------------------------
    # Structural tests
    # ------------------------------------------------------------------
    def test_is_str_enum(self, config: StrEnumTestConfig) -> None:
        assert issubclass(config.enum_class, StrEnum), f"{config.enum_class.__name__} is not a {StrEnum.__name__}"

    def test_has_members(self, config: StrEnumTestConfig) -> None:
        members = list(config.enum_class)
        assert len(members) > 0, f"{config.enum_class.__name__} has no members"

    # ------------------------------------------------------------------
    # Contract tests (members)
    # ------------------------------------------------------------------
    def test_members_unchanged(self, config: StrEnumTestConfig) -> None:
        enum_cls = config.enum_class

        current_members = {member.name for member in enum_cls}

        assert current_members == config.expected_members, (
            f"Enum members changed! Current: {current_members}, Expected: {config.expected_members}"
        )

        for member in enum_cls:
            assert isinstance(member.value, str), f"{member} value is not a string"

    def test_member_values_unique(self, config: StrEnumTestConfig) -> None:
        enum_cls = config.enum_class

        # StrEnum allows aliases — we forbid them
        member_values = [member.value for member in enum_cls]
        duplicates = {value for value in member_values if member_values.count(value) > 1}

        assert len(member_values) == len(set(member_values)), (
            f"Duplicate member values found in {enum_cls.__name__}: {duplicates}"
        )

    # ------------------------------------------------------------------
    # Contract tests (properties)
    # ------------------------------------------------------------------
    def test_properties_unchanged(self, config: StrEnumTestConfig) -> None:
        enum_cls = config.enum_class

        current_props = {name for name, value in vars(enum_cls).items() if _is_property_defined_on(enum_cls, value)}

        assert current_props == config.expected_properties, (
            f"Properties changed! Current: {current_props}, Expected: {config.expected_properties}"
        )
