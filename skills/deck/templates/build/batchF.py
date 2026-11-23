"""Measured rebuild, designs d21-d24."""
import math, sys
from lib2 import *

prs = new_deck()


def arc_band(s, cx, cy, r0, r1, a0, a1, fill, name=None, n=40):
    """Ring segment between radii r0<r1, from angle a0 to a1 (degrees, counter-clockwise positive, y up)."""
    outer = [(cx + r1 * math.cos(math.radians(a0 + (a1 - a0) * t / n)), cy - r1 * math.sin(math.radians(a0 + (a1 - a0) * t / n)))
             for t in range(n + 1)]
    inner = [(cx + r0 * math.cos(math.radians(a1 + (a0 - a1) * t / n)), cy - r0 * math.sin(math.radians(a1 + (a0 - a1) * t / n)))
             for t in range(n + 1)]
    return polyline(s, outer + inner, None, fill=fill, close=True, name=name)


# d21 process container pointing to impact ----------------------------------------------------------------
def d21():
    s = slide(prs)
    header(s, "{Automating process} cuts {time} and {effort}", "{source}", "{abbreviations}")
    f = Frame((5, 95, 1320, 600), body=(0.5, 1.15, 12.3, 5.0)); X, Y, L, F = f.X, f.Y, f.L, f.F
    pts = [(X(12), Y(103)), (X(980), Y(103)), (X(1052), Y(350)), (X(980), Y(595)), (X(12), Y(595))]
    c = polyline(s, pts, "accent300", lw=1.75, close=True, name="process_container")
    rrect(s, *f.R(27, 123, 943, 78), L(6), fill="accent100", name="architecture_band")
    icon(s, X(100), Y(162), L(50), "accent500", name="architecture_icon")
    text(s, X(150), Y(132), L(240), L(60), [[("{Solution architecture}", {"bold": True})]], size=F(21), color="accent500",
         anchor="m", margin=0)
    text(s, X(412), Y(132), L(540), L(60), "{One line on the architecture}", size=F(17), color="text", anchor="m",
         margin=0, name="architecture_text")
    for k, cx in enumerate((176, 508, 842), 1):
        text(s, X(cx - 120), Y(222), L(240), L(32), [[("{Step verb}", {"bold": True})]], size=F(21), color="accent500",
             align="c", margin=0, name=f"step_{k}")
        icon(s, X(cx), Y(310), L(100), "white", fill="accent500", name=f"step_{k}_icon")
    for xa, xb in ((238, 318), (368, 448), (570, 650), (700, 780)):
        c = soft_line(s, X(xa), Y(312), X(xb), Y(312), "accent300", lw=1.25)
        c.line.dash_style = MSO_LINE_DASH_STYLE.SQUARE_DOT
    for x in (343, 675):
        chevron(s, X(x) - 0.12, Y(312) - 0.2, 0.24, 0.4, 0.14, fill="accent500")
    for k, x in enumerate((58, 375, 711), 1):
        text(s, X(x), Y(398), L(280), L(175),
             ["{What happens in this step}", "", "• {item}", "• {item}", "• {item}"], size=F(17), color="grey600",
             margin=0, name=f"step_{k}_text")
        for para in s.shapes[-1].text_frame.paragraphs:
            para.line_spacing = 1.15
    text(s, X(1100), Y(118), L(200), L(28), [[("{Impact}", {"bold": True})]], size=F(20), color="accent500", align="c",
         margin=0)
    for k, cy in enumerate((205, 410), 1):
        box(s, X(1150), Y(cy - 50), L(100), L(100), fill="accent700", shape=MSO_SHAPE.OVAL,
            parts=[[("x%", {"bold": True})]], size=F(30), color="white", margin=0, name=f"kpi_{k}")
        text(s, X(1080), Y(cy + 60), L(240), L(50), "{what the figure measures}", size=F(17), color="text", align="c",
             margin=0, name=f"kpi_{k}_label")


