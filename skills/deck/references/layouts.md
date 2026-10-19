# Slide design catalogue: the form follows the logical relation and the number of arguments in the title.

Pick the layout from the relation between the blocks of the slide, never from a wish to vary. Two consecutive slides may share a layout if their blocks share a relation. Practitioner sources for these designs: `consulting-practices.md`.

| Logical relation between the blocks | Layout | Avoid when |
|---|---|---|
| The whole argument, one takeaway per line (first content slide, written last) | `executive_summary` | Never used elsewhere |
| Parallel arguments that together prove the title (2 to 4) | `columns` | The blocks follow a time or maturity order |
| Stacked arguments, each with longer detail | `rows` | More than 5 rows |
| Maturity build-up, roadmap, graded scenarios | `progression` (growing boxes, arrow) | Steps carry equal weight: use `chevrons` |
| Sequential process, method steps | `chevrons` | More than 7 steps: group them |
| Positioning items on two criteria (impact vs effort...) | `matrix` (2x2) | One criterion dominates |
| Options compared on several criteria | `table` with Harvey balls `[0]` to `[4]`, `accent_column` on the recommended option | More than 8 rows or 5 options |
| A data point and what it means | `chart_text` (chart left, callouts right) | The data is not CONFIRMED |
| One figure carries the message | `big_number` | Several figures matter equally |
| A gap between two values, broken into contributions | `waterfall` | Contributions do not add up |
| Volume lost from stage to stage | `funnel` (`accent_stage` on the largest drop) | Stages are not nested |
| Current state versus target | `before_after` | More than two states: use `progression` |
| Phases with one deliverable each | `timeline` | Workstreams overlap: use `gantt` |
| Workstreams scheduled over periods, milestones | `gantt` | Fewer than three workstreams |
| Breakdown of a question or a whole | `tree` (issue tree) | More than 4 branches |
| Interview or survey evidence and its reading | `quotes` | The quotes are not traceable to a real person or survey |
| A recommendation and its conditions or reasons | `recommendation` | The body has not yet proven it |
| Plain list with no other relation | `bullets` | The points have an order or hierarchy another layout shows better |
| Market shares by actor, grouped (treemap) | `market_map` | Values are not parts of one total |
| Units × attributes grid with banded column categories (benchmark) | `band_matrix` (●/○, "n.d.", Harvey balls, computed values in blue) | Fewer than 4 units: use `table` |
| Reference card for one unit of a grid (one country, one bank, one vendor) | `fact_sheet` | The slide must compare units: use `band_matrix` |
| Title page | `cover` | |

## Choosing and varying layouts
- Name the logical relation first, then compare at least two candidate layouts for it, and record the choice in `layout_rationale` (relation, alternative, why).
- In argument decks, never use the same layout more than twice in a row; the linter blocks it. Benchmark decks (`meta.mode: "benchmark"`) repeat one exhibit per unit of the grid by design.
- Useful diversity follows a change of relation. Decorative variety (changing the look while the relation stays the same) is a defect: when the rule above forces a change, take the second-best layout for the same relation.

## Shared rules
- White background, grey boxes, one accent colour for the element the title points to.
- The key element sits top left or at the end of the reading path (last box of a progression, highlighted quadrant, accent bar): the eye starts top left.
- 2 to 4 blocks, 2 to 6 points per block, 25 words at most per point.
- One block per question the title raises; a block that answers none leaves the slide.
- A chart or block next to a chart adds information; it never restates what the chart shows.
