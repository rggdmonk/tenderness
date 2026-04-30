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

from dataclasses import dataclass

import pytest

from tenderness.core.base_interface import BaseInterface, BaseInterfaceParameters
from tenderness.core.sentinel import _UNSET_PARAM

# ---------------------------------------------------------------------------
# Concrete helpers shared across test classes
# ---------------------------------------------------------------------------


@dataclass
class SimpleParams(BaseInterfaceParameters):
    width: int = _UNSET_PARAM  # type: ignore[assignment]
    height: int = _UNSET_PARAM  # type: ignore[assignment]
    label: str = _UNSET_PARAM  # type: ignore[assignment]


class SimpleInterface(BaseInterface):
    def __init__(self, name: str = "") -> None:
        super().__init__(name)
        self._width: int = 0
        self._height: int = 0
        self._label: str = ""

    @property
    def width(self) -> int:
        return self._width

    @width.setter
    def width(self, value: int) -> None:
        self._width = value

    @property
    def height(self) -> int:
        return self._height

    @height.setter
    def height(self, value: int) -> None:
        self._height = value

    @property
    def label(self) -> str:
        return self._label

    @label.setter
    def label(self, value: str) -> None:
        self._label = value

    @property
    def read_only(self) -> str:
        return "immutable"


# ---------------------------------------------------------------------------
# TestBaseInterfaceParameters
# ---------------------------------------------------------------------------


class TestBaseInterfaceParameters:
    def test_all_set_fields_are_collected(self) -> None:
        params = SimpleParams(width=100, height=200, label="hello")
        assert params._set_params == {"width": 100, "height": 200, "label": "hello"}

    def test_unset_fields_are_excluded(self) -> None:
        params = SimpleParams(width=42)
        assert params._set_params == {"width": 42}
        assert "height" not in params._set_params
        assert "label" not in params._set_params

    def test_empty_params_produces_empty_dict(self) -> None:
        params = SimpleParams()
        assert params._set_params == {}

    def test_falsy_values_are_kept(self) -> None:
        """0, empty string, and False are valid values, not sentinels."""
        params = SimpleParams(width=0, label="")
        assert params._set_params["width"] == 0
        assert params._set_params["label"] == ""

    def test_sentinel_itself_is_excluded(self) -> None:
        params = SimpleParams(width=_UNSET_PARAM)  # type: ignore[arg-type]
        assert "width" not in params._set_params


# ---------------------------------------------------------------------------
# TestSetterDispatch
# ---------------------------------------------------------------------------


class TestSetterDispatch:
    def test_dispatch_contains_all_settable_properties(self) -> None:
        dispatch = SimpleInterface._SETTER_DISPATCH
        assert "width" in dispatch
        assert "height" in dispatch
        assert "label" in dispatch

    def test_read_only_property_excluded_from_dispatch(self) -> None:
        assert "read_only" not in SimpleInterface._SETTER_DISPATCH

    def test_dispatch_values_are_callable(self) -> None:
        for setter in SimpleInterface._SETTER_DISPATCH.values():
            assert callable(setter)

    def test_subclass_inherits_parent_setters(self) -> None:
        class ChildInterface(SimpleInterface):
            def __init__(self) -> None:
                super().__init__()
                self._extra: str = ""

            @property
            def extra(self) -> str:
                return self._extra

            @extra.setter
            def extra(self, value: str) -> None:
                self._extra = value

        dispatch = ChildInterface._SETTER_DISPATCH
        assert "width" in dispatch
        assert "height" in dispatch
        assert "extra" in dispatch

    def test_subclass_override_replaces_parent_setter(self) -> None:
        class OverridingInterface(SimpleInterface):
            @property
            def width(self) -> int:
                return self._width * 2

            @width.setter
            def width(self, value: int) -> None:
                self._width = value * 2

        iface = OverridingInterface()
        iface.width = 10
        assert iface._width == 20  # setter ran: 10 * 2

    def test_dispatch_is_per_class_not_shared(self) -> None:
        class SiblingInterface(BaseInterface):
            @property
            def sibling_prop(self) -> int:
                return 0

            @sibling_prop.setter
            def sibling_prop(self, v: int) -> None:
                pass

        assert "sibling_prop" not in SimpleInterface._SETTER_DISPATCH
        assert "width" not in SiblingInterface._SETTER_DISPATCH


# ---------------------------------------------------------------------------
# TestUpdateParameters
# ---------------------------------------------------------------------------


