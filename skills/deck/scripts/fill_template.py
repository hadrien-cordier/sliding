"""Copy an exhibit template slide into a deck and fill its named shapes.

A storyboard slide using a template looks like:
  {"layout": "template", "template": "two_lanes_before_after", "title": "...", "source": "...",
   "slots": {"current_step_1": ["Collect", "data"], "kpi_1": [{"text": "40-60%", "bold": true}, "time to decision"]},
   "drop": ["kpi_3"]}

Slot values: a string (one paragraph), a list of paragraphs, and each paragraph a string or a dict
{text, bold, italic, color} or a list of such runs. Each paragraph keeps the size and colour of the
template paragraph at the same position (the last one when there are more), so the design survives.
`drop` removes shapes the content does not need (an unused fourth KPI, a fifth stage).
The template's own "title" and "source" shapes receive the slide title and source.
"""
import copy
import re
from pathlib import Path

import yaml
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.oxml.ns import qn

TPL_DIR = Path(__file__).resolve().parent.parent / "templates"
PLACEHOLDER = re.compile(r"\{[^{}]*\}")
_CACHE = {}


def catalog():
    if "catalog" not in _CACHE:
        cat = yaml.safe_load((TPL_DIR / "catalog.yaml").read_text(encoding="utf-8"))
        _CACHE["catalog"] = {t["id"]: t for t in cat["templates"]}
    return _CACHE["catalog"]


def template_slide(tid):
    t = catalog().get(tid)
    if not t:
        raise KeyError(f"unknown template '{tid}' (see templates/catalog.yaml)")
    f = TPL_DIR / f"{t['file']}.pptx"
    if f not in _CACHE:
        _CACHE[f] = Presentation(str(f))
    return _CACHE[f].slides[t["slide"] - 1]


def _group_count(names, pattern):
    k = 0
    while pattern.format(k=k + 1) in names:
        k += 1
    return k


def slot_names(tid, repeat=None):
    """Names a storyboard may fill: the template's shapes plus those of instances added by `repeat`."""
    names = {sh.name for sh in template_slide(tid).shapes}
    for g in catalog()[tid].get("repeat", []):
        n = (repeat or {}).get(g["group"], 0)
        for k in range(1, n + 1):
            names |= {p.format(k=k) for p in g["shapes"]}
    return names


def apply_repeat(slide, groups, counts, warn=print):
    """Resize repeatable groups to the requested count inside the template's area.
    Fewer: extra instances are removed and the others keep their place. More: instances are re-spaced
    and shrunk along the group's axis; added instances copy the last template instance (its colour role)."""
    tree = slide.shapes._spTree
    for g in groups:
        n = counts.get(g["group"])
        if n is None:
            continue
        if n > g.get("max", 99):
            warn(f"repeat: {g['group']} capped at {g['max']}")
            n = g["max"]
        byname = {sh.name: sh for sh in slide.shapes}
        N = _group_count(byname, g["shapes"][0])
        if N == 0:
            warn(f"repeat: group {g['group']} not found")
            continue
        inst = lambda k: [byname[p.format(k=k)] for p in g["shapes"] if p.format(k=k) in byname]
        vert = g.get("axis", "vertical") == "vertical"
        pos = (lambda sh: sh.top) if vert else (lambda sh: sh.left)
        size = (lambda sh: sh.height) if vert else (lambda sh: sh.width)
        first, last = inst(1), inst(N)
        start = min(pos(sh) for sh in first)
        end = max(pos(sh) + size(sh) for sh in last)
        pitch = (min(pos(sh) for sh in inst(2)) - start) if N > 1 else (end - start)
        if n <= N:
            for k in range(n + 1, N + 1):
                for sh in inst(k):
                    tree.remove(sh._element)
            continue
        f = (end - start) / ((n - 1) * pitch + (end - start - (N - 1) * pitch))
        geo = [(pos(sh) - start, size(sh)) for sh in first]
        for k in range(1, n + 1):
            if k <= N:
                shapes = inst(k)
            else:
                shapes = []
                for p, src in zip(g["shapes"], inst(N)):
                    el = copy.deepcopy(src._element)
                    tree.append(el)
                    sh = slide.shapes[-1]
                    sh.name = p.format(k=k)
                    if sh.has_text_frame and sh.text_frame.text.strip() == str(N):
                        sh.text_frame.paragraphs[0].runs[0].text = str(k)
                    shapes.append(sh)
            for sh, (off, sz) in zip(shapes, geo):
                new_pos = int(start + (k - 1) * pitch * f + off * f)
                square = abs(sh.width - sh.height) < 0.05 * max(sh.width, sh.height, 1)
                if square:   # discs and icons keep their shape: shrink both sides around the centre
                    cross = (sh.left + sh.width / 2) if vert else (sh.top + sh.height / 2)
                    d = max(1, int(sz * f))
                    sh.width = sh.height = d
                    if vert:
                        sh.top, sh.left = new_pos, int(cross - d / 2)
                    else:
                        sh.left, sh.top = new_pos, int(cross - d / 2)
                elif vert:
                    sh.top, sh.height = new_pos, max(1, int(sz * f))
                else:
                    sh.left, sh.width = new_pos, max(1, int(sz * f))
        if f < 0.6:
            warn(f"repeat: {g['group']} x{n} shrinks items to {int(f * 100)}% of their size; consider splitting the slide")


