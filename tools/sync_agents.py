#!/usr/bin/env python3
"""Génère agents/*.md (sous-agents Claude Code) à partir de skills/deck/roles/*.md.

Les rôles restent la source unique : le skill les lit en mode séquentiel (claude.ai),
le plugin les expose comme sous-agents (Claude Code). Relancer après toute modification d'un rôle :
    python3 tools/sync_agents.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ROLES = ROOT / "skills" / "deck" / "roles"
AGENTS = ROOT / "agents"

PREAMBULE = """> Fichier généré depuis `skills/deck/roles/{src}` par `tools/sync_agents.py`. Modifier le rôle, pas ce fichier.

L'orchestrateur te donne dans sa consigne : `SKILL_DIR` (dossier du skill deck), le dossier de travail, les fichiers à lire et le fichier à écrire. Tous les chemins `SKILL_DIR/...` ci-dessous s'y rapportent. Tu ne parles pas à l'utilisateur : tu rends ton livrable et un compte rendu court à l'orchestrateur.

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
        fm = "\n".join(f"{k}: {meta[k]}" for k in ("name", "description", "tools", "model") if k in meta)
        out = AGENTS / f"{meta['name']}.md"
        out.write_text(f"---\n{fm}\n---\n\n{PREAMBULE.format(src=role.name)}{body}", encoding="utf-8")
        print("écrit", out.relative_to(ROOT))


if __name__ == "__main__":
    main()
