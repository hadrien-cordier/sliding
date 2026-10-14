#!/usr/bin/env python3
"""Contrôle mécanique d'un storyboard avant la revue humaine ou par le reviewer.

Le linter attrape ce qu'une règle peut détecter sans comprendre le sens :
structure du JSON, chiffres sans source, tirets longs, points-virgules et questions dans
les titres, adverbes de modulation, tournures « ne pas X mais Y », voix passive probable,
titres de blocs réduits à une étiquette, titres de slides en double.

Il ne juge ni le narratif ni la couverture du titre par le corps : ces contrôles
reviennent au reviewer. Un AVERTISSEMENT demande un regard ; une ERREUR bloque la construction.

Usage : python3 lint_storyboard.py storyboard.json   (code de sortie 1 si erreur)
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from layouts_spec import HARVEY, IDEA_TITLE_FIELDS, LAYOUTS  # noqa: E402

ADVERBES = [
    # français
    "seulement", "uniquement", "déjà", "désormais", "dorénavant", "maintenant", "à peine",
    "vraiment", "très", "extrêmement", "particulièrement", "plus de", "moins de", "juste",
    "même", "simplement", "clairement", "fortement", "réellement",
    # anglais
    "only", "now", "already", "more than", "less than", "just", "even", "really", "very",
    "clearly", "simply",
]
PASSIF_FR = re.compile(
    r"\b(est|sont|était|étaient|sera|seront|serait|seraient|a été|ont été|avait été|avaient été|"
    r"être|été|soit|soient|fut|furent)\s+(\w+(?:é|ée|és|ées|is|ise|ises|it|ite|its|ites|u|ue|us|ues|"
    r"ert|erte|erts|ertes))\b",
    re.IGNORECASE,
)
PASSIF_EN = re.compile(r"\b(is|are|was|were|been|be|being)\s+(\w+ed|\w+en)\b", re.IGNORECASE)
PAS_MAIS = re.compile(r"\b(ne|n')\s?[^.;]{0,50}\bpas\b[^.;]{0,80}\bmais\b|\bnot\b[^.;]{0,60}\bbut\b",
                      re.IGNORECASE)
CHIFFRE = re.compile(r"\d")
TIRETS = re.compile(r"[—–]")
# participes passés qui sont en pratique des adjectifs ou des attributs fréquents
FAUX_PASSIFS = {"prêt", "prête", "nécessaire", "connu", "connue", "lié", "liée", "liés", "liées",
                "exposé", "exposée", "exposés", "exposées", "dû", "due", "dus", "dues"}


def textes(obj, path=""):
    """Parcourt le JSON et rend (chemin, texte) pour chaque chaîne."""
    if isinstance(obj, str):
        yield path, obj
    elif isinstance(obj, dict):
        for k, v in obj.items():
            if k in ("layout", "accent", "police", "format", "unite", "type", "id"):
                continue
            yield from textes(v, f"{path}.{k}" if path else k)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from textes(v, f"{path}[{i}]")


def main(fp):
    story = json.loads(Path(fp).read_text(encoding="utf-8"))
    err, warn = [], []
    titres = {}
    for i, s in enumerate(story.get("slides", []), start=1):
        lay = s.get("layout")
        tag = f"slide {i}"
        if lay not in LAYOUTS:
            err.append(f"{tag} : gabarit inconnu « {lay} »")
            continue
        for f in LAYOUTS[lay][0]:
            if f not in s:
                err.append(f"{tag} ({lay}) : champ obligatoire manquant « {f} »")
        t = s.get("titre", "")
        if not t:
            err.append(f"{tag} : titre manquant")
        if lay != "couverture":
            if t.strip().endswith("?"):
                err.append(f"{tag} : le titre pose une question ; il doit affirmer le message")
            if ";" in t:
                err.append(f"{tag} : point-virgule dans le titre (une seule phrase, une seule idée)")
            if ":" in t:
                warn.append(f"{tag} : deux-points dans le titre ; vérifier qu'il reste une phrase unique")
            if t.count(",") >= 2 or "(" in t:
                warn.append(f"{tag} : incise probable dans le titre")
            if len(t.split()) < 6:
                warn.append(f"{tag} : titre court ({len(t.split())} mots) ; porte-t-il le message entier ?")
            if len(t.split()) > 32:
                warn.append(f"{tag} : titre de {len(t.split())} mots ; vérifier qu'il porte une seule idée")
            key = t.strip().lower()
            if key in titres:
                err.append(f"{tag} : titre identique à la slide {titres[key]}")
            titres[key] = i
        # titres de blocs : ils énoncent une idée
        for field in IDEA_TITLE_FIELDS.get(lay, []):
            items = s.get(field)
            items = [items] if isinstance(items, dict) else (items or [])
            for k, b in enumerate(items):
                bt = (b or {}).get("titre", "")
                if not bt:
                    err.append(f"{tag} : {field}[{k}] sans titre ; chaque bloc répond à une question par une idée")
                elif len(bt.split()) < 4:
                    warn.append(f"{tag} : titre de bloc « {bt} » ressemble à une étiquette ; écrire l'idée")
        graph = s.get("graphique") or {}
        if lay in ("graphique_texte",) and not graph.get("titre"):
            warn.append(f"{tag} : graphique sans titre ; son titre énonce ce que montre la donnée")
        if lay == "waterfall" and not s.get("titre_graphique"):
            warn.append(f"{tag} : waterfall sans titre_graphique")
        # chiffres : toute slide qui en contient cite une source
        has_digit = any(CHIFFRE.search(txt) for p, txt in textes(s)
                        if not p.startswith("source") and txt.strip() not in HARVEY)
        has_digit = has_digit or lay in ("graphique_texte", "waterfall")
        if has_digit and not s.get("source") and lay != "couverture":
            err.append(f"{tag} : chiffres présents sans source")
        # règles d'écriture sur tous les textes
        for p, txt in textes(s):
            if p.startswith("notes"):
                continue
            low = txt.lower()
            if TIRETS.search(txt):
                err.append(f"{tag} [{p}] : tiret long ou demi-cadratin ; reformuler")
            for a in ADVERBES:
                if re.search(rf"(?<![\w-]){re.escape(a)}(?![\w-])", low):
                    warn.append(f"{tag} [{p}] : adverbe de modulation « {a} »")
            for m in PASSIF_FR.finditer(txt):
                if m.group(2).lower() not in FAUX_PASSIFS:
                    warn.append(f"{tag} [{p}] : voix passive probable « {m.group(0)} »")
            for m in PASSIF_EN.finditer(txt):
                warn.append(f"{tag} [{p}] : passive voice probable « {m.group(0)} »")
            if PAS_MAIS.search(txt):
                warn.append(f"{tag} [{p}] : tournure « ne pas X mais Y » ; affirmer Y")
    for e in err:
        print("ERREUR", e)
    for w in warn:
        print("AVERTISSEMENT", w)
    print(f"\n{len(err)} erreur(s), {len(warn)} avertissement(s)")
    return 1 if err else 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(sys.argv[1]))
