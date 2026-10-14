#!/usr/bin/env python3
"""Rend un .pptx en images PNG (une par slide) pour le contrôle visuel.

Nécessite LibreOffice (soffice) et poppler (pdftoppm).
Usage : python3 render_check.py deck.pptx [dossier_sortie]
Le rendu LibreOffice diffère légèrement de PowerPoint (polices, ajustement du texte) :
il sert à repérer les débordements et chevauchements, pas à valider la typographie fine.
"""
import shutil
import subprocess
import sys
from pathlib import Path


def main(pptx, out=None):
    pptx = Path(pptx).resolve()
    out = Path(out or pptx.with_suffix("")).resolve()
    out.mkdir(parents=True, exist_ok=True)
    soffice = shutil.which("soffice") or shutil.which("libreoffice")
    if not soffice or not shutil.which("pdftoppm"):
        sys.exit("soffice et pdftoppm sont requis pour le rendu")
    subprocess.run([soffice, "--headless", "--convert-to", "pdf", "--outdir", str(out), str(pptx)],
                   check=True, capture_output=True)
    pdf = out / (pptx.stem + ".pdf")
    subprocess.run(["pdftoppm", "-png", "-r", "60", str(pdf), str(out / "slide")], check=True)
    for p in sorted(out.glob("slide-*.png")):
        print(p)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    main(*sys.argv[1:3])
