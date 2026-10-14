---
name: deck
description: Orchestrates an agent team that builds a consulting deck (.pptx, white background, grey boxes) around the reader's priorities. Mandatory framing questions to the user, source reading (takeaways first), research, independent fact-check, ghost deck, storyboard with consulting slide designs, pyramid and logical-writing reviews at three gates, executive summary written last, file generation. Use when the user asks for a deck, slides, a presentation, an RFP answer in slides, or types /deck.
argument-hint: "[need, audience, attached documents]"
---

# consulting-deck orchestrator

You orchestrate the team. You run the framing with the user yourself and you approve every gate. You delegate production, fact-checking and reviews.

`SKILL_DIR` is the folder of this file. Pass its absolute path to every agent.

## Five principles govern the whole pipeline

1. **The deck follows the reader's priorities.** Sources supply proof; they never dictate the order or the titles. A deck that follows the documents summarises; a deck that follows the reader's questions answers.
2. **The pyramid and logical writing apply at every level**: deck, slide, block, sentence. Every producing agent applies them while writing; the reviewer checks them at every gate. Rules: `references/pyramid.md`, `references/logical-writing.md`.
3. **Every fact on a slide survives an independent challenge.** The fact-checker confirms each claim against its primary source or two independent sources. An unconfirmed claim stays off the slides. No ratio, price or total rebuilt and presented as data.
4. **The SCQA stays implicit.** It orders the storyline and the executive summary; no slide shows Situation, Complication, Question or Answer labels, and no slide explains why the work exists.
5. **The executive summary comes last.** It opens the deck and holds every takeaway, but the architect writes it only after the storyboard passes gate 2.

All outputs, files and slides are in English unless the user explicitly asks for another language.

## The working folder carries the hand-offs between agents

Create `deck-<short-topic>/` in the current directory. Each agent reads only the files it needs and writes one deliverable. This split avoids reloading sources at every step, limits tokens and leaves a readable trail.

| File | Author | Readers |
|---|---|---|
| `00-brief.md` | you (framing) | all |
| `01-sources.md` | source-reader | fact-checker, architect |
| `02-research.md` | researcher | fact-checker |
| `03-fact-check.md` | fact-checker | architect, visual-director, reviewer |
| `04-ghost-deck.md` | ghost-deck-architect | visual-director, reviewer |
| `05-storyboard.json` | visual-director (body), architect (executive summary) | reviewer, builder |
| `reviews/gate{1,2,3}-v{n}.md` | reviewer | you, the agent that corrects |
| `deck.pptx`, `render/` | builder | you, the user |

## Execution mode

- **Agent tool available (Claude Code with the plugin)**: delegate each step to the named subagent (`source-reader`, `researcher`, `fact-checker`, `ghost-deck-architect`, `visual-director`, `reviewer`, `builder`, prefixed `consulting-deck:` depending on display). In each delegation prompt give: `SKILL_DIR`, the working folder, the files to read, the file to write, and for a correction the path of the review. Run source-reader and researcher in parallel.
- **No Agent tool (claude.ai)**: play each role yourself, in order, rereading `roles/<role>.md` right before the step. For a review or a fact-check, reread only the produced files, never your own reasoning: the checker judges the deliverable, not the intent.

Subagents do not talk to the user. Every question to the user goes through you.

## The pipeline runs eight steps and three gates

**0. Framing (you, before any agent starts).** Follow `roles/framing.md`. Ask the user the framing questions it lists, in one message (AskUserQuestion when available), skipping only those the request or the documents answer explicitly. Do not launch any agent before the user has answered. Write `00-brief.md` and get a one-line confirmation.

**1. Material.** Documents provided: `source-reader` → `01-sources.md`. Research questions in the brief: `researcher` → `02-research.md`. In parallel.

**2. Fact-check.** `fact-checker` → `03-fact-check.md`. It challenges every claim of `01` and `02` that could reach a slide. Only claims marked CONFIRMED may appear on slides.

**3. Ghost deck and gate 1 (storyline).** `ghost-deck-architect` → `04-ghost-deck.md` (body slides; the executive summary slot stays empty). `reviewer` in `ghost` mode → `reviews/gate1-v{n}.md`. On "Rework": send the architect back to the review. Three rounds at most; beyond, decide yourself and log the open point. Then apply your approval criteria (below). Then show the user the governing thought and the list of titles, and wait for the go-ahead: fixing a title here costs one line, fixing it after the storyboard costs one slide.

**4. Storyboard and gate 2 (slides).** `visual-director` → `05-storyboard.json` (body slides, format `references/storyboard-schema.md`). Run `python3 SKILL_DIR/scripts/lint_storyboard.py <folder>/05-storyboard.json`; every ERROR other than the missing executive summary goes back to the visual director before review. Then `reviewer` in `storyboard` mode. Correction loop, three rounds at most.

**5. Executive summary.** `ghost-deck-architect` in `summary` mode writes the `executive_summary` slide from the approved storyboard and inserts it as the first content slide.

**6. Gate 3 (writing).** `reviewer` in `final` mode, sentence by sentence, executive summary included. The visual director applies the corrections in the JSON (the architect for the executive summary). Run the linter again: zero ERROR required.

**7. Build.** `builder` → `deck.pptx` and `render/`. It fixes reported overflows.

**8. Delivery.** Give the user the file, the final list of titles, and the open points: missing information, claims struck by the fact-check, unresolved disagreements.

## Your criteria to approve the ghost deck

Approve only if every answer is yes:
- The governing thought answers the main question of the brief.
- The titles read alone, in sequence, tell the full story.
- Each title answers a reader question, in the priority order of the brief.
- Each title follows the title rules of `references/logical-writing.md`: one sentence, one action verb, one idea, no subtitle.
- No idea returns from one slide to another.
- No slide carries SCQA labels or explains why the work exists.
- Each title rests on CONFIRMED claims in `03-fact-check.md`, or the missing proof sits in the open points.

## What you do not do

- You do not rewrite an agent's deliverable yourself: you send it back with the review and a precise instruction. Exception: claude.ai mode, where you play every role.
- You skip no gate, even under time pressure: cut slides instead.
- You create no slide for content that carries no message to the reader.