class TestUpdateParameters:
    def test_sets_provided_fields(self) -> None:
        iface = SimpleInterface()
        params = SimpleParams(width=800, height=600)
        iface.update_with_parameters(params)
        assert iface.width == 800
        assert iface.height == 600

    def test_does_not_overwrite_unset_fields(self) -> None:
        iface = SimpleInterface()
        iface._width = 999
        params = SimpleParams(height=100)
        iface.update_with_parameters(params)
        assert iface.width == 999  # untouched
        assert iface.height == 100

    def test_empty_params_is_a_no_op(self) -> None:
        iface = SimpleInterface()
        iface._width = 42
        iface.update_with_parameters(SimpleParams())
        assert iface.width == 42

    def test_raises_on_unknown_parameter(self) -> None:
        @dataclass
        class ParamsWithUnknown(BaseInterfaceParameters):
            nonexistent: int = _UNSET_PARAM  # type: ignore[assignment]

        iface = SimpleInterface()
        with pytest.raises(AttributeError, match="unknown or read-only parameter 'nonexistent'"):
            iface.update_with_parameters(ParamsWithUnknown(nonexistent=1))

    def test_raises_on_read_only_parameter(self) -> None:
        @dataclass
        class ParamsWithReadOnly(BaseInterfaceParameters):
            read_only: str = _UNSET_PARAM  # type: ignore[assignment]

        iface = SimpleInterface()
        with pytest.raises(AttributeError, match="unknown or read-only parameter 'read_only'"):
            iface.update_with_parameters(ParamsWithReadOnly(read_only="x"))

    def test_error_message_includes_class_name(self) -> None:
        @dataclass
        class BadParams(BaseInterfaceParameters):
            ghost: int = _UNSET_PARAM  # type: ignore[assignment]

        iface = SimpleInterface(name="my_iface")
        with pytest.raises(AttributeError, match="SimpleInterface"):
            iface.update_with_parameters(BadParams(ghost=0))

    def test_second_call_merges_not_resets(self) -> None:
        iface = SimpleInterface()
        iface.update_with_parameters(SimpleParams(width=10))
        iface.update_with_parameters(SimpleParams(height=20))
        assert iface.width == 10
        assert iface.height == 20


# ---------------------------------------------------------------------------
# TestUpdateParametersFromKwargs
# ---------------------------------------------------------------------------


class TestUpdateParametersFromKwargs:
    def test_sets_single_kwarg(self) -> None:
        iface = SimpleInterface()
        iface._update_with_parameters_from_kwargs(width=50)
        assert iface.width == 50

    def test_sets_multiple_kwargs(self) -> None:
        iface = SimpleInterface()
        iface._update_with_parameters_from_kwargs(width=1, height=2, label="x")
        assert iface.width == 1
        assert iface.height == 2
        assert iface.label == "x"

    def test_no_kwargs_is_a_no_op(self) -> None:
        iface = SimpleInterface()
        iface._width = 7
        iface._update_with_parameters_from_kwargs()
        assert iface.width == 7

    def test_raises_on_unknown_kwarg(self) -> None:
        iface = SimpleInterface()
        with pytest.raises(AttributeError, match="unknown or read-only parameter 'ghost'"):
            iface._update_with_parameters_from_kwargs(ghost=1)

    def test_raises_on_read_only_kwarg(self) -> None:
        iface = SimpleInterface()
        with pytest.raises(AttributeError, match="unknown or read-only parameter 'read_only'"):
            iface._update_with_parameters_from_kwargs(read_only="nope")

    def test_error_halts_remaining_kwargs(self) -> None:
        """Once an unknown kwarg is hit, processing stops — later kwargs are not applied."""
        iface = SimpleInterface()
        with pytest.raises(AttributeError):
            # dict ordering is insertion-ordered in 3.7+; ghost is processed first
            iface._update_with_parameters_from_kwargs(ghost=99, width=10)
        assert iface.width == 0  # never reached


# ---------------------------------------------------------------------------
# TestUpdateParametersUnsafeKwargs
# ---------------------------------------------------------------------------


class TestUpdateParametersUnsafeKwargs:
    def test_sets_known_property(self) -> None:
        iface = SimpleInterface()
        iface._update_with_parameters_unsafe_kwargs(width=123)
        assert iface.width == 123

    def test_sets_arbitrary_attribute_without_raising(self) -> None:
        iface = SimpleInterface()
        iface._update_with_parameters_unsafe_kwargs(totally_unknown=True)
        assert iface.totally_unknown is True  # type: ignore[attr-defined]

    def test_overwrites_existing_attribute(self) -> None:
        iface = SimpleInterface()
        iface._update_with_parameters_unsafe_kwargs(name="first")
        iface._update_with_parameters_unsafe_kwargs(name="second")
        assert iface.name == "second"

    def test_no_kwargs_is_a_no_op(self) -> None:
        iface = SimpleInterface()
        iface._update_with_parameters_unsafe_kwargs()
        assert not hasattr(iface, "surprise")


# ---------------------------------------------------------------------------
# TestBaseInterfaceRepr
# ---------------------------------------------------------------------------


class TestBaseInterfaceRepr:
    def test_repr_includes_class_name_and_name(self) -> None:
        iface = SimpleInterface(name="my_layout")
        assert repr(iface) == "SimpleInterface(name='my_layout')"

    def test_repr_with_empty_name(self) -> None:
        iface = SimpleInterface()
        assert repr(iface) == "SimpleInterface(name='')"
