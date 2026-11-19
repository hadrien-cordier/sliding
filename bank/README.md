# Bank: what the deck engine learns from reference documents

The bank stores what makes a good document work, never its content: genres and their arcs, narrative moves, paragraph shapes, exhibit layouts and title patterns, all anonymised.

## Files
- `genres.yaml`: eight genres (reader question, evidence, default arc, typical exhibits) and the arc variants learned from examples. A default arc is a starting point: two examples of the same genre can argue differently, and each validated one adds a variant.
- `sources/<id>.yaml`: one extraction per reference document, produced with `skills/deck/references/reading-method.md`.
- `design-systems/<id>.yaml`: the design system of an issuer, recorded once and referenced by its source entries. Roles and rules transfer to decks; colours do not.

## How an entry gets in
1. The user sends a reference (article, report, slides).
2. Claude extracts it top-down: context and genre, skeleton, paragraphs, exhibits, threads.
3. Claude filters out patterns that break the house rules and anonymises the rest.
4. The user validates, edits or rejects each element. Only validated elements are used.

## How generation uses it
Classify the input text by genre, pick the closest arc variant, then load only the patterns and exhibit fiches tagged with that genre or relation. The model reads a small slice of the bank, never the whole of it.

## Never in the bank
Client or company names, figures, dates, verbatim sentences, images, brand colours of an employer.
