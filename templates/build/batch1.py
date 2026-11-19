"""Batch 1: designs d01 to d08 rebuilt as native, named PowerPoint shapes (placeholder text)."""
import math, random, sys
from lib import *

prs = new_deck()


# d01 process map with variants ---------------------------------------------------------------
def d01():
    s = slide(prs)
    header(s, "{Process} runs through more variants than its design foresees",
           "{source}", "Illustrative; counts on connectors show cases per path")
    def node(x, y, w, label, dotc="accent500", name=None):
        b = box(s, x, y, w, 0.42, fill="white", line="grey200", lw=1.0, name=name)
        dot(s, x + 0.2, y + 0.21, 0.16, dotc)
        text(s, x + 0.35, y + 0.04, w - 0.4, 0.36, [[(label, {})], [("{count}", {"size": 8, "color": "grey600"})]],
             size=10, color="grey600")
        return b
    start = box(s, 5.6, 1.15, 1.2, 0.42, fill="white", line="grey200", name="start")
    dot(s, 5.8, 1.36, 0.16, "grey600"); text(s, 5.95, 1.2, 0.8, 0.32, "Start", size=10, color="grey600")
    row1 = [node(1.0, 1.85, 3.0, "Main step A", "accent700", "step_1"), node(7.4, 1.85, 3.0, "Alternative entry", "accent500", "step_1b")]
    n2 = node(1.0, 2.55, 3.0, "Main step B", "accent700", "step_2")
    row3 = [node(1.0, 3.3, 2.6, "Main step C", "accent700", "step_3"),
            node(3.9, 3.3, 2.6, "Variant C1", "accent500", "var_1"),
            node(6.8, 3.3, 2.6, "Variant C2", "accent500", "var_2"),
            node(9.7, 3.3, 2.6, "Variant C3", "accent500", "var_3")]
    sub = [node(2.6, 4.0, 2.4, "Sub-step 1", "accent500", "sub_1"),
           node(2.6, 4.6, 2.4, "Sub-step 2", "accent500", "sub_2"),
           node(6.8, 4.3, 2.6, "Exception handling", "accent500", "exc_1")]
    n4 = node(1.0, 5.3, 3.0, "Main step D", "accent700", "step_4")
    n5 = node(1.0, 5.95, 3.0, "Main step E", "accent700", "step_5")
    end = box(s, 11.2, 5.95, 1.2, 0.42, fill="white", line="grey200", name="end")
    dot(s, 11.4, 6.16, 0.16, "grey600"); text(s, 11.55, 6.0, 0.8, 0.32, "End", size=10, color="grey600")
    # main flow
    line(s, 6.2, 1.57, 6.2, 1.7, "grey400"); polyline(s, [(2.5, 1.7), (8.9, 1.7)], "grey400", dash=True)
    line(s, 2.5, 1.7, 2.5, 1.85, "grey400", arrow="tail"); line(s, 8.9, 1.7, 8.9, 1.85, "grey400", arrow="tail")
    line(s, 2.5, 2.27, 2.5, 2.55, "grey400", arrow="tail"); polyline(s, [(8.9, 2.27), (8.9, 2.4), (2.5, 2.4)], "grey400", arrow="tail")
    polyline(s, [(4.0, 2.76), (11.0, 2.76), (11.0, 3.3)], "grey400", arrow="tail")
    for x in (2.3, 5.2, 8.1):
        line(s, x, 2.97 if x == 2.3 else 2.76, x, 3.3, "grey400", arrow="tail")
    polyline(s, [(3.0, 3.72), (3.0, 3.85), (3.8, 3.85), (3.8, 4.0)], "grey400", arrow="tail")
    line(s, 3.8, 4.42, 3.8, 4.6, "grey400", arrow="tail")
    line(s, 8.1, 3.72, 8.1, 4.3, "grey400", arrow="tail")
    line(s, 2.0, 3.72, 2.0, 5.3, "grey400", arrow="tail")
    polyline(s, [(3.8, 5.02), (3.8, 5.15), (2.8, 5.15), (2.8, 5.3)], "grey400", arrow="tail")
    polyline(s, [(8.1, 4.72), (8.1, 5.15), (3.2, 5.15)], "grey400", arrow="tail")
    line(s, 2.5, 5.72, 2.5, 5.95, "grey400", arrow="tail")
    # exception paths to the end
    for x in (11.4, 11.8, 12.2):
        polyline(s, [(x if x != 12.2 else 11.0, 3.72), (x, 3.9), (x, 5.95)], "grey400", dash=True, arrow="tail")
    polyline(s, [(4.0, 6.16), (10.6, 6.16), (10.6, 6.16), (11.2, 6.16)], "grey400", dash=True, arrow="tail")
    for x, y in [(2.6, 2.3), (6.5, 1.55), (2.6, 3.05), (5.3, 3.05), (8.2, 3.05), (11.1, 3.05), (2.1, 4.9), (8.2, 4.9)]:
        text(s, x, y, 0.5, 0.2, "{n}", size=7, color="grey400")


