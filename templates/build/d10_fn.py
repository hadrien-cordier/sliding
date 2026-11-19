from lib2 import *
PX = 112.0  # reference pixels per inch, measured: 1375 px wide image spans the 12.3 in body


def bezier(p0, p1, p2, p3, t):
    u = 1 - t
    return (u**3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t**3 * p3[0],
            u**3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t**3 * p3[1])



def d10():
    s = slide(prs)
    header(s, "{Capability} grows {multiple} every {period}", "{source}", "{definition of the measure}")
    vals = [0.05, 0.05, 0.05, 0.05, 0.1, 0.1, 0.2, 0.2, 0.2, 0.25, 0.4, 0.4, 0.7, 0.7, 1.0, 1.0, 2.0, 2.0, 2.0, 2.0,
            3.4, 3.4, 3.4, 4.9, 5.9, 5.9, 12, 12]
    months = ["Jan", "Mar", "May", "Jul", "Sep", "Nov"] * 2 + ["Jan", "Mar"]
    labels = {1: "<0.1", 4: "0.1", 6: "0.2", 10: "0.4", 12: "0.7", 14: "1.0", 17: "2.0", 21: "3.4", 23: "4.9", 24: "5.9", 26: "12"}
    x0, base, top = 0.85, 6.0, 2.9
    bw, gap = 41 / PX, 5 / PX            # measured bar width and gap
    hmax = base - top
    text(s, 0.5, 2.05, 1.2, 0.28, "{Unit}", size=11, color="grey600", name="unit_label")
    line(s, 0.75, 2.35, 0.75, base, "grey600", lw=1.25)
    line(s, 0.75, base, x0 + len(vals) * (bw + gap) + 0.05, base, "grey400", lw=1)
    for i, v in enumerate(vals):
        h = max(0.035, v / 12 * hmax)
        x = x0 + i * (bw + gap)
        b = box(s, x, base - h, bw, h, fill="accent500", shape=MSO_SHAPE.ROUND_2_SAME_RECTANGLE, name=f"bar_{i+1}")
        b.adjustments[0] = 0.12; b.adjustments[1] = 0
        if i in labels:
            text(s, x - 0.25, base - h - 0.32, bw + 0.5, 0.28, [[("{v}", {"bold": True})]], size=12, color="grey600",
                 align="c", name=f"bar_{i+1}_label")
        if i % 2 == 0:
            text(s, x - 0.3, base + 0.07, bw + 0.6, 0.28, months[i // 2], size=11, color="grey600", align="c",
                 name=f"month_{i+1}")
    xb = lambda i: x0 + i * (bw + gap) + bw / 2
    # swooshes: measured body 4 px at tail to 31 px before the head
    arrows = [((xb(1.6), 5.6), (xb(3), 4.95), (xb(7), 4.45), (xb(13) + 0.1, 4.3), 0.62, 0.55, "multiplier_1"),
              ((xb(13.5), 5.25), (xb(16), 4.25), (xb(20), 3.5), (xb(25.2) - 0.25, 3.25), 0.66, 0.58, "multiplier_2")]
    for p0, p1, p2, tip, hw, hl, nm in arrows:
        swoosh(s, p0, p1, p2, tip, 4 / PX, 34 / PX, hw, hl, "accent700", nm)
        lx, ly = bez(p0, p1, p2, tip, 20)[16]
        text(s, lx - 0.4, ly - 0.13, 0.8, 0.26, [[("~{n}x", {"bold": True})]], size=13, color="white", align="c",
             anchor="m", margin=0, name=f"{nm}_label")
    # period brackets: soft rule with round caps, end ticks, full-round pill
    for (a, b_, lab, k) in [(0, 11, "{Period 1}", 1), (12, 23, "{Period 2}", 2), (24, 27, "{Period 3}", 3)]:
        xa, xz = xb(a) - 0.15, xb(b_) + 0.15
        for seg in (line(s, xa, 6.62, xz, 6.62, "current_dark", lw=1.25), line(s, xa, 6.54, xa, 6.7, "current_dark", lw=1.25),
                    line(s, xz, 6.54, xz, 6.7, "current_dark", lw=1.25)):
            round_caps(seg)
        pw = 0.95
        p = box(s, (xa + xz) / 2 - pw / 2, 6.47, pw, 0.3, fill="warm500", shape=MSO_SHAPE.ROUNDED_RECTANGLE,
                parts=[[(lab, {"bold": True})]], size=11, color="white", margin=0, name=f"period_{k}")
        p.adjustments[0] = 0.5
