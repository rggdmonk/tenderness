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

import pathlib
from datetime import UTC, datetime

import pytest
from _pytest.fixtures import FixtureRequest

from tests._test_utils.paths_test import TESTS_OUTPUT_DIR

E2E_TESTS_OUTPUT_DIR = TESTS_OUTPUT_DIR / "e2e"
E2E_BRANCHES = ["via_standard"]
E2E_FORMATS = ["image", "svg", "pdf"]


@pytest.fixture
def e2e_output_dir(request: FixtureRequest) -> pathlib.Path:
    """
    Creates output directory structure for tests:
    TESTS_OUTPUT_DIR/e2e/{base_dir}/{test_name}/{format}/{test_case_id}/{timestamp}/

    Works for:
    - tests/e2e/via_standard/tables/test_*.py
    - tests/e2e/via_standard/text/test_*.py


    Example: via_standard/tables/test_table_simple_uniform_grid.py[image-bleed] creates:
    .../e2e/via_standard/test_table_simple_uniform_grid/image/bleed/2024-03-31_10-30-45_123456/
    """
    # determine base directory (via_standard or others)
    test_file_path = pathlib.Path(request.node.fspath)

    # find which base directory this test is under
    base_dir: str = "unknown"
    for parent in test_file_path.parents:
        if parent.name in E2E_BRANCHES:
            base_dir = parent.name
            break

    # get test name without parameters (e.g., "test_table_simple_uniform_grid")
    test_name: str = request.node.originalname

    # extract parametrize IDs from the full node name
    format_id: str = "default"
    test_case_id: str = "default"

    if hasattr(request.node, "callspec") and request.node.callspec.id:
        # get the full ID string (e.g., "image-bleed" or "image-0" or just "bleed")
        full_id: str = request.node.callspec.id

        # try to split into format and test_case_id
        parts = full_id.split("-", 1)

        if len(parts) == 2:
            # we have both format and test_case (e.g., "image-bleed")
            format_id = parts[0]
            test_case_id = parts[1]
        elif len(parts) == 1:
            # only one parameter - could be either format or test_case
            # check if it's a known format
            if parts[0] in E2E_FORMATS:
                format_id = parts[0]
            else:
                test_case_id = parts[0]

    # sanitize IDs to be filesystem-safe
    format_id = format_id.replace(" ", "_").replace("/", "_")
    test_case_id = test_case_id.replace(" ", "_").replace("/", "_")

    # create timestamp for uniqueness
    timestamp: str = datetime.now(tz=UTC).strftime("%Y-%m-%d_%H-%M-%S_%f")

    # build the full path
    test_dir: pathlib.Path = E2E_TESTS_OUTPUT_DIR / base_dir / test_name / format_id / test_case_id / timestamp

    test_dir.mkdir(parents=True, exist_ok=True)
    return test_dir