# d02 customer journey road with KPIs and rationale/benefit -----------------------------------
def d02():
    s = slide(prs)
    header(s, "{Simulating options} shows which {measures} carry the highest impact",
           "{source}", "Illustrative")
    pts = []
    for i in range(0, 61):
        t = i / 60
        pts.append((0.4 + t * 12.5, 3.5 + 0.36 * math.sin(t * 2.6 * math.pi + 0.6) + 0.12 * t))
    polyline(s, [(x, y + 0.09) for x, y in pts], "current_dark", lw=30, name="road_shadow")
    polyline(s, pts, "current", lw=30, name="road")
    moments = [(2.35, 1.2, True), (3.75, 4.35, False), (5.15, 1.2, True), (6.55, 4.35, False),
               (7.95, 1.2, True), (9.35, 4.35, False)]
    for k, (x, y, above) in enumerate(moments, 1):
        icon(s, x - 0.38, y + 0.3, 0.52, "accent700", dash=True, name=f"moment_{k}_icon")
        text(s, x, y, 2.3, 0.85, [[("{Moment title}", {"bold": True, "color": "accent700"})],
                                   "{What the provider does at this moment}"],
             size=9, color="grey600", name=f"moment_{k}")
        tx = x + 0.12
        road_y = min(pts, key=lambda p: abs(p[0] - tx))[1]
        if above:
            line(s, tx, y + 0.88, tx, road_y - 0.02, "accent700", lw=0.75, dash=True)
        else:
            line(s, tx, y - 0.02, tx, road_y + 0.02, "accent700", lw=0.75, dash=True)
        dot(s, tx, road_y, 0.09, "accent700")
    def kpi(x, y, name, w=1.3):
        b = box(s, x, y, w, 0.8, fill="white", line="grey200", radius=0.12, name=name,
                parts=["{KPI label}", [("{value}", {"bold": True, "color": "accent500", "size": 12})],
                       [("({delta})", {"color": "grey600"})]], size=8, color="grey600")
        dot(s, x + w / 2, y, 0.2, "grey200")
        return b
    kpi(0.5, 1.2, "kpi_1"); kpi(0.5, 2.15, "kpi_2"); kpi(10.45, 1.2, "kpi_3", 1.12); kpi(11.68, 1.2, "kpi_4", 1.12)
    kpi(0.5, 4.3, "kpi_5")
    line(s, 0.5, 5.4, 4.9, 5.4, "grey200"); line(s, 8.4, 5.4, 12.8, 5.4, "grey200")
    text(s, 4.9, 5.26, 3.5, 0.3, [[("{Panel title}", {"bold": True})]], size=11, color="current_dark", align="c",
         name="panel_title")
    for r, (lab, y) in enumerate([("Rationale", 5.57), ("Benefit", 6.3)]):
        box(s, 0.5, y, 0.3, 0.5, fill="current_dark", name=f"row_{r+1}_tab")
        t = text(s, 0.27, y + 0.13, 0.76, 0.24, [[(lab, {"bold": True})]], size=8, color="white", align="c",
                 name=f"row_{r+1}_label")
        t.rotation = 270
        for c in range(3):
            x0 = 1.05 + c * 3.95
            text(s, x0, y, 3.7, 0.5, "{Statement for this column}", size=10, color="grey600",
                 align="c", anchor="m", name=f"row_{r+1}_col_{c+1}")
            if r == 0:
                cx = x0 + 1.85
                dot(s, cx, 6.17, 0.2, "current_dark")
                polyline(s, [(cx - 0.05, 6.15), (cx, 6.2), (cx + 0.05, 6.15)], "white", lw=1.25)
    for c in (1, 2):
        line(s, 1.05 + c * 3.95 - 0.12, 5.57, 1.05 + c * 3.95 - 0.12, 6.8, "grey200", dash=True)


