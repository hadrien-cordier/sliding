#!/usr/bin/env python3
"""Génère un .pptx de conseil (fond blanc, boxes grises) à partir d'un storyboard JSON.

Usage :
    python3 build_deck.py storyboard.json -o deck.pptx

Le format du storyboard est décrit dans references/schema-storyboard.md.
Le script écrit les avertissements de mise en page (texte trop long pour sa box) sur stderr.
"""
import argparse
import json
import math
import sys
from pathlib import Path

from lxml import etree
from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE, XL_LABEL_POSITION
from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, MSO_AUTO_SIZE, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Emu, Inches, Pt

sys.path.insert(0, str(Path(__file__).resolve().parent))
from layouts_spec import HARVEY, LAYOUTS  # noqa: E402

# ---------------------------------------------------------------- charte
SW, SH = 13.333, 7.5
ML, MR = 0.5, 0.5
CX, CY = ML, 1.55
CW, CH = SW - ML - MR, 5.25  # zone de contenu : 1.55 -> 6.80

NOIR = RGBColor(0x1A, 0x1A, 0x1A)
GRIS_TEXTE = RGBColor(0x59, 0x59, 0x59)
GRIS_BOX = RGBColor(0xF2, 0xF2, 0xF2)
GRIS_MOYEN = RGBColor(0xA6, 0xA6, 0xA6)
GRIS_FONCE = RGBColor(0x7F, 0x7F, 0x7F)
GRIS_LIGNE = RGBColor(0xBF, 0xBF, 0xBF)
BLANC = RGBColor(0xFF, 0xFF, 0xFF)
ACCENT = RGBColor(0x1F, 0x4E, 0x79)
POLICE = "Arial"

WARNINGS = []
_CTX = {"slide": 0}


def warn(msg):
    WARNINGS.append(f"slide {_CTX['slide']} : {msg}")


# ---------------------------------------------------------------- texte
def _para(item):
    """Normalise un paragraphe : str ou dict {texte, gras, puce, couleur, taille_rel}."""
    if isinstance(item, str):
        return {"texte": item}
    return item


def estimate_height(paras, width_in, size):
    """Hauteur (pouces) estimée pour Arial : largeur moyenne d'un caractère ≈ 0,5 × corps."""
    total = 0.0
    for p in paras:
        s = size * p.get("taille_rel", 1.0)
        w = width_in - (0.2 if p.get("puce") else 0)
        cpl = max(1, int(w * 72 / (s * (0.56 if p.get("gras") else 0.5))))
        longest = max((len(x) for x in str(p["texte"]).split()), default=0)
        if longest > cpl:  # un mot coupé en deux : taille trop grande
            return 99.0
        lines = 0
        for chunk in str(p["texte"]).split("\n"):
            lines += max(1, math.ceil(len(chunk) / cpl))
        total += lines * s * 1.18 / 72 + p.get("espace_avant", 3) / 72
    return total


def fit_size(paras, w, h, size, min_size):
    s = size
    while s > min_size and estimate_height(paras, w, s) > h:
        s -= 0.5
    if estimate_height(paras, w, s) > h:
        warn(f"texte trop long pour sa box ({str(paras[0]['texte'])[:50]}…) : raccourcir")
    return s


def _set_bullet(p, char="•"):
    pPr = p._p.get_or_add_pPr()
    pPr.set("marL", str(Inches(0.18)))
    pPr.set("indent", str(-Inches(0.18)))
    for tag in ("a:buNone", "a:buChar", "a:buAutoNum"):
        for el in pPr.findall(qn(tag)):
            pPr.remove(el)
    bu = etree.SubElement(pPr, qn("a:buChar"))
    bu.set("char", char)


def fill_text(tf, paras, w, h, size=12, min_size=9, color=NOIR, align=PP_ALIGN.LEFT,
              anchor=MSO_ANCHOR.TOP, margin=0.1, fit=True):
    paras = [_para(p) for p in paras if p is not None and _para(p).get("texte", "") != ""]
    if not paras:
        return
    tf.word_wrap = True
    tf.auto_size = MSO_AUTO_SIZE.NONE
    tf.vertical_anchor = anchor
    m = Inches(margin)
    tf.margin_left = tf.margin_right = m
    tf.margin_top = tf.margin_bottom = Inches(margin * 0.8)
    s = fit_size(paras, w - 2 * margin, h - 1.6 * margin, size, min_size) if fit else size
    for i, p in enumerate(paras):
        para = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        para.alignment = p.get("align", align)
        if i > 0:
            para.space_before = Pt(p.get("espace_avant", 3))
        run = para.add_run()
        run.text = str(p["texte"])
        f = run.font
        f.name = POLICE
        f.size = Pt(round(s * p.get("taille_rel", 1.0) * 2) / 2)
        f.bold = bool(p.get("gras", False))
        f.color.rgb = p.get("couleur", color)
        if p.get("puce"):
            _set_bullet(para)


def textbox(slide, x, y, w, h, paras, **kw):
    shape = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    fill_text(shape.text_frame, paras, w, h, **kw)
    return shape


def rect(slide, x, y, w, h, fill=GRIS_BOX, line=None, kind=MSO_SHAPE.RECTANGLE, line_w=1.0):
    s = slide.shapes.add_shape(kind, Inches(x), Inches(y), Inches(w), Inches(h))
    if fill is None:
        s.fill.background()
    else:
        s.fill.solid()
        s.fill.fore_color.rgb = fill
    if line is None:
        s.line.fill.background()
    else:
        s.line.color.rgb = line
        s.line.width = Pt(line_w)
    s.shadow.inherit = False
    sty = s._element.find(qn("p:style"))
    if sty is not None:  # le style de thème ajoute ombre et couleurs implicites
        s._element.remove(sty)
    return s


def bloc_paras(titre, points, title_color=NOIR, text_color=NOIR):
    paras = []
    if titre:
        paras.append({"texte": titre, "gras": True, "taille_rel": 1.08, "couleur": title_color})
    for pt in points or []:
        paras.append({"texte": pt, "puce": True, "couleur": text_color, "espace_avant": 5})
    return paras


def bloc(slide, x, y, w, h, titre, points, fill=GRIS_BOX, line=None, size=14,
         title_color=NOIR, text_color=NOIR, anchor=MSO_ANCHOR.TOP, fit=True):
    s = rect(slide, x, y, w, h, fill=fill, line=line)
    fill_text(s.text_frame, bloc_paras(titre, points, title_color, text_color), w, h,
              size=size, anchor=anchor, margin=0.15, fit=fit)
    return s


def common_size(items, size=14, min_size=9, margin=0.15):
    """Taille unique pour des blocs frères : (w, h, titre, points) -> plus petite taille qui tient partout.
    Des blocs voisins en corps différents cassent la lecture en couches."""
    best = size
    for w, h, titre, points in items:
        paras = [_para(p) for p in bloc_paras(titre, points)]
        if paras:
            best = min(best, fit_size(paras, w - 2 * margin, h - 1.6 * margin, size, min_size))
    return best


def line(slide, x1, y1, x2, y2, color=GRIS_LIGNE, width=1.0, arrow=False, elbow=False):
    kind = MSO_CONNECTOR.ELBOW if elbow else MSO_CONNECTOR.STRAIGHT
    c = slide.shapes.add_connector(kind, Inches(x1), Inches(y1), Inches(x2), Inches(y2))
    c.line.color.rgb = color
    c.line.width = Pt(width)
    if arrow:
        ln = c.line._get_or_add_ln()
        tail = etree.SubElement(ln, qn("a:tailEnd"))
        tail.set("type", "triangle")
    return c


# ---------------------------------------------------------------- squelette
def header(slide, s, num):
    textbox(slide, ML, 0.35, CW, 1.05, [{"texte": s["titre"], "gras": True}],
            size=22, min_size=15, anchor=MSO_ANCHOR.TOP, margin=0.02)
    if s.get("source"):
        textbox(slide, ML, 6.92, CW - 1.0, 0.4, [f"Source : {s['source']}"],
                size=9, min_size=7, color=GRIS_TEXTE, margin=0.02, anchor=MSO_ANCHOR.BOTTOM)
    textbox(slide, SW - MR - 0.8, 6.92, 0.8, 0.4, [str(num)], size=9, color=GRIS_TEXTE,
            align=PP_ALIGN.RIGHT, margin=0.02, anchor=MSO_ANCHOR.BOTTOM, fit=False)
    if s.get("notes"):
        slide.notes_slide.notes_text_frame.text = s["notes"]


def split_w(total, n, gap):
    w = (total - gap * (n - 1)) / n
    return [(i * (w + gap), w) for i in range(n)]


