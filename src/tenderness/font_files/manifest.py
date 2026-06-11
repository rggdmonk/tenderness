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

"""Font manifest I/O, integrity verification, and download orchestration."""

from __future__ import annotations

import json
import logging
import pathlib
import shutil
from dataclasses import asdict, dataclass
from typing import Self

from tenderness.core.cache_paths import TENDERNESS_FONTS_DIR
from tenderness.font_files.downloader import FontFileDownloader
from tenderness.font_files.downloader_spec import FontFileDownloadResult, FontFileDownloadSource
from tenderness.font_files.integrity import CheckSumUtils

logger = logging.getLogger(__name__)

TENDERNESS_FONT_FILES_MANIFEST_SUBDIR = "manifests"


@dataclass(slots=True)
class FontManifestEntry:
    """Single font file entry within a manifest.

    Attributes
    ----------
    file_name
        Local filename for the font file.
    url
        Download URL for the font file.
    sha256
        Expected SHA-256 checksum of the font file.
    """

    file_name: str
    url: str
    sha256: str

    def to_dict(self) -> dict[str, str]:
        """Return a dict representation of this entry.

        Returns
        -------
        dict[str, str]
            Dictionary with ``file_name``, ``url``, and ``sha256`` keys.
        """
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> Self:
        """Create a FontManifestEntry from a dict.

        Parameters
        ----------
        data
            Dictionary with ``file_name``, ``url``, and ``sha256`` keys.

        Returns
        -------
        Self
            A new ``FontManifestEntry`` instance.
        """
        return cls(file_name=data["file_name"], url=data["url"], sha256=data["sha256"])

    def to_download_source(self) -> FontFileDownloadSource:
        """Return a FontFileDownloadSource for this entry.

        Returns
        -------
        FontFileDownloadSource
            Download source derived from this entry's URL and filename.
        """
        return FontFileDownloadSource(url=self.url, file_name=self.file_name)


class FontManifestFile:
    """Reads and writes manifest JSON files to disk."""

    def __init__(self, manifest_path: pathlib.Path) -> None:
        """Initialize FontManifestFile.

        Parameters
        ----------
        manifest_path
            Path to the manifest JSON file.
        """
        self.manifest_path = manifest_path

    @property
    def manifest_name(self) -> str:
        """Stem of the manifest file path."""
        return self.manifest_path.stem

    def save_manifest(self, entries: list[FontManifestEntry]) -> None:
        """Write entries to the manifest JSON file.

        Parameters
        ----------
        entries
            Font manifest entries to write.
        """
        with self.manifest_path.open("w", encoding="utf-8") as f:
            json.dump([e.to_dict() for e in entries], f, indent=4)

    def load_manifest(self) -> list[FontManifestEntry]:
        """Load and return entries from the manifest JSON file.

        Returns
        -------
        list[FontManifestEntry]
            Deserialized list of manifest entries.

        Raises
        ------
        FileNotFoundError
            If the manifest file does not exist.
        ValueError
            If the file content is not a list of dicts.
        """
        if not self.manifest_path.is_file():
            msg = f"Manifest not found: {self.manifest_path}"
            raise FileNotFoundError(msg)

        with self.manifest_path.open("r", encoding="utf-8") as f:
            raw = json.load(f)

        if not isinstance(raw, list) or not all(isinstance(i, dict) for i in raw):
            msg = f"Invalid manifest format in {self.manifest_path}: expected a list of dicts, got {type(raw).__name__}"
            msg += f"\nRaw content: {raw!r}"
            raise ValueError(msg)

        return [FontManifestEntry.from_dict(item) for item in raw]