# d03 zoom from end-to-end process to deep dive and KPI dashboard -----------------------------
def d03():
    s = slide(prs)
    header(s, "{Process intelligence} gives a fact base to assess {value potential}", "{source}", "Illustrative")
    for x, w, t in [(0.5, 3.3, "{End-to-end view}"), (4.55, 4.35, "{Deep dive into one part}"), (9.2, 3.6, "{Dashboard with KPIs}")]:
        text(s, x, 1.15, w, 0.3, t, size=12, color="text", align="c")
    box(s, 0.5, 1.5, 3.3, 5.2, fill="accent50", radius=0.04, name="overview_panel")
    sel = 2
    ys = [1.75 + i * 0.68 for i in range(7)]
    for i, y in enumerate(ys, 1):
        col = "accent500" if i == sel else "accent700"
        box(s, 0.65, y, 0.26, 0.26, fill=col, shape=MSO_SHAPE.OVAL, parts=[[(str(i), {"bold": True})]], size=9,
            color="white", margin=0)
        text(s, 1.0, y - 0.02, 2.7, 0.3, [[("{Stage name}", {"bold": True})]], size=11, color=col,
             name=f"stage_{i}", anchor="m")
        if i < 7:
            line(s, 0.78, y + 0.3, 0.78, y + 0.62, "grey400", lw=0.75, arrow="tail")
    # zoom wedge
    wy = ys[sel - 1]
    w = polyline(s, [(3.8, wy - 0.05), (4.55, 1.5), (4.55, 6.7), (3.8, wy + 0.32)], None, fill="accent500",
                 close=True, name="zoom_wedge")
    w.fill.gradient(); w.fill.gradient_angle = 0
    st = w.fill.gradient_stops
    st[0].color.rgb = C("accent500"); st[0].position = 0
    st[1].color.rgb = C("accent100"); st[1].position = 1.0
    box(s, 4.55, 1.5, 4.35, 5.2, fill="accent100", radius=0.04, name="deep_dive_panel")
    text(s, 4.55, 1.6, 4.35, 0.3, [[("{Selected stage}", {"color": "accent500"})]], size=11, align="c")
    lx = 5.6
    line(s, lx, 2.05, lx, 6.5, "accent500", lw=2.5, arrow="tail")
    steps = ["Process start", "Step", "Step", "Step", "Step", "Step", "Step", "Step", "Step", "Process end"]
    for k, lab in enumerate(steps):
        y = 2.15 + k * 0.42
        if k in (0, 9):
            line(s, lx - 0.12, y, lx + 0.12, y, "accent700", lw=2)
        else:
            line(s, lx - 0.08, y, lx, y, "accent300", lw=1.5)
        text(s, lx + 0.15, y - 0.12, 2.4, 0.24, lab, size=9, color="grey600", name=f"dd_step_{k}")
    # branches: loop back, exception (negative) and side outcome
    polyline(s, [(7.0, 2.57), (8.3, 2.57)], "accent300", lw=0.75, dash=True, arrow="tail")
    box(s, 8.3, 2.49, 0.15, 0.15, line="accent500", shape=MSO_SHAPE.HEXAGON)
    polyline(s, [(5.55, 3.83), (5.0, 3.83), (5.0, 4.3)], "accent300", lw=0.75, dash=True, arrow="tail")
    text(s, 4.6, 4.3, 0.95, 0.4, [[("{Side outcome}", {"italic": True})]], size=8, color="accent500", align="c")
    polyline(s, [(7.4, 5.51), (8.25, 5.51), (8.25, 5.75)], "negative", lw=0.75, dash=True, arrow="tail")
    box(s, 8.17, 5.78, 0.17, 0.17, line="negative", shape=MSO_SHAPE.HEXAGON)
    text(s, 7.7, 5.95, 1.15, 0.25, [[("{Negative outcome}", {"italic": True})]], size=8, color="negative", align="c")
    # KPI dashboard
    box(s, 9.2, 1.5, 3.6, 5.2, fill="grey100", radius=0.04, name="kpi_panel")
    for r in range(3):
        for c in range(2):
            x, y = 9.3 + c * 1.75, 1.6 + r * 0.95
            text(s, x, y, 1.65, 0.9, ["{KPI label}", [("{value}", {"bold": True, "size": 18, "color": "grey600"})]],
                 size=9, color="grey600", align="c", name=f"kpi_{r*2+c+1}")
        line(s, 9.35, 2.53 + r * 0.95, 12.65, 2.53 + r * 0.95, "grey200", lw=0.75)
    from pptx.chart.data import CategoryChartData
    from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION
    cd = CategoryChartData(); cd.categories = [str(i) for i in range(1, 13)]
    cd.add_series("As-is", [52, 60, 62, 48, 58, 60, 55, 57, 52, 57, 58, 59])
    cd.add_series("Target", [32] * 12)
    gf = s.shapes.add_chart(XL_CHART_TYPE.LINE, I(9.3), I(4.5), I(3.4), I(2.1), cd); gf.name = "trend_chart"
    ch = gf.chart; ch.has_legend = True; ch.legend.position = XL_LEGEND_POSITION.BOTTOM
    ch.legend.include_in_layout = False; ch.font.size = Pt(7); ch.font.name = FONT
    ch.value_axis.has_major_gridlines = False
    for ser, col in zip(ch.plots[0].series, ("grey400", "current_dark")):
        ser.format.line.color.rgb = C(col); ser.format.line.width = Pt(1.5); ser.smooth = False


