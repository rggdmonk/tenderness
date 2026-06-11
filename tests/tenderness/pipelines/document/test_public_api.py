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

# ruff: noqa: PLC0415
from __future__ import annotations

_EXPECTED_EXPORTS: frozenset[str] = frozenset(
    {
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
        "TableBlockResult",
        "TextBlock",
        "TextBlockBBoxesResult",
        "TextBlockResult",
        "TextCell",
        "TextCellResult",
        "TextStyle",
        "TextBlockHelpers",
        "TableBlockHelpers",
    }
)


class TestDocumentRenderPipelinePublicAPI:
    def test_exports_match_snapshot(self) -> None:
        import tenderness.pipelines.document as pkg

        actual = frozenset(pkg.__all__)
        assert actual == _EXPECTED_EXPORTS, (
            f"Public API changed. Added: {actual - _EXPECTED_EXPORTS}, Removed: {_EXPECTED_EXPORTS - actual}"
        )

    def test_all_exports_are_importable(self) -> None:
        import tenderness.pipelines.document as pkg

        for name in pkg.__all__:
            assert hasattr(pkg, name), f"{name!r} is in __all__ but not importable"
