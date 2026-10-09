# Thesis knowledge base: design

Date: 2026-10-08
Status: draft, awaiting review
Scope of this spec: steps 1 to 3 in full (schema and lint, ValDX seed, introduction hub). Steps 4 and 5 are outlines and each gets its own spec.

## 1. Purpose

Assemble thesis chapters from claims that have already been checked against their sources, starting with the introduction (due 14 Oct 2026), then ValDX (28 Oct) and JaxENT (14 Nov).

The KB holds three kinds of content:

1. **Literature**: attributed claims from papers, each anchored to a page and a verbatim quote.
2. **Own work**: claims from the author's manuscripts and results, tied to figures and code.
3. **Example theses**: rhetorical moves and concept trails from three reference theses (Crook, Carlos, Vost). These are a writing aid, never evidence.

A fourth component, **methods**, follows later and must be able to map onto the same concepts.

### Success criteria

- For the introduction, every sentence drafted from the KB can be traced to a claim note, and every literature claim to a page and quote that a script has found in the source PDF.
- Nothing in the KB is marked `supported` on the strength of unverified LLM output.
- A method note can be traced to the code (file, lines, commit) it describes.
- The author only needs to open notes the KB has flagged as needing review.

## 2. Context (verified 2026-10-08)

- Repo: `Interpretable-Integration-of-HDX-MS-with-Modern-Protein-Ensemble-Generation` (Overleaf-synced, git).
- `kb/` is an empty Obsidian vault with templates `claim`, `concept`, `paper`, `decision`, `figure` and folders `chapters/ claims/ concepts/ methods/ papers/ decisions/ inbox/`.
- `kb/README.md` rules: one idea per note, links in body text, claims need evidence before leaving `draft`, figures referenced by ID, paper notes named `@<citekey>` matching `thesis/references.bib`.
- `thesis/references.bib` is empty (0 bytes); `01-introduction.tex` and `02-background.tex` are stubs.
- Seeds: `projects/1-ValDX/manuscript/` (clean, post-review; `main_omc.tex` inputs `report/1_introduction_omc`; `references.bib` has 779 entries), `milestones/2025-11-confirmation-of-status/introduction/` (`biological_dynamics`, `ensemble_generators`, `measuring_dynamics`, `connect_simulation_experiment`, `thesis_outline`).
- Code lives in pinned submodules under `projects/*/code`.
- `examples/*/thesis.json` (schema 2.0.0) already hold page-anchored `claims`, `entities`, `edges`, and `journey` stages for the three reference theses. Source PDFs are gitignored (`*.pdf`).
- Existing tooling lives in `tools/` (`project-map`, `thesis-map`).

## 3. Trust tiers

| Content | Who extracts | Who verifies |
|---|---|---|
| ValDX claims and its literature | Claude | Lint checks mechanically; the author resolves only notes flagged `needs_review` |
| Literature for the introduction | Claude (assumed, same tier as ValDX) | Same |
| JaxENT claims and methods | Claude proposes into `inbox/` only | The author promotes each note; the manuscript has outdated experiments, so its text is context, not evidence |
| Example theses | Generator script plus Claude for moves | Moves are flagged `needs_review`; nothing is evidence |

## 4. Note types

All notes are Markdown with YAML frontmatter. Existing templates are kept and extended.

### 4.1 Paper (`papers/@<citekey>.md`)

Frontmatter:

```yaml
type: paper
citekey:            # must exist in thesis/references.bib
year:
read: false
pdf:                # kb/_pdf/@<citekey>.pdf (gitignored); empty if unavailable
extraction: auto    # auto | manual | none
```

Attributed claims live as blocks in the body, one per claim, with an Obsidian block ID so other notes can link to a single claim (`[[@smith2020#^c3]]`):

```markdown
## Claims

- HDX-MS reports on backbone amide exchange. ^c1
  - page: 4
  - quote: "verbatim text, 25 words or fewer"
  - quote_check: unchecked
  - reviewed: false
```

- `page` is the 1-based **PDF page index**, not the printed page label (unambiguous for `pdftotext`).
- `quote_check` is `pass | fail | unchecked` and is written **only by the lint**.
- `reviewed` is written **only by the author**.
- With `extraction: none` no quote can be checked, so the claim stays `unchecked` and the paper note is flagged `needs_review`.

### 4.2 Own claim (`claims/<full sentence>.md`)

Existing fields (`type, chapter, project, basis, confidence, status`) plus:

```yaml
origin:                # file and anchor the claim was drawn from, e.g. projects/1-ValDX/manuscript/main_omc.tex#sec:intro
source_state: current  # current | outdated
needs_review: false
review_reason:         # one line; required when needs_review is true
figures: []            # figure IDs; each must exist as figures/<id>/
cites: []              # block links, e.g. "[[@smith2020#^c3]]"
code: []               # optional, see 4.6
```

`status` ladder: `draft` → `supported` → `in-thesis`.

- `supported` requires at least one resolvable `figures` or `cites` entry and a clean lint.
- A claim whose only origin is text with `source_state: outdated` stays `draft`.
- `in-thesis` is set when the claim is used in a `.tex` chapter.

