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
python3 tools/kb-lint/lint.py --write   # also records quote_check results and regenerates kb/review-queue.md and kb/notation.md
python3 -m pytest tools/kb-lint/tests -q
```

Exit codes: 0 with no errors, 1 with errors, 2 when there is no `kb/` folder. Warnings never fail the run.

## Checks

| # | Check | Severity |
|---|---|---|
| 1 | Frontmatter matches the schema for the note type; `review_reason` present when `needs_review` is true; paper notes named `@<citekey>` with `pdf` empty or `kb/_pdf/@<citekey>.pdf`; papers without a PDF flagged and their `quote_check` left `unchecked`; claim blocks complete; quotes of 5 to 25 words | error (unexpected fields: warning) |
| 2 | Each quote appears, as whole words, on its cited PDF page or running onto the next one | error if the block is `reviewed` or cited by a claim, otherwise warning; PDF absent locally: warning |
| 3 | Figure IDs are plain folder names that exist under `figures/` | error |
| 4 | `cites` (claims) and `sources` (concepts, methods) entries resolve to a block in a paper note; citekeys exist in `thesis/references.bib` | error |
| 5 | No claim or concept/method `sources` entry points into `ref-theses/` | error |
| 6 | `supported` / `in-thesis` claims have evidence, are not flagged for review, cite only quotes verified against their PDF in this run (a recorded `pass` is not enough), and outdated sources come with a figure | error |
| 7 | Code references resolve: commit, file and line range exist in the submodule | error; a real submodule that is not checked out: warning |
| 8 | The referenced file changed between the recorded commit and the pinned one | warning |
| 9 | Method notes have at least one code reference | error |
| 10 | A notation symbol has one meaning across concept notes. Symbols are compared without spaces, braces and `\text{}`/`\mathrm{}` wrappers; meanings ignore case and punctuation. The note later in path order is flagged | warning |

Check 11 (phrase echo against the example theses) arrives with the example-thesis store, step 4 of the spec.

## Behaviour

- Notes are every `*.md` under `kb/` except `kb/README.md`, `kb/review-queue.md`, `kb/notation.md`, `_templates/`, `_pdf/` and hidden folders. Notes saved at the vault root are linted too. Notes in `chapters/` and `inbox/` may have no frontmatter type.
- PDF text comes from `pdftotext` without `-layout`, which keeps two-column articles in reading order. It is cached in `kb/.cache/pdftext/` by the PDF's SHA-256. Ligatures, line-break hyphens, curly quotes, dashes, case and spacing are normalised before comparing.
- A code reference is `<submodule path>@<sha>:<file>#L<start>-<end>` (`#L<n>` for one line). Drift is measured against the commit the superproject pins (`git ls-tree HEAD`), or the submodule's checked-out commit when there is no gitlink.
- A claim can only be `supported` on a machine that has the cited PDFs, because the ladder trusts only quotes checked in the current run.
- `kb/review-queue.md` also lists, under "Mis-cited papers in supported claims", every supported or in-thesis claim whose body records a cited paper with "no passage supporting this claim found", so those mis-citations stay visible after the claim is promoted.
- `kb/notation.md` is a table of every concept's `notation:` entries (symbol, meaning, units, defining notes), merged when symbol and meaning agree.
- `--write` touches only `quote_check:` lines in paper notes, `kb/review-queue.md` and `kb/notation.md`, and only when they change.
