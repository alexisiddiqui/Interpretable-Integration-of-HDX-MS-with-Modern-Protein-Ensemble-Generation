# KB seed: introduction literature (step 2) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn the two existing introductions (the ValDX manuscript and the confirmation-of-status report) into checked KB content. Every citation should end up either supported by a quote the lint has found in the cited PDF, or flagged for review with a reason.

**Architecture:** A new tool folder, `tools/kb-seed/`, sits next to `tools/kb-lint/` and reuses its parsing and PDF code. `seed.py` resolves every `\cite` key to a Zotero/Better BibTeX key, then writes `thesis/references.bib`, `thesis/citekey-map.tsv`, paper stubs and PDFs. `find.py`, `cite_coverage.py` and `promote.py` support the content work: finding quotes, proving every citation is accounted for, and promoting claims the lint has verified. The content tasks (7 to 11) follow one written protocol, one source file at a time, each ending with the lint, promotion and a coverage check.

**Tech Stack:** Python 3.10, PyYAML (via kb-lint), sqlite3 (standard library), Poppler `pdftotext`, pytest; Zotero 7 data directory at `~/Zotero`.

**Spec:** `docs/superpowers/specs/2026-10-08-thesis-kb-design.md`. See section 6 "Step 2", amended 2026-10-09 to make Zotero/BBT keys canonical, and section 2, which gives the citekey facts.

## Global Constraints

- Repository root: `Interpretable-Integration-of-HDX-MS-with-Modern-Protein-Ensemble-Generation/`. Run every command from it, on a branch (`git switch -c kb-seed-step2`).
- **Canonical citekeys are Zotero `citationKey` values** (Better BibTeX). ValDX manuscript keys are mapped to them, and the map lives in `thesis/citekey-map.tsv`.
- **Zotero is read-only.** Never write to `~/Zotero`. The tools read a temporary copy of `zotero.sqlite` and copy PDFs *out* of `storage/`.
- **PDFs live only in `kb/_pdf/`**, which is gitignored and never committed.
- **kb-lint stays the single judge of `supported`.** Nothing in this plan sets `status: supported` by hand; only `tools/kb-seed/promote.py` does, and it reverts anything the status ladder rejects.
- **Quotes are verbatim, 5 to 25 words**, copied from `find.py` output. A failing quote is fixed by copying the PDF text more exactly, never by rewording the quote to fit the claim.
- **Trust tier** (spec section 3): introduction literature is Claude-extracted. The author reviews only notes with `needs_review: true`.
- **Introduction sources** (all paths repository-relative):
  - `projects/1-ValDX/manuscript/report/1_introduction_omc.tex`
  - `milestones/2025-11-confirmation-of-status/introduction/{biological_dynamics,measuring_dynamics,ensemble_generators,connect_simulation_experiment,packages,thesis_outline}.tex` (the last two cite nothing)
  - Source bib for ValDX keys: `projects/1-ValDX/manuscript/report/_references.bib`
  - Library bib: `milestones/2025-11-confirmation-of-status/zotero_library.bib`

### Decisions where the spec is silent (made here, flagged for review)

- **Better BibTeX duplicates** (`key` and `keya` for the same DOI) resolve to the unsuffixed key, and the run prints a reminder to merge them in Zotero. Three exist today: Masson 2019, James 2022 and Lee 2021.
- **A Zotero PDF with no extractable text** (fewer than 20 words on pages 1 to 3, i.e. damaged or scanned) is treated as no PDF. Today that is one paper, Hollingsworth 2018, which is a truncated download.
- **kb-lint whole-word matching** treats a digit as a word boundary, so a quote may end at `function` when the PDF reads `function1.` (a glued reference number). Without this, most quotes ending at a cited word fail (found in the pilot).
- **Claim granularity:** one claim note per cited *sentence*. Uncited sentences are the author's own framing and are left to step 3.
- **ValDX results claims** (chapter 3) are **not** in this step. `figures/` has no figure folders yet, so they could never be supported. They come with the ValDX chapter work, due 28 Oct.
- **Coverage is checked per paragraph.** Both sources put one paragraph per line, so a citation is "covered" by any claim from that line that links the key.

## Review Focus

- A citation whose key is in neither Zotero nor any source bib. Expected: `UNRESOLVED`, and nothing written. Tested in Task 4.
- A re-run after notes have been edited by hand. Expected: no note, PDF or bib entry is overwritten. Tested in Task 4.
- Zotero open while seeding (database locked). Expected: works, because it reads a copy. Tested in Task 3.
- A claim made in both introductions. Expected: one note with `origin` for the first location and `Also stated in:` for the second, and coverage counts both. Tested in Task 5.
- A content task that invents a quote. Expected: kb-lint check 2 fails it, the ladder keeps the claim `draft`, and coverage still counts the citation, so the claim stays visible. Protocol step 5, with mechanics tested in kb-lint.

## File Structure

| File | Responsibility |
|---|---|
| `tools/kb-lint/quotes.py` (modify) | `contains_words`: digits count as a word boundary |
| `tools/kb-seed/bibtex.py` | `find_citations`, `parse_bib`, `normalise_doi`, `normalise_title`, `plain_title` |
| `tools/kb-seed/zotero.py` | `ZoteroLibrary(home)`: keys, DOI/title index, PDFs; `.match(doi, title)`; `duplicate_base` |
| `tools/kb-seed/seed.py` | `resolve`, `plan_seed`, `readable`, `paper_stub`, `apply_seed`, CLI |
| `tools/kb-seed/find.py` | `search(pdf, pattern, cache_dir, context)`, CLI |
| `tools/kb-seed/cite_coverage.py` | `missing(root, tex_rel)`, CLI |
| `tools/kb-seed/promote.py` | `candidates(root)`, `promote(root, dry_run)`, CLI |
| `tools/kb-seed/tests/` | `conftest.py`, `seed_helpers.py` (Zotero DB and repo fixtures), one test file per module |
| `tools/kb-seed/README.md` | Usage and rules |
| `thesis/references.bib`, `thesis/citekey-map.tsv` | Generated in Task 6, then committed |
| `kb/papers/`, `kb/claims/`, `kb/concepts/`, `kb/review-queue.md` | Content (Tasks 6 to 12) |

---

### Task 1: kb-lint treats glued reference numbers as word boundaries

**Files:**
- Modify: `tools/kb-lint/quotes.py` (function `contains_words`)
- Test: `tools/kb-lint/tests/test_quotes.py` (append one test)

**Interfaces:**
- Consumes: nothing new.
- Produces: `contains_words(text, quote) -> bool`, with the same signature as before.

- [ ] **Step 1: Write the failing test.** Append to `tools/kb-lint/tests/test_quotes.py`:

```python


def test_quote_may_end_at_a_reference_number_glued_to_the_word():
    from quotes import contains_words
    page = normalise("a link between structure, conformational dynamics and function1. HDX-MS measures")
    assert contains_words(page, normalise("conformational dynamics and function"))
    assert not contains_words(page, normalise("conformational dynamics and funct"))
```

- [ ] **Step 2: Run it to verify it fails**

Run: `python3 -m pytest tools/kb-lint/tests/test_quotes.py -q`
Expected: `1 failed, 10 passed`.

- [ ] **Step 3: Replace `contains_words` in `tools/kb-lint/quotes.py`** with:

```python
def contains_words(text, quote):
    """True if quote occurs in text without starting or ending inside a word.

    Only letters count as "inside a word": PDFs glue reference numbers to the preceding word
    ("function1."), and a quote ending at "function" must still match.
    """
    return re.search(r"(?<![^\W\d_])" + re.escape(quote) + r"(?![^\W\d_])", text) is not None
```

- [ ] **Step 4: Run the kb-lint suite**

Run: `python3 -m pytest tools/kb-lint/tests -q`
Expected: `97 passed`.

- [ ] **Step 5: Commit**

```bash
git add tools/kb-lint/quotes.py tools/kb-lint/tests/test_quotes.py
git commit -m "kb-lint: reference numbers glued to a word are a word boundary"
```

---

### Task 2: BibTeX and citation parsing, with test fixtures

**Files:**
- Create: `tools/kb-seed/bibtex.py`
- Create: `tools/kb-seed/tests/conftest.py`
- Create: `tools/kb-seed/tests/seed_helpers.py`
- Test: `tools/kb-seed/tests/test_bibtex.py`

**Interfaces:**
- Consumes: `make_pdf` from `tools/kb-lint/tests/helpers.py`, imported by `seed_helpers`.
- Produces:
  - `Citation(key, path, line)` and `BibEntry(key, text, doi, title, year)`.
  - `find_citations(path, label=None) -> list[Citation]`, `parse_bib(path) -> dict[str, BibEntry]`.
  - `normalise_doi(str|None) -> str|None`, `normalise_title(str|None) -> str`, `plain_title(str|None) -> str`.
  - Fixtures `zotero_home`, `seed_repo`; helpers `make_zotero(home, items=ITEMS, deleted=DELETED)`, `make_repo(root, templates)`, `make_pdf`, plus the constants `TEX`, `SOURCE_BIBS`, `LIBRARY`, `VALDX_TEX`, `CONF_TEX`, `LIBRARY_BIB`.

- [ ] **Step 1: Write the fixtures and the failing test**

`tools/kb-seed/tests/seed_helpers.py`:

```python
"""Fixtures for kb-seed: a minimal Zotero 7 database and a small repository with LaTeX and .bib files."""

from pathlib import Path
import shutil
import sqlite3
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "kb-lint" / "tests"))
from helpers import make_pdf  # noqa: E402  (kb-lint's minimal text PDF)

SCHEMA = """
CREATE TABLE items (itemID INTEGER PRIMARY KEY, key TEXT);
CREATE TABLE fields (fieldID INTEGER PRIMARY KEY, fieldName TEXT);
CREATE TABLE itemDataValues (valueID INTEGER PRIMARY KEY, value TEXT);
CREATE TABLE itemData (itemID INTEGER, fieldID INTEGER, valueID INTEGER);
CREATE TABLE itemAttachments (itemID INTEGER PRIMARY KEY, parentItemID INTEGER, contentType TEXT, path TEXT);
CREATE TABLE deletedItems (itemID INTEGER PRIMARY KEY);
"""

# itemID: (citationKey, DOI, title, PDF file name or None)
ITEMS = {
    1: ("andersonHDXMSMDSimulations2022", "10.1000/anderson", "HDX-MS and MD Simulations", "anderson.pdf"),
    2: ("massonOverviewHydrogenDeuterium2017", "10.1000/masson", "An Overview of Hydrogen–Deuterium Exchange", "masson.pdf"),
    3: ("bradshawInterpretationHDX2020", None, "Interpretation of {HDX} Data", None),
    4: ("trashedPaper2019", "10.1000/trashed", "A Trashed Paper", "trashed.pdf"),
    5: ("duplicateTitleA2021", None, "Same Title", None),
    6: ("duplicateTitleB2021", None, "Same Title", None),
}
DELETED = {4}

LIBRARY_BIB = """@article{andersonHDXMSMDSimulations2022,
  title = {{HDX-MS} and {MD} Simulations},
  doi = {10.1000/anderson},
  date = {2022-03-01},
}

@article{massonOverviewHydrogenDeuterium2017,
  title = {An Overview of Hydrogen--Deuterium Exchange},
  year = {2017},
  doi = {10.1000/MASSON},
}

@article{bradshawInterpretationHDX2020,
  title = {Interpretation of {HDX} Data},
  year = 2020,
}

@comment{jabref-meta: ignored}
"""

SOURCE_BIB = """@article{anderson_hdx-ms_2022,
  title = {{HDX}-{MS} and {MD} simulations},
  doi = {https://doi.org/10.1000/Anderson},
  year = {2022},
}
@article{bradshaw_interpretation_2020,
  title = "Interpretation of {HDX} data",
  year = {2020},
}
@article{same_title_2021,
  title = {Same Title},
}
@article{unknown_paper_2001,
  title = {Nothing Like This In Zotero},
}
"""

VALDX_TEX = """\\section{Introduction}
HDX-MS measures dynamics.\\cite{anderson_hdx-ms_2022,masson_overview_2017}
% Old text \\cite{unknown_paper_2001}
Simulations help.\\citep[see][p.~3]{bradshaw_interpretation_2020}
"""

CONF_TEX = """Ensembles matter \\cite{
  andersonHDXMSMDSimulations2022,
  massonOverviewHydrogenDeuterium2017}.
"""


def make_zotero(home, items=ITEMS, deleted=DELETED):
    """Create a Zotero data directory with the tables and PDFs kb-seed reads."""
    home.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(home / "zotero.sqlite")
    db.executescript(SCHEMA)
    db.executemany("INSERT INTO fields VALUES (?, ?)", [(1, "title"), (58, "DOI"), (92, "citationKey")])
    value_id = 0
    for item_id, (key, doi, title, pdf) in items.items():
        db.execute("INSERT INTO items VALUES (?, ?)", (item_id, f"ITEM{item_id:04d}"))
        for field_id, value in ((92, key), (58, doi), (1, title)):
            if value is None:
                continue
            value_id += 1
            db.execute("INSERT INTO itemDataValues VALUES (?, ?)", (value_id, value))
            db.execute("INSERT INTO itemData VALUES (?, ?, ?)", (item_id, field_id, value_id))
        if pdf:
            attachment = 100 + item_id
            folder = f"ATT{attachment:05d}"
            db.execute("INSERT INTO items VALUES (?, ?)", (attachment, folder))
            db.execute("INSERT INTO itemAttachments VALUES (?, ?, ?, ?)",
                       (attachment, item_id, "application/pdf", f"storage:{pdf}"))
            (home / "storage" / folder).mkdir(parents=True)
            text = f"{title}. This stored article has enough words on its first page to count as readable text. " * 2
            ascii_text = text.encode("ascii", "replace").decode()  # the minimal PDF uses a Latin-1 font
            (home / "storage" / folder / pdf).write_bytes(make_pdf([ascii_text]))
    db.executemany("INSERT INTO deletedItems VALUES (?)", [(i,) for i in deleted])
    db.commit()
    db.close()
    return home


def make_repo(root, kb_lint_templates):
    """A repository with two introductions, a source bib, a library bib and the real paper template."""
    files = {
        "projects/1-ValDX/manuscript/report/1_introduction_omc.tex": VALDX_TEX,
        "projects/1-ValDX/manuscript/report/_references.bib": SOURCE_BIB,
        "milestones/conf/introduction/ensembles.tex": CONF_TEX,
        "milestones/conf/zotero_library.bib": LIBRARY_BIB,
    }
    for rel, text in files.items():
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    shutil.copytree(kb_lint_templates, root / "kb" / "_templates")
    return root


TEX = ["projects/1-ValDX/manuscript/report/1_introduction_omc.tex", "milestones/conf/introduction/ensembles.tex"]
SOURCE_BIBS = ["projects/1-ValDX/manuscript/report/_references.bib"]
LIBRARY = "milestones/conf/zotero_library.bib"
```

`tools/kb-seed/tests/conftest.py`:

```python
from pathlib import Path
import sys

import pytest

TOOLS = Path(__file__).resolve().parents[2]
REPO = TOOLS.parent
sys.path.insert(0, str(TOOLS / "kb-seed"))
sys.path.insert(0, str(Path(__file__).resolve().parent))  # seed_helpers

from seed_helpers import make_repo, make_zotero  # noqa: E402


@pytest.fixture
def zotero_home(tmp_path):
    return make_zotero(tmp_path / "Zotero")


@pytest.fixture
def seed_repo(tmp_path):
    """Repository with the two introductions and bibs, using the real kb/_templates/."""
    return make_repo(tmp_path / "repo", REPO / "kb" / "_templates")
```

`tools/kb-seed/tests/test_bibtex.py`:

```python
from bibtex import find_citations, normalise_doi, normalise_title, parse_bib, plain_title
from seed_helpers import CONF_TEX, LIBRARY_BIB, VALDX_TEX


def test_citations_skip_comments_and_keep_lines(tmp_path):
    tex = tmp_path / "intro.tex"
    tex.write_text(VALDX_TEX, encoding="utf-8")
    found = [(c.key, c.line) for c in find_citations(tex, label="intro.tex")]
    assert found == [
        ("anderson_hdx-ms_2022", 2),
        ("masson_overview_2017", 2),
        ("bradshaw_interpretation_2020", 4),
    ]


def test_citation_spanning_lines(tmp_path):
    tex = tmp_path / "conf.tex"
    tex.write_text(CONF_TEX, encoding="utf-8")
    assert [(c.key, c.line) for c in find_citations(tex)] == [
        ("andersonHDXMSMDSimulations2022", 1),
        ("massonOverviewHydrogenDeuterium2017", 1),
    ]


def test_escaped_percent_is_not_a_comment(tmp_path):
    tex = tmp_path / "pct.tex"
    tex.write_text("Up 50\\% \\cite{a} % \\cite{b}\n", encoding="utf-8")
    assert [c.key for c in find_citations(tex)] == ["a"]


def test_parse_bib_fields_and_verbatim_text(tmp_path):
    bib = tmp_path / "lib.bib"
    bib.write_text(LIBRARY_BIB, encoding="utf-8")
    entries = parse_bib(bib)
    assert set(entries) == {"andersonHDXMSMDSimulations2022", "massonOverviewHydrogenDeuterium2017", "bradshawInterpretationHDX2020"}
    anderson = entries["andersonHDXMSMDSimulations2022"]
    assert (anderson.doi, anderson.year) == ("10.1000/anderson", 2022)
    assert anderson.text.startswith("@article{andersonHDXMSMDSimulations2022,") and anderson.text.endswith("}")
    assert entries["massonOverviewHydrogenDeuterium2017"].doi == "10.1000/masson"
    assert entries["bradshawInterpretationHDX2020"].year == 2020


def test_normalisers():
    assert normalise_doi("https://doi.org/10.1000/ABC ") == "10.1000/abc"
    assert normalise_doi("doi:10.1/x") == "10.1/x"
    assert normalise_title("{HDX}-{MS} and {MD} simulations") == normalise_title("HDX-MS and MD Simulations")
    assert normalise_title("Hydrogen--Deuterium") == normalise_title("Hydrogen–Deuterium")
    assert normalise_title("Caf\\'{e} r\u00e9sum\u00e9") == "caf e resume"
    assert plain_title("{HDX-MS} and {MD} Simulations") == "HDX-MS and MD Simulations"
```

- [ ] **Step 2: Run it to verify it fails**

Run: `python3 -m pytest tools/kb-seed/tests/test_bibtex.py -q`
Expected: collection error, `ModuleNotFoundError: No module named 'bibtex'`.