# ---------------------------------------------------------------- gabarits
def l_couverture(slide, s):
    rect(slide, 0, 0, 0.18, SH, fill=ACCENT)
    textbox(slide, 1.0, 2.3, SW - 2.0, 1.9, [{"texte": s["titre"], "gras": True}],
            size=34, min_size=24, anchor=MSO_ANCHOR.BOTTOM, margin=0.02)
    if s.get("contexte"):
        textbox(slide, 1.0, 4.35, SW - 2.0, 0.8, [s["contexte"]], size=16, color=GRIS_TEXTE,
                margin=0.02)


def l_colonnes(slide, s):
    blocs = s["blocs"]
    h = CH - (0.95 if s.get("synthese") else 0)
    geo = split_w(CW, len(blocs), 0.2)
    sz = common_size([(w, h, b.get("titre"), b.get("points")) for (dx, w), b in zip(geo, blocs)])
    for (dx, w), b in zip(geo, blocs):
        acc = b.get("accent")
        bloc(slide, CX + dx, CY, w, h, b.get("titre"), b.get("points"), size=sz, fit=False,
             line=ACCENT if acc else None, title_color=ACCENT if acc else NOIR)
    if s.get("synthese"):
        sh = rect(slide, CX, CY + h + 0.2, CW, 0.75, fill=BLANC, line=ACCENT, line_w=1.25)
        fill_text(sh.text_frame, [{"texte": s["synthese"], "gras": True, "couleur": ACCENT}],
                  CW, 0.75, size=13, anchor=MSO_ANCHOR.MIDDLE, margin=0.15)


def l_lignes(slide, s):
    blocs = s["blocs"]
    n = len(blocs)
    gap = 0.15
    rh = (CH - gap * (n - 1)) / n
    lw = s.get("largeur_titres", 3.6)
    for i, b in enumerate(blocs):
        y = CY + i * (rh + gap)
        t = rect(slide, CX, y, lw, rh, fill=GRIS_BOX)
        fill_text(t.text_frame, [{"texte": b["titre"], "gras": True}], lw, rh, size=15,
                  anchor=MSO_ANCHOR.MIDDLE, margin=0.15)
        textbox(slide, CX + lw + 0.2, y, CW - lw - 0.2, rh,
                [{"texte": p, "puce": True, "espace_avant": 4} for p in b.get("points", [])],
                size=14, anchor=MSO_ANCHOR.MIDDLE)
        if i < n - 1:
            line(slide, CX + lw + 0.2, y + rh + gap / 2, CX + CW, y + rh + gap / 2)


def l_puces(slide, s):
    paras = []
    if s.get("titre_bloc"):
        paras.append({"texte": s["titre_bloc"], "gras": True, "taille_rel": 1.08})
    paras += [{"texte": p, "puce": True, "espace_avant": 8} for p in s["points"]]
    r = rect(slide, CX, CY, CW, CH)
    fill_text(r.text_frame, paras, CW, CH, size=16, margin=0.3)


def l_progression(slide, s):
    blocs = s["blocs"]
    n = len(blocs)
    ah = 0.5
    rect_arrow = rect(slide, CX, CY, CW, ah, fill=ACCENT, kind=MSO_SHAPE.RIGHT_ARROW)
    if s.get("axe"):
        fill_text(rect_arrow.text_frame, [{"texte": s["axe"], "gras": True, "couleur": BLANC}],
                  CW, ah, size=12, anchor=MSO_ANCHOR.MIDDLE, margin=0.2, fit=False)
    top = CY + ah + 0.2
    full = CY + CH - top
    geo = split_w(CW, n, 0.2)
    hs = [full * (0.6 + 0.4 * (i / (n - 1) if n > 1 else 1)) for i in range(n)]
    sz = common_size([(w, h, b.get("titre"), b.get("points")) for (dx, w), h, b in zip(geo, hs, blocs)])
    for i, ((dx, w), h, b) in enumerate(zip(geo, hs, blocs)):
        last = i == n - 1 and s.get("accent_derniere", True)
        bloc(slide, CX + dx, top + full - h, w, h, b.get("titre"), b.get("points"), size=sz,
             fit=False, line=ACCENT if last else None, title_color=ACCENT if last else NOIR)


