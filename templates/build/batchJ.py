"""Measured rebuild, designs d37-d41."""
import math, sys
from lib2 import *

prs = new_deck()


def ring_arc(s, cx, cy, r0, r1, a0, a1, fill, name=None, n=50, line=None, lw=0):
    outer = [(cx + r1 * math.cos(math.radians(a0 + (a1 - a0) * t / n)), cy - r1 * math.sin(math.radians(a0 + (a1 - a0) * t / n)))
             for t in range(n + 1)]
    inner = [(cx + r0 * math.cos(math.radians(a1 + (a0 - a1) * t / n)), cy - r0 * math.sin(math.radians(a1 + (a0 - a1) * t / n)))
             for t in range(n + 1)]
    return polyline(s, outer + inner, line, lw=lw, fill=fill, close=True, name=name)


# d37 five units, each with an arched header, levers and a coverage row ---------------------------------
def d37():
    s = slide(prs)
    header(s, "Each {unit} can capture the {benefits}", "{source}")
    f = Frame((15, 65, 1150, 690)); X, Y, L, F = f.X, f.Y, f.L, f.F
    cols = ["accent900", "accent700", "accent500", "accent400", "cat6"]
    on = ["11111", "11100", "00111", "11100", "11111"]
    for k, x0 in enumerate((30, 255, 480, 705, 930)):
        col = cols[k]; cx = x0 + 104
        ring_arc(s, X(cx), Y(103), L(47), L(57), 0, 180, col, name=f"unit_{k+1}_arch")
        box(s, X(x0), Y(103), L(207), L(484), fill="white", line=col, lw=1.25, name=f"unit_{k+1}")
        box(s, X(x0), Y(578), L(207), L(9), fill=col)
        icon(s, X(cx), Y(112), L(40), col, name=f"unit_{k+1}_icon")
        text(s, X(x0 + 8), Y(145), L(191), L(48), [[("{Unit}", {"bold": True})]], size=F(21), color=col, align="c",
             anchor="b", margin=0, name=f"unit_{k+1}_title")
        text(s, X(x0 + 15), Y(205), L(177), L(85), "{What the unit does, in three lines}", size=F(16.5), color="grey800",
             align="c", margin=0, name=f"unit_{k+1}_role")
        text(s, X(x0 + 15), Y(295), L(177), L(225), ["{Lever}", "", "{Lever}", "", "{Lever}"], size=F(16), color="grey600",
             align="c", margin=0, name=f"unit_{k+1}_levers")
        for j in range(5):
            dot(s, X(x0 + 26 + j * 39), Y(550), L(31), "accent500" if on[k][j] == "1" else "grey200")
            box(s, X(x0 + 26 + j * 39) - L(8), Y(550) - L(8), L(16), L(16), line="white", lw=1, shape=MSO_SHAPE.OVAL,
                name=f"unit_{k+1}_line_{j+1}")
    g = box(s, *f.R(30, 603, 1107, 33), fill="warm300", name="risk_bar",
            parts="{Scale: level of risk and potential reward}", size=F(18), color="text")
    g.fill.gradient(); g.fill.gradient_angle = 0
    st = g.fill.gradient_stops
    st[0].color.rgb = C("warm300"); st[0].position = 0
    st[1].color.rgb = C("accent400"); st[1].position = 1.0
    text(s, X(50), Y(605), L(30), L(28), [[("–", {"bold": True})]], size=F(22), color="text", margin=0)
    text(s, X(1100), Y(605), L(30), L(28), [[("+", {"bold": True})]], size=F(22), color="text", margin=0)
    text(s, X(70), Y(655), L(80), L(24), [[("Legend", {"bold": True})]], size=F(15), color="text", margin=0)
    for j, x in enumerate((165, 370, 580, 760, 950)):
        icon(s, X(x), Y(667), L(26), "grey600", name=f"legend_{j+1}_icon")
        text(s, X(x + 22), Y(655), L(160), L(24), "{Business line}", size=F(14.5), color="grey600", margin=0,
             name=f"legend_{j+1}")


