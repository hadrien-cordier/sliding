# Logical writing: rules for every sentence

These rules codify the consulting writing practice of the project's author. No published method carries this name; the sourced foundation is Minto (`pyramid.md`), with practitioner guidance in `consulting-practices.md`. They apply to every text the team produces: titles, blocks, notes, intermediate deliverables.

## Structure
1. **Every paragraph, block or section answers a question.** If you cannot phrase the question, the block has no reason to exist.
2. **Every paragraph, block or chart title holds the main idea of what sits below it.** The text below details that idea. "Costs" is a label; "Compliance costs double in three years" is an idea.
3. **Idea, analysis, conclusion.** One sentence carries one claim.
4. **Answer first.** The conclusion comes before the arguments, at every level.

## Slide titles
5. **One sentence, affirmative, complete.** No question, no semicolon, no aside, no parenthesis.
6. **One action verb.** The title has one main verb that carries the message: "Automation cuts onboarding time by 40%". A second conjugated verb ("..., which drives...", "... while ...", "... and reduces ...") means a second idea: split the slide.
7. **One idea.** "And" may join items of one kind; it never joins two claims.
8. **Ternary rhythm is welcome.** Three parallel items of one kind under the single verb give weight and stay one idea: "The new process cuts cost, delay and error rate".
9. **No subtitle, no overline, no tagline.** If a title needs a subtitle, the title is wrong. Hierarchy stops at three levels: slide title, block title, text or list.
10. **The title carries the conclusion or the tension, never the topic.** It is specific and, when a confirmed figure allows, quantified.
11. **Aim for two lines at most.** A longer title is acceptable only if it still carries one idea with one verb.
12. **Consistent across the deck**: same tense (present by default), same syntax, same final punctuation (none).

## Sentences
13. **Active voice, always.** The subject acts. "The bank cuts its delays", not "Delays are cut". If the actor is unknown, find it; if it stays unknown, say so.
14. **Every word earns its place.** Remove what does not change the meaning.
15. **No hedging adverbs**: only, now, already, more than, just, really, very, still, currently, significantly. They weaken the claim. A precise figure replaces "more than".
16. **No "not X but Y" or "rather than"**: state Y.
17. **No em or en dash.** Use a comma, a full stop or two sentences.
18. **No rhetorical scaffolding or hollow intensifiers** ("it is important to note that", "key", "critical", "robust").
19. **Plain vocabulary in the reader's register.** No jargon the reader does not use.
20. **Explicit logical relations.** Say whether the next sentence is a cause, a consequence, a condition or a contrast.
21. **Known before new.** Each sentence starts from what the reader already has and ends on the new information.
22. **Main message before nuance.** State the claim, then its limit.
23. **Parallel lists.** Items of one list share one grammatical form.
24. **Stable vocabulary.** One term per concept across the whole deck; a new word suggests a new concept.
25. **Negation test.** If the negation of a sentence is absurd ("banks do not want to reduce risk"), the sentence says nothing: replace it with a claim someone could dispute.
26. **Certainty matches evidence.** A sentence claims no more than its proof and the confidence the reasoning map grants. Calibrate with scope ("in the five markets studied") rather than hedging adverbs.

## Figures
27. Every figure points to a named origin, with unit, scope and date, and appears in `02-fact-register.md` as CONFIRMED, CORRECTED or USER DOCUMENT.
28. No ratio, price or total rebuilt and presented as data.

## Rewrite examples

| Before | After | Rule |
|---|---|---|
| A review of the KYC process was launched | The bank redesigns its KYC process | 13 |
| Market overview | Three regulatory deadlines force a decision before June | 2, 10 |
| Automation reduces cost and the bank gains market share | Automation cuts cost by 30% (second slide: the cost gain funds market-share growth) | 6, 7 |
| Context: strong growth; multiple risks | The market grows 12% a year and exposes the bank to three risks | 5, 9 (two verbs: split if both matter) |
| Costs already exceed 20% of the budget | Costs reach 23% of the budget (origin, year) | 15, 27 |
| This is not a technology issue but an organisational one | The issue sits in the organisation | 16 |

## Automatic check
`scripts/lint_storyboard.py` detects part of these defects: likely passive voice, hedging adverbs, dashes, semicolons, question titles, likely second verbs, visible SCQA labels, subtitle fields, label-like block titles, figures without source. It does not replace review: a regular expression misses some passives and flags some false ones, and a title can pass every rule without carrying an idea.