def l_chevrons(slide, s):
    etapes = s["etapes"]
    n = len(etapes)
    ch_h = 0.75
    geo = split_w(CW, n, 0.06)
    lab = min(fit_size([{"texte": e["titre"], "gras": True}], max(0.6, w - 0.9) - 0.1, ch_h, 14, 9)
              for (dx, w), e in zip(geo, etapes))
    sz = common_size([(w, CH - ch_h - 0.2, None, e.get("points")) for (dx, w), e in zip(geo, etapes)])
    for i, (dx, w) in enumerate(geo):
        e = etapes[i]
        kind = MSO_SHAPE.PENTAGON if i == 0 else MSO_SHAPE.CHEVRON
        c = rect(slide, CX + dx, CY, w + (0.12 if i < n - 1 else 0), ch_h, fill=ACCENT, kind=kind)
        # la géométrie du chevron réserve ses pointes : la zone de texte réelle est plus étroite
        fill_text(c.text_frame, [{"texte": e["titre"], "gras": True, "couleur": BLANC,
                                  "align": PP_ALIGN.CENTER}], max(0.6, w - 0.9), ch_h, size=lab,
                  anchor=MSO_ANCHOR.MIDDLE, margin=0.05, fit=False)
        bloc(slide, CX + dx, CY + ch_h + 0.2, w, CH - ch_h - 0.2, None, e.get("points"), size=sz,
             fit=False)


def l_matrice(slide, s):
    ax, ay, q = s["axe_x"], s["axe_y"], s["quadrants"]
    side = s.get("commentaire")
    gw = CW * (0.62 if side else 1.0)
    lx = CX + 1.0                 # début de la grille
    gx_w = gw - 1.0
    gy, gh = CY, CH - 0.75
    # axe Y : libellé vertical + extrêmes
    # boîte horizontale de largeur gh, tournée de 270° autour de son centre (CX + 0.2, milieu de grille)
    lab = textbox(slide, CX + 0.2 - gh / 2, gy + gh / 2 - 0.2, gh, 0.4,
                  [{"texte": ay["label"], "gras": True, "align": PP_ALIGN.CENTER}],
                  size=11, color=GRIS_TEXTE, fit=False, margin=0.02)
    lab.rotation = 270
    textbox(slide, CX + 0.35, gy, 0.6, 0.4, [ay.get("haut", "Fort")], size=9, color=GRIS_TEXTE,
            fit=False, margin=0.02)
    textbox(slide, CX + 0.35, gy + gh - 0.4, 0.6, 0.4, [ay.get("bas", "Faible")], size=9,
            color=GRIS_TEXTE, fit=False, margin=0.02, anchor=MSO_ANCHOR.BOTTOM)
    line(slide, lx - 0.08, gy + gh, lx - 0.08, gy, color=GRIS_FONCE, width=1.25, arrow=True)
    line(slide, lx - 0.08, gy + gh + 0.08, lx + gx_w, gy + gh + 0.08, color=GRIS_FONCE, width=1.25,
         arrow=True)
    textbox(slide, lx, gy + gh + 0.15, gx_w, 0.35, [{"texte": ax["label"], "gras": True,
            "align": PP_ALIGN.CENTER}], size=11, color=GRIS_TEXTE, fit=False, margin=0.02)
    textbox(slide, lx, gy + gh + 0.15, 1.5, 0.35, [ax.get("bas", "Faible")], size=9,
            color=GRIS_TEXTE, fit=False, margin=0.02)
    textbox(slide, lx + gx_w - 1.5, gy + gh + 0.15, 1.5, 0.35, [{"texte": ax.get("haut", "Fort"),
            "align": PP_ALIGN.RIGHT}], size=9, color=GRIS_TEXTE, fit=False, margin=0.02)
    qw, qh = (gx_w - 0.1) / 2, (gh - 0.1) / 2
    pos = [(0, 0), (1, 0), (0, 1), (1, 1)]  # haut-gauche, haut-droite, bas-gauche, bas-droite
    sz = common_size([(qw, qh, quad.get("titre"), quad.get("points")) for quad in q], size=13)
    for (cx, cy), quad in zip(pos, q):
        acc = quad.get("accent")
        bloc(slide, lx + cx * (qw + 0.1), gy + cy * (qh + 0.1), qw, qh, quad.get("titre"),
             quad.get("points"), fill=GRIS_BOX, line=ACCENT if acc else None,
             title_color=ACCENT if acc else NOIR, size=sz, fit=False)
    if side:
        _side_blocs(slide, side, CX + gw + 0.3, CW - gw - 0.3)


def _side_blocs(slide, blocs, x, w):
    n = len(blocs)
    gap = 0.15
    h = (CH - gap * (n - 1)) / n
    sz = common_size([(w, h, b.get("titre"), b.get("points")) for b in blocs])
    for i, b in enumerate(blocs):
        bloc(slide, x, CY + i * (h + gap), w, h, b.get("titre"), b.get("points"), size=sz, fit=False)


