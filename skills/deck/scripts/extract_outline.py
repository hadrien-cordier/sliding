#!/usr/bin/env python3
"""Print a compact text outline of a storyboard: titles, block titles, points, sources.

Reviewers and the summary writer read this outline instead of the full JSON, which carries
layout parameters they do not need. Typically 40 to 60% fewer tokens.

Usage: python3 extract_outline.py 04-storyboard.json [--titles-only] > outline.md
"""
import json
import sys
from pathlib import Path

SKIP = {"layout_rationale", "accent", "format", "unit", "type", "start", "end", "chart_share",
        "map_share", "title_width", "label_width", "first_column_width", "accent_last",
        "accent_column", "accent_stage", "milestone", "font"}


def flat(obj, depth=0):
    pad = "  " * depth
    if isinstance(obj, str):
        yield f"{pad}- {obj}"
    elif isinstance(obj, dict):
        if "text" in obj and set(obj) <= {"text", "calc"}:
            yield f"{pad}- {obj['text']}{' (computed)' if obj.get('calc') else ''}"
            return
        scalars = {k: v for k, v in obj.items() if isinstance(v, (str, int, float, bool)) and k not in SKIP}
        if len(scalars) == len(obj) - len(set(obj) & SKIP) and len(scalars) <= 4:
            yield pad + "- " + " · ".join(f"{v}" if k in ("title", "label", "text") else f"{k}: {v}"
                                          for k, v in scalars.items())
            return
        head = obj.get("title") or obj.get("takeaway") or obj.get("label") or obj.get("period")
        if head:
            yield f"{pad}- **{head}**"
        for k, v in obj.items():
            if k in SKIP or k in ("title", "takeaway", "label", "period"):
                continue
            if isinstance(v, (str, int, float)):
                yield f"{pad}  {k}: {v}"
            else:
                yield f"{pad}  {k}:"
                yield from flat(v, depth + 2)
    elif isinstance(obj, list):
        if obj and all(isinstance(x, (str, int, float)) for x in obj):
            yield f"{pad}- " + " | ".join(str(x) for x in obj)
        else:
            for x in obj:
                yield from flat(x, depth)


def main(fp, titles_only=False):
    story = json.loads(Path(fp).read_text(encoding="utf-8"))
    for i, s in enumerate(story["slides"], start=1):
        print(f"\n## {i}. [{s.get('layout')}] {s.get('title', '')}")
        if titles_only:
            continue
        body = {k: v for k, v in s.items() if k not in ("layout", "title", "notes") and k not in SKIP}
        for line in flat(body):
            try:
                print(line)
            except BrokenPipeError:
                sys.exit(0)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    main(sys.argv[1], "--titles-only" in sys.argv)