- [ ] **Step 3: Write `tools/kb-seed/bibtex.py`**

```python
"""Find \\cite keys in LaTeX and parse BibTeX entries (key, verbatim text, DOI, title, year)."""

from dataclasses import dataclass
from pathlib import Path
import re
import unicodedata

CITE = re.compile(r"\\[A-Za-z]*cite[A-Za-z]*\*?(?:\[[^\]]*\]){0,2}\{([^}]*)\}")
COMMENT = re.compile(r"(?<!\\)%.*")
ENTRY_START = re.compile(r"@(\w+)\s*\{\s*([^,\s]+)\s*,")
SKIP_TYPES = {"comment", "string", "preamble"}


@dataclass
class Citation:
    key: str
    path: str   # as given, repository-relative
    line: int   # 1-based line of the \cite command


@dataclass
class BibEntry:
    key: str
    text: str   # the entry verbatim, from @ to its closing brace
    doi: str | None
    title: str | None
    year: int | None


def find_citations(path, label=None):
    """Every cited key in a .tex file, in order, ignoring commented-out text."""
    lines = Path(path).read_text(encoding="utf-8", errors="replace").split("\n")
    text = "\n".join(COMMENT.sub("", line) for line in lines)
    found = []
    for m in CITE.finditer(text):
        line = text.count("\n", 0, m.start()) + 1
        for key in m.group(1).split(","):
            if key.strip():
                found.append(Citation(key.strip(), label or str(path), line))
    return found


def parse_bib(path):
    """Map citekey -> BibEntry for every real entry in a .bib file."""
    text = Path(path).read_text(encoding="utf-8", errors="replace")
    entries = {}
    pos = 0
    while (m := ENTRY_START.search(text, pos)):
        end = _closing_brace(text, text.index("{", m.start()))
        pos = end + 1
        if m.group(1).lower() in SKIP_TYPES or end < 0:
            continue
        body = text[m.start():end + 1]
        year = _field(body, "year") or (_field(body, "date") or "")[:4]
        entries[m.group(2)] = BibEntry(
            key=m.group(2),
            text=body,
            doi=normalise_doi(_field(body, "doi")),
            title=_field(body, "title"),
            year=int(year) if year and year.isdigit() else None,
        )
    return entries


def normalise_doi(doi):
    if not doi:
        return None
    doi = doi.strip().lower()
    doi = re.sub(r"^(https?://(dx\.)?doi\.org/|doi:)", "", doi)
    return doi or None


def normalise_title(title):
    """Lower-case words only: drops braces, LaTeX accents, punctuation and diacritics."""
    if not title:
        return ""
    title = unicodedata.normalize("NFKD", title)
    title = "".join(c for c in title if not unicodedata.combining(c))
    title = re.sub(r"\\[A-Za-z]+|\\.", " ", title)
    return " ".join(re.sub(r"[^\w\s]|_", " ", title.lower()).split())


def plain_title(title):
    return " ".join(re.sub(r"[{}]", "", title or "").split())


def _closing_brace(text, start):
    depth = 0
    for i in range(start, len(text)):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return i
    return -1


def _field(body, name):
    m = re.search(r"(?:^|[,\s])" + name + r"\s*=\s*", body, re.I)
    if not m:
        return None
    i = m.end()
    if i < len(body) and body[i] == "{":
        end = _closing_brace(body, i)
        return body[i + 1:end].strip() if end > 0 else None
    if i < len(body) and body[i] == '"':
        end = body.find('"', i + 1)
        return body[i + 1:end].strip() if end > 0 else None
    bare = re.match(r"[^,\n}]+", body[i:])
    return bare.group(0).strip() if bare else None
```

- [ ] **Step 4: Run it to verify it passes**

Run: `python3 -m pytest tools/kb-seed/tests/test_bibtex.py -q`
Expected: `5 passed`.

- [ ] **Step 5: Commit**

```bash
git add tools/kb-seed/bibtex.py tools/kb-seed/tests/conftest.py tools/kb-seed/tests/seed_helpers.py tools/kb-seed/tests/test_bibtex.py
git commit -m "kb-seed: citation and BibTeX parsing"
```

---

### Task 3: Zotero library reader

**Files:**
- Create: `tools/kb-seed/zotero.py`
- Test: `tools/kb-seed/tests/test_zotero.py`

**Interfaces:**
- Consumes: `normalise_doi`, `normalise_title` (Task 2); fixtures `zotero_home`, `make_zotero`.
- Produces: `ZoteroLibrary(home)` with `.keys: set[str]`, `.pdf_by_key: dict[str, Path]`, `.key_by_doi` and `.key_by_title` (each a `dict[str, set[str]]`), and `.match(doi, title) -> (key|None, how_or_reason: str)`; also `duplicate_base(keys) -> str|None`.

- [ ] **Step 1: Write the failing test**

`tools/kb-seed/tests/test_zotero.py`:

```python
import sqlite3

from seed_helpers import make_zotero
from zotero import ZoteroLibrary


def test_keys_exclude_trashed_items(zotero_home):
    library = ZoteroLibrary(zotero_home)
    assert "andersonHDXMSMDSimulations2022" in library.keys
    assert "trashedPaper2019" not in library.keys


def test_pdfs_found_in_storage(zotero_home):
    library = ZoteroLibrary(zotero_home)
    pdf = library.pdf_by_key["andersonHDXMSMDSimulations2022"]
    assert pdf == zotero_home / "storage" / "ATT00101" / "anderson.pdf"
    assert "bradshawInterpretationHDX2020" not in library.pdf_by_key
    assert "trashedPaper2019" not in library.pdf_by_key


def test_pdf_missing_on_disk_is_ignored(zotero_home):
    (zotero_home / "storage" / "ATT00102" / "masson.pdf").unlink()
    assert "massonOverviewHydrogenDeuterium2017" not in ZoteroLibrary(zotero_home).pdf_by_key


def test_match_by_doi_then_title(zotero_home):
    library = ZoteroLibrary(zotero_home)
    assert library.match("https://doi.org/10.1000/ANDERSON", None) == ("andersonHDXMSMDSimulations2022", "doi")
    assert library.match(None, "Interpretation of HDX data") == ("bradshawInterpretationHDX2020", "title")
    assert library.match("10.9/none", "nothing at all") == (None, "no Zotero item with this DOI or title")


def test_unrelated_keys_sharing_a_title_are_ambiguous(zotero_home):
    assert ZoteroLibrary(zotero_home).match(None, "Same Title") == (
        None, "title same title matches several Zotero items: duplicateTitleA2021, duplicateTitleB2021")


def test_better_bibtex_duplicate_resolves_to_the_original_key(tmp_path):
    items = {
        1: ("massonRecommendations2019", "10.1/masson", "Recommendations", "a.pdf"),
        2: ("massonRecommendations2019a", "10.1/MASSON", "Recommendations", "b.pdf"),
    }
    library = ZoteroLibrary(make_zotero(tmp_path / "Z", items=items, deleted=set()))
    assert library.match("10.1/masson", None) == ("massonRecommendations2019", "doi; Zotero duplicates massonRecommendations2019a")


def test_reads_a_copy_while_the_live_database_is_locked(zotero_home):
    lock = sqlite3.connect(zotero_home / "zotero.sqlite")
    lock.execute("BEGIN EXCLUSIVE")
    try:
        assert "andersonHDXMSMDSimulations2022" in ZoteroLibrary(zotero_home).keys
    finally:
        lock.rollback()
        lock.close()
```

- [ ] **Step 2: Run it to verify it fails**

Run: `python3 -m pytest tools/kb-seed/tests/test_zotero.py -q`
Expected: collection error, `ModuleNotFoundError: No module named 'zotero'`.

- [ ] **Step 3: Write `tools/kb-seed/zotero.py`**

```python
"""Read-only view of a local Zotero 7 library: citation keys, DOIs, titles and stored PDFs."""

from pathlib import Path
import re
import shutil
import sqlite3
import tempfile

from bibtex import normalise_doi, normalise_title


class ZoteroLibrary:
    def __init__(self, home):
        self.home = Path(home)
        with tempfile.TemporaryDirectory() as tmp:
            # Work on a copy: a running Zotero holds a lock on the live database.
            copy = Path(tmp) / "zotero.sqlite"
            shutil.copyfile(self.home / "zotero.sqlite", copy)
            db = sqlite3.connect(copy)
            try:
                self._load(db)
            finally:
                db.close()

    def _load(self, db):
        deleted = {row[0] for row in db.execute("SELECT itemID FROM deletedItems")}

        def field(name):
            rows = db.execute(
                "SELECT d.itemID, v.value FROM itemData d JOIN itemDataValues v USING (valueID) "
                "JOIN fields f USING (fieldID) WHERE f.fieldName = ?", (name,))
            return {item: value for item, value in rows if item not in deleted}

        keys = field("citationKey")
        self.keys = set(keys.values())
        self.key_by_doi = _index(keys, field("DOI"), normalise_doi)
        self.key_by_title = _index(keys, field("title"), normalise_title)
        self.pdf_by_key = {}
        rows = db.execute(
            "SELECT a.itemID, a.parentItemID, i.key, a.path FROM itemAttachments a "
            "JOIN items i ON i.itemID = a.itemID "
            "WHERE a.contentType = 'application/pdf' AND a.path LIKE 'storage:%' ORDER BY a.itemID")
        for attachment, parent, folder, path in rows:
            if parent in keys and attachment not in deleted:
                pdf = self.home / "storage" / folder / path[len("storage:"):]
                if pdf.is_file():
                    self.pdf_by_key.setdefault(keys[parent], pdf)

    def match(self, doi, title):
        """(citekey, how) for a DOI or title, or (None, reason) when nothing matches unambiguously."""
        for how, index, value in (("doi", self.key_by_doi, normalise_doi(doi)),
                                  ("title", self.key_by_title, normalise_title(title))):
            keys = index.get(value) if value else None
            if not keys:
                continue
            if len(keys) == 1:
                return next(iter(keys)), how
            base = duplicate_base(keys)
            if base:
                others = ", ".join(sorted(keys - {base}))
                return base, f"{how}; Zotero duplicates {others}"
            return None, f"{how} {value} matches several Zotero items: {', '.join(sorted(keys))}"
        return None, "no Zotero item with this DOI or title"


def duplicate_base(keys):
    """The original key when the others are Better BibTeX's duplicate suffixes (key, keya, keyb, ...)."""
    shortest = min(keys, key=len)
    if all(k == shortest or re.fullmatch(re.escape(shortest) + "[a-z]", k) for k in keys):
        return shortest
    return None


def _index(keys, values, normalise):
    """Normalised value -> set of citekeys carrying it."""
    index = {}
    for item, value in values.items():
        norm = normalise(value) if item in keys else None
        if norm:
            index.setdefault(norm, set()).add(keys[item])
    return index
```

