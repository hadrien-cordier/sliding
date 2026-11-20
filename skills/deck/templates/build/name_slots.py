"""Give every text shape that still has a default name a slot name derived from its placeholder,
numbered in reading order (top to bottom, left to right): "{Group}" -> group_1, group_2...
Then write each template's slot list into catalog.yaml (field `slots_named`), so the model
knows which names to fill. Run after the batch scripts: python3 name_slots.py
"""
import re
from pathlib import Path

import yaml
from pptx import Presentation

ROOT = Path(__file__).resolve().parent.parent
DEFAULT = re.compile(r"^(TextBox|Rectangle|Rounded Rectangle|Oval|Freeform|Chevron|Pentagon|Shape|Round Same Side Corner Rectangle|"
                     r"Isosceles Triangle|Hexagon)\s*\d+$")
PH = re.compile(r"\{([^{}]*)\}")


def slug(txt):
    m = PH.search(txt)
    base = m.group(1) if m else txt
    base = re.sub(r"[^a-z0-9]+", "_", base.lower()).strip("_")
    return "_".join(base.split("_")[:3]) or "text"


def main():
    cat_path = ROOT / "catalog.yaml"
    cat = yaml.safe_load(cat_path.read_text(encoding="utf-8"))
    by_slide = {(t["file"], t["slide"]): t for t in cat["templates"]}
    for f in sorted(ROOT.glob("lot*.pptx")):
        prs = Presentation(str(f))
        for si, slide in enumerate(prs.slides, start=1):
            counts = {}
            shapes = sorted(slide.shapes, key=lambda s: (round(s.top / 91440 / 0.15), s.left))
            for sh in shapes:
                if not sh.has_text_frame or not DEFAULT.match(sh.name):
                    continue
                txt = sh.text_frame.text.strip()
                if not PH.search(txt):
                    continue
                base = slug(txt)
                counts[base] = counts.get(base, 0) + 1
                sh.name = f"{base}_{counts[base]}"
            t = by_slide.get((f.stem, si))
            if t is not None:
                names = []
                for sh in shapes:
                    if sh.has_text_frame and PH.search(sh.text_frame.text) and sh.name not in names:
                        names.append(sh.name)
                t["slots_named"] = names
        prs.save(str(f))
    head = cat_path.read_text(encoding="utf-8").split("\nindex:")[0]
    cat_path.write_text(head + "\n" + yaml.safe_dump({"index": cat["index"], "templates": cat["templates"]},
                                                     sort_keys=False, allow_unicode=True, width=130), encoding="utf-8")
    print("named slots written to", cat_path.name)


if __name__ == "__main__":
    main()
