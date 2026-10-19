"""Layout catalogue: required fields and the logical relation each layout encodes.

Single source of truth for build_deck.py and lint_storyboard.py.
"""

# layout -> (required fields, logical relation it shows)
LAYOUTS = {
    "cover": (["title"], "Title page"),
    "executive_summary": (["items"], "The whole argument, one bold takeaway per line, written last"),
    "columns": (["blocks"], "Parallel arguments (2 to 4 pillars)"),
    "rows": (["blocks"], "Stacked arguments, each with longer detail on the right"),
    "bullets": (["points"], "Plain enumeration with no other relation"),
    "progression": (["blocks"], "Maturity build-up or roadmap, left to right"),
    "chevrons": (["steps"], "Sequential process"),
    "matrix": (["x_axis", "y_axis", "quadrants"], "Positioning on two criteria"),
    "table": (["columns", "rows"], "Options compared on several criteria"),
    "chart_text": (["chart", "blocks"], "A data point and what it means"),
    "big_number": (["number", "label"], "One figure carries the message"),
    "waterfall": (["steps"], "Gap between two values, broken into contributions"),
    "funnel": (["stages"], "Volume lost from stage to stage"),
    "before_after": (["before", "after"], "Current state versus target state"),
    "timeline": (["phases"], "Implementation phases"),
    "gantt": (["periods", "tasks"], "Workstreams scheduled over time"),
    "tree": (["root", "branches"], "Breakdown of a question or a whole (issue tree)"),
    "quotes": (["quotes", "blocks"], "Interview or survey evidence and its reading"),
    "recommendation": (["recommendation", "pillars"], "A recommendation and its conditions or reasons"),
    "market_map": (["items"], "Market shares as areas, one colour per group (treemap)"),
    "band_matrix": (["column_bands", "rows"], "Units x attributes grid with banded categories (benchmark)"),
    "fact_sheet": (["facts"], "Reference card for one unit of a benchmark: key facts and their reading"),
}

# Fields whose items carry a "title" that must state an idea (logical writing).
# Step, phase, quadrant, stage and table header titles stay labels.
IDEA_TITLE_FIELDS = {
    "columns": ["blocks"],
    "rows": ["blocks"],
    "progression": ["blocks"],
    "chart_text": ["blocks"],
    "big_number": ["blocks"],
    "waterfall": ["blocks"],
    "funnel": ["blocks"],
    "quotes": ["blocks"],
    "before_after": ["before", "after"],
    "recommendation": ["pillars"],
    "fact_sheet": ["blocks"],
    "market_map": ["blocks"],
}

HARVEY = {"[0]": 0, "[1]": 1, "[2]": 2, "[3]": 3, "[4]": 4}
