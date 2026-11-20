# Exhibit templates

Native PowerPoint slides rebuilt from reference exhibits, with placeholder text and named shapes. No reference image is stored here.

- `catalog.yaml`: one index line per template (read at every generation), then one fiche per template (message pattern, visual vectors, details, slots).
- `lotA.pptx` to `lotJ.pptx`: the 41 templates, four or five per file (`file` and `slide` in the catalog). Shapes are named after their slots (`stage_3`, `kpi_2`...): code fills them by name.
- `build/`: the scripts that draw the templates. `theme.json` holds every colour by role; swap it for a brand and rebuild.

## How a template is rebuilt
1. **Measure the reference** (`measure.py`): solid regions, sizes, gaps, stroke widths, colours.
2. **Place shapes on the reference pixels** (`lib2.Frame`): proportions carry over exactly. `Frame2` stretches a tall reference to the 16:9 body.
3. **Use soft primitives** (`lib2`): rounded corners in inches, chevrons with a point depth, Bezier curves, tapered arrows with a flared head, round line caps, bars with rounded tops.
4. **Compare at full size** (`compare.py`) and have an independent reviewer list the defects before release.

## Use in a deck
A storyboard slide `{"layout": "template", "template": "<id>", "slots": {...}, "drop": [...], "bars": [...]}` is copied from its lot file and filled by `scripts/fill_template.py`. `slots_named` in each fiche lists the names to fill. Example: `examples/demo-templates/`.

Rebuild: `cd templates/build && python3 batchA.py ../lotA.pptx` (same for B to J), then `python3 name_slots.py` to name every placeholder shape and refresh `slots_named`.

Icons are placeholders (circles marked "icon"): replace them with PowerPoint icons of the same name and size.
