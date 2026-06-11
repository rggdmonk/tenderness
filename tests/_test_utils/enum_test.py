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
from enum import Enum

import pytest

from tests._test_utils.eternal_contracts_helpers import _is_classmethod_defined_on, _is_method_defined_on


@dataclass(slots=True, frozen=True)
class EnumTestConfig:
    enum_class: type[Enum]
    expected_members: set[str] = field(default_factory=set)
    expected_properties: set[str] = field(default_factory=set)
    expected_methods: set[str] = field(default_factory=set)
    expected_class_methods: set[str] = field(default_factory=set)


class EnumTestBase:
    pytestmark = pytest.mark.eternal_contract

    # ------------------------------------------------------------------
    # Structural tests
    # ------------------------------------------------------------------
    def test_is_enum(self, config: EnumTestConfig) -> None:
        assert issubclass(config.enum_class, Enum), f"{config.enum_class.__name__} is not an Enum"

    def test_has_members(self, config: EnumTestConfig) -> None:
        members = list(config.enum_class)
        assert len(members) > 0, f"{config.enum_class.__name__} has no members"

    # ------------------------------------------------------------------
    # Contract tests (members)
    # ------------------------------------------------------------------
    def test_members_unchanged(self, config: EnumTestConfig) -> None:
        current_members = {member.name for member in config.enum_class}

        assert current_members == config.expected_members, (
            f"Enum members changed! Current: {current_members}, Expected: {config.expected_members}"
        )

    def test_all_members_same_type(self, config: EnumTestConfig) -> None:
        member_types = {type(member.value) for member in config.enum_class}

        assert len(member_types) == 1, f"Not all enum members have the same type! Found types: {member_types}"

    # ------------------------------------------------------------------
    # Contract tests (properties)
    # ------------------------------------------------------------------
    def test_properties_unchanged(self, config: EnumTestConfig) -> None:
        enum_cls = config.enum_class

        current_props = {name for name, value in vars(enum_cls).items() if isinstance(value, property)}

        assert current_props == config.expected_properties, (
            f"Properties changed! Current: {current_props}, Expected: {config.expected_properties}"
        )

    # ------------------------------------------------------------------
    # Contract tests (methods)
    # ------------------------------------------------------------------
    def test_methods_unchanged(self, config: EnumTestConfig) -> None:
        enum_cls = config.enum_class

        current_methods = {name for name, value in vars(enum_cls).items() if _is_method_defined_on(enum_cls, value)}

        assert current_methods == config.expected_methods, (
            f"Methods changed! Current: {current_methods}, Expected: {config.expected_methods}"
        )

    # ------------------------------------------------------------------
    # Contract tests (class methods)
    # ------------------------------------------------------------------
    def test_class_methods_unchanged(self, config: EnumTestConfig) -> None:
        enum_cls = config.enum_class

        current_class_methods = {
            name for name, value in vars(enum_cls).items() if _is_classmethod_defined_on(enum_cls, value)
        }

        assert current_class_methods == config.expected_class_methods, (
            f"Class methods changed! Current: {current_class_methods}, Expected: {config.expected_class_methods}"
        )
