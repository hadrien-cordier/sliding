"""Measured rebuild, designs d17-d20."""
import math, sys
from lib2 import *

prs = new_deck()


# d17 value chain x activity heatmap with three automation levels ---------------------------------------
def d17():
    s = slide(prs)
    header(s, "In an {AI-first operating model}, {AI} executes most tasks while {people} focus on {judgment}",
           "{source}", "{Scope of the example}")
    f = Frame2((10, 132, 850, 622), body=(0.5, 1.35, 12.3, 5.35)); X, Y, W, H, D, F = f.X, f.Y, f.W, f.H, f.D, f.F
    cols = [15, 132, 250, 368, 486, 604, 722, 840]
    cat = {"A": "accent700", "G": "accent900", "H": "accent400"}
    grid = ["AAAAAAA", "AAGAAGA", "GGGGGGG", "HHHHHHG"]
    for c in range(7):
        x0, x1 = cols[c], cols[c + 1]
        if c < 6:
            chevron(s, X(x0), Y(137), W(x1 - x0 + 12), H(85), W(14), first=(c == 0), fill="grey200", name=f"stage_{c+1}")
        else:
            polyline(s, [(X(x0), Y(137)), (X(836), Y(137)), (X(836), Y(222)), (X(x0), Y(222)), (X(x0 + 14), Y(179.5))],
                     None, fill="grey200", close=True, name=f"stage_{c+1}")
        text(s, X(x0 + 10 + (0 if c == 0 else 12)), Y(144), W(x1 - x0 - 30), H(74),
             [[("{Stage}", {"bold": True})], [("{Up to n% capacity unlock}", {"size": F(12)})]], size=F(13),
             color="text", margin=0, name=f"stage_{c+1}_label")
        for r, (y0, y1) in enumerate(((226, 288), (292, 354), (358, 419), (423, 485))):
            rrect(s, X(x0), Y(y0), W(x1 - x0 - 4), H(y1 - y0), 0.06, fill=cat[grid[r][c]], parts="{Activity}", size=F(12),
                color="white", align="l", anchor="t", margin=0.1, name=f"cell_{r+1}_{c+1}")
    rrect(s, *f.R(15, 489, 821, 66), H(6), fill="grey100", name="support_band")
    text(s, X(23), Y(493), W(105), H(60), [[("{Support}", {"bold": True})], "{Up to n%", "capacity unlock}"], size=F(11.5),
         color="text", margin=0, name="support_label")
    for k, ((x0, x1), c) in enumerate(zip(((132, 262), (268, 398), (410, 543), (552, 683), (692, 822)), "AAGGG"), 1):
        rrect(s, X(x0), Y(501), W(x1 - x0), H(42), H(7), fill=cat[c], parts="{Activity}", size=F(12), color="white",
              align="l", margin=0.08, name=f"support_{k}")
    text(s, X(500), Y(112), W(336), H(20), [[("{Scope of the example}", {"italic": True})]], size=11, color="grey600",
         align="r", margin=0, name="scope_tag")
    for k, (x, c, lab) in enumerate(((78, "A", "{Level 1 (share AI)}"), (305, "G", "{Level 2 (share AI)}"),
                                     (552, "H", "{Level 3 (share AI)}")), 1):
        box(s, X(x), Y(578), W(12), H(12), fill=cat[c])
        text(s, X(x + 20), Y(571), W(230), H(55), [[(lab, {"size": F(13), "color": "text"})], "{What this level means}"],
             size=F(12), color="grey600", margin=0, name=f"legend_{k}")