def _cell_border_bottom(cell, color="BFBFBF", w=9525):
    tcPr = cell._tc.get_or_add_tcPr()
    for tag in ("a:lnL", "a:lnR", "a:lnT", "a:lnB"):
        ln = etree.SubElement(tcPr, qn(tag))
        if tag == "a:lnB":
            ln.set("w", str(w))
            sf = etree.SubElement(ln, qn("a:solidFill"))
            c = etree.SubElement(sf, qn("a:srgbClr"))
            c.set("val", color)
        else:
            ln.set("w", "0")
            etree.SubElement(ln, qn("a:noFill"))


def harvey_ball(slide, cx, cy, quarters, color, d=0.28):
    """Harvey ball dessinée en formes (0 à 4 quarts) : rendu identique quelle que soit la police."""
    x, y = cx - d / 2, cy - d / 2
    if quarters >= 4:
        rect(slide, x, y, d, d, fill=color, kind=MSO_SHAPE.OVAL)
        return
    rect(slide, x, y, d, d, fill=BLANC, line=color, kind=MSO_SHAPE.OVAL, line_w=1.25)
    if quarters > 0:
        pie = rect(slide, x, y, d, d, fill=color, kind=MSO_SHAPE.PIE)
        # angles en degrés × 0,6 (unités python-pptx) ; départ à midi, sens horaire
        pie.adjustments[0] = 270 * 0.6
        pie.adjustments[1] = ((270 + 90 * quarters) % 360) * 0.6


def l_tableau(slide, s):
    cols, rows = s["colonnes"], s["lignes"]
    acc = s.get("colonne_accent")
    nr, nc = len(rows) + 1, len(cols)
    rh = min(0.7, CH / nr)
    gf = slide.shapes.add_table(nr, nc, Inches(CX), Inches(CY), Inches(CW), Inches(rh * nr))
    tbl = gf.table
    tblPr = tbl._tbl.tblPr
    for el in tblPr.findall(qn("a:tableStyleId")):
        tblPr.remove(el)
    sid = etree.SubElement(tblPr, qn("a:tableStyleId"))
    sid.text = "{2D5ABB26-0587-4C30-8999-92F81FD0307C}"  # No Style, No Grid
    tblPr.set("firstRow", "0")
    tblPr.set("bandRow", "0")
    first_w = s.get("largeur_premiere_colonne", CW * 0.26)
    other = (CW - first_w) / (nc - 1) if nc > 1 else CW
    tbl.columns[0].width = Inches(first_w)
    for j in range(1, nc):
        tbl.columns[j].width = Inches(other)
    size = 13 if nr <= 7 else 11
    balls = []
    for i in range(nr):
        tbl.rows[i].height = Inches(rh)
        for j in range(nc):
            cell = tbl.cell(i, j)
            raw = cols[j] if i == 0 else (rows[i - 1][j] if j < len(rows[i - 1]) else "")
            raw = str(raw)
            harvey = raw.strip() in HARVEY
            txt = "" if harvey else raw
            if harvey:
                cx = CX + (first_w + (j - 1) * other if j else 0) + (other if j else first_w) / 2
                balls.append((cx, CY + i * rh + rh / 2, int(raw.strip()[1]), j == acc))
            cell.fill.solid()
            cell.fill.fore_color.rgb = GRIS_BOX if i == 0 else BLANC
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            cell.margin_left = cell.margin_right = Inches(0.1)
            tf = cell.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            p.alignment = PP_ALIGN.CENTER if (harvey or (j > 0 and i == 0)) else PP_ALIGN.LEFT
            r = p.add_run()
            r.text = txt
            r.font.name = POLICE
            r.font.size = Pt(size)
            r.font.bold = i == 0 or j == 0
            r.font.color.rgb = ACCENT if (acc is not None and j == acc and (i == 0 or harvey)) else NOIR
            _cell_border_bottom(cell, "1A1A1A" if i == 0 else "BFBFBF")
    for cx, cy, v, is_acc in balls:
        harvey_ball(slide, cx, cy, v, ACCENT if is_acc else NOIR)
    if acc is not None:
        x = CX + first_w + (acc - 1) * other
        rect(slide, x, CY, other, rh * nr, fill=None, line=ACCENT, line_w=1.5)
    if s.get("legende"):
        textbox(slide, CX, CY + rh * nr + 0.1, CW, 0.35, [s["legende"]], size=9,
                color=GRIS_TEXTE, fit=False, margin=0.02)


def _fmt(g):
    f = g.get("format", "0")
    u = g.get("unite")
    return f + (f'"{u}"' if u else "")


