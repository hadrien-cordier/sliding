#!/usr/bin/env python3
"""Mechanical check of a storyboard before the reviewer reads it.

The linter catches what a rule can detect without understanding meaning: JSON structure,
numbers without a source, subtitles, visible SCQA labels, a missing executive summary,
a layout used three times in a row, a missing layout rationale,
dashes and semicolons, question titles, likely second verbs in titles, hedging adverbs,
"not X but Y", likely passive voice, block titles reduced to labels, duplicate titles.

It does not judge the storyline or whether the body covers the title: the reviewer does.
A WARNING asks for a look; an ERROR blocks the build.

Usage: python3 lint_storyboard.py storyboard.json   (exit code 1 on error)
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from layouts_spec import HARVEY, IDEA_TITLE_FIELDS, LAYOUTS  # noqa: E402

HEDGES = ["only", "now", "already", "more than", "less than", "just", "even", "really", "very",
          "clearly", "simply", "currently", "still", "merely", "quite", "rather", "somewhat",
          "significantly", "extremely", "highly", "truly", "basically"]
IRREGULAR_PP = ("done|made|taken|given|seen|known|shown|driven|held|built|set|put|paid|sold|led|kept|"
                "brought|found|lost|met|spent|won|written|chosen|grown|drawn|left|cut|bought|thought|"
                "told|sent|run|begun|broken|spoken|undertaken|overtaken|withdrawn|hidden")
PASSIVE = re.compile(rf"\b(am|is|are|was|were|be|been|being)\s+(\w+ly\s+)?(\w+ed|{IRREGULAR_PP})\b",
                     re.IGNORECASE)
NOT_BUT = re.compile(r"\bnot\b[^.;]{0,60}\bbut\b|\brather than\b", re.IGNORECASE)
CLAUSE = re.compile(r",\s*which\b|\bwhile\b|\bwhereas\b|\bbut\b|\bbecause\b|\balthough\b|\bso that\b|"
                    r"\band then\b|\bthereby\b|\bwhich\b", re.IGNORECASE)
AUX = re.compile(r"\b(is|are|was|were|has|have|had|will|would|can|could|should|must|may|might|does|do)\b",
                 re.IGNORECASE)
SCQA = re.compile(r"\b(situation|complication|question|resolution)\s*:", re.IGNORECASE)
DIGIT = re.compile(r"\d")
DASHES = re.compile(r"[—–]")
SUBTITLE_KEYS = {"subtitle", "sub_title", "kicker", "tagline", "overline"}
SKIP_KEYS = {"layout", "accent", "font", "format", "unit", "type", "id", "start", "end", "layout_rationale"}


def texts(obj, path=""):
    """Yield (path, text) for every string in the JSON."""
    if isinstance(obj, str):
        yield path, obj
    elif isinstance(obj, dict):
        for k, v in obj.items():
            if k not in SKIP_KEYS:
                yield from texts(v, f"{path}.{k}" if path else k)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from texts(v, f"{path}[{i}]")


def main(fp):
    story = json.loads(Path(fp).read_text(encoding="utf-8"))
    err, warn = [], []
    seen = {}
    slides = story.get("slides", [])
    content = [s for s in slides if s.get("layout") != "cover"]
    if not content or content[0].get("layout") != "executive_summary":
        err.append("deck: the first content slide must be the executive_summary, written last")
    # layout diversity: the same layout never more than twice in a row (argument mode only;
    # a benchmark repeats one exhibit per unit of its grid by design)
    benchmark = story.get("meta", {}).get("mode") == "benchmark"
    run, prev = 0, None
    first_of_run = set()
    for i, s in enumerate(slides, start=1):
        lay = s.get("layout")
        run = run + 1 if lay == prev else 1
        if run == 1:
            first_of_run.add(i)
        prev = lay
        if run == 3 and not benchmark and lay not in ("cover", "executive_summary"):
            err.append(f"slide {i}: layout '{lay}' used three times in a row; change the layout or merge slides")
    for i, s in enumerate(slides, start=1):
        lay = s.get("layout")
        tag = f"slide {i}"
        if lay not in LAYOUTS:
            err.append(f"{tag}: unknown layout '{lay}'")
            continue
        for f in LAYOUTS[lay][0]:
            if f not in s:
                err.append(f"{tag} ({lay}): missing required field '{f}'")
        for k in SUBTITLE_KEYS & set(s):
            err.append(f"{tag}: '{k}' field found; slides carry no subtitle")
        t = s.get("title", "")
        if not t:
            err.append(f"{tag}: missing title")
        if lay != "cover":
            words = len(t.split())
            if t.strip().endswith("?"):
                err.append(f"{tag}: the title asks a question; it must state the message")
            if ";" in t:
                err.append(f"{tag}: semicolon in title (one sentence, one idea)")
            if ":" in t:
                warn.append(f"{tag}: colon in title; check it stays one sentence with one idea")
            if "(" in t:
                warn.append(f"{tag}: parenthesis in title; remove the aside")
            m = CLAUSE.search(t)
            if m or len(AUX.findall(t)) > 1:
                warn.append(f"{tag}: title may carry a second verb ('{m.group(0) if m else 'two auxiliaries'}');"
                            " keep one action verb")
            if words < 6:
                warn.append(f"{tag}: short title ({words} words); does it carry the whole message?")
            if words > 30:
                warn.append(f"{tag}: {words}-word title; check it carries one idea")
            key = t.strip().lower()
            if key in seen:
                err.append(f"{tag}: same title as slide {seen[key]}")
            seen[key] = i
        if lay not in ("cover", "executive_summary") and (not benchmark or i in first_of_run):
            r = s.get("layout_rationale") or {}
            for k in ("relation", "alternative", "why"):
                if not r.get(k):
                    err.append(f"{tag}: layout_rationale.{k} missing; name the relation, the second candidate"
                               " layout and why this one wins")
        if lay == "executive_summary":
            n = len(s.get("items", []))
            if not 3 <= n <= 6:
                warn.append(f"{tag}: executive summary with {n} takeaways (3 to 6 expected)")
            for k, it in enumerate(s.get("items", [])):
                if not it.get("takeaway"):
                    err.append(f"{tag}: items[{k}] without takeaway")
        for field in IDEA_TITLE_FIELDS.get(lay, []):
            items = s.get(field)
            items = [items] if isinstance(items, dict) else (items or [])
            for k, b in enumerate(items):
                bt = (b or {}).get("title", "")
                if not bt:
                    err.append(f"{tag}: {field}[{k}] has no title; each block answers a question with an idea")
                elif len(bt.split()) < 4:
                    warn.append(f"{tag}: block title '{bt}' reads like a label; write the idea")
        if lay == "chart_text" and not (s.get("chart") or {}).get("title"):
            warn.append(f"{tag}: chart without title; its title states what the data shows")
        if lay == "waterfall" and not s.get("chart_title"):
            warn.append(f"{tag}: waterfall without chart_title")
        has_digit = any(DIGIT.search(x) for p, x in texts(s)
                        if not p.startswith(("source", "notes", "periods")) and x.strip() not in HARVEY)
        has_digit = has_digit or lay in ("chart_text", "waterfall", "big_number")
        if has_digit and not s.get("source") and lay not in ("cover", "executive_summary"):
            err.append(f"{tag}: numbers without a source")
        for p, x in texts(s):
            if p.startswith("notes"):
                continue
            low = x.lower()
            if DASHES.search(x):
                err.append(f"{tag} [{p}]: em or en dash; rephrase")
            if SCQA.search(x):
                err.append(f"{tag} [{p}]: visible SCQA label; the SCQA stays implicit")
            for a in HEDGES:
                if re.search(rf"(?<![\w-]){re.escape(a)}(?![\w-])", low):
                    warn.append(f"{tag} [{p}]: hedging adverb '{a}'")
            for m in PASSIVE.finditer(x):
                warn.append(f"{tag} [{p}]: likely passive voice '{m.group(0)}'")
            if NOT_BUT.search(x):
                warn.append(f"{tag} [{p}]: 'not X but Y' or 'rather than'; state Y")
    for e in err:
        print("ERROR", e)
    for w in warn:
        print("WARNING", w)
    print(f"\n{len(err)} error(s), {len(warn)} warning(s)")
    return 1 if err else 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(sys.argv[1]))
