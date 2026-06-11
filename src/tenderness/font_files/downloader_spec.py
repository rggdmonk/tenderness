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

"""Font file download source and result dataclasses."""

from __future__ import annotations

import pathlib
from dataclasses import asdict, dataclass
from urllib.parse import unquote, urlparse


@dataclass(slots=True)
class FontFileDownloadSource:
    """Source specification for a font file download.

    Attributes
    ----------
    url
        URL to download from.
    file_name
        Target file name; inferred from the URL path when empty.
    """

    url: str
    file_name: str = ""

    def __post_init__(self) -> None:
        """Infer file_name from url when not provided."""
        if not self.file_name:
            self.extract_file_name()

    def extract_file_name(self) -> None:
        """Extract and set file_name from the URL path.

        Raises
        ------
        ValueError
            If a file name cannot be inferred from the URL.
        TypeError
            If the parsed file name is not a string.
        """
        parsed_url = urlparse(self.url)
        file_name = pathlib.Path(unquote(parsed_url.path)).name

        if not file_name:
            msg = f"Cannot infer file_name from URL: {self.url}"
            raise ValueError(msg)
        if not isinstance(file_name, str):
            msg = f"Parsed file_name is not a string: {file_name!r} from URL: {self.url}"
            raise TypeError(msg)

        self.file_name = file_name.lower()

    def to_dict(self) -> dict[str, str]:
        """Return a dict representation of this source.

        Returns
        -------
        dict[str, str]
            Dictionary with ``url`` and ``file_name`` keys.
        """
        return asdict(self)

    def __str__(self) -> str:
        """Return a human-readable summary.

        Returns
        -------
        str
            ``"<file_name> ← <url>"`` formatted string.
        """
        return f"{self.file_name} ← {self.url}"


@dataclass(slots=True)
class FontFileDownloadResult:
    """Result of a single font file download attempt.

    Attributes
    ----------
    url
        URL that was downloaded.
    output_file_path
        Path where the file was saved.
    success
        ``True`` if the download succeeded.
    sha256
        Hex digest of the downloaded file; ``None`` if the download failed.
    """

    url: str
    output_file_path: pathlib.Path
    success: bool
    sha256: str | None = None  # hex digest; None if download failed

    def to_dict(self) -> dict[str, str | bool | pathlib.Path | None]:
        """Return a dict representation of this result.

        Returns
        -------
        dict[str, str | bool | pathlib.Path | None]
            Dictionary with ``url``, ``output_file_path``, ``success``, and ``sha256`` keys.
        """
        return asdict(self)
