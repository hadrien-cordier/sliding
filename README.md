# consulting-deck

An agent team for Claude that builds consulting decks, argument or benchmark, around one persistent reasoning context, and fact-checks every figure it displays. Output: an editable .pptx on a white background, grey boxes, one accent colour.

```
/consulting-deck:deck Steering-committee deck on the KYC redesign, from the three attached PDFs
```

## One context per job, resumed instead of restarted

```
Framing questions to the user (orchestrator) ── always, before any agent starts:
   │   deck kind, expected slides and exhibits, benchmark grid, reader, material
   ▼
source-reader (Haiku) ──► one call per heavy document, relevant sections only
   ▼
engagement-manager (Opus, one persistent context) ──────────────────────────┐
   map → spawns researchers (Sonnet, ≤3) → revises hypotheses on their       │
   compact answers → resumes the same researchers for cycle 2 →             │
   falsification test → ghost deck with exhibit sketches                     │
   ▼                                                                         │
GATE 1  challenger (Opus) → engagement manager fixes → challenger re-checks  │
        the change list → user sees titles and sketches ── feedback ────────►│
   ▼                                                                         │
fact-checker (Sonnet) ──► displayed figures only, once ── results ──────────►│
   ▼                                                                         │
visual-director (Sonnet, stays alive) ──► storyboard · lint (code)           │
GATE 2  slide-reviewer (Sonnet) → visual director fixes → one re-check       │
   ▼                                                                         │
executive summary ◄── engagement manager, resumed with the titles outline ◄──┘
   ▼
build and render (code) · visual-qa (Haiku) → visual director fixes
```

What keeps token use down:

- **Thinking happens in one context.** The engagement manager holds the brief, the map, the research answers and the storyline for the whole run. The hypothesis → research → revision loop runs inside it, with no hand-off and no reread.
- **Agents are resumed, not restarted.** A resumed subagent keeps its full history and reads it from the prompt cache. Researchers keep their sources for the second cycle; the challenger and the slide-reviewer re-check only the change list; the visual director applies fixes to a storyboard it already holds.
- **Cache lifetimes match waiting times.** The engagement manager and the challenger, who wait through the user's gate 1 review, keep a one-hour cache; the others keep the five-minute default and are resumed promptly.
- **One check per fact.** Only displayed figures are fact-checked, once; reviewers never re-verify.
- **Small inputs.** A one-page rules card, register excerpts (`scripts/excerpt.py`), compact outlines (`scripts/extract_outline.py`), and replies capped at 10 to 25 lines.

What keeps the deck on target:

- **The structure comes from the user.** Every expected slide and exhibit exists, with "n.d." where data is missing.
- **Two kinds of deck.** Argument decks prove a governing thought; benchmark decks fill a grid.
- **An independent challenger** tests the reasoning the engagement manager built.

## Twenty-two slide designs

Argument: `executive_summary`, `columns`, `rows`, `bullets`, `progression`, `chevrons`, `matrix` 2x2, `table` with Harvey balls, `chart_text`, `big_number`, `waterfall`, `funnel`, `before_after`, `timeline`, `gantt`, `tree`, `quotes`, `recommendation`, `cover`.
Benchmark: `market_map` (treemap sized by value, one colour per group), `band_matrix` (units × banded attributes, ●/○, "n.d.", computed values in blue), `fact_sheet` (one card per unit).

Demos: `examples/demo-layouts/` and `examples/demo-benchmark/`.

## Install

**Claude Code in the Claude app (web, desktop or mobile, recommended)**: the agent team needs Claude Code. In a Claude Code session, add the marketplace `hadrien-cordier/sliding`, install `consulting-deck`, then run `/consulting-deck:deck`. The .pptx comes back in the conversation, ready to download.

**claude.ai chat (plugin)**: Customize > Plugins > Add > Add marketplace > Add from a repository, enter `hadrien-cordier/sliding`, install `consulting-deck`, then type `/` and pick `deck`. Chat runs the skill and its scripts; if subagents are unavailable there, the orchestrator plays the roles in sequence.

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
