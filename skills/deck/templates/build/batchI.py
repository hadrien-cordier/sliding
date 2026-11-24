"""Measured rebuild, designs d33-d36."""
import math, random, sys
from lib2 import *

prs = new_deck()


# d33 selection criteria, value x realisability matrix, numbered list -------------------------------
def d33():
    s = slide(prs)
    header(s, "{Actor} embraces a {selective approach} to ensure {boldness and focus}", "{source}", "{Case study}")
    f = Frame((10, 125, 820, 465)); X, Y, L, F = f.X, f.Y, f.L, f.F
    text(s, X(45), Y(130), L(260), L(22), [[("{Criteria}", {"bold": True})]], size=F(15), color="text", margin=0)
    soft_line(s, X(16), Y(160), X(16), Y(440), "grey400", lw=1.25, arrow="tail", aw="med", al="med")
    for k, y in enumerate((160, 233, 306, 379), 1):
        rrect(s, X(32), Y(y), L(286), L(60), 0.08, fill="grey100", parts="{Criterion} (e.g., {threshold})", size=F(13),
              color="text", align="l", margin=0.12, name=f"criterion_{k}")
    text(s, X(352), Y(130), L(260), L(22), [[("{Identification}", {"bold": True})]], size=F(15), color="text", margin=0)
    quads = [((352, 160, 95, 92), "accent500", "white", "{Quadrant}", "q_high"),
             ((352, 252, 95, 92), "accent200", "text", "{Quadrant}", "q_long"),
             ((447, 160, 148, 184), "accent700", "white", "{Selected opportunities, with the logic that unites them}", "q_selected"),
             ((352, 344, 143, 92), "grey300", "text", "{Quadrant}", "q_low"),
             ((495, 344, 100, 92), "grey100", "text", "{Quadrant}", "q_quick")]
    for (x, y, w, h), fill, tc, t, nm in quads:
        box(s, X(x), Y(y), L(w), L(h), fill=fill, parts=t, size=F(12.5), color=tc, align="l", anchor="t", margin=0.08,
            name=nm)
    t = text(s, X(306), Y(185), L(60), L(18), "{AXIS Y}", size=F(11.5), color="text", align="c", margin=0)
    t.rotation = 270
    text(s, X(470), Y(444), L(125), L(18), "{AXIS X}", size=F(11.5), color="text", align="r", margin=0)
    soft_line(s, X(600), Y(155), X(600), Y(440), "accent300", lw=1.5)
    soft_line(s, X(595), Y(252), X(600), Y(252), "accent300", lw=1.25)
    for k in range(10):
        y = 160 + k * 27.6
        text(s, X(602), Y(y), L(22), L(20), [[(str(k + 1), {"bold": True})]], size=F(12.5), color="accent700",
             align="r", margin=0, name=f"opportunity_{k+1}_number")
        text(s, X(630), Y(y), L(188), L(20), "{Opportunity}", size=F(12.5), color="text", margin=0,
             name=f"opportunity_{k+1}")


