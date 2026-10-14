#!/usr/bin/env python3
"""Render a .pptx to PNG images (one per slide) for visual checking.

Requires LibreOffice (soffice) and poppler (pdftoppm).
Usage: python3 render_check.py deck.pptx [output_dir]
LibreOffice renders slightly differently from PowerPoint (fonts, text fitting):
use it to spot overflow and overlap, not to sign off fine typography.
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
        sys.exit("soffice and pdftoppm are required for rendering")
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