### 4.3 Concept (`concepts/<name>.md`)

One shared namespace for literature, example theses and methods. Adds a notation table so chapters 3 to 6 share symbols:

```yaml
type: concept
aliases: []
notation:              # list of {symbol, meaning, units}
```

### 4.4 Method (`methods/<name> (<project>).md`)

```yaml
type: method
project:
code: []               # REQUIRED, at least one entry
status: draft
needs_review: false
review_reason:
```

Concepts the method implements are linked in the body text, per the existing rule. Reserved now, built in step 5.

### 4.5 Figure and decision

Figure note: existing fields plus optional `code:` (the script that makes it). Decision template unchanged.

### 4.6 Code references

A `code:` entry is a string:

```
projects/2-jaxENT/code@3f9a1c2:jaxent/models/hdx.py#L40-88
```

submodule path, `@`, commit SHA, `:`, file path, `#L`, line range. The SHA is recorded in the note, not inherited from the pinned submodule, so a later submodule bump cannot silently change what a note describes.

- Required on method notes. Optional on claim and figure notes. Not used on paper or example-thesis notes.

### 4.7 Example-thesis notes (`ref-theses/<author>/`)

Generated by a script from `examples/<author>-map/thesis.json`; carry `generated: true`. Anything under a `## Mine` heading is preserved on regeneration.

- `index.md`: thesis hub (arc and stages from `journey`).
- Move notes: `type: move`, `thesis`, `page`, `move_type`, a paraphrase, an optional locator quote of 25 words or fewer marked not for reuse. `needs_review: true` by default.
- Concept candidates: from `entities`; link to a shared concept when an alias matches, otherwise stay as candidates.
- Citation trails: raw reference strings only. They never create `@citekey` notes and never count as verification. A paper note is created only after the primary PDF has been read and quote-checked.

## 5. Lint (`tools/kb-lint/`)

Read-only by default. `--write` updates only `quote_check` fields and regenerates `kb/review-queue.md`. Errors fail the run; warnings do not.

| # | Check | Severity |
|---|---|---|
| 1 | Frontmatter matches the schema for the note type; `review_reason` present when `needs_review` is true | error |
| 2 | Each quote found in the PDF text of its cited page (`pdftotext` per page, cached in `kb/.cache/`; whitespace, hyphenation and ligatures normalised) | `fail` recorded; error if `reviewed` or a claim depends on it |
| 3 | Every `figures` ID exists under `figures/` | error |
| 4 | Every `cites` link resolves to a block ID; every citekey is in `references.bib` | error |
| 5 | No note outside `ref-theses/` cites into `ref-theses/` | error |
| 6 | Status ladder rules from 4.2 | error |
| 7 | Code references: SHA exists in the submodule, file exists at that SHA, lines in range | error |
| 8 | Code drift: file changed between the recorded SHA and the currently pinned commit | warning |
| 9 | Method note without a `code:` entry | error |
| 10 | Phrase echo: a `.tex` chapter shares a run of 8 or more consecutive words with an example thesis | warning |

`kb/review-queue.md` is generated, grouped by `review_reason`, and never hand-edited.

Gitignore additions: `kb/_pdf/`, `kb/.cache/`.

## 6. Build order and acceptance criteria

### Step 1: schema, templates, lint

Update the five templates; add `method` and the example-thesis templates; implement the lint.
Acceptance: a fixture vault passes; one deliberately broken fixture per check in section 5 fails with the expected message; tests live in `tools/kb-lint/tests/`.

### Step 2: ValDX seed

From the ValDX manuscript introduction and the confirmation-of-status introduction: populate `thesis/references.bib` with only the entries those texts cite (deduplicated, keys kept from the 779-entry manuscript bib, not the whole file), create paper stubs, concept notes and ValDX claim notes with `origin`, then run the lint. Ambiguities become `needs_review` with a reason. Literature PDFs the author supplies go in `kb/_pdf/`.
Acceptance: every reference cited in the manuscript introduction has a paper note; every ValDX claim note has an `origin`; the lint is clean apart from flagged review items; `review-queue.md` generated.

### Step 3: introduction hub

`kb/chapters/01-introduction.md` lists claims in argument order, per the existing README rule, with placeholder stubs where a needed claim has no source yet. The gap list drives which papers to read next.
Acceptance: the hub reads as an outline of the introduction; each non-gap entry links to a claim note.

### Step 4 (outline): example-thesis store

Generator for section 4.7 over the three `thesis.json` files, plus phrase-echo lint (check 10). Own spec later.

### Step 5 (outline): methods and JaxENT

Method notes with code links, notation table filled, JaxENT claims promoted from `inbox/` under supervision. Own spec later.

## 7. Out of scope

- A KB-to-LaTeX export or citation helper (the hub order and citekeys are enough for now).
- Hosting the vault anywhere other than the repo, or a second vault.
- Full ingestion of the literature ahead of the introduction outline.

## 8. Assumptions to confirm

- Literature extraction for the introduction follows the ValDX tier (Claude extracts, lint verifies, author reviews flagged notes).
- The author supplies PDFs for papers that are not openly available; papers without one stay `draft`.
- The spec is committed only when the author asks.
