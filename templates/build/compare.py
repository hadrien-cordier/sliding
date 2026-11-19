"""Render a deck and stack each slide under its reference image at full width for review.
Usage: python3 compare.py deck.pptx outprefix d01 d02 ..."""
import subprocess, sys, os, glob
from PIL import Image, ImageDraw

deck, prefix, ids = sys.argv[1], sys.argv[2], sys.argv[3:]
outdir = os.path.dirname(os.path.abspath(deck))
subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", outdir, deck], capture_output=True, timeout=240)
pdf = os.path.splitext(os.path.abspath(deck))[0] + ".pdf"
for f in glob.glob(f"{prefix}-r-*.png"):
    os.remove(f)
subprocess.run(["pdftoppm", "-r", "110", "-png", pdf, f"{prefix}-r"], check=True)
renders = sorted(glob.glob(f"{prefix}-r-*.png"), key=lambda p: int(p.rsplit("-", 1)[1].split(".")[0]))
pages = []
for d, r in zip(ids, renders):
    o = Image.open(f"" + os.environ.get("REF_DIR", "refs") + "/{d}.png").convert("RGB")
    rr = Image.open(r).convert("RGB")
    W = 1300
    o = o.resize((W, int(o.height * W / o.width))) if o.width / o.height > 1.2 else o.resize((int(o.width * 700 / o.height), 700))
    rr = rr.resize((W, int(rr.height * W / rr.width)))
    c = Image.new("RGB", (W, o.height + rr.height + 70), "white")
    dr = ImageDraw.Draw(c)
    dr.text((5, 5), f"{d}  reference", fill="black"); c.paste(o, (0, 25))
    dr.text((5, o.height + 40), f"{d}  rebuilt template (neutral theme, editable shapes)", fill="black")
    c.paste(rr, (0, o.height + 65))
    c.save(f"{prefix}-{d}.png")
    pages.append(c)
pages[0].save(f"{prefix}.pdf", save_all=True, append_images=pages[1:], resolution=110)
print("ok", len(pages))
