---
name: deck
description: Orchestrates an agent team that builds a consulting deck (.pptx, white background, grey boxes). Always asks framing questions first (deck kind argument or benchmark, expected slides and exhibits, reader, material). One persistent engagement manager holds the whole reasoning, spawns and resumes its researchers, and writes the ghost deck and executive summary; an independent challenger reviews gate 1; one targeted fact-check of displayed figures; resumed reviewers re-check only what changed; deterministic build and visual QA. Use when the user asks for a deck, slides, a presentation, a benchmark, an RFP answer in slides, or types /deck.
argument-hint: "[need, audience, attached documents]"
---

# consulting-deck orchestrator

You run the framing with the user, route work between agents, hold the user gates and run the scripts. You do not do the thinking: the engagement manager does.

`SKILL_DIR` is the folder of this file. Pass its absolute path to every agent.

## How the team saves tokens: one context per job, resumed instead of restarted

A new subagent starts cold and rereads everything before writing a line. A **resumed** subagent (`SendMessage` to its agent ID) keeps its full history and reads it from the prompt cache. So the team is built around agents that stay alive:

| Agent | Lives for | Resumed for | Cache |
|---|---|---|---|
| engagement-manager (Opus) | the whole run | gate 1 fixes, user feedback, fact-check results, executive summary | 1 h |
| researcher × ≤3 (Sonnet) | the research loop | the second cycle, by the engagement manager | 5 min |
| challenger (Opus) | gate 1 | one re-check on the change list | 1 h |
| visual-director (Sonnet) | storyboard to visual QA | gate 2 and visual-QA fixes | 5 min |
| slide-reviewer (Sonnet) | gate 2 | one re-check on changed slides | 5 min |
| source-reader (Haiku), fact-checker (Sonnet), visual-qa (Haiku) | one task | | 5 min |

Rules that follow:
- **Record every agent ID** in `run-log.md` (agent, ID, step, files passed, outcome). Never spawn a second agent of a type that is still alive for the same job: resume it.
- **Resume five-minute agents promptly.** Send the visual director its corrections as soon as the review lands; past five minutes, its cache expires and the resume rereads everything at full price.
- **Pass the smallest input**: file paths, never pasted content; register excerpts (`scripts/excerpt.py`); outlines instead of the storyboard (`scripts/extract_outline.py`); a change list instead of a full file on re-checks.
- **Apply wording-only corrections yourself** (a verb, an adverb, a number format). Send agents only structural or content corrections.
- **One check per fact.** A CONFIRMED row is never checked again; reviewers turn doubts into open points, never into new research.
- Ceiling: 14 agent spawns per deck (resumptions do not count). Before exceeding it, ask the user and say what the extra spawn would change.

All outputs are in English unless the user asks otherwise.

## Principles
1. **The deck fills the structure the user expects.** Framing captures expected sections, units and exhibits; every one gets a slide, with "n.d." where data is missing. Sources decide what slides say, never which slides exist.
2. **Two kinds of deck**: argument (pyramid under a governing thought) or benchmark (grid of units × dimensions, titles concluding on the grid).
3. **Research and thinking co-evolve inside one context**, the engagement manager's, in at most two cycles (`references/reasoning-loop.md`).
4. **Only displayed figures are fact-checked**, once, after gate 1.
5. **The pyramid and logical writing apply at every level** (`references/rules-card.md`); the SCQA stays implicit; the executive summary comes last.
6. **Every rule-based check runs as code.**

## Pipeline

**0. Framing (you, always).** Follow `roles/framing.md`: ask the framing questions in one message and wait for the answers. No agent starts before. Write `00-brief.md`. When the user later changes a structural rule, edit the brief's Structure section in place.

**1. Sources.** Documents provided: one `source-reader` per heavy document, in parallel (≤ 3).

**2. Reasoning and research (engagement manager, one call).** Spawn `engagement-manager` with: `SKILL_DIR`, the working folder, `00-brief.md`, the `01-sources-*.md` files. It builds the map, spawns and resumes its researchers, stabilises the reasoning and writes `03-ghost-deck.md`. It replies with a summary of 15 lines.

**3. Gate 1, challenge.** Spawn `challenger` (inputs listed in its role). Apply its wording corrections yourself. Structural corrections: resume the engagement manager with `reviews/gate1.md`; it replies with a change list; resume the challenger with that change list for one re-check.

**4. Gate 1, user.** Show the user the titles read alone, the exhibit sketches, the challenger's open points and the main residual uncertainties. Wait for the go-ahead. Feedback: resume the engagement manager with it.

**5. Fact-check, once.** Build the excerpt of the displayed figures (`excerpt.py research/*.md 01-sources-*.md <refs>`) and spawn `fact-checker`. Then resume the engagement manager with its reply so it adjusts titles and exhibits hit by CORRECTED or REJECTED figures.

**6. Storyboard.** Spawn `visual-director`. Run `lint_storyboard.py`; send ERRORs back to it (resume).

**7. Gate 2.** `extract_outline.py 04-storyboard.json > outline.md`; spawn `slide-reviewer`. Wording fixes: you. Content fixes: resume the visual director at once; then resume the slide-reviewer with the list of changed slides for one re-check.

**8. Executive summary.** `extract_outline.py 04-storyboard.json --titles-only > outline-titles.md`; resume the engagement manager to write it.

**9. Build (code).** Lint (zero ERROR), `build_deck.py`, `render_check.py`. Install `python-pptx` if missing.

**10. Visual QA.** Spawn `visual-qa`; resume the visual director with the flagged slides; rebuild once.

**11. Delivery.** Send the .pptx to the user, with the titles, residual uncertainties and what the deck does not claim, figures struck by the fact-check, open points, and the spawn count from the run log.

## Without the Agent tool
If you cannot spawn subagents, play each role yourself in this order, rereading `roles/<role>.md` before each step. Your own context then plays the engagement manager's role; for the challenger and the slide review, judge only the written deliverables against the brief.

## Approval criteria for the ghost deck
- Every section, unit and exhibit the brief expects has its slide; nothing excluded appears.
- Argument: the governing thought answers the decision and matches the map. Benchmark: the grid is complete, gaps shown as "n.d.".
- Titles read alone tell the story; each follows the title rules; none claims more than the evidence.
- Persistent tensions sit on a slide or are stated as limits.
- No idea repeated across slides; no SCQA labels; no "why this work" slide.
