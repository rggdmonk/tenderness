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

"""Duplicate detection and checksum utilities for font file integrity checks."""

from __future__ import annotations

import hashlib
import itertools
import pathlib
from collections import defaultdict
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Callable, Iterable


class DuplicateChecker:
    """Utilities for detecting duplicate values across object collections."""

    @staticmethod
    def find_duplicate[T](
        items: Iterable[T], attr_name: str, transform: Callable[[Any], Any] | None = None
    ) -> dict[Any, list[T]]:
        """Return a mapping of duplicate values to the objects that share them.

        Parameters
        ----------
        items
            Objects to inspect.
        attr_name
            Attribute name to check for duplicates.
        transform
            Optional callable to normalize values before comparison (e.g. ``str.lower``).

        Returns
        -------
        dict[Any, list[T]]
            Mapping of duplicate values to the objects that share them.
        """
        grouped = defaultdict(list)

        for item in items:
            # dynamically get the value from the dataclass/object
            val = getattr(item, attr_name)
            # apply transformation (e.g., .lower()) if provided
            key = transform(val) if transform else val
            grouped[key].append(item)

        # filter to return only entries that have more than one object
        return {value: instances for value, instances in grouped.items() if len(instances) > 1}

    @staticmethod
    def raise_if_duplicates[T](items: Iterable[T], attr_name: str) -> None:
        """Raise ValueError if any duplicate values are found for attr_name.

        Parameters
        ----------
        items
            Objects to inspect.
        attr_name
            Attribute name to check for duplicates.

        Raises
        ------
        ValueError
            If any attribute value appears more than once.
        """
        dups = DuplicateChecker.find_duplicate(items, attr_name)
        if dups:
            first_val = list(dups.keys())[0]  # noqa: RUF015
            count = len(dups[first_val])
            msg = f"Field '{attr_name}' has duplicates: '{first_val}' found {count} times."
            raise ValueError(msg)

    @staticmethod
    def validate[T](*iterables: Iterable[T], check_fields: Iterable[str]) -> list[T]:
        """Merge iterables, validate field uniqueness, and return a flattened list.

        Parameters
        ----------
        *iterables
            One or more iterables to combine.
        check_fields
            Attribute names that must be unique across all items.

        Returns
        -------
        list[T]
            Flattened list of all items from the merged iterables.
        """
        combined_list = list(itertools.chain.from_iterable(iterables))
        for field in check_fields:
            DuplicateChecker.raise_if_duplicates(combined_list, field)

        return combined_list


class CheckSumUtils:
    """SHA-256 checksum utilities for file integrity verification."""

    @staticmethod
    def compute_sha256(file_path: pathlib.Path) -> str:
        """Compute and return the SHA-256 hex digest of a file.

        Parameters
        ----------
        file_path
            Path to the file to hash.

        Returns
        -------
        str
            SHA-256 hex digest of the file.

        Raises
        ------
        FileNotFoundError
            If file_path does not exist or is not a regular file.
        """
        if not isinstance(file_path, pathlib.Path):
            file_path = pathlib.Path(file_path)

        if not file_path.is_file():
            msg = f"File {file_path} does not exist or is not a file."
            raise FileNotFoundError(msg)

        hash_sha256 = hashlib.sha256()
        with file_path.open("rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)

        return hash_sha256.hexdigest()
