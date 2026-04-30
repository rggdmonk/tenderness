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

import pytest

from tenderness.font_files.manifest import (
    FontManifestEntry,
    FontManifestFile,
    FontManifestManager,
    FontManifestStore,
    FontManifestVerifier,
    ManifestVerificationReport,
)
from tests._test_utils.class_test import ClassTestBase, ClassTestConfig
from tests._test_utils.dataclass_test import DataclassTestBase, DataclassTestConfig

# --------------------------
# Tests for FontManifestEntry
# --------------------------
FONT_MANIFEST_ENTRY_EXPECTED_FIELDS = {"file_name", "url", "sha256"}
FONT_MANIFEST_ENTRY_EXPECTED_METHODS = {"to_dict", "to_download_source"}
FONT_MANIFEST_ENTRY_EXPECTED_CLASS_METHODS = {"from_dict"}

FONT_MANIFEST_ENTRY_TEST_DATACLASS_CONFIG = [
    DataclassTestConfig(
        dataclass_class=FontManifestEntry,
        has_slots=True,
        expected_fields=FONT_MANIFEST_ENTRY_EXPECTED_FIELDS,
        expected_methods=FONT_MANIFEST_ENTRY_EXPECTED_METHODS,
        expected_class_methods=FONT_MANIFEST_ENTRY_EXPECTED_CLASS_METHODS,
    )
]


@pytest.mark.parametrize("config", FONT_MANIFEST_ENTRY_TEST_DATACLASS_CONFIG, ids=lambda c: c.dataclass_class.__name__)
class TestFontManifestEntryContract(DataclassTestBase):
    pass


# --------------------------
# Tests for FontManifestFile
# --------------------------
FONT_MANIFEST_FILE_EXPECTED_METHODS = {"save_manifest", "load_manifest"}
FONT_MANIFEST_FILE_EXPECTED_PROPERTIES = {"manifest_name"}

FONT_MANIFEST_FILE_TEST_CLASS_CONFIG = [
    ClassTestConfig(
        cls=FontManifestFile,
        expected_properties=FONT_MANIFEST_FILE_EXPECTED_PROPERTIES,
        expected_methods=FONT_MANIFEST_FILE_EXPECTED_METHODS,
    )
]


@pytest.mark.parametrize("config", FONT_MANIFEST_FILE_TEST_CLASS_CONFIG, ids=lambda c: c.cls.__name__)
class TestFontManifestFileContract(ClassTestBase):
    pass


# --------------------------
# Tests for FontManifestStore
# --------------------------
FONT_MANIFEST_STORE_EXPECTED_METHODS = {
    "get_manifest_file",
    "get_fonts_dir_for",
    "list_manifests",
    "clear",
    "_clear_specific_manifest",
    "_clear_all_cache",
}
FONT_MANIFEST_STORE_TEST_CLASS_CONFIG = [
    ClassTestConfig(
        cls=FontManifestStore,
        expected_methods=FONT_MANIFEST_STORE_EXPECTED_METHODS,
    )
]


@pytest.mark.parametrize("config", FONT_MANIFEST_STORE_TEST_CLASS_CONFIG, ids=lambda c: c.cls.__name__)
class TestFontManifestStoreContract(ClassTestBase):
    pass


# --------------------------
# Tests for ManifestVerificationReport
# --------------------------
MANIFEST_VERIFICATION_REPORT_EXPECTED_FIELDS = {"manifest_name", "valid", "missing", "corrupt"}
MANIFEST_VERIFICATION_REPORT_EXPECTED_PROPERTIES = {"is_healthy"}

MANIFEST_VERIFICATION_REPORT_TEST_DATACLASS_CONFIG = [
    DataclassTestConfig(
        dataclass_class=ManifestVerificationReport,
        has_slots=True,
        expected_fields=MANIFEST_VERIFICATION_REPORT_EXPECTED_FIELDS,
        expected_properties=MANIFEST_VERIFICATION_REPORT_EXPECTED_PROPERTIES,
    )
]


@pytest.mark.parametrize(
    "config", MANIFEST_VERIFICATION_REPORT_TEST_DATACLASS_CONFIG, ids=lambda c: c.dataclass_class.__name__
)
class TestManifestVerificationReportContract(DataclassTestBase):
    pass


# --------------------------
# Tests for FontManifestVerifier
# --------------------------
FONT_MANIFEST_VERIFIER_EXPECTED_METHODS = {"is_ready", "verify"}
FONT_MANIFEST_VERIFIER_TEST_CLASS_CONFIG = [
    ClassTestConfig(
        cls=FontManifestVerifier,
        expected_methods=FONT_MANIFEST_VERIFIER_EXPECTED_METHODS,
    )
]


@pytest.mark.parametrize("config", FONT_MANIFEST_VERIFIER_TEST_CLASS_CONFIG, ids=lambda c: c.cls.__name__)
class TestFontManifestVerifierContract(ClassTestBase):
    pass


# --------------------------
# Tests for FontManifestManager
# --------------------------
FONT_MANIFEST_MANAGER_EXPECTED_METHODS = {
    "prepare_font_files",
    "create_manifest_file",
    "get_fonts_dir",
    "list_available_manifests",
    "clear",
    "_entries_needing_download",
    "_raise_if_failed",
    "is_manifest_ready",
    "verify_manifest",
}
FONT_MANIFEST_MANAGER_TEST_CLASS_CONFIG = [
    ClassTestConfig(
        cls=FontManifestManager,
        expected_methods=FONT_MANIFEST_MANAGER_EXPECTED_METHODS,
    )
]


@pytest.mark.parametrize("config", FONT_MANIFEST_MANAGER_TEST_CLASS_CONFIG, ids=lambda c: c.cls.__name__)
class TestFontManifestManagerContract(ClassTestBase):
    pass