- [ ] **Step 4: Run it to verify it passes**

Run: `python3 -m pytest tools/kb-seed/tests/test_zotero.py -q`
Expected: `7 passed`.

- [ ] **Step 5: Commit**

```bash
git add tools/kb-seed/zotero.py tools/kb-seed/tests/test_zotero.py
git commit -m "kb-seed: read-only Zotero library reader"
```

---

### Task 4: Seeder

**Files:**
- Create: `tools/kb-seed/seed.py`
- Test: `tools/kb-seed/tests/test_seed.py`

**Interfaces:**
- Consumes: Tasks 2 and 3; `kb/_templates/paper.md` (the real template, read at run time); `lint.run` (in the test only).
- Produces:
  - `Plan` with `.mapping`, `.unresolved`, `.missing_entries`, `.new_entries`, `.new_stubs`, `.new_pdfs`, `.no_pdf`, `.unreadable`, `.canonical` and `.ok`.
  - `plan_seed(root, tex_paths, source_bib_paths, library_bib_path, library) -> (Plan, library_bib, existing)`.
  - `readable(pdf) -> bool`, `paper_stub(...)`, `apply_seed(...)`, and `main(argv) -> int` (0 when written or on a dry run; 1 when unresolved or missing).

- [ ] **Step 1: Write the failing test**

`tools/kb-seed/tests/test_seed.py`:

```python
import sys

import pytest

from seed import main, plan_seed
from seed_helpers import LIBRARY, SOURCE_BIBS, TEX
from zotero import ZoteroLibrary

TOOLS = __import__("pathlib").Path(__file__).resolve().parents[2]


def args(repo, zotero_home, *extra, tex=TEX):
    return ["--root", str(repo), "--zotero", str(zotero_home), "--tex", *tex,
            "--source-bib", *SOURCE_BIBS, "--library-bib", LIBRARY, *extra]


def test_plan_resolves_and_reports_unresolved(seed_repo, zotero_home):
    library = ZoteroLibrary(zotero_home)
    plan, _, _ = plan_seed(seed_repo, TEX, SOURCE_BIBS, LIBRARY, library)
    assert plan.mapping["anderson_hdx-ms_2022"][:2] == ("andersonHDXMSMDSimulations2022", "doi")
    assert plan.mapping["bradshaw_interpretation_2020"][:2] == ("bradshawInterpretationHDX2020", "title")
    assert plan.mapping["andersonHDXMSMDSimulations2022"][:2] == ("andersonHDXMSMDSimulations2022", "key")
    assert [k for k, _ in plan.unresolved] == ["masson_overview_2017"]  # not in the source bib
    assert not plan.ok


def test_unresolved_key_writes_nothing(seed_repo, zotero_home, capsys):
    assert main(args(seed_repo, zotero_home)) == 1
    out = capsys.readouterr().out
    assert "UNRESOLVED masson_overview_2017: not a Zotero key and not in any source bib" in out
    assert "Nothing written." in out
    assert not (seed_repo / "thesis").exists()
    assert not (seed_repo / "kb" / "papers").exists()


@pytest.fixture
def resolvable(seed_repo):
    bib = seed_repo / SOURCE_BIBS[0]
    bib.write_text(bib.read_text() + "@article{masson_overview_2017,\n  doi = {10.1000/masson},\n}\n")
    return seed_repo


def test_seed_writes_bib_map_stubs_and_pdfs(resolvable, zotero_home, capsys):
    assert main(args(resolvable, zotero_home)) == 0
    out = capsys.readouterr().out
    assert "5 cited keys -> 3 papers (3 remapped to Zotero keys)" in out
    assert "NO PDF bradshawInterpretationHDX2020" in out

    bib = (resolvable / "thesis/references.bib").read_text()
    assert bib.index("@article{andersonHDXMSMDSimulations2022,") < bib.index("@article{bradshawInterpretationHDX2020,")
    assert "@comment" not in bib

    rows = (resolvable / "thesis/citekey-map.tsv").read_text().splitlines()
    assert rows[0] == "source_key\tcanonical_key\tmatched_by\tfirst_cited_in"
    assert f"anderson_hdx-ms_2022\tandersonHDXMSMDSimulations2022\tdoi\t{TEX[0]}:2" in rows

    pdf = resolvable / "kb/_pdf/@andersonHDXMSMDSimulations2022.pdf"
    assert pdf.read_bytes() == (zotero_home / "storage/ATT00101/anderson.pdf").read_bytes()

    with_pdf = (resolvable / "kb/papers/@andersonHDXMSMDSimulations2022.md").read_text()
    assert with_pdf.startswith("---\ntype: paper\ncitekey: andersonHDXMSMDSimulations2022\nyear: 2022\n")
    assert "pdf: kb/_pdf/@andersonHDXMSMDSimulations2022.pdf\nextraction: auto\nneeds_review: false\n" in with_pdf
    assert "# HDX-MS and MD Simulations (2022)" in with_pdf
    assert "## Claims" in with_pdf  # body comes from the real template

    no_pdf = (resolvable / "kb/papers/@bradshawInterpretationHDX2020.md").read_text()
    assert 'pdf:\nextraction: none\nneeds_review: true\nreview_reason: "No PDF in Zotero; add kb/_pdf/@<citekey>.pdf' in no_pdf


def test_seed_output_passes_the_lint(resolvable, zotero_home):
    assert main(args(resolvable, zotero_home)) == 0
    sys.path.insert(0, str(TOOLS / "kb-lint"))
    from lint import run
    issues = [str(i) for i in run(resolvable).issues]
    assert issues == []


def test_rerun_overwrites_nothing(resolvable, zotero_home, capsys):
    assert main(args(resolvable, zotero_home)) == 0
    note = resolvable / "kb/papers/@andersonHDXMSMDSimulations2022.md"
    note.write_text(note.read_text() + "\nMy notes.\n")
    pdf = resolvable / "kb/_pdf/@andersonHDXMSMDSimulations2022.pdf"
    pdf.write_bytes(b"%PDF-1.4 my own copy")
    capsys.readouterr()
    assert main(args(resolvable, zotero_home)) == 0
    assert "0 new bib entries, 0 new paper notes, 0 PDFs to copy" in capsys.readouterr().out
    assert note.read_text().endswith("\nMy notes.\n")
    assert pdf.read_bytes() == b"%PDF-1.4 my own copy"


def test_existing_bib_entries_are_kept(resolvable, zotero_home):
    bib = resolvable / "thesis/references.bib"
    bib.parent.mkdir(parents=True)
    bib.write_text("@book{zzzMine2000,\n  title = {Kept},\n}\n")
    assert main(args(resolvable, zotero_home)) == 0
    text = bib.read_text()
    assert "@book{zzzMine2000," in text and text.index("andersonHDXMS") < text.index("zzzMine2000")


def test_missing_library_entry_writes_nothing(resolvable, zotero_home, capsys):
    lib = resolvable / LIBRARY
    lib.write_text(lib.read_text().replace("@article{bradshawInterpretationHDX2020,", "@article{renamedElsewhere2020,"))
    assert main(args(resolvable, zotero_home)) == 1
    assert "MISSING bradshawInterpretationHDX2020" in capsys.readouterr().out
    assert not (resolvable / "thesis").exists()


def test_unreadable_zotero_pdf_is_not_copied(resolvable, zotero_home, capsys):
    (zotero_home / "storage/ATT00101/anderson.pdf").write_bytes(b"%PDF-1.5 truncated download")
    assert main(args(resolvable, zotero_home)) == 0
    assert "UNREADABLE andersonHDXMSMDSimulations2022" in capsys.readouterr().out
    assert not (resolvable / "kb/_pdf/@andersonHDXMSMDSimulations2022.pdf").exists()
    note = (resolvable / "kb/papers/@andersonHDXMSMDSimulations2022.md").read_text()
    assert 'extraction: none\nneeds_review: true\nreview_reason: "PDF in Zotero has no readable text' in note


def test_dry_run_writes_nothing(resolvable, zotero_home, capsys):
    assert main(args(resolvable, zotero_home, "--dry-run")) == 0
    assert "Dry run: nothing written." in capsys.readouterr().out
    assert not (resolvable / "thesis").exists()
    assert not (resolvable / "kb/_pdf").exists()
```

