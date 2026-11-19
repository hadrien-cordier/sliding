"""Batch 2: designs d09 to d16 rebuilt as native, named PowerPoint shapes (placeholder text)."""
import math, sys
from lib import *
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LABEL_POSITION

prs = new_deck()


def plain_chart(ch, size=8):
    ch.has_title = False
    ch.has_legend = False
    ch.font.size = Pt(size); ch.font.name = FONT; ch.font.color.rgb = C("grey600")
    va = ch.value_axis
    va.has_major_gridlines = False; va.visible = False
    ca = ch.category_axis
    ca.format.line.color.rgb = C("grey400"); ca.has_major_gridlines = False
    ca.tick_labels.font.size = Pt(size)


def range_rule(s, x1, x2, y, label, color, size=22):
    line(s, x1, y, x2, y, color, lw=1)
    line(s, x1, y - 0.06, x1, y + 0.06, color, lw=1); line(s, x2, y - 0.06, x2, y + 0.06, color, lw=1)
    w = 0.25 + 0.17 * len(label)
    box(s, (x1 + x2) / 2 - w / 2, y - 0.22, w, 0.44, fill="white", parts=[[(label, {"bold": True})]],
        size=size, color=color, margin=0)


# d09 evidence ladder: finding, shift, remaining gap ------------------------------------------
def d09():
    s = slide(prs)
    header(s, "{Structural change} is reshaping {decisions}", "{survey source}", "{base of respondents}")
    def panel(y, h, head, col, name):
        box(s, 0.5, y, 12.3, h, fill="white", line=col, lw=1.25, radius=0.06, name=f"{name}_body")
        box(s, 0.5, y + 0.25, 12.3, 0.19, fill=col)
        box(s, 0.5, y, 12.3, 0.44, fill=col, radius=0.3, parts=[[(head, {"bold": True})]], size=13, color="white",
            name=f"{name}_head")
    panel(1.15, 1.55, "{Finding stated as a full sentence}", "accent500", "finding")
    for k in range(3):
        x = 0.75 + k * 4.1
        icon(s, x + 0.45, 2.2, 0.72, "white", fill="accent500", name=f"finding_{k+1}_icon")
        text(s, x + 0.95, 1.65, 3.0, 0.5, [[("{Value}", {"bold": True})]], size=24, color="accent500",
             name=f"finding_{k+1}_value")
        text(s, x + 0.95, 2.12, 2.9, 0.55, "{What this share of respondents reports}", size=10, color="grey600",
             name=f"finding_{k+1}_text")
        if k:
            line(s, x - 0.15, 1.75, x - 0.15, 2.6, "grey200")
    panel(2.85, 2.05, "{Shift stated as a full sentence}", "accent700", "shift")
    box(s, 0.52, 3.29, 12.26, 0.3, fill="accent100", parts="{Lead-in to the consequences, including:}", size=10,
        color="grey600", name="shift_leadin")
    range_rule(s, 0.75, 8.6, 3.92, "{Value}", "accent700")
    range_rule(s, 9.2, 12.55, 3.92, "{Value}", "accent700")
    line(s, 8.9, 3.75, 8.9, 4.75, "grey400")
    for k, x in enumerate((0.75, 3.55, 6.35, 9.2)):
        icon(s, x + 0.35, 4.4, 0.62, "white", fill="accent700", name=f"shift_{k+1}_icon")
        text(s, x + 0.75, 4.12, 1.95, 0.65, "{Consequence in a few words}", size=10, color="grey600",
             name=f"shift_{k+1}_text")
    panel(5.05, 1.6, "{Where the gap remains}", "accent900", "gap")
    icon(s, 1.0, 6.05, 0.8, "white", fill="accent900", name="gap_icon")
    text(s, 1.55, 5.62, 2.2, 0.85, [[("{Value}", {"bold": True})]], size=38, color="accent900", anchor="m",
         name="gap_value")
    text(s, 3.8, 5.7, 8.8, 0.75, "{What respondents plan, set against how mature the capability is}", size=11,
         color="grey600", anchor="m", name="gap_text")


