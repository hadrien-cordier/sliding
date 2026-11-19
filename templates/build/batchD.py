"""Measured rebuild, designs d13-d16."""
import math, sys
from lib2 import *

prs = new_deck()


# d13 roadmap with deep dive and keyed callouts (stretched to the 16:9 body) ------------------------
def d13():
    s = slide(prs)
    header(s, "{Acceleration roadmap} for {use cases}: {an example}", "{source}")
    f = Frame2((25, 100, 1080, 910)); X, Y, W, H, D, F = f.X, f.Y, f.W, f.H, f.D, f.F
    text(s, X(30), Y(103), W(70), H(38), [[("Months", {"bold": True})]], size=12, color="warm700", anchor="m", margin=0)
    for i in range(14):
        now = i < 2
        chevron(s, X(102 + i * 69.5), Y(103), W(72), H(38), H(12), first=(i == 0),
                fill="warm500" if now else "grey100", parts="{Mon}", size=11, color="white" if now else "grey600",
                margin=0, name=f"month_{i+1}")
    box(s, *f.R(102, 145, 833, 30), fill="warm50", parts="{Workstream 1}", size=F(16), color="grey600", margin=0,
        name="workstream_1")
    chevron(s, *f.R(102, 183, 972, 31), H(12), first=True, fill="warm100", parts="{Workstream 2}", size=F(16),
            color="grey600", margin=0, name="workstream_2")
    def key(x, y, k, col="second500"):
        box(s, X(x) - D(12), Y(y) - D(12), D(24), D(24), fill=col, shape=MSO_SHAPE.OVAL,
            parts=[[(k, {"bold": True})]], size=F(14), color="white", margin=0)
    key(101, 178, "A")
    swoosh(s, (X(70), Y(185)), (X(32), Y(200)), (X(38), Y(222)), (X(70), Y(232)), 0.02, 0.07, 0.17, 0.13, "second500")
    text(s, X(76), Y(222), W(200), H(34), [[("{Deep-dive}:", {"bold": True})]], size=F(20), color="second500",
         anchor="m", margin=0)
    box(s, *f.R(25, 275, 1047, 397), fill="grey100", name="deep_dive_panel")
    text(s, X(28), Y(360), W(88), H(30), [[("{Segment 1}", {"bold": True})]], size=12, color="second700", margin=0,
         name="lane_1_label")
    text(s, X(28), Y(568), W(88), H(30), [[("{Segment 2}", {"bold": True})]], size=12, color="accent700", margin=0,
         name="lane_2_label")
    P = lambda x, y, w, h, fill, lab, name, first=False: chevron(
        s, X(x), Y(y), W(w), H(h), W(24), first=first, fill=fill, parts=lab, size=F(14.5), color="text", margin=0.04,
        name=name)
    P(251, 288, 160, 164, "second100", "{Phase}", "lane_1_phase_1", True)
    P(409, 288, 180, 78, "second100", "{Parallel phase A}", "lane_1_phase_2")
    P(506, 375, 175, 77, "second100", "{Parallel phase B}", "lane_1_phase_3")
    P(605, 288, 175, 78, "second100", "{Phase}", "lane_1_phase_4")
    P(775, 288, 160, 164, "second100", "{Phase}", "lane_1_phase_5")
    P(922, 288, 151, 164, "second100", "{Phase}", "lane_1_phase_6")
    P(118, 499, 90, 161, "grey200", "{Phase}", "lane_2_phase_1", True)
    P(202, 499, 135, 78, "accent100", "{Parallel phase A}", "lane_2_phase_2")
    P(350, 499, 155, 78, "accent100", "{Phase}", "lane_2_phase_3")
    P(262, 586, 160, 77, "accent100", "{Parallel phase B}", "lane_2_phase_4")
    P(506, 497, 140, 165, "accent100", "{Phase}", "lane_2_phase_5")
    P(637, 497, 140, 165, "accent100", "{Phase}", "lane_2_phase_6")
    P(768, 497, 305, 165, "grey200", "{Next scope extension}", "lane_2_phase_7")
    for x in (128, 155):
        soft_line(s, X(x), Y(345 if x == 128 else 392), X(x), Y(497), "grey400", lw=1.25)
    elbow(s, [(X(155), Y(392)), (X(170), Y(392))], "grey400", lw=1.25)
    text(s, X(140), Y(318), W(105), H(36), "{Link to another use case}", size=F(12), color="grey600", margin=0)
    elbow(s, [(X(200), Y(390)), (X(245), Y(390))], "grey400", lw=1.25, arrow="tail", aw="sm", al="sm")
    for (a, b, c, d) in (((440, 392), (430, 430), (470, 435), (500, 422)), ((700, 438), (728, 428), (738, 402), (716, 382)),
                         ((210, 588), (200, 620), (230, 632), (255, 628)), ((440, 610), (465, 600), (470, 580), (460, 565))):
        curve(s, (X(a[0]), Y(a[1])), (X(b[0]), Y(b[1])), (X(c[0]), Y(c[1])), (X(d[0]), Y(d[1])), "second500", lw=2.75,
              arrow="tail", aw="lg", al="lg")
    key(182, 390, "C"); key(70, 556, "B"); key(412, 326, "D"); key(258, 497, "D")
    for (x, y) in ((598, 326), (343, 535)):
        box(s, X(x) - D(12), Y(y) - D(12), D(24), D(24), fill="accent500", shape=MSO_SHAPE.OVAL, name="iteration_badge")
        r = D(16); cx_, cy_ = X(x), Y(y)
        arc = [(cx_ + r * math.cos(math.radians(a)), cy_ - r * math.sin(math.radians(a))) for a in range(200, 30, -10)]
        c = polyline(s, arc, "second500", lw=1.25); round_caps(c); arrow_size(c, "tail", "sm", "sm")
    for (x, y) in ((805, 305), (950, 305), (752, 345), (548, 400), (535, 515), (665, 515), (482, 525)):
        box(s, X(x) - D(11), Y(y) - D(11), D(22), D(22), fill="cat6", shape=MSO_SHAPE.OVAL, name="reuse_badge")
    text(s, X(28), Y(690), W(250), H(30), [[("Key callouts", {"bold": True})]], size=F(20), color="second500", margin=0)
    marks = [("", "accent500"), ("A", "second500"), ("B", "second500"), ("C", "second500"), ("D", "second500"), ("", "cat6")]
    for k, (m, col) in enumerate(marks):
        x = 28 + k * 178
        key(x + 12, 748, m, col)
        text(s, X(x), Y(768), W(160), H(135), "{What this marker means on the roadmap, in one or two sentences}",
             size=F(12.5), color="grey600", margin=0, name=f"callout_{k+1}")


