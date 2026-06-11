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

from tenderness.pipelines.renderer_configurator import RendererConfigurator
from tests._test_utils.class_test import ClassTestBase, ClassTestConfig

# --------------------------
# Tests RendererConfigurator
# --------------------------
RENDER_CONFIGURATOR_EXPECTED_METHODS = {
    "create_surface",
    "create_cairo_context",
    "create_layout_interface_from_cairo_context",
    "create_layout_interface_from_existing",
    "create_font_description_interface",
    "create_font_description_interface_from_existing",
    "create_font_description_interface_from_string",
    "create_layout_context_interface_from_layout_interface",
    "create_layout_context_interface_from_existing",
    "create_layout_context_interface_from_pango_layout",
    "create_font_options_interface",
    "create_transform_pipeline_from_cairo_context",
    "create_transform_pipeline_from_existing",
    "show_layout",
}
RENDER_CONFIGURATOR_TEST_CLASS_CONFIG = [
    ClassTestConfig(
        cls=RendererConfigurator,
        expected_methods=RENDER_CONFIGURATOR_EXPECTED_METHODS,
    ),
]


@pytest.mark.parametrize("config", RENDER_CONFIGURATOR_TEST_CLASS_CONFIG, ids=lambda c: c.cls.__name__)
class TestRendererConfiguratorContract(ClassTestBase):
    pass
