"""Measured rebuild, designs d09-d12, placed on the reference pixels (d10 reuses the approved v2)."""
import sys
from lib2 import *
import d10_fn

prs = new_deck()
d10_fn.prs = prs


def rule(s, f, x1, x2, y, label, col, size):
    X, Y, L = f.X, f.Y, f.L
    soft_line(s, X(x1), Y(y), X(x2), Y(y), col, lw=1.25)
    soft_line(s, X(x1), Y(y - 7), X(x1), Y(y + 7), col, lw=1.25); soft_line(s, X(x2), Y(y - 7), X(x2), Y(y + 7), col, lw=1.25)
    w = 40 + 19 * len(label)
    box(s, X((x1 + x2) / 2 - w / 2), Y(y - 22), L(w), L(44), fill="white", parts=[[(label, {"bold": True})]],
        size=size, color=col, margin=0)


# d09 evidence ladder ---------------------------------------------------------------------------
def d09():
    s = slide(prs)
    header(s, "{Structural change} is reshaping {decisions}", "{survey source}", "{base of respondents}")
    f = Frame((15, 105, 1075, 790)); X, Y, L, F = f.X, f.Y, f.L, f.F
    def panel(y0, y1, col, title, name):
        rrect(s, X(22), Y(y0), L(1044), L(y1 - y0), L(18), fill="white", line=col, lw=1.75, name=f"{name}_body")
        top_round(s, X(22), Y(y0), L(1044), L(50), L(18), fill=col, name=f"{name}_head",
                  parts=[[(title, {"bold": True})]], size=F(21), color="white")
    panel(110, 300, "accent500", "{Finding stated as a full sentence}", "finding")
    for k, cx in enumerate((84, 432, 780), 1):
        icon(s, X(cx), Y(228), L(80), "white", fill="accent500", name=f"finding_{k}_icon")
        text(s, X(cx + 55), Y(170), L(230), L(44), [[("{Value}", {"bold": True})]], size=F(36), color="accent500",
             margin=0, name=f"finding_{k}_value")
        text(s, X(cx + 55), Y(216), L(215), L(70), "{What this share of respondents reports}", size=F(17),
             color="grey600", margin=0, name=f"finding_{k}_text")
    for x in (370, 718):
        soft_line(s, X(x), Y(178), X(x), Y(282), "accent500", lw=1.5)
    panel(318, 597, "accent700", "{Shift stated as a full sentence}", "shift")
    box(s, X(24), Y(370), L(1040), L(33), fill="accent100", parts="{Lead-in to the consequences, including:}",
        size=F(15), color="grey600", margin=0, name="shift_leadin")
    rule(s, f, 50, 717, 450, "{Value}", "accent700", F(30))
    rule(s, f, 765, 1040, 450, "{Value}", "accent700", F(30))
    soft_line(s, X(743), Y(428), X(743), Y(578), "grey400", lw=1)
    for k, (cx, w) in enumerate(((78, 140), (295, 140), (512, 175), (790, 220)), 1):
        icon(s, X(cx), Y(528), L(64), "white", fill="accent700", name=f"shift_{k}_icon")
        text(s, X(cx + 42), Y(484), L(w), L(90), "{Consequence in a few words}", size=F(17),
             color="grey600", anchor="m", margin=0, name=f"shift_{k}_text")
    panel(615, 785, "accent900", "{Where the gap remains}", "gap")
    icon(s, X(92), Y(725), L(85), "white", fill="accent900", name="gap_icon")
    text(s, X(140), Y(682), L(185), L(85), [[("{V}%", {"bold": True})]], size=F(58), color="accent900",
         anchor="m", margin=0, name="gap_value")
    text(s, X(335), Y(695), L(715), L(60), "{What respondents plan, set against how mature the capability is}",
         size=F(17), color="grey600", anchor="m", margin=0, name="gap_text")


# d11 numbered journey cards ------------------------------------------------------------------------
def d11():
    s = slide(prs)
    header(s, "{Target journey}: {technology} and {people} combine at every step", "{source}")
    f = Frame((35, 180, 1095, 880)); X, Y, L, F = f.X, f.Y, f.L, f.F
    xs = [(75, 250), (280, 455), (485, 660), (690, 862), (893, 1065)]
    for row in range(2):
        dy = row * 372
        soft_line(s, X(38), Y(216 + dy), X(66), Y(216 + dy), "accent700", lw=1.75, arrow="tail", aw="sm", al="sm")
        if row == 0:
            soft_line(s, X(1066), Y(216), X(1092), Y(216), "accent700", lw=1.75, arrow="tail", aw="sm", al="sm")
        for c, (x0, x1) in enumerate(xs):
            k = row * 5 + c + 1
            rrect(s, X(x0), Y(225 + dy), L(x1 - x0), L(265), L(12), fill="accent100", name=f"card_{k}")
            if c < 4:
                soft_line(s, X(x1), Y(216 + dy), X(xs[c + 1][0]), Y(216 + dy), "accent700", lw=1.75)
            rrect(s, X(x0 + 8), Y(188 + dy), L(x1 - x0 - 8), L(55), L(27), fill="accent900" if k == 10 else "accent700",
                  parts=[[("{Step name}", {"bold": True})]], size=F(15), color="white", margin=0.05, name=f"card_{k}_title")
            box(s, X(x0 - 10), Y(203 + dy), L(26), L(26), fill="accent900" if k == 10 else "white", line="accent700",
                lw=1.5, shape=MSO_SHAPE.OVAL, parts=[[(str(k), {"bold": True})]], size=F(13),
                color="white" if k == 10 else "accent700", margin=0)
            rrect(s, X(x0 + 12), Y(254 + dy), L(x1 - x0 - 24), L(92), L(8), fill="white", line="grey200", dash=True,
                  parts="{illustration}", size=F(10), color="grey400", name=f"card_{k}_visual")
            text(s, X(x0 + 12), Y(355 + dy), L(x1 - x0 - 22), L(110),
                 [[("• {Action} ", {}), ("{key phrase}", {"bold": True, "color": "accent500"}), (" {detail}", {})],
                  [("• {Action} ", {}), ("{key phrase}", {"bold": True, "color": "accent500"}), (" {detail}", {})]],
                 size=F(14), color="grey600", margin=0, name=f"card_{k}_text")
            for para in s.shapes[-1].text_frame.paragraphs:
                pPr = para._p.get_or_add_pPr(); pPr.set("marL", str(int(I(0.1)))); pPr.set("indent", str(-int(I(0.1))))
            if k not in (1, 3):
                rrect(s, X(x0 + 10), Y(480 + dy), L(x1 - x0 - 20), L(24), L(12), fill="accent500")
                rrect(s, X(x0 + 10), Y(480 + dy), L(45), L(24), L(12), fill="accent300",
                      parts=[[("AI", {"bold": True})]], size=F(12), color="accent900", margin=0)
                text(s, X(x0 + 58), Y(480 + dy), L(x1 - x0 - 72), L(24), "{Agent name}", size=F(12), color="white",
                     align="c", anchor="m", margin=0, name=f"card_{k}_badge")
    rrect(s, X(377), Y(523), L(175), L(24), L(12), fill="negative", parts="{Exception path}", size=F(12.5),
          color="white", margin=0, name="exception_callout")
    soft_line(s, X(465), Y(547), X(465), Y(588), "negative", lw=1.75)
    dot(s, X(465), Y(588), L(9), "negative")


# d12 swimlanes ---------------------------------------------------------------------------------------
def d12():
    s = slide(prs)
    header(s, "{Agents} run the {process} and escalate to people only {when it matters}", "{source}")
    f = Frame((40, 25, 1100, 500)); X, Y, L, F = f.X, f.Y, f.L, f.F
    soft_line(s, X(90), Y(40), X(1092), Y(40), "grey600", lw=1.5, arrow="tail", aw="med", al="med")
    def band(y0, y1, col, label, name):
        pts = [(X(45), Y(y0)), (X(77), Y(y0)), (X(77), Y(y1)), (X(61), Y(y1 + 14)), (X(45), Y(y1))]
        polyline(s, pts, None, fill=col, close=True, name=name)
        t = text(s, X(61) - L(y1 - y0) / 2, Y((y0 + y1) / 2) - L(14), L(y1 - y0), L(28), [[(label, {"bold": True})]],
                 size=F(18), color="white", align="c", anchor="m", margin=0, name=f"{name}_label")
        t.rotation = 270
    box(s, X(77), Y(50), L(1015), L(290), fill="accent50", name="lane_actors")
    box(s, X(77), Y(348), L(1015), L(112), fill="grey100", name="lane_process")
    band(33, 340, "accent500", "{Who does it}", "band_who")
    band(352, 470, "accent700", "{Process}", "band_process")
    text(s, X(92), Y(118), L(110), L(26), [[("{Humans}", {"bold": True})]], size=F(17), color="accent500", margin=0)
    text(s, X(95), Y(285), L(90), L(50), [[("{AI /}", {"bold": True})], [("{Agents}", {"bold": True})]], size=F(17),
         color="accent500", margin=0)
    cols = [131, 232, 333, 433, 535, 636, 736, 836, 937, 1038]
    soft_line(s, X(90), Y(159), X(1092), Y(159), "accent500", lw=1, dash=True)
    for i, cx in enumerate(cols, 1):
        if i not in (7, 8):
            icon(s, X(cx), Y(88), L(45), "accent500", name=f"human_{i}_icon")
        last = i == 10
        rrect(s, X(cx - 47), Y(380), L(94), L(67), L(12), fill="accent700" if last else "white", line="accent700",
              lw=1.5, parts="{Step}", size=F(12), color="white" if last else "text", name=f"step_{i}")
        box(s, X(cx - 14), Y(356), L(28), L(28), fill="accent900" if last else "white", line="accent700", lw=1.5,
            shape=MSO_SHAPE.OVAL, parts=[[(str(i), {"bold": True})]], size=F(13), color="white" if last else "accent700",
            margin=0)
    for i in (2, 4, 5, 6, 8, 9, 10):
        cx = cols[i - 1]
        box(s, X(cx - 21), Y(253), L(42), L(42), fill="accent500", shape=MSO_SHAPE.OVAL,
            parts=[[("AI", {"bold": True})]], size=F(16), color="white", margin=0, name=f"agent_{i}")
        rrect(s, X(cx - 44), Y(300), L(88), L(32), L(6), fill="white", line="accent500", lw=1.25, parts="{Agent name}",
              size=F(11), color="accent700", margin=0.01, name=f"agent_{i}_label")
        text(s, X(cx - 46), Y(188), L(92), L(55), "{What the agent does}", size=F(10), color="grey600", align="c",
             margin=0, name=f"agent_{i}_task")
        if i in (2, 4, 5, 9, 10):
            soft_line(s, X(cx), Y(146), X(cx), Y(118), "negative", lw=2.25, arrow="tail", aw="lg", al="med")
    soft_line(s, X(cols[5]), Y(186), X(cols[5]), Y(118), "negative", lw=2.25, arrow="tail", aw="lg", al="med")
    rrect(s, X(188), Y(143), L(390), L(32), L(8), fill="negative", parts="{Escalation rule}", size=F(13), color="white",
          margin=0, name="escalation_1")
    rrect(s, X(888), Y(143), L(200), L(45), L(8), fill="negative", parts="{Escalation rule}", size=F(13), color="white",
          margin=0, name="escalation_2")
    for a, b in ((6, 8), (8, 9)):
        soft_line(s, X(cols[a - 1] + 30), Y(274), X(cols[b - 1] - 28), Y(274), "accent500", lw=1.5, arrow="tail",
                  aw="sm", al="sm")
    rrect(s, X(660), Y(165), L(112), L(22), L(11), fill="white", line="second500", lw=1.25, parts="{Tool name}",
          size=F(11), color="second700", margin=0, name="tool_label")
    box(s, X(713) - L(17), Y(213) - L(17), L(34), L(34), fill="second500", shape=MSO_SHAPE.OVAL,
        parts=[[("Tool", {"bold": True})]], size=F(10), color="white", margin=0, name="tool_badge")
    for k, (x, lab, kind) in enumerate([(340, "Escalation", "arrow"), (470, "AI agent", "ai"), (585, "{Actor 1}", "icon"),
                                        (700, "{Actor 2}", "icon")]):
        if kind == "arrow":
            soft_line(s, X(x), Y(495), X(x), Y(471), "negative", lw=2.25, arrow="tail", aw="lg", al="med")
        elif kind == "ai":
            box(s, X(x - 12), Y(471), L(24), L(24), fill="accent500", shape=MSO_SHAPE.OVAL,
                parts=[[("AI", {"bold": True})]], size=F(10), color="white", margin=0)
        else:
            icon(s, X(x), Y(483), L(24), "accent500", name=f"legend_{k}_icon")
        text(s, X(x + 18), Y(472), L(95), L(22), lab, size=F(12), color="grey600", anchor="m", margin=0,
             name=f"legend_{k}")


for fn in (d09, d10_fn.d10, d11, d12):
    fn()
prs.save(sys.argv[1])
print("saved")
