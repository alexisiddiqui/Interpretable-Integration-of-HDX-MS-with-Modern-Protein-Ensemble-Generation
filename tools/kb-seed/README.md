# KB seed

Tools for filling the vault in [`kb/`](../../kb/README.md) from LaTeX sources and the Zotero library, and for checking how far that has got. They build on [kb-lint](../kb-lint/README.md), which remains the single judge of whether a claim is supported.

## Requirements

Python 3.10 or later, Poppler's `pdftotext`, PyYAML (for kb-lint), and a Zotero 7 data directory (default `~/Zotero`). Zotero can stay open: its database is copied before reading.

## Tools

From the repository root:

| Command | What it does |
|---|---|
| `python3 tools/kb-seed/seed.py --tex <files> --source-bib <bibs> --library-bib <export.bib> [--dry-run]` | Resolves every `\cite` key to a Zotero (Better BibTeX) key, then writes `thesis/references.bib`, `thesis/citekey-map.tsv`, paper stubs in `kb/papers/` and PDFs in `kb/_pdf/` |
| `python3 tools/kb-seed/find.py @<citekey> "<regex>"` | Searches a paper's PDF text page by page, to find a verbatim quote and its PDF page index |
| `python3 tools/kb-seed/cite_coverage.py --tex <files>` | Lists citations in the `.tex` files that no claim note accounts for yet |
| `python3 tools/kb-seed/promote.py [--dry-run]` | Sets draft claims to `supported` when the lint confirms their evidence; any the status ladder rejects stay `draft` |

Tests: `python3 -m pytest tools/kb-seed/tests -q`.

## Seeding rules

- **Canonical keys** are Zotero's `citationKey` values. A cited key that is not one is looked up in the `--source-bib` files and matched to Zotero by DOI, then by normalised title.
- **Better BibTeX duplicates** (`key`, `keya`, ...) resolve to the original key, and a `DUPLICATE` line asks you to merge the items in Zotero. Any other ambiguity is `UNRESOLVED`.
- **Nothing is written** unless every key resolves and every canonical key has an entry in `--library-bib`.
- **Existing files are never overwritten.** That covers bib entries, paper notes and PDFs, so re-running only adds what is new.
- **A PDF is copied only if `pdftotext` finds text** (at least 20 words on its first three pages). A damaged or scanned PDF is reported as `UNREADABLE`, and its paper note is flagged for review, like a paper with no PDF.
- **`thesis/citekey-map.tsv`** records `source_key`, `canonical_key`, `matched_by` and `first_cited_in` for every cited key. Use it to re-key manuscript text when adapting it into a chapter.

## Coverage rule

A citation of key K on line L of file F is covered when a claim note has `origin: F#L<L>` and links K's canonical key anywhere in the note: in `cites`, or in the body, for example under "Unverified citations". The manuscripts put one paragraph per line, so coverage is checked per paragraph, not per sentence.