class FontManifestStore:
    """Manages the cache directory layout and manifest discovery."""

    def __init__(self, cache_dir: pathlib.Path) -> None:
        """Initialize FontManifestStore.

        Parameters
        ----------
        cache_dir
            Root cache directory; created if it does not exist.
        """
        self.cache_dir = cache_dir
        self.manifest_files_dir = cache_dir / TENDERNESS_FONT_FILES_MANIFEST_SUBDIR
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.manifest_files_dir.mkdir(parents=True, exist_ok=True)

    def get_manifest_file(self, name_or_path: str | pathlib.Path) -> FontManifestFile:
        """Return a FontManifestFile for the given name or path.

        Parameters
        ----------
        name_or_path
            An absolute path to a manifest file, or a bare name resolved
            within the manifest files directory.

        Returns
        -------
        FontManifestFile
            File handle for the manifest at the resolved path.
        """
        path = pathlib.Path(name_or_path).resolve()
        if path.is_file():
            return FontManifestFile(manifest_path=path)
        return FontManifestFile(manifest_path=self.manifest_files_dir / f"{path.stem}.json")

    def get_fonts_dir_for(self, manifest_name: str) -> pathlib.Path:
        """Return the fonts directory for a manifest, creating it if needed.

        Parameters
        ----------
        manifest_name
            Name of the manifest.

        Returns
        -------
        pathlib.Path
            Path to the fonts directory for this manifest.
        """
        fonts_dir = self.cache_dir / manifest_name
        fonts_dir.mkdir(parents=True, exist_ok=True)
        return fonts_dir

    def list_manifests(self) -> list[str]:
        """Return a sorted list of available manifest names.

        Returns
        -------
        list[str]
            Sorted manifest names.
        """
        return sorted(p.stem for p in self.manifest_files_dir.glob("*.json"))

    def clear(self, manifest_name: str | None = None, *, should_remove_manifests: bool = False) -> None:
        """Clear cached fonts, optionally removing manifest files.

        Parameters
        ----------
        manifest_name
            Name of a specific manifest to clear; all manifests are cleared when ``None``.
        should_remove_manifests
            Also delete manifest JSON files when ``True``.
        """
        if manifest_name:
            self._clear_specific_manifest(manifest_name, remove_manifest_file=should_remove_manifests)
        else:
            self._clear_all_cache(remove_manifests=should_remove_manifests)

    def _clear_specific_manifest(self, manifest_name: str, *, remove_manifest_file: bool) -> None:
        """Clear fonts and optionally the manifest file for a specific manifest.

        Parameters
        ----------
        manifest_name
            Name of the manifest to clear.
        remove_manifest_file
            Also delete the manifest JSON file when ``True``.
        """
        fonts_dir = self.cache_dir / manifest_name
        if fonts_dir.exists():
            shutil.rmtree(fonts_dir)
        if remove_manifest_file:
            manifest_path = self.manifest_files_dir / f"{manifest_name}.json"
            manifest_path.unlink(missing_ok=True)

    def _clear_all_cache(self, *, remove_manifests: bool) -> None:
        """Clear all cached fonts and optionally all manifest files.

        Parameters
        ----------
        remove_manifests
            Also delete all manifest JSON files when ``True``.
        """
        for item in self.cache_dir.iterdir():
            if item.is_dir() and item.name != TENDERNESS_FONT_FILES_MANIFEST_SUBDIR:
                shutil.rmtree(item)
        if remove_manifests:
            shutil.rmtree(self.manifest_files_dir)
            self.manifest_files_dir.mkdir()


@dataclass(slots=True)
class ManifestVerificationReport:
    """Result of verifying cached fonts against a manifest.

    Attributes
    ----------
    manifest_name
        Name of the manifest that was verified.
    valid
        File names of fonts that are present and have correct checksums.
    missing
        File names of fonts that are not present in the cache.
    corrupt
        File names of fonts that failed the checksum check.
    """

    manifest_name: str
    valid: list[str]
    missing: list[str]
    corrupt: list[str]

    @property
    def is_healthy(self) -> bool:
        """True when no fonts are missing or corrupt."""
        return not self.missing and not self.corrupt


