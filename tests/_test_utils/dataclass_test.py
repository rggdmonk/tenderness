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

import inspect
from abc import ABC
from dataclasses import dataclass, field, is_dataclass

import pytest

from tests._test_utils.helpers import (
    _dataclass_generated_methods,
    _is_classmethod_defined_on,
    _is_method_defined_on,
    _is_property_defined_on,
)


@dataclass(slots=True, frozen=True)
class DataclassTestConfig:
    dataclass_class: type
    is_abstract: bool = field(default=False)
    has_slots: bool = field(default=False)
    is_frozen: bool = field(default=False)

    expected_fields: set[str] = field(default_factory=set)

    expected_properties: set[str] = field(default_factory=set)
    expected_abstract_properties: set[str] = field(default_factory=set)

    expected_methods: set[str] = field(default_factory=set)
    expected_abstract_methods: set[str] = field(default_factory=set)

    expected_class_methods: set[str] = field(default_factory=set)


class DataclassTestBase:
    pytestmark = pytest.mark.eternal_contract

    # ----------------------------------------------------------------------
    # Structural tests
    # ----------------------------------------------------------------------
    def test_is_dataclass(self, config: DataclassTestConfig) -> None:
        assert is_dataclass(config.dataclass_class), f"{config.dataclass_class.__name__} is not a dataclass"

    def test_is_abstract(self, config: DataclassTestConfig) -> None:
        is_actually_abstract = inspect.isabstract(config.dataclass_class) or bool(
            getattr(config.dataclass_class, "__abstractmethods__", False)
        )

        if config.is_abstract:
            assert is_actually_abstract, f"{config.dataclass_class.__name__} should be abstract but is concrete."
            assert issubclass(config.dataclass_class, ABC), (
                f"{config.dataclass_class.__name__} is abstract so it should inherit from ABC."
            )
        else:
            assert not is_actually_abstract, f"{config.dataclass_class.__name__} should be concrete but is abstract."

    def test_has_slots(self, config: DataclassTestConfig) -> None:
        has_slots = "__slots__" in vars(config.dataclass_class)
        if config.has_slots:
            assert has_slots, f"{config.dataclass_class.__name__} is expected to have __slots__"
        else:
            assert not has_slots, f"{config.dataclass_class.__name__} is NOT expected to have __slots__"

    def test_is_frozen(self, config: DataclassTestConfig) -> None:
        is_frozen = config.dataclass_class.__dataclass_params__.frozen  # type: ignore
        if config.is_frozen:
            assert is_frozen, f"{config.dataclass_class.__name__} should be frozen."
        else:
            assert not is_frozen, f"{config.dataclass_class.__name__} should NOT be frozen."

    # ----------------------------------------------------------------------
    # Contract tests (fields)
    # ----------------------------------------------------------------------
    def test_fields_unchanged(self, config: DataclassTestConfig) -> None:
        current_fields = set(config.dataclass_class.__annotations__)

        assert current_fields == config.expected_fields, (
            f"Fields changed! Current: {current_fields}, Expected: {config.expected_fields}"
        )

    # ----------------------------------------------------------------------
    # Contract tests (properties)
    # ----------------------------------------------------------------------
    def test_properties_unchanged(self, config: DataclassTestConfig) -> None:
        cls = config.dataclass_class

        current_props = {
            name
            for name, value in vars(cls).items()
            if _is_property_defined_on(cls, value)
            and not getattr(getattr(value, "fget", None), "__isabstractmethod__", False)
        }

        assert current_props == config.expected_properties, (
            f"Properties changed! Current: {current_props}, Expected: {config.expected_properties}"
        )

    def test_abstract_properties_unchanged(self, config: DataclassTestConfig) -> None:
        cls = config.dataclass_class

        current_abstract_props = {
            name
            for name, value in vars(cls).items()
            if _is_property_defined_on(cls, value)
            and getattr(getattr(value, "fget", None), "__isabstractmethod__", False)
        }

        assert current_abstract_props == config.expected_abstract_properties, (
            f"Abstract properties changed! Current: {current_abstract_props}, Expected: {config.expected_abstract_properties}"
        )

    # ----------------------------------------------------------------------
    # Contract tests (methods)
    # ----------------------------------------------------------------------
    def test_methods_unchanged(self, config: DataclassTestConfig) -> None:
        cls = config.dataclass_class
        generated = _dataclass_generated_methods(cls)

        current_methods = {
            name
            for name, value in vars(cls).items()
            if _is_method_defined_on(cls, value)
            and not getattr(value, "__isabstractmethod__", False)
            and name not in generated
        }

        assert current_methods == config.expected_methods, (
            f"Methods changed! Current: {current_methods}, Expected: {config.expected_methods}"
        )

    def test_abstract_methods_unchanged(self, config: DataclassTestConfig) -> None:
        cls = config.dataclass_class
        generated = _dataclass_generated_methods(cls)

        current_abstract_methods = {
            name
            for name, value in vars(cls).items()
            if _is_method_defined_on(cls, value)
            and getattr(value, "__isabstractmethod__", False)
            and name not in generated
        }

        assert current_abstract_methods == config.expected_abstract_methods, (
            f"Abstract methods changed! Current: {current_abstract_methods}, Expected: {config.expected_abstract_methods}"
        )

    # ----------------------------------------------------------------------
    # Contract tests (class methods)
    # ----------------------------------------------------------------------
    def test_class_methods_unchanged(self, config: DataclassTestConfig) -> None:
        cls = config.dataclass_class

        current_class_methods = {name for name, value in vars(cls).items() if _is_classmethod_defined_on(cls, value)}

        assert current_class_methods == config.expected_class_methods, (
            f"Class methods changed! Current: {current_class_methods}, Expected: {config.expected_class_methods}"
        )
