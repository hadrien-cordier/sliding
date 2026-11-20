"""Measured-rebuild primitives: map reference pixels to slide inches, soft shapes, Bezier curves, tapered arrows."""
import math
from lib import *

BODY = (0.5, 1.15, 12.3, 5.55)   # x, y, w, h of the exhibit body on the slide, in inches


class Frame:
    """Maps a crop of the reference image (pixels) onto the slide body, keeping the aspect ratio."""
    def __init__(self, crop, body=BODY, align="top"):
        self.x0, self.y0, x1, y1 = crop
        bw, bh = body[2], body[3]
        self.ppi = max((x1 - self.x0) / bw, (y1 - self.y0) / bh)
        self.ox = body[0] + (bw - (x1 - self.x0) / self.ppi) / 2
        self.oy = body[1] if align == "top" else body[1] + (bh - (y1 - self.y0) / self.ppi) / 2

    def X(self, px): return self.ox + (px - self.x0) / self.ppi
    def Y(self, py): return self.oy + (py - self.y0) / self.ppi
    def L(self, p): return p / self.ppi
    def F(self, px_text):
        """Font size in points from the cap-to-descender height of a text line in pixels."""
        return round(px_text / self.ppi * 72 * 1.15, 1)
    def R(self, x, y, w, h): return self.X(x), self.Y(y), self.L(w), self.L(h)


def round_caps(shp):
    shp.line._get_or_add_ln().set("cap", "rnd")


def arrow_size(shp, end="tail", w="med", length="med", kind="triangle"):
    arrowhead(shp, end, kind)
    ln = shp.line._get_or_add_ln()
    el = ln.find(qn("a:tailEnd" if end == "tail" else "a:headEnd"))
    el.set("w", w); el.set("len", length)


def rrect(slide, x, y, w, h, r, **kw):
    """Rounded rectangle with a corner radius in inches."""
    s = box(slide, x, y, w, h, shape=MSO_SHAPE.ROUNDED_RECTANGLE, **kw)
    s.adjustments[0] = min(0.5, r / min(w, h))
    return s


def top_round(slide, x, y, w, h, r, **kw):
    s = box(slide, x, y, w, h, shape=MSO_SHAPE.ROUND_2_SAME_RECTANGLE, **kw)
    s.adjustments[0] = min(0.5, r / min(w, h)); s.adjustments[1] = 0
    return s


def chevron(slide, x, y, w, h, depth, first=False, **kw):
    """Chevron (or pentagon when first) whose point depth is given in inches."""
    s = box(slide, x, y, w, h, shape=MSO_SHAPE.PENTAGON if first else MSO_SHAPE.CHEVRON, **kw)
    s.adjustments[0] = depth / min(w, h)
    return s


def bez(p0, p1, p2, p3, n=40):
    pts = []
    for i in range(n + 1):
        t = i / n; u = 1 - t
        pts.append((u**3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t**3 * p3[0],
                    u**3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t**3 * p3[1]))
    return pts


def curve(slide, p0, p1, p2, p3, color="grey400", lw=1.0, dash=False, arrow=None, aw="med", al="med", name=None):
    s = polyline(slide, bez(p0, p1, p2, p3), color, lw=lw, dash=dash, name=name)
    round_caps(s)
    if arrow:
        arrow_size(s, arrow, aw, al)
    return s