- [ ] **Step 2: Run it to verify it fails**

Run: `python3 -m pytest tools/kb-seed/tests/test_seed.py -q`
Expected: collection error, `ModuleNotFoundError: No module named 'seed'`.

- [ ] **Step 3: Write `tools/kb-seed/seed.py`**

```python
#!/usr/bin/env python3
"""Seed thesis/references.bib, thesis/citekey-map.tsv, kb/papers/ stubs and kb/_pdf/ from LaTeX and Zotero.

Zotero (Better BibTeX) citekeys are canonical. A cited key that is not a Zotero key is matched through
its entry in a source .bib, by DOI and then by title. Nothing is written unless every key resolves and
every canonical key has an entry in the library .bib. Existing notes, PDFs and bib entries are never
overwritten. See README.md.
"""

import argparse
from dataclasses import dataclass, field
from pathlib import Path
import shutil
import subprocess
import sys

from bibtex import find_citations, parse_bib, plain_title
from zotero import ZoteroLibrary

REPO = Path(__file__).resolve().parents[2]
MAP_HEADER = "source_key\tcanonical_key\tmatched_by\tfirst_cited_in\n"
# Reasons name no citekey, so kb/review-queue.md groups these papers under one heading each.
NO_PDF_REASON = "No PDF in Zotero; add kb/_pdf/@<citekey>.pdf, then set pdf and extraction: auto"
UNREADABLE_REASON = ("PDF in Zotero has no readable text (damaged or scanned); add a text PDF as "
                     "kb/_pdf/@<citekey>.pdf, then set pdf and extraction: auto")
MIN_WORDS = 20  # on the first three pages; a scanned or damaged PDF yields none


@dataclass
class Plan:
    mapping: dict = field(default_factory=dict)      # source key -> (canonical key, how, first citation)
    unresolved: list = field(default_factory=list)   # (source key, reason)
    missing_entries: list = field(default_factory=list)  # canonical keys absent from the library .bib
    new_entries: list = field(default_factory=list)
    new_stubs: list = field(default_factory=list)
    new_pdfs: list = field(default_factory=list)
    no_pdf: list = field(default_factory=list)
    unreadable: list = field(default_factory=list)  # Zotero has a PDF but pdftotext finds no text

    @property
    def canonical(self):
        return sorted({canonical for canonical, _, _ in self.mapping.values()})

    @property
    def ok(self):
        return not self.unresolved and not self.missing_entries


def resolve(citations, source_bibs, library):
    """Map each cited key to a canonical Zotero key. Returns (mapping, unresolved)."""
    mapping, unresolved = {}, []
    for citation in citations:
        key = citation.key
        if key in mapping or any(key == k for k, _ in unresolved):
            continue
        where = f"{citation.path}:{citation.line}"
        if key in library.keys:
            mapping[key] = (key, "key", where)
            continue
        entry = next((bib[key] for bib in source_bibs if key in bib), None)
        if entry is None:
            unresolved.append((key, f"not a Zotero key and not in any source bib (cited at {where})"))
            continue
        canonical, how = library.match(entry.doi, entry.title)
        if canonical:
            mapping[key] = (canonical, how, where)
        else:
            unresolved.append((key, f"{how} (cited at {where})"))
    return mapping, unresolved


def plan_seed(root, tex_paths, source_bib_paths, library_bib_path, library):
    citations = [c for path in tex_paths for c in find_citations(root / path, label=str(path))]
    source_bibs = [parse_bib(root / p) for p in source_bib_paths]
    library_bib = parse_bib(root / library_bib_path)
    plan = Plan()
    plan.mapping, plan.unresolved = resolve(citations, source_bibs, library)
    thesis_bib = root / "thesis" / "references.bib"
    existing = parse_bib(thesis_bib) if thesis_bib.is_file() else {}
    for key in plan.canonical:
        if key not in existing:
            (plan.new_entries if key in library_bib else plan.missing_entries).append(key)
        if not (root / "kb" / "papers" / f"@{key}.md").exists():
            plan.new_stubs.append(key)
        if not (root / "kb" / "_pdf" / f"@{key}.pdf").exists():
            if key not in library.pdf_by_key:
                plan.no_pdf.append(key)
            elif readable(library.pdf_by_key[key]):
                plan.new_pdfs.append(key)
            else:
                plan.unreadable.append(key)
    return plan, library_bib, existing


def readable(pdf):
    """True if pdftotext finds at least MIN_WORDS words on the first three pages."""
    try:
        result = subprocess.run(["pdftotext", "-q", "-l", "3", "-enc", "UTF-8", str(pdf), "-"],
                                capture_output=True, text=True, errors="replace")
    except FileNotFoundError:
        raise SystemExit("pdftotext not found; install Poppler (brew install poppler)")
    return result.returncode == 0 and len(result.stdout.split()) >= MIN_WORDS


def paper_stub(key, entry, has_pdf, template, reason=NO_PDF_REASON):
    body = template.split("\n---\n", 1)[1]
    year = entry.year if entry and entry.year else ""
    title = plain_title(entry.title) if entry else key
    lines = [
        "---",
        "type: paper",
        f"citekey: {key}",
        f"year: {year}",
        "read: false",
        f"pdf: kb/_pdf/@{key}.pdf" if has_pdf else "pdf:",
        f"extraction: {'auto' if has_pdf else 'none'}",
        f"needs_review: {'false' if has_pdf else 'true'}",
        "review_reason:" if has_pdf else f'review_reason: "{reason}"',  # quoted: the text contains ": "
        "---",
        "",
        f"# {title} ({year})" if year else f"# {title}",
    ]
    return "\n".join(lines) + "\n" + body


def apply_seed(root, plan, library_bib, existing, library):
    bib_path = root / "thesis" / "references.bib"
    entries = {key: e.text for key, e in existing.items()}
    entries.update({key: library_bib[key].text for key in plan.new_entries})
    bib_path.parent.mkdir(parents=True, exist_ok=True)
    bib_path.write_text("\n\n".join(entries[k] for k in sorted(entries)) + "\n", encoding="utf-8")

    map_path = root / "thesis" / "citekey-map.tsv"
    rows = {}
    if map_path.is_file():
        for line in map_path.read_text(encoding="utf-8").splitlines()[1:]:
            if line.strip():
                rows[line.split("\t")[0]] = line
    for source, (canonical, how, where) in plan.mapping.items():
        rows.setdefault(source, f"{source}\t{canonical}\t{how}\t{where}")
    map_path.write_text(MAP_HEADER + "".join(rows[k] + "\n" for k in sorted(rows)), encoding="utf-8")

    pdf_dir = root / "kb" / "_pdf"
    for key in plan.new_pdfs:
        pdf_dir.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(library.pdf_by_key[key], pdf_dir / f"@{key}.pdf")

    template = (root / "kb" / "_templates" / "paper.md").read_text(encoding="utf-8")
    for key in plan.new_stubs:
        has_pdf = (pdf_dir / f"@{key}.pdf").is_file()
        note = root / "kb" / "papers" / f"@{key}.md"
        note.parent.mkdir(parents=True, exist_ok=True)
        reason = UNREADABLE_REASON if key in plan.unreadable else NO_PDF_REASON
        note.write_text(paper_stub(key, library_bib.get(key), has_pdf, template, reason), encoding="utf-8")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--tex", nargs="+", required=True, type=Path, help="LaTeX files whose citations to seed")
    parser.add_argument("--source-bib", nargs="*", default=[], type=Path, help=".bib files that define non-Zotero keys")
    parser.add_argument("--library-bib", required=True, type=Path, help="Better BibTeX export of the Zotero library")
    parser.add_argument("--zotero", type=Path, default=Path.home() / "Zotero", help="Zotero data directory")
    parser.add_argument("--root", type=Path, default=REPO, help="repository root (default: this repository)")
    parser.add_argument("--dry-run", action="store_true", help="report what would be written; write nothing")
    args = parser.parse_args(argv)

    library = ZoteroLibrary(args.zotero)
    plan, library_bib, existing = plan_seed(args.root, args.tex, args.source_bib, args.library_bib, library)
    remapped = sum(1 for source, (canonical, _, _) in plan.mapping.items() if source != canonical)
    print(f"{len(plan.mapping) + len(plan.unresolved)} cited keys -> {len(plan.canonical)} papers ({remapped} remapped to Zotero keys)")
    for source, (canonical, how, _) in sorted(plan.mapping.items()):
        if "duplicates" in how:
            print(f"DUPLICATE {source} -> {canonical} ({how}); merge these items in Zotero")
    for key, reason in plan.unresolved:
        print(f"UNRESOLVED {key}: {reason}")
    for key in plan.missing_entries:
        print(f"MISSING {key}: not in {args.library_bib}; re-export the Zotero library")
    if not plan.ok:
        print("Nothing written.")
        return 1
    print(f"{len(plan.new_entries)} new bib entries, {len(plan.new_stubs)} new paper notes, "
          f"{len(plan.new_pdfs)} PDFs to copy, {len(plan.no_pdf)} papers without a PDF, "
          f"{len(plan.unreadable)} unreadable")
    for key in plan.no_pdf:
        print(f"NO PDF {key}")
    for key in plan.unreadable:
        print(f"UNREADABLE {key}: {library.pdf_by_key[key]}")
    if args.dry_run:
        print("Dry run: nothing written.")
        return 0
    apply_seed(args.root, plan, library_bib, existing, library)
    print("Written: thesis/references.bib, thesis/citekey-map.tsv, kb/papers/, kb/_pdf/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 4: Run it to verify it passes**

Run: `python3 -m pytest tools/kb-seed/tests/test_seed.py -q`
Expected: `9 passed`.

- [ ] **Step 5: Commit**

```bash
git add tools/kb-seed/seed.py tools/kb-seed/tests/test_seed.py
git commit -m "kb-seed: seed bib, citekey map, paper stubs and PDFs from Zotero"
```

---

### Task 5: Content helpers (find, coverage, promote) and the README

**Files:**
- Create: `tools/kb-seed/find.py`, `tools/kb-seed/cite_coverage.py`, `tools/kb-seed/promote.py`, `tools/kb-seed/README.md`
- Modify: `kb/README.md` (one line)
- Test: `tools/kb-seed/tests/test_find_and_coverage.py`, `tools/kb-seed/tests/test_promote.py`

**Interfaces:**
- Consumes: `quotes.PdfText`, `model.load_vault` and `lint.run` from kb-lint; `bibtex.find_citations`; the kb-lint fixture `helpers.build_repo` and `helpers.edit` (in `test_promote.py`).
- Produces:
  - `search(pdf, pattern, cache_dir, context=200) -> Iterator[(page, snippet)]`.
  - `missing(root, tex_rel) -> list[(line, source_key, canonical_key)]`.
  - `promote(root, dry_run=False) -> (promoted, rejected)`.
  - The CLIs used by Tasks 7 to 12.

- [ ] **Step 1: Write the failing tests**

`tools/kb-seed/tests/test_find_and_coverage.py`:

```python
from cite_coverage import main as coverage_main
from cite_coverage import missing
from find import main as find_main
from find import search
from seed_helpers import make_pdf

