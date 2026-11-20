"""Measured rebuild, designs d25-d28."""
import math, sys
from lib2 import *

prs = new_deck()


# d25 staged model with a tapering band that points to the end state ------------------------------------
def d25():
    s = slide(prs)
    header(s, "{End state}: {approach} embraced to its full potential", "{source}", "{Client example}")
    f = Frame2((30, 215, 1095, 845)); X, Y, W, H, D, F = f.X, f.Y, f.W, f.H, f.D, f.F
    for n, x in ((1, 60), (2, 428), (3, 625), (4, 830)):
        text(s, X(x - 8), Y(212), W(60), H(52), str(n), size=F(40), color="grey600", anchor="b", margin=0, name=f"stage_{n}_number")
    for k, (x0, w) in enumerate(((37, 368), (407, 197), (606, 201), (809, 272)), 1):
        box(s, X(x0), Y(273), W(w), H(78), fill="grey200", name=f"stage_{k}",
            parts=[[("{STAGE NAME ON}", {"bold": True})], [("{TWO LINES}", {"bold": True})]], size=12, color="text", align="l", margin=0.15)
    band = [(X(210), Y(497)), (X(800), Y(555)), (X(800), Y(630)), (X(822), Y(665)), (X(800), Y(700)), (X(800), Y(790)),
            (X(210), Y(845))]
    polyline(s, band, None, fill="accent100", close=True, name="progress_band")
    for x in (405, 605):
        soft_line(s, X(x), Y(480), X(x), Y(850), "white", lw=2)
    for k, x in enumerate((55, 228, 427, 624, 835), 1):
        icon(s, X(x + 22), Y(395), D(52), "accent700", fill="accent300", name=f"lever_{k}_icon")
        text(s, X(x), Y(442), W(170), H(50), [[("{Lever}", {"bold": True})]], size=F(17), color="text", margin=0,
             name=f"lever_{k}")
    for k, (x, y, n) in enumerate(((55, 555, 1), (228, 610, 2), (427, 575, 2), (624, 575, 2), (835, 528, 4)), 1):
        paras = []
        for i in range(n):
            paras += ([""] if i else []) + ["{Action in a few words}"]
        text(s, X(x), Y(y), W(165 if k < 5 else 230), H(260), paras, size=F(17), color="text", margin=0,
             name=f"lever_{k}_actions")


# d26 maturity curve with phases, then the key levers by phase ----------------------------------------
def d26():
    s = slide(prs)
    header(s, "{Capability} has evolved beyond {first purpose} into {current form}", "{source}")
    f = Frame((25, 150, 1075, 695)); X, Y, L, F = f.X, f.Y, f.L, f.F
    for k, (y0, y1) in enumerate(((170, 326), (328, 494), (497, 645)), 1):
        box(s, X(28), Y(y0), L(82), L(y1 - y0), fill="accent700", parts="{Phase}", size=F(17), color="white", margin=0.04,
            name=f"phase_{k}")
    box(s, *f.R(133, 170, 297, 475), fill="accent150", name="curve_panel")
    for c in (soft_line(s, X(120), Y(655), X(120), Y(158), "grey300", lw=1.25),
              soft_line(s, X(120), Y(655), X(1072), Y(655), "grey300", lw=1.25)):
        arrow_size(c, "tail", "med", "med", "arrow")
    text(s, X(122), Y(672), L(200), L(22), "{X-AXIS START}", size=F(15), color="text", margin=0)
    text(s, X(872), Y(672), L(200), L(22), "{X-AXIS END}", size=F(15), color="text", align="r", margin=0)
    curve(s, (X(155), Y(635)), (X(185), Y(430)), (X(250), Y(290)), (X(405), Y(238)), "accent700", lw=1.75,
          arrow="tail", aw="lg", al="lg")
    for k, (x, y) in enumerate(((161, 600), (187, 482), (251, 346), (386, 246)), 1):
        dot(s, X(x), Y(y), L(11), "accent900")
        tx = x - 130 if k == 4 else x + 12
        text(s, X(tx), Y(y - 12), L(118), L(24), "{period}", size=F(15), color="text", margin=0,
             align="r" if k == 4 else "l", name=f"period_{k}")
    text(s, X(710), Y(143), L(300), L(24), [[("{Key levers}", {"bold": True})]], size=F(17), color="accent700", margin=0)
    rows = [171, 291, 411, 532, 650]
    for k in range(4):
        y0, y1 = rows[k], rows[k + 1]
        soft_line(s, X(440), Y(y0), X(1062), Y(y0), "grey200", lw=1, name=f"lever_{k+1}_rule")
        icon(s, X(472), Y((y0 + y1) / 2), L(52), "accent700", fill="accent300", name=f"lever_{k+1}_icon")
        text(s, X(521), Y(y0 + 10), L(175), L(y1 - y0 - 20), [[("{Lever}", {"bold": True})]], size=F(18),
             color="accent700", anchor="m", margin=0, name=f"lever_{k+1}")
        text(s, X(710), Y(y0 + 12), L(355), L(y1 - y0 - 18),
             [[("{What changes}", {"bold": True})], "· {proof point}", "· {proof point}", "· {proof point}"],
             size=F(14.5), color="text", margin=0, name=f"lever_{k+1}_text")


# d27 manifesto, then the inverted funnel of capabilities ----------------------------------------------------
def d27():
    s = slide(prs)
    header(s, "{Successful outcome} starts with {approach} that leverages {capability}", "{source}")
    f = Frame((15, 165, 1090, 595)); X, Y, L, F = f.X, f.Y, f.L, f.F
    text(s, X(20), Y(170), L(480), L(26), [[("{The promise}…", {"bold": True})]], size=F(17), color="text", margin=0,
         name="left_title")
    for k, y in enumerate((250, 348, 446, 544), 1):
        icon(s, X(48), Y(y), L(52), "accent700", fill="accent300", name=f"promise_{k}_icon")
        text(s, X(115), Y(y - 32), L(360), L(66),
             [[("{We commit to} ", {}), ("{key phrase}", {"bold": True}), (": {how we deliver it}", {})]],
             size=F(16), color="text", anchor="m", margin=0, name=f"promise_{k}")
    text(s, X(535), Y(170), L(480), L(26), [[("…{requires these capabilities}", {"bold": True})]], size=F(17),
         color="text", margin=0, name="right_title")
    tiers = [(210, 293, "accent900", "white"), (305, 388, "accent700", "white"), (400, 483, "accent500", "white"),
             (494, 577, "accent300", "text")]
    slope = (1065 - 1002 - 12) / (577 - 210)
    rows = []
    for y0, y1, fill, tc in tiers:
        a, b = 535 + (y0 - 210) * slope, 1065 - (y0 - 210) * slope
        c, d = 535 + (y1 - 210) * slope, 1065 - (y1 - 210) * slope
        rows.append(((a, b, c, d), y0, y1, fill, tc))
    for k, ((a, b, c, d), y0, y1, fill, tc) in enumerate(rows, 1):
        polyline(s, [(X(a), Y(y0)), (X(b), Y(y0)), (X(d), Y(y1)), (X(c), Y(y1))], None, fill=fill, close=True,
                 name=f"capability_{k}")
        text(s, X(c + 20), Y(y0), L(d - c - 40), L(y1 - y0), [[("{Capability}", {"bold": True})], "{What it means for the customer}"],
             size=F(15.5), color=tc, align="c", anchor="m", margin=0, name=f"capability_{k}_text")


