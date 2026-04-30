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
from dataclasses import dataclass, field
from functools import cached_property

import pytest

from tests._test_utils.helpers import (
    _is_classmethod_defined_on,
    _is_method_defined_on,
    _is_property_defined_on,
    _is_staticmethod_defined_on,
)


@dataclass(slots=True, frozen=True)
class ClassTestConfig:
    cls: type
    is_abstract: bool = field(default=False)

    expected_properties: set[str] = field(default_factory=set)
    expected_abstract_properties: set[str] = field(default_factory=set)

    expected_methods: set[str] = field(default_factory=set)
    expected_abstract_methods: set[str] = field(default_factory=set)

    expected_class_methods: set[str] = field(default_factory=set)
    expected_static_methods: set[str] = field(default_factory=set)

    expected_class_vars: set[str] = field(default_factory=set)


class ClassTestBase:
    pytestmark = pytest.mark.eternal_contract

    # ----------------------------------------------------------------------
    # Structural tests
    # ----------------------------------------------------------------------
    def test_is_class(self, config: ClassTestConfig) -> None:
        assert inspect.isclass(config.cls), f"{config.cls.__name__} is not a class"

    def test_is_abstract(self, config: ClassTestConfig) -> None:
        is_actually_abstract = inspect.isabstract(config.cls) or bool(getattr(config.cls, "__abstractmethods__", False))

        if config.is_abstract:
            assert is_actually_abstract, f"{config.cls.__name__} should be abstract but is concrete."
            assert issubclass(config.cls, ABC), f"{config.cls.__name__} is abstract so it should inherit from ABC."
        else:
            assert not is_actually_abstract, f"{config.cls.__name__} should be concrete but is abstract."

    # ----------------------------------------------------------------------
    # Contract tests (properties)
    # ----------------------------------------------------------------------
    def test_properties_unchanged(self, config: ClassTestConfig) -> None:
        cls = config.cls
        current_props = {
            name
            for name, value in vars(cls).items()
            if _is_property_defined_on(cls, value) and not getattr(value.fget, "__isabstractmethod__", False)
        }
        assert current_props == config.expected_properties, (
            f"Properties changed! Current: {current_props}, Expected: {config.expected_properties}"
        )

    def test_abstract_properties_unchanged(self, config: ClassTestConfig) -> None:
        cls = config.cls
        current_abstract_props = {
            name
            for name, value in vars(cls).items()
            if _is_property_defined_on(cls, value) and getattr(value.fget, "__isabstractmethod__", False)
        }
        assert current_abstract_props == config.expected_abstract_properties, (
            f"Abstract properties changed! Current: {current_abstract_props}, Expected: {config.expected_abstract_properties}"
        )

    # ----------------------------------------------------------------------
    # Contract tests (methods)
    # ----------------------------------------------------------------------
    def test_methods_unchanged(self, config: ClassTestConfig) -> None:
        cls = config.cls
        current_methods = {
            name
            for name, value in vars(cls).items()
            if _is_method_defined_on(cls, value)
            and not getattr(value, "__isabstractmethod__", False)
            and not name.startswith("__")
        }
        assert current_methods == config.expected_methods, (
            f"Methods changed! Current: {current_methods}, Expected: {config.expected_methods}"
        )

    def test_abstract_methods_unchanged(self, config: ClassTestConfig) -> None:
        cls = config.cls
        current_abstract_methods = {
            name
            for name, value in vars(cls).items()
            if _is_method_defined_on(cls, value) and getattr(value, "__isabstractmethod__", False)
        }
        assert current_abstract_methods == config.expected_abstract_methods, (
            f"Abstract methods changed! Current: {current_abstract_methods}, Expected: {config.expected_abstract_methods}"
        )

    # ----------------------------------------------------------------------
    # Contract tests (class methods)
    # ----------------------------------------------------------------------
    def test_class_methods_unchanged(self, config: ClassTestConfig) -> None:
        cls = config.cls
        current_class_methods = {
            name
            for name, value in vars(cls).items()
            if _is_classmethod_defined_on(cls, value) and not name.startswith("__")
        }
        assert current_class_methods == config.expected_class_methods, (
            f"Class methods changed! Current: {current_class_methods}, Expected: {config.expected_class_methods}"
        )

    # ----------------------------------------------------------------------
    # Contract tests (static methods)
    # ----------------------------------------------------------------------
    def test_static_methods_unchanged(self, config: ClassTestConfig) -> None:
        cls = config.cls
        current_static_methods = {
            name
            for name, value in vars(cls).items()
            if _is_staticmethod_defined_on(cls, value) and not name.startswith("__")
        }
        assert current_static_methods == config.expected_static_methods, (
            f"Static methods changed! Current: {current_static_methods}, Expected: {config.expected_static_methods}"
        )

    # ----------------------------------------------------------------------
    # Contract tests (class vars)
    # ----------------------------------------------------------------------
    def test_class_vars_unchanged(self, config: ClassTestConfig) -> None:
        cls = config.cls
        current_class_vars = {
            name
            for name, value in vars(cls).items()
            if not name.startswith("__")
            and not name.startswith("_abc_")
            and not _is_method_defined_on(cls, value)
            and not isinstance(value, (property, cached_property, classmethod, staticmethod))
        }
        assert current_class_vars == config.expected_class_vars, (
            f"Class vars changed! Current: {current_class_vars}, Expected: {config.expected_class_vars}"
        )
