"""Shared helpers for native PowerPoint exhibit templates. All colours come from theme.json."""
import json, os
from lxml import etree
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.dml import MSO_LINE_DASH_STYLE
from pptx.oxml.ns import qn

HERE = os.path.dirname(os.path.abspath(__file__))
THEME = json.load(open(os.path.join(HERE, "theme.json")))
FONT = THEME["font"]
I = Inches


def C(role):
    return RGBColor.from_string(THEME["colors"][role].lstrip("#"))


def new_deck():
    p = Presentation()
    p.slide_width, p.slide_height = I(13.333), I(7.5)
    return p


def _style_runs(p, size, bold, color, italic=False):
    for r in p.runs:
        f = r.font
        f.name, f.size, f.bold, f.italic = FONT, Pt(size), bold, italic
        f.color.rgb = color


def text(slide, x, y, w, h, parts, size=11, color="text", align="l", anchor="t",
         name=None, margin=0.02, bold=False):
    """parts: str, or list of paragraphs; a paragraph is str or list of (text, {bold,color,size,italic})."""
    tb = slide.shapes.add_textbox(I(x), I(y), I(w), I(h))
    if name:
        tb.name = name
    _fill_tf(tb.text_frame, parts, size, color, align, anchor, margin, bold)
    return tb


def _fill_tf(tf, parts, size, color, align, anchor, margin, bold):
    tf.word_wrap = True
    for side in ("left", "right", "top", "bottom"):
        setattr(tf, f"margin_{side}", I(margin))
    tf.vertical_anchor = {"t": MSO_ANCHOR.TOP, "m": MSO_ANCHOR.MIDDLE, "b": MSO_ANCHOR.BOTTOM}[anchor]
    paras = [parts] if isinstance(parts, str) else parts
    for i, para in enumerate(paras):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = {"l": PP_ALIGN.LEFT, "c": PP_ALIGN.CENTER, "r": PP_ALIGN.RIGHT}[align]
        runs = [(para, {})] if isinstance(para, str) else para
        for t, st in runs:
            r = p.add_run()
            r.text = t
            f = r.font
            f.name = FONT
            f.size = Pt(st.get("size", size))
            f.bold = st.get("bold", bold)
            f.italic = st.get("italic", False)
            f.color.rgb = C(st.get("color", color))


def box(slide, x, y, w, h, fill=None, line=None, lw=1.0, shape=MSO_SHAPE.RECTANGLE, radius=None,
        name=None, parts=None, size=11, color="text", align="c", anchor="m", bold=False, margin=0.06,
        dash=False):
    if radius is not None and shape == MSO_SHAPE.RECTANGLE:
        shape = MSO_SHAPE.ROUNDED_RECTANGLE
    s = slide.shapes.add_shape(shape, I(x), I(y), I(w), I(h))
    if radius is not None and len(s.adjustments):
        s.adjustments[0] = radius
    if fill:
        s.fill.solid()
        s.fill.fore_color.rgb = C(fill)
    else:
        s.fill.background()
    if line:
        s.line.color.rgb = C(line)
        s.line.width = Pt(lw)
        if dash:
            s.line.dash_style = MSO_LINE_DASH_STYLE.DASH
    else:
        s.line.fill.background()
    _no_style(s)
    if name:
        s.name = name
    tf = s.text_frame
    if parts is not None:
        _fill_tf(tf, parts, size, color, align, anchor, margin, bold)
    return s


def _no_style(shp):
    """Drop the theme style reference so no renderer adds a default shadow or effect."""
    st = shp._element.find(qn("p:style"))
    if st is not None:
        shp._element.remove(st)


def arrowhead(shp, end="tail", kind="triangle"):
    ln = shp.line._get_or_add_ln()
    tag = qn("a:tailEnd" if end == "tail" else "a:headEnd")
    for e in ln.findall(tag):
        ln.remove(e)
    el = etree.SubElement(ln, tag)
    el.set("type", kind)
    el.set("w", "med")
    el.set("len", "med")


def line(slide, x1, y1, x2, y2, color="grey400", lw=1.0, dash=False, arrow=None, name=None):
    c = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, I(x1), I(y1), I(x2), I(y2))
    c.line.color.rgb = C(color)
    c.line.width = Pt(lw)
    if dash:
        c.line.dash_style = MSO_LINE_DASH_STYLE.DASH
    if arrow:
        arrowhead(c, arrow)
    _no_style(c)
    if name:
        c.name = name
    return c


def polyline(slide, pts, color="grey400", lw=1.0, dash=False, arrow=None, name=None, fill=None, close=False):
    fb = slide.shapes.build_freeform(I(pts[0][0]), I(pts[0][1]), scale=1.0)
    fb.add_line_segments([(I(x), I(y)) for x, y in pts[1:]], close=close)
    s = fb.convert_to_shape()
    if fill:
        s.fill.solid()
        s.fill.fore_color.rgb = C(fill)
    else:
        s.fill.background()
    if color:
        s.line.color.rgb = C(color)
        s.line.width = Pt(lw)
        if dash:
            s.line.dash_style = MSO_LINE_DASH_STYLE.DASH
        if arrow:
            arrowhead(s, arrow)
    else:
        s.line.fill.background()
    _no_style(s)
    if name:
        s.name = name
    return s


def dot(slide, cx, cy, d, fill, line_c=None, lw=1.0, name=None):
    return box(slide, cx - d / 2, cy - d / 2, d, d, fill=fill, line=line_c, lw=lw, shape=MSO_SHAPE.OVAL, name=name)


def icon(slide, cx, cy, d, color="accent700", fill=None, dash=False, name=None):
    """Icon placeholder: replace with a PowerPoint icon of the same name and size."""
    s = box(slide, cx - d / 2, cy - d / 2, d, d, fill=fill, line=color, lw=1.0, shape=MSO_SHAPE.OVAL,
            name=name, dash=dash)
    t = slide.shapes.add_textbox(I(cx - d / 2), I(cy - 0.09), I(d), I(0.18))
    _fill_tf(t.text_frame, "icon", 6, "white" if fill else color, "c", "m", 0, False)
    return s


def header(slide, title, source, note=None):
    text(slide, 0.5, 0.3, 12.3, 0.8, [[(title, {"bold": True})]], size=20, color="text", name="title",
         anchor="t")
    src = [[("Source: ", {"bold": True}), (source, {})]]
    if note:
        src.append([("Note: ", {"bold": True}), (note, {})])
    text(slide, 0.5, 6.85, 12.3, 0.45, src, size=8, color="grey600", name="source", anchor="b")


def slide(prs):
    return prs.slides.add_slide(prs.slide_layouts[6])