# d10 time series columns with multiplier arrows and period brackets -------------------------
def d10():
    s = slide(prs)
    header(s, "{Capability} grows {multiple} every {period}", "{source}", "{definition of the measure}")
    text(s, 0.5, 1.15, 2, 0.3, "{Unit}", size=10, color="grey600", name="unit_label")
    months = ["Jan", "", "Mar", "", "May", "", "Jul", "", "Sep", "", "Nov", "",
              "Jan", "", "Mar", "", "May", "", "Jul", "", "Sep", "", "Nov", "", "Jan", "", "Mar"]
    vals = [0.05, 0.05, 0.05, 0.06, 0.1, 0.1, 0.2, 0.2, 0.2, 0.3, 0.4, 0.4, 0.7, 0.7, 1.0, 1.0, 2.0, 2.0, 2.0, 2.0,
            3.4, 3.4, 3.4, 4.9, 5.9, 5.9, 12, 12][:27]
    cd = CategoryChartData(); cd.categories = months; cd.add_series("Value", vals)
    gf = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, I(0.5), I(1.4), I(12.3), I(4.65), cd); gf.name = "chart"
    ch = gf.chart; plain_chart(ch, 9)
    pl = ch.plots[0]; pl.gap_width = 18
    ser = pl.series[0]; ser.format.fill.solid(); ser.format.fill.fore_color.rgb = C("accent500")
    for i in (2, 6, 10, 12, 14, 16, 20, 23, 24, 26):
        dl = ser.points[i].data_label
        dl.has_text_frame = True; dl.text_frame.text = "{v}"; dl.position = XL_LABEL_POSITION.OUTSIDE_END
        dl.font.bold = True; dl.font.size = Pt(10); dl.font.color.rgb = C("grey600")
    for (a, b, c, d, lab, nm) in [(1.2, 5.3, 4.2, 3.5, "~{n}x", "multiplier_1"), (5.6, 4.6, 10.0, 2.3, "~{n}x", "multiplier_2")]:
        pts = [(a + (c - a) * t / 20, b + (d - b) * (t / 20) ** 0.55) for t in range(21)]
        polyline(s, pts, "accent700", lw=16, arrow="tail", name=nm)
        px, py = pts[15]
        text(s, px - 0.45, py - 0.16, 0.9, 0.3, [[(lab, {"bold": True})]], size=12, color="white", align="c",
             name=f"{nm}_label")
    for (x1, x2, lab, k) in [(0.75, 5.2, "{Period 1}", 1), (5.5, 10.4, "{Period 2}", 2), (10.75, 12.65, "{Period 3}", 3)]:
        line(s, x1, 6.35, x2, 6.35, "current_dark", lw=0.75)
        line(s, x1, 6.28, x1, 6.42, "current_dark", lw=0.75); line(s, x2, 6.28, x2, 6.42, "current_dark", lw=0.75)
        box(s, (x1 + x2) / 2 - 0.45, 6.22, 0.9, 0.26, fill="current", radius=0.5, parts=[[(lab, {"bold": True})]],
            size=9, color="grey600", margin=0, name=f"period_{k}")


