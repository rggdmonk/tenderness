
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/logo/tenderness-lockup-horizontal-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="docs/assets/logo/tenderness-lockup-horizontal-light.svg">
  <img alt="Fallback image description" src="docs/assets/logo/tenderness-lockup-horizontal-dark.svg">
</picture>

<p align="center">
  <a href="https://github.com/paperchase-labs/tenderness"><img src="https://img.shields.io/badge/source-GitHub-181717?logo=github&logoColor=white&style=flat" alt="Source Code"/></a>
  <a href="https://github.com/paperchase-labs/tenderness-examples"><img src="https://img.shields.io/badge/examples-GitHub-181717?logo=github&logoColor=white&style=flat" alt="Examples"/></a>
  <a href="https://paperchase-labs.github.io/tenderness/"><img src="https://img.shields.io/badge/docs-online-75528b?logo=github&logoColor=white&style=flat" alt="Documentation"/></a>
  <a href="https://pypi.org/project/tenderness"><img src="https://img.shields.io/pypi/v/tenderness?logo=python&logoColor=white&label=PyPI" alt="Python Package Index"/></a>
  <a href="https://pypi.org/project/tenderness"><img src="https://img.shields.io/pypi/pyversions/tenderness?logo=python&logoColor=white&style=flat" alt="Python versions"/></a>
</p>
<p align="center">
  <a href="https://github.com/astral-sh/ruff"><img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json" alt="Ruff"/></a>
  <a href="https://github.com/pre-commit/pre-commit"><img src="https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white&style=flat" alt="pre-commit"/></a>
  <a href="https://numpydoc.readthedocs.io/en/latest/format.html"><img src="https://img.shields.io/badge/docstrings-NumPy-4DABCF?logo=numpy&logoColor=white&style=flat" alt="NumPy docstrings"/></a>
  <a href="https://github.com/jsh9/pydoclint"><img src="https://img.shields.io/badge/pydoclint-checked-4DABCF?logo=python&logoColor=white&style=flat" alt="pydoclint"/></a>
  <a href="https://mypy-lang.org/"><img src="https://img.shields.io/badge/type--checked-mypy-blue?logo=python&logoColor=white&style=flat" alt="mypy"/></a>
  <a href="https://github.com/paperchase-labs/tenderness/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-Apache--2.0-4caf50?logo=apache&logoColor=white&style=flat" alt="License: Apache-2.0"/></a>
</p>

**tenderness** is a fast library for *synthetic*, deterministic document rendering from text and images, powered by [Cairo](https://www.cairographics.org/) and [Pango](https://docs.gtk.org/Pango/index.html).


## Why tenderness?

Most document datasets don’t come from real structure — they come from reconstruction. Text is rendered, then reverse-engineered back into layout using OCR, heuristics, or fragile parsing pipelines. The result is noisy, incomplete, and not reproducible.

**tenderness** flips this entirely.

It renders text directly into documents producing images, SVGs, and PDFs with fully known layout from the start. Every character placement, line break, and block position is defined at render time — not inferred afterward.


## What this gives you

- Generate large-scale synthetic document datasets
- Provide precise structural supervision for vision-language models
- Build benchmarks for layout understanding systems
- Ground-truth layout across characters, clusters, runs, and lines

**No OCR. No heuristics. No reconstruction. No manual annotation.**

Just text in → fully structured document out.


## Main Features

 - **Multi-format output**: Render text and images into Image, SVG, PDF, or NumPy arrays.

 - **Composable content blocks**: Build documents from simple primitives: `TextBlock`, `ImageBlock`, and `TableBlock`.

 - **Minimal flexbox layout engine**: A lightweight system that automatically resolves positioning and flow.

 - **Exact bounding boxes (OBB + AABB, logical + ink)**: Extract multi-level data for text (character, cluster, run, line, layout) and blocks.

 - **Rich typography & text flow**: Custom fonts, hierarchical styling, Pango markup, automatic font fallback, and overflow-aware text continuation across blocks.

 - **Composable pipelines**: Use the built-in pipeline with pre-defined layouts, or build your own from scratch.