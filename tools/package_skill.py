#!/usr/bin/env python3
"""Package skills/deck as dist/deck.zip for upload to claude.ai."""
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "skills" / "deck"
OUT = ROOT / "dist" / "deck.zip"

OUT.parent.mkdir(exist_ok=True)
with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
    for f in sorted(SRC.rglob("*")):
        if f.is_file() and "__pycache__" not in f.parts:
            z.write(f, Path("deck") / f.relative_to(SRC))
print("wrote", OUT.relative_to(ROOT))