# d11 numbered journey cards on two rows, with agent badges ----------------------------------
def d11():
    s = slide(prs)
    header(s, "{Target journey}: {technology} and {people} combine at every step", "{source}")
    for row in range(2):
        y0 = 1.25 + row * 2.85
        line(s, 0.15, y0 + 0.25, 0.55, y0 + 0.25, "accent700", lw=1.5, arrow="tail")
        if row == 0:
            line(s, 12.75, y0 + 0.25, 13.15, y0 + 0.25, "accent700", lw=1.5, arrow="tail")
        for c in range(5):
            k = row * 5 + c + 1
            x = 0.6 + c * 2.5
            box(s, x + 0.1, y0 + 0.2, 2.25, 2.3, fill="accent50", radius=0.06, name=f"card_{k}")
            hc = "accent900" if k == 10 else "accent700"
            box(s, x + 0.2, y0, 2.05, 0.5, fill=hc, radius=0.5, parts=[[("{Step name}", {"bold": True})]], size=10,
                color="white", name=f"card_{k}_title")
            box(s, x - 0.02, y0 + 0.09, 0.32, 0.32, fill="white", line="accent700", lw=1.25, shape=MSO_SHAPE.OVAL,
                parts=[[(str(k), {"bold": True})]], size=9, color="accent700", margin=0)
            if c < 4:
                line(s, x + 2.25, y0 + 0.25, x + 2.5, y0 + 0.25, "accent700", lw=1.5)
            box(s, x + 0.55, y0 + 0.62, 1.35, 0.62, fill="grey100", line="grey200", dash=True, radius=0.1,
                parts="illustration", size=7, color="grey400", name=f"card_{k}_visual")
            text(s, x + 0.2, y0 + 1.3, 2.05, 0.95,
                 [[("• {Action} ", {}), ("{key phrase}", {"bold": True, "color": "accent500"}), (" {detail}", {})],
                  [("• {Action} ", {}), ("{key phrase}", {"bold": True, "color": "accent500"})]],
                 size=8, color="grey600", name=f"card_{k}_text")
            if k not in (1, 3):
                box(s, x + 0.35, y0 + 2.18, 0.42, 0.25, fill="accent700", radius=0.5, parts=[[("AI", {"bold": True})]],
                    size=8, color="white", margin=0)
                box(s, x + 0.77, y0 + 2.18, 1.33, 0.25, fill="accent500", radius=0.5, parts="{Agent name}", size=8,
                    color="white", margin=0, name=f"card_{k}_badge")
    # exception callout on the second row, between steps 7 and 8
    box(s, 4.45, 3.8, 2.0, 0.28, fill="negative", radius=0.5, parts="{Exception path}", size=9, color="white",
        name="exception_callout")
    line(s, 5.45, 4.08, 5.45, 4.45, "negative", lw=1.25); dot(s, 5.45, 4.45, 0.1, "negative")


# d12 swimlanes: humans, agents, process ------------------------------------------------------
def d12():
    s = slide(prs)
    header(s, "{Agents} run the {process} and escalate to people only {when it matters}", "{source}")
    line(s, 1.05, 1.2, 12.8, 1.2, "grey600", lw=1.25, arrow="tail")
    box(s, 0.45, 1.35, 0.45, 3.55, fill="accent500", name="band_who")
    t = text(s, -1.0, 2.95, 3.35, 0.35, [[("{Who does it}", {"bold": True})]], size=13, color="white", align="c")
    t.rotation = 270
    box(s, 0.45, 4.98, 0.45, 1.3, fill="accent700", name="band_process")
    t = text(s, 0.0, 5.45, 1.35, 0.35, [[("{Process}", {"bold": True})]], size=12, color="white", align="c")
    t.rotation = 270
    box(s, 0.45, 6.28, 0.45, 0.22, fill="accent700", shape=MSO_SHAPE.CHEVRON).rotation = 90
    box(s, 1.0, 1.35, 11.8, 3.55, fill="accent50", name="lane_actors")
    box(s, 1.0, 4.98, 11.8, 1.3, fill="grey100", name="lane_process")
    text(s, 1.05, 1.95, 1.0, 0.35, [[("{Humans}", {"bold": True})]], size=12, color="accent500", name="lane_1_label")
    text(s, 1.05, 3.75, 1.0, 0.5, [[("{AI / Agents}", {"bold": True})]], size=12, color="accent500", name="lane_2_label")
    xs = [2.05 + i * 1.08 for i in range(10)]
    line(s, 1.95, 2.55, 12.75, 2.55, "accent300", lw=1, dash=True)
    for i, x in enumerate(xs, 1):
        if i in (1, 2, 3, 4, 5, 6, 9, 10):
            icon(s, x + 0.5, 1.72, 0.48, "accent500", name=f"human_{i}_icon")
        last = i == 10
        box(s, x + 0.36, 5.05, 0.3, 0.3, fill="accent900" if last else "white", line="accent700", lw=1.25,
            shape=MSO_SHAPE.OVAL, parts=[[(str(i), {"bold": True})]], size=9, color="white" if last else "accent700",
            margin=0)
        box(s, x, 5.38, 1.02, 0.78, fill="accent900" if last else "white", line="accent700", lw=1, radius=0.15,
            parts="{Step}", size=8, color="white" if last else "text", name=f"step_{i}")
        if i in (2, 4, 5, 6, 7, 9, 10):
            box(s, x + 0.26, 3.55, 0.5, 0.5, fill="accent500", shape=MSO_SHAPE.OVAL, parts=[[("AI", {"bold": True})]],
                size=11, color="white", margin=0, name=f"agent_{i}")
            box(s, x + 0.03, 4.12, 0.96, 0.42, fill="white", line="accent500", lw=1, radius=0.1, parts="{Agent name}",
                size=7, color="accent700", margin=0.02, name=f"agent_{i}_label")
            text(s, x - 0.02, 2.75, 1.06, 0.75, "{What the agent does}", size=7, color="grey600", align="c",
                 name=f"agent_{i}_task")
            if i in (2, 4, 5, 9, 10):
                line(s, x + 0.51, 2.75, x + 0.51, 2.42, "negative", lw=1.5, arrow="tail")
    box(s, xs[1], 2.3, xs[4] + 1.0 - xs[1], 0.3, fill="negative", radius=0.2, parts="{Escalation rule}", size=9,
        color="white", name="escalation_1")
    box(s, xs[8], 2.3, xs[9] + 1.0 - xs[8], 0.3, fill="negative", radius=0.2, parts="{Escalation rule}", size=9,
        color="white", name="escalation_2")
    for a, b in ((6, 7), (7, 9)):
        line(s, xs[a - 1] + 0.8, 3.8, xs[b - 1] + 0.22, 3.8, "accent500", lw=1.25, arrow="tail")
    box(s, xs[6] + 0.3, 3.0, 0.42, 0.42, fill="accent700", shape=MSO_SHAPE.OVAL, parts=[[("Tool", {"bold": True})]],
        size=7, color="white", margin=0, name="tool_badge")
    for k, (lab, kind) in enumerate([("Escalation", "arrow"), ("AI agent", "ai"), ("{Actor 1}", "icon"), ("{Actor 2}", "icon")]):
        x = 3.0 + k * 2.2
        if kind == "arrow":
            line(s, x, 6.75, x, 6.5, "negative", lw=1.5, arrow="tail")
        elif kind == "ai":
            box(s, x - 0.14, 6.48, 0.28, 0.28, fill="accent500", shape=MSO_SHAPE.OVAL, parts=[[("AI", {"bold": True})]],
                size=7, color="white", margin=0)
        else:
            icon(s, x, 6.62, 0.28, "accent500", name=f"legend_{k}_icon")
        text(s, x + 0.2, 6.5, 1.6, 0.25, lab, size=8, color="grey600", name=f"legend_{k}")


