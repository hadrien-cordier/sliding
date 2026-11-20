"""Measured rebuild, designs d29-d32."""
import math, random, sys
from lib2 import *

prs = new_deck()


# d29 three paired bar charts chained by ellipses, with multiplier brackets ---------------------------
def d29():
    s = slide(prs)
    header(s, "{Group A} trades at a premium over {group B} because of {driver}", "{source}")
    f = Frame2((15, 155, 820, 495), body=(0.5, 1.0, 12.3, 5.65)); X, Y, W, H, D, F = f.X, f.Y, f.W, f.H, f.D, f.F
    panels = [(20, "{Claim}…", "#acc", (378, 300), "accent500"), (305, "…{despite this}…", "#neg", (338, 300), "grey800"),
              (590, "…{because of this}", "#acc", (366, 300), "accent500")]
    for k, (x0, head, _, (ya, yb), col) in enumerate(panels, 1):
        text(s, X(x0), Y(160), W(230), H(52), [[(head, {"bold": True})]], size=16, color="text", anchor="b", margin=0,
             name=f"panel_{k}_title")
        text(s, X(x0), Y(218), W(230), H(18), "{MEASURE (UNIT)}", size=F(12), color="grey600", margin=0)
        for j, (bx, top, fill) in enumerate(((x0 + 15, ya, "grey200"), (x0 + 140, yb, col))):
            box(s, X(bx), Y(top), W(72), H(467 - top), fill=fill, name=f"panel_{k}_bar_{j+1}")
            text(s, X(bx), Y(top - 22), W(72), H(18), [[("{v}", {"bold": True})]], size=12, color="text", align="c",
                 margin=0, name=f"panel_{k}_value_{j+1}")
            text(s, X(bx - 20), Y(474), W(112), H(18), "{Group}", size=13, color="grey800", align="c", margin=0)
        lx, rx, ty = x0 + 51, x0 + 176, 262
        elbow(s, [(X(lx), Y(ya - 30)), (X(lx), Y(ty)), (X(rx), Y(ty)), (X(rx), Y(yb - 28))], "grey500", lw=1, r=0.0,
              arrow="tail", aw="med", al="med")
        box(s, X(x0 + 90), Y(ty - 10), W(50), H(20), fill="white", parts=[[("{n}x", {"bold": True})]], size=F(13),
            color="text", margin=0, name=f"panel_{k}_multiplier")


