# consulting-deck

An agent team for Claude that builds consulting decks around the reader's priorities and proves every answer with fact-checked sources. Output: an editable .pptx on a white background, grey boxes, one accent colour.

```
/consulting-deck:deck Steering-committee deck on the KYC redesign, from the three attached PDFs
```

## The pipeline separates thinking from formatting

```
Framing questions to the user (orchestrator) ── no agent starts before the answers
   │  decision, reader, reader's questions by priority, format, material, hypothesis
   ├──► source-reader ───► takeaways first, facts with page references
   └──► researcher ──────► facts traced to their origin
            ▼
   fact-checker ─────────► every claim CONFIRMED, CORRECTED or REJECTED
            ▼
   ghost-deck-architect ─► governing thought, pyramid, titles (SCQA implicit)
            ▼
   GATE 1  reviewer (storyline) + orchestrator approval + user go-ahead
            ▼
   visual-director ──────► block content + slide design per slide (JSON)
            ▼
   GATE 2  linter + reviewer (title coverage, scope, design, data)
            ▼
   ghost-deck-architect ─► executive summary, written last, placed first
            ▼
   GATE 3  reviewer (logical writing, sentence by sentence)
            ▼
   builder ──────────────► deck.pptx, PNG render, overflow fixes
```

Four choices shape the tool:

- **The pyramid and logical writing are no steps.** They are references (`skills/deck/references/`) that every agent applies while writing and that the reviewer checks at every gate, from deck to sentence.
- **Checkers never judge their own work.** The fact-checker did not collect the facts; the reviewer did not write the deck. Each runs in a separate context.
- **The SCQA orders the storyline and stays invisible.** No context slide, no labels. The executive summary opens the deck and is written last.
- **Agents hand off through files** (`00-brief.md` → `05-storyboard.json`). Each agent reads only what it needs, which limits tokens and leaves a trail you can reread.

## Nineteen slide designs encode the standard consulting relations

`executive_summary`, `columns`, `rows`, `bullets`, `progression` (growing boxes with arrow), `chevrons`, `matrix` 2x2, `table` with Harvey balls, `chart_text` (chart with callouts), `big_number`, `waterfall`, `funnel`, `before_after`, `timeline`, `gantt`, `tree` (issue tree), `quotes`, `recommendation`, `cover`. The visual director picks the design from the relation between blocks (`references/layouts.md`). Charts are native PowerPoint objects, so they stay editable.

Demo: `examples/demo-layouts/` (storyboard JSON and generated deck).

## Install

**Claude Code (recommended: separate agents)**
```bash
claude plugin marketplace add <your-account>/consulting-deck
claude plugin install consulting-deck@consulting-deck
```
Then in a session: `/consulting-deck:deck <your need>`. Requires Python 3.9+ and `pip install python-pptx`. LibreOffice and poppler are optional, for the visual render check.

**claude.ai (sequential mode)**
```bash
python3 tools/package_skill.py   # writes dist/deck.zip
```
Upload `dist/deck.zip` in Claude's settings under Skills, with code execution on. Without subagents, the orchestrator plays each role in turn and rereads its role file before each step.

**Scripts only**
```bash
python3 skills/deck/scripts/lint_storyboard.py storyboard.json
python3 skills/deck/scripts/build_deck.py storyboard.json -o deck.pptx
python3 skills/deck/scripts/render_check.py deck.pptx render/
```

## Repo layout

```
.claude-plugin/        plugin and marketplace manifests
agents/                Claude Code subagents (generated from the roles)
skills/deck/
  SKILL.md             orchestrator: pipeline, gates, approval criteria
  roles/               one file per role: single source of the prompts
  references/          pyramid, logical writing, consulting practices, source quality,
                       layouts, charts, storyboard schema
  scripts/             .pptx generator, linter, PNG render
tools/                 role → agent sync, claude.ai packaging
examples/              demo deck
```

To change an agent, edit `skills/deck/roles/<role>.md`, then run `python3 tools/sync_agents.py`.

## Adapting to a corporate template

The house style lives in the constants at the top of `build_deck.py` (colours, font, margins) and in `meta.accent` of the storyboard. To add internal examples (winning proposals, battle cards), create a `references/internal-examples/` folder outside the public repo and cite it in the architect's role.

## Known limits

- The linter spots likely passive voice and second verbs with regular expressions: it misses some and flags false ones. Gate 3 stays necessary.
- Text fitting estimates glyph widths. LibreOffice renders slightly differently from PowerPoint; the builder checks overflow on the render.
- Consulting-practice references come from practitioner accounts, not from the firms' internal manuals (see `references/consulting-practices.md`).
- Chart figures in the demo are fictitious.

## Credits

The architecture draws on [enterprise-ai-skills](https://github.com/sruthir28/enterprise-ai-skills) (strategist, builder, critic chain) and [pyramid-principle](https://github.com/tyroneross/pyramid-principle) (canonical rules in one place). The code and prompts of this repo are original.

MIT licence.
