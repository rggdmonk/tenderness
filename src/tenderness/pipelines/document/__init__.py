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

from tenderness.pipelines.document.bbox_helper import (
    BlockBBox,
    BlockBBoxesResult,
    CellBBox,
    TableBlockBBoxesResult,
    TextBlockBBoxesResult,
)
from tenderness.pipelines.document.draw_block_bboxes import (
    BlockDrawConfig,
    ImageBlockBoundingBoxDrawer,
    SVGBlockBoundingBoxDrawer,
)
from tenderness.pipelines.document.image_block_helpers import ImageBlock, ImageBlockResult
from tenderness.pipelines.document.pipeline import DocumentRenderPipeline
from tenderness.pipelines.document.pipeline_schema import (
    BaseBlock,
    DocumentBlocksConfig,
    DocumentConfig,
    DocumentRenderResult,
    DocumentSetupResult,
)
from tenderness.pipelines.document.setup_helpers import BlockPosition
from tenderness.pipelines.document.table_block_helpers import (
    TableBlock,
    TableBlockHelpers,
    TableBlockResult,
    TextCell,
    TextCellResult,
)
from tenderness.pipelines.document.text_block_helpers import TextBlock, TextBlockHelpers, TextBlockResult, TextStyle

__all__ = [
    "BaseBlock",
    "BlockBBox",
    "BlockBBoxesResult",
    "BlockDrawConfig",
    "BlockPosition",
    "CellBBox",
    "DocumentBlocksConfig",
    "DocumentConfig",
    "DocumentRenderPipeline",
    "DocumentRenderResult",
    "DocumentSetupResult",
    "ImageBlock",
    "ImageBlockBoundingBoxDrawer",
    "ImageBlockResult",
    "SVGBlockBoundingBoxDrawer",
    "TableBlock",
    "TableBlockBBoxesResult",
    "TableBlockHelpers",
    "TableBlockResult",
    "TextBlock",
    "TextBlockBBoxesResult",
    "TextBlockHelpers",
    "TextBlockResult",
    "TextCell",
    "TextCellResult",
    "TextStyle",
]