# d30 technology waves stepping up, with a mechanism inset ------------------------------------------------
def d30():
    s = slide(prs)
    header(s, "{Technology} will enable a step change in {process} with {mechanism}", "{source}", "{abbreviations}")
    f = Frame2((10, 160, 805, 615), body=(0.5, 1.1, 12.3, 5.6)); X, Y, W, H, D, F = f.X, f.Y, f.W, f.H, f.D, f.F
    text(s, X(10), Y(162), W(400), H(18), "{AXIS LABEL: YEAR WHEN THE TECHNOLOGY ENTERS}", size=F(12), color="text", margin=0)
    cols = [(70, "{era}"), (200, "{era}"), (322, "{era}"), (472, "{era}"), (609, "{era}"), (737, "{era}")]
    for x, lab in cols:
        text(s, X(x - 50), Y(186), W(100), H(18), lab, size=F(13), color="text", align="c", margin=0)
    for x in (130, 395):
        soft_line(s, X(x), Y(190), X(x), Y(600), "grey200", lw=1)
    steps = [(70, 397), (196, 362), (322, 315), (472, 290), (609, 262), (737, 232)]
    for i, (x, y) in enumerate(steps):
        text(s, X(x - 60), Y(y - 12), W(120), H(40), [[("{Wave}", {"bold": True})]], size=F(15), color="text", align="c",
             margin=0, name=f"wave_{i+1}")
        if 0 < i < 5:
            text(s, X(x - 65), Y(y + 18), W(130), H(32), "{(e.g., how)}", size=F(12), color="text", align="c", margin=0)
        if i < 5:
            nx, ny = steps[i + 1]
            elbow(s, [(X(x - 40), Y(y - 25)), (X(x - 40), Y(ny + 3)), (X(nx - 45), Y(ny + 3))], "accent500", lw=1.5,
                  r=0.0, arrow="tail", aw="med", al="med")
    # wave visuals
    dot(s, X(30), Y(436), D(12), "accent500"); box(s, *f.R(50, 427, 40, 18), line="accent500", lw=1)
    dot(s, X(110), Y(436), D(12), "grey200")
    soft_line(s, X(36), Y(436), X(50), Y(436), "accent500", lw=1, arrow="tail", aw="sm", al="sm")
    soft_line(s, X(90), Y(436), X(104), Y(436), "accent500", lw=1, arrow="tail", aw="sm", al="sm")
    random.seed(3)
    for i in range(12):
        dot(s, X(172 + random.uniform(0, 52)), Y(415 + random.uniform(0, 38)), D(10), "accent500")
    soft_line(s, X(160), Y(462), X(232), Y(462), "grey400", lw=0.75); soft_line(s, X(160), Y(462), X(160), Y(408), "grey400", lw=0.75)
    lay = [(418,), (392, 418, 444), (392, 418, 444), (418,)]
    for li in range(3):
        for ya in lay[li]:
            for yb in lay[li + 1]:
                soft_line(s, X(293 + li * 22), Y(ya), X(315 + li * 22), Y(yb), "grey300", lw=0.5)
    for layer, ys in enumerate(lay):
        for yy in ys:
            dot(s, X(293 + layer * 22), Y(yy), D(14), "accent500" if layer == 0 else "grey200")
    box(s, *f.R(408, 332, 120, 128), line="grey400", lw=0.75, name="inset_model")
    text(s, X(415), Y(340), W(60), H(16), "{Model}", size=F(11), color="text", margin=0)
    for x in (413, 476):
        box(s, *f.R(x, 371, 48, 62), line="grey400", lw=0.75, dash=True)
        text(s, X(x), Y(374), W(48), H(14), "{Part}", size=F(10), color="text", align="c", margin=0)
    for k, (y, lab) in enumerate(((306, "{Observe}"), (352, "{Plan}"), (400, "{Act}"))):
        rrect(s, X(567), Y(y), W(83), H(31), 0.05, fill="white", line="grey400", lw=0.75, parts=lab, size=F(12),
              color="text", name=f"loop_{k+1}")
        if k < 2:
            soft_line(s, X(608), Y(y + 31), X(608), Y(y + 46), "grey400", lw=0.75, arrow="tail", aw="sm", al="sm")
    elbow(s, [(X(650), Y(415)), (X(662), Y(415)), (X(662), Y(321)), (X(650), Y(321))], "grey400", lw=0.75, r=0.03,
          arrow="tail", aw="sm", al="sm")
    soft_line(s, X(608), Y(431), X(608), Y(447), "grey400", lw=0.75, arrow="tail", aw="sm", al="sm")
    rrect(s, X(562), Y(450), W(93), H(31), 0.05, fill="accent100", parts="{Final answer}", size=10, color="text", margin=0,
          name="loop_final")
    for i in range(18):
        hh = 6 + 30 * abs(math.sin(i * 0.7))
        soft_line(s, X(707 + i * 3.6), Y(410 - hh / 2), X(707 + i * 3.6), Y(410 + hh / 2), "grey200", lw=1)
    icon(s, X(737), Y(410), D(32), "white", fill="accent500", name="last_wave_icon")
    for k, (x, t) in enumerate(((70, None), (200, None), (322, None), (472, "{What it leverages}"),
                                (609, "{What it leverages}"), (737, "{What it leverages}")), 1):
        paras = ([[(t, {"bold": True})]] if t else []) + ["{What the systems do, in one or two lines}"]
        text(s, X(x - 60), Y(495), W(120), H(110), paras, size=11, color="text", align="c", anchor="b", margin=0,
             name=f"wave_text_{k}")


# d31 ranges by role family, under a roof with a progress ring ------------------------------------------------
def d31():
    s = slide(prs)
    header(s, "{Leading institutions} are setting big ambitions for {change}", "{source}")
    f = Frame2((15, 120, 820, 545), body=(0.5, 1.1, 12.3, 5.65)); X, Y, W, H, D, F = f.X, f.Y, f.W, f.H, f.D, f.F
    polyline(s, [(X(22), Y(253)), (X(259), Y(128)), (X(463), Y(253))], None, fill="grey100", close=True, name="roof")
    cx, cy, r = X(244), Y(192), D(44)
    c = box(s, cx - r, cy - r, 2 * r, 2 * r, line="grey200", lw=6, shape=MSO_SHAPE.OVAL)
    arc = [(cx + r * math.cos(math.radians(90 - a)), cy - r * math.sin(math.radians(90 - a))) for a in range(0, 64, 3)]
    a = polyline(s, arc, "accent500", lw=6, name="roof_ring"); round_caps(a)
    text(s, cx - 0.55, cy - 0.2, 1.1, 0.4, "{Top family}", size=F(13), color="text", align="c", anchor="m", margin=0,
         name="roof_label")
    soft_line(s, X(282), Y(163), X(465), Y(163), "grey400", lw=0.75)
    box(s, X(722), Y(114), W(90), H(26), fill="grey100", parts=[[("{Case example}", {"italic": True})]], size=11,
        color="text", margin=0, name="case_tag")
    text(s, X(473), Y(155), W(270), H(80), [[("{v}%–{v}%", {"bold": True})], "{What changes for this family}"],
         size=F(12.5), color="text", margin=0, name="roof_text")
    bars = [(262, 242, "accent700", "white"), (319, 340, "accent500", "white"), (376, 222, "accent900", "white"),
            (432, 299, "grey400", "white"), (489, 207, "grey600", "white")]
    for k, (y, w, fill, tc) in enumerate(bars, 1):
        box(s, *f.R(22, y, 441, 50), fill="grey100", name=f"family_{k}_track")
        box(s, *f.R(22, y, w - 22, 50), fill=fill, name=f"family_{k}_bar",
            parts="{Role family}", size=F(14), color=tc, align="l", margin=0.15)
        text(s, X(w + 12), Y(y), W(100), H(50), [[("{v}%–{v}%", {"bold": True})]], size=F(13), color="text",
             anchor="m", margin=0, name=f"family_{k}_range")
        text(s, X(475), Y(y + 3), W(330), H(46), "{What drives the change for this family}", size=F(12), color="text",
             anchor="m", margin=0, name=f"family_{k}_text")


