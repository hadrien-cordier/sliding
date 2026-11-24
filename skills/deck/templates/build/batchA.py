"""Measured rebuild, designs d01-d04."""
import math, random, sys
from lib2 import *
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION

prs = new_deck()


# d01 process map: measured box 30 px high, dot 10 px, 2 px light border, 1 px grey connectors ----------
def d01():
    s = slide(prs)
    header(s, "{Process} runs through more variants than its design foresees", "{source}",
           "Illustrative; figures on connectors show cases per path")
    H, D = 0.42, 0.14
    def node(x, y, w, label, main=True, name=None):
        b = box(s, x, y, w, H, fill="white", line="line", lw=1.5, name=name)
        dot(s, x + 0.22, y + H / 2, D, "accent700" if main else "accent500")
        text(s, x + 0.4, y + 0.05, w - 0.45, H - 0.08, [[(label, {})], [("{count}", {"size": 7, "color": "grey400"})]],
             size=9.5, color="grey600", anchor="m", margin=0)
        return b
    def cnt(x, y):
        text(s, x, y, 0.45, 0.18, "{n}", size=7, color="grey400", margin=0)
    def ends(x, y, label, name):
        box(s, x, y, 1.05, H, fill="white", line="line", lw=1.5, name=name)
        dot(s, x + 0.22, y + H / 2, D, "grey600")
        text(s, x + 0.4, y + 0.05, 0.6, H - 0.08, [[(label, {})], [("{count}", {"size": 7, "color": "grey400"})]],
             size=9.5, color="grey600", anchor="m", margin=0)
    A = dict(color="grey400", lw=1.4, aw="med", al="med")
    ends(5.9, 1.2, "Start", "start")
    node(0.7, 1.95, 2.9, "{Main step}", True, "step_1"); node(7.3, 1.95, 2.9, "{Alternative entry}", False, "entry_2")
    node(0.7, 2.7, 2.9, "{Main step}", True, "step_2")
    for k, x in enumerate((0.7, 3.85, 6.95, 10.05)):
        node(x, 3.45, 2.75, "{Main step}" if k == 0 else "{Variant}", k == 0, "step_3" if k == 0 else f"variant_{k}")
    node(2.3, 4.2, 2.5, "{Sub-step}", False, "sub_1"); node(2.3, 4.8, 2.5, "{Sub-step}", False, "sub_2")
    node(6.95, 4.5, 2.75, "{Exception handling}", False, "exception_1")
    node(0.7, 5.45, 2.9, "{Main step}", True, "step_4"); node(0.7, 6.1, 2.9, "{Main step}", True, "step_5")
    ends(11.5, 6.1, "End", "end")
    elbow(s, [(6.42, 1.62), (6.42, 1.78), (2.15, 1.78), (2.15, 1.95)], arrow="tail", dash=True, **A)
    elbow(s, [(6.42, 1.78), (8.75, 1.78), (8.75, 1.95)], arrow="tail", dash=True, **A); cnt(6.55, 1.6)
    soft_line(s, 2.15, 2.37, 2.15, 2.7, arrow="tail", **A); cnt(2.25, 2.45)
    elbow(s, [(8.75, 2.37), (8.75, 2.53), (2.6, 2.53), (2.6, 2.7)], arrow="tail", **A); cnt(8.85, 2.4)
    elbow(s, [(3.6, 2.91), (11.4, 2.91), (11.4, 3.45)], arrow="tail", **A)
    for x in (5.2, 8.3):
        soft_line(s, x, 2.91, x, 3.45, arrow="tail", **A); cnt(x + 0.08, 3.1)
    soft_line(s, 2.0, 3.12, 2.0, 3.45, arrow="tail", **A); cnt(2.08, 3.18)
    elbow(s, [(2.9, 3.87), (2.9, 4.03), (3.55, 4.03), (3.55, 4.2)], arrow="tail", **A)
    soft_line(s, 3.55, 4.62, 3.55, 4.8, arrow="tail", **A)
    soft_line(s, 8.3, 3.87, 8.3, 4.5, arrow="tail", **A); cnt(8.38, 4.1)
    soft_line(s, 1.6, 3.87, 1.6, 5.45, arrow="tail", **A); cnt(1.68, 4.6)
    elbow(s, [(3.55, 5.22), (3.55, 5.33), (2.6, 5.33), (2.6, 5.45)], arrow="tail", **A)
    elbow(s, [(8.3, 4.92), (8.3, 5.33), (3.0, 5.33), (3.0, 5.45)], arrow="tail", **A); cnt(8.38, 5.05)
    soft_line(s, 2.15, 5.87, 2.15, 6.1, arrow="tail", **A)
    for x in (11.75, 12.05, 12.35):
        elbow(s, [(x, 3.87), (x, 6.1)], arrow="tail", dash=True, **A)
    elbow(s, [(3.6, 6.31), (11.5, 6.31)], arrow="tail", dash=True, **A); cnt(10.9, 6.12)
    node(9.95, 4.5, 1.45, "{Variant}", False, "variant_4"); node(9.95, 5.2, 1.45, "{Variant}", False, "variant_5")
    elbow(s, [(9.7, 4.71), (9.95, 4.71)], arrow="tail", **A)
    soft_line(s, 10.6, 4.92, 10.6, 5.2, arrow="tail", **A)
    elbow(s, [(10.3, 5.62), (10.3, 5.95), (3.4, 5.95), (3.4, 6.1)], arrow="tail", **A); cnt(9.6, 5.78)
    elbow(s, [(10.95, 5.62), (10.95, 6.1)], arrow="tail", dash=True, **A)
    elbow(s, [(4.8, 4.41), (6.2, 4.41), (6.2, 5.6), (11.3, 5.6), (11.3, 6.1)], arrow="tail", dash=True, **A)


