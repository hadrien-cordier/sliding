#!/usr/bin/env python3
"""Feedback log of the deck engine: every critique after a build, from the user, a reviewer or the scorecard.

The log is one JSON line per critique. Default location: feedback/log.jsonl at the repo root when the
skill runs from a clone of the repo, otherwise ./feedback.jsonl in the working folder (to submit later).

  python3 feedback.py add --deck kyc-study --slide 4 --axis design --key title-describes-content \
      --critique "Title names the topic instead of the conclusion the data supports" --source user [--template id]
  python3 feedback.py add --from-scorecard scorecard.json --deck kyc-study
  python3 feedback.py list [--status open]

Write the critique as a reusable pattern: no client name, no figure, no verbatim sentence from the deck.
Axes: storyline, writing, design, data, template. Keys are short kebab-case labels reused across decks
(the curator groups entries by axis and key).
"""
import argparse
import datetime as dt
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO_LOG = HERE.parent.parent.parent / "feedback" / "log.jsonl"


def log_path(arg=None):
    if arg:
        return Path(arg)
    if (HERE.parent.parent.parent / ".claude-plugin").exists():
        return REPO_LOG
    return Path("feedback.jsonl")


def append(path, entries):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        for e in entries:
            f.write(json.dumps(e, ensure_ascii=False) + "\n")


def read(path):
    if not path.exists():
        return []
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["add", "list"])
    ap.add_argument("--log")
    ap.add_argument("--deck")
    ap.add_argument("--slide", type=int)
    ap.add_argument("--axis", choices=["storyline", "writing", "design", "data", "template"])
    ap.add_argument("--key")
    ap.add_argument("--critique")
    ap.add_argument("--template")
    ap.add_argument("--source", default="user", choices=["user", "reviewer", "scorecard"])
    ap.add_argument("--severity", default="med", choices=["low", "med", "high"])
    ap.add_argument("--from-scorecard")
    ap.add_argument("--status")
    a = ap.parse_args()
    path = log_path(a.log)
    today = dt.date.today().isoformat()
    if a.cmd == "add":
        if a.from_scorecard:
            card = json.loads(Path(a.from_scorecard).read_text(encoding="utf-8"))
            entries = [{"date": today, "deck": a.deck, "axis": f["axis"], "key": f["key"], "critique": f["message"],
                        "source": "scorecard", "severity": "low", "status": "open"} for f in card["findings"]]
        else:
            if not (a.axis and a.key and a.critique):
                ap.error("add needs --axis, --key and --critique (or --from-scorecard)")
            entries = [{"date": today, "deck": a.deck, "slide": a.slide, "axis": a.axis, "key": a.key,
                        "template": a.template, "critique": a.critique, "source": a.source,
                        "severity": a.severity, "status": "open"}]
        append(path, entries)
        print(f"{len(entries)} entr{'y' if len(entries) == 1 else 'ies'} added to {path}")
    else:
        for e in read(path):
            if a.status and e.get("status") != a.status:
                continue
            print(f"{e['date']} [{e['axis']}/{e['key']}] {e.get('deck')} s{e.get('slide') or '-'} ({e['source']}, "
                  f"{e['status']}): {e['critique']}")


if __name__ == "__main__":
    main()