# d04 three views: designed, assumed, real ---------------------------------------------------
def d04():
    s = slide(prs)
    header(s, "{Organisations} run {process} variants they are not aware of", "{source}", "Illustrative, simplified")
    heads = ["{How it was designed}…", "…{how we think it runs}…", "…and {how it really runs}"]
    for k, (x, h) in enumerate(zip((0.5, 4.6, 8.7), heads)):
        text(s, x, 1.15, 3.9, 0.55, [[(h, {"bold": True})]], size=13, color="text", name=f"view_{k+1}_title")
    for x in (4.45, 8.55):
        line(s, x, 1.15, x, 6.6, "grey200", dash=True)
    cats = ["cat1", "cat2", "cat3", "cat4", "cat5", "cat6"]
    def tag(x, y, dark=False):
        box(s, x, y, 0.62, 0.2, fill="grey600" if dark else "current", parts="{count}", size=7,
            color="white" if dark else "grey600", margin=0)
    def path(x0, branch):
        y = 1.95
        dot(s, x0, y, 0.2, "grey400"); text(s, x0 + 0.2, y - 0.14, 1.5, 0.28, "Process start", size=10, color="grey600")
        tag(x0 + 0.25, y + 0.15, True)
        for i, c in enumerate(cats):
            y2 = y + 0.62
            line(s, x0, y + 0.1, x0, y2 - 0.1, "grey400", lw=0.75, dash=(not branch), arrow="tail")
            tag(x0 - 0.75, y + 0.22)
            dot(s, x0, y2, 0.2, c)
            text(s, x0 + 0.2, y2 - 0.14, 1.6, 0.28, "{Step}", size=10, color=c)
            y = y2
        y2 = y + 0.62
        line(s, x0, y + 0.1, x0, y2 - 0.1, "grey400", lw=0.75, arrow="tail"); tag(x0 - 0.75, y + 0.22)
        dot(s, x0, y2, 0.2, "grey400"); text(s, x0 + 0.2, y2 - 0.14, 1.5, 0.28, "Process end", size=10, color="grey600")
        tag(x0 + 0.25, y2 + 0.15, True)
    path(1.7, False)
    path(6.2, True)
    # branches in the middle view
    polyline(s, [(6.1, 2.57), (5.2, 2.57), (5.2, 2.95)], "grey600", lw=0.75, arrow="tail"); dot(s, 5.2, 3.05, 0.2, "accent900")
    text(s, 4.45, 2.92, 0.62, 0.3, "{Extra step}", size=8, color="text", align="r")
    polyline(s, [(5.2, 3.15), (5.2, 3.19), (6.1, 3.19)], "grey600", lw=0.75, arrow="tail")
    polyline(s, [(6.3, 3.19), (7.5, 3.19), (7.5, 3.45)], "grey600", lw=0.75, arrow="tail"); dot(s, 7.5, 3.55, 0.2, "cat5")
    text(s, 7.62, 3.42, 0.95, 0.4, "{Rework loop}", size=9, color="cat5")
    polyline(s, [(7.5, 3.65), (7.5, 3.95), (6.3, 3.95)], "grey600", lw=0.75, arrow="tail")
    polyline(s, [(6.1, 5.05), (5.2, 5.05), (5.2, 5.35)], "grey600", lw=0.75, arrow="tail"); dot(s, 5.2, 5.45, 0.2, "cat5")
    text(s, 4.6, 5.62, 1.2, 0.3, "{Exit}", size=9, color="cat5")
    polyline(s, [(5.2, 5.55), (5.2, 6.3), (6.1, 6.3)], "grey600", lw=0.75, dash=True, arrow="tail")
    # spaghetti view
    random.seed(7)
    pts = [(random.uniform(8.9, 12.6), random.uniform(1.85, 6.4)) for _ in range(34)]
    for _ in range(70):
        a, b = random.sample(pts, 2)
        mx, my = (a[0] + b[0]) / 2 + random.uniform(-0.6, 0.6), (a[1] + b[1]) / 2 + random.uniform(-0.6, 0.6)
        polyline(s, [a, (mx, my), b], "grey200", lw=0.5)
    for k, (x, y) in enumerate(pts):
        dot(s, x, y, 0.17, cats[k % 6] if k % 7 else "grey400")
    tag(8.7, 6.45); text(s, 9.4, 6.4, 3.0, 0.28, "{number of cases}", size=8, color="grey600")