def swoosh(slide, p0, p1, p2, tip, w0, w1, head_w, head_len, color, name=None):
    """Filled curved arrow: body tapers from w0 to w1 along a cubic curve, then a flared head ending at tip."""
    dx, dy = tip[0] - p2[0], tip[1] - p2[1]
    L = math.hypot(dx, dy); ux, uy = dx / L, dy / L
    p3 = (tip[0] - ux * head_len, tip[1] - uy * head_len)
    cen = bez(p0, p1, p2, p3, 60)
    left, right = [], []
    for i, (x, y) in enumerate(cen):
        a = cen[max(0, i - 1)]; b = cen[min(len(cen) - 1, i + 1)]
        tx, ty = b[0] - a[0], b[1] - a[1]; tl = math.hypot(tx, ty) or 1
        nx, ny = -ty / tl, tx / tl
        w = (w0 + (w1 - w0) * (i / 60) ** 0.8) / 2
        left.append((x + nx * w, y + ny * w)); right.append((x - nx * w, y - ny * w))
    nx, ny = -uy, ux
    head = [(p3[0] + nx * head_w / 2, p3[1] + ny * head_w / 2), tip, (p3[0] - nx * head_w / 2, p3[1] - ny * head_w / 2)]
    return polyline(slide, left + head + right[::-1], None, fill=color, close=True, name=name), p3


def soft_line(slide, x1, y1, x2, y2, color="grey400", lw=1.0, dash=False, arrow=None, aw="med", al="med", name=None):
    s = line(slide, x1, y1, x2, y2, color, lw=lw, dash=dash, name=name)
    round_caps(s)
    if arrow:
        arrow_size(s, arrow, aw, al)
    return s


def elbow(slide, pts, color="grey400", lw=1.0, dash=False, arrow=None, r=0.06, aw="med", al="med", name=None):
    """Orthogonal path through pts with softly rounded corners."""
    pts = [p for i, p in enumerate(pts) if i == 0 or math.hypot(p[0] - pts[i - 1][0], p[1] - pts[i - 1][1]) > 1e-6]
    out = [pts[0]]
    for i in range(1, len(pts) - 1):
        (ax, ay), (bx, by), (cx, cy) = pts[i - 1], pts[i], pts[i + 1]
        d1 = math.hypot(bx - ax, by - ay); d2 = math.hypot(cx - bx, cy - by)
        rr = min(r, d1 / 2, d2 / 2)
        p_in = (bx - (bx - ax) / d1 * rr, by - (by - ay) / d1 * rr)
        p_out = (bx + (cx - bx) / d2 * rr, by + (cy - by) / d2 * rr)
        out += bez(p_in, (bx, by), (bx, by), p_out, 6)
    out.append(pts[-1])
    s = polyline(slide, out, color, lw=lw, dash=dash, name=name)
    round_caps(s)
    if arrow:
        arrow_size(s, arrow, aw, al)
    return s


class Frame2:
    """Like Frame, but fills the body: x and y scale independently (for references taller than 16:9).
    W/H convert widths and heights, D converts sizes that must stay round, F scales text on the mean."""
    def __init__(self, crop, body=BODY):
        self.x0, self.y0, x1, y1 = crop
        self.px = (x1 - self.x0) / body[2]
        self.py = (y1 - self.y0) / body[3]
        self.bx, self.by = body[0], body[1]

    def X(self, p): return self.bx + (p - self.x0) / self.px
    def Y(self, p): return self.by + (p - self.y0) / self.py
    def W(self, p): return p / self.px
    def H(self, p): return p / self.py
    def D(self, p): return p / max(self.px, self.py) * 1.25
    def F(self, p): return round(p / (self.px * self.py) ** 0.5 * 72 * 1.15, 1)
    def R(self, x, y, w, h): return self.X(x), self.Y(y), self.W(w), self.H(h)


def open_frame(slide, x, y, w, h, r, color="text", lw=2.5, name=None):
    """Device outline: rounded top corners, open bottom."""
    return elbow(slide, [(x, y + h), (x, y), (x + w, y), (x + w, y + h)], color, lw=lw, r=r, name=name)


def alpha(shp, pct):
    """Fill transparency in percent (0 opaque) so overlapping shapes blend."""
    sf = shp._element.spPr.find(qn("a:solidFill"))
    clr = sf[0]
    for e in clr.findall(qn("a:alpha")):
        clr.remove(e)
    a = etree.SubElement(clr, qn("a:alpha")); a.set("val", str(int((100 - pct) * 1000)))