def _copy_shapes(src_slide, dst_slide):
    """Deep-copy every shape; charts get their chart part re-linked in the destination slide."""
    tree = dst_slide.shapes._spTree
    for sh in src_slide.shapes:
        el = copy.deepcopy(sh._element)
        if sh.has_chart if hasattr(sh, "has_chart") else False:
            rid_old = sh._element.xpath(".//c:chart/@r:id")[0]
            part = src_slide.part.related_part(rid_old)
            rid_new = dst_slide.part.relate_to(part, "http://schemas.openxmlformats.org/officeDocument/2006/relationships/chart")
            el.xpath(".//c:chart")[0].set(qn("r:id"), rid_new)
        tree.append(el)


def _runs(par):
    if isinstance(par, str):
        return [{"text": par}]
    if isinstance(par, dict):
        return [par]
    return [r if isinstance(r, dict) else {"text": r} for r in par]


def set_text(shape, value):
    """Replace the text of a shape, keeping each template paragraph's run formatting."""
    tf = shape.text_frame
    paras = value if isinstance(value, list) else [value]
    tpl = [p for p in tf.paragraphs]
    protos = []
    for p in tpl:
        r = p.runs[0]._r if p.runs else None
        protos.append((copy.deepcopy(p._p.pPr) if p._p.pPr is not None else None,
                       copy.deepcopy(r.rPr) if r is not None and r.rPr is not None else None))
    txBody = tf._txBody
    for p in list(txBody.findall(qn("a:p"))):
        txBody.remove(p)
    for i, par in enumerate(paras):
        pPr, rPr = protos[min(i, len(protos) - 1)] if protos else (None, None)
        p_el = txBody.makeelement(qn("a:p"), {})
        txBody.append(p_el)
        if pPr is not None:
            p_el.append(copy.deepcopy(pPr))
        runs = _runs(par)
        for run in runs:
            if len(runs) > 1 and "bold" not in run:
                run = dict(run, bold=False)
            r_el = p_el.makeelement(qn("a:r"), {})
            p_el.append(r_el)
            if rPr is not None:
                r_el.append(copy.deepcopy(rPr))
            t = r_el.makeelement(qn("a:t"), {})
            t.text = run.get("text", "")
            r_el.append(t)
            rp = r_el.find(qn("a:rPr"))
            if rp is None:
                rp = r_el.makeelement(qn("a:rPr"), {}); r_el.insert(0, rp)
            if "bold" in run:
                rp.set("b", "1" if run["bold"] else "0")
            if "italic" in run:
                rp.set("i", "1" if run["italic"] else "0")
            if run.get("color"):
                for sf in rp.findall(qn("a:solidFill")):
                    rp.remove(sf)
                sf = rp.makeelement(qn("a:solidFill"), {})
                clr = sf.makeelement(qn("a:srgbClr"), {"val": run["color"].lstrip("#")})
                sf.append(clr)
                rp.insert(0, sf)


def scale_bars(slide, specs, warn=print):
    """Resize bar shapes to the data. Each spec: {"shapes": [...], "values": [...], "axis": "vertical"|"horizontal",
    "labels": [...]} - the largest value keeps the template's largest bar; bars grow from their base (bottom or left);
    optional label shapes move with the end of their bar."""
    by_name = {sh.name: sh for sh in slide.shapes}
    for spec in specs:
        bars = [by_name.get(n) for n in spec["shapes"]]
        if None in bars or len(bars) != len(spec["values"]):
            warn(f"bars: shapes {spec['shapes']} not found or values do not match")
            continue
        vertical = spec.get("axis", "vertical") == "vertical"
        size = (lambda b: b.height) if vertical else (lambda b: b.width)
        full = max(size(b) for b in bars)
        vmax = max(spec["values"]) or 1
        labels = [by_name.get(n) for n in spec.get("labels", [])]
        for i, (b, v) in enumerate(zip(bars, spec["values"])):
            new = int(full * v / vmax)
            delta = new - size(b)
            if vertical:
                b.top, b.height = b.top - delta, new
            else:
                b.width = new
            if i < len(labels) and labels[i] is not None:
                if vertical:
                    labels[i].top = labels[i].top - delta
                else:
                    labels[i].left = labels[i].left + delta


def add_template_slide(prs, s, warn=print):
    tid = s["template"]
    src = template_slide(tid)
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    _copy_shapes(src, slide)
    if s.get("repeat"):
        apply_repeat(slide, catalog()[tid].get("repeat", []), s["repeat"], warn)
    values = dict(s.get("slots", {}))
    values.setdefault("title", s.get("title", ""))
    if s.get("source"):
        values.setdefault("source", [[{"text": "Source: ", "bold": True}, {"text": s["source"]}]])
    drop = set(s.get("drop", []))
    by_name = {}
    for sh in slide.shapes:
        by_name.setdefault(sh.name, []).append(sh)
    for name in drop:
        for sh in by_name.get(name, []):
            sh._element.getparent().remove(sh._element)
    for name, val in values.items():
        targets = [sh for sh in by_name.get(name, []) if sh.has_text_frame]
        if not targets:
            warn(f"template {tid}: no shape named '{name}'")
            continue
        set_text(targets[0], val)
    if s.get("bars"):
        scale_bars(slide, s["bars"], warn)
    if not s.get("source"):
        for sh in by_name.get("source", []):
            sh._element.getparent().remove(sh._element)
    left = sorted({sh.name for sh in slide.shapes if sh.has_text_frame and PLACEHOLDER.search(sh.text_frame.text)
                   and sh.name not in drop})
    if left:
        warn(f"template {tid}: unfilled placeholders in {', '.join(left[:8])}{'...' if len(left) > 8 else ''}")
    return slide