TEX = "intro.tex"


def test_search_reports_pdf_page_index(tmp_path):
    pdf = tmp_path / "p.pdf"
    pdf.write_bytes(make_pdf(["First page.", "Exchange reports on\nprotein dynamics here."]))
    hits = list(search(pdf, r"protein dynamics", tmp_path / "cache", context=20))
    assert [page for page, _ in hits] == [2]
    assert "reports on protein dynamics here" in hits[0][1]  # line breaks collapsed


def test_find_cli(tmp_path, capsys):
    (tmp_path / "kb" / "_pdf").mkdir(parents=True)
    (tmp_path / "kb" / "_pdf" / "@k2020.pdf").write_bytes(make_pdf(["Alpha beta gamma."]))
    assert find_main(["@k2020", "beta", "--root", str(tmp_path)]) == 0
    assert "page 1: ...Alpha beta gamma...." in capsys.readouterr().out
    assert find_main(["@k2020", "delta", "--root", str(tmp_path)]) == 1
    assert find_main(["@missing", "x", "--root", str(tmp_path)]) == 2


def write(root, rel, text):
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def claim(origin, cites=(), body=""):
    cite_lines = "".join(f'  - "{c}"\n' for c in cites)
    return (f"---\ntype: claim\norigin: {origin}\ncites:\n{cite_lines or '  []'}\n---\n\n{body}\n"
            .replace("cites:\n  []", "cites: []"))


def setup(root):
    write(root, TEX, "Intro.\nA sentence.\\cite{old_key,keyB}\nAnother.\\cite{keyC}\n")
    write(root, "thesis/citekey-map.tsv",
          "source_key\tcanonical_key\tmatched_by\tfirst_cited_in\nold_key\tkeyA2020\tdoi\tintro.tex:2\n")


def test_uncovered_citations_are_listed_with_canonical_keys(tmp_path):
    setup(tmp_path)
    assert missing(tmp_path, TEX) == [(2, "old_key", "keyA2020"), (2, "keyB", "keyB"), (3, "keyC", "keyC")]


def test_claims_cover_by_cites_or_body_link_on_the_same_line(tmp_path):
    setup(tmp_path)
    write(tmp_path, "kb/claims/One.md", claim(f"{TEX}#L2", cites=["[[@keyA2020#^c1]]"],
                                              body="Unverified citations: [[@keyB]] (no PDF)"))
    write(tmp_path, "kb/claims/Two.md", claim(f"{TEX}#L9", cites=["[[@keyC#^c1]]"]))  # wrong line
    assert missing(tmp_path, TEX) == [(3, "keyC", "keyC")]


def test_key_prefix_does_not_count(tmp_path):
    setup(tmp_path)
    write(tmp_path, "kb/claims/One.md", claim(f"{TEX}#L3", cites=["[[@keyCa#^c1]]"]))
    assert (3, "keyC", "keyC") in missing(tmp_path, TEX)


def test_coverage_cli(tmp_path, capsys):
    setup(tmp_path)
    assert coverage_main(["--root", str(tmp_path), "--tex", TEX]) == 1
    out = capsys.readouterr().out
    assert "MISSING intro.tex:2 old_key (@keyA2020)" in out
    assert "0 of 3 citations covered" in out


def test_also_stated_in_covers_a_second_location(tmp_path):
    setup(tmp_path)
    write(tmp_path, "kb/claims/One.md", claim("other.tex#L5", cites=["[[@keyC#^c1]]"],
                                              body=f"Also stated in: {TEX}#L3"))
    write(tmp_path, "kb/claims/Two.md", claim(f"{TEX}#L30", cites=["[[@keyA2020#^c1]]", "[[@keyB#^c1]]"]))
    assert missing(tmp_path, TEX) == [(2, "old_key", "keyA2020"), (2, "keyB", "keyB")]  # L30 is not L3 or L2
```

`tools/kb-seed/tests/test_promote.py`:

```python
"""promote.py against the kb-lint fixture repository (a vault that passes every check)."""

from pathlib import Path
import sys

import pytest

KB_LINT_TESTS = Path(__file__).resolve().parents[2] / "kb-lint" / "tests"
sys.path.insert(0, str(KB_LINT_TESTS))

from helpers import build_repo, edit  # noqa: E402
from promote import main, promote  # noqa: E402

CLAIM = "kb/claims/HDX-MS constrains ensemble reweighting.md"
DRAFT = "kb/claims/Ensembles explain exchange.md"


@pytest.fixture
def repo(tmp_path):
    root = tmp_path / "repo"
    build_repo(root)
    edit(root, CLAIM, "status: supported", "status: draft")
    return root


def status(root, rel):
    return next(l for l in (root / rel).read_text().splitlines() if l.startswith("status:"))


def test_verified_draft_is_promoted(repo):
    promoted, rejected = promote(repo)
    assert [n.kb_rel for n in promoted] == ["claims/HDX-MS constrains ensemble reweighting.md"]
    assert rejected == []
    assert status(repo, CLAIM) == "status: supported"
    assert status(repo, DRAFT) == "status: draft"  # flagged needs_review, never a candidate


def test_failing_quote_is_put_back_to_draft(repo):
    edit(repo, "kb/papers/@smith2020.md", '"reports on backbone amide protection factors"', '"words the paper never said here"')
    promoted, rejected = promote(repo)
    # The failed quote is a lint error on the paper, not the claim, so the claim is a candidate,
    # then the ladder rejects it and it goes back to draft.
    assert promoted == []
    assert [n.kb_rel for n in rejected] == ["claims/HDX-MS constrains ensemble reweighting.md"]
    assert status(repo, CLAIM) == "status: draft"


def test_claim_with_lint_errors_is_not_a_candidate(repo):
    edit(repo, CLAIM, "  - fig-hdx-uptake", "  - fig-missing")
    assert promote(repo) == ([], [])
    assert status(repo, CLAIM) == "status: draft"


def test_status_comment_survives(repo):
    edit(repo, CLAIM, "status: draft", "status: draft          # draft | supported | in-thesis")
    promote(repo)
    assert status(repo, CLAIM) == "status: supported          # draft | supported | in-thesis"


def test_dry_run_changes_nothing(repo, capsys):
    assert main(["--root", str(repo), "--dry-run"]) == 0
    assert "would promote claims/HDX-MS constrains ensemble reweighting.md" in capsys.readouterr().out
    assert status(repo, CLAIM) == "status: draft"
```

- [ ] **Step 2: Run them to verify they fail**

Run: `python3 -m pytest tools/kb-seed/tests/test_find_and_coverage.py tools/kb-seed/tests/test_promote.py -q`
Expected: collection errors, `No module named 'cite_coverage'` and `No module named 'promote'`.

- [ ] **Step 3: Write the three tools**

`tools/kb-seed/find.py`:

```python
#!/usr/bin/env python3
"""Search a paper's PDF text by page, to find a verbatim quote and its 1-based PDF page index.

    python3 tools/kb-seed/find.py @citekey "regex" [--context 200]

Uses the same pdftotext extraction and cache as tools/kb-lint, so a passage found here is
the text the lint will check the quote against.
"""

import argparse
from pathlib import Path
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "kb-lint"))
from quotes import PdfText  # noqa: E402

REPO = Path(__file__).resolve().parents[2]