# d13 roadmap: month header, workstreams, deep-dive lanes, keyed callouts --------------------
def d13():
    s = slide(prs)
    header(s, "{Acceleration roadmap} for {use cases}: {an example}", "{source}")
    text(s, 0.5, 1.13, 0.9, 0.32, [[("Months", {"bold": True})]], size=11, color="current_dark", anchor="m")
    n, x0, w = 14, 1.4, 11.4 / 14
    for i in range(n):
        now = i < 2
        b = box(s, x0 + i * w, 1.13, w + 0.04, 0.32, fill="current_dark" if now else "grey100",
                shape=MSO_SHAPE.PENTAGON if i == 0 else MSO_SHAPE.CHEVRON, parts="{Mon}", size=9,
                color="white" if now else "grey600", margin=0, name=f"month_{i+1}")
        b.adjustments[0] = 0.3
    box(s, x0, 1.55, w * 12, 0.3, fill="accent50", parts="{Workstream 1}", size=10, color="grey600", name="workstream_1")
    b = box(s, x0, 1.92, w * 14, 0.3, fill="accent50", shape=MSO_SHAPE.PENTAGON, parts="{Workstream 2}", size=10,
            color="grey600", name="workstream_2"); b.adjustments[0] = 0.3
    def key(x, y, k, col="accent500"):
        box(s, x - 0.14, y - 0.14, 0.28, 0.28, fill=col, shape=MSO_SHAPE.OVAL, parts=[[(k, {"bold": True})]], size=9,
            color="white", margin=0)
    key(1.25, 1.88, "A")
    polyline(s, [(1.0, 1.9), (0.75, 2.1), (0.8, 2.35), (1.05, 2.45)], "accent500", lw=2.5, arrow="tail")
    text(s, 1.1, 2.3, 2.0, 0.3, [[("{Deep-dive}:", {"bold": True})]], size=13, color="accent500")
    box(s, 0.5, 2.68, 12.3, 2.72, fill="grey100", name="deep_dive_panel")
    def phases(y, h, tint, labels, x_start, name):
        x = x_start
        for j, (lab, ww) in enumerate(labels):
            b = box(s, x, y, ww, h, fill=tint, shape=MSO_SHAPE.PENTAGON if j == 0 else MSO_SHAPE.CHEVRON,
                    parts=lab, size=9, color="text", name=f"{name}_{j+1}")
            b.adjustments[0] = 0.12
            x += ww - 0.08
    text(s, 0.6, 3.25, 1.2, 0.35, [[("{Segment 1}", {"bold": True})]], size=12, color="accent700", name="lane_1_label")
    phases(2.78, 1.2, "accent100", [("{Phase}", 1.75), ("{Parallel phase A}", 1.85), ("{Parallel phase B}", 1.85),
                                    ("{Phase}", 1.75), ("{Phase}", 1.75)], 3.2, "lane_1_phase")
    text(s, 0.6, 4.6, 1.2, 0.35, [[("{Segment 2}", {"bold": True})]], size=12, color="accent700", name="lane_2_label")
    phases(4.1, 1.2, "accent50", [("{Phase}", 1.2), ("{Parallel phase A}", 1.7), ("{Parallel phase B}", 1.6),
                                  ("{Phase}", 1.45), ("{Phase}", 1.45), ("{Next scope extension}", 3.9)], 2.1, "lane_2_phase")
    for (xa, ya) in ((5.25, 3.85), (4.15, 5.15)):
        polyline(s, [(xa, ya - 0.3), (xa - 0.15, ya), (xa + 0.3, ya + 0.12)], "accent500", lw=2, arrow="tail")
    key(1.4, 3.05, "C"); key(0.85, 4.35, "B"); key(5.35, 2.95, "D"); key(4.05, 4.28, "D")
    for x, y in ((7.0, 3.0), (8.65, 3.0), (10.3, 3.0), (6.6, 4.3), (8.0, 4.3)):
        box(s, x, y, 0.24, 0.24, fill="cat6", shape=MSO_SHAPE.OVAL, parts="R", size=7, color="white", margin=0)
    text(s, 0.5, 5.5, 3, 0.3, [[("Key callouts", {"bold": True})]], size=13, color="accent500")
    marks = [("~", "accent500"), ("A", "accent500"), ("B", "accent500"), ("C", "accent500"), ("D", "accent500"), ("R", "cat6")]
    for k, (m, col) in enumerate(marks):
        x = 0.5 + k * 2.07
        key(x + 0.14, 5.98, m, col)
        text(s, x, 6.17, 1.95, 0.65, "{What this marker means on the roadmap}", size=8, color="grey600",
             name=f"callout_{k+1}")


