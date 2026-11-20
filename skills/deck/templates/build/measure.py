"""Measure an exhibit image: solid colour regions (bounding boxes, colours, shape hint).
Usage: python3 measure.py <image> [min_area] [crop x0,y0,x1,y1]"""
import sys
import numpy as np
from PIL import Image
from scipy import ndimage

img = Image.open(sys.argv[1]).convert("RGB")
min_area = int(sys.argv[2]) if len(sys.argv) > 2 else 400
a = np.asarray(img).astype(int)
if len(sys.argv) > 3:
    x0, y0, x1, y1 = map(int, sys.argv[3].split(","))
else:
    x0, y0, x1, y1 = 0, 0, a.shape[1], a.shape[0]
a = a[y0:y1, x0:x1]
# quantise to 16 levels per channel; ignore near-white background
q = (a // 16) * 16 + 8
key = q[..., 0] * 65536 + q[..., 1] * 256 + q[..., 2]
white = (a.min(axis=2) > int(__import__("os").environ.get("WHITE", "238")))
out = []
for k in np.unique(key[~white]):
    mask = (key == k) & ~white
    if mask.sum() < min_area:
        continue
    lab, n = ndimage.label(mask)
    for i, sl in enumerate(ndimage.find_objects(lab), 1):
        comp = lab[sl] == i
        area = int(comp.sum())
        if area < min_area:
            continue
        h, w = comp.shape
        fill = area / (h * w)
        col = a[sl][comp].mean(axis=0).astype(int)
        hint = "rect" if fill > 0.9 else ("ellipse" if 0.72 < fill < 0.82 and abs(w - h) < 0.15 * max(w, h) else "other")
        out.append((sl[1].start + x0, sl[0].start + y0, w, h, "#%02X%02X%02X" % tuple(col), round(fill, 2), hint, area))
out.sort(key=lambda r: (r[1] // 10, r[0]))
print(f"image {img.size}, crop {(x0, y0, x1, y1)}; x y w h colour fill hint")
for r in out:
    print(*r[:7])