def _chart(slide, g, x, y, w, h):
    kind = {"barres": XL_CHART_TYPE.COLUMN_CLUSTERED, "barres_h": XL_CHART_TYPE.BAR_CLUSTERED,
            "courbe": XL_CHART_TYPE.LINE_MARKERS}[g.get("type", "barres")]
    cd = CategoryChartData()
    cats = g["categories"]
    if kind == XL_CHART_TYPE.BAR_CLUSTERED:  # barres horizontales : première catégorie en haut
        cats = list(reversed(cats))
    cd.categories = cats
    for se in g["series"]:
        vals = se["valeurs"]
        cd.add_series(se.get("nom", ""), list(reversed(vals)) if kind == XL_CHART_TYPE.BAR_CLUSTERED else vals)
    gf = slide.shapes.add_chart(kind, Inches(x), Inches(y), Inches(w), Inches(h), cd)
    ch = gf.chart
    ch.has_title = False
    ch.font.name = POLICE
    ch.font.size = Pt(12)
    ch.font.color.rgb = NOIR
    multi = len(g["series"]) > 1
    ch.has_legend = multi
    if multi:
        from pptx.enum.chart import XL_LEGEND_POSITION
        ch.legend.position = XL_LEGEND_POSITION.TOP
        ch.legend.include_in_layout = False
    plot = ch.plots[0]
    va = ch.value_axis
    va.has_major_gridlines = False
    va.visible = False
    if kind != XL_CHART_TYPE.LINE_MARKERS:
        plot.gap_width = 60
        va.minimum_scale = 0  # barres à zéro
    ca = ch.category_axis
    ca.format.line.color.rgb = GRIS_LIGNE
    ca.tick_labels.font.size = Pt(11)
    from pptx.enum.chart import XL_TICK_MARK
    ca.major_tick_mark = XL_TICK_MARK.NONE
    plot.has_data_labels = True
    dl = plot.data_labels
    dl.number_format = _fmt(g)
    dl.number_format_is_linked = False
    dl.font.size = Pt(11)
    if kind != XL_CHART_TYPE.LINE_MARKERS:
        dl.position = XL_LABEL_POSITION.OUTSIDE_END
    else:
        dl.position = XL_LABEL_POSITION.ABOVE
    palette = [ACCENT, GRIS_FONCE, GRIS_LIGNE, RGBColor(0x40, 0x40, 0x40)]
    accents = set(g.get("accent", []))
    n = len(g["categories"])
    for k, series in enumerate(plot.series):
        if kind == XL_CHART_TYPE.LINE_MARKERS:
            series.format.line.color.rgb = palette[k % 4]
            series.format.line.width = Pt(2.25)
            series.smooth = False
            continue
        series.format.fill.solid()
        series.format.fill.fore_color.rgb = palette[k % 4]
        if not multi:
            for i in range(n):
                idx = (n - 1 - i) if kind == XL_CHART_TYPE.BAR_CLUSTERED else i
                pt = series.points[idx]
                pt.format.fill.solid()
                pt.format.fill.fore_color.rgb = ACCENT if (i in accents or not accents) else GRIS_MOYEN
    return ch


def _chart_title(slide, txt, x, y, w):
    textbox(slide, x, y, w, 0.6, [{"texte": txt, "gras": True}], size=13, min_size=11,
            anchor=MSO_ANCHOR.TOP, margin=0.02)


def l_graphique_texte(slide, s):
    g = s["graphique"]
    gw = CW * s.get("part_graphique", 0.6)
    top = CY
    if g.get("titre"):
        _chart_title(slide, g["titre"], CX, CY, gw)
        top = CY + 0.65
    _chart(slide, g, CX, top, gw, CY + CH - top)
    _side_blocs(slide, s["blocs"], CX + gw + 0.3, CW - gw - 0.3)