# d28 architecture in columns, from sources to channels -------------------------------------------------------
def d28():
    s = slide(prs)
    header(s, "{Architecture} to enable {capability} across every {touchpoint}", "{source}", "{Client example}")
    f = Frame2((10, 150, 810, 830), body=(1.4, 1.1, 10.5, 5.65)); X, Y, W, H, D, F = f.X, f.Y, f.W, f.H, f.D, f.F
    G = dict(lw=1, color="grey400")
    for k, (cx, lab) in enumerate(((215, "{Layer 1}"), (410, "{Layer 2}"), (575, "{Layer 3}"), (737, "{Layer 4}")), 1):
        icon(s, X(cx), Y(178), D(46), "accent700", fill="accent300", name=f"layer_{k}_icon")
        text(s, X(cx - 80), Y(212), W(160), H(48), [[(lab, {"bold": True})]], size=F(16), color="text", align="c",
             margin=0, name=f"layer_{k}")
    for x, w in ((110, 212), (345, 138), (505, 140), (668, 137)):
        box(s, X(x), Y(268), W(w), H(382), fill="grey100")
    rrect(s, *f.R(15, 270, 73, 170), 0.06, fill="accent100", name="sources")
    icon(s, X(50), Y(300), D(34), "accent700", name="sources_icon")
    text(s, X(22), Y(345), W(64), H(80), "{Data sources}", size=F(12.5), color="text", margin=0)
    B = lambda x, y, w, h, t, name, fill="grey200", line=None: rrect(
        s, X(x), Y(y), W(w), H(h), 0.08, fill=fill, line=line, lw=0.75, parts=t, size=F(12.5), color="text", align="l",
        anchor="t", margin=0.06, name=name)
    B(120, 282, 90, 77, "{Input stream}", "input_1")
    B(222, 282, 90, 103, ["{Data asset}", "· {attribute}", "· {attribute}"], "data_1")
    B(222, 391, 90, 40, "{Data asset}", "data_2")
    B(222, 450, 92, 85, "{Processing step}", "data_3", fill="white", line="grey300")
    B(120, 445, 90, 128, "{Input stream}", "input_2")
    B(352, 283, 120, 218, "{Engine}", "engine")
    B(362, 323, 103, 92, "{Model or method}", "engine_core", fill="white", line="grey300")
    text(s, X(362), Y(425), W(103), H(70), "{Guardrails}", size=F(12.5), color="text", margin=0)
    B(352, 530, 124, 44, "{Trigger}", "trigger")
    B(515, 282, 120, 218, "{Execution stack}", "execution")
    for k, y in enumerate((283, 333, 383, 445, 495, 545, 595), 1):
        B(676, y, 96, 40, "{Channel}", f"channel_{k}")
        elbow(s, [(X(657), Y(y + 20)), (X(674), Y(y + 20))], arrow="tail", aw="sm", al="sm", **G)
    elbow(s, [(X(657), Y(303)), (X(657), Y(615))], **G)
    for (y0, y1, lab) in ((290, 425, "{GROUP A}"), (440, 640, "{GROUP B}")):
        t = text(s, X(788) - H(y1 - y0) / 2, Y((y0 + y1) / 2) - 0.1, H(y1 - y0), 0.2, [[(lab, {"bold": False})]],
                 size=F(13), color="text", align="c", anchor="m", margin=0)
        t.rotation = 270
    elbow(s, [(X(88), Y(335)), (X(120), Y(335))], **G)
    elbow(s, [(X(50), Y(440)), (X(50), Y(588)), (X(500), Y(588)), (X(500), Y(450)), (X(515), Y(450))], **G)
    elbow(s, [(X(476), Y(552)), (X(500), Y(552))], **G)
    elbow(s, [(X(312), Y(335)), (X(352), Y(335))], **G)
    elbow(s, [(X(314), Y(410)), (X(352), Y(410))], **G)
    elbow(s, [(X(472), Y(433)), (X(515), Y(433))], **G)
    elbow(s, [(X(635), Y(433)), (X(657), Y(433))], **G)
    elbow(s, [(X(215), Y(580)), (X(215), Y(690)), (X(345), Y(690))], dash=True, **G)
    elbow(s, [(X(578), Y(650)), (X(578), Y(662)), (X(665), Y(662)), (X(665), Y(690)), (X(645), Y(690))], dash=True, **G)
    rrect(s, *f.R(345, 673, 300, 38), 0.08, fill="accent100", parts="{Measurement}", size=F(14), color="text",
          name="measurement")
    text(s, X(150), Y(730), W(500), H(26), [[("{Operating model and organisation}", {"bold": True})]], size=F(16),
         color="text", align="c", margin=0)
    for k, x in enumerate((48, 230, 440, 618), 1):
        soft_line(s, X(x - 8), Y(768), X(x - 8), Y(815), "grey400", lw=1)
        text(s, X(x), Y(766), W(170), H(55), "{Principle of the operating model}", size=F(14), color="text", margin=0,
             name=f"principle_{k}")


for fn in (d25, d26, d27, d28):
    fn()
prs.save(sys.argv[1])
print("saved")