class FontManifestVerifier:
    """Read-only integrity checks against a manifest store."""

    def __init__(self, manifest_store: FontManifestStore) -> None:
        """Initialize FontManifestVerifier.

        Parameters
        ----------
        manifest_store
            Store to read manifests and font directories from.
        """
        self.manifest_store = manifest_store

    def is_ready(self, manifest_name: str) -> bool:
        """Check if the manifest exists and all fonts are cached and intact.

        Parameters
        ----------
        manifest_name
            Name of the manifest to check.

        Returns
        -------
        bool
            ``True`` if all fonts are present and pass integrity checks.
        """
        try:
            report = self.verify(manifest_name=manifest_name)
        except FileNotFoundError:
            return False
        return report.is_healthy

    def verify(self, manifest_name: str) -> ManifestVerificationReport:
        """Check cached fonts against the manifest without downloading anything.

        Parameters
        ----------
        manifest_name
            Name of the manifest to verify.

        Returns
        -------
        ManifestVerificationReport
            Verification report listing valid, missing, and corrupt fonts.
        """
        manifest_file = self.manifest_store.get_manifest_file(name_or_path=manifest_name)
        entries = manifest_file.load_manifest()
        fonts_dir = self.manifest_store.get_fonts_dir_for(manifest_name=manifest_name)

        valid, missing, corrupt = [], [], []

        for entry in entries:
            font_path = fonts_dir / entry.file_name
            if not font_path.exists():
                missing.append(entry.file_name)
            elif entry.sha256 and CheckSumUtils.compute_sha256(file_path=font_path) != entry.sha256:
                corrupt.append(entry.file_name)
            else:
                valid.append(entry.file_name)

        return ManifestVerificationReport(
            manifest_name=manifest_name,
            valid=valid,
            missing=missing,
            corrupt=corrupt,
        )