# d14 small multiples of bridges, drawn as shapes (stretched) ------------------------------------
def d14():
    s = slide(prs)
    header(s, "{Innovation} lets {institutions} extend {the perimeter of their business}", "{sources}",
           "{definitions}; {projection method}")
    f = Frame2((20, 110, 860, 520)); X, Y, W, H, D, F = f.X, f.Y, f.W, f.H, f.D, f.F
    base = 395
    for x in (303, 595):
        soft_line(s, X(x), Y(115), X(x), Y(505), "grey200", lw=1)
    shades = ["accent100", "accent300", "accent700", "accent900"]
    for k, x0 in enumerate((25, 318, 610)):
        w0 = 264 if k < 2 else 241
        rrect(s, *f.R(x0, 119, w0, 61), H(14), fill="grey100", name=f"segment_{k+1}_head")
        icon(s, X(x0 + 40), Y(150), D(40), "accent700", name=f"segment_{k+1}_icon")
        text(s, X(x0 + 72), Y(125), W(w0 - 80), H(50), [[("{Segment}", {"bold": True})]], size=F(15), anchor="m",
             margin=0, name=f"segment_{k+1}")
        text(s, X(x0), Y(196), W(w0), H(20), "{MEASURE (UNIT)}", size=F(13), color="grey600", align="c", margin=0)
        if k < 2:
            cats = [(32, 21, 350, "{v}"), (88, 21, 249, "{v}"), (138, 28, None, None), (184, 21, None, None), (233, 21, 249, "{v}")]
            for i, (cx, bw, top, lab) in enumerate(cats):
                xx = x0 + cx
                if top is not None:
                    box(s, X(xx), Y(top), W(bw), H(base - top), fill="grey200", name=f"segment_{k+1}_bar_{i+1}")
                    text(s, X(xx - 20), Y(top - 22), W(bw + 40), H(20), [[(lab, {"bold": True})]], size=F(13),
                         align="c", margin=0)
                    if i in (0, 1, 4):   # axis break on the tall bars
                        polyline(s, [(X(xx - 3), Y(375)), (X(xx + bw + 3), Y(368)), (X(xx + bw + 3), Y(374)), (X(xx - 3), Y(381))],
                                 None, fill="white", close=True)
            box(s, X(x0 + 138), Y(249), W(21), H(56), fill="negative_bg", name=f"segment_{k+1}_erosion")
            ys = [305, 290, 272, 258, 249]
            for j in range(4):
                box(s, X(x0 + 184), Y(ys[j + 1]), W(21), H(ys[j] - ys[j + 1]), fill=shades[j],
                    name=f"segment_{k+1}_lever_{j+1}_bar")
            for (xa, xb, y) in ((x0 + 109, x0 + 138, 249), (x0 + 159, x0 + 184, 305), (x0 + 205, x0 + 233, 249)):
                soft_line(s, X(xa), Y(y), X(xb), Y(y), "grey400", lw=0.75, dash=True)
            for i, (cx, lab) in enumerate(((42, "{Start}"), (98, "{BaU}"), (148, "{Erosion}"), (194, "{New levers}"),
                                           (243, "{End}"))):
                text(s, X(x0 + cx - 30), Y(base + 6), W(60), H(40), lab, size=F(11), color="grey600", align="c", margin=0)
            for j in range(4):
                lx, ly = x0 + (j % 2) * 120, 448 + (j // 2) * 18
                box(s, X(lx), Y(ly), W(10), H(10), fill=shades[j])
                text(s, X(lx + 16), Y(ly - 4), W(100), H(18), "{Lever}", size=F(12), color="grey600", margin=0,
                     name=f"segment_{k+1}_legend_{j+1}")
        else:
            for i, (xx, top, lab, cat) in enumerate(((618, 283, "{v}", "{Start}"), (749, 249, "{v}", "{End}"))):
                box(s, X(xx), Y(top), W(81), H(base - top), fill="grey200", name=f"segment_3_bar_{i+1}")
                text(s, X(xx), Y(top - 22), W(81), H(20), [[(lab, {"bold": True})]], size=F(13), align="c", margin=0)
                text(s, X(xx), Y(base + 6), W(81), H(20), cat, size=F(11), color="grey600", align="c", margin=0)


# d15 spotlight: case trajectory and its drivers ---------------------------------------------------
def d15():
    s = slide(prs)
    header(s, "{Lever} led to a {multiple} of {metric} for {actor}", "{sources}", "{data definitions}")
    rrect(s, 0.45, 1.1, 12.4, 5.65, 0.2, fill="grey100", name="spotlight_panel")
    icon(s, 0.95, 1.7, 0.6, "accent700", fill="accent300", name="spotlight_icon")
    text(s, 1.4, 1.4, 4.2, 0.62, [[("SPOTLIGHT", {"bold": True, "color": "accent500"})],
                                  [("{Spotlight title}", {"bold": True})]], size=11, margin=0, name="spotlight_title")
    text(s, 6.85, 1.32, 5.75, 0.9, "{Two sentences: what the actor achieved, and the model that drove it}",
         size=10.5, color="grey600", margin=0, name="spotlight_intro")
    text(s, 0.75, 2.42, 5.5, 0.25, "{MEASURE (UNIT)}", size=9, color="grey600", margin=0, name="measure_label")
    vals = [1.8, 2.1, 2.4, 3.2, 4.0, 4.9, 5.3, 5.7, 6.7]
    x0, x1, yb, yt, vmax = 1.05, 6.55, 6.25, 3.35, 7.0
    px = lambda i: x0 + i * (x1 - x0) / (len(vals) - 1)
    py = lambda v: yb - v / vmax * (yb - yt)
    soft_line(s, 0.95, yb, 6.75, yb, "grey400", lw=0.75); soft_line(s, 0.95, yt - 0.2, 0.95, yb, "grey400", lw=0.75)
    for v in (0, 2, 4, 6):
        text(s, 0.45, py(v) - 0.1, 0.42, 0.2, "{tick}", size=8, color="grey600", align="r", margin=0)
    for i, v in enumerate(vals):
        text(s, px(i) - 0.3, yb + 0.05, 0.6, 0.2, "{yr}", size=8, color="grey600", align="c", margin=0)
        text(s, px(i) - (0.2 if i == 0 else 0.35), py(v) - 0.27, 0.7, 0.22, [[("{v}", {"bold": True})]], size=9, color="text", align="c",
             margin=0, name=f"point_{i+1}_label")
    polyline(s, [(px(i), py(v)) for i, v in enumerate(vals)], "accent500", lw=1.75, name="trend_line")
    soft_line(s, 0.95, 2.95, px(8), 2.95, "grey400", lw=0.75); soft_line(s, 0.95, 2.95, 0.95, 3.12, "grey400", lw=0.75)
    soft_line(s, px(8), 2.95, px(8), py(vals[-1]) - 0.36, "grey400", lw=0.75, arrow="tail", aw="sm", al="sm")
    rrect(s, 3.6, 2.865, 0.45, 0.17, 0.085, fill="accent300", parts=[[("{n}x", {"bold": True})]], size=8, color="text",
          margin=0, name="multiplier")
    rrect(s, 7.35, 2.75, 5.25, 3.75, 0.14, fill="grey200", name="drivers_panel")
    t = box(s, 7.1, 4.42, 0.4, 0.42, fill="grey200", shape=MSO_SHAPE.ISOSCELES_TRIANGLE)
    t.rotation = 270
    for k in range(3):
        y = 3.15 + k * 1.05
        icon(s, 8.0, y + 0.38, 0.58, "white", fill="grey400", name=f"driver_{k+1}_icon")
        text(s, 8.5, y, 4.0, 1.05, [[("{Driver stated as a claim, on two lines at most}", {"bold": True})],
                                    "· {proof point}", "· {proof point}"], size=10.5, color="text", margin=0,
             name=f"driver_{k+1}")


# d16 platform between two sides ---------------------------------------------------------------------
def d16():
    s = slide(prs)
    header(s, "{Platform} gives {actors} a role in {ecosystem}", "{source}")
    f = Frame((35, 85, 835, 525)); X, Y, L, F = f.X, f.Y, f.L, f.F
    pw = 170
    for (x, y, h, side, k) in ((-52, 92, 198, "left", 1), (753, 92, 198, "right", 1), (-52, 322, 195, "left", 2),
                               (753, 322, 195, "right", 2)):
        top_round(s, X(x), Y(y), L(pw), L(30), L(16), fill="accent700", parts=[[("{App name}", {"bold": True})]],
                  size=F(14), color="white", margin=0, name=f"{side}_app_{k}_head")
        open_frame(s, X(x), Y(y), L(pw), L(h), L(16), "text", lw=3.5, name=f"{side}_app_{k}")
        def blk(dx, dy, w, h, fill="grey200", r=0):
            (rrect(s, X(x + dx), Y(y + dy), L(w), L(h), L(r), fill=fill) if r else box(s, X(x + dx), Y(y + dy), L(w), L(h), fill=fill))
        if (side, k) == ("left", 1):
            blk(2, 32, pw - 4, 30, "accent100"); blk(18, 40, pw - 36, 14, "white", 7); blk(2, 74, pw - 4, 54)
            for i in range(5):
                dot(s, X(x + pw / 2 - 26 + i * 13), Y(y + 143), L(6), "accent500" if i == 2 else "grey400")
            for i in range(3):
                blk(2 + i * 57, 158, 52, 40)
        elif (side, k) == ("right", 1):
            blk(6, 44, 44, 72); blk(56, 44, pw - 62, 72, "accent100")
            for i in range(3):
                dot(s, X(x + 30 + i * 55), Y(y + 160), L(42), "grey200")
        elif side == "left":
            for dy in (50, 114):
                blk(16, dy, pw - 32, 53, r=2); blk(pw - 62, dy + 36, 40, 12, "accent100", 6)
            blk(16, 179, pw - 32, 16)
        else:
            blk(14, 50, 66, 53); blk(88, 50, 68, 53)
            for i, hh in enumerate((55, 20, 37, 30, 55)):
                blk(14 + i * 30, 178 - hh, 18, hh, "accent100")
    cx, cy, r = 431, 300, 143
    box(s, X(cx - r), Y(cy - r), L(2 * r), L(2 * r), fill="accent100", shape=MSO_SHAPE.OVAL, name="hub")
    text(s, X(cx - 110), Y(cy - 80), L(220), L(110), "{Open network for the ecosystem}", size=F(23), color="text",
         align="c", anchor="m", margin=0, name="hub_title")
    text(s, X(cx - 80), Y(cy + 38), L(160), L(40), "{Key fact about ownership}", size=F(13), color="text", align="c",
         margin=0, name="hub_fact")
    ra = r + 16; dy = 96; dx = math.sqrt(ra * ra - dy * dy)
    for side in (-1, 1):
        half = math.degrees(math.atan2(dy, dx))
        a0, a1 = (math.radians(180 - half), math.radians(180 + half)) if side < 0 else (math.radians(-half), math.radians(half))
        pts = [(X(cx + ra * math.cos(a0 + (a1 - a0) * t / 30)), Y(cy - ra * math.sin(a0 + (a1 - a0) * t / 30)))
               for t in range(31)]
        c = polyline(s, pts, "grey400", lw=2); round_caps(c)
        for y in (cy - dy, cy + dy):
            c = soft_line(s, X(cx + side * dx), Y(y), X(cx + side * 205), Y(y), "grey400", lw=2)
            arrow_size(c, "tail", "med", "med", "arrow")
        xi = cx + side * 255
        for k, (iy, ly, lab) in enumerate(((128, 160, "{Side A actors}"), (283, 315, "{Intermediary}"),
                                            (492, 428, "{Side B actors}"))):
            icon(s, X(xi), Y(iy), L(42), "text", name=f"{'left' if side < 0 else 'right'}_actor_{k+1}_icon")
            text(s, X(xi - 46), Y(ly), L(92), L(36), [[(lab, {"bold": True})]], size=12, align="c", margin=0,
                 name=f"{'left' if side < 0 else 'right'}_actor_{k+1}")
    text(s, X(cx - 80), Y(cy + r + 12), L(160), L(66), [[("{Services offered}", {"bold": True})], "· {service}", "· {service}"],
         size=F(13), align="c", margin=0, name="services")


for fn in (d13, d14, d15, d16):
    fn()
prs.save(sys.argv[1])
print("saved")
