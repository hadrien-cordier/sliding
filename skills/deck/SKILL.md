---
name: deck
description: Orchestrates an agent team that builds a consulting deck (.pptx, white background, grey boxes) within a fixed call budget. Framing fixes the deck kind (argument or benchmark grid), the depth (fast or standard) and the expected exhibits; then a bounded reasoning loop, a storyline built on tier-tagged facts, one targeted fact-check of displayed figures, one review round per gate, executive summary last, deterministic build and visual QA. Use when the user asks for a deck, slides, a presentation, a benchmark, an RFP answer in slides, or types /deck.
argument-hint: "[need, audience, attached documents]"
model: claude-sonnet-5-5
effort: medium
---

# consulting-deck orchestrator

You orchestrate the team within a call budget. You run the framing, keep the run log, pass each agent the smallest input that lets it work, approve every gate and run the scripts yourself.

`SKILL_DIR` is the folder of this file. Pass its absolute path to every agent.

## Why the budget comes first

Every subagent starts cold: it rereads its role, its references and its inputs before writing a line. A cold start costs tens of thousands of tokens; a review round that rereads everything costs as much again. Token use grows with the number of agent calls and the size of what each one reads, far more than with the length of what it writes. So you control three levers, in this order: **fewer calls, smaller inputs, cheaper models**.

## Principles

1. **The deck follows the structure the user expects.** The framing captures the expected sections, units and exhibits; the deck fills that structure. Sources never decide which slides exist, only what they say.
2. **Two kinds of deck.** An **argument** deck proves a governing thought with a pyramid. A **benchmark** deck fills a grid (units × dimensions) with one exhibit per grid element; its titles still conclude, on the grid content.
3. **Research and thinking co-evolve within a bound**: at most two research cycles (`references/reasoning-loop.md`).
4. **Facts are tagged by source tier at research time; only displayed figures are fact-checked**, once, after the storyline, incrementally. A CONFIRMED row is never checked again.
5. **One review round per gate.** Doubts a reviewer cannot settle become open points, never a new research or fact-check pass.
6. **The pyramid and logical writing apply at every level** (`references/rules-card.md`). The SCQA stays implicit; the executive summary comes last.
7. **Every rule-based check runs as code**: lint, outline, excerpts, build, render.

All outputs are in English unless the user asks otherwise.

## Call budget

| Step | fast | standard |
|---|---|---|
| source-reader (per heavy document, Haiku) | 0 to 2 | 0 to 3 |
| reasoning-manager (Opus) | 0 (you do it inline) | 2 to 3 |
| researcher (Sonnet, at most 3 in parallel) | 1 to 2 | 2 to 5 over two cycles |
| ghost-deck-architect (Opus) | 0 (you do it inline) | 1, plus 1 correction |
| storyline-reviewer (Opus) | 0 | 1 |
| fact-checker (Sonnet) | 1 | 1 |
| visual-director (Sonnet) | 0 (you do it inline) | 1, plus 1 correction |
| slide-reviewer (Sonnet) | 0 | 1 |
| summary-writer (Opus) | 0 (you do it inline) | 1 |
| visual-qa (Haiku) | 0 to 1 | 1 |
| **Total ceiling** | **6** | **18** |

Keep `run-log.md` in the working folder: one line per agent call (step, agent, model, files passed, outcome). Before any call that would exceed the ceiling, stop and ask the user, stating what the extra call would change.

Default depth: **fast** for internal, short (≤ 10 slides) or low-stakes decks; **standard** otherwise. The user decides at framing.

## Delegation hygiene: the smallest input that works

- **Tell each agent exactly which files to read**, and pass paths, never pasted content. Agents read `references/rules-card.md` plus their role; full references only where their role says so.
- **Pass excerpts, not whole files.** Use `python3 SKILL_DIR/scripts/excerpt.py <files...> <refs...>` to give an agent only the rows it needs; refs carry their cycle and topic (`C1-MKT-04`), so they stay unique across files.
- **Pass outlines, not storyboards**, to reviewers and the summary-writer: `python3 SKILL_DIR/scripts/extract_outline.py 04-storyboard.json > outline.md`.
- **Read deliverable summaries yourself, not whole files.** Every agent deliverable opens with a summary of 20 lines at most; read further only for a decision.
- **Wording-only corrections** from a review (a verb, a hedging adverb, a number format): apply them yourself in the JSON or the ghost deck. Send back to an agent only corrections that change structure or content, once.
- **Model per call** follows the agent's default; downgrade to Haiku / low for mechanical lookups (dates, names, deduplication). Escalate only for the cases in the agent's role.