# d18 four overlapping evaluation dimensions ----------------------------------------------------------------
def d18():
    s = slide(prs)
    header(s, "{Method} is essential to assess {quality} across {factors}", "{source}")
    f = Frame((340, 190, 980, 790)); X, Y, L, F = f.X, f.Y, f.L, f.F
    r = 152
    pos = {1: (531, 362), 2: (781, 362), 3: (531, 617), 4: (781, 617)}
    style = {1: ("accent700", "white"), 2: ("accent500", "white"), 3: ("accent300", "grey800"), 4: ("accent100", "grey800")}
    for k in (4, 3, 2, 1):
        cx, cy = pos[k]
        c = box(s, X(cx - r), Y(cy - r), L(2 * r), L(2 * r), fill=style[k][0], shape=MSO_SHAPE.OVAL, name=f"dimension_{k}")
        alpha(c, 12)
    # lens of the two top circles, darkest, as in the reference
    (ax, ay), (bx, by) = pos[1], pos[2]
    d = bx - ax; h = math.sqrt(r * r - (d / 2) ** 2); half = math.degrees(math.atan2(h, d / 2))
    left = [(X(ax + r * math.cos(math.radians(a))), Y(ay - r * math.sin(math.radians(a)))) for a in
            [-half + 2 * half * t / 30 for t in range(31)]]
    right = [(X(bx + r * math.cos(math.radians(a))), Y(by - r * math.sin(math.radians(a)))) for a in
             [180 - half + 2 * half * t / 30 for t in range(31)]]
    polyline(s, left + right, None, fill="accent900", close=True, name="lens_top")
    for k, (cx, cy) in pos.items():
        t = text(s, X(cx - 120), Y(cy - 78), L(240), L(170), [[("{Dimension}", {"bold": True, "size": 20})],
                                                              "{metric}", "{metric}", "{metric}"],
                 size=14, color=style[k][1], align="c", margin=0, name=f"dimension_{k}_text")
        for i, para in enumerate(t.text_frame.paragraphs):
            para.line_spacing = 1.3
            if i == 1:
                para.space_before = Pt(4)


# d19 before/after flows with the same entry and exit ------------------------------------------------------
def d19():
    s = slide(prs)
    header(s, "{Technology} can substantially reduce {effort} in {process}", "{source}")
    f = Frame((10, 195, 1345, 810)); X, Y, L, F = f.X, f.Y, f.L, f.F
    A = dict(lw=1.25, arrow="tail", aw="sm", al="sm")
    def node(x, y, w, fill, tc, lab, name, h=46):
        b = box(s, X(x), Y(y), L(w), L(h), fill=fill, name=name)
        if w < 300:
            icon(s, X(x + w / 2 - 95), Y(y + h / 2), L(26), tc, name=f"{name}_icon")
            text(s, X(x + w / 2 - 72), Y(y), L(w / 2 + 70), L(h), [[(lab, {"bold": True})]], size=F(16), color=tc,
                 anchor="m", margin=0)
        else:
            icon(s, X(x + w / 2 - 125), Y(y + h / 2), L(26), tc, name=f"{name}_icon")
            text(s, X(x + w / 2 - 100), Y(y), L(260), L(h), [[(lab, {"bold": True})]], size=F(16), color=tc, anchor="m",
                 margin=0)
        return b
    text(s, X(60), Y(200), L(520), L(32), [[("{Current process}", {"bold": True})]], size=F(21), color="accent700",
         align="c", margin=0, name="before_title")
    text(s, X(785), Y(200), L(520), L(32), [[("{Target process}", {"bold": True})]], size=F(21), color="accent500",
         align="c", margin=0, name="after_title")
    for x, nm in ((185, "before_entry"), (910, "after_entry")):
        node(x, 255, 283, "accent100", "accent700", "{ENTRY}", nm, 45)
    elbow(s, [(X(326), Y(300)), (X(326), Y(330))], "accent700", lw=1.25)
    elbow(s, [(X(157), Y(330)), (X(475), Y(330))], "accent700", lw=1.25)
    for x in (157, 475):
        soft_line(s, X(x), Y(330), X(x), Y(352), "accent700", **A)
    rows = [(360, "accent700", "white", "{AUTOMATED CHECK}"), (437, "accent100", "accent700", "{MANUAL REVIEW}"),
            (515, "accent700", "white", "{AUTOMATED CHECK}"), (592, "accent100", "accent700", "{MANUAL REVIEW}")]
    for i, (y, fill, tc, lab) in enumerate(rows):
        for j, x in enumerate((17, 335)):
            node(x, y, 282, fill, tc, lab, f"before_{i+1}_{j+1}")
            if i < 3:
                soft_line(s, X(x + 141), Y(y + 46), X(x + 141), Y(rows[i + 1][0] - 6), "accent700", **A)
    for x in (158, 476):
        soft_line(s, X(x), Y(638), X(x), Y(663), "accent700", **A)
    node(17, 669, 374, "accent700", "white", "{CONTROL FUNCTION}", "before_5_1")
    node(391, 669, 226, "accent100", "accent700", "{RISK}", "before_5_2")
    soft_line(s, X(317), Y(715), X(317), Y(752), "accent700", **A)
    node(176, 758, 282, "accent700", "white", "{DECISION}", "before_exit")
    elbow(s, [(X(1051), Y(300)), (X(1051), Y(330))], "accent500", lw=1.25)
    elbow(s, [(X(882), Y(330)), (X(1200), Y(330))], "accent500", lw=1.25)
    for x in (882, 1200):
        soft_line(s, X(x), Y(330), X(x), Y(352), "accent500", **A)
    box(s, *f.R(741, 406, 600, 222), fill="accent50", name="after_container")
    node(741, 360, 600, "accent500", "white", "{AGENTIC STEP}", "after_step")
    for i, x in enumerate((750, 947, 1145)):
        for r, y in enumerate((448, 553)):
            rrect(s, X(x), Y(y), L(190), L(64), L(3), fill="accent150", name=f"after_tile_{r+1}_{i+1}")
            icon(s, X(x + 26), Y(y + 32), L(30), "accent500", name=f"after_tile_{r+1}_{i+1}_icon")
            text(s, X(x + 46), Y(y), L(140), L(64), [[("{INPUT}" if r == 0 else "{OUTPUT}", {"bold": True})]],
                 size=F(16), color="accent500", anchor="m", margin=0)
        soft_line(s, X(x + 95), Y(410), X(x + 95), Y(440), "accent500", **A)
        soft_line(s, X(x + 95), Y(515), X(x + 95), Y(546), "accent500", **A)
    soft_line(s, X(1041), Y(632), X(1041), Y(662), "accent500", **A)
    node(741, 669, 600, "accent500", "white", "{FINAL REVIEW}", "after_review")
    soft_line(s, X(1043), Y(715), X(1043), Y(752), "accent500", **A)
    node(903, 758, 282, "accent500", "white", "{DECISION}", "after_exit")


