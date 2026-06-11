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

"""HTTP font file downloader with retry and parallel support."""

from __future__ import annotations

import concurrent.futures
import logging
import random
import time
from typing import TYPE_CHECKING

import requests
from tqdm import tqdm

from tenderness.font_files.downloader_spec import FontFileDownloadResult, FontFileDownloadSource
from tenderness.font_files.integrity import CheckSumUtils, DuplicateChecker

if TYPE_CHECKING:
    import pathlib

logger = logging.getLogger(__name__)


class FontFileDownloader:
    """HTTP downloader for font files with retry, backoff, and parallel support.

    Attributes
    ----------
    DEFAULT_TIMEOUT
        Default request timeout in seconds.
    DEFAULT_MAX_RETRIES
        Default maximum number of download attempts per file.
    DEFAULT_BACKOFF_BASE
        Default base for exponential backoff between retries.
    DEFAULT_DELAY_BETWEEN
        Default seconds to wait between parallel download submissions.
    DEFAULT_MAX_WORKERS
        Default maximum number of concurrent download threads.
    CHUNK_SIZE
        Byte size of each streamed chunk when writing to disk.
    """

    DEFAULT_TIMEOUT = 30
    DEFAULT_MAX_RETRIES = 3
    DEFAULT_BACKOFF_BASE = 2.0
    DEFAULT_DELAY_BETWEEN = 0.5
    DEFAULT_MAX_WORKERS = 4
    CHUNK_SIZE = 1024 * 64

    def __init__(
        self,
        *,
        timeout: int = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
        backoff_base: float = DEFAULT_BACKOFF_BASE,
        delay_between: float = DEFAULT_DELAY_BETWEEN,
        max_workers: int = DEFAULT_MAX_WORKERS,
        session: requests.Session | None = None,
    ) -> None:
        """Initialize FontFileDownloader.

        Parameters
        ----------
        timeout
            Request timeout in seconds.
        max_retries
            Maximum number of download attempts per file.
        backoff_base
            Base for exponential backoff between retries.
        delay_between
            Seconds to wait between parallel download submissions.
        max_workers
            Maximum number of concurrent download threads.
        session
            Requests session to use; a default session is created when ``None``.
        """
        self.timeout = timeout
        self.max_retries = max_retries
        self.backoff_base = backoff_base
        self.delay_between = delay_between
        self.max_workers = max_workers
        self._session = session or self._build_session()

    def download(self, source: FontFileDownloadSource, output_dir: pathlib.Path) -> FontFileDownloadResult:
        """Download a single font file to output_dir with retry on transient errors.

        Parameters
        ----------
        source
            Download source specifying the URL and target file name.
        output_dir
            Directory to save the downloaded file.

        Returns
        -------
        FontFileDownloadResult
            Result with success status, output path, and SHA-256 checksum.
        """
        output_dir = output_dir.resolve()
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file_path = output_dir.joinpath(source.file_name)

        for attempt in range(1, self.max_retries + 1):
            try:
                logger.debug("Attempt %d/%d — %s", attempt, self.max_retries, source.url)
                self._fetch_to_disk(url=source.url, dest_path=output_file_path)
                sha256_val = CheckSumUtils.compute_sha256(file_path=output_file_path)
                logger.debug("Downloaded %s → %s (sha256: %s)", source.url, output_file_path, sha256_val)
                return FontFileDownloadResult(
                    url=source.url,
                    output_file_path=output_file_path,
                    success=True,
                    sha256=sha256_val,
                )

            except (requests.ConnectionError, requests.Timeout) as exc:
                logger.warning("Transient error on attempt %d for %s: %s", attempt, source.url, exc)
            except requests.HTTPError as exc:
                status = exc.response.status_code if exc.response is not None else "?"
                if status in {429, 500, 502, 503, 504}:
                    logger.warning("Retryable HTTP %s on attempt %d for %s", status, attempt, source.url)
                else:
                    logger.exception("Non-retryable HTTP %s for %s — giving up", status, source.url)
                    break

            if attempt < self.max_retries:
                wait = self.backoff_base**attempt * random.uniform(0.8, 1.2)
                logger.debug("Backing off %.2fs before retry", wait)
                time.sleep(wait)

        logger.error("All %d attempts failed for %s", self.max_retries, source.url)
        return FontFileDownloadResult(url=source.url, output_file_path=output_dir, success=False, sha256=None)

    def download_parallel(
        self, sources: list[FontFileDownloadSource], output_dir: pathlib.Path
    ) -> list[FontFileDownloadResult]:
        """Download multiple font files in parallel.

        Parameters
        ----------
        sources
            List of download sources; duplicate URLs or file names are rejected.
        output_dir
            Directory to save the downloaded files.

        Returns
        -------
        list[FontFileDownloadResult]
            One result per source, in completion order.
        """
        # validate no duplicates in sources before starting downloads
        sources = DuplicateChecker.validate(sources, check_fields=["url", "file_name"])

        results: list[FontFileDownloadResult] = []

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as pool:
            future_to_source: dict[concurrent.futures.Future[FontFileDownloadResult], FontFileDownloadSource] = {}

            for i, source in enumerate(sources):
                if i > 0:
                    time.sleep(self.delay_between)
                future = pool.submit(self.download, source, output_dir)
                future_to_source[future] = source

            with tqdm(total=len(sources), desc="Downloading fonts", unit="file") as bar:
                for future in concurrent.futures.as_completed(future_to_source):
                    source = future_to_source[future]
                    try:
                        result = future.result()
                    except Exception:
                        logger.exception("Unexpected error downloading")
                        result = FontFileDownloadResult(
                            url=source.url,
                            output_file_path=output_dir.joinpath(source.file_name),
                            success=False,
                        )
                    results.append(result)
                    status = "✓" if result.success else "✗"
                    bar.set_postfix_str(f"{status} {source.file_name}")
                    bar.update(1)

        # validate no duplicates in results — exclude failed downloads (sha256=None) from sha256 check
        successful = [r for r in results if r.sha256 is not None]
        if successful:
            DuplicateChecker.validate(successful, check_fields=["sha256", "output_file_path"])

        ok = sum(r.success for r in results)
        logger.info("Completed %d/%d downloads successfully.", ok, len(results))
        return results

    def _fetch_to_disk(self, url: str, dest_path: pathlib.Path) -> None:
        """Stream a single URL to a .part file, then atomically rename on success.

        Parameters
        ----------
        url
            URL to download.
        dest_path
            Final destination path for the downloaded file.

        Raises
        ------
        Exception
            Re-raises any exception from the HTTP request or disk write after
            cleaning up the partial file.
        """
        tmp_path = dest_path.with_suffix(dest_path.suffix + ".part")
        try:
            with self._session.get(url, stream=True, timeout=self.timeout) as resp:
                resp.raise_for_status()
                with tmp_path.open("wb") as fh:
                    for chunk in resp.iter_content(chunk_size=self.CHUNK_SIZE):
                        if chunk:
                            fh.write(chunk)
            tmp_path.replace(dest_path)
        except Exception:
            tmp_path.unlink(missing_ok=True)
            raise

    @staticmethod
    def _build_session() -> requests.Session:
        session = requests.Session()
        session.headers.update({"User-Agent": "font-downloader/1.0 (python-requests)"})
        return session
