---
icon: lucide/file-text
hide:
  - path
---

# Document Pipeline


## Overview

The document pipeline renders a structured document in two phases: **setup** then **render**. Setup produces the complete geometry — surface dimensions, content area, and every block's exact position — before any content is drawn. Render takes that geometry and draws each block into its pre-computed position in order.

## Features

- Three block types: `TextBlock`, `ImageBlock`, `TableBlock`
- Flex layout engine for block positioning
- Text overflow continuation across blocks
- Base style shared across all blocks, overridable per block
- Multi-format output: PNG, SVG, PDF, NumPy array
- Text bounding boxes per block at any granularity level
- Block bounding boxes (AABB) — surface, content area, and each block; available from setup, before rendering


## Code and Output

| Example | Code | Output |
|---|---|---|
| `figure_caption` | [code](https://github.com/paperchase-labs/tenderness-examples/tree/main/examples/document_pipeline/figure_caption) | [output](https://github.com/paperchase-labs/tenderness-examples/tree/main/examples_output/document_pipeline/figure_caption) |
| `multilingual` | [code](https://github.com/paperchase-labs/tenderness-examples/tree/main/examples/document_pipeline/multilingual) | [output](https://github.com/paperchase-labs/tenderness-examples/tree/main/examples_output/document_pipeline/multilingual) |
| `simple_table` | [code](https://github.com/paperchase-labs/tenderness-examples/tree/main/examples/document_pipeline/simple_table) | [output](https://github.com/paperchase-labs/tenderness-examples/tree/main/examples_output/document_pipeline/simple_table) |
| `song_lyrics` | [code](https://github.com/paperchase-labs/tenderness-examples/tree/main/examples/document_pipeline/song_lyrics) | [output](https://github.com/paperchase-labs/tenderness-examples/tree/main/examples_output/document_pipeline/song_lyrics) |
| `text_bboxes` | [code](https://github.com/paperchase-labs/tenderness-examples/tree/main/examples/document_pipeline/text_bboxes) | [output](https://github.com/paperchase-labs/tenderness-examples/tree/main/examples_output/document_pipeline/text_bboxes) |
| `two_columns_page` | [code](https://github.com/paperchase-labs/tenderness-examples/tree/main/examples/document_pipeline/two_columns_page) | [output](https://github.com/paperchase-labs/tenderness-examples/tree/main/examples_output/document_pipeline/two_columns_page) |
| `reaction_meme` | [code](https://github.com/paperchase-labs/tenderness-examples/tree/main/examples/document_pipeline/reaction_meme) | [output](https://github.com/paperchase-labs/tenderness-examples/tree/main/examples_output/document_pipeline/reaction_meme) |