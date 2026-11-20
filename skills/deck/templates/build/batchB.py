"""Measured rebuild, designs d05-d08, placed on the reference pixels."""
import sys
from lib2 import *

prs = new_deck()


# d05 chevron band with pain points ------------------------------------------------------------
def d05():
    s = slide(prs)
    header(s, "Pain points cluster along the {process}", "{source}")
    f = Frame((0, 150, 1344, 702)); X, Y, L, F = f.X, f.Y, f.L, f.F
    bounds = [0, 105, 310, 510, 680, 915, 1110, 1290]
    depth = 45
    for i in range(7):
        x0, x1 = bounds[i], bounds[i + 1]
        b = chevron(s, X(x0), Y(245), L(x1 - x0 + depth), L(110), L(depth), first=(i == 0), fill="accent500",
                    line="white", lw=2.5, parts=[[("{Stage}", {"bold": True})]], size=F(19), color="white",
                    margin=0.05, name=f"stage_{i+1}")
        icon(s, X((x0 + x1) / 2 + 12), Y(197), L(58), "accent500", name=f"stage_{i+1}_icon")
    groups = [(33, 280), (340, 330), (703, 200), (930, 170), (1128, 200)]
    for g, (x, w) in enumerate(groups, 1):
        text(s, X(x), Y(385), L(w), L(270),
             [[("{Pain point}: ", {"bold": True, "color": "accent500"}), ("{what goes wrong}", {})],
              [("", {"size": F(14)})],
              [("{Pain point}: ", {"bold": True, "color": "accent500"}), ("{what goes wrong}", {})]],
             size=F(18.5), color="grey600", margin=0, name=f"pains_{g}")
    for x in (307, 680, 912, 1107):
        soft_line(s, X(x), Y(360), X(x), Y(570), "accent500", lw=1, dash=True)


# d06 two lanes ----------------------------------------------------------------------------------
def d06():
    s = slide(prs)
    header(s, "Today {the work waits for a person}, with {change} {it stays current}", "{source}",
           "{Scope of the representation}; figures are indicative ranges")
    f = Frame((0, 165, 1344, 725)); X, Y, L, F = f.X, f.Y, f.L, f.F
    for xl, xa, xb in ((263, 410, 318), (594, 740, 648)):
        text(s, X(xl), Y(170), L(220), L(24), "{Backward flow}", size=F(18), color="grey600", margin=0)
        c = soft_line(s, X(xa), Y(200), X(xb), Y(200), "accent500", lw=1.25)
        arrow_size(c, "tail", "med", "med", "arrow")
    text(s, X(10), Y(212), L(500), L(26), [[("{CURRENT}: {SEQUENTIAL}", {"bold": True})]], size=F(19), margin=0,
         name="lane_1_label")
    for (xa, xb) in ((497, 228), (888, 500)):
        c = curve(s, (X(xa), Y(272)), (X(xa - (xa - xb) * 0.25), Y(232)), (X(xb + (xa - xb) * 0.25), Y(232)), (X(xb), Y(272)),
                  "accent500", lw=1.25, dash=True)
        arrow_size(c, "tail", "med", "med", "arrow")
    bounds = [10, 225, 450, 675, 900, 1125, 1337]
    for i in range(6):
        x0, x1 = bounds[i], bounds[i + 1]
        chevron(s, X(x0), Y(280), L(x1 - x0 - 8), L(68), L(22), first=(i == 0), fill="current",
                parts=["{Step}", "{second line}"], size=F(18.5), color="text", margin=0.04, name=f"current_step_{i+1}")
    box(s, X(10), Y(360), L(1327), L(18), fill="accent500", name="time_bar")
    text(s, X(10), Y(384), L(600), L(24), "{Elapsed time to outcome}", size=F(18), margin=0)
    text(s, X(1100), Y(384), L(237), L(24), [[("{Weeks}", {"bold": True})]], size=F(18), align="r", margin=0,
         name="time_unit")
    soft_line(s, X(10), Y(427), X(1337), Y(427), "grey200", lw=1)
    text(s, X(10), Y(445), L(600), L(26), [[("{TARGET}: {CONTINUOUS}", {"bold": True})]], size=F(19), margin=0,
         name="lane_2_label")
    text(s, X(10), Y(476), L(1300), L(28), [[("{What changes for people, in one line}", {"bold": True})]], size=F(21),
         margin=0, name="lane_2_message")
    ramp = [("accent100", "text"), ("accent300", "text"), ("accent500", "text"), ("accent700", "white")]
    tb = [10, 280, 552, 825, 1085]
    for i, (fc, tc) in enumerate(ramp):
        chevron(s, X(tb[i]), Y(532), L(tb[i + 1] - tb[i] - 7), L(81), L(24), first=(i == 0), fill=fc,
                parts=[[("{Step}", {"bold": True})], [("{what it does}", {"size": F(16)})]], size=F(19.5), color=tc,
                margin=0.04, name=f"target_step_{i+1}")
    rrect(s, X(1093), Y(512), L(244), L(118), L(10), fill="accent900", name="value_box",
          parts=[[("{Value released}", {"bold": True})], [("{to whom or to what}", {"size": F(15.5)})]], size=F(19.5),
          color="white")
    for k, x in enumerate((38, 392, 745)):
        rrect(s, X(x), Y(633), L(296), L(85), L(6), fill="white", line="grey400", lw=1.25, name=f"kpi_{k+1}",
              parts=[[("{value}", {"bold": True, "size": F(21)})], "{what it measures}"], size=F(16.5), color="text")


