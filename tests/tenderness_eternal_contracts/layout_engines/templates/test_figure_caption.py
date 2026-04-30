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

from tenderness.layout_engines.minimal_flexbox.templates.figure_caption import MinimalFlexBoxTemplateFigureCaption
from tests._test_utils.class_test import ClassTestBase, ClassTestConfig

# --------------------------
# Eternal contract tests for MinimalFlexBoxTemplateFigureCaption
# --------------------------
MINIMAL_FLEXBOX_TEMPLATE_FIGURE_CAPTION_EXPECTED_METHODS = {"stack_figure_caption"}
MINIMAL_FLEXBOX_TEMPLATE_FIGURE_CAPTION_TEST_CLASS_CONFIG = [
    ClassTestConfig(
        cls=MinimalFlexBoxTemplateFigureCaption,
        expected_methods=MINIMAL_FLEXBOX_TEMPLATE_FIGURE_CAPTION_EXPECTED_METHODS,
    )
]


@pytest.mark.parametrize(
    "config", MINIMAL_FLEXBOX_TEMPLATE_FIGURE_CAPTION_TEST_CLASS_CONFIG, ids=lambda c: c.cls.__name__
)
class TestMinimalFlexBoxTemplateFigureCaptionEternalContract(ClassTestBase):
    pass
