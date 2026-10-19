# consulting-deck

An agent team for Claude that builds consulting decks, argument or benchmark, within a fixed call budget, and fact-checks every figure it displays. Output: an editable .pptx on a white background, grey boxes, one accent colour.

```
/consulting-deck:deck Steering-committee deck on the KYC redesign, from the three attached PDFs
```

## The pipeline runs within a call budget

```
Framing (orchestrator) ── kind (argument | benchmark), depth (fast | standard),
   │                       expected slides and exhibits, benchmark grid
   ▼
source-reader (Haiku) ──► one call per heavy document, relevant sections only
   ▼
reasoning-manager (Opus) ──► map v0: at most 8 questions in at most 3 topics
   ▼
researcher × ≤3 (Sonnet) ──► ≤12 page reads each, facts tagged by source tier
   ▼
reasoning-manager ──► stabilise, or one discriminant cycle (two cycles at most)
   ▼
ghost-deck-architect (Opus) ──► one slide per expected item, exhibit sketches,
   │                              list of displayed figures
GATE 1  storyline-reviewer (Opus, one round) + user sees titles and sketches
   ▼
fact-checker (Sonnet) ──► displayed figures only, once, incremental
   ▼
visual-director (Sonnet) ──► storyboard · lint (code)
GATE 2  slide-reviewer (Sonnet, one round, on a compact outline)
   ▼
summary-writer (Opus) ──► executive summary, written last, placed first
   ▼
build and render (code) · visual-qa (Haiku, one round)
```

In **fast** mode the orchestrator writes the map, the ghost deck, the storyboard and the summary itself: about six agent calls in total. **Standard** mode stays under eighteen.

What keeps token use down:

- **Fewer cold starts.** Every subagent rereads its inputs before writing; the budget caps calls per step, and every agent has a `maxTurns` limit.
- **Smaller inputs.** Agents read a one-page rules card instead of the full references, register excerpts instead of registers (`scripts/excerpt.py`), and a compact outline instead of the storyboard (`scripts/extract_outline.py`). Every deliverable opens with a summary of 20 lines.
- **Checks where they matter.** Facts are tagged by source tier at research time; only the figures that will be displayed are fact-checked, once, and a CONFIRMED row is never checked again.
- **One review round per gate.** Wording fixes are applied by the orchestrator; doubts become open points, never new research.
- **Bounded research.** At most three researchers in parallel, twelve page reads each, two cycles, never a full annual report.

What keeps the deck on target:

- **The structure comes from the user.** Framing asks which slides and exhibits the user pictures; every expected item gets a slide, with "n.d." where data is missing, so source availability never decides the plan.
- **Two kinds of deck.** Argument decks prove a governing thought; benchmark decks fill a grid of units × dimensions.
- **The pyramid and logical writing apply at every level**, the SCQA stays implicit, and the executive summary comes last.

## Twenty-two slide designs

Argument: `executive_summary`, `columns`, `rows`, `bullets`, `progression`, `chevrons`, `matrix` 2x2, `table` with Harvey balls, `chart_text`, `big_number`, `waterfall`, `funnel`, `before_after`, `timeline`, `gantt`, `tree`, `quotes`, `recommendation`, `cover`.
Benchmark: `market_map` (treemap sized by value, one colour per group), `band_matrix` (units × banded attributes, ●/○, "n.d.", computed values in blue), `fact_sheet` (one card per unit).

Demos: `examples/demo-layouts/` and `examples/demo-benchmark/`.

## Install

**claude.ai (plugin, recommended)**: Customize > Plugins > Add > Add marketplace > Add from a repository, enter `hadrien-cordier/sliding`, install `consulting-deck`, then type `/` in a chat and pick `deck`.

**Claude Code**
```bash
claude plugin marketplace add hadrien-cordier/sliding
claude plugin install consulting-deck@consulting-deck
```
Then in a session: `/consulting-deck:deck <your need>`. Requires Python 3.9+ and `pip install python-pptx`. LibreOffice and poppler are optional, for the visual render check.

**claude.ai (skill zip, sequential mode, no subagents)**
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
agents/                subagents with model, effort and maxTurns (generated from the roles)
skills/deck/
  SKILL.md             orchestrator: pipeline, gates, approval criteria
  roles/               one file per role: single source of the prompts
  references/          rules card, reasoning loop, pyramid, logical writing, consulting practices,
                       source quality, layouts, charts, storyboard schema
  scripts/             .pptx generator, linter, PNG render, outline and excerpt helpers
tools/                 role → agent sync, claude.ai packaging
examples/              argument and benchmark demo decks
```

To change an agent, edit `skills/deck/roles/<role>.md`, then run `python3 tools/sync_agents.py`.

## Adapting to a corporate template

The house style lives in the constants at the top of `build_deck.py` (colours, font, margins) and in `meta.accent` of the storyboard. To add internal examples (winning proposals, battle cards), create a `references/internal-examples/` folder outside the public repo and cite it in the architect's role.

## Known limits

- The linter spots likely passive voice and second verbs with regular expressions: it misses some and flags false ones. The slide-reviewer stays necessary.
- Text fitting estimates glyph widths. LibreOffice renders slightly differently from PowerPoint; visual QA checks overflow on the render.
- Consulting-practice references come from practitioner accounts, not from the firms' internal manuals (see `references/consulting-practices.md`).
- Chart figures in the demo are fictitious.

## Credits

The architecture draws on [enterprise-ai-skills](https://github.com/sruthir28/enterprise-ai-skills) (strategist, builder, critic chain) and [pyramid-principle](https://github.com/tyroneross/pyramid-principle) (canonical rules in one place). The code and prompts of this repo are original.

MIT licence.
