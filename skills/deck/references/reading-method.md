# Reading method: how to extract a reference document into the bank

Use this method whenever the user sends an article, a report or slides as a model to learn from. The output is one entry in `bank/sources/`, anonymised, validated element by element by the user. Read top-down, and report in the same order: the architecture matters more than the phrasing.

## The unit of analysis is a vector: (role, target)

Every element of the document, from a sentence to an exhibit, does one thing (its **role**) for one other element (its **target**): the section title, the exhibit, the next section, the introduction. An element without a target is filler. Record both for every element you analyse.

## Level 0: context and genre, before anything else

- **Issuer, reader, intention**: who writes, for whom, to obtain what (inform, convince, sell a mission). Mark the intention as your reading when the text does not state it.
- **Why now**: the change that makes the document timely.
- **Genre**: one primary genre and, if needed, one secondary genre for a section, from `bank/genres.yaml`.
- **Arc variant**: compare the document's arc with the genre's default arc and its known variants. Reuse a variant if it matches; otherwise propose a new variant, named after its logic, for the user to validate. A genre is a category; the way of arguing inside it can differ from one example to the next.
- **Evidence regime**: what counts as proof here (market data, project experience, calculated figures, test indicators). It must fit the genre.

## Level 1: skeleton, titles only

Read section titles and exhibit titles in order, without the body.
- **Move** of each title relative to the previous one, from a closed list: `reframe` (names the real subject by setting aside the wrong one), `zoom_in`, `zoom_out`, `split` (MECE bucket at the same level), `answer`, `prove`, `condition`, `decide`.
- **Zoom level**: 1 system or market, 2 process, 3 mechanism. The sequence of levels is the document's narrative signature.
- **Funnels and buckets**: a funnel is a run of titles going down in zoom; a bucket splits at the same level.
- **SCQA mapping**: which sections carry situation, complication, question, answer.

## Level 2: inside each paragraph

For each sentence: its role, from `observation`, `concession`, `thesis`, `mechanism`, `example`, `sourced_figure`, `nuance`, `reversal`, `consequence`, `restate_title`, `bridge` (to an exhibit or the next section); and its target.
Then name the paragraph's shape (for example: concession then thesis; announced count, bucket, return to the title) and the path the sentences draw towards the title. Note the sentence that calls each exhibit and what the next paragraph does with it.

## Level 3: exhibits

For each exhibit:
- **Served claim**: the sentence that calls it and the title it proves.
- **Logical relation**: Zelazny comparison for data (component, item, time, frequency, correlation) or a conceptual relation (sequence, before/after, layers, convergence, gated phases...).
- **Visual vectors**: each visual element and the meaning it carries (position, direction of arrows, colour, size, count of boxes, width of a band).
- **Typography**: hierarchy of sizes; which numbers are large and why.
- **Title pattern**, abstracted with slots.
- **Slots**: number of items and text length, so the layout can be rebuilt by code.

## Level 3b: design specification, read in the same pass

Read the design with the claim it serves: a choice (two flows sharing entry and exit nodes, one rectangle among circles) only makes sense against its title. Capture the design from the same screenshots, never in a second pass.
- **Anatomy**: what sits above and below the body (label, title, scope line, legend, sources, note) and in which style.
- **Palette by role**: each colour and the meaning it carries (established, new, context, current state, negative). Sample approximate hex codes from the screenshot; mark them approximate.
- **Shapes and lines**: fills versus outlines, corner radius, shadows, arrow and connector style, what a unique shape singles out.
- **Typography**: typeface family per role (message, labels, data), relative sizes, case, weight.
- **Grid**: columns, alignment, which elements share an axis.
- **Verdict**: keep, adapt or leave, with the reason.

When several documents share an issuer, record its design system once in `bank/design-systems/` and keep only the exhibit-specific choices in each source entry.

## Level 4: threads between levels

Look for what ties the document together: an introduction that previews the sections (fractal structure), a recurring image or phrase, a figure announced early and explained later, visual rhymes between exhibits (same position, same colour for the same meaning), title rhymes.

## Filter and anonymise before writing the entry

- **A shared reference is relevant by default.** The bank records several valid ways of arguing and designing, tagged by genre and context; there is no single right way. Extraction looks first for what works.
- **Tensions with the house rules are recorded, not discarded.** Each goes to `house_rule_tensions` with a handling:
  - `use_sparingly`: tolerated in moderation ("not X but Y", "not just X", intensifiers such as significantly or dramatically); note how often the source uses it and where it works.
  - `adapt_for_slides`: kept as an idea, rebuilt to fit the deck rules (semicolon in a slide title, scope line under a title, topic-label section titles, hedging adverbs).
- **Anonymise**: no client or company name, no figure, no date, no verbatim sentence. Patterns use slots (`{actor}`, `{process}`, `{kpi}`, `{milestone}`); examples are paraphrased in a few words.
- **Status**: every element starts `pending`. The user sets `validated`, `edited` or `rejected`. Only validated elements are used at generation.
