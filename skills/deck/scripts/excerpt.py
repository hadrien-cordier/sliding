#!/usr/bin/env python3
"""Print only the table rows of a markdown register whose Ref column matches given refs.

The orchestrator passes agents excerpts of the fact register, never the whole register.
Header rows are kept so the excerpt stays readable.

Usage: python3 excerpt.py research/cycle-1-*.md C1-MKT-04 C1-REG-02 > excerpt.md
       python3 excerpt.py 02-fact-register.md --status CONFIRMED   (rows containing a word)
Arguments ending in .md are files; the others are refs.
"""
import sys
from pathlib import Path


def main(files, keys, status=None):
    for fp in files:
        print(f"<!-- {fp} -->")
        one(fp, keys, status)


def one(fp, keys, status=None):
    lines = Path(fp).read_text(encoding="utf-8").splitlines()
    header = None
    out = []
    for i, ln in enumerate(lines):
        if ln.startswith("|") and i + 1 < len(lines) and set(lines[i + 1].replace("|", "").strip()) <= set("-: "):
            header = (ln, lines[i + 1])
            continue
        if not ln.startswith("|") or set(ln.replace("|", "").strip()) <= set("-: "):
            continue
        cells = [c.strip() for c in ln.strip("|").split("|")]
        hit = (cells and cells[0] in keys) or (status and status in ln)
        if hit:
            if header and (not out or out[-1] is not header):
                out.append(header)
            out.append(ln)
    for o in out:
        print("\n".join(o) if isinstance(o, tuple) else o)


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(2)
    status = None
    if "--status" in args:
        k = args.index("--status")
        status = args[k + 1]
        args = args[:k] + args[k + 2:]
    files = [a for a in args if a.endswith(".md")]
    main(files, {a for a in args if not a.endswith(".md")}, status)