# d05 chevron process with pain points grouped by stage ---------------------------------------
def d05():
    s = slide(prs)
    header(s, "Pain points cluster along the {process}", "{source}")
    n, x0, w = 7, 0.5, 12.3
    sw = w / n
    for i in range(n):
        x = x0 + i * sw
        shp = MSO_SHAPE.PENTAGON if i == 0 else MSO_SHAPE.CHEVRON
        b = box(s, x, 2.35, sw + 0.12, 0.95, fill="accent500", line="white", lw=2.5, shape=shp,
                parts=[[("{Stage}", {"bold": True})]], size=13, color="white", name=f"stage_{i+1}")
        b.adjustments[0] = 0.28
        icon(s, x + sw / 2, 1.75, 0.6, "accent700", name=f"stage_{i+1}_icon")
    groups = [(0, 2), (2, 4), (4, 5), (5, 6), (6, 7)]
    for g, (a, b) in enumerate(groups, 1):
        x = x0 + a * sw + 0.12
        text(s, x, 3.5, (b - a) * sw - 0.25, 2.9,
             [[("{Pain point}: ", {"bold": True, "color": "accent500"}), ("{what goes wrong}", {})],
              "",
              [("{Pain point}: ", {"bold": True, "color": "accent500"}), ("{what goes wrong}", {})]],
             size=12, color="grey600", name=f"pains_{g}")
        if g > 1:
            line(s, x0 + a * sw, 3.4, x0 + a * sw, 5.8, "accent500", lw=1, dash=True)