# d14 small multiples: revenue bridges by segment --------------------------------------------
def d14():
    s = slide(prs)
    header(s, "{Innovation} lets {institutions} extend {the perimeter of their business}", "{sources}",
           "{definitions}; {projection method}")
    shades = ["accent300", "accent500", "accent700", "accent900"]
    for k, x in enumerate((0.5, 4.65, 8.8)):
        box(s, x, 1.15, 3.95, 0.6, fill="grey100", radius=0.25, name=f"segment_{k+1}_head")
        icon(s, x + 0.45, 1.45, 0.4, "accent700", name=f"segment_{k+1}_icon")
        text(s, x + 0.8, 1.2, 3.0, 0.5, [[("{Segment}", {"bold": True})]], size=12, anchor="m", name=f"segment_{k+1}")
        text(s, x, 1.95, 3.95, 0.3, "{MEASURE (UNIT)}", size=9, color="grey600", align="c")
        if k < 2:
            cd = CategoryChartData()
            cd.categories = ["{Start}", "{BaU}", "{Erosion}", "{New}", "{End}"]
            cd.add_series("base", [0, 0, 3200, 3200, 0])
            cd.add_series("total", [2900, 3800, 0, 0, 4000])
            cd.add_series("erosion", [0, 0, 600, 0, 0])
            for j in range(4):
                cd.add_series(f"lever_{j+1}", [0, 0, 0, [200, 250, 200, 150][j], 0])
            gf = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_STACKED, I(x), I(2.25), I(3.95), I(3.3), cd)
            gf.name = f"segment_{k+1}_bridge"
            ch = gf.chart; plain_chart(ch, 8); ch.plots[0].gap_width = 45
            cols = [None, "grey200", "negative_bg"] + shades
            for ser, col in zip(ch.plots[0].series, cols):
                if col is None:
                    ser.format.fill.background()
                else:
                    ser.format.fill.solid(); ser.format.fill.fore_color.rgb = C(col)
            tot = ch.plots[0].series[1]
            for i in (0, 1, 4):
                dl = tot.points[i].data_label; dl.has_text_frame = True; dl.text_frame.text = "{v}"
                dl.position = XL_LABEL_POSITION.INSIDE_END; dl.font.bold = True; dl.font.size = Pt(9)
            # series lines draw the dashed bridge between columns
            bc = ch.plots[0]._element
            sl = etree.SubElement(bc, qn("c:serLines"))
            sp = etree.SubElement(sl, qn("c:spPr")); ln = etree.SubElement(sp, qn("a:ln"), w="6350")
            sf = etree.SubElement(ln, qn("a:solidFill")); etree.SubElement(sf, qn("a:srgbClr"), val=THEME["colors"]["grey400"][1:])
            etree.SubElement(ln, qn("a:prstDash"), val="dash")
            ax = bc.findall(qn("c:axId"))[0]; ax.addprevious(sl)
            for j in range(4):
                box(s, x + 0.2 + (j % 2) * 1.9, 5.65 + (j // 2) * 0.27, 0.16, 0.16, fill=shades[j])
                text(s, x + 0.42 + (j % 2) * 1.9, 5.6 + (j // 2) * 0.27, 1.6, 0.25, "{Lever}", size=8, color="grey600",
                     name=f"segment_{k+1}_lever_{j+1}")
        else:
            cd = CategoryChartData(); cd.categories = ["{Start}", "{End}"]; cd.add_series("total", [990, 1300])
            gf = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, I(x + 0.3), I(2.25), I(3.35), I(3.3), cd)
            gf.name = f"segment_{k+1}_bars"
            ch = gf.chart; plain_chart(ch, 8); ch.plots[0].gap_width = 35
            ser = ch.plots[0].series[0]; ser.format.fill.solid(); ser.format.fill.fore_color.rgb = C("grey200")
            ser.data_labels.show_value = True; ser.data_labels.position = XL_LABEL_POSITION.OUTSIDE_END
            ser.data_labels.font.bold = True; ser.data_labels.font.size = Pt(9)
    for x in (4.57, 8.72):
        line(s, x, 1.15, x, 6.2, "grey200")


# d15 spotlight case: line chart with multiplier bracket and notched callout panel -----------
def d15():
    s = slide(prs)
    header(s, "{Lever} led to a {multiple} of {metric} for {actor}", "{sources}", "{data definitions}")
    box(s, 0.4, 1.1, 12.5, 5.65, fill="grey100", radius=0.04, name="spotlight_panel")
    icon(s, 1.05, 1.75, 0.8, "accent700", fill="accent300", name="spotlight_icon")
    text(s, 1.6, 1.45, 4.5, 0.6, [[("SPOTLIGHT", {"bold": True, "color": "accent500"})],
                                   [("{Spotlight title}", {"bold": True})]], size=11, name="spotlight_title")
    text(s, 6.9, 1.35, 5.8, 0.85, "{Two sentences: what the actor achieved, and what drove it}", size=10,
         color="grey600", name="spotlight_intro")
    text(s, 0.7, 2.45, 6, 0.3, "{MEASURE (UNIT)}", size=9, color="grey600")
    cd = CategoryChartData(); cd.categories = [str(y) for y in range(2017, 2026)]
    cd.add_series("share", [1.8, 2.1, 2.4, 3.2, 4.0, 4.9, 5.3, 5.7, 6.7])
    gf = s.shapes.add_chart(XL_CHART_TYPE.LINE_MARKERS, I(0.6), I(3.1), I(6.3), I(3.4), cd); gf.name = "chart"
    ch = gf.chart; plain_chart(ch, 8); ch.value_axis.visible = True
    ch.value_axis.format.line.color.rgb = C("grey400")
    ser = ch.plots[0].series[0]; ser.format.line.color.rgb = C("accent500"); ser.format.line.width = Pt(2.25)
    ser.smooth = False; ser.marker.style = None
    from pptx.enum.chart import XL_MARKER_STYLE
    ser.marker.style = XL_MARKER_STYLE.NONE
    ser.data_labels.show_value = True; ser.data_labels.position = XL_LABEL_POSITION.ABOVE
    ser.data_labels.font.bold = True; ser.data_labels.font.size = Pt(9)
    line(s, 1.0, 2.95, 6.55, 2.95, "grey400", lw=1); line(s, 1.0, 2.95, 1.0, 3.2, "grey400", lw=1)
    line(s, 6.55, 2.95, 6.55, 3.25, "grey400", lw=1, arrow="tail")
    box(s, 3.4, 2.83, 0.75, 0.25, fill="accent300", radius=0.5, parts=[[("{n}x", {"bold": True})]], size=10,
        color="text", margin=0, name="multiplier")
    box(s, 7.45, 2.9, 5.2, 3.6, fill="grey200", radius=0.05, name="drivers_panel")
    tri = box(s, 7.2, 4.5, 0.32, 0.4, fill="grey200", shape=MSO_SHAPE.ISOSCELES_TRIANGLE)
    tri.rotation = 270
    for k in range(3):
        y = 3.15 + k * 1.1
        icon(s, 8.05, y + 0.38, 0.6, "white", fill="grey600", name=f"driver_{k+1}_icon")
        text(s, 8.55, y, 4.0, 1.0, [[("{Driver stated as a claim}", {"bold": True})], "· {proof point}",
                                    "· {proof point}"], size=10, color="text", name=f"driver_{k+1}")


# d16 platform hub between two sides ---------------------------------------------------------
def d16():
    s = slide(prs)
    header(s, "{Platform} gives {actors} a role in {ecosystem}", "{source}")
    cx, cy, r = 6.67, 3.95, 1.25
    box(s, cx - r, cy - r, 2 * r, 2 * r, fill="accent100", shape=MSO_SHAPE.OVAL, name="hub",
        parts=[[("{Open network}", {"size": 15})], [("{for the ecosystem}", {"size": 15})], "",
               [("{Key fact about ownership}", {"size": 9})]], size=17, color="text")
    for side in (-1, 1):
        a0 = math.radians(130 if side < 0 else -50)
        pts = [(cx + 1.55 * math.cos(a0 + math.radians(100) * t / 20), cy - 1.55 * math.sin(a0 + math.radians(100) * t / 20))
               for t in range(21)]
        polyline(s, pts, "grey400", lw=1)
        for y in (cy - 1.15, cy + 1.15):
            xa = cx + side * 1.0
            line(s, xa, y, cx + side * 2.95, y, "grey400", lw=1, arrow="tail")
        for k, (y, lab) in enumerate([(cy - 1.75, "{Side A actors}"), (cy - 0.05, "{Intermediary}"), (cy + 0.95, "{Side B actors}")]):
            xi = cx + side * 3.55
            icon(s, xi, y, 0.5, "text", name=f"{'left' if side < 0 else 'right'}_actor_{k+1}_icon")
            text(s, xi - 0.8, y + 0.28, 1.6, 0.3, [[(lab, {"bold": True})]], size=10, align="c",
                 name=f"{'left' if side < 0 else 'right'}_actor_{k+1}")
        for k, y in enumerate((1.25, 4.15)):
            x = 0.6 if side < 0 else 10.75
            box(s, x, y, 1.95, 2.45, fill="white", line="text", lw=2.25, radius=0.08,
                name=f"{'left' if side < 0 else 'right'}_app_{k+1}")
            box(s, x + 0.02, y + 0.02, 1.91, 0.36, fill="accent700", radius=0.3,
                parts=[[("{App name}", {"bold": True})]], size=10, color="white", margin=0)
            for j in range(3):
                box(s, x + 0.18, y + 0.55 + j * 0.6, 1.6, 0.45, fill="accent100" if j == 0 else "grey200")
    text(s, cx - 1.4, cy + 1.55, 2.8, 0.85, [[("{Services offered}", {"bold": True})], "· {service}", "· {service}"],
         size=10, align="c", name="services")


for f in (d09, d10, d11, d12, d13, d14, d15, d16):
    f()
prs.save(sys.argv[1] if len(sys.argv) > 1 else "batch2.pptx")
print("saved")