def l_waterfall(slide, s):
    et = s["etapes"]
    blocs = s.get("blocs")
    gw = CW * (0.62 if blocs else 1.0)
    top = CY
    if s.get("titre_graphique"):
        _chart_title(slide, s["titre_graphique"], CX, CY, gw)
        top = CY + 0.65
    base, val, kinds, run = [], [], [], 0.0
    for e in et:
        v = float(e["valeur"])
        if e.get("total"):
            base.append(0)
            val.append(v)
            run = v
            kinds.append("total")
        elif v >= 0:
            base.append(run)
            val.append(v)
            run += v
            kinds.append("plus")
        else:
            base.append(run + v)
            val.append(-v)
            run += v
            kinds.append("moins")
    cd = CategoryChartData()
    cd.categories = [e["label"] for e in et]
    cd.add_series("base", base)
    cd.add_series("valeur", val)
    gf = slide.shapes.add_chart(XL_CHART_TYPE.COLUMN_STACKED, Inches(CX), Inches(top), Inches(gw),
                                Inches(CY + CH - top), cd)
    ch = gf.chart
    ch.has_title = False
    ch.font.name = POLICE
    ch.font.size = Pt(12)
    ch.has_legend = False
    plot = ch.plots[0]
    plot.gap_width = 50
    plot.overlap = 100
    ch.value_axis.visible = False
    ch.value_axis.has_major_gridlines = False
    ch.value_axis.minimum_scale = 0
    ch.category_axis.format.line.color.rgb = GRIS_LIGNE
    from pptx.enum.chart import XL_TICK_MARK
    ch.category_axis.major_tick_mark = XL_TICK_MARK.NONE
    sb, sv = plot.series
    sb.format.fill.background()
    sb.format.line.fill.background()
    fmt = s.get("format", "0")
    unit = s.get("unite", "")
    for i, k in enumerate(kinds):
        pt = sv.points[i]
        pt.format.fill.solid()
        pt.format.fill.fore_color.rgb = {"total": ACCENT, "plus": GRIS_FONCE, "moins": GRIS_LIGNE}[k]
        v = val[i] if k != "moins" else -val[i]
        txt = _num(v, fmt, signed=(k != "total")) + unit
        dlab = pt.data_label
        dlab.has_text_frame = True
        dlab.text_frame.text = txt
        dlab.position = XL_LABEL_POSITION.INSIDE_END
        r = dlab.text_frame.paragraphs[0].runs[0]
        r.font.size = Pt(11)
        r.font.bold = k == "total"
        r.font.color.rgb = BLANC if k in ("total", "plus") else NOIR
    if blocs:
        _side_blocs(slide, blocs, CX + gw + 0.3, CW - gw - 0.3)


def _num(v, fmt, signed=False):
    dec = len(fmt.split(".")[1]) if "." in fmt else 0
    t = f"{abs(v):,.{dec}f}".replace(",", " ").replace(".", ",")
    sign = ("+" if v >= 0 else "−") if signed else ("−" if v < 0 else "")
    return sign + t


def l_avant_apres(slide, s):
    aw = 1.0
    w = (CW - aw - 0.4) / 2
    a, b = s["avant"], s["apres"]
    sz = common_size([(w, CH, a.get("titre"), a.get("points")), (w, CH, b.get("titre"), b.get("points"))])
    bloc(slide, CX, CY, w, CH, a.get("titre"), a.get("points"), size=sz, fit=False)
    bloc(slide, CX + w + aw + 0.4, CY, w, CH, b.get("titre"), b.get("points"), line=ACCENT,
         title_color=ACCENT, size=sz, fit=False)
    ar = rect(slide, CX + w + 0.2, CY + CH / 2 - 0.45, aw, 0.9, fill=ACCENT,
              kind=MSO_SHAPE.RIGHT_ARROW)
    if s.get("transition"):
        textbox(slide, CX + w + 0.05, CY + CH / 2 + 0.55, aw + 0.3, 1.2,
                [{"texte": s["transition"], "align": PP_ALIGN.CENTER}], size=10,
                color=GRIS_TEXTE, margin=0.02)


def l_timeline(slide, s):
    ph = s["phases"]
    n = len(ph)
    ly = CY + 0.75
    line(slide, CX, ly, CX + CW, ly, color=ACCENT, width=2.5, arrow=True)
    geo = split_w(CW, n, 0.2)
    bh = CY + CH - ly - 0.3
    sz = common_size([(w, bh, p.get("titre"), p.get("points")) for (dx, w), p in zip(geo, ph)])
    for i, (dx, w) in enumerate(geo):
        p = ph[i]
        cx = CX + dx + w / 2
        textbox(slide, CX + dx, CY, w, 0.55, [{"texte": p["periode"], "gras": True,
                "align": PP_ALIGN.CENTER, "couleur": ACCENT}], size=12, margin=0.02,
                anchor=MSO_ANCHOR.BOTTOM)
        rect(slide, cx - 0.11, ly - 0.11, 0.22, 0.22, fill=ACCENT, kind=MSO_SHAPE.OVAL)
        bloc(slide, CX + dx, ly + 0.3, w, bh, p.get("titre"), p.get("points"), size=sz, fit=False)