# d20 maturity curve with distribution and player tags ------------------------------------------------------
def d20():
    s = slide(prs)
    header(s, "{Actors} lag in {scaling capability}", "{survey source}",
           "{Stages and current distribution}; illustrative")
    f = Frame((10, 165, 1345, 830), body=(0.5, 1.05, 12.3, 5.75)); X, Y, F = f.X, f.Y, f.F
    W = H = f.L; D = lambda p: f.L(p) * 0.95
    cur = bez((X(12), Y(446)), (X(700), Y(440)), (X(1010), Y(400)), (X(1133), Y(205)), 60)
    c = polyline(s, cur, "grey400", lw=1, name="maturity_curve"); round_caps(c)
    stages = [(179, 292, 387, "accent300", "text"), (511, 274, 367, "accent500", "accent500"),
              (845, 243, 335, "accent700", "accent700"), (1175, 192, 281, "accent900", "accent900")]
    for k, (cx, ny, dy, fill, tc) in enumerate(stages, 1):
        text(s, X(cx - 110), Y(ny - 14), W(220), H(26), [[("{Stage}", {"bold": True})]], size=F(19),
             color="grey600" if k == 1 else tc, align="c", margin=0, name=f"stage_{k}")
        text(s, X(cx - 110), Y(ny + 12), W(220), H(24), "({share})", size=F(16), color="grey600", align="c", margin=0,
             name=f"stage_{k}_share")
        icon(s, X(cx), Y(dy), D(86), "white" if k > 1 else fill, fill=fill, name=f"stage_{k}_icon")
    for (x, y, col) in ((354, 283, "accent300"), (672, 262, "accent500"), (1008, 213, "accent700")):
        b = chevron(s, X(x) - 0.125, Y(y) - 0.225, 0.25, 0.45, 0.14, fill=col)
    for k, (x, y, n) in enumerate(((50, 476, 2), (389, 462, 4), (703, 446, 2), (1047, 370, 2)), 1):
        paras = []
        for i in range(n):
            paras += ([""] if i else []) + ["{Criterion for this stage}"]
        text(s, X(x), Y(y), W(285), H(220), paras, size=F(16), color="grey600", margin=0, name=f"stage_{k}_criteria")
    tags = [((18, 672), "accent300", "text"), ((350, 672), "accent500", "white"), ((350, 727), "accent500", "white"),
            ((350, 781), "accent500", "white"), ((683, 672), "accent700", "white"), ((1014, 672), "accent900", "white")]
    for k, ((x, y), fill, tc) in enumerate(tags, 1):
        rrect(s, X(x), Y(y), W(322), H(51), 0.05, fill=fill, parts="{Type of player}", size=F(17), color=tc, margin=0,
              name=f"player_tag_{k}")


for fn in (d17, d18, d19, d20):
    fn()
prs.save(sys.argv[1])
print("saved")