# d02 journey road: ribbon 60 px with darker side face, dashed icon rings, pinned moments --------------
def d02():
    s = slide(prs)
    header(s, "{Simulating options} shows which {measures} carry the highest impact", "{source}", "Illustrative")
    cps = [((0.0, 2.95), (1.6, 2.85), (2.4, 4.55), (3.6, 4.35)), ((3.6, 4.35), (4.9, 4.15), (5.2, 2.6), (6.6, 2.75)),
           ((6.6, 2.75), (8.0, 2.9), (8.2, 4.6), (9.6, 4.4)), ((9.6, 4.4), (11.0, 4.2), (11.6, 3.0), (13.33, 3.05))]
    cen = []
    for seg in cps:
        cen += bez(*seg, n=40)[:-1]
    cen.append(cps[-1][3])
    left, right = [], []
    for i, (x, y) in enumerate(cen):
        a_, b_ = cen[max(0, i - 1)], cen[min(len(cen) - 1, i + 1)]
        tx, ty = b_[0] - a_[0], b_[1] - a_[1]; tl = math.hypot(tx, ty) or 1
        nx, ny = -ty / tl, tx / tl
        w = (0.42 + (y - 2.6) / 2.0 * 0.45) / 2      # perspective: nearer (lower) is wider
        left.append((x + nx * w, y + ny * w)); right.append((x - nx * w, y - ny * w))
    low = [p if p[1] >= q[1] else q for p, q in zip(left, right)]
    polyline(s, low + [(x, y + 0.13) for x, y in low[::-1]], None, fill="warm300", close=True, name="road_side")
    polyline(s, left + right[::-1], None, fill="warm100", close=True, name="road")
    roady = lambda x: min(cen, key=lambda p: abs(p[0] - x))[1]
    moments = [(2.5, 1.2, 1), (4.15, 4.62, -1), (5.55, 1.2, 1), (7.2, 4.62, -1), (8.6, 1.2, 1), (10.25, 4.62, -1)]
    for k, (x, y, side) in enumerate(moments, 1):
        icx, icy = x - 0.42, y + 0.32
        icon(s, icx, icy, 0.62, "second700", dash=True, name=f"moment_{k}_icon")
        text(s, x, y, 1.95, 0.95, [[("{Moment title}", {"bold": True, "color": "second700", "size": 10.5})],
                                    "{What the provider does for the client at this moment}"],
             size=9, color="grey600", margin=0, name=f"moment_{k}")
        ry = roady(icx)
        y1, y2 = (icy + 0.31, ry) if side > 0 else (icy - 0.31, ry)
        soft_line(s, icx, y1, icx, y2, "second700", lw=0.75, dash="dot")
        dot(s, icx, ry, 0.09, "second700")
    def kpi(x, y, name, w=1.0):
        rrect(s, x, y, w, 0.88, 0.07, fill="white", line="grey200", lw=1, name=name,
              parts=["{KPI label}", [("{value}", {"bold": True, "color": "accent500", "size": 11})],
                     [("({delta})", {"color": "second500", "size": 9})]], size=9, color="grey600", margin=0.03)
        dot(s, x + w / 2, y, 0.3, "warm300")
        icon(s, x + w / 2, y, 0.22, "white", name=f"{name}_badge")
    kpi(0.5, 1.25, "kpi_1"); kpi(0.5, 2.4, "kpi_2"); kpi(10.65, 1.25, "kpi_3"); kpi(11.8, 1.25, "kpi_4")
    kpi(11.8, 4.45, "kpi_5")
    for xa, xb in ((0.55, 5.82), (7.52, 12.75)):
        soft_line(s, xa, 5.47, xb, 5.47, "warm300", lw=1.5)
    dot(s, 0.55, 5.47, 0.07, "warm300"); dot(s, 12.75, 5.47, 0.07, "warm300")
    text(s, 5.9, 5.33, 1.55, 0.3, [[("{Panel title}", {"bold": True})]], size=12, color="warm700", align="c",
         name="panel_title", margin=0)
    for r, (lab, y) in enumerate([("Rationale", 5.6), ("Benefit", 6.27)]):
        box(s, 0.5, y, 0.32, 0.6, fill="warm700", name=f"row_{r+1}_tab")
        t = text(s, 0.36, y + 0.17, 0.6, 0.26, [[(lab, {"bold": True})]], size=8, color="white", align="c", margin=0,
                 anchor="m", name=f"row_{r+1}_label")
        t.rotation = 270
        for c in range(3):
            x0 = 1.1 + c * 3.9
            text(s, x0, y, 3.6, 0.6, "{Statement for this column}", size=10.5, color="grey600", align="c",
                 anchor="m", margin=0, name=f"row_{r+1}_col_{c+1}")
            if r == 0:
                cx = x0 + 1.8
                dot(s, cx, 6.235, 0.27, "warm500")
                elbow(s, [(cx - 0.065, 6.205), (cx, 6.27), (cx + 0.065, 6.205)], "white", lw=1.5)
    for c in (1, 2):
        xx = 1.1 + c * 3.9 - 0.15
        soft_line(s, xx, 5.62, xx, 6.85, "grey200", lw=1, dash=True)


