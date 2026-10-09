# KB lint

Checks the Obsidian vault in [`kb/`](../../kb/README.md) against its schema, its sources and its code. The design is in [the KB spec](../../docs/superpowers/specs/2026-10-08-thesis-kb-design.md), section 5.

## Requirements

Python 3.10 or later with PyYAML, plus Poppler's `pdftotext` and `git`. On macOS: `brew install poppler`.

```sh
python3 -m pip install -r tools/kb-lint/requirements.txt
```

## Commands

From the repository root:

```sh
python3 tools/kb-lint/lint.py           # report only; changes nothing
python3 tools/kb-lint/lint.py --write   # also records quote_check results and regenerates kb/review-queue.md
python3 -m pytest tools/kb-lint/tests -q
```

Exit codes: 0 with no errors, 1 with errors, 2 when there is no `kb/` folder. Warnings never fail the run.

## Checks

| # | Check | Severity |
|---|---|---|
| 1 | Frontmatter matches the schema for the note type; `review_reason` present when `needs_review` is true; paper notes named `@<citekey>`; papers without a PDF flagged; claim blocks complete; quotes of 25 words or fewer | error (unexpected fields: warning) |
| 2 | Each quote appears on its cited PDF page, or runs onto the next one | error if the block is `reviewed` or cited by a claim, otherwise warning; PDF absent locally: warning |
| 3 | Figure IDs exist under `figures/` | error |
| 4 | `cites` entries resolve to a block in a paper note; citekeys exist in `thesis/references.bib` | error |
| 5 | No claim cites a note in `ref-theses/` | error |
| 6 | `supported` / `in-thesis` claims have evidence, are not flagged for review, cite only quotes that passed, and outdated sources come with a figure | error |
| 7 | Code references resolve: commit, file and line range exist in the submodule | error; submodule not checked out: warning |
| 8 | The referenced file changed between the recorded commit and the pinned one | warning |
| 9 | Method notes have at least one code reference | error |

Check 10 (phrase echo against the example theses) arrives with the example-thesis store, step 4 of the spec.

## Behaviour

- Notes are every `*.md` under `kb/` except files directly in `kb/` (`README.md`, `review-queue.md`), `_templates/`, `_pdf/` and hidden folders. Notes in `chapters/` and `inbox/` may have no frontmatter type.
- PDF text comes from `pdftotext` without `-layout`, which keeps two-column articles in reading order. It is cached in `kb/.cache/pdftext/` by the PDF's SHA-256. Ligatures, line-break hyphens, curly quotes, dashes, case and spacing are normalised before comparing.
- A code reference is `<submodule path>@<sha>:<file>#L<start>-<end>` (`#L<n>` for one line). Drift is measured against the commit the superproject pins (`git ls-tree HEAD`), or the submodule's checked-out commit when there is no gitlink.
- `--write` touches only `quote_check:` lines in paper notes and `kb/review-queue.md`, and only when they change.
