#!/usr/bin/env python3
"""Turn the feedback log into improvement proposals for the user to validate.

Usage: python3 curate_feedback.py [--log feedback/log.jsonl] [-o feedback/proposals.md]

Rules:
- Entries are grouped by (axis, key).
- A group becomes a proposal when it recurs on at least 2 different decks, or holds one high-severity
  user critique. One-off remarks stay in the log: they were fixed in their own deck.
- Scorecard-only groups need 3 decks: code findings are cheap and noisy.
- Each proposal says where the change belongs: a linter check when the rule can be tested by code,
  a template fiche or build script when it names a template, otherwise the rules card or layouts guide.
Nothing changes in the engine until the user validates a proposal; the curator role then applies it.
"""
import argparse
from collections import defaultdict
from pathlib import Path

from feedback import log_path, read

CODE_HINTS = ("overflow", "placeholder", "semicolon", "colon", "length", "words", "verb", "source", "dash", "repeat",
              "bars", "font", "size", "count")


def target(axis, key, template):
    if template:
        return f"templates: fiche or build script of `{template}`"
    if any(h in key for h in CODE_HINTS):
        return "scripts/lint_storyboard.py (new or stricter check)"
    if axis == "design":
        return "references/layouts.md or templates/catalog.yaml"
    return "references/rules-card.md (merge with an existing rule, keep one page)"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--log")
    ap.add_argument("-o", "--out", default=None)
    a = ap.parse_args()
    path = log_path(a.log)
    entries = [e for e in read(path) if e.get("status") in ("open", "proposed")]
    groups = defaultdict(list)
    for e in entries:
        groups[(e["axis"], e["key"])].append(e)
    props = []
    for (axis, key), es in groups.items():
        decks = {e.get("deck") for e in es}
        users = [e for e in es if e["source"] != "scorecard"]
        need = 3 if not users else 2
        high = any(e["severity"] == "high" and e["source"] == "user" for e in es)
        if len(decks) >= need or high:
            tpl = next((e.get("template") for e in es if e.get("template")), None)
            props.append((len(decks), axis, key, tpl, es))
    props.sort(key=lambda p: (-p[0], p[1]))
    out = Path(a.out) if a.out else path.parent / "proposals.md"
    lines = ["# Improvement proposals", "", f"From {len(entries)} open entries in `{path.name}`. Validate, edit or reject each one.", ""]
    for n, axis, key, tpl, es in props:
        lines += [f"## [{axis}] {key}  ({n} deck{'s' if n > 1 else ''}, {len(es)} entries)",
                  f"- Where: {target(axis, key, tpl)}",
                  "- Evidence:"] + [f"  - {e.get('deck')} s{e.get('slide') or '-'} ({e['source']}): {e['critique']}" for e in es[:5]] + [
                  "- Proposed change: (curator writes it here)", "- Decision: pending", ""]
    if not props:
        lines.append("No group meets the threshold yet.")
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"{len(props)} proposal(s) written to {out}")


if __name__ == "__main__":
    main()
