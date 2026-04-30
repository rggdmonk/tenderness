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

"""Base interface and parameter classes for cairo interfaces."""

from __future__ import annotations

import functools
import logging
from dataclasses import Field, fields
from typing import TYPE_CHECKING, Any, ClassVar

from tenderness.core.sentinel import _UNSET_PARAM

if TYPE_CHECKING:
    from collections.abc import Callable


logger = logging.getLogger(__name__)


class BaseInterfaceParameters:
    """Base class for interface parameter dataclasses with coercion and validation support."""

    __slots__ = ("_set_params",)

    _set_params: dict[str, Any]
    _COERCE_DISPATCH: ClassVar[dict[str, Callable[[Any], Any]]] = {}

    @classmethod
    @functools.cache
    def _get_coerce_dispatch(cls) -> dict[str, Callable[[Any], Any]]:
        result: dict[str, Callable[[Any], Any]] = {}
        for klass in reversed(cls.__mro__):
            if "_COERCE_DISPATCH" in klass.__dict__:
                result.update(klass.__dict__["_COERCE_DISPATCH"])
        return result

    @classmethod
    @functools.cache
    def _get_valid_field_names(cls) -> frozenset[str]:
        return frozenset(f.name for f in fields(cls))  # type: ignore[arg-type]

    @classmethod
    @functools.cache
    def _get_all_fields(cls) -> tuple[Field[Any], ...]:
        return fields(cls)  # type: ignore[arg-type]

    def _validate(self, proposed: dict[str, Any]) -> None:
        pass

    def __post_init__(self) -> None:
        """Coerce field values and collect set parameters."""
        dispatch = self._get_coerce_dispatch()
        for name, coerce in dispatch.items():
            value = getattr(self, name)
            if value is not _UNSET_PARAM:
                object.__setattr__(self, name, coerce(value))

        set_params = {
            f.name: value for f in self._get_all_fields() if (value := getattr(self, f.name)) is not _UNSET_PARAM
        }
        object.__setattr__(self, "_set_params", set_params)

        self._validate(set_params)

    def update_parameters(self, **kwargs: object) -> None:
        """Update one or more parameters by name.

        Parameters
        ----------
        **kwargs
            Parameter names and their new values.

        Raises
        ------
        AttributeError
            If any key is not a valid parameter name.
        """
        valid_names = self._get_valid_field_names()
        for key in kwargs:
            if key not in valid_names:
                msg = f"{type(self).__name__}: unknown parameter {key!r}"
                raise AttributeError(msg)

        dispatch = self._get_coerce_dispatch()
        coerced = {name: dispatch[name](value) if name in dispatch else value for name, value in kwargs.items()}

        merged = dict(self._set_params)
        for name, value in coerced.items():
            if value is not _UNSET_PARAM:
                merged[name] = value
            else:
                merged.pop(name, None)
        self._validate(merged)

        for name, value in coerced.items():
            object.__setattr__(self, name, value)
        object.__setattr__(self, "_set_params", merged)

    def _update_parameters_unsafe(self, **kwargs: object) -> None:
        """Update parameters from kwargs without name validation.

        Notes
        -----
        No field-name check is performed; callers must ensure all keys are valid.
        """
        dispatch = self._get_coerce_dispatch()
        set_params = self._set_params
        for name, value in kwargs.items():
            coerced = dispatch[name](value) if name in dispatch else value
            object.__setattr__(self, name, coerced)
            if coerced is not _UNSET_PARAM:
                set_params[name] = coerced
            else:
                set_params.pop(name, None)


class BaseInterface:
    """Base class for cairo interface wrappers.

    Parameters
    ----------
    name
        Optional label for the interface instance.
    """

    _SETTER_DISPATCH: ClassVar[dict[str, Callable[[Any, Any], None]]]

    def __init__(self, name: str = "") -> None:
        self.name = name

    def __repr__(self) -> str:
        """Return a string representation."""
        return f"{type(self).__name__}(name={self.name!r})"

    def __init_subclass__(cls, **kwargs: object) -> None:
        """Build the property setter dispatch map for the subclass on class creation."""
        super().__init_subclass__(**kwargs)

        dispatch: dict[str, Callable[[Any, Any], None]] = {}
        for klass in reversed(cls.__mro__):
            for name, obj in klass.__dict__.items():
                if isinstance(obj, property):
                    if obj.fset is not None:
                        dispatch[name] = obj.fset
                    else:
                        dispatch.pop(name, None)

        cls._SETTER_DISPATCH = dispatch

    def update_with_parameters(self, params: BaseInterfaceParameters) -> None:
        """Apply a set of parameters to the interface using property setters.

        Parameters
        ----------
        params
            Parameter object whose set fields are applied.

        Raises
        ------
        AttributeError
            If a parameter name has no corresponding writable property.
        """
        dispatch = self._SETTER_DISPATCH
        for name, value in params._set_params.items():  # noqa: SLF001
            setter = dispatch.get(name)
            if setter is None:
                msg = f"{type(self).__name__}: unknown or read-only parameter {name!r}"
                raise AttributeError(msg)
            setter(self, value)

    def _update_with_parameters_from_kwargs(self, **kwargs: object) -> None:
        """Update parameters from kwargs.

        Raises
        ------
        AttributeError
            If any name has no corresponding writable property.
        """
        dispatch = self._SETTER_DISPATCH
        for name, value in kwargs.items():
            setter = dispatch.get(name)
            if setter is None:
                msg = f"{type(self).__name__}: unknown or read-only parameter {name!r}"
                raise AttributeError(msg)
            setter(self, value)

    def _update_with_parameters_unsafe_kwargs(self, **kwargs: object) -> None:
        """Update parameters from kwargs without validation.

        Notes
        -----
        Unknown parameters are set as plain attributes; no setter dispatch is used.
        """
        for name, value in kwargs.items():
            setattr(self, name, value)
