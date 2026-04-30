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

from tenderness.layout_engines.minimal_flexbox.templates.base import CaptionSpec, MinimalFlexBoxTemplateBase
from tests._test_utils.class_test import ClassTestBase, ClassTestConfig
from tests._test_utils.dataclass_test import DataclassTestBase, DataclassTestConfig

# --------------------------
# Eternal contract tests for CaptionSpec
# --------------------------
CAPTION_SPEC_EXPECTED_FIELDS = {"height", "gap", "on_top", "name"}
CAPTION_SPEC_TEST_DATACLASS_CONFIG = [
    DataclassTestConfig(
        dataclass_class=CaptionSpec,
        has_slots=True,
        expected_fields=CAPTION_SPEC_EXPECTED_FIELDS,
    )
]


@pytest.mark.parametrize("config", CAPTION_SPEC_TEST_DATACLASS_CONFIG, ids=lambda c: c.dataclass_class.__name__)
class TestCaptionSpecEternalContract(DataclassTestBase):
    pass


# --------------------------
# Eternal contract tests for MinimalFlexBoxTemplateBase
# --------------------------
MINIMAL_FLEXBOX_TEMPLATE_BASE_EXPECTED_METHODS = {"_add_name", "_wrap_with_caption"}
MINIMAL_FLEXBOX_TEMPLATE_BASE_TEST_CLASS_CONFIG = [
    ClassTestConfig(
        cls=MinimalFlexBoxTemplateBase,
        expected_methods=MINIMAL_FLEXBOX_TEMPLATE_BASE_EXPECTED_METHODS,
    )
]


@pytest.mark.parametrize("config", MINIMAL_FLEXBOX_TEMPLATE_BASE_TEST_CLASS_CONFIG, ids=lambda c: c.cls.__name__)
class TestMinimalFlexBoxTemplateBaseEternalContract(ClassTestBase):
    pass
