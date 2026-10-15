#!/usr/bin/env python3
"""Generate agents/*.md (Claude Code subagents) from skills/deck/roles/*.md.

Roles stay the single source: the skill reads them in sequential mode (claude.ai),
the plugin exposes them as subagents (Claude Code). Rerun after editing any role:
    python3 tools/sync_agents.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ROLES = ROOT / "skills" / "deck" / "roles"
AGENTS = ROOT / "agents"

PREAMBLE = """> Generated from `skills/deck/roles/{src}` by `tools/sync_agents.py`. Edit the role, not this file.

The orchestrator gives you in its instruction: `SKILL_DIR` (folder of the deck skill), the working folder, the files to read and the file to write. Every `SKILL_DIR/...` path below refers to it. You do not talk to the user: you return your deliverable and a short report to the orchestrator. You write in English.

"""


def parse(text):
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    meta = {}
    for line in m.group(1).splitlines():
        k, _, v = line.partition(":")
        meta[k.strip()] = v.strip()
    return meta, m.group(2).lstrip()


def main():
    AGENTS.mkdir(exist_ok=True)
    for old in AGENTS.glob("*.md"):
        old.unlink()
    for role in sorted(ROLES.glob("*.md")):
        meta, body = parse(role.read_text(encoding="utf-8"))
        if meta.get("agent") != "true":
            continue
        fm = "\n".join(f"{k}: {meta[k]}" for k in ("name", "description", "tools", "model", "effort") if k in meta)
        out = AGENTS / f"{meta['name']}.md"
        out.write_text(f"---\n{fm}\n---\n\n{PREAMBLE.format(src=role.name)}{body}", encoding="utf-8")
        print("wrote", out.relative_to(ROOT))


if __name__ == "__main__":
    main()
