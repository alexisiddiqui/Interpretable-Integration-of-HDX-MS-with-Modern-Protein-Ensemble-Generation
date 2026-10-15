# Agent instructions

## Writing in my voice

Before drafting, rewriting or editing prose (thesis `.tex`, manuscript text, captions, chapter hubs or claim wording in `kb/`), read, in order:

1. `kb/voice/style.md`: argumentative habits and register per chapter
2. `kb/voice/spag.md`: spelling, punctuation and grammar
3. `kb/voice/examples.md`: annotated passages to model sentences on

Run the checklist at the end of `style.md` before handing a draft back. The voice notes guide wording only; evidence still comes from `kb/claims/` and `kb/papers/` (see `kb/README.md`).

<!-- Draft from the full claim note (Argument and Caveats), and draft a chapter one section at a time, stopping for review after the first. In `.tex`, refer to chapters and sections with `\cref`, never hard-coded numbers, and give every section a `\label`. -->

## Sources and hub upkeep

The aim of `kb/` is to get the thesis written. Do not add bookkeeping for its own sake.

**Trust order.** BMSB chapters (`@bmsb2012ch*`) > ValDX `projects/1-ValDX/manuscript/report/*_omc.tex` > jaxENT `projects/2-jaxENT/manuscript/report/*.tex` > confirmation `milestones/2025-11-confirmation-of-status/introduction/*.tex` > other papers in `kb/papers/`. I have checked and written the manuscripts. A point that one of them makes is settled: reuse its wording and cite the file and line. Do not open a task to "assemble a claim note", find a primary source or check the paper for it, and do not hedge it.

**Hub lines.** Never cut a line from a chapter hub because its citation is weak or missing; the phrasing is the value. Keep the line where it sits and fix the citation, or mark it `(own)` if it is the thesis's own reading. Hubs carry no status markers and no "drafting caution", "do not say…" or "(draft; its citations only…)" asides. Technical facts stay, stated as facts.

**Gaps sections.** An entry is something that blocks writing a paragraph: a missing result or figure, an open scope decision, or a citation the text needs with none in hand. One line each. Never list `read:`/`reviewed:`/`quote_check` status, dropped, replaced or superseded claims (git keeps history), dates, Zotero import lists, "inferred, not stated by a source" caveats, near-duplicate sets, or mis-citations noticed in passing. A mis-citation goes in that claim note as `needs_review: true` with a `review_reason`; the review queue picks it up. If a Gaps section would be empty, delete it.
