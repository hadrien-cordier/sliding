# Storyboard format (`04-storyboard.json`)

Full examples: `examples/demo-layouts/` (argument) and `examples/demo-benchmark/` (benchmark) in the repo. File name in a working folder: `04-storyboard.json`.

```json
{
  "meta": {"title": "Deck name", "accent": "1F4E79", "font": "Arial", "mode": "argument | benchmark"},
  "slides": [ { "layout": "...", "title": "...", "source": "...", "notes": "...", "...": "layout fields" } ]
}
```

Slide order: `cover`, then `executive_summary` (written last), then the body slides.

## Fields shared by all slides
| Field | Required | Role |
|---|---|---|
| `layout` | yes | A layout from the table below |
| `title` | yes | The title approved in the ghost deck, word for word |
| `source` | when the slide holds a figure | Footer, prefixed "Source:". Name the origin and year |
| `notes` | no | Speaker notes: what the presenter adds, open points |
| `layout_rationale` | yes on body slides (benchmark: first slide of each series) | `{"relation": "...", "alternative": "second candidate layout", "why": "why this layout wins"}`. Not rendered |

No `subtitle` field exists: the linter rejects it.

A **block** is `{"title": "idea of the block", "points": ["detail", "detail"], "accent": false}`.

## Fields by layout
| `layout` | Fields | Notes |
|---|---|---|
| `cover` | `title`, `context` | `context`: audience, date |
| `executive_summary` | `items`: `[{takeaway, points, accent}]` (3 to 6) | Bold takeaways read alone give the argument |
| `columns` | `blocks` (2 to 4), `summary` (optional) | `summary`: band under the columns; only if it adds information |
| `rows` | `blocks` (2 to 5), `title_width` (inches, default 3.6) | Block title left, points right |
| `bullets` | `points`, `block_title` (optional) | |
| `progression` | `blocks` (2 to 5), `axis_label`, `accent_last` (default true) | Growing boxes, left to right |
| `chevrons` | `steps`: `[{title, points}]` (2 to 7) | Step titles stay short (1 to 2 words) |
| `matrix` | `x_axis`, `y_axis`: `{label, low, high}`; `quadrants`: 4 blocks, order top-left, top-right, bottom-left, bottom-right; `side_blocks` (optional) | `accent: true` on the quadrant the title points to |
| `table` | `columns` (headers), `rows` (lists of cells), `accent_column` (index), `legend`, `first_column_width` | Cell `"[0]"` to `"[4]"`: Harvey ball, 0 to 4 quarters |
| `chart_text` | `chart`: `{title, type: bars \| hbars \| line \| stacked, categories, series: [{name, values}], unit, format, accent: [index]}`; `blocks` (1 to 3); `chart_share` (default 0.6) | `accent`: categories in colour, others grey |
| `big_number` | `number` (string, e.g. "€4.2bn"), `label`, `blocks` (optional) | |
| `waterfall` | `steps`: `[{label, value, total}]`; `chart_title`, `unit`, `format`, `blocks` (optional) | `total: true` on start and end bars; other values are signed changes |
| `funnel` | `stages`: `[{label, value}]`, `accent_stage` (index), `blocks` (optional) | |
| `before_after` | `before`, `after` (blocks), `transition` (optional) | |
| `timeline` | `phases`: `[{period, title, points}]` (2 to 6) | |
| `gantt` | `periods` (column labels), `tasks`: `[{label, start, end, accent, milestone}]`, `label_width` | `start` and `end` are period indexes from 0 |
| `tree` | `root` (text), `branches`: `[{text, leaves: []}]` (2 to 4) | |
| `quotes` | `quotes`: `[{text, author}]` (1 to 3), `blocks` | |
| `recommendation` | `recommendation` (text), `pillars` (blocks, 2 to 4) | |

| `market_map` | `items`: `[{label, value, group}]`, `unit`, `blocks` (optional), `map_share` (default 0.68) | Area proportional to value, one colour per group (6 groups at most); labels hide in boxes too small |
| `band_matrix` | `column_bands`: `[{label, columns: []}]`; `rows`: `[{label, group, accent, cells: []}]`; `band_header`, `row_header`, `legend`, `first_column_width` | Cells: text, "●"/"○", "n.d.", `"[0]"`..`"[4]"` Harvey balls, or `{"text": "12%", "calc": true}` printed in blue. Rows with a new `group` get a group header row. Up to about 18 rows |
| `fact_sheet` | `facts`: `[{label, value}]` (value may be `{"text", "calc"}`), `blocks` (optional) | One card per unit of a benchmark |

Cells or values marked `calc` are figures the team computed from sourced data; they print in blue with a legend line.

`format` follows Excel syntax (`"0"`, `"0.0"`); `unit` follows the number (`"%"`, `" bn€"`).