def l_arbre(slide, s):
    br = s["branches"]
    n = len(br)
    rw, bw = 2.6, 3.2
    gap = 0.2
    bh = (CH - gap * (n - 1)) / n
    root = rect(slide, CX, CY + CH / 2 - 0.9, rw, 1.8, fill=ACCENT)
    fill_text(root.text_frame, [{"texte": s["racine"], "gras": True, "couleur": BLANC}], rw, 1.8,
              size=15, anchor=MSO_ANCHOR.MIDDLE, margin=0.15)
    bx = CX + rw + 0.6
    fx = bx + bw + 0.5
    fw = CX + CW - fx
    xm = CX + rw + 0.3  # colonne verticale qui distribue les branches
    line(slide, CX + rw, CY + CH / 2, xm, CY + CH / 2, color=GRIS_FONCE, width=1.25)
    line(slide, xm, CY + bh / 2, xm, CY + (n - 1) * (bh + gap) + bh / 2, color=GRIS_FONCE, width=1.25)
    for i, b in enumerate(br):
        y = CY + i * (bh + gap)
        line(slide, xm, y + bh / 2, bx, y + bh / 2, color=GRIS_FONCE, width=1.25)
        r = rect(slide, bx, y, bw, bh, fill=GRIS_BOX)
        fill_text(r.text_frame, [{"texte": b["texte"], "gras": True}], bw, bh, size=14,
                  anchor=MSO_ANCHOR.MIDDLE, margin=0.15)
        if b.get("feuilles"):
            line(slide, bx + bw, y + bh / 2, fx, y + bh / 2, color=GRIS_FONCE, width=1.25)
            textbox(slide, fx, y, fw, bh, [{"texte": f, "puce": True, "espace_avant": 3}
                                           for f in b["feuilles"]], size=13,
                    anchor=MSO_ANCHOR.MIDDLE)


def l_recommandation(slide, s):
    rh = 1.25
    r = rect(slide, CX, CY, CW, rh, fill=ACCENT)
    fill_text(r.text_frame, [{"texte": s["recommandation"], "gras": True, "couleur": BLANC}], CW, rh,
              size=16, anchor=MSO_ANCHOR.MIDDLE, margin=0.25)
    pil = s["piliers"]
    top = CY + rh + 0.3
    geo = split_w(CW, len(pil), 0.2)
    ph = CY + CH - top
    sz = common_size([(w, ph, p.get("titre"), p.get("points")) for (dx, w), p in zip(geo, pil)])
    for i, (dx, w) in enumerate(geo):
        line(slide, CX + dx + w / 2, CY + rh, CX + dx + w / 2, top, color=ACCENT, width=1.5)
        bloc(slide, CX + dx, top, w, ph, pil[i].get("titre"), pil[i].get("points"), size=sz, fit=False)


BUILDERS = {k: globals()[f"l_{k}"] for k in LAYOUTS}


# ---------------------------------------------------------------- main
def build(story, out):
    global ACCENT, POLICE
    meta = story.get("meta", {})
    if meta.get("accent"):
        ACCENT = RGBColor.from_string(meta["accent"].lstrip("#"))
    POLICE = meta.get("police", POLICE)
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(SW), Inches(SH)
    blank = prs.slide_layouts[6]
    for i, s in enumerate(story["slides"], start=1):
        _CTX["slide"] = i
        lay = s.get("layout")
        if lay not in BUILDERS:
            raise SystemExit(f"slide {i} : gabarit inconnu « {lay} » (voir layouts_spec.py)")
        missing = [f for f in LAYOUTS[lay][0] if f not in s]
        if missing:
            raise SystemExit(f"slide {i} ({lay}) : champs manquants {missing}")
        slide = prs.slides.add_slide(blank)
        if lay == "couverture":
            l_couverture(slide, s)
            if s.get("notes"):
                slide.notes_slide.notes_text_frame.text = s["notes"]
        else:
            header(slide, s, i)
            BUILDERS[lay](slide, s)
    prs.save(out)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("storyboard")
    ap.add_argument("-o", "--out", default="deck.pptx")
    a = ap.parse_args()
    story = json.loads(Path(a.storyboard).read_text(encoding="utf-8"))
    build(story, a.out)
    for w in WARNINGS:
        print("AVERTISSEMENT", w, file=sys.stderr)
    print(f"OK {a.out} ({len(story['slides'])} slides, {len(WARNINGS)} avertissement(s))")


if __name__ == "__main__":
    main()