# d32 iceberg: three layers with their share of effort ------------------------------------------------------
def d32():
    s = slide(prs)
    header(s, "{Scaling} is the hardest challenge", "{source}")
    f = Frame((5, 80, 820, 425)); X, Y, L, F = f.X, f.Y, f.L, f.F
    for y in (162, 260):
        soft_line(s, X(10), Y(y), X(820), Y(y), "grey200", lw=1)
    P = lambda pts: [(X(x), Y(y)) for x, y in pts]
    above = [(142, 260), (150, 228), (163, 180), (172, 162), (180, 140), (188, 113), (200, 135), (212, 152), (220, 172),
             (233, 182), (244, 168), (252, 195), (264, 215), (282, 238), (298, 260)]
    below = [(298, 260), (318, 300), (308, 345), (288, 378), (258, 403), (222, 428), (198, 405), (172, 385), (152, 345),
             (138, 300), (142, 260)]
    polyline(s, P(above), None, fill="accent500", close=True, name="iceberg_above")
    polyline(s, P(below), None, fill="accent900", close=True, name="iceberg_below")
    facets = [([(188, 113), (200, 135), (190, 150), (180, 140)], "accent200"),
              ([(180, 140), (190, 150), (172, 185), (163, 180), (172, 162)], "accent300"),
              ([(200, 135), (212, 152), (220, 172), (205, 190), (190, 150)], "accent700"),
              ([(244, 168), (252, 195), (240, 205), (233, 182)], "accent200"),
              ([(233, 182), (240, 205), (226, 230), (215, 205)], "accent400"),
              ([(150, 228), (163, 180), (172, 185), (178, 225), (160, 260), (142, 260)], "accent700"),
              ([(252, 195), (264, 215), (282, 238), (298, 260), (262, 260), (240, 205)], "accent700"),
              ([(205, 190), (226, 230), (215, 260), (190, 250)], "accent400"),
              ([(160, 260), (190, 250), (215, 260)], "accent700"),
              ([(142, 260), (160, 260), (170, 300), (152, 345), (138, 300)], "accent700"),
              ([(215, 260), (262, 260), (250, 300), (225, 290)], "accent700"),
              ([(262, 260), (298, 260), (318, 300), (290, 320), (250, 300)], "grey800"),
              ([(170, 300), (200, 330), (198, 405), (172, 385), (152, 345)], "accent700"),
              ([(250, 300), (290, 320), (288, 378), (258, 403), (240, 360)], "accent700"),
              ([(200, 330), (225, 290), (240, 360), (222, 428), (198, 405)], "grey800")]
    for pts, col in facets:
        polyline(s, P(pts), None, fill=col, close=True)
    for k, (y, lab) in enumerate(((112, "{Layer}"), (192, "{Layer}"), (310, "{Layer}")), 1):
        text(s, X(10), Y(y - 16), L(120), L(38), [[("{v}%", {"bold": True})]], size=F(24),
             color=("accent500", "accent700", "accent900")[k - 1], margin=0, name=f"layer_{k}_share")
        text(s, X(10), Y(y + 20), L(130), L(36), lab, size=F(12.5), color="text", margin=0, name=f"layer_{k}")
    text(s, X(362), Y(85), L(200), L(22), [[("{Model name}", {"bold": True})]], size=F(14), color="text", margin=0)
    text(s, X(580), Y(85), L(200), L(22), [[("{Capabilities}", {"bold": True})]], size=F(14), color="text", margin=0)
    for k, (y0, y1) in enumerate(((112, 158), (166, 256), (266, 410)), 1):
        c = soft_line(s, X(343), Y(y0 + 6), X(343), Y(y1 - 6), "grey400", lw=1)
        arrow_size(c, "tail", "med", "med"); arrow_size(c, "head", "med", "med")
        text(s, X(362), Y(y0), L(200), L(y1 - y0), ["{What this layer covers}"] + (["", "{Why it matters most}"] if k == 3 else []),
             size=F(12.5), color="text",
             anchor="t" if k != 2 else "m", margin=0, name=f"layer_{k}_text")
        text(s, X(580), Y(y0), L(235), L(y1 - y0), ["· {capability}", "· {capability}"] + (["· {capability}"] * (k - 1)),
             size=F(12.5), color="text", margin=0, name=f"layer_{k}_capabilities")


for fn in (d29, d30, d31, d32):
    fn()
prs.save(sys.argv[1])
print("saved")