# d03 zoom: placed on the reference pixels (crop 20,125 to 900,585) --------------------------------
def d03():
    s = slide(prs)
    header(s, "{Process intelligence} gives a fact base to assess {value potential}", "{source}", "Illustrative")
    f = Frame((20, 128, 900, 585))
    X, Y, L, F = f.X, f.Y, f.L, f.F
    for cx, t in [(142, "{End-to-end view}"), (465, "{Deep dive into one part}"), (768, "{Dashboard with KPIs}")]:
        text(s, X(cx - 150), Y(133), L(300), L(22), t, size=F(15), color="text", align="c", margin=0)
    rrect(s, *f.R(29, 157, 226, 389), L(8), fill="second50", name="overview_panel")
    sel = 2
    ys = [181, 236, 293, 350, 407, 464, 520]
    for i, y in enumerate(ys, 1):
        col = "accent500" if i == sel else "second700"
        box(s, X(38), Y(y - 8), L(16), L(16), fill=col, shape=MSO_SHAPE.OVAL, parts=[[(str(i), {"bold": True})]],
            size=F(10), color="white", margin=0)
        text(s, X(60), Y(y - 11), L(190), L(22), [[("{Stage name}", {"bold": True})]], size=F(13.5), color=col,
             anchor="m", margin=0, name=f"stage_{i}")
        if i < 7:
            soft_line(s, X(46), Y(y + 14), X(46), Y(ys[i] - 14), "grey400", lw=0.75, arrow="tail", aw="sm", al="sm")
    wy0, wy1 = Y(ys[sel - 1] - 16), Y(ys[sel - 1] + 16)
    w = polyline(s, [(X(255), wy0), (X(308), Y(157)), (X(308), Y(546)), (X(255), wy1)], None, fill="accent500",
                 close=True, name="zoom_wedge")
    w.fill.gradient(); w.fill.gradient_angle = 0
    st = w.fill.gradient_stops
    st[0].color.rgb = C("accent500"); st[0].position = 0
    st[1].color.rgb = C("accent50"); st[1].position = 1.0
    rrect(s, *f.R(308, 157, 313, 389), L(8), fill="accent50", name="deep_dive_panel")
    text(s, X(320), Y(165), L(290), L(20), "{Selected stage}", size=F(13), color="accent500", align="c", margin=0)
    sx = X(384)
    soft_line(s, sx, Y(197), sx, Y(549), "accent500", lw=2.5, arrow="tail", aw="lg", al="lg")
    steps = [204, 237, 270, 303, 336, 369, 402, 435, 467, 500]
    for k, y in enumerate(steps):
        if k in (0, 9):
            soft_line(s, sx - L(9), Y(y), sx + L(9), Y(y), "accent700", lw=2.5)
        else:
            soft_line(s, sx - L(7), Y(y), sx, Y(y), "accent300", lw=1.5)
            dot(s, sx + L(6), Y(y), L(7), "accent300")
        text(s, X(403), Y(y - 9), L(200), L(18), "{Step}" if k not in (0, 9) else ("{Process start}" if k == 0 else "{Process end}"),
             size=F(11.5), color="grey600", anchor="m", margin=0, name=f"dd_step_{k}")
    Dh = dict(color="accent300", lw=1, dash=True, aw="sm", al="sm")
    def hexa(x, y, col="accent500"):
        box(s, X(x) - L(6), Y(y) - L(6), L(12), L(12), fill="white", line=col, lw=1, shape=MSO_SHAPE.HEXAGON)
    def lab(x, y, t, col="accent500", w=90):
        text(s, X(x) - L(w / 2), Y(y), L(w), L(30), [[(t, {"italic": True})]], size=F(10), color=col, align="c", margin=0)
    elbow(s, [(X(505), Y(237)), (X(566), Y(237))], arrow="tail", **Dh); hexa(573, 237)
    elbow(s, [(X(548), Y(303)), (X(548), Y(327)), (X(562), Y(327))], arrow="tail", **Dh); hexa(570, 327)
    elbow(s, [(X(570), Y(320)), (X(570), Y(270)), (X(500), Y(270))], arrow="tail", **Dh)
    text(s, X(580), Y(318), L(45), L(40), [[("{Side request}", {"italic": True})]], size=F(10), color="accent500", margin=0)
    elbow(s, [(X(380), Y(336)), (X(343), Y(336)), (X(343), Y(362))], arrow="tail", **Dh); hexa(343, 369)
    lab(343, 377, "{Correction}"); elbow(s, [(X(343), Y(405)), (X(343), Y(425))], arrow="tail", **Dh)
    lab(343, 430, "{Cancellation}")
    elbow(s, [(X(520), Y(435)), (X(573), Y(435)), (X(573), Y(450))], arrow="tail", color="negative", lw=1, dash=True,
          aw="sm", al="sm"); hexa(573, 457, "negative"); lab(573, 465, "{Negative outcome}", "negative", 110)
    elbow(s, [(X(573), Y(480)), (X(573), Y(494))], arrow="tail", **Dh); hexa(573, 500); lab(573, 508, "{Outcome}")
    rrect(s, *f.R(651, 157, 235, 390), L(8), fill="warm50", name="kpi_panel")
    for r in range(3):
        for c in range(2):
            x, y = 660 + c * 113, 165 + r * 77
            text(s, X(x), Y(y), L(105), L(70), ["{KPI label}", [("{value}", {"bold": True, "size": F(19), "color": "warm700"})]],
                 size=F(12), color="grey600", align="c", margin=0, name=f"kpi_{r*2+c+1}")
        soft_line(s, X(662), Y(238 + r * 77), X(876), Y(238 + r * 77), "warm300", lw=0.75, dash=True)
    soft_line(s, X(769), Y(168), X(769), Y(388), "warm300", lw=0.75, dash=True)
    text(s, X(661), Y(402), L(120), L(18), "{Trend label}", size=F(11), color="grey600", margin=0)
    cd = CategoryChartData(); cd.categories = [str(i) for i in range(1, 13)]
    cd.add_series("{As-is}", [52, 60, 62, 48, 58, 60, 55, 57, 52, 57, 58, 59]); cd.add_series("{Target}", [32] * 12)
    gf = s.shapes.add_chart(XL_CHART_TYPE.LINE, I(X(655)), I(Y(415)), I(L(225)), I(L(125)), cd); gf.name = "trend_chart"
    ch = gf.chart; ch.has_title = False; ch.has_legend = True; ch.legend.position = XL_LEGEND_POSITION.BOTTOM
    ch.legend.include_in_layout = False; ch.font.size = Pt(7); ch.font.name = FONT
    ch.value_axis.has_major_gridlines = False; ch.value_axis.format.line.color.rgb = C("grey400")
    ch.value_axis.maximum_scale = 80; ch.value_axis.minimum_scale = 0; ch.value_axis.major_unit = 20
    ch.value_axis.tick_labels.font.size = Pt(8); ch.category_axis.tick_labels.font.size = Pt(8)
    ch.category_axis.format.line.color.rgb = C("grey400")
    for ser, col in zip(ch.plots[0].series, ("warm300", "warm700")):
        ser.format.line.color.rgb = C(col); ser.format.line.width = Pt(1.5); ser.smooth = False