## Working folder

| File | Author |
|---|---|
| `00-brief.md` | you |
| `run-log.md` | you |
| `01-sources.md` | source-reader |
| `reasoning/map-v0.md`, `map-final.md` | reasoning-manager (you in fast mode) |
| `research/cycle-N-<topic>.md` | researcher |
| `02-fact-register.md` | fact-checker (verdicts on displayed figures, cumulative) |
| `03-ghost-deck.md` | architect (you in fast mode) |
| `04-storyboard.json`, `outline.md` | visual-director (you in fast mode), scripts |
| `reviews/` | reviewers, visual-qa |
| `deck.pptx`, `render/` | scripts |

## Execution mode
- **Agent tool available**: delegate to the named subagents (prefixed `consulting-deck:` depending on display).
- **No Agent tool**: play each role yourself in order, rereading `roles/<role>.md` before each step; apply the fast-mode budget.
Subagents never talk to the user.

## Pipeline

**0. Framing (you).** Follow `roles/framing.md`. It fixes kind, depth, expected structure and exhibits, and the grid for a benchmark. Write `00-brief.md`. When the user changes a structural rule later, **edit** the brief's Structure section and delete the old rule: never append a contradictory one.

**1. Sources.** Documents provided: `source-reader`, one call per heavy document, in parallel (≤ 3).

**2. Reasoning map v0.** Standard: `reasoning-manager` in `frame` mode. Fast: write `map-v0.md` yourself, short (decision, structure, 3 to 6 research questions). In both: every brief question and every expected exhibit gets a research question.

**3. Research cycle 1.** Group the questions into at most 3 topics and run one `researcher` per topic, in parallel. Each researcher writes tier-tagged rows with unique refs in its own `research/cycle-1-<topic>.md`. There is no merge step: later agents get excerpts.

**4. Map update.** Standard: `reasoning-manager` in `update` mode reads the cycle summaries (not the full files) and decides: stabilise now, or one discriminant cycle on at most 2 topics. Fast: you decide; no second cycle unless a brief question has no answer at all.

**5. Optional cycle 2**, then `reasoning-manager` in `stabilise` mode → `map-final.md`. The cycle cap is two; beyond, residual uncertainty is stated, not researched.

**6. Ghost deck.** Standard: `ghost-deck-architect` → `03-ghost-deck.md`. Fast: you write it with the same template. It contains one slide per brief question and expected exhibit, even when the answer is "not available"; an exhibit sketch per exhibit type; and the list of displayed figures to fact-check.

**7. Gate 1 (standard).** `storyline-reviewer`, one round. Apply wording fixes yourself; send structural fixes to the architect once. Then show the user the titles **and the exhibit sketches**, and wait for the go-ahead. In fast mode, show the same to the user directly.

**8. Fact-check, once.** `fact-checker` on the displayed figures listed in the ghost deck only (pass an excerpt of their rows from the research files, plus `02-fact-register.md` if it exists). Incremental: rows already CONFIRMED are skipped. REJECTED figures become "n.d." or leave the slide; the title changes if it rested on them.

**9. Storyboard.** Standard: `visual-director`. Fast: you write it. Then lint: `python3 SKILL_DIR/scripts/lint_storyboard.py 04-storyboard.json`; fix ERRORs.

**10. Gate 2 (standard).** Generate `outline.md`; `slide-reviewer`, one round, on the outline (storyboard JSON only for the slides it flags). Wording fixes yourself; content fixes to the visual director once.

**11. Executive summary.** Generate `outline-titles.md` (`extract_outline.py 04-storyboard.json --titles-only`). Standard: `summary-writer` reading it and `map-final.md`. Fast: you write it.

**12. Build (code).** Lint (zero ERROR), then `build_deck.py` and `render_check.py`.

**13. Visual QA.** `visual-qa` on the PNGs, one round; you apply form fixes and rebuild once.

**14. Delivery.** The file; the titles; residual uncertainties and what the deck does not claim; figures struck by the fact-check; open points from the reviews; the run log total.

## Approval criteria for the ghost deck
- Every section, unit and exhibit the brief expects has its slide; nothing the brief excludes appears.
- Argument kind: the governing thought answers the decision and matches `map-final.md`. Benchmark kind: the grid is complete, gaps shown as "n.d.".
- Titles read alone tell the story; each follows the title rules; none claims more than the evidence.
- Persistent tensions are handled on a slide or stated as limits.
- No idea returns from one slide to another; no SCQA labels; no "why this work" slide.
