---
icon: lucide/vector-square
hide:
  - path
---
# Text Bounding Boxes

## Overview

| Level | What it covers | Logical | Ink |
|---|---|:---:|:---:|
| `CHAR` | One Unicode code point | :lucide-check: | :lucide-x: |
| `CLUSTER` | Grapheme cluster - one or more code points treated as an indivisible unit of text | :lucide-check: | :lucide-check: |
| `RUN` | Contiguous span with uniform shaping properties (script, direction, font, etc.) | :lucide-check: | :lucide-check: |
| `LINE` | Full layout line | :lucide-check: | :lucide-check: |
| `LAYOUT` | Entire layout | :lucide-check: | :lucide-check: |

!!! info "Terminology"

    **Extent** (also called bounding box) — the rectangle describing the bounds of a piece of text.

    **Code point** — a numeric value in the Unicode codespace (U+0000 to U+10FFFF).

    **Grapheme** — a unit of a writing system, defined by the Unicode Standard ([UAX #29](https://www.unicode.org/reports/tr29/)). `e` + `◌́` = one grapheme cluster (two code points, one unit). This is a text concept.

    **Glyph** — a rendered shape in a font. A single grapheme cluster may map to one glyph or multiple glyphs (ligatures, stacked diacritics, etc.). This is a font/rendering concept.



### Logical vs ink

- **Logical** extent is the rectangle defined by the glyph's advance width and the line's ascent/descent — the space it occupies in the layout, not the space it paints.
- **Ink** extent is the tight bounding box of what is actually painted.

### Char

One logical extent per Unicode code point. No ink extent - a code point may be a combining mark with no ink of its own. 

Example: `café` has 5 code points (`c`-`a`-`f`-`e`-`́`).


<iframe
  src="../../components/bbox_visualizer.html?image=https://raw.githubusercontent.com/paperchase-labs/tenderness-examples/main/_docs_output/_generate_text_bboxes_examples/cafe_example/output.png&char=https://raw.githubusercontent.com/paperchase-labs/tenderness-examples/main/_docs_output/_generate_text_bboxes_examples/cafe_example/bboxes_char.json&cluster=https://raw.githubusercontent.com/paperchase-labs/tenderness-examples/main/_docs_output/_generate_text_bboxes_examples/cafe_example/bboxes_cluster.json&run=https://raw.githubusercontent.com/paperchase-labs/tenderness-examples/main/_docs_output/_generate_text_bboxes_examples/cafe_example/bboxes_run.json&line=https://raw.githubusercontent.com/paperchase-labs/tenderness-examples/main/_docs_output/_generate_text_bboxes_examples/cafe_example/bboxes_line.json&layout=https://raw.githubusercontent.com/paperchase-labs/tenderness-examples/main/_docs_output/_generate_text_bboxes_examples/cafe_example/bboxes_layout.json&on=char"
  style="width:100%;height:200px;border:none;display:block;"
></iframe>



### Cluster

Both logical and ink extents are available per grapheme cluster. `CLUSTER` boundaries are determined by grapheme rules, not by how many glyphs the shaper produces. 

Example: `café` has 4 clusters (`c`-`a`-`f`-`é`).


<iframe
  src="../../components/bbox_visualizer.html?image=https://raw.githubusercontent.com/paperchase-labs/tenderness-examples/main/_docs_output/_generate_text_bboxes_examples/cafe_example/output.png&char=https://raw.githubusercontent.com/paperchase-labs/tenderness-examples/main/_docs_output/_generate_text_bboxes_examples/cafe_example/bboxes_char.json&cluster=https://raw.githubusercontent.com/paperchase-labs/tenderness-examples/main/_docs_output/_generate_text_bboxes_examples/cafe_example/bboxes_cluster.json&run=https://raw.githubusercontent.com/paperchase-labs/tenderness-examples/main/_docs_output/_generate_text_bboxes_examples/cafe_example/bboxes_run.json&line=https://raw.githubusercontent.com/paperchase-labs/tenderness-examples/main/_docs_output/_generate_text_bboxes_examples/cafe_example/bboxes_line.json&layout=https://raw.githubusercontent.com/paperchase-labs/tenderness-examples/main/_docs_output/_generate_text_bboxes_examples/cafe_example/bboxes_layout.json&on=cluster"
  style="width:100%;height:200px;border:none;display:block;"
></iframe>


### Run


Both logical and ink extents are available per run, along with a baseline. A run is a contiguous span with uniform shaping properties (script, direction, font, etc.).

Example: ` Hello 你好 ` produces 2 runs - ` Hello ` (Latin) and `你好 ` (CJK) - split at the script boundary.


<iframe
  src="../../components/bbox_visualizer.html?image=https://raw.githubusercontent.com/paperchase-labs/tenderness-examples/main/_docs_output/_generate_text_bboxes_examples/latin_chinese_example/output.png&char=https://raw.githubusercontent.com/paperchase-labs/tenderness-examples/main/_docs_output/_generate_text_bboxes_examples/latin_chinese_example/bboxes_char.json&cluster=https://raw.githubusercontent.com/paperchase-labs/tenderness-examples/main/_docs_output/_generate_text_bboxes_examples/latin_chinese_example/bboxes_cluster.json&run=https://raw.githubusercontent.com/paperchase-labs/tenderness-examples/main/_docs_output/_generate_text_bboxes_examples/latin_chinese_example/bboxes_run.json&line=https://raw.githubusercontent.com/paperchase-labs/tenderness-examples/main/_docs_output/_generate_text_bboxes_examples/latin_chinese_example/bboxes_line.json&layout=https://raw.githubusercontent.com/paperchase-labs/tenderness-examples/main/_docs_output/_generate_text_bboxes_examples/latin_chinese_example/bboxes_layout.json&on=run"
  style="width:100%;height:200px;border:none;display:block;"
></iframe>


### Line

Both logical and ink extents are available per line, along with a baseline. Lines stack vertically with no gap — the bottom of one logical extent is the top of the next.

Example: `"This is the 1st line.\nThis is the 2nd line."` produces 2 lines.

<iframe
  src="../../components/bbox_visualizer.html?image=https://raw.githubusercontent.com/paperchase-labs/tenderness-examples/main/_docs_output/_generate_text_bboxes_examples/multiline_example/output.png&char=https://raw.githubusercontent.com/paperchase-labs/tenderness-examples/main/_docs_output/_generate_text_bboxes_examples/multiline_example/bboxes_char.json&cluster=https://raw.githubusercontent.com/paperchase-labs/tenderness-examples/main/_docs_output/_generate_text_bboxes_examples/multiline_example/bboxes_cluster.json&run=https://raw.githubusercontent.com/paperchase-labs/tenderness-examples/main/_docs_output/_generate_text_bboxes_examples/multiline_example/bboxes_run.json&line=https://raw.githubusercontent.com/paperchase-labs/tenderness-examples/main/_docs_output/_generate_text_bboxes_examples/multiline_example/bboxes_line.json&layout=https://raw.githubusercontent.com/paperchase-labs/tenderness-examples/main/_docs_output/_generate_text_bboxes_examples/multiline_example/bboxes_layout.json&on=line"
  style="width:100%;height:250px;border:none;display:block;"
></iframe>


### Layout

Both logical and ink extents are available for the entire layout as a single rectangle.

Example: `"Some XZY?!\nАБВ for sure"` produces one layout extent spanning both lines.

<iframe
  src="../../components/bbox_visualizer.html?image=https://raw.githubusercontent.com/paperchase-labs/tenderness-examples/main/_docs_output/_generate_text_bboxes_examples/long_text_example/output.png&char=https://raw.githubusercontent.com/paperchase-labs/tenderness-examples/main/_docs_output/_generate_text_bboxes_examples/long_text_example/bboxes_char.json&cluster=https://raw.githubusercontent.com/paperchase-labs/tenderness-examples/main/_docs_output/_generate_text_bboxes_examples/long_text_example/bboxes_cluster.json&run=https://raw.githubusercontent.com/paperchase-labs/tenderness-examples/main/_docs_output/_generate_text_bboxes_examples/long_text_example/bboxes_run.json&line=https://raw.githubusercontent.com/paperchase-labs/tenderness-examples/main/_docs_output/_generate_text_bboxes_examples/long_text_example/bboxes_line.json&layout=https://raw.githubusercontent.com/paperchase-labs/tenderness-examples/main/_docs_output/_generate_text_bboxes_examples/long_text_example/bboxes_layout.json&on=layout"
  style="width:100%;height:250px;border:none;display:block;"
></iframe>



### Whitespace and line breaks

- Whitespace characters are included at all levels with a valid logical extent — they occupy layout space but paint nothing. Their **ink extent** collapses to a zero-area point while their **logical extent** retains full dimensions.

```json title="Example: whitespace ink extent vs logical extent"
    "text": " ",
    "logical_bbox": {
      "top_left":     [10.0, 14.0],
      "top_right":    [20.0, 14.0],
      "bottom_right": [20.0, 69.0],
      "bottom_left":  [10.0, 69.0]
    },
    "ink_bbox": {
      "top_left":     [10.0, 57.0],
      "top_right":    [10.0, 57.0],
      "bottom_right": [10.0, 57.0],
      "bottom_left":  [10.0, 57.0]
    }
```

- Line breaks behave differently per level:
    - **`CHAR`** — included. Each line break is included with a zero-width, full-height logical bounding box at the end of its line. `\r\n` produces two separate entries (one for `\r`, one for `\n`) each with a correct `byte_index` and `byte_length`.
    - **`CLUSTER` / `RUN`** — line breaks are excluded — the `byte_index` of the next cluster or run jumps past them (`+1` for `\n`/`\r`, `+2` for `\r\n`, `+3` for `U+2029`). `U+2028` (LINE SEPARATOR) is an exception: it is included as a whitespace character with a zero-width logical extent.
    - **`LINE`** — line breaks are excluded from each line's `text` and `byte_length`; the next line's `byte_index` jumps past them (`+1`, `+1`, `+2`, `+3` respectively). `U+2028` is an exception: it is included as whitespace in the preceding line's `text` and `byte_length`.
    - **`LAYOUT`** — included. `text` is the full original string unchanged.


### Reconstruction

| Level | Reconstructable | Sort needed | Line breaks |
|---|---|:---:|:---:|
| `CHAR` | Full text | sort by `byte_index` | included |
| `CLUSTER` | Full text excluding line breaks | sort by `byte_index` | excluded[^1] |
| `RUN` | Full text excluding line breaks | sort by `byte_index` | excluded[^1] |
| `LINE` | Full text excluding line breaks | no | excluded[^1] |
| `LAYOUT` | Full text | no | included |

[^1]: `U+2028 (LINE SEPARATOR)` is treated as whitespace and is included, not excluded.

Sorting by `byte_index` is required at `CHAR`, `CLUSTER`, and `RUN` levels because RTL text is returned in visual order, making `byte_index` values non-monotonic. `LINE` and `LAYOUT` are always in logical order.


## Data model

### Quadrilateral

Every bounding box is stored as a `Quadrilateral` — an oriented bounding box (OBB) defined by four corners in user-space coordinates:

```python
@dataclass
class Quadrilateral:
    top_left:     tuple[float, float]
    top_right:    tuple[float, float]
    bottom_right: tuple[float, float]
    bottom_left:  tuple[float, float]
```

Coordinates are in the user-space of the surface used during rendering. For axis-aligned text — the common case — this is a rectangle. The quadrilateral form correctly represents rotated or skewed layouts.

### Fields per level

The following fields can be present at each level:

| Field | `CHAR` | `CLUSTER` | `RUN` | `LINE` | `LAYOUT` |
|---|:---:|:---:|:---:|:---:|:---:|
| `logical_bbox` | ✓ | ✓ | ✓ | ✓ | ✓ |
| `ink_bbox` | — | ✓ | ✓ | ✓ | ✓ |
| `text` | ✓ | ✓ | ✓ | ✓ | ✓ |
| `byte_index` | ✓ | ✓ | ✓ | ✓ | — |
| `byte_length` | ✓ | ✓ | ✓ | ✓ | — |
| `baseline` | — | — | ✓ | ✓ | — |
| `resolved_direction` | — | — | — | ✓ | — |
| `is_paragraph_start` | — | — | — | ✓ | — |