# d04 three views: placed on the reference pixels (crop 18,90 to 891,590) ------------------------------
def d04():
    s = slide(prs)
    header(s, "{Organisations} run {process} variants they are not aware of", "{source}",
           "Illustrative, simplified; tags show the number of {cases}")
    f = Frame((15, 95, 891, 590))
    X, Y, L, F = f.X, f.Y, f.L, f.F
    heads = [(25, "How {it was} {designed}…", "l"), (300, "…how {we think it runs}…", "c"), (600, "…and how {it really runs}", "c")]
    for k, (x, h, al) in enumerate(heads):
        text(s, X(x), Y(100), L(250 if k else 175), L(40), [[(h, {"bold": True})]], size=F(14.5), color="text",
             align=al, margin=0, name=f"view_{k+1}_title")
    for x in (200, 597):
        soft_line(s, X(x), Y(85), X(x), Y(585), "grey200", lw=1, dash=True)
    cols = ["second700", "second500", "accent300", "accent700", "cat6", "cat8"]
    A = dict(color="warm500", lw=1, aw="sm", al="sm")
    def tag(x, y, dark=False, w=40):
        rrect(s, X(x), Y(y), L(w), L(16 if not dark else 20), L(2.5), fill="grey600" if dark else "warm500",
              parts="{n}", size=F(10.5 if not dark else 13), color="white", margin=0)
    def spine(cx, labels_x, dashed, tags=True):
        ys = [164, 221, 269, 318, 365, 413, 463, 512]
        for i, y in enumerate(ys):
            c = "grey400" if i in (0, 7) else cols[i - 1]
            dot(s, X(cx), Y(y), L(20), c)
            t = "{Process start}" if i == 0 else ("{Process end}" if i == 7 else "{Step}")
            text(s, X(labels_x), Y(y - 10), L(110), L(22), t, size=F(12.5),
                 color="grey600" if i in (0, 7) else c, anchor="m", margin=0)
            if i < 7:
                soft_line(s, X(cx), Y(y + 10), X(cx), Y(ys[i + 1] - 11), dash=dashed, arrow="tail", **A)
                if tags:
                    tag(cx - 50, (y + ys[i + 1]) / 2 - 7)
        tag(cx + 22, 176, True, 58); tag(cx + 22, 524, True, 58)
    spine(73, 92, True)
    spine(366, 383, False, tags=False)
    elbow(s, [(X(358), Y(221)), (X(267), Y(221)), (X(267), Y(235))], arrow="tail", **A)
    dot(s, X(267), Y(245), L(17), "second900")
    text(s, X(281), Y(234), L(80), L(26), "{Extra step}", size=F(12.5), color="second900", margin=0)
    elbow(s, [(X(267), Y(254)), (X(267), Y(269)), (X(356), Y(269))], arrow="tail", **A)
    elbow(s, [(X(432), Y(269)), (X(483), Y(269)), (X(483), Y(285))], arrow="tail", **A)
    dot(s, X(483), Y(295), L(17), "cat5"); text(s, X(497), Y(282), L(95), L(28), "{Rework loop}", size=F(12.5), color="cat5", margin=0)
    elbow(s, [(X(483), Y(304)), (X(483), Y(318)), (X(436), Y(318))], arrow="tail", **A)
    elbow(s, [(X(358), Y(365)), (X(267), Y(365)), (X(267), Y(404))], arrow="tail", **A)
    dot(s, X(267), Y(413), L(17), "cat5"); text(s, X(281), Y(400), L(70), L(28), "{Exit}", size=F(12.5), color="cat5", margin=0)
    soft_line(s, X(267), Y(422), X(267), Y(454), arrow="tail", **A)
    dot(s, X(267), Y(463), L(17), "second300"); text(s, X(281), Y(450), L(70), L(28), "{Close}", size=F(12.5), color="second500", margin=0)
    elbow(s, [(X(267), Y(472)), (X(267), Y(512)), (X(356), Y(512))], arrow="tail", dash=True, **A)
    for (x, y) in ((248, 202), (315, 187), (379, 239), (248, 279), (315, 289), (463, 253), (463, 326), (315, 334),
                   (248, 345), (315, 382), (218, 432), (315, 432), (315, 478), (248, 521)):
        tag(x - 20, y - 8, False)
    random.seed(11)
    box_l, box_t, box_r, box_b = 615, 150, 880, 575
    pts = [(random.uniform(box_l + 15, box_r - 15), random.uniform(box_t + 15, box_b - 15)) for _ in range(38)]
    for _ in range(150):
        a, b = random.sample(pts, 2)
        c1 = (a[0] + random.uniform(-200, 200), a[1] + random.uniform(-200, 200))
        c2 = (b[0] + random.uniform(-200, 200), b[1] + random.uniform(-200, 200))
        clamp = lambda p: (min(max(p[0], box_l), box_r), min(max(p[1], box_t), box_b))
        c1, c2 = clamp(c1), clamp(c2)
        curve(s, (X(a[0]), Y(a[1])), (X(c1[0]), Y(c1[1])), (X(c2[0]), Y(c2[1])), (X(b[0]), Y(b[1])), "grey200", lw=0.5)
    palette = cols + ["cat5", "second300", "second900", "grey400"]
    for k, (x, y) in enumerate(pts):
        dot(s, X(x), Y(y), L(17), palette[k % len(palette)])
    tag(375, 568); text(s, X(422), Y(565), L(200), L(20), "{number of cases}", size=F(11), color="grey600", margin=0)


for fn in (d01, d02, d03, d04):
    fn()
prs.save(sys.argv[1])
print("saved")
