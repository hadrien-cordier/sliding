#!/usr/bin/env python3
"""Self-evaluation of a built deck, run after every build. Code only, no model call.

Usage: python3 scorecard.py 04-storyboard.json deck.pptx [-o scorecard.json]

Scores four axes from 0 to 100 and lists the findings behind each penalty:
- storyline: linter errors on structure (executive summary, titles that ask, repeated layouts...)
- writing:   linter warnings on wording (second verb, colon, hedging...)
- design:    text likely to overflow its box, placeholders left, template coverage, density
- data:      numbers without a source, data shapes not resized from the data
Each finding is a candidate feedback entry (`feedback.py add --from-scorecard`).
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

from pptx import Presentation
from pptx.util import Emu

HERE = Path(__file__).resolve().parent
PH = re.compile(r"\{[^{}]*\}")
AXES = ("storyline", "writing", "design", "data")
DATA_HINTS = ("source", "numbers", "figure", "bars", "redraw", "draws figures")
STORY_HINTS = ("executive_summary", "layout", "question", "semicolon", "subtitle", "title")


def lint(story_path):
    r = subprocess.run([sys.executable, str(HERE / "lint_storyboard.py"), str(story_path)], capture_output=True, text=True)
    out = []
    for line in (r.stdout + r.stderr).splitlines():
        m = re.match(r"(ERROR|WARNING) (.*)", line)
        if m:
            out.append((m.group(1), m.group(2)))
    return out


def overflow(pptx_path):
    """Estimate text overflow: characters x line height against the box area (Arial, 0.5 em average width)."""
    found = []
    prs = Presentation(str(pptx_path))
    for i, slide in enumerate(prs.slides, start=1):
        for sh in slide.shapes:
            if not sh.has_text_frame or not sh.text_frame.text.strip():
                continue
            if PH.search(sh.text_frame.text):
                found.append(("design", f"slide {i}: placeholder left in '{sh.name}'", "placeholder-left"))
            w, h = Emu(sh.width).inches, Emu(sh.height).inches
            if w < 0.3 or h < 0.15 or sh.rotation:
                continue
            need = 0.0
            for p in sh.text_frame.paragraphs:
                size = max([r.font.size.pt for r in p.runs if r.font.size] or [12])
                chars = len("".join(r.text for r in p.runs))
                per_line = max(1, int(w * 72 / (size * 0.5)))
                lines = max(1, -(-chars // per_line))
                need += lines * size * 1.2 / 72
            if need > h * 1.5 and need - h > 0.3:
                found.append(("design", f"slide {i}: text in '{sh.name}' needs about {need:.1f} in for {h:.1f} in", "text-overflow"))
    return found, len(prs.slides)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("storyboard")
    ap.add_argument("deck")
    ap.add_argument("-o", "--out", default="scorecard.json")
    a = ap.parse_args()
    story = json.loads(Path(a.storyboard).read_text(encoding="utf-8"))
    findings = []
    for level, msg in lint(a.storyboard):
        low = msg.lower()
        axis = "data" if any(k in low for k in DATA_HINTS) else (
            "storyline" if level == "ERROR" and any(k in low for k in STORY_HINTS) else "writing")
        key = re.sub(r"[^a-z]+", "-", re.sub(r"^slide \d+( \([^)]*\))?: ", "", low))[:48].strip("-")
        findings.append((axis, f"{level}: {msg}", key, level))
    ov, n = overflow(a.deck)
    findings += [(ax, m, k, "WARNING") for ax, m, k in ov]
    body = [s for s in story.get("slides", []) if s.get("layout") not in ("cover", "executive_summary")]
    tpl = sum(1 for s in body if s.get("layout") == "template")
    scores = {}
    for ax in AXES:
        pen = sum(12 if lvl == "ERROR" else 4 for a_, _, _, lvl in findings if a_ == ax)
        scores[ax] = max(0, 100 - pen)
    card = {"slides": n, "body_slides": len(body), "template_share": round(tpl / max(1, len(body)), 2),
            "scores": scores, "findings": [{"axis": a_, "message": m, "key": k} for a_, m, k, _ in findings]}
    Path(a.out).write_text(json.dumps(card, indent=1, ensure_ascii=False), encoding="utf-8")
    print(" | ".join(f"{k} {v}" for k, v in scores.items()), f"| templates {card['template_share']:.0%} of body slides")
    for f in card["findings"][:25]:
        print(f"- [{f['axis']}] {f['message']}")


if __name__ == "__main__":
    main()