# d38 four steps, the same architecture filled progressively ------------------------------------------------
def d38():
    s = slide(prs)
    header(s, "A {four-step} approach to building the {platform}", "{source}")
    f = Frame((15, 85, 1180, 560)); X, Y, L, F = f.X, f.Y, f.L, f.F
    heads = ["accent900", "accent700", "accent500", "accent300"]
    for k, x0 in enumerate((28, 318, 607, 890)):
        col = heads[k]
        text(s, X(x0), Y(88), L(120), L(22), [[(f"Step {k+1}:", {"bold": True})]], size=F(15), color=col, margin=0)
        c = soft_line(s, X(x0), Y(112), X(x0 + 285), Y(112), col, lw=1.25, dash=True)
        arrow_size(c, "tail", "sm", "sm", "arrow")
        icon(s, X(x0 + 25), Y(152), L(46), col, name=f"step_{k+1}_icon")
        text(s, X(x0 + 63), Y(130), L(205), L(66), "{What this step does, in two lines}", size=F(15.5), color="grey600",
             margin=0, name=f"step_{k+1}_text")
        lvl = k  # 0 nothing filled ... 3 everything filled
        G = lambda filled: dict(fill="accent100" if filled else None, line="accent500" if filled else "grey200", lw=1)
        bx = x0 - 3
        # use cases grid
        box(s, X(bx), Y(238), L(208), L(132), **G(lvl >= 3))
        for r, y in enumerate((241, 291, 309, 327)):
            for c_ in range(6):
                filled = lvl >= 3 or (lvl == 2 and (c_ < 3 or c_ == 5) and r < 3) or (lvl == 1 and c_ == 0)
                box(s, X(bx + 3 + c_ * 34), Y(y), L(31), L(16 if r else 22), **G(filled))
        box(s, X(bx + 3), Y(266), L(202), L(13), **G(lvl >= 2))
        box(s, X(bx + 70), Y(279), L(68), L(12), fill="white", parts="{Layer}", size=F(11), color="grey600", margin=0)
        box(s, X(bx + 3), Y(350), L(202), L(16), **G(lvl >= 1))
        text(s, X(bx + 3), Y(350), L(110), L(16), "{Layer}", size=F(11.5), color="grey600", align="c", margin=0)
        box(s, X(bx), Y(376), L(208), L(22), **G(lvl >= 1))
        text(s, X(bx), Y(378), L(140), L(18), "{Layer}", size=F(11.5), color="grey600", align="c", margin=0)
        box(s, X(bx), Y(404), L(208), L(86), **G(lvl >= 1))
        box(s, X(bx + 70), Y(405), L(68), L(12), fill="white" if lvl < 1 else "accent100", parts="{Layer}", size=F(11),
            color="grey600", margin=0)
        box(s, X(bx + 4), Y(419), L(12), L(66), **G(lvl >= 1))
        for r, (y, parts) in enumerate(((419, 2), (443, 3), (467, 1))):
            w = (185 - (parts - 1) * 4) / parts
            for j in range(parts):
                box(s, X(bx + 20 + j * (w + 4)), Y(y), L(w), L(18), **G(lvl >= 1 and not (lvl == 1 and r == 0 and j == 1)))
        for y in (352, 380):
            box(s, X(bx + 140), Y(y + 2), L(60), L(11), fill="white", line="grey200" if lvl < 3 else "accent500", lw=0.75)
        for y in (290, 380):
            box(s, X(bx + 219), Y(y), L(34), L(70), **G(lvl >= 2))
        if lvl == 1:
            box(s, X(bx + 2), Y(240), L(34), L(158), fill="accent100", line="accent500", lw=1)
        if lvl == 2:
            o = box(s, X(bx), Y(238), L(138), L(160), fill="accent100", line="accent500", lw=1)
            alpha(o, 70)
        box(s, X(bx + 214), Y(240), L(44), L(226), **G(lvl >= 2))
        t = text(s, X(bx + 236) - L(100), Y(353) - L(9), L(200), L(18), "{Interaction layer}", size=F(11.5),
                 color="grey600", align="c", margin=0)
        t.rotation = 270
        for j in range(5):
            box(s, X(bx + j * 42), Y(500), L(37), L(27), **G(lvl >= 3 or (lvl == 2 and j < 4) or (lvl == 1 and j < 2)))
        text(s, X(bx), Y(533), L(208), L(16), "{Source layer}", size=F(11.5), color="grey600", align="c", margin=0)