# d06 two lanes: current sequential vs target continuous --------------------------------------
def d06():
    s = slide(prs)
    header(s, "Today {the work waits for a person}, with {change} {it stays current}", "{source}",
           "{Scope of the representation}; figures are indicative ranges")
    text(s, 0.5, 1.45, 6, 0.3, [[("{CURRENT}: {SEQUENTIAL}", {"bold": True})]], size=12, name="lane_1_label")
    n, sw = 6, 12.3 / 6
    for i in range(n):
        shp = MSO_SHAPE.PENTAGON if i == 0 else MSO_SHAPE.CHEVRON
        b = box(s, 0.5 + i * sw, 2.05, sw - 0.06, 0.7, fill="current", shape=shp, parts=["{Step}", "{in two lines}"],
                size=11, color="text", name=f"current_step_{i+1}")
        b.adjustments[0] = 0.22
    for xa, xb in [(5.3, 2.7), (8.9, 4.8)]:
        pts = [(xa - (xa - xb) * t / 20, 2.0 - 0.32 * math.sin(math.pi * t / 20)) for t in range(21)]
        polyline(s, pts, "accent500", lw=1, dash=True, arrow="tail")
        line(s, (xa + xb) / 2 + 0.45, 1.45, (xa + xb) / 2 - 0.25, 1.45, "accent500", lw=1, arrow="tail")
        text(s, (xa + xb) / 2 - 0.9, 1.15, 2.2, 0.25, "{Backward flow}", size=10, color="grey600", align="c")
    box(s, 0.5, 2.85, 12.3, 0.13, fill="accent500", name="time_bar")
    text(s, 0.5, 3.0, 5, 0.25, "{Elapsed time to outcome}", size=10, color="text")
    text(s, 10.8, 3.0, 2.0, 0.25, [[("{Weeks}", {"bold": True})]], size=10, align="r", name="time_unit")
    line(s, 0.5, 3.4, 12.8, 3.4, "grey200")
    text(s, 0.5, 3.5, 6, 0.3, [[("{TARGET}: {CONTINUOUS}", {"bold": True})]], size=12, name="lane_2_label")
    text(s, 0.5, 3.8, 12, 0.3, [[("{What changes for people, in one line}", {"bold": True})]], size=13,
         name="lane_2_message")
    ramp = [("accent100", "text"), ("accent300", "text"), ("accent500", "white"), ("accent700", "white")]
    sw2 = 2.35
    for i, (f, tc) in enumerate(ramp):
        shp = MSO_SHAPE.PENTAGON if i == 0 else MSO_SHAPE.CHEVRON
        b = box(s, 0.5 + i * sw2, 4.3, sw2 - 0.06, 0.85, fill=f, shape=shp,
                parts=[[("{Step}", {"bold": True})], [("{what it does}", {"size": 9})]], size=12, color=tc,
                name=f"target_step_{i+1}")
        b.adjustments[0] = 0.18
    box(s, 0.5 + 4 * sw2 + 0.05, 4.2, 12.8 - (0.5 + 4 * sw2 + 0.05), 1.05, fill="accent900", radius=0.08,
        parts=[[("{Value released}", {"bold": True})], [("{to whom or to what}", {"size": 9})]], size=12,
        color="white", name="value_box")
    for k in range(3):
        box(s, 0.75 + k * 3.25, 5.4, 2.9, 0.8, fill="white", line="grey400", radius=0.1,
            parts=[[("{value}", {"bold": True, "size": 15})], "{what it measures}"], size=10, color="text",
            name=f"kpi_{k+1}")


