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

_E2E_TESTS_DIR = pathlib.Path(__file__).parent
_SURFACE_CONFIG_FIXTURE = "surface_config"


@pytest.fixture
def e2e_output_dir(request: FixtureRequest, tests_output_dir: pathlib.Path) -> pathlib.Path:
    """
    Creates output directory structure for tests:
    tests_output_dir/e2e/{base_dir}/{test_name}/{format}/{test_case_id}/{timestamp}/

    base_dir is derived automatically from the test file's location relative to tests/e2e/.
    format_id is derived from the surface_config fixture parametrize ID (first part of callspec.id).
    Example: tests/e2e/pipelines/document/test_latin_text.py[image-single_line] creates:
    .../e2e/pipelines/document/test_latin_text/image/single_line/2024-03-31_10-30-45_123456/
    """
    test_file_path = pathlib.Path(request.node.fspath)

    try:
        rel = test_file_path.relative_to(_E2E_TESTS_DIR)
        base_dir: pathlib.Path = rel.parent
    except ValueError:
        base_dir = pathlib.Path("unknown")

    test_name: str = request.node.originalname

    format_id: str = "default"
    test_case_id: str = "default"

    if hasattr(request.node, "callspec") and request.node.callspec.id:
        full_id: str = request.node.callspec.id
        has_surface_config = _SURFACE_CONFIG_FIXTURE in request.node.callspec.params
        parts = full_id.split("-", 1)

        if len(parts) == 2:
            format_id = parts[0]
            test_case_id = parts[1]
        elif len(parts) == 1:
            if has_surface_config:
                format_id = parts[0]
            else:
                test_case_id = parts[0]

    format_id = format_id.replace(" ", "_").replace("/", "_")
    test_case_id = test_case_id.replace(" ", "_").replace("/", "_")

    timestamp: str = datetime.now(tz=UTC).strftime("%Y-%m-%d_%H-%M-%S_%f")

    test_dir: pathlib.Path = tests_output_dir / "e2e" / base_dir / test_name / format_id / test_case_id / timestamp

    test_dir.mkdir(parents=True, exist_ok=True)
    return test_dir