# d39 four maturity stages rising, with a wedge underneath ----------------------------------------------------
def d39():
    s = slide(prs)
    header(s, "{Maturity} progresses from {first stage} to {last stage}", "{source}")
    f = Frame((10, 115, 1350, 725)); X, Y, L, F = f.X, f.Y, f.L, f.F
    stages = [((18, 393), "grey100", "accent700"), ((356, 320), "accent100", "accent500"),
              ((694, 245), "second100", "second500"), ((1032, 172), "second100", "second700")]
    for k, ((x, y), fill, col) in enumerate(stages, 1):
        rrect(s, X(x), Y(y), L(312), L(297), 0.1, fill=fill, name=f"stage_{k}")
        box(s, X(x + 156 - 52), Y(y - 52), L(104), L(104), fill="white", line=col, lw=2.5, shape=MSO_SHAPE.OVAL)
        box(s, X(x + 156 - 34), Y(y - 34), L(68), L(68), fill={"accent700": "accent200", "accent500": "accent200",
            "second500": "second300", "second700": "second300"}[col], shape=MSO_SHAPE.OVAL, name=f"stage_{k}_icon")
        text(s, X(x + 10), Y(y + 62), L(292), L(32), [[("{Stage}", {"bold": True})]], size=F(22), color="text",
             align="c", margin=0, name=f"stage_{k}_title")
        soft_line(s, X(x + 133), Y(y + 97), X(x + 179), Y(y + 97), col, lw=2)
        text(s, X(x + 20), Y(y + 105), L(272), L(180), "{What characterises this stage, in three to four lines}",
             size=F(18), color="text", align="c", margin=0, name=f"stage_{k}_text")
    polyline(s, [(X(20), Y(722)), (X(1345), Y(662)), (X(1345), Y(722))], None, fill="accent900", close=True,
             name="maturity_wedge")
    text(s, X(950), Y(683), L(380), L(32), "{Axis label}", size=F(19), color="white", align="r", anchor="m", margin=0)