def search(pdf, pattern, cache_dir, context=200):
    """Yield (page index, snippet) for every match; snippets have line breaks collapsed."""
    regex = re.compile(pattern, re.I)
    for number, page in enumerate(PdfText(cache_dir).pages(pdf), start=1):
        flat = " ".join(page.split())
        for m in regex.finditer(flat):
            start, end = max(0, m.start() - context), min(len(flat), m.end() + context)
            yield number, flat[start:end]


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("paper", help="paper note name, e.g. @smith2020")
    parser.add_argument("pattern", help="case-insensitive regular expression")
    parser.add_argument("--context", type=int, default=200, help="characters shown either side")
    parser.add_argument("--root", type=Path, default=REPO)
    args = parser.parse_args(argv)
    pdf = args.root / "kb" / "_pdf" / f"{args.paper}.pdf"
    if not pdf.is_file():
        print(f"no PDF at {pdf.relative_to(args.root)}", file=sys.stderr)
        return 2
    hits = 0
    for number, snippet in search(pdf, args.pattern, args.root / "kb" / ".cache" / "pdftext", args.context):
        hits += 1
        print(f"page {number}: ...{snippet}...\n")
    print(f"{hits} matches")
    return 0 if hits else 1


if __name__ == "__main__":
    sys.exit(main())
```

`tools/kb-seed/cite_coverage.py`:

```python
#!/usr/bin/env python3
"""List the \\cite occurrences in .tex files that no claim note accounts for yet.

    python3 tools/kb-seed/cite_coverage.py --tex <file.tex> [...]

A citation of key K on line L of file F is covered when a claim note mentions `F#L<L>` (as its
`origin`, or in an "Also stated in: F#L<L>" line for a claim made in two places) and links the
canonical key of K anywhere in the note: in `cites` ("[[@key#^c1]]") or in its body, e.g. under
"Unverified citations" ("[[@key]]"). Canonical keys come from thesis/citekey-map.tsv.
"""

import argparse
import csv
from pathlib import Path
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "kb-lint"))
from bibtex import find_citations  # noqa: E402
from model import load_vault  # noqa: E402

REPO = Path(__file__).resolve().parents[2]
LOCATION = re.compile(r"([\w./-]+\.tex)#L(\d+)")


def canonical_map(root):
    path = root / "thesis" / "citekey-map.tsv"
    if not path.is_file():
        return {}
    with path.open(encoding="utf-8") as f:
        return {row["source_key"]: row["canonical_key"] for row in csv.DictReader(f, delimiter="\t")}


def missing(root, tex_rel):
    """[(line, source key, canonical key)] for citations in tex_rel with no claim note covering them."""
    mapping = canonical_map(root)
    by_location = {}
    for note in load_vault(root).notes:
        if note.type == "claim":
            text = "".join(note.lines)
            for path, line in set(LOCATION.findall(text)):
                by_location.setdefault((path, int(line)), []).append(text)
    gaps = []
    for citation in find_citations(root / tex_rel, label=str(tex_rel)):
        key = mapping.get(citation.key, citation.key)
        link = re.compile(r"\[\[@" + re.escape(key) + r"[#|\]]")
        texts = by_location.get((str(tex_rel), citation.line), [])
        if not any(link.search(text) for text in texts):
            gaps.append((citation.line, citation.key, key))
    return gaps


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--tex", nargs="+", required=True, help="repository-relative .tex paths")
    parser.add_argument("--root", type=Path, default=REPO)
    args = parser.parse_args(argv)
    total = uncovered = 0
    for tex in args.tex:
        gaps = missing(args.root, tex)
        total += len(find_citations(args.root / tex))
        uncovered += len(gaps)
        for line, source, key in gaps:
            print(f"MISSING {tex}:{line} {source}" + (f" (@{key})" if key != source else ""))
    print(f"{total - uncovered} of {total} citations covered")
    return 1 if uncovered else 0


if __name__ == "__main__":
    sys.exit(main())
```

`tools/kb-seed/promote.py`:

```python
#!/usr/bin/env python3
"""Promote draft claims to supported when the lint confirms their evidence. See README.md.

A draft claim is a candidate when it is not flagged for review, has at least one figure or cite, and
has no lint errors. Candidates are set to supported and the lint runs again; any claim the status
ladder (check 6) rejects is put back to draft. The ladder stays the single definition of "supported".
"""

import argparse
from pathlib import Path
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "kb-lint"))
from lint import run  # noqa: E402
from model import load_vault  # noqa: E402

REPO = Path(__file__).resolve().parents[2]
STATUS_LINE = re.compile(r"^(status:[ \t]*)(draft|supported)\b", re.M)


def set_status(path, status):
    text = path.read_text(encoding="utf-8")
    end = text.index("\n---", 3)  # only touch the frontmatter
    head, count = STATUS_LINE.subn(lambda m: m.group(1) + status, text[:end], count=1)
    if count:
        path.write_text(head + text[end:], encoding="utf-8")


def candidates(root):
    errors = {i.path for i in run(root).errors}
    found = []
    for note in load_vault(root).notes:
        meta = note.meta or {}
        if note.type != "claim" or meta.get("status") != "draft" or meta.get("needs_review") is not False:
            continue
        if not (meta.get("figures") or meta.get("cites")) or note.rel in errors:
            continue
        found.append(note)
    return found


def promote(root, dry_run=False):
    """Returns (promoted notes, rejected notes)."""
    notes = candidates(root)
    if dry_run or not notes:
        return notes, []
    for note in notes:
        set_status(note.path, "supported")
    rejected_paths = {i.path for i in run(root).errors if i.check == 6}
    rejected = [n for n in notes if n.rel in rejected_paths]
    for note in rejected:
        set_status(note.path, "draft")
    return [n for n in notes if n not in rejected], rejected


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--root", type=Path, default=REPO, help="repository root (default: this repository)")
    parser.add_argument("--dry-run", action="store_true", help="list candidates; change nothing")
    args = parser.parse_args(argv)
    promoted, rejected = promote(args.root, dry_run=args.dry_run)
    for note in promoted:
        print(("would promote " if args.dry_run else "promoted ") + note.kb_rel)
    for note in rejected:
        print("kept as draft (status ladder) " + note.kb_rel)
    print(f"{len(promoted)} promoted, {len(rejected)} kept as draft")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 4: Run the whole kb-seed suite and the kb-lint suite together**

Run: `python3 -m pytest tools/kb-seed/tests tools/kb-lint/tests -q`
Expected: `130 passed`. Running both suites in one session also proves their module names don't collide.

- [ ] **Step 5: Write `tools/kb-seed/README.md`**

````markdown
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
````

- [ ] **Step 6: Point to it from `kb/README.md`.** Directly after the paragraph that begins "`review-queue.md` is generated by", add:

```markdown
[tools/kb-seed](../tools/kb-seed/README.md) seeds paper notes and PDFs from Zotero, finds quotes in PDFs, checks that every citation in a `.tex` file is accounted for, and promotes verified claims.
```

- [ ] **Step 7: Commit**

```bash
git add tools/kb-seed kb/README.md
git commit -m "kb-seed: find, citation coverage and promote tools"
```

---

### Task 6: Seed the introduction literature

**Files (generated):** `thesis/references.bib`, `thesis/citekey-map.tsv`, `kb/papers/@*.md` (81 notes), `kb/review-queue.md`; `kb/_pdf/` (gitignored).

- [ ] **Step 1: Dry run**

```bash
python3 tools/kb-seed/seed.py --dry-run --tex projects/1-ValDX/manuscript/report/1_introduction_omc.tex milestones/2025-11-confirmation-of-status/introduction/biological_dynamics.tex milestones/2025-11-confirmation-of-status/introduction/measuring_dynamics.tex milestones/2025-11-confirmation-of-status/introduction/ensemble_generators.tex milestones/2025-11-confirmation-of-status/introduction/connect_simulation_experiment.tex milestones/2025-11-confirmation-of-status/introduction/packages.tex milestones/2025-11-confirmation-of-status/introduction/thesis_outline.tex --source-bib projects/1-ValDX/manuscript/report/_references.bib --library-bib milestones/2025-11-confirmation-of-status/zotero_library.bib
```

