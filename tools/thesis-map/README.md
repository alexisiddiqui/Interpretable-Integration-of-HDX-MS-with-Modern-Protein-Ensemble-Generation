# Thesis maps

One local pipeline builds the Crook, Carlos and Vost examples from their PDFs and curated profiles. Every output follows [schema.json](schema.json), version **2.0.0**, and every map uses the same offline HTML interface. Example map directories contain only `thesis.json` and `map.html`.

## Requirements and commands

Use Python 3.10 or later with `jsonschema`, plus Poppler (`pdfinfo`, `pdftotext`, `pdftoppm`). Scanned PDFs also require Tesseract and its English language data. On macOS, Poppler and Tesseract are available through Homebrew; Python dependencies are listed in [requirements.txt](requirements.txt).

From the repository root:

```sh
python3 -m venv tools/thesis-map/.venv
tools/thesis-map/.venv/bin/python -m pip install -r tools/thesis-map/requirements.txt
```

With that environment activated, rebuild an example:

```sh
python tools/thesis-map/cli.py build --profile crook --pdf examples/crook-thesis.pdf --out examples/crook-map
python tools/thesis-map/cli.py build --profile carlos --pdf examples/carlos-thesis.pdf --out examples/carlos-map --jobs 4
python tools/thesis-map/cli.py build --profile vost --pdf examples/vost-thesis.pdf --out examples/vost-map
```

Validate or render an existing version 2 map:

```sh
python tools/thesis-map/cli.py validate examples/carlos-map/thesis.json
python tools/thesis-map/cli.py validate examples/carlos-map/thesis.json --profile carlos --pdf examples/carlos-thesis.pdf
python tools/thesis-map/cli.py render examples/carlos-map/thesis.json --out examples/carlos-map/map.html
```

Commands work from any directory when their arguments point to the right files. A JSON-only validation checks the schema, hierarchy, page mappings and references; it reports that source-text checks were not run. Supplying a PDF and profile performs a validated rebuild and checks that the artifact matches it, including extraction provenance. Rendering requires neither Poppler nor Tesseract.

PDFs remain local inputs in `examples/` and are excluded by the repository's existing `*.pdf` rule. Open any `map.html` directly in a browser; no server, CDN, fonts download or account is required. Page chips identify PDF indices and whether thesis page labels are printed or counted. Carlos's embedded article retains its journal pagination.

## Build behavior

The shared CLI handles PDF extraction, content-addressed caches, schema assembly, validation and output publication. Format adapters receive page text and curated data; they do no file I/O. Their results are internal adapter records, not a supported public JSON format.

Born-digital PDFs use `pdftotext -layout`. Fully scanned PDFs use `pdftoppm` at 220 DPI and Tesseract English OCR. Blank pages in digital PDFs remain blank; partially scanned PDFs with an existing text layer require a format adapter/extraction extension. OCR jobs default to four workers, with one Tesseract thread per worker. `--jobs` changes the worker count.

The default cache is the ignored `tools/thesis-map/.cache/` directory. `--cache <directory>` selects another location. Cache keys include the PDF's SHA-256, extraction settings and tool versions. Each completed OCR page is saved independently, so interrupted OCR resumes. Raw text and rendered page images are never stored in example directories; page images are temporary and removed after OCR.

Builds verify IDs, ancestry, reciprocal child links, depths, section/own-text ranges, pagination, cross-references, source quotations and curated evidence tokens. Source observations remain separate from build failures. A failed build leaves existing outputs intact. Both artifacts are prepared and validated before publication; replacing the two files is not a filesystem transaction, so an interruption between replacements can be repaired by rerunning the build.

Outputs contain no runtime date or absolute workspace paths. Identical PDFs, profiles, extraction versions and template produce identical files. Changing OCR software can change word counts and extracted occurrences; rebuilding refreshes provenance and reruns all checks. The Carlos profile includes visually checked equation-label corrections, and its journal-caption filter distinguishes caption locations from references beginning a line.

## Public schema

All documents contain the same seven top-level keys:

| Key | Content |
| --- | --- |
| `schema_version` | Exactly `2.0.0`; unsupported versions are rejected. |
| `meta` | Thesis identity, local PDF basename, PDF count, profile hash and extraction provenance. |
| `pagemap` | One record per one-based PDF index; thesis labels are strings, with numbering status and alternate publication labels. |
| `journey` | Ordered stages with origin/research/destination roles, explicit evidence spans, contributions, transitions and negative results. |
| `structure` | Ordered roots and an ID-keyed node dictionary; figures and tables are ordinary leaves. |
| `links` | Edges, entities, claims and a relationship-type catalogue with display labels/families. |
| `quality` | Source observations, structured coverage and validation results. |

A node's `pages` cover its full textual section; `own_pages` cover the text before the next heading. Printed page ranges are inclusive, so adjacent sections may share a page. Figures can be owned by the section that first cites them even when their captions appear later. `children` includes structural and figure/table children; `figures` and `tables` list direct leaves, while their counts include descendants.

An object's `source_pages` are cited thesis labels, not PDF indices. Evidence spans carry both labels and PDF indices. `basis` distinguishes stated content from inference; missing summaries, quotes and confidence remain missing/null rather than being fabricated. Source-token checks verify configured terms/numbers on cited pages; they do not establish every scientific interpretation in a claim.

## Adding a thesis

Add `profiles/<name>.json` and `profiles/<name>.py`; no CLI registry change is needed. Profile names use lowercase letters, digits and underscores. JSON curation is data, never executable code. Each configuration supplies `profile_version: 1`, its `name`, `pdf_pages`, thesis `meta`, the explicit `pagemap`, and adapter-specific TOC/annotation/reference rules. Optional `source_checks` contain a record ID, cited string labels, token-alternative lists, and a continuation flag.

The adapter exports `parse(pages, config)`, returning `(records, diagnostics)`. `pages` is a list of PDF-page strings in PDF order. The existing adapters document the internal structural, journey and link records accepted by the shared normalizer. Diagnostics supply `failures`, `unresolved` references and heading `positions` as `{pdf, line}` or `{pdf, offset}`. Keep document-specific parsing and manually checked corrections there; keep filesystem operations, public schema conversion, validation and rendering in the shared modules. Use the existing profiles as examples.

A new profile requires curated scientific annotations and checked page/TOC conventions. This tool does not infer a research narrative automatically. Scientific content was preserved during the v2 migration; hierarchy depths and Vost's parent ranges were corrected, and Vost's start/end markers became valid stages.

## Tests

Python regression tests cover the schema, preserved scientific content/IDs, numbering, hierarchy, source checks, safe embedding, cache behavior and failed publication:

```sh
python -m unittest discover -s tools/thesis-map/tests -v
```

Optional interface tests use development-only Node dependencies; generated maps have no JavaScript dependencies:

```sh
npm ci --prefix tools/thesis-map/tests
npm test --prefix tools/thesis-map/tests
```

`tests/rebuild.py` exercises actual PDF rebuilds and compares both artifacts with the checked-in examples. Its default uses the normal cache; `--cold-cache` creates a temporary empty cache and exercises OCR from scratch.

```sh
python tools/thesis-map/tests/rebuild.py
python tools/thesis-map/tests/rebuild.py --cold-cache --jobs 4
```

For isolated desktop and mobile browser checks (developer dependencies only):

```sh
npx --prefix tools/thesis-map/tests playwright install chromium
npm run test:browser --prefix tools/thesis-map/tests
```