# d40 traditional vs enabled analysis per step, with time allocation ----------------------------------------
def d40():
    s = slide(prs)
    header(s, "{Technology} reshapes {activity} from {old mode} to {new mode}", "{source}")
    f = Frame2((10, 155, 1345, 810), body=(0.5, 1.05, 12.3, 5.7)); X, Y, W, H, D, F = f.X, f.Y, f.W, f.H, f.D, f.F
    text(s, X(15), Y(158), W(900), H(30), [[("{Example question the exhibit answers?}", {"bold": True})]], size=14,
         color="text", margin=0, name="example")
    xs = [142, 345, 540, 737, 932, 1128]
    for i in range(5):
        chevron(s, X(xs[i]), Y(202), W(xs[i + 1] - xs[i] + 6), H(88), W(14), first=(i == 0), fill="accent700",
                parts=[[("{Step}", {"bold": True})]], size=F(18.5), color="white", align="l", margin=0.12,
                name=f"step_{i+1}")
    chevron(s, X(1128), Y(202), W(212), H(88), W(14), fill="accent100", parts=[[("{Time allocation} ", {"bold": True}), ("(%)", {})]],
            size=12, color="text", margin=0.1, name="allocation_head")
    for r, (y0, y1, fill, tc, lab) in enumerate(((297, 530, "warm700", "white", "{Current mode}"),
                                                 (553, 808, "warm300", "text", "{New mode}"))):
        box(s, X(15), Y(y0), W(125), H(y1 - y0), fill=fill, parts=[[(lab, {"bold": True})]], size=F(18.5), color=tc,
            margin=0.05, name=f"row_{r+1}_label")
        for i in range(5):
            text(s, X(xs[i] + 10), Y(y0 + (15 if r == 0 else 30)), W(xs[i + 1] - xs[i] - 18), H(y1 - y0 - 35),
                 "{What happens at this step in this mode, in four to six lines}", size=F(17.5), color="grey600", margin=0,
                 name=f"row_{r+1}_step_{i+1}")
        rrect(s, X(1128), Y(y0 + 3), W(212), H(y1 - y0 - 6), 0.1, fill="accent50", name=f"row_{r+1}_allocation")
    soft_line(s, X(152), Y(545), X(1120), Y(545), "grey800", lw=1)
    box(s, X(653) - D(22), Y(545) - D(22), D(44), D(44), fill="accent900", shape=MSO_SHAPE.OVAL)
    elbow(s, [(X(653) - D(10), Y(545) - D(4)), (X(653), Y(545) + D(6)), (X(653) + D(10), Y(545) - D(4))], "white", lw=1.5)
    for r, (base, h1, h2) in enumerate(((470, 130, 33), (688, 13, 53))):
        for j, (bx, hh, fill) in enumerate(((1165, h1, "accent900"), (1260, h2, "accent300"))):
            box(s, X(bx), Y(base - hh), W(48), H(hh), fill=fill, name=f"row_{r+1}_bar_{j+1}")
            text(s, X(bx - 20), Y(base - hh - 30), W(88), H(26), [[("{v}", {"bold": True})]], size=F(19), color="text",
                 align="c", margin=0)
            text(s, X(bx - 30), Y(base + 8), W(108), H(44), "{Activity}", size=F(15), color="text", align="c", margin=0)