# d07 lifecycle, solutions, shared layers --------------------------------------------------------
def d07():
    s = slide(prs)
    header(s, "Many {solutions}, shared {capabilities}, one {foundation}", "{source}",
           "{Scope}; solution set is illustrative and non-exhaustive")
    f = Frame((0, 172, 1360, 600)); X, Y, L, F = f.X, f.Y, f.L, f.F
    bounds = [25, 247, 470, 692, 915, 1137, 1352]
    for i in range(6):
        x0, x1 = bounds[i], bounds[i + 1]
        if i < 5:
            chevron(s, X(x0), Y(187), L(x1 - x0 - 6 + 16), L(61), L(16), first=(i == 0), fill="accent900",
                    parts=[[("{Stage}", {"bold": True})]], size=F(20), color="white", margin=0.04, name=f"stage_{i+1}")
        else:
            pts = [(X(x0), Y(187)), (X(1352), Y(187)), (X(1352), Y(248)), (X(x0), Y(248)), (X(x0 + 16), Y(217.5))]
            polyline(s, pts, None, fill="accent900", close=True, name=f"stage_{i+1}")
            text(s, X(x0 + 16), Y(187), L(1352 - x0 - 16), L(61), [[("{Stage}", {"bold": True})]], size=F(20),
                 color="white", align="c", anchor="m", margin=0)
        for r, y in enumerate((260, 332)):
            if (i, r) == (4, 1):
                continue
            rrect(s, X(x0), Y(y), L((1352 - x0) if i == 5 else (x1 - x0 - 7)), L(60), L(8), fill="accent100", parts="{Solution}", size=F(17),
                  color="text", name=f"solution_{i+1}_{r+1}")
    rrect(s, X(25), Y(405), L(1327), L(88), L(8), fill="accent300", name="shared_layer",
          parts=[[("{Shared capabilities, built once and reused}", {"bold": True})],
                 [("{list of the shared capabilities}", {"size": F(17.5)})]], size=F(21), color="text")
    rrect(s, X(25), Y(506), L(1327), L(87), L(8), fill="current", name="foundation_layer",
          parts=[[("{Shared foundation}", {"bold": True})],
                 [("{data, controls and governance every solution relies on}", {"size": F(17.5)})]], size=F(21),
          color="text")