Expected (verified against the author's library on 2026-10-09; counts can shift if Zotero changed since):

```text
90 cited keys -> 81 papers (26 remapped to Zotero keys)
DUPLICATE james_advances_2022 -> jamesAdvancesHydrogenDeuterium2022 (...)
DUPLICATE lee_interpreting_2021 -> leeInterpretingHydrogenDeuteriumExchange2021 (...)
DUPLICATE masson_recommendations_2019 -> massonRecommendationsPerformingInterpreting2019 (...)
81 new bib entries, 81 new paper notes, 70 PDFs to copy, 10 papers without a PDF, 1 unreadable
```

There should be no `UNRESOLVED` or `MISSING` lines. If there are, stop and report them; they mean the Zotero library and the export have drifted apart.

- [ ] **Step 2: Real run.** Run the same command without `--dry-run`.
Expected: the same summary, then `Written: thesis/references.bib, thesis/citekey-map.tsv, kb/papers/, kb/_pdf/`.

- [ ] **Step 3: Lint and review queue**

Run: `python3 tools/kb-lint/lint.py --write`
Expected: `wrote kb/review-queue.md` and `0 errors, 0 warnings`. The queue has two headings, "No PDF in Zotero…" (10 papers) and "PDF in Zotero has no readable text…" (1 paper).

- [ ] **Step 4: Commit** (the PDFs are gitignored, so they won't be staged)

```bash
git add thesis/references.bib thesis/citekey-map.tsv kb/papers kb/review-queue.md
git status --short | grep -c "_pdf" || true   # expect 0
git commit -m "kb: seed introduction literature from Zotero (81 papers)"
```

---

## Extraction protocol (Tasks 7 to 11)

Each content task applies this protocol to one `.tex` file, called **SRC** below.

1. **List the work.** Run `python3 tools/kb-seed/cite_coverage.py --tex SRC`. Each `MISSING SRC:L key (@canonical)` line is a citation to account for. Read paragraph L with `sed -n 'Lp' SRC`.
2. **One claim per cited sentence.** Split the paragraph into sentences. Each sentence containing `\cite` becomes one claim. Skip sentences without citations; they are the author's own framing, handled in step 3 of the spec.
3. **Find the claim note, or create it.**
   - **Reuse:** if a note in `kb/claims/` already states this claim (because it is made in both introductions), don't create a duplicate. Add a body line `Also stated in: SRC#L<L>` and add any new cites to it.
   - **Create:** otherwise create `kb/claims/<title>.md` from `kb/_templates/claim.md`.
   - **Title:** the claim as one plain-English sentence with LaTeX removed, at most about 120 characters, and none of these characters: `/ \ : # ^ [ ] | ? *`. Keep the source's meaning, and don't strengthen it.
   - **Frontmatter:**
     - `type: claim`, `chapter: 01-introduction`, `project:` (empty), `basis: stated`
     - `confidence:` high, medium or low (see 5)
     - `status: draft`, `origin: SRC#L<L>`, `source_state: current`
     - `needs_review` and `review_reason` (see 5)
     - `figures: []`, `cites:` (see 4), `code: []`
4. **For each key the sentence cites**, take the canonical key from the coverage line or `thesis/citekey-map.tsv`.
   - **The paper has a PDF** (`extraction: auto`):
     - Run `python3 tools/kb-seed/find.py @KEY "<regex>"` with terms from the claim, and read the snippets.
     - Choose a passage that states what the sentence attributes to the paper.
     - **Reuse** an existing block in `kb/papers/@KEY.md` if one already says this.
     - **Otherwise add a block** under `## Claims`, after the template's comment, with the next free ID (`^c1`, `^c2`, ...):
       - the bullet text is what *the paper* says, in one paraphrased sentence
       - `page` is the number `find.py` printed
       - `quote` is 5 to 25 words copied exactly from the snippet, starting and ending on whole words
       - `quote_check: unchecked`
       - `reviewed: false`
     - Add `"[[@KEY#^cN]]"` to the claim's `cites`, quoted as shown.
   - **The paper has no PDF, or no supporting passage exists:**
     - Do not add a block or invent a quote.
     - Add a body section `## Unverified citations` with a line `- [[@KEY]]: no PDF` or `- [[@KEY]]: no passage supporting this claim found`.
5. **Confidence and review.** Use exactly one of these `review_reason` texts, so the review queue groups them:

   | Situation | Settings |
   |---|---|
   | Every cite has a block that directly states the claim | `confidence: high`, `needs_review: false` |
   | The passages support it only partly or indirectly, e.g. a review cited for a general statement, or the sentence goes beyond the paper | `confidence: medium` or `low`, `needs_review: true`, `review_reason: Support is partial or indirect` |
   | A cited paper's passage contradicts the sentence, or nothing supports it | `needs_review: true`, `review_reason: Cited paper does not support the claim` |
   | No cite could be checked (every cited paper lacks a PDF) | `needs_review: true`, `review_reason: No PDF for any cited paper` |
   | The sentence is ambiguous, or splitting it needs the author's call | `needs_review: true`, `review_reason: Claim wording needs the author's judgement` |

6. **Body:**
   - `## Argument`: one to three sentences on how the cited passages support the claim. Link key technical terms as `[[Concept name]]`; Task 12 creates those notes.
   - `## Caveats`: only if needed.
   - `## Unverified citations`: if any.
7. **Close the file** with these commands, in order:

   ```bash
   python3 tools/kb-lint/lint.py --write          # fix every ERROR; quote failures: re-run find.py and copy the text exactly
   python3 tools/kb-seed/promote.py               # promotes only what the ladder accepts
   python3 tools/kb-lint/lint.py --write          # expect 0 errors
   python3 tools/kb-seed/cite_coverage.py --tex SRC   # expect "N of N citations covered"
   ```

   A `WARN [check 2]` on an uncited block means a quote that failed but no claim relies on it. Fix the quote or delete the block.

**Worked example** (from the pilot, ValDX introduction line 8). This is the sentence "HDX-MS is a biophysical technique that measures conformational dynamics in solution.", which cites `masson_overview_2017` (no PDF), `masson_recommendations_2019`, `narang_hdx-ms_2020` and `james_advances_2022`.

- Block in `kb/papers/@narangHDXMSAnalyticalTool2020.md`:

  ```markdown
  - HDX-MS data are most informative read as a measure of conformational dynamics on a reference structure. ^c1
    - page: 2
    - quote: "HDX-MS data are much more informative when viewed as a measure of conformational dynamics"
    - quote_check: unchecked
    - reviewed: false
  ```

- Claim `kb/claims/HDX-MS measures protein conformational dynamics in solution.md`:
  - `origin: projects/1-ValDX/manuscript/report/1_introduction_omc.tex#L8`
  - `cites:` the Masson 2019, Narang and James blocks
  - body: `## Unverified citations` with `- [[@massonOverviewHydrogenDeuterium2017]]: no PDF`

In the pilot, all three quotes passed and `promote.py` promoted the claim.

---

### Task 7: Extract the ValDX introduction

**SRC:** `projects/1-ValDX/manuscript/report/1_introduction_omc.tex` (39 citations in 5 paragraphs).

- [ ] **Step 1:** Run `python3 tools/kb-seed/cite_coverage.py --tex SRC`. Expected: `0 of 39 citations covered`.
- [ ] **Step 2:** Apply protocol steps 2 to 6 to every `MISSING` line.
- [ ] **Step 3:** Run protocol step 7. Expected: lint `0 errors`; coverage `39 of 39 citations covered`.
- [ ] **Step 4: Commit**

```bash
git add kb/claims kb/papers kb/review-queue.md
git commit -m "kb: claims from the ValDX introduction"
```

### Task 8: Extract `measuring_dynamics.tex`

**SRC:** `milestones/2025-11-confirmation-of-status/introduction/measuring_dynamics.tex`. Steps as in Task 7. Expected coverage: all citations covered (the count is printed by step 1). Commit message: `kb: claims from the confirmation report, measuring dynamics`.

### Task 9: Extract `biological_dynamics.tex`

**SRC:** `milestones/2025-11-confirmation-of-status/introduction/biological_dynamics.tex`. Steps as in Task 7. Commit message: `kb: claims from the confirmation report, biological dynamics`.

### Task 10: Extract `ensemble_generators.tex`

**SRC:** `milestones/2025-11-confirmation-of-status/introduction/ensemble_generators.tex`. Steps as in Task 7. Commit message: `kb: claims from the confirmation report, ensemble generators`.

### Task 11: Extract `connect_simulation_experiment.tex`

**SRC:** `milestones/2025-11-confirmation-of-status/introduction/connect_simulation_experiment.tex`. Steps as in Task 7. Commit message: `kb: claims from the confirmation report, simulation and experiment`.

---

### Task 12: Concept notes and the final check

- [ ] **Step 1: List the concept links that don't resolve to a note**

```bash
python3 - <<'EOF'
import re, sys
sys.path.insert(0, "tools/kb-lint")
from model import load_vault
vault = load_vault(".")
names = {n.name for n in vault.notes}
links = {}
for note in vault.notes:
    if note.type == "claim":
        for target in re.findall(r"\[\[([^\]#|@][^\]#|]*)", "".join(note.lines)):
            if target not in names:
                links.setdefault(target, []).append(note.name)
for target, users in sorted(links.items(), key=lambda kv: -len(kv[1])):
    print(f"{len(users):3d}  {target}")
EOF
```

- [ ] **Step 2: Write the concept notes.** For every target linked from two or more claims:
  - Create `kb/concepts/<target>.md` from `kb/_templates/concept.md`, and add `aliases` for other spellings.
  - `## Definition`: one to three sentences in plain English.
  - `## Why it matters here`: link the claim notes that use it.
  - Leave `notation: []` unless the claims use a symbol.
  - For a target used only once, rewrite the link as plain text instead.
- [ ] **Step 3: Final checks**

```bash
python3 tools/kb-lint/lint.py --write
python3 tools/kb-seed/cite_coverage.py --tex projects/1-ValDX/manuscript/report/1_introduction_omc.tex milestones/2025-11-confirmation-of-status/introduction/measuring_dynamics.tex milestones/2025-11-confirmation-of-status/introduction/biological_dynamics.tex milestones/2025-11-confirmation-of-status/introduction/ensemble_generators.tex milestones/2025-11-confirmation-of-status/introduction/connect_simulation_experiment.tex
```

Expected: `0 errors`, and every citation covered.

- [ ] **Step 4: Report for the author.** Write a short summary in the final message:
  - claims by status
  - review-queue headings with their counts
  - the list of papers without a readable PDF
  - the 3 Zotero duplicates to merge
- [ ] **Step 5: Commit**

```bash
git add kb/concepts kb/claims kb/review-queue.md
git commit -m "kb: concept notes for the introduction"
```