# d07 lifecycle stages, solutions per stage, shared layers -----------------------------------
def d07():
    s = slide(prs)
    header(s, "Many {solutions}, shared {capabilities}, one {foundation}", "{source}",
           "Solution set is illustrative and non-exhaustive")
    n, sw = 6, 12.3 / 6
    for i in range(n):
        shp = MSO_SHAPE.PENTAGON if i == 0 else MSO_SHAPE.CHEVRON
        b = box(s, 0.5 + i * sw, 1.4, sw - 0.04, 0.62, fill="accent900", shape=shp,
                parts=[[("{Stage}", {"bold": True})]], size=13, color="white", name=f"stage_{i+1}")
        b.adjustments[0] = 0.2
        for r in range(2):
            if (i, r) == (4, 1):
                continue
            box(s, 0.5 + i * sw, 2.12 + r * 0.62, sw - 0.1, 0.52, fill="accent100", radius=0.1,
                parts="{Solution}", size=11, color="text", name=f"solution_{i+1}_{r+1}")
    box(s, 0.5, 3.45, 12.3, 0.85, fill="accent300", radius=0.1, name="shared_layer",
        parts=[[("{Shared capabilities, built once and reused}", {"bold": True, "size": 13})],
               "{list of the shared capabilities}"], size=11, color="text")
    box(s, 0.5, 4.42, 12.3, 0.85, fill="current", radius=0.1, name="foundation_layer",
        parts=[[("{Shared foundation}", {"bold": True, "size": 13})],
               "{data, controls and governance that every solution relies on}"], size=11, color="text")


# d08 forces converge into a squeeze, resolved by two levers ----------------------------------
def d08():
    s = slide(prs)
    header(s, "{Three forces} create a {squeeze} that {two levers} resolve together", "{source}")
    def card(x, y, w, head_fill, name):
        box(s, x, y, w, 0.68, fill=head_fill, radius=0.12, name=f"{name}_head")
        box(s, x, y + 0.45, w, 0.25, fill=head_fill)
        icon(s, x + 0.45, y + 0.34, 0.42, "white", name=f"{name}_icon")
        text(s, x + 0.8, y + 0.08, w - 0.9, 0.55, [[("{Force or lever}", {"bold": True})]], size=13, color="white",
             anchor="m")
        box(s, x, y + 0.68, w, 0.9, fill="white", line=head_fill, lw=1.25, name=f"{name}_body",
            parts="{One sentence on what it does to the organisation}", size=11, color="grey600")
    for k, x in enumerate((0.5, 4.75, 9.0), 1):
        card(x, 1.2, 3.8, "accent500", f"force_{k}")
    # central squeeze with outer frame
    box(s, 3.55, 3.15, 6.2, 1.6, line="accent500", lw=1.25, radius=0.18, name="squeeze_frame")
    box(s, 3.75, 3.27, 5.8, 0.6, fill="accent900", radius=0.12,
        parts=[[("{The squeeze}", {"bold": True})]], size=15, color="white", name="squeeze_head")
    box(s, 3.75, 3.87, 5.8, 0.75, fill="white", line="accent500", lw=1, name="squeeze_body",
        parts="{Rising demands collide with constrained resources}", size=11, color="grey600")
    # connectors with junction dots
    polyline(s, [(2.4, 2.78), (2.4, 3.95), (3.55, 3.95)], "accent500", lw=1.25); dot(s, 3.55, 3.95, 0.12, "white", "accent500")
    line(s, 6.65, 2.78, 6.65, 3.15, "accent500", lw=1.25); dot(s, 6.65, 3.15, 0.12, "white", "accent500")
    polyline(s, [(10.9, 2.78), (10.9, 3.95), (9.75, 3.95)], "accent500", lw=1.25); dot(s, 9.75, 3.95, 0.12, "white", "accent500")
    # solution pill and lever cards
    line(s, 6.65, 4.75, 6.65, 5.55, "accent700", lw=1.25); dot(s, 6.65, 4.75, 0.12, "white", "accent700")
    box(s, 5.3, 5.55, 2.7, 0.7, fill="accent700", radius=0.25, name="solution_pill",
        parts=[[("{The solution}", {"bold": True})]], size=15, color="white")
    card(0.5, 5.1, 3.8, "accent700", "lever_1")
    card(9.0, 5.1, 3.8, "accent700", "lever_2")
    line(s, 4.3, 5.9, 5.3, 5.9, "accent700", lw=1.25); dot(s, 5.3, 5.9, 0.12, "white", "accent700")
    line(s, 8.0, 5.9, 9.0, 5.9, "accent700", lw=1.25); dot(s, 8.0, 5.9, 0.12, "white", "accent700")


for f in (d01, d02, d03, d04, d05, d06, d07, d08):
    f()
prs.save(sys.argv[1] if len(sys.argv) > 1 else "batch1.pptx")
print("saved")