class FontManifestManager:
    """Orchestrates: manifest I/O, integrity checks, and font downloading."""

    def __init__(
        self,
        cache_dir: pathlib.Path | None = None,
        downloader: FontFileDownloader | None = None,
        *,
        timeout: int = FontFileDownloader.DEFAULT_TIMEOUT,
        max_retries: int = FontFileDownloader.DEFAULT_MAX_RETRIES,
        backoff_base: float = FontFileDownloader.DEFAULT_BACKOFF_BASE,
        delay_between: float = FontFileDownloader.DEFAULT_DELAY_BETWEEN,
        max_workers: int = FontFileDownloader.DEFAULT_MAX_WORKERS,
    ) -> None:
        """Initialize FontManifestManager.

        Parameters
        ----------
        cache_dir
            Root cache directory; defaults to the tenderness cache.
        downloader
            Font file downloader; a default instance is created when ``None``.
        timeout
            Download timeout in seconds.
        max_retries
            Maximum number of retry attempts per file.
        backoff_base
            Base delay in seconds for exponential back-off between retries.
        delay_between
            Delay in seconds between consecutive downloads.
        max_workers
            Maximum number of parallel download workers.
        """
        self.cache_dir = cache_dir or TENDERNESS_FONTS_DIR
        self.manifest_store = FontManifestStore(cache_dir=self.cache_dir)
        self.font_file_downloader = downloader or FontFileDownloader(
            timeout=timeout,
            max_retries=max_retries,
            backoff_base=backoff_base,
            delay_between=delay_between,
            max_workers=max_workers,
        )
        self.verifier = FontManifestVerifier(manifest_store=self.manifest_store)

    def prepare_font_files(
        self,
        sources: list[FontFileDownloadSource],
        manifest_name: str,
        *,
        force_download: bool = False,
    ) -> pathlib.Path:
        """Download fonts, save manifest, and return the fonts directory in one step.

        Parameters
        ----------
        sources
            Download sources for the font files.
        manifest_name
            Name of the manifest to create.
        force_download
            Re-download all fonts even if they are already cached.

        Returns
        -------
        pathlib.Path
            Path to the fonts directory.
        """
        self.create_manifest_file(sources=sources, manifest_name=manifest_name)
        return self.get_fonts_dir(name_or_path=manifest_name, force_download=force_download)

    def create_manifest_file(self, sources: list[FontFileDownloadSource], manifest_name: str) -> pathlib.Path:
        """Download fonts, compute hashes, and generate a new manifest file.

        Parameters
        ----------
        sources
            Download sources for the font files.
        manifest_name
            Name for the generated manifest.

        Returns
        -------
        pathlib.Path
            Path to the saved manifest JSON file.

        Raises
        ------
        ValueError
            If a downloaded file is missing its SHA-256 checksum.
        """
        fonts_dir = self.manifest_store.get_fonts_dir_for(manifest_name=manifest_name)
        results = self.font_file_downloader.download_parallel(sources=sources, output_dir=fonts_dir)
        self._raise_if_failed(results=results)

        entries = []
        for r in results:
            if r.sha256 is None:
                msg = f"Missing sha256 checksum for downloaded file: {r.output_file_path.name}"
                raise ValueError(msg)
            entries.append(FontManifestEntry(file_name=r.output_file_path.name, url=r.url, sha256=r.sha256))

        manifest_file = self.manifest_store.get_manifest_file(name_or_path=manifest_name)
        manifest_file.save_manifest(entries=entries)
        logger.info("Manifest '%s' saved (%d fonts).", manifest_name, len(entries))
        return manifest_file.manifest_path

    def get_fonts_dir(self, name_or_path: str | pathlib.Path, *, force_download: bool = False) -> pathlib.Path:
        """Return the fonts directory, downloading only what is missing or corrupt.

        Parameters
        ----------
        name_or_path
            Manifest name or path.
        force_download
            Re-download all fonts even if they are already cached.

        Returns
        -------
        pathlib.Path
            Path to the fonts directory.
        """
        manifest_file = self.manifest_store.get_manifest_file(name_or_path=name_or_path)
        entries = manifest_file.load_manifest()
        fonts_dir = self.manifest_store.get_fonts_dir_for(manifest_name=manifest_file.manifest_name)

        to_download = self._entries_needing_download(entries=entries, fonts_dir=fonts_dir, force=force_download)

        if to_download:
            sources = [e.to_download_source() for e in to_download]
            results = self.font_file_downloader.download_parallel(sources=sources, output_dir=fonts_dir)
            self._raise_if_failed(results=results)

        logger.info("Manifest '%s' ready in %s.", manifest_file.manifest_name, fonts_dir)
        return fonts_dir

    def list_available_manifests(self) -> list[str]:
        """Return a sorted list of available manifest names.

        Returns
        -------
        list[str]
            Sorted manifest names.
        """
        return self.manifest_store.list_manifests()

    def clear(self, manifest_name: str | None = None, *, should_remove_manifests: bool = False) -> None:
        """Clear cached fonts, optionally removing manifest files.

        Parameters
        ----------
        manifest_name
            Name of a specific manifest to clear; all manifests are cleared when ``None``.
        should_remove_manifests
            Also delete manifest JSON files when ``True``.
        """
        self.manifest_store.clear(manifest_name=manifest_name, should_remove_manifests=should_remove_manifests)

    def _entries_needing_download(
        self,
        entries: list[FontManifestEntry],
        fonts_dir: pathlib.Path,
        *,
        force: bool,
    ) -> list[FontManifestEntry]:
        if force:
            return entries

        needs_download = []
        for entry in entries:
            font_path = fonts_dir / entry.file_name
            if not font_path.exists():
                needs_download.append(entry)
            elif entry.sha256 and CheckSumUtils.compute_sha256(file_path=font_path) != entry.sha256:
                logger.warning("Hash mismatch for %s — queued for re-download.", entry.file_name)
                needs_download.append(entry)

        return needs_download

    def _raise_if_failed(self, results: list[FontFileDownloadResult]) -> None:
        failed = [r for r in results if not r.success]
        if failed:
            msg = f"{len(failed)} font(s) failed to download:\n" + "\n".join(f"- {r.url}" for r in failed)
            raise RuntimeError(msg)

    def is_manifest_ready(self, manifest_name: str) -> bool:
        """Check if the manifest exists and all fonts are cached and intact.

        Parameters
        ----------
        manifest_name
            Name of the manifest to check.

        Returns
        -------
        bool
            ``True`` if all fonts are present and pass integrity checks.
        """
        return self.verifier.is_ready(manifest_name=manifest_name)

    def verify_manifest(self, manifest_name: str) -> ManifestVerificationReport:
        """Verify cached fonts against the manifest and return a report.

        Parameters
        ----------
        manifest_name
            Name of the manifest to verify.

        Returns
        -------
        ManifestVerificationReport
            Verification report listing valid, missing, and corrupt fonts.
        """
        return self.verifier.verify(manifest_name=manifest_name)
