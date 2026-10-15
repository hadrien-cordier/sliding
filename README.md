# consulting-deck

An agent team for Claude that builds consulting decks around the reader's priorities and proves every answer with fact-checked sources. Output: an editable .pptx on a white background, grey boxes, one accent colour.

```
/consulting-deck:deck Steering-committee deck on the KYC redesign, from the three attached PDFs
```

## Research and thinking co-evolve until one message is defensible

```
Framing questions to the user (orchestrator, Sonnet) ── no agent starts before the answers
   ▼
source-reader (Haiku) ──► claims, figures and quotes each document explicitly supports
   ▼
┌─► reasoning-manager (Opus) ──► reasoning map: decision, problem dimensions,
│                                competing narratives, evidence and tensions registers,
│                                open questions with stop conditions
│      ▼
│   researcher (Sonnet) ───────► cycle 1 coverage, then discriminant cycles that search
│                                for evidence against the leading narrative
│      ▼
│   claim-screener (Haiku) ────► pass 1: reference, figure, date, quote, duplicate
│   fact-checker (Sonnet) ─────► pass 2: exact support, scope, year, metric, causality
│      ▼
└── new cycle only while a high-impact question stays open
   ▼
reasoning-manager ──► falsification test, stabilised reasoning, what the deck cannot claim
   ▼
ghost-deck-architect (Opus) ──► governing thought, pyramid, titles, tensions placed
GATE 1  storyline-reviewer (Opus) + user go-ahead
   ▼
visual-director (Sonnet) ──► blocks and layout per slide, two candidates compared
lint (code) · GATE 2  storyboard-reviewer (Sonnet, high on key slides)
   ▼
summary-writer (Opus) ──► executive summary, written last, placed first
GATE 3  writing-reviewer (Sonnet, high)
   ▼
build and render (code) · visual-qa (Haiku) on the PNGs
```

Five choices shape the tool:

- **One agent owns the convergence.** The reasoning-manager decides what can be concluded; the architect decides in which order the reader meets it. Method: `skills/deck/references/reasoning-loop.md`.
- **Research stops on decision value.** Every research question carries its decision impact and a stop condition; a new cycle starts only while a high-impact question stays open.
- **Each task gets the cheapest model that does it well.** Haiku handles volume, Sonnet the standard professional work, Opus the decisions that structure the deck, code every rule-based check. The orchestrator escalates per task (policy table in `SKILL.md`).
- **Checkers never judge their own work.** The fact-checker did not collect the facts; the reviewers did not write the deck.
- **The pyramid and logical writing apply at every level**, the SCQA stays implicit, and the executive summary comes last.

## Nineteen slide designs encode the standard consulting relations

`executive_summary`, `columns`, `rows`, `bullets`, `progression` (growing boxes with arrow), `chevrons`, `matrix` 2x2, `table` with Harvey balls, `chart_text` (chart with callouts), `big_number`, `waterfall`, `funnel`, `before_after`, `timeline`, `gantt`, `tree` (issue tree), `quotes`, `recommendation`, `cover`. The visual director picks the design from the relation between blocks (`references/layouts.md`). Charts are native PowerPoint objects, so they stay editable.

Demo: `examples/demo-layouts/` (storyboard JSON and generated deck).

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
agents/                subagents with model and effort (generated from the roles)
skills/deck/
  SKILL.md             orchestrator: pipeline, gates, approval criteria
  roles/               one file per role: single source of the prompts
  references/          reasoning loop, pyramid, logical writing, consulting practices,
                       source quality, layouts, charts, storyboard schema
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
