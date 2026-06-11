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

import pathlib
import sys

import pytest

from tests._test_utils.paths_test import TESTS_OUTPUT_DIR


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--output-path",
        default=None,
        help="Base output directory for test artifacts",
    )


@pytest.fixture(scope="session")
def tests_output_dir(request: pytest.FixtureRequest) -> pathlib.Path:
    opt = request.config.getoption("--output-path")
    py_version = f"{sys.version_info.major}.{sys.version_info.minor}"
    path = pathlib.Path(opt) if opt else TESTS_OUTPUT_DIR / f"{py_version}_local"
    path.mkdir(parents=True, exist_ok=True)
    return path