# d41 flywheel between two families of cards ------------------------------------------------------------------
def d41():
    s = slide(prs)
    header(s, "{Momentum}: we are starting to see the {flywheel} spin", "{sources}")
    f = Frame((30, 115, 1070, 690)); X, Y, L, F = f.X, f.Y, f.L, f.F
    cx, cy = X(548), Y(397)
    box(s, cx - L(126), cy - L(126), L(252), L(252), line="grey800", lw=1, shape=MSO_SHAPE.OVAL, dash=True)
    ring_arc(s, cx, cy, L(75), L(112), 90, 270, "accent700", name="half_left")
    ring_arc(s, cx, cy, L(75), L(112), -90, 90, "accent500", name="half_right")
    for sgn in (-1, 1):
        y_out, y_in = cy + sgn * L(112), cy + sgn * L(75)
        ym = (y_out + y_in) / 2
        polyline(s, [(cx - 0.02, y_out), (cx + 0.2 * -sgn, ym), (cx - 0.02, y_in), (cx - 0.08, y_in), (cx + 0.14 * -sgn - 0.06, ym),
                     (cx - 0.08, y_out)], None, fill="white", close=True)
    box(s, cx - L(73), cy - L(73), L(146), L(146), fill="accent100", line="white", lw=4, shape=MSO_SHAPE.OVAL,
        name="core", parts=[[("{Flywheel}", {"bold": True})], [("{name}", {"bold": True})]], size=F(15), color="text", margin=0.05)
    box(s, X(360), Y(370), L(115), L(58), fill="white", line="accent700", lw=1.25, name="left_family",
        parts=[[("{Family A}", {"bold": True})]], size=F(16), color="accent700")
    box(s, X(625), Y(370), L(112), L(58), fill="white", line="accent500", lw=1.25, name="right_family",
        parts=[[("{Family B}", {"bold": True})]], size=F(16), color="accent500")
    status = {"ok": "accent500", "up": "accent300", "wip": "grey400"}

    def badge(x, y, d, st):
        box(s, x - d / 2, y - d / 2, d, d, fill=status[st], line="white", lw=1, shape=MSO_SHAPE.OVAL, name=f"status_{st}")
        u = d / 4
        if st == "ok":
            elbow(s, [(x - u, y), (x - u * 0.2, y + u * 0.8), (x + u * 1.1, y - u * 0.8)], "white", lw=1.5, r=0)
        elif st == "up":
            soft_line(s, x, y + u * 1.1, x, y - u * 1.1, "white", lw=1.5, arrow="tail", aw="sm", al="sm")
        else:
            elbow(s, [(x, y - u * 1.1), (x, y), (x + u * 0.9, y)], "white", lw=1.5, r=0)
    def card(x, y0, y1, head_h, col, st, name, n_bul):
        box(s, X(x), Y(y0), L(288), L(y1 - y0), fill="white", line=col, lw=1, name=f"{name}_frame")
        box(s, X(x), Y(y0), L(288), L(head_h), fill=col, name=f"{name}_head",
            parts=[[("{Item}: ", {"bold": True}), ("{headline}", {})]], size=F(14.5), color="white", align="l", margin=0.1)
        badge(X(x + 262), Y(y0 + head_h / 2), L(22), st)
        t = text(s, X(x + 12), Y(y0 + head_h + 8), L(266), L(y1 - y0 - head_h - 12), ["• {proof point}"] * n_bul,
                 size=11, color="grey600", margin=0, name=f"{name}_text")
        for para in t.text_frame.paragraphs:
            para.space_before = Pt(4)
            pPr = para._p.get_or_add_pPr(); pPr.set("marL", str(int(I(0.15)))); pPr.set("indent", str(-int(I(0.15))))
    left = [(125, 272, 32, "ok", 2), (340, 466, 32, "wip", 2), (532, 669, 52, "up", 1)]
    for k, (y0, y1, hh, st, nb) in enumerate(left, 1):
        card(37, y0, y1, hh, "accent700", st, f"left_{k}", nb)
    right = [(125, 240, 32, "up", 3), (255, 345, 32, "up", 2), (358, 440, 32, "wip", 2), (462, 555, 32, "up", 2),
             (568, 670, 52, "up", 1)]
    for k, (y0, y1, hh, st, nb) in enumerate(right, 1):
        card(768, y0, y1, hh, "accent500", st, f"right_{k}", nb)
    G = dict(lw=1)
    soft_line(s, X(325), Y(141), X(340), Y(141), "accent700", **G); soft_line(s, X(325), Y(355), X(340), Y(355), "accent700", **G)
    soft_line(s, X(325), Y(557), X(340), Y(557), "accent700", **G)
    soft_line(s, X(340), Y(141), X(340), Y(557), "accent700", **G); soft_line(s, X(340), Y(401), X(360), Y(401), "accent700", **G)
    dot(s, X(360), Y(401), L(8), "white", "accent700")
    soft_line(s, X(755), Y(141), X(755), Y(610), "accent500", **G)
    for y in (141, 271, 374, 479, 594):
        soft_line(s, X(755), Y(y), X(768), Y(y), "accent500", **G)
    soft_line(s, X(737), Y(401), X(755), Y(401), "accent500", **G); dot(s, X(737), Y(401), L(8), "white", "accent500")
    for k, (y, st) in enumerate(((597, "ok"), (630, "up"), (662, "wip")), 1):
        badge(X(398), Y(y), 0.22, st)
        text(s, X(414), Y(y - 10), L(300), L(20), "{What this status means}", size=11, color="grey600", margin=0,
             name=f"legend_{k}")


for fn in (d37, d38, d39, d40, d41):
    fn()
prs.save(sys.argv[1])
print("saved")