# d22 value migrating from a large pool to focused players ------------------------------------------------
def d22():
    s = slide(prs)
    header(s, "{Value migration} to {focused models} is set to accelerate", "{source}")
    f = Frame((0, 165, 1196, 835), body=(0.5, 1.3, 12.3, 5.65)); f.ox = 0.5; X, Y, L, F = f.X, f.Y, f.L, f.F
    text(s, 0.5, 1.0, 6.0, 0.28, [[("{MEASURE (UNIT), YEAR}", {"bold": True})]], size=11, color="grey800", margin=0,
         name="measure_label")
    cx, cy, R = 0, 1080, 650
    arc = [(X(cx + R * math.cos(math.radians(a))), Y(cy - R * math.sin(math.radians(a)))) for a in
           [90 - i * (90 - math.degrees(math.asin(245 / R))) / 40 for i in range(41)]]
    polyline(s, [(X(0), Y(835))] + arc + [(X(602), Y(835))], None, fill="accent500", close=True, name="incumbent_pool")
    icon(s, X(107), Y(620), L(90), "white", name="incumbent_icon")
    text(s, X(5), Y(690), L(230), L(95), [[("{Incumbents}", {"size": F(30)})], [("{value}", {"bold": True})]],
         size=F(28), color="white", align="c", margin=0, name="incumbent_label")
    bubbles = [(32, 311, 11, 0, None), (148, 300, 32, 18, (143, 207)), (299, 316, 55, 24, (359, 258)),
               (446, 383, 60, 26, (525, 348)), (597, 494, 75, 30, (696, 469)), (801, 694, 140, 56, (963, 678))]
    for k, (bx, by, r, fs, lab) in enumerate(bubbles, 1):
        b = box(s, X(bx - r), Y(by - r), L(2 * r), L(2 * r), fill="accent500", shape=MSO_SHAPE.OVAL, name=f"player_{k}")
        b.fill.gradient(); b.fill.gradient_angle = 45
        st = b.fill.gradient_stops
        st[0].color.rgb = C("accent500"); st[0].position = 0.45
        st[1].color.rgb = C("accent100"); st[1].position = 1.0
        if fs:
            text(s, X(bx - r), Y(by - fs * 0.7), L(2 * r), L(fs * 1.4), [[("{$v}", {"bold": True})]], size=F(fs),
                 color="white", align="c", anchor="m", margin=0, name=f"player_{k}_value")
        if lab:
            text(s, X(lab[0]), Y(lab[1]), L(240), L(60), "{Type of player}", size=F(21), color="text", margin=0,
                 name=f"player_{k}_label")
    text(s, X(5), Y(178), L(120), L(100), ["{Type of", "player}", [("{$v}", {"bold": True, "color": "accent500"})]],
         size=F(21), color="text", margin=0, name="player_1_label")
    for (a, b) in (((25, 415), (25, 335)), ((128, 405), (130, 345)), ((245, 455), (255, 375)), ((370, 520), (385, 440)),
                   ((497, 630), (520, 555)), ((608, 790), (640, 720))):
        mx = (a[0] + b[0]) / 2 - 12
        c = curve(s, (X(a[0]), Y(a[1] + 12)), (X(mx - 14), Y(a[1] - 30)), (X(mx - 6), Y(b[1] + 22)), (X(b[0]), Y(b[1] - 4)),
                  "grey300", lw=1.4)
        arrow_size(c, "tail", "med", "med", "arrow")