# d08 forces, squeeze, solution ------------------------------------------------------------------
def d08():
    s = slide(prs)
    header(s, "{Three forces} create a {squeeze} that {two levers} resolve together", "{source}")
    f = Frame((0, 112, 1348, 812)); X, Y, L, F = f.X, f.Y, f.L, f.F
    def card(x, y, w, head_h, body_h, col, name):
        rrect(s, X(x), Y(y), L(w), L(head_h + body_h), L(20), fill="white", line=col, lw=1.5, name=f"{name}_frame")
        top_round(s, X(x), Y(y), L(w), L(head_h), L(20), fill=col, name=f"{name}_head")
        icon(s, X(x + 58), Y(y + head_h / 2), L(66), "white", name=f"{name}_icon")
        text(s, X(x + 118), Y(y + 8), L(w - 130), L(head_h - 16), [[("{Force or lever}", {"bold": True})]],
             size=F(25), color="white", anchor="m", margin=0, name=f"{name}_title")
        text(s, X(x + 20), Y(y + head_h + 8), L(w - 40), L(body_h - 16),
             "{One sentence on what it does to the organisation}", size=F(21), color="grey600", align="c",
             anchor="m", margin=0, name=f"{name}_text")
    for k, x in enumerate((18, 473, 928), 1):
        card(x, 125, 416, 90, 117, "accent500", f"force_{k}")
    J = lambda x, y, col: dot(s, X(x), Y(y), L(12), "white", col, lw=1.5)
    for xa, xb in ((434, 473), (889, 928)):
        soft_line(s, X(xa), Y(262), X(xb), Y(262), "accent500", lw=1.5)
    rrect(s, X(363), Y(365), L(637), L(175), L(42), line="accent500", lw=1.5, name="squeeze_frame")
    for xg in (360, 997):
        box(s, X(xg), Y(418), L(7), L(58), fill="white")
    rrect(s, X(380), Y(381), L(605), L(144), L(10), fill="white", line="accent500", lw=1.25, name="squeeze_body",
          parts=["", "", "{Rising demands collide with constrained resources}"], size=F(19), color="grey600")
    top_round(s, X(380), Y(381), L(605), L(66), L(10), fill="accent900", name="squeeze_head",
              parts=[[("{The squeeze}", {"bold": True})]], size=F(26), color="white")
    elbow(s, [(X(222), Y(332)), (X(222), Y(404)), (X(363), Y(404))], "accent500", lw=1.5, r=0.08); J(363, 404, "accent500")
    soft_line(s, X(679), Y(332), X(679), Y(365), "accent500", lw=1.5); J(679, 365, "accent500")
    elbow(s, [(X(1140), Y(332)), (X(1140), Y(404)), (X(1000), Y(404))], "accent500", lw=1.5, r=0.08); J(1000, 404, "accent500")
    soft_line(s, X(679), Y(540), X(679), Y(663), "accent700", lw=1.5); J(679, 540, "accent700")
    rrect(s, X(522), Y(663), L(318), L(94), L(22), fill="accent700", name="solution_pill")
    icon(s, X(575), Y(710), L(52), "white", name="solution_icon")
    text(s, X(610), Y(680), L(220), L(60), [[("{The solution}", {"bold": True})]], size=F(26), color="white",
         anchor="m", margin=0, name="solution_label")
    card(18, 573, 416, 90, 143, "accent700", "lever_1")
    card(928, 573, 416, 90, 143, "accent700", "lever_2")
    soft_line(s, X(434), Y(710), X(522), Y(710), "accent700", lw=1.5); J(522, 710, "accent700")
    soft_line(s, X(840), Y(710), X(928), Y(710), "accent700", lw=1.5); J(840, 710, "accent700")


for fn in (d05, d06, d07, d08):
    fn()
prs.save(sys.argv[1])
print("saved")