# d34 hub-and-spoke networks connected by a central exchange --------------------------------------------
def d34():
    s = slide(prs)
    header(s, "Should {actors} play a bigger role in {ecosystem}?", "{source}")
    f = Frame((5, 85, 820, 490)); X, Y, L, F = f.X, f.Y, f.L, f.F
    random.seed(5)
    hubs = [(100, 255, "accent500", True), (300, 155, "accent500", True), (185, 405, "accent500", True),
            (500, 155, "accent100", False), (685, 220, "accent100", False), (650, 390, "accent100", False)]
    ex, ey = 405, 305
    for hx, hy, col, linked in hubs:
        if linked:
            soft_line(s, X(hx), Y(hy), X(ex), Y(ey), "accent500", lw=1.5)
    for k, (hx, hy, col, linked) in enumerate(hubs, 1):
        n = 16
        cust = []
        if linked:
            base = 40 if k != 2 else 175
            cust = [base + 32 * j for j in range(3)]
        for i in range(n):
            a_deg = 360 * i / n + 11
            if any(abs((a_deg - c + 180) % 360 - 180) < 20 for c in cust):
                continue
            rr = 54 if i % 2 else 70
            a = math.radians(a_deg)
            px, py = hx + rr * math.cos(a), hy - rr * math.sin(a)
            soft_line(s, X(hx), Y(hy), X(px), Y(py), "grey400", lw=0.5)
            box(s, X(px) - L(8), Y(py) - L(8), L(16), L(16), fill="white", line="grey600", lw=0.75,
                shape=MSO_SHAPE.OVAL if i % 3 else MSO_SHAPE.RECTANGLE)
        for c in cust:
            a = math.radians(c)
            px, py = hx + 58 * math.cos(a), hy - 58 * math.sin(a)
            soft_line(s, X(hx), Y(hy), X(px), Y(py), "accent500", lw=2)
            box(s, X(px) - L(13), Y(py) - L(13), L(26), L(26), fill="accent700", shape=MSO_SHAPE.OVAL)
        if k == 2:
            soft_line(s, X(hx), Y(hy), X(hx), Y(hy + 55), "accent500", lw=2)
            box(s, X(hx) - L(18), Y(hy + 55) - L(18), L(36), L(36), fill="accent500", shape=MSO_SHAPE.OVAL, name="offer")
            text(s, X(hx - 40), Y(hy + 75), L(80), L(18), [[("{Offer}", {"bold": True})]], size=12, color="text",
                 align="c", margin=0)
        box(s, X(hx) - L(28), Y(hy) - L(28), L(56), L(56), fill=col, shape=MSO_SHAPE.OVAL, name=f"network_{k}_hub")
        icon(s, X(hx), Y(hy), L(28), "white" if linked else "accent700", name=f"network_{k}_icon")
    box(s, X(ex) - L(62), Y(ey) - L(62), L(124), L(124), fill="accent500", shape=MSO_SHAPE.OVAL, name="exchange",
        parts=[[("{Exchange}", {"bold": True})]], size=14, color="white", margin=0.0)
    text(s, X(300), Y(395), L(260), L(65), ["· {More X, less Y}", "· {More X, less Y}", "· {More X, less Y}"],
         size=F(13), color="text", margin=0, name="shifts")


# d35 table with category column, dashed row rules and a bold growth column ----------------------------
def d35():
    s = slide(prs)
    header(s, "{Demand} is coming from a variety of {sectors}", "{sources}", "{definitions}")
    f = Frame2((15, 85, 1350, 715)); X, Y, W, H, D, F = f.X, f.Y, f.W, f.H, f.D, f.F
    cols = [(18, 344, "{Category}", "l"), (367, 503, "{Key segments}", "c"), (875, 230, "{Measure (unit)}", "c"),
            (1110, 236, "{Growth (unit)}", "c")]
    for k, (x, w, lab, al) in enumerate(cols, 1):
        rrect(s, X(x), Y(91), W(w), H(58), 0.1, fill="accent500", parts=[[(lab, {"bold": True})]], size=F(19),
                  color="white", align=al, margin=0.1, name=f"head_{k}")
    for r in range(9):
        y0 = 152 + r * 62
        for k, (x, w, lab, al) in enumerate(cols, 1):
            st = {"bold": True} if k in (1, 4) else {}
            col = "accent500" if k == 1 else ("text" if k == 4 else "grey600")
            text(s, X(x + (8 if k == 1 else 0)), Y(y0), W(w - 8), H(60), [[("{Category}" if k == 1 else "{value}", st)]],
                 size=F(17.5), color=col, align=al, anchor="m", margin=0, name=f"cell_{r+1}_{k}")
        c = soft_line(s, X(18), Y(y0 + 61), X(1346), Y(y0 + 61), "accent300", lw=1, name=f"rule_{r+1}")
        c.line.dash_style = MSO_LINE_DASH_STYLE.DASH