# d23 radial bars: growth by segment ---------------------------------------------------------------------
def d23():
    s = slide(prs)
    header(s, "{Measure} of {selected top performers} by {segment}", "{sources}", "{definition of top performers}")
    f = Frame((10, 120, 545, 650)); X, Y, L, F = f.X, f.Y, f.L, f.F
    text(s, X(30), Y(128), L(200), L(24), "{MEASURE (UNIT)}", size=F(15), color="grey600", margin=0)
    cx, cy = X(40), Y(385)
    a0 = 95
    rings = [("grey400", 0.05), ("accent150", 0.20), ("accent200", 0.31), ("accent500", 0.51), ("accent700", 0.75),
             ("accent900", 0.86)]
    arc_band(s, cx, cy, L(93 + 5 * 20), L(93 + 5 * 20 + 19), a0 - 190 * 0.86, a0 - 190, "grey100", name="track")
    for i, (col, share) in enumerate(rings):
        r0 = L(93 + i * 20); r1 = r0 + L(20)
        a1 = a0 - 190 * share
        arc_band(s, cx, cy, r0, r1, a0, a1, col, name=f"ring_{i+1}")
        for a in range(int(a0) - 19, int(a1), -19):
            ang = math.radians(a)
            soft_line(s, cx + r0 * math.cos(ang), cy - r0 * math.sin(ang), cx + r1 * math.cos(ang),
                      cy - r1 * math.sin(ang), "accent900" if i >= 3 else "grey400", lw=0.5)
    ends = [(35, 160), (90, 215), (140, 267), (180, 390), (157, 545), (118, 618)]
    label_y = [160, 215, 267, 393, 573, 620]
    ring_end = []
    for i, (col, share) in enumerate(rings):
        rm = L(93 + i * 20 + 9.5); a1 = math.radians(a0 - 190 * share)
        ring_end.append((cx + rm * math.cos(a1), cy - rm * math.sin(a1)))
    label_y = [148, 203, 255, 393, 573, 620]
    for i, (ex, ey) in enumerate(ring_end):
        ly = Y(label_y[i])
        kx = ex + abs(ly - ey) * 0.45 * (1 if i < 3 else 1)
        if i in (3,):
            kx = X(240)
        elbow(s, [(ex, ey), (kx, ly), (X(300), ly)], "grey400", lw=0.75, r=0.01)
        text(s, X(305), ly - L(14), L(230), L(48), [[("{v}%–{v}%", {"bold": True})], "{Segment}"], size=F(15),
             color="text", margin=0, name=f"ring_{i+1}_label")


# d24 from / to shifts --------------------------------------------------------------------------------------
def d24():
    s = slide(prs)
    header(s, "How is {new approach} different from {traditional approach}?", "{source}")
    f = Frame2((0, 150, 1137, 925)); X, Y, W, H, D, F = f.X, f.Y, f.W, f.H, f.D, f.F
    text(s, X(108), Y(150), W(200), H(24), "FROM", size=11, color="grey800", margin=0)
    text(s, X(585), Y(150), W(200), H(24), "TO", size=11, color="grey800", margin=0)
    fills = [("accent900", "white"), ("accent700", "white"), ("accent500", "white"), ("grey800", "white"),
             ("grey600", "white"), ("grey500", "white")]
    for i, (fill, tc) in enumerate(fills):
        y = 185 + i * 125
        text(s, X(18), Y(y + 10), W(60), H(92), str(i + 1), size=F(62), color="grey500", align="c", anchor="m", margin=0,
             name=f"row_{i+1}_number")
        rrect(s, X(83), Y(y), W(490), H(112), 0.08, fill="grey100", name=f"from_{i+1}")
        text(s, X(108), Y(y), W(420), H(112), [[("{Old practice} ", {"bold": True}), ("{and its limit}", {})]],
             size=F(16.5), color="text", anchor="m", margin=0, name=f"from_{i+1}_text")
        pts = [(X(530), Y(y)), (X(1137), Y(y)), (X(1137), Y(y + 112)), (X(530), Y(y + 112)), (X(557), Y(y + 56))]
        polyline(s, pts, None, fill=fill, close=True, name=f"to_{i+1}")
        text(s, X(585), Y(y), W(535), H(112), [[("{New practice} ", {"bold": True}), ("{and its gain}", {})]],
             size=F(16.5), color=tc, anchor="m", margin=0, name=f"to_{i+1}_text")


for fn in (d21, d22, d23, d24):
    fn()
prs.save(sys.argv[1])
print("saved")
