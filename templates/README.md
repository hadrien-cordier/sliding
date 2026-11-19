# Exhibit templates

Native PowerPoint slides rebuilt from reference exhibits, with placeholder text and named shapes. No reference image is stored here.

- `catalog.yaml`: one index line per template (read at every generation), then one fiche per template (message pattern, visual vectors, details, slots).
- `lot<n>.pptx`: the templates. Shapes are named after their slots (`stage_3`, `kpi_2`...): code fills them by name.
- `build/`: the scripts that draw the templates. `theme.json` holds every colour by role; swap it for a brand and rebuild.

Rebuild: `cd templates/build && python3 batch1.py ../lot1.pptx && python3 batch2.py ../lot2.pptx`

Icons are placeholders (circles marked "icon"): replace them with PowerPoint icons of the same name and size.
