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

"""Pre-built MinimalFlexBox layout template collections."""

from __future__ import annotations

from tenderness.layout_engines.minimal_flexbox.templates.documents import MinimalFlexBoxTemplateDocuments
from tenderness.layout_engines.minimal_flexbox.templates.figure_caption import (
    MinimalFlexBoxTemplateFigureCaption,
)
from tenderness.layout_engines.minimal_flexbox.templates.flow import MinimalFlexBoxTemplateFlow
from tenderness.layout_engines.minimal_flexbox.templates.tables import MinimalFlexBoxTemplateTables


class MinimalFlexBoxTemplates:
    """Pre-built layout templates grouped by document region."""

    flow_templates = MinimalFlexBoxTemplateFlow()
    figure_caption_templates = MinimalFlexBoxTemplateFigureCaption()
    table_templates = MinimalFlexBoxTemplateTables()
    documents_templates = MinimalFlexBoxTemplateDocuments()