# d36 concentric wheel: four outer arcs (how), inner ring of areas (what), core (why) ---------------------
def d36():
    s = slide(prs)
    header(s, "{Effective action} requires a {cross-sector, systems-based} approach", "{source}")
    f = Frame((5, 125, 1190, 700)); X, Y, L, F = f.X, f.Y, f.L, f.F
    cx, cy = X(315), Y(400)

    def band(r0, r1, a0, a1, fill, name):
        n = 50
        outer = [(cx + L(r1) * math.cos(math.radians(a0 + (a1 - a0) * t / n)), cy - L(r1) * math.sin(math.radians(a0 + (a1 - a0) * t / n)))
                 for t in range(n + 1)]
        inner = [(cx + L(r0) * math.cos(math.radians(a1 + (a0 - a1) * t / n)), cy - L(r0) * math.sin(math.radians(a1 + (a0 - a1) * t / n)))
                 for t in range(n + 1)]
        return polyline(s, outer + inner, "white", lw=3, fill=fill, close=True, name=name)
    ring = box(s, cx - L(250), cy - L(250), L(500), L(500), line="accent300", lw=1, shape=MSO_SHAPE.OVAL, dash=True)
    band(195, 236, 93, 208, "accent900", "arc_1")
    band(195, 236, -28, 87, "accent700", "arc_2")
    band(195, 236, 214, 326, "accent500", "arc_3")
    labels = [(150, "① {Pillar}", -60), (32, "② {Pillar}", 58), (268, "③ {Pillar}", 0)]
    for ang, lab, rot in labels:
        rx = cx + L(216) * math.cos(math.radians(ang)); ry = cy - L(216) * math.sin(math.radians(ang))
        t = text(s, rx - 0.75, ry - 0.16, 1.5, 0.32, [[(lab, {"bold": True})]], size=F(21), color="white", align="c",
                 anchor="m", margin=0)
        t.rotation = rot
    text(s, X(215), Y(645), L(200), L(36), [[("④ {Enabler}", {"bold": True})]], size=F(24), color="second500", align="c",
         margin=0, name="enabler")
    box(s, cx - L(190), cy - L(190), L(380), L(380), fill="white", shape=MSO_SHAPE.OVAL, name="areas_ring")
    box(s, cx - L(105), cy - L(105), L(210), L(210), fill="white", line="grey200", lw=1, shape=MSO_SHAPE.OVAL, name="core")
    for i in range(10):
        a = math.radians(90 - 18 + i * 36)
        soft_line(s, cx + L(108) * math.cos(a), cy - L(108) * math.sin(a), cx + L(180) * math.cos(a), cy - L(180) * math.sin(a),
                  "grey200", lw=0.75)
        a2 = math.radians(90 + i * 36)
        tx, ty = cx + L(150) * math.cos(a2), cy - L(150) * math.sin(a2)
        text(s, tx - 0.45, ty - 0.17, 0.9, 0.34, [[("{Area}", {"bold": True})]], size=F(14), color="grey600", align="c",
             anchor="m", margin=0, name=f"area_{i+1}")
    text(s, cx - L(95), cy - L(75), L(190), L(70), [[("{Why this is needed, in one sentence}", {"bold": True})]],
         size=F(16), color="warm700", align="c", margin=0, name="core_text")
    for k in range(3):
        icon(s, cx + L(-50 + k * 50), cy + L(40), L(30), "warm700", name=f"core_icon_{k+1}")
        text(s, cx + L(-75 + k * 50), cy + L(58), L(50), L(18), "{Type}", size=F(11), color="warm700", align="c", margin=0)
    callouts = [(470, 248, "accent700", "{How}", "{question on the pillars?}"),
                (468, 398, "grey800", "{What}", "{question on the areas?}"),
                (330, 492, "warm700", "{Why}", "{question on the core?}")]
    for k, (ax, ay, col, q, rest) in enumerate(callouts, 1):
        dot(s, X(ax), Y(ay), L(8), col)
        soft_line(s, X(ax), Y(ay), X(600), Y(ay), col, lw=1.25)
        text(s, X(607), Y(ay - 15), L(150), L(80), [[(q, {"bold": True, "size": F(24), "color": col})], rest],
             size=F(19), color="grey600", margin=0, name=f"callout_{k}")
    c = soft_line(s, X(770), Y(120), X(770), Y(685), "grey300", lw=1); c.line.dash_style = MSO_LINE_DASH_STYLE.DASH
    chevron(s, X(770) - 0.02, Y(400) - 0.12, 0.12, 0.24, 0.1, fill="white", line="grey300", lw=1)
    for k, (y, col) in enumerate(((157, "accent700"), (290, "accent700"), (423, "accent500"), (556, "second500")), 1):
        box(s, X(817), Y(y - 12), L(26), L(26), fill="white", line=col, lw=1.5, shape=MSO_SHAPE.OVAL,
            parts=[[(str(k), {"bold": True})]], size=F(14), color=col, margin=0)
        text(s, X(860), Y(y - 12), L(290), L(110), [[("{Pillar}. ", {"bold": True, "color": col}),
                                                    ("{What it takes, in two or three lines}", {})]],
             size=13, color="grey600", margin=0, name=f"pillar_{k}_text")


for fn in (d33, d34, d35, d36):
    fn()
prs.save(sys.argv[1])
print("saved")
