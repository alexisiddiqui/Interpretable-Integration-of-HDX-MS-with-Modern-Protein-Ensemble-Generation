# KB lint and schema (step 1) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Give the Obsidian vault in `kb/` a checked schema, so that no claim reaches `supported` without a quote found in its source PDF, a figure that exists, or code that exists at a recorded commit.

**Architecture:** A small Python tool in `tools/kb-lint/`, alongside the existing `tools/thesis-map/` and `tools/project-map/`. `model.py` loads the vault once (frontmatter, paper claim blocks, bib keys). Each check is a pure function `check_*(vault) -> list[Issue]` in its own module, numbered as in spec section 5. `lint.py` runs them in order, prints the issues and, with `--write`, records quote-check results and regenerates `kb/review-queue.md`. Templates in `kb/_templates/` are tested against the schema, so the two cannot drift apart.

**Tech Stack:** Python 3.10 (same floor as `tools/thesis-map`), PyYAML, pytest, Poppler `pdftotext`, git.

**Spec:** `docs/superpowers/specs/2026-10-08-thesis-kb-design.md` (sections 4, 5 and 6 "Step 1").

## Global Constraints

- Repository root: `Interpretable-Integration-of-HDX-MS-with-Modern-Protein-Ensemble-Generation/`. Run every command below from it.
- Work on a branch, e.g. `git switch -c kb-lint-step1`; `main` is the published branch.
- Python 3.10 or later; third-party imports limited to `yaml` (PyYAML) and, in tests, `pytest`. External programs: `pdftotext` (Poppler) and `git`.
- Check numbers and severities follow spec section 5 exactly. Check 10 (phrase echo) is **not** in this plan: spec section 6 assigns it to step 4.
- Read-only by default. `--write` changes only `quote_check:` lines inside paper claim blocks and the generated `kb/review-queue.md`.
- `page` is the 1-based PDF page index. Quotes are at most 25 words.
- Code reference format: `<submodule path>@<sha>:<file>#L<start>-<end>` (spec 4.6).
- Paper notes are named `@<citekey>` and the citekey must exist in `thesis/references.bib`.
- Gitignore additions: `kb/_pdf/`, `kb/.cache/`.
- Output line format, relied on by tests: `ERROR [check N] <repo-relative path>: <message>` or `WARN  [check N] ...`, then `<n> errors, <m> warnings`. Exit code 0 (no errors), 1 (errors), 2 (no `kb/` folder).

### Decisions where the spec is silent (made here, flagged for review)

- **PDF absent locally** (PDFs are gitignored, so a fresh clone has none): warning, quotes not checked, the recorded `quote_check` is left as it is.
- **Submodule not checked out**: warning with a `git submodule update --init` hint, not an error. A SHA that is missing, or a file or lines that do not exist, is still an error.
- **`supported` / `in-thesis`** require: at least one figure or cite; `needs_review: false`; and every cited block at `quote_check: pass` (using this run's result when the PDF was read). `in-thesis` is not cross-checked against `.tex` files.
- **`source_state: outdated`** claims need at least one figure ID to leave `draft`. Literature cites alone are not enough.
- **Every key in a template is required** in notes of that type. A value may be empty where the validator allows it, e.g. `code: []`.
- **`chapters/` and `inbox/`** notes may have no frontmatter type. Elsewhere a type is required.
- **Pinned commit for drift** is the superproject's gitlink (`git ls-tree HEAD`); if there is none, it falls back to the submodule's checked-out `HEAD`.

## Review Focus

- Wikilinks typed unquoted in YAML frontmatter, as Obsidian users often do (`- [[@key#^c1]]` is a YAML error; `- [[name#^c1]]` silently becomes a nested list). Expected: a check 1 error that says to quote the link. Tested in Tasks 1 and 2.
- A fresh clone with no PDFs. Expected: a warning only, with `quote_check` never overwritten to `fail`. Tested in Task 4.
- A fresh clone without submodules checked out. Expected: a warning, not a wall of errors. Tested in Task 5.
- Quotes that cross a page break, a line-break hyphen, a ligature (`ﬁ`) or curly quotes. Expected: found. Tested in Task 4.
- The commented example claim in the paper template, which every new paper note inherits. Expected: ignored, never parsed as a real `^c1` block. Tested in Task 1.

## File Structure

| File | Responsibility |
|---|---|
| `tools/kb-lint/model.py` | `Issue`, `Block`, `Note`, `Vault`; frontmatter, claim-block, wikilink and bib parsing; `load_vault(root)` |
| `tools/kb-lint/schema.py` | Check 1 (schema per type, folder/type, paper rules, block problems) and check 9 (methods need code) |
| `tools/kb-lint/links.py` | Checks 3 (figure IDs), 4 (cites and citekeys resolve), 5 (no cites into `ref-theses/`) |
| `tools/kb-lint/quotes.py` | Check 2: `normalise`, `PdfText` (pdftotext with cache), `check_quotes`, `write_quote_checks` |
| `tools/kb-lint/coderefs.py` | Checks 7 (code refs resolve at the SHA) and 8 (drift from the pinned commit) |
| `tools/kb-lint/ladder.py` | Check 6: status ladder rules |
| `tools/kb-lint/review_queue.py` | `render_queue(vault) -> str` for `kb/review-queue.md` |
| `tools/kb-lint/lint.py` | `run(root, write=False, cache_dir=None) -> Result` and the CLI |
| `tools/kb-lint/tests/helpers.py` | Fixture repository builder: a valid vault, a generated 3-page PDF, a git "submodule" pinned by gitlink |
| `tools/kb-lint/tests/conftest.py` | `repo` fixture; puts `tools/kb-lint` and `tests/` on `sys.path` |
| `tools/kb-lint/tests/test_*.py` | One test file per module, plus `test_lint.py` end to end |
| `tools/kb-lint/README.md`, `requirements.txt` | Usage and dependencies |
| `kb/_templates/*.md` | Five updated templates and four new ones (`method`, `ref-thesis`, `move`, `concept-candidate`) |
| `kb/README.md`, `.gitignore` | Rules and folders updated; `kb/_pdf/` and `kb/.cache/` ignored |

---

### Task 1: Vault model and fixture repository

**Files:**
- Create: `tools/kb-lint/model.py`
- Create: `tools/kb-lint/requirements.txt`
- Create: `tools/kb-lint/tests/helpers.py`
- Create: `tools/kb-lint/tests/conftest.py`
- Test: `tools/kb-lint/tests/test_model.py`

**Interfaces:**
- Consumes: nothing.
- Produces (used by every later task):
  - `Issue(severity: str, check: int, path: str, message: str)`, where `str(issue)` gives the output line format.
  - `Block`: `.id .text .line .page .quote .quote_check .reviewed .quote_check_line .computed .effective_quote_check`.
  - `Note`: `.path .rel .kb_rel .lines .meta .meta_error .blocks .block_problems .name .type .folder .in_ref_theses .block(id)`.
  - `Vault`: `.root .notes .bib_keys .find(name) -> Note | None .duplicates() -> dict .citations() -> dict[(paper_name, block_id), list[Note]]`.
  - `parse_wikilink(text) -> (target, block_id | None) | None`, `parse_frontmatter(lines) -> (meta, error, body_index)`, `parse_blocks(lines, start) -> (blocks, problems)`, `load_vault(root) -> Vault`.
  - Test helpers: `build_repo(root) -> sha`, `make_pdf(pages) -> bytes`, `git(cwd, *args)`, `commit_file(repo, path, content) -> sha`, `pin(root, repo_rel, sha)`, `write(root, rel, text)`, `edit(root, rel, old, new)`, `MODEL_PY`.

- [ ] **Step 1: Write the requirements, fixture helpers and the failing test**

`tools/kb-lint/requirements.txt`:

```text
PyYAML>=6,<7
pytest>=7
```

`tools/kb-lint/tests/helpers.py` (the fixture repository; later tasks rely on its exact note texts):

```python
"""Build a small, valid fixture repository for the lint tests."""

from pathlib import Path
import subprocess

PDF_PAGES = [
    "Hydrogen deuterium exchange reports on\nbackbone amide protec-\ntion factors.",
    "Reweighting corrects force field bias without\nrefitting the model. The effect carries",
    "over to the next page of the article.",
]
MODEL_PY = "def protection(k_int, k_obs):\n    return k_int / k_obs\n\n"


def make_pdf(pages):
    """A minimal PDF with one Helvetica text page per string; lines split on newlines."""
    kids = " ".join(f"{4 + 2 * i} 0 R" for i in range(len(pages)))
    objects = [
        "<< /Type /Catalog /Pages 2 0 R >>",
        f"<< /Type /Pages /Kids [{kids}] /Count {len(pages)} >>",
        "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
    ]
    for i, page in enumerate(pages):
        ops = ["BT", "/F1 11 Tf", "14 TL", "72 720 Td"]
        for line in page.split("\n"):
            escaped = line.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
            ops.append(f"({escaped}) Tj T*")
        ops.append("ET")
        stream = "\n".join(ops)
        objects.append(
            f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
            f"/Resources << /Font << /F1 3 0 R >> >> /Contents {5 + 2 * i} 0 R >>"
        )
        objects.append(f"<< /Length {len(stream.encode('latin-1'))} >>\nstream\n{stream}\nendstream")
    out = bytearray(b"%PDF-1.4\n")
    offsets = []
    for number, body in enumerate(objects, start=1):
        offsets.append(len(out))
        out += f"{number} 0 obj\n{body}\nendobj\n".encode("latin-1")
    xref = len(out)
    out += f"xref\n0 {len(objects) + 1}\n0000000000 65535 f \n".encode()
    for offset in offsets:
        out += f"{offset:010d} 00000 n \n".encode()
    out += f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode()
    return bytes(out)


def git(cwd, *args):
    result = subprocess.run(
        ["git", "-c", "user.name=kb-lint", "-c", "user.email=kb-lint@example.com",
         "-c", "commit.gpgsign=false", "-c", "init.defaultBranch=main", *args],
        cwd=cwd, capture_output=True, text=True, check=True,
    )
    return result.stdout.strip()


def commit_file(repo, path, content):
    """Write and commit one file in a git repository; returns the new commit SHA."""
    (repo / path).write_text(content, encoding="utf-8")
    git(repo, "add", path)
    git(repo, "commit", "-q", "-m", f"update {path}")
    return git(repo, "rev-parse", "HEAD")


def pin(root, repo_rel, sha):
    """Record sha as the superproject's pinned commit for repo_rel, like a submodule bump."""
    git(root, "update-index", "--add", "--cacheinfo", f"160000,{sha},{repo_rel}")
    git(root, "commit", "-q", "-m", f"pin {repo_rel}")


def write(root, rel, text):
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def edit(root, rel, old, new):
    """Replace one exact snippet in a fixture file; fails loudly if the snippet is absent."""
    path = root / rel
    text = path.read_text(encoding="utf-8")
    assert old in text, f"{old!r} not in {rel}"
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


PAPER = """---
type: paper
citekey: smith2020
year: 2020
read: true
pdf: kb/_pdf/@smith2020.pdf
extraction: auto
needs_review: false
review_reason:
---

## Main point

HDX-MS reports on protection.

## Claims

<!-- Example, ignored by the lint:
- Paraphrase. ^c9
  - page: 1
-->

- HDX-MS reports on backbone amide protection. ^c1
  - page: 1
  - quote: "reports on backbone amide protection factors"
  - quote_check: unchecked
  - reviewed: false
- Reweighting corrects bias without refitting, across a page break. ^c2
  - page: 2
  - quote: "The effect carries over to the next page"
  - quote_check: unchecked
  - reviewed: false

## What I use from it
"""

PAPER_NO_PDF = """---
type: paper
citekey: jones2019
year: 2019
read: false
pdf:
extraction: none
needs_review: true
review_reason: No PDF available
---

## Claims

- Ensembles explain HDX better than single structures. ^c1
  - page: 3
  - quote: "ensembles explain exchange better"
  - quote_check: unchecked
  - reviewed: false
"""

CLAIM = """---
type: claim
chapter: 01-introduction
project:
basis: stated
confidence: high
status: supported
origin: projects/1-ValDX/manuscript/main_omc.tex#sec:intro
source_state: current
needs_review: false
review_reason:
figures:
  - fig-hdx-uptake
cites:
  - "[[@smith2020#^c1]]"
code: []
---

## Argument
"""

DRAFT_CLAIM = """---
type: claim
chapter: 01-introduction
project:
basis: inferred
confidence: low
status: draft
origin: milestones/2025-11-confirmation-of-status/introduction/ensemble_generators.tex
source_state: current
needs_review: true
review_reason: Ambiguous wording in the confirmation report
figures: []
cites:
  - "[[@jones2019#^c1]]"
code: []
---
"""

CONCEPT = """---
type: concept
aliases: [PF]
notation:
  - {symbol: "P_i", meaning: "protection factor of residue i", units: null}
---

## Definition
"""

METHOD = """---
type: method
project: 2-jaxENT
status: draft
needs_review: false
review_reason:
code:
  - "projects/demo/code@{sha}:model.py#L1-2"
---

## What it does
"""

DECISION = """---
type: decision
date: 2026-10-08
project:
status: active
---

## Decision
"""

FIGURE = """---
type: figure
fig_id: fig-hdx-uptake
chapter: 03-valdx
source: script
code: []
---
"""

MOVE = """---
type: move
thesis: crook
page: 11
move_type: gap-framing
locator_quote: up to half the proteome cannot be robustly assigned
generated: true
needs_review: true
review_reason: Generated move; check the paraphrase against the page
---

## Paraphrase
"""

BIB = """@article{smith2020,
  title = {Protection factors},
}
@book{jones2019,
  title = {Ensembles},
}
"""


def build_repo(root):
    """Create a repository that passes every check. Returns the demo submodule's commit SHA."""
    root.mkdir(parents=True, exist_ok=True)
    code = root / "projects" / "demo" / "code"
    code.mkdir(parents=True)
    git(code, "init", "-q")
    sha = commit_file(code, "model.py", MODEL_PY)
    git(root, "init", "-q")
    pin(root, "projects/demo/code", sha)

    write(root, "thesis/references.bib", BIB)
    write(root, "figures/fig-hdx-uptake/README.md", "Uptake figure.\n")
    (root / "kb" / "_pdf").mkdir(parents=True)
    (root / "kb" / "_pdf" / "@smith2020.pdf").write_bytes(make_pdf(PDF_PAGES))
    write(root, "kb/README.md", "# Knowledge base\n")
    write(root, "kb/_templates/claim.md", "---\ntype: claim\nchapter:\n---\n")
    write(root, "kb/papers/@smith2020.md", PAPER)
    write(root, "kb/papers/@jones2019.md", PAPER_NO_PDF)
    write(root, "kb/claims/HDX-MS constrains ensemble reweighting.md", CLAIM)
    write(root, "kb/claims/Ensembles explain exchange.md", DRAFT_CLAIM)
    write(root, "kb/concepts/Protection factor.md", CONCEPT)
    write(root, "kb/methods/Protection factor model (2-jaxENT).md", METHOD.format(sha=sha[:7]))
    write(root, "kb/decisions/2026-10-08 Use the PDF page index.md", DECISION)
    write(root, "kb/figures/fig-hdx-uptake.md", FIGURE)
    write(root, "kb/ref-theses/crook/Gap framing.md", MOVE)
    write(root, "kb/chapters/01-introduction.md", "# Introduction\n\n1. [[HDX-MS constrains ensemble reweighting]]\n")
    return sha
```

`tools/kb-lint/tests/conftest.py`:

```python
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # tools/kb-lint
sys.path.insert(0, str(Path(__file__).resolve().parent))      # tests/helpers.py

from helpers import build_repo  # noqa: E402


@pytest.fixture
def repo(tmp_path):
    """A fixture repository that passes every check; tests break one thing at a time."""
    root = tmp_path / "repo"
    build_repo(root)
    return root
```

`tools/kb-lint/tests/test_model.py`:

```python
from model import load_vault, parse_blocks, parse_frontmatter, parse_wikilink


def lines(text):
    return text.splitlines(keepends=True)


def test_frontmatter_parses_fields_and_body_start():
    meta, error, body = parse_frontmatter(lines("---\ntype: claim\nfigures: []\n---\nBody\n"))
    assert meta == {"type": "claim", "figures": []}
    assert error is None
    assert body == 4


def test_unquoted_wikilink_in_frontmatter_gets_a_hint():
    meta, error, _ = parse_frontmatter(lines("---\ncites: [[@a#^c1]]\n---\n"))
    assert meta is None
    assert "quote wikilinks" in error


def test_note_without_frontmatter_has_no_meta_and_no_error():
    assert parse_frontmatter(lines("# Hub\n")) == (None, None, 0)


def test_wikilink_with_and_without_block():
    assert parse_wikilink("[[@smith2020#^c1]]") == ("@smith2020", "c1")
    assert parse_wikilink("[[Protection factor|PF]]") == ("Protection factor", None)
    assert parse_wikilink("@smith2020") is None


def test_blocks_parse_fields_and_skip_comments():
    text = (
        "## Claims\n\n<!--\n- Example. ^c9\n-->\n"
        "- A claim. ^c1\n  - page: 2\n  - quote: \"some words\"\n"
        "  - quote_check: unchecked\n  - reviewed: true\n\n## Other\n- Not a claim\n"
    )
    blocks, problems = parse_blocks(lines(text), 0)
    assert problems == []
    assert [b.id for b in blocks] == ["c1"]
    b = blocks[0]
    assert (b.text, b.page, b.quote, b.quote_check, b.reviewed) == ("A claim.", 2, "some words", "unchecked", True)
    assert b.quote_check_line == 8


def test_block_problems_are_reported():
    text = "## Claims\n- No id here\n- Fine. ^c1\n  - page: zero\n- Again. ^c1\n"
    _, problems = parse_blocks(lines(text), 0)
    assert any("no block ID" in p for p in problems)
    assert any("page must be a whole number" in p for p in problems)
    assert any("^c1 is used twice" in p for p in problems)
    assert any("missing 'quote'" in p for p in problems)


def test_load_vault_skips_templates_and_root_files(repo):
    vault = load_vault(repo)
    rels = {note.kb_rel for note in vault.notes}
    assert "papers/@smith2020.md" in rels
    assert not any(r.startswith("_templates/") for r in rels)
    assert "README.md" not in rels
    assert vault.bib_keys == {"smith2020", "jones2019"}
    assert [b.id for b in vault.find("@smith2020").blocks] == ["c1", "c2"]


def test_citations_map_blocks_to_citing_claims(repo):
    cited = load_vault(repo).citations()
    assert [n.name for n in cited[("@smith2020", "c1")]] == ["HDX-MS constrains ensemble reweighting"]
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `python3 -m pytest tools/kb-lint/tests/test_model.py -q`
Expected: collection error, `ModuleNotFoundError: No module named 'model'`.

- [ ] **Step 3: Write `tools/kb-lint/model.py`**

```python
"""Load the vault: notes, frontmatter, paper claim blocks, wikilinks and bib keys."""

from dataclasses import dataclass, field
from pathlib import Path
import re

import yaml

SKIP_DIRS = {"_templates", "_pdf"}
REF_THESES = "ref-theses"
QUOTE_STATES = ("pass", "fail", "unchecked")
BLOCK_FIELDS = ("page", "quote", "quote_check", "reviewed")
BLOCK_RE = re.compile(r"^- (?P<text>.*?)\s+\^(?P<id>[A-Za-z0-9-]+)\s*$")
FIELD_RE = re.compile(r"^\s+- (?P<key>\w+):\s*(?P<value>.*?)\s*$")
WIKILINK_RE = re.compile(
    r"^\[\[(?P<target>[^\]#|]+?)(?:#\^(?P<block>[A-Za-z0-9-]+))?(?:\|[^\]]*)?\]\]$"
)
BIB_RE = re.compile(r"@(?P<kind>\w+)\s*\{\s*(?P<key>[^,\s]+)\s*,")


@dataclass
class Issue:
    severity: str  # "error" or "warning"
    check: int     # check number in the spec, section 5
    path: str      # repository-relative path of the note
    message: str

    def __str__(self):
        label = "ERROR" if self.severity == "error" else "WARN "
        return f"{label} [check {self.check}] {self.path}: {self.message}"


@dataclass
class Block:
    """One attributed claim in a paper note's ## Claims section."""

    id: str
    text: str
    line: int                          # index into Note.lines of the bullet
    page: int | None = None
    quote: str | None = None
    quote_check: str | None = None
    reviewed: bool | None = None
    quote_check_line: int | None = None
    computed: str | None = None        # this run's quote check, when the PDF was read
    fields_seen: set = field(default_factory=set)

    @property
    def effective_quote_check(self):
        return self.computed or self.quote_check


@dataclass
class Note:
    path: Path
    rel: str                           # relative to the repository root
    kb_rel: str                        # relative to kb/
    lines: list                        # file lines, line endings kept
    meta: dict | None = None
    meta_error: str | None = None
    blocks: list = field(default_factory=list)
    block_problems: list = field(default_factory=list)

    @property
    def name(self):
        return self.path.stem

    @property
    def type(self):
        return (self.meta or {}).get("type")

    @property
    def folder(self):
        return self.kb_rel.split("/")[0]

    @property
    def in_ref_theses(self):
        return self.folder == REF_THESES

    def block(self, block_id):
        return next((b for b in self.blocks if b.id == block_id), None)


@dataclass
class Vault:
    root: Path
    notes: list
    bib_keys: set

    def __post_init__(self):
        self._by_name = {}
        for note in self.notes:
            self._by_name.setdefault(note.name, []).append(note)

    def find(self, name):
        """The note with this name, or None if there is no note or more than one."""
        matches = self._by_name.get(name, [])
        return matches[0] if len(matches) == 1 else None

    def duplicates(self):
        return {name: notes for name, notes in self._by_name.items() if len(notes) > 1}

    def citations(self):
        """Map (paper note name, block ID) to the claim notes that cite it."""
        cited = {}
        for note in self.notes:
            if note.type != "claim":
                continue
            for entry in note.meta.get("cites") or []:
                link = parse_wikilink(entry) if isinstance(entry, str) else None
                if link and link[1]:
                    cited.setdefault(link, []).append(note)
        return cited


def parse_wikilink(text):
    """'[[@smith2020#^c1]]' -> ('@smith2020', 'c1'); the block is None when absent."""
    m = WIKILINK_RE.match(text.strip())
    return (m["target"].strip(), m["block"]) if m else None


def parse_frontmatter(lines):
    """Return (meta, error, index of the first body line)."""
    if not lines or lines[0].rstrip("\r\n") != "---":
        return None, None, 0
    for end in range(1, len(lines)):
        if lines[end].rstrip("\r\n") == "---":
            break
    else:
        return None, "frontmatter has no closing ---", 0
    text = "".join(lines[1:end])
    try:
        meta = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        hint = ' (quote wikilinks in frontmatter, e.g. - "[[@key#^c1]]")' if "[[" in text else ""
        problem = getattr(exc, "problem", None) or "parse error"
        return None, f"frontmatter is not valid YAML: {problem}{hint}", end + 1
    if meta is None:
        meta = {}
    if not isinstance(meta, dict):
        return None, "frontmatter must be a mapping of field: value", end + 1
    return meta, None, end + 1


def parse_blocks(lines, start):
    """Parse the ## Claims section of a paper note. Returns (blocks, problems)."""
    blocks, problems = [], []
    in_claims = in_comment = False
    current = None
    for i in range(start, len(lines)):
        line = lines[i].rstrip("\r\n")
        if in_comment:
            in_comment = "-->" not in line
            continue
        if line.lstrip().startswith("<!--"):
            in_comment = "-->" not in line
            continue
        if line.startswith("#"):
            in_claims = line.strip() == "## Claims"
            current = None
            continue
        if not in_claims or not line.strip():
            continue
        if line.startswith("- "):
            m = BLOCK_RE.match(line)
            current = Block(id=m["id"], text=m["text"], line=i) if m else None
            if current:
                blocks.append(current)
            else:
                problems.append(f"line {i + 1}: claim bullet has no block ID; end it with ^c<N>")
            continue
        m = FIELD_RE.match(line)
        if m and current is not None:
            _set_field(current, m["key"], m["value"], i, problems)
    seen = set()
    for block in blocks:
        if block.id in seen:
            problems.append(f"block ID ^{block.id} is used twice")
        seen.add(block.id)
        for name in BLOCK_FIELDS:
            if name not in block.fields_seen:
                problems.append(f"^{block.id}: missing '{name}'")
    return blocks, problems


def _set_field(block, key, value, index, problems):
    block.fields_seen.add(key)
    where = f"^{block.id}"
    if key == "page":
        if value.isdigit() and int(value) >= 1:
            block.page = int(value)
        else:
            problems.append(f"{where}: page must be a whole number from 1 (the PDF page index), got '{value}'")
    elif key == "quote":
        if len(value) >= 2 and value[0] == value[-1] == '"' and value[1:-1].strip():
            block.quote = value[1:-1]
        else:
            problems.append(f"{where}: quote must be non-empty text in double quotes")
    elif key == "quote_check":
        block.quote_check_line = index
        if value in QUOTE_STATES:
            block.quote_check = value
        else:
            problems.append(f"{where}: quote_check must be one of {', '.join(QUOTE_STATES)}")
    elif key == "reviewed":
        if value.lower() in ("true", "false"):
            block.reviewed = value.lower() == "true"
        else:
            problems.append(f"{where}: reviewed must be true or false")


def read_bib_keys(path):
    if not path.is_file():
        return set()
    text = path.read_text(encoding="utf-8", errors="replace")
    skip = {"comment", "string", "preamble"}
    return {m["key"] for m in BIB_RE.finditer(text) if m["kind"].lower() not in skip}


def load_vault(root):
    root = Path(root)
    kb = root / "kb"
    notes = []
    for path in sorted(kb.rglob("*.md")):
        parts = path.relative_to(kb).parts
        if len(parts) == 1 or any(p.startswith(".") or p in SKIP_DIRS for p in parts[:-1]):
            continue  # kb/README.md, kb/review-queue.md, templates, PDFs, Obsidian state
        note = Note(path=path, rel=path.relative_to(root).as_posix(), kb_rel="/".join(parts), lines=[])
        try:
            note.lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
        except UnicodeDecodeError:
            note.meta_error = "file is not valid UTF-8"
            notes.append(note)
            continue
        note.meta, note.meta_error, body = parse_frontmatter(note.lines)
        if note.type == "paper":
            note.blocks, note.block_problems = parse_blocks(note.lines, body)
        notes.append(note)
    return Vault(root=root, notes=notes, bib_keys=read_bib_keys(root / "thesis" / "references.bib"))
```

- [ ] **Step 4: Run the test to verify it passes**

Run: `python3 -m pytest tools/kb-lint/tests/test_model.py -q`
Expected: `8 passed`.

- [ ] **Step 5: Commit**

```bash
git add tools/kb-lint/model.py tools/kb-lint/requirements.txt tools/kb-lint/tests/helpers.py tools/kb-lint/tests/conftest.py tools/kb-lint/tests/test_model.py
git commit -m "kb-lint: vault model and fixture repository"
```

---

### Task 2: Templates and schema (checks 1 and 9)

**Files:**
- Modify (replace whole file): `kb/_templates/claim.md`, `kb/_templates/paper.md`, `kb/_templates/concept.md`, `kb/_templates/figure.md`
- Unchanged: `kb/_templates/decision.md` (its fields already match the schema)
- Create: `kb/_templates/method.md`, `kb/_templates/ref-thesis.md`, `kb/_templates/move.md`, `kb/_templates/concept-candidate.md`
- Create: `tools/kb-lint/schema.py`
- Test: `tools/kb-lint/tests/test_schema.py`

**Interfaces:**
- Consumes: `Issue`, `load_vault`, `parse_frontmatter` from Task 1; helpers `edit`, `write`.
- Produces: `SCHEMAS: dict[type, dict[key, validator]]`, `STATUSES`, `MAX_QUOTE_WORDS = 25`, `check_schema(vault) -> list[Issue]` (checks 1 and 9), `check_note(note) -> list[Issue]`.

- [ ] **Step 1: Write the failing test**

`tools/kb-lint/tests/test_schema.py`:

```python
from pathlib import Path

import pytest

from helpers import edit, write
from model import load_vault, parse_frontmatter
from schema import SCHEMAS, check_schema

TEMPLATES = Path(__file__).resolve().parents[3] / "kb" / "_templates"
CLAIM = "kb/claims/HDX-MS constrains ensemble reweighting.md"
PAPER = "kb/papers/@smith2020.md"


def messages(repo):
    return [(i.severity, i.check, i.path, i.message) for i in check_schema(load_vault(repo))]


def test_fixture_repo_passes(repo):
    assert messages(repo) == []


@pytest.mark.parametrize("name, kind", [
    ("paper.md", "paper"), ("claim.md", "claim"), ("concept.md", "concept"),
    ("method.md", "method"), ("figure.md", "figure"), ("decision.md", "decision"),
    ("ref-thesis.md", "ref-thesis"), ("move.md", "move"), ("concept-candidate.md", "concept-candidate"),
])
def test_templates_match_schema(name, kind):
    meta, error, _ = parse_frontmatter((TEMPLATES / name).read_text(encoding="utf-8").splitlines(keepends=True))
    assert error is None
    assert meta["type"] == kind
    assert set(meta) - {"type"} == set(SCHEMAS[kind])


@pytest.mark.parametrize("old, new, expected", [
    ("status: supported", "status: done", "'status' must be one of draft, supported, in-thesis"),
    ("origin: projects/1-ValDX/manuscript/main_omc.tex#sec:intro\n", "", "missing field 'origin'"),
    ('  - "[[@smith2020#^c1]]"', "  - [[smith2020#^c1]]", "unquoted wikilink"),
    ("needs_review: false\nreview_reason:", "needs_review: true\nreview_reason:", "review_reason is required"),
    ("code: []", "code: []\nmood: happy", "unexpected field 'mood'"),
])
def test_claim_schema_errors(repo, old, new, expected):
    edit(repo, CLAIM, old, new)
    assert any(expected in m[3] for m in messages(repo))


def test_unquoted_block_link_is_a_frontmatter_error(repo):
    edit(repo, CLAIM, '  - "[[@smith2020#^c1]]"', "  - [[@smith2020#^c1]]")
    assert any("quote wikilinks" in m[3] for m in messages(repo))


def test_wrong_type_for_folder(repo):
    edit(repo, CLAIM, "type: claim", "type: concept")
    assert any("notes in claims/ must have type claim" in m[3] for m in messages(repo))


def test_paper_name_must_match_citekey(repo):
    edit(repo, PAPER, "citekey: smith2020", "citekey: smith2021")
    assert any("note name must be @smith2021" in m[3] for m in messages(repo))


def test_paper_without_pdf_must_be_flagged(repo):
    edit(repo, "kb/papers/@jones2019.md", "needs_review: true", "needs_review: false")
    assert any("papers without a PDF must set needs_review" in m[3] for m in messages(repo))


def test_long_quote_is_rejected(repo):
    long_quote = " ".join(["word"] * 26)
    edit(repo, PAPER, '"reports on backbone amide protection factors"', f'"{long_quote}"')
    assert any("quote is 26 words" in m[3] for m in messages(repo))


def test_untyped_note_outside_chapters_and_inbox(repo):
    write(repo, "kb/concepts/Loose note.md", "Just text\n")
    write(repo, "kb/inbox/Idea.md", "Just text\n")
    found = messages(repo)
    assert any(m[2] == "kb/concepts/Loose note.md" and "missing frontmatter type" in m[3] for m in found)
    assert not any(m[2] == "kb/inbox/Idea.md" for m in found)


def test_duplicate_note_names(repo):
    write(repo, "kb/inbox/Protection factor.md", "Duplicate\n")
    assert any("also named 'Protection factor'" in m[3] for m in messages(repo))


def test_method_without_code_is_check_9(repo):
    path = repo / "kb/methods/Protection factor model (2-jaxENT).md"
    text = path.read_text(encoding="utf-8")
    start = text.index("code:")
    path.write_text(text[:start] + "code: []\n---\n", encoding="utf-8")
    assert ("error", 9) in {(m[0], m[1]) for m in messages(repo)}
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `python3 -m pytest tools/kb-lint/tests/test_schema.py -q`
Expected: collection error, `ModuleNotFoundError: No module named 'schema'`.

- [ ] **Step 3: Write the templates**

`kb/_templates/claim.md`:

````markdown
---
type: claim
chapter:               # e.g. 03-valdx
project:               # e.g. 1-ValDX; empty for introduction claims
basis: stated          # stated (shown by my results / a source) | inferred (my reading)
confidence: medium     # high | medium | low
status: draft          # draft | supported | in-thesis
origin:                # where the claim came from, e.g. projects/1-ValDX/manuscript/main_omc.tex#sec:intro
source_state: current  # current | outdated (e.g. JaxENT manuscript text)
needs_review: false
review_reason:         # one line; required when needs_review is true
figures: []            # figure IDs; each must exist as figures/<id>/
cites: []              # quoted block links, e.g. - "[[@smith2020#^c1]]"
code: []               # optional: <submodule>@<sha>:<file>#L<start>-<end>
---

<!-- Title of this note = the claim as one full sentence. -->

## Argument

## Caveats
````

`kb/_templates/paper.md`:

````markdown
---
type: paper
citekey:            # must match thesis/references.bib; note name = @<citekey>
year:
read: false
pdf:                # kb/_pdf/@<citekey>.pdf (gitignored); leave empty if unavailable
extraction: auto    # auto | manual | none
needs_review: false
review_reason:      # required when needs_review is true; papers without a PDF need both
---

## Main point

## Claims

<!-- One bullet per claim, ending in a block ID. page is the 1-based PDF page index.
- The claim paraphrased in one sentence. ^c1
  - page: 1
  - quote: "verbatim text, 25 words or fewer"
  - quote_check: unchecked
  - reviewed: false
quote_check is written only by tools/kb-lint; reviewed only by me. -->

## What I use from it

## Disagreements / limitations
````

`kb/_templates/concept.md`:

````markdown
---
type: concept
aliases: []
notation: []        # e.g. - {symbol: "P_i", meaning: "protection factor of residue i", units: null}
---

## Definition

## Why it matters here

## Related
````

`kb/_templates/figure.md`:

````markdown
---
type: figure
fig_id:             # matches figures/<fig-id>/
chapter:
source: script      # script | reused (from manuscript)
code: []            # optional: the script that makes it, <submodule>@<sha>:<file>#L<start>-<end>
---

## What it shows

## Claims it supports
````

`kb/_templates/method.md`:

````markdown
---
type: method
project:            # e.g. 2-jaxENT; methods may differ between projects
status: draft       # draft | supported | in-thesis
needs_review: false
review_reason:
code: []            # required: <submodule>@<sha>:<file>#L<start>-<end>
---

<!-- Note name: <Method name> (<project>). Link the concepts it implements in the text. -->

## What it does

## Equations

## Implementation notes
````

`kb/_templates/ref-thesis.md`:

````markdown
---
type: ref-thesis
thesis:             # crook | carlos | vost
generated: true
---

## Arc

## Stages

## Mine
````

`kb/_templates/move.md`:

````markdown
---
type: move
thesis:             # crook | carlos | vost
page:               # 1-based PDF page index
move_type:          # e.g. gap-framing, method-lineage, scope, contributions, outline
locator_quote:      # optional, 25 words or fewer, only for finding the passage; never reuse it
generated: true
needs_review: true
review_reason: Generated move; check the paraphrase against the page
---

## Paraphrase

## Mine
````

`kb/_templates/concept-candidate.md`:

````markdown
---
type: concept-candidate
thesis:             # crook | carlos | vost
aliases: []
generated: true
needs_review: true
review_reason: Candidate concept; link it to a shared concept or promote it
---

## Description

## Mine
````

Check that `kb/_templates/decision.md` still reads exactly as below. If it does not, replace it with this content:

````markdown
---
type: decision
date:               # YYYY-MM-DD
project:
status: active      # active | superseded
---

## Decision

## Alternatives considered

## Why

## Consequences
````

- [ ] **Step 4: Write `tools/kb-lint/schema.py`**

```python
"""Check 1 (frontmatter matches the schema for its type) and check 9 (methods need code)."""

import datetime
import re

from model import Issue

STATUSES = ("draft", "supported", "in-thesis")
MAX_QUOTE_WORDS = 25
ANY_TYPE_KEYS = {"tags", "aliases", "cssclasses"}  # Obsidian's own properties
UNTYPED_FOLDERS = {"chapters", "inbox"}
FOLDER_TYPES = {
    "papers": {"paper"},
    "claims": {"claim"},
    "concepts": {"concept"},
    "methods": {"method"},
    "decisions": {"decision"},
    "ref-theses": {"ref-thesis", "move", "concept-candidate"},
}


def one_of(*values):
    def check(value):
        if value not in values:
            return "must be one of " + ", ".join(values)
    return check


def text(value):
    if not isinstance(value, str) or not value.strip():
        return "must be non-empty text"


def optional_text(value):
    if value is not None and not isinstance(value, str):
        return "must be text or empty"


def boolean(value):
    if not isinstance(value, bool):
        return "must be true or false"


def whole_number(value):
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        return "must be a whole number from 1"


def optional_year(value):
    if value is not None and (isinstance(value, bool) or not isinstance(value, int)):
        return "must be a year such as 2020, or empty"


def text_list(value):
    if value is None:
        return None
    if not isinstance(value, list):
        return "must be a list"
    for item in value:
        if isinstance(item, list):
            return 'contains an unquoted wikilink; write it as "[[...]]"'
        if not isinstance(item, str):
            return "must be a list of text"


def iso_date(value):
    if isinstance(value, datetime.date):
        return None
    if isinstance(value, str) and re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        return None
    return "must be a date, YYYY-MM-DD"


def notation(value):
    if value is None:
        return None
    if not isinstance(value, list):
        return "must be a list of {symbol, meaning, units}"
    for entry in value:
        if (
            not isinstance(entry, dict)
            or text(entry.get("symbol"))
            or text(entry.get("meaning"))
            or optional_text(entry.get("units"))
        ):
            return "each entry needs text symbol and meaning, and optional units"


def locator_quote(value):
    if value is None:
        return None
    if not isinstance(value, str):
        return "must be text or empty"
    if len(value.split()) > MAX_QUOTE_WORDS:
        return f"must be {MAX_QUOTE_WORDS} words or fewer"


REVIEW = {"needs_review": boolean, "review_reason": optional_text}

# Every key listed here must be present; the validator decides which values are allowed.
SCHEMAS = {
    "paper": {
        "citekey": text, "year": optional_year, "read": boolean, "pdf": optional_text,
        "extraction": one_of("auto", "manual", "none"), **REVIEW,
    },
    "claim": {
        "chapter": optional_text, "project": optional_text,
        "basis": one_of("stated", "inferred"), "confidence": one_of("high", "medium", "low"),
        "status": one_of(*STATUSES), "origin": text, "source_state": one_of("current", "outdated"),
        **REVIEW, "figures": text_list, "cites": text_list, "code": text_list,
    },
    "concept": {"aliases": text_list, "notation": notation},
    "method": {"project": text, "status": one_of(*STATUSES), **REVIEW, "code": text_list},
    "figure": {
        "fig_id": text, "chapter": optional_text, "source": one_of("script", "reused"),
        "code": text_list,
    },
    "decision": {"date": iso_date, "project": optional_text, "status": one_of("active", "superseded")},
    "ref-thesis": {"thesis": text, "generated": boolean},
    "move": {
        "thesis": text, "page": whole_number, "move_type": text, "locator_quote": locator_quote,
        "generated": boolean, **REVIEW,
    },
    "concept-candidate": {"thesis": text, "aliases": text_list, "generated": boolean, **REVIEW},
}


def check_schema(vault):
    issues = []
    for name, notes in sorted(vault.duplicates().items()):
        for note in notes:
            issues.append(Issue("error", 1, note.rel, f"another note is also named '{name}'; links to it are ambiguous"))
    for note in vault.notes:
        issues += check_note(note)
    return issues


def check_note(note):
    def error(message, check=1):
        return Issue("error", check, note.rel, message)

    if note.meta_error:
        return [error(note.meta_error)]
    if not note.type:
        if note.folder in UNTYPED_FOLDERS:
            return []
        return [error("missing frontmatter type; start the note from a template in kb/_templates/")]
    kind = note.type
    if kind not in SCHEMAS:
        return [error(f"unknown type '{kind}'")]
    issues = []
    allowed = FOLDER_TYPES.get(note.folder)
    if allowed and kind not in allowed:
        issues.append(error(f"notes in {note.folder}/ must have type {' or '.join(sorted(allowed))}, not '{kind}'"))
    schema = SCHEMAS[kind]
    for key, validate in schema.items():
        if key not in note.meta:
            issues.append(error(f"missing field '{key}'"))
            continue
        problem = validate(note.meta[key])
        if problem:
            issues.append(error(f"'{key}' {problem}"))
    for key in note.meta:
        if key != "type" and key not in schema and key not in ANY_TYPE_KEYS:
            issues.append(Issue("warning", 1, note.rel, f"unexpected field '{key}'"))
    reason = note.meta.get("review_reason")
    if note.meta.get("needs_review") is True and not (isinstance(reason, str) and reason.strip()):
        issues.append(error("review_reason is required when needs_review is true"))
    if kind == "paper":
        issues += _check_paper(note, error)
    if kind == "method" and not note.meta.get("code"):
        issues.append(error("method notes need at least one code entry (<submodule>@<sha>:<file>#L<start>-<end>)", check=9))
    return issues


def _check_paper(note, error):
    meta = note.meta
    issues = []
    if isinstance(meta.get("citekey"), str) and note.name != "@" + meta["citekey"]:
        issues.append(error(f"note name must be @{meta['citekey']} to match its citekey"))
    if (meta.get("extraction") == "none" or not meta.get("pdf")) and meta.get("needs_review") is not True:
        issues.append(error("papers without a PDF must set needs_review: true with a review_reason"))
    issues += [error(problem) for problem in note.block_problems]
    for block in note.blocks:
        words = len(block.quote.split()) if block.quote else 0
        if words > MAX_QUOTE_WORDS:
            issues.append(error(f"^{block.id}: quote is {words} words; keep it to {MAX_QUOTE_WORDS} or fewer"))
    return issues
```

- [ ] **Step 5: Run the tests to verify they pass**

Run: `python3 -m pytest tools/kb-lint/tests/test_schema.py tools/kb-lint/tests/test_model.py -q`
Expected: `31 passed`.

- [ ] **Step 6: Commit**

```bash
git add kb/_templates tools/kb-lint/schema.py tools/kb-lint/tests/test_schema.py
git commit -m "kb-lint: templates and frontmatter schema (checks 1, 9)"
```

---

### Task 3: Links (checks 3, 4 and 5)

**Files:**
- Create: `tools/kb-lint/links.py`
- Test: `tools/kb-lint/tests/test_links.py`

**Interfaces:**
- Consumes: `Issue`, `load_vault`, `parse_wikilink`, `Vault.find`, `Note.block`, `Note.in_ref_theses`; helper `edit`.
- Produces: `check_links(vault) -> list[Issue]`.

- [ ] **Step 1: Write the failing test**

`tools/kb-lint/tests/test_links.py`:

```python
import pytest

from helpers import edit
from links import check_links
from model import load_vault

CLAIM = "kb/claims/HDX-MS constrains ensemble reweighting.md"


def messages(repo):
    return [(i.check, i.message) for i in check_links(load_vault(repo))]


def test_fixture_repo_passes(repo):
    assert messages(repo) == []


@pytest.mark.parametrize("old, new, check, expected", [
    ("  - fig-hdx-uptake", "  - fig-missing", 3, "figure 'fig-missing' not found under figures/"),
    ('"[[@smith2020#^c1]]"', '"[[@nobody2000#^c1]]"', 4, "no single note has that name"),
    ('"[[@smith2020#^c1]]"', '"[[@smith2020#^c7]]"', 4, "block ^c7 not found in @smith2020"),
    ('"[[@smith2020#^c1]]"', '"[[@smith2020]]"', 4, "without a block ID"),
    ('"[[@smith2020#^c1]]"', '"[[Protection factor#^c1]]"', 4, "which is not a paper note"),
    ('"[[@smith2020#^c1]]"', '"@smith2020"', 4, "is not a wikilink"),
    ('"[[@smith2020#^c1]]"', '"[[Gap framing]]"', 5, "example theses are never evidence"),
])
def test_claim_link_errors(repo, old, new, check, expected):
    edit(repo, CLAIM, old, new)
    assert any(c == check and expected in m for c, m in messages(repo))


def test_citekey_missing_from_bib(repo):
    edit(repo, "thesis/references.bib", "@book{jones2019,", "@book{jones2018,")
    assert (4, "citekey 'jones2019' is not in thesis/references.bib") in messages(repo)


def test_figure_note_id_must_exist(repo):
    edit(repo, "kb/figures/fig-hdx-uptake.md", "fig_id: fig-hdx-uptake", "fig_id: fig-gone")
    assert (3, "figure 'fig-gone' not found under figures/") in messages(repo)
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `python3 -m pytest tools/kb-lint/tests/test_links.py -q`
Expected: collection error, `ModuleNotFoundError: No module named 'links'`.

- [ ] **Step 3: Write `tools/kb-lint/links.py`**

```python
"""Checks 3 (figure IDs exist), 4 (cites and citekeys resolve) and 5 (example theses are never cited)."""

from model import Issue, parse_wikilink


def check_links(vault):
    issues = []
    for note in vault.notes:
        meta = note.meta or {}

        def error(check, message):
            issues.append(Issue("error", check, note.rel, message))

        if note.type == "claim":
            for fig_id in _strings(meta.get("figures")):
                if not (vault.root / "figures" / fig_id).is_dir():
                    error(3, f"figure '{fig_id}' not found under figures/")
            for entry in _strings(meta.get("cites")):
                _check_cite(vault, note, entry, error)
        if note.type == "figure" and isinstance(meta.get("fig_id"), str):
            if not (vault.root / "figures" / meta["fig_id"]).is_dir():
                error(3, f"figure '{meta['fig_id']}' not found under figures/")
        if note.type == "paper" and isinstance(meta.get("citekey"), str):
            if meta["citekey"] not in vault.bib_keys:
                error(4, f"citekey '{meta['citekey']}' is not in thesis/references.bib")
    return issues


def _check_cite(vault, note, entry, error):
    link = parse_wikilink(entry)
    if not link:
        error(4, f"cites entry '{entry}' is not a wikilink like [[@key#^c1]]")
        return
    target_name, block_id = link
    target = vault.find(target_name)
    if target is None:
        error(4, f"cites [[{target_name}]] but no single note has that name")
    elif target.in_ref_theses and not note.in_ref_theses:
        error(5, f"cites example-thesis note [[{target_name}]]; example theses are never evidence, cite the primary paper")
    elif target.type != "paper":
        error(4, f"cites [[{target_name}]], which is not a paper note")
    elif block_id is None:
        error(4, f"cites [[{target_name}]] without a block ID; link one claim, e.g. [[{target_name}#^c1]]")
    elif target.block(block_id) is None:
        error(4, f"block ^{block_id} not found in {target_name}")


def _strings(value):
    return [item for item in value if isinstance(item, str)] if isinstance(value, list) else []
```

- [ ] **Step 4: Run the test to verify it passes**

Run: `python3 -m pytest tools/kb-lint/tests/test_links.py -q`
Expected: `10 passed`.

- [ ] **Step 5: Commit**

```bash
git add tools/kb-lint/links.py tools/kb-lint/tests/test_links.py
git commit -m "kb-lint: figure, cite and example-thesis link checks (3, 4, 5)"
```

---

### Task 4: Quote check against the PDF (check 2)

**Files:**
- Create: `tools/kb-lint/quotes.py`
- Test: `tools/kb-lint/tests/test_quotes.py`

**Interfaces:**
- Consumes: `Issue`, `load_vault`, `Vault.citations`, `Block` fields from Task 1; helper `edit`.
- Produces: `normalise(text) -> str`; `PdfText(cache_dir)` with `.pages(pdf: Path) -> list[str]`; `check_quotes(vault, pdf_text) -> list[Issue]`, which sets `Block.computed` to `"pass"` or `"fail"` for each quote it can check; `write_quote_checks(vault) -> list[Path]`.

Requires `pdftotext` on `PATH` (`brew install poppler`; `/opt/homebrew/bin/pdftotext` is already present on the author's machine).

- [ ] **Step 1: Write the failing test**

`tools/kb-lint/tests/test_quotes.py`:

```python
from helpers import edit
from model import load_vault
from quotes import PdfText, check_quotes, normalise, write_quote_checks

PAPER = "kb/papers/@smith2020.md"


def run_quotes(repo, tmp_path):
    vault = load_vault(repo)
    issues = check_quotes(vault, PdfText(tmp_path / "cache"))
    return vault, [(i.severity, i.check, i.message) for i in issues]


def test_normalise_handles_ligatures_hyphens_quotes_and_spacing():
    assert normalise("ﬁeld  pro-\ntection “x”") == normalise('field protection "x"')
    assert normalise("force-field") == normalise("force‐\nfield")
    assert normalise("soft­hyphen") == "softhyphen"


def test_pdf_pages_split_and_cache(repo, tmp_path):
    pdf_text = PdfText(tmp_path / "cache")
    pages = pdf_text.pages(repo / "kb/_pdf/@smith2020.pdf")
    assert len(pages) == 3
    assert "protection factors" in pages[0]
    assert len(list((tmp_path / "cache").glob("*.txt"))) == 1


def test_quotes_found_including_across_a_page_break(repo, tmp_path):
    vault, issues = run_quotes(repo, tmp_path)
    assert issues == []
    assert [b.computed for b in vault.find("@smith2020").blocks] == ["pass", "pass"]
    assert [b.computed for b in vault.find("@jones2019").blocks] == [None]  # no PDF, not checked


def test_missing_quote_in_cited_block_is_an_error(repo, tmp_path):
    edit(repo, PAPER, '"reports on backbone amide protection factors"', '"words the paper never said"')
    _, issues = run_quotes(repo, tmp_path)
    assert ("error", 2, "^c1: quote not found on PDF page 1") in issues


def test_missing_quote_in_uncited_unreviewed_block_is_a_warning(repo, tmp_path):
    edit(repo, PAPER, '"The effect carries over to the next page"', '"invented text"')
    _, issues = run_quotes(repo, tmp_path)
    assert ("warning", 2, "^c2: quote not found on PDF page 2") in issues


def test_page_outside_pdf(repo, tmp_path):
    edit(repo, PAPER, "  - page: 2", "  - page: 9")
    _, issues = run_quotes(repo, tmp_path)
    assert ("warning", 2, "^c2: page 9 is outside the PDF (3 pages)") in issues


def test_pdf_not_present_locally_is_a_warning_and_keeps_recorded_state(repo, tmp_path):
    (repo / "kb/_pdf/@smith2020.pdf").unlink()
    vault, issues = run_quotes(repo, tmp_path)
    assert issues == [("warning", 2, "PDF kb/_pdf/@smith2020.pdf not found locally; quotes not checked")]
    assert [b.computed for b in vault.find("@smith2020").blocks] == [None, None]


def test_write_changes_only_quote_check_lines(repo, tmp_path):
    before = (repo / PAPER).read_text(encoding="utf-8")
    vault, _ = run_quotes(repo, tmp_path)
    assert write_quote_checks(vault) == [repo / PAPER]
    after = (repo / PAPER).read_text(encoding="utf-8")
    assert after == before.replace("quote_check: unchecked", "quote_check: pass")
    vault, _ = run_quotes(repo, tmp_path)
    assert write_quote_checks(vault) == []  # nothing left to change
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `python3 -m pytest tools/kb-lint/tests/test_quotes.py -q`
Expected: collection error, `ModuleNotFoundError: No module named 'quotes'`.

- [ ] **Step 3: Write `tools/kb-lint/quotes.py`**

```python
"""Check 2: each paper claim's quote appears on its cited PDF page."""

import hashlib
import re
import subprocess
import unicodedata

from model import Issue

QUOTE_CHARS = str.maketrans({"‘": "'", "’": "'", "“": '"', "”": '"'})
LINE_BREAK_HYPHEN = re.compile("[-‐­]\\s*\\n\\s*")
DASHES = re.compile("[-‐‒–—­]")


def normalise(text):
    """Make PDF text and typed quotes comparable: ligatures, hyphenation, quotes, dashes, case, spacing."""
    text = unicodedata.normalize("NFKC", text)
    text = LINE_BREAK_HYPHEN.sub("", text)
    text = text.translate(QUOTE_CHARS)
    text = DASHES.sub("", text)
    return " ".join(text.split()).lower()


class PdfText:
    """Per-page PDF text from pdftotext, cached by the PDF's SHA-256."""

    def __init__(self, cache_dir):
        self.cache_dir = cache_dir

    def pages(self, pdf):
        digest = hashlib.sha256(pdf.read_bytes()).hexdigest()
        cached = self.cache_dir / (digest + ".txt")
        if cached.is_file():
            text = cached.read_text(encoding="utf-8")
        else:
            # Without -layout, pdftotext keeps two-column text in reading order.
            text = subprocess.run(
                ["pdftotext", "-q", "-enc", "UTF-8", str(pdf), "-"],
                capture_output=True, text=True, check=True,
            ).stdout
            self.cache_dir.mkdir(parents=True, exist_ok=True)
            cached.write_text(text, encoding="utf-8")
        pages = text.split("\f")  # pdftotext ends every page with a form feed
        return pages[:-1] if text.endswith("\f") else pages


def check_quotes(vault, pdf_text):
    """Set Block.computed for every quote it can check and report failures."""
    issues = []
    cited = vault.citations()
    for note in vault.notes:
        meta = note.meta or {}
        if note.type != "paper" or not note.blocks:
            continue
        if meta.get("extraction") == "none" or not isinstance(meta.get("pdf"), str) or not meta["pdf"]:
            continue
        pdf = vault.root / meta["pdf"]
        if not pdf.is_file():
            issues.append(Issue("warning", 2, note.rel, f"PDF {meta['pdf']} not found locally; quotes not checked"))
            continue
        try:
            pages = pdf_text.pages(pdf)
        except FileNotFoundError:
            issues.append(Issue("error", 2, note.rel, "pdftotext not found; install Poppler (brew install poppler)"))
            continue
        except subprocess.CalledProcessError:
            issues.append(Issue("error", 2, note.rel, f"pdftotext could not read {meta['pdf']}"))
            continue
        for block in note.blocks:
            if block.page is None or block.quote is None:
                continue  # reported by check 1
            if block.page > len(pages):
                found, detail = False, f"page {block.page} is outside the PDF ({len(pages)} pages)"
            else:
                # A quote may run onto the next page.
                window = pages[block.page - 1] + "\n" + (pages[block.page] if block.page < len(pages) else "")
                found = normalise(block.quote) in normalise(window)
                detail = f"quote not found on PDF page {block.page}"
            block.computed = "pass" if found else "fail"
            if not found:
                serious = block.reviewed or (note.name, block.id) in cited
                issues.append(Issue("error" if serious else "warning", 2, note.rel, f"^{block.id}: {detail}"))
    return issues


def write_quote_checks(vault):
    """Write each computed result into its quote_check line. Returns the paths changed."""
    changed = []
    for note in vault.notes:
        edits = [
            b for b in note.blocks
            if b.computed and b.computed != b.quote_check and b.quote_check_line is not None
        ]
        for block in edits:
            line = note.lines[block.quote_check_line]
            note.lines[block.quote_check_line] = re.sub(
                r"(quote_check:\s*)\S*", lambda m: m.group(1) + block.computed, line, count=1
            )
            block.quote_check = block.computed
        if edits:
            note.path.write_text("".join(note.lines), encoding="utf-8")
            changed.append(note.path)
    return changed
```

- [ ] **Step 4: Run the test to verify it passes**

Run: `python3 -m pytest tools/kb-lint/tests/test_quotes.py -q`
Expected: `8 passed`.

- [ ] **Step 5: Commit**

```bash
git add tools/kb-lint/quotes.py tools/kb-lint/tests/test_quotes.py
git commit -m "kb-lint: quote check against PDF pages (check 2)"
```

---

### Task 5: Code references (checks 7 and 8)

**Files:**
- Create: `tools/kb-lint/coderefs.py`
- Test: `tools/kb-lint/tests/test_coderefs.py`

**Interfaces:**
- Consumes: `Issue`, `load_vault`; helpers `MODEL_PY`, `commit_file`, `git`, `pin`.
- Produces: `CODE_REF` (regex), `check_code_refs(vault) -> list[Issue]`, `check_entry(root: Path, rel: str, entry: str) -> list[Issue]`, `pinned_commit(root, repo_rel) -> str | None`.

- [ ] **Step 1: Write the failing test**

`tools/kb-lint/tests/test_coderefs.py`:

```python
import shutil

import pytest

from coderefs import check_code_refs, check_entry
from helpers import MODEL_PY, commit_file, git, pin
from model import load_vault


def entry_messages(repo, entry):
    return [(i.severity, i.check, i.message) for i in check_entry(repo, "kb/methods/x.md", entry)]


def head(repo):
    return git(repo / "projects/demo/code", "rev-parse", "HEAD")


def test_fixture_repo_passes(repo):
    assert check_code_refs(load_vault(repo)) == []


def test_full_and_short_sha_and_single_line(repo):
    sha = head(repo)
    assert entry_messages(repo, f"projects/demo/code@{sha}:model.py#L1-L2") == []
    assert entry_messages(repo, f"projects/demo/code@{sha[:7]}:model.py#L2") == []


@pytest.mark.parametrize("entry_template, expected", [
    ("projects/demo/code:model.py#L1-2", "is not of the form"),
    ("projects/demo/code@{sha}:model.py", "is not of the form"),
    ("projects/demo/code@abcdef1:model.py#L1-2", "commit abcdef1 not found in projects/demo/code"),
    ("projects/demo/code@{sha}:missing.py#L1-2", "missing.py does not exist in projects/demo/code"),
    ("projects/demo/code@{sha}:model.py#L2-9", "lines 2-9 are out of range; model.py has 3 lines"),
    ("projects/demo/code@{sha}:model.py#L3-1", "lines 3-1 are out of range"),
    ("../outside@{sha}:model.py#L1-2", "points outside the repository"),
])
def test_bad_entries_are_check_7_errors(repo, entry_template, expected):
    found = entry_messages(repo, entry_template.format(sha=head(repo)[:7]))
    assert len(found) == 1
    severity, check, message = found[0]
    assert (severity, check) == ("error", 7)
    assert expected in message


def test_submodule_not_checked_out_is_a_warning(repo):
    sha = head(repo)
    shutil.rmtree(repo / "projects/demo/code")
    (repo / "projects/demo/code").mkdir()
    [(severity, check, message)] = entry_messages(repo, f"projects/demo/code@{sha[:7]}:model.py#L1-2")
    assert (severity, check) == ("warning", 7)
    assert "git submodule update --init" in message


def test_drift_after_submodule_bump_is_check_8_warning(repo):
    old = head(repo)
    code = repo / "projects/demo/code"
    new = commit_file(code, "model.py", MODEL_PY + "def extra():\n    pass\n")
    pin(repo, "projects/demo/code", new)
    [(severity, check, message)] = entry_messages(repo, f"projects/demo/code@{old[:7]}:model.py#L1-2")
    assert (severity, check) == ("warning", 8)
    assert f"pinned commit {new[:7]}" in message


def test_bump_that_does_not_touch_the_file_is_not_drift(repo):
    old = head(repo)
    code = repo / "projects/demo/code"
    new = commit_file(code, "other.py", "x = 1\n")
    pin(repo, "projects/demo/code", new)
    assert entry_messages(repo, f"projects/demo/code@{old[:7]}:model.py#L1-2") == []
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `python3 -m pytest tools/kb-lint/tests/test_coderefs.py -q`
Expected: collection error, `ModuleNotFoundError: No module named 'coderefs'`.

- [ ] **Step 3: Write `tools/kb-lint/coderefs.py`**

```python
"""Checks 7 (code references resolve) and 8 (code drifted since the recorded commit)."""

import re
import subprocess

from model import Issue

CODE_REF = re.compile(
    r"^(?P<repo>[^@\s]+)@(?P<sha>[0-9a-f]{7,40}):(?P<path>[^#\s]+)#L(?P<start>\d+)(?:-L?(?P<end>\d+))?$"
)
FORMAT = "<submodule>@<sha>:<file>#L<start>-<end>"


def git(repo, *args):
    return subprocess.run(
        ["git", "-C", str(repo), *args], capture_output=True, text=True, errors="replace"
    )


def pinned_commit(root, repo_rel):
    """The commit the superproject pins for this submodule, else the one checked out."""
    tree = git(root, "ls-tree", "HEAD", "--", repo_rel)
    m = re.match(r"160000 commit ([0-9a-f]{40})\t", tree.stdout)
    if m:
        return m.group(1)
    head = git(root / repo_rel, "rev-parse", "HEAD")
    return head.stdout.strip() if head.returncode == 0 else None


def check_code_refs(vault):
    issues = []
    for note in vault.notes:
        entries = (note.meta or {}).get("code")
        if not isinstance(entries, list):
            continue
        for entry in entries:
            if isinstance(entry, str):
                issues += check_entry(vault.root, note.rel, entry)
    return issues


def check_entry(root, rel, entry):
    def issue(severity, check, message):
        return [Issue(severity, check, rel, message)]

    m = CODE_REF.match(entry.strip())
    if not m:
        return issue("error", 7, f"code entry '{entry}' is not of the form {FORMAT}")
    repo_rel, sha, path = m["repo"].rstrip("/"), m["sha"], m["path"]
    repo = (root / repo_rel).resolve()
    if not repo.is_relative_to(root.resolve()):
        return issue("error", 7, f"code entry '{entry}' points outside the repository")
    if not (repo / ".git").exists():
        return issue("warning", 7, f"{repo_rel} is not checked out; run git submodule update --init to check '{entry}'")
    resolved = git(repo, "rev-parse", "--verify", "--quiet", sha + "^{commit}")
    if resolved.returncode != 0:
        return issue("error", 7, f"commit {sha} not found in {repo_rel} (try git -C {repo_rel} fetch)")
    full_sha = resolved.stdout.strip()
    blob = git(repo, "show", f"{full_sha}:{path}")
    if blob.returncode != 0:
        return issue("error", 7, f"{path} does not exist in {repo_rel} at {sha}")
    start = int(m["start"])
    end = int(m["end"] or start)
    count = len(blob.stdout.splitlines())
    if not 1 <= start <= end <= count:
        return issue("error", 7, f"lines {start}-{end} are out of range; {path} has {count} lines at {sha}")
    pinned = pinned_commit(root, repo_rel)
    if pinned and pinned != full_sha:
        if git(repo, "diff", "--quiet", full_sha, pinned, "--", path).returncode == 1:
            return issue("warning", 8, f"{path} changed between {sha} and the pinned commit {pinned[:7]}; check the note still matches the code")
    return []
```

- [ ] **Step 4: Run the test to verify it passes**

Run: `python3 -m pytest tools/kb-lint/tests/test_coderefs.py -q`
Expected: `12 passed`.

- [ ] **Step 5: Commit**

```bash
git add tools/kb-lint/coderefs.py tools/kb-lint/tests/test_coderefs.py
git commit -m "kb-lint: code reference and drift checks (7, 8)"
```

---

### Task 6: Status ladder (check 6)

**Files:**
- Create: `tools/kb-lint/ladder.py`
- Test: `tools/kb-lint/tests/test_ladder.py`

**Interfaces:**
- Consumes: `Issue`, `load_vault`, `parse_wikilink`, `Block.effective_quote_check`; `PdfText`, `check_quotes` from Task 4 (the ladder reads this run's quote results); helper `edit`.
- Produces: `check_ladder(vault) -> list[Issue]`. It must run **after** `check_quotes` on the same `Vault` object.

- [ ] **Step 1: Write the failing test**

`tools/kb-lint/tests/test_ladder.py`:

```python
import pytest

from helpers import edit
from ladder import check_ladder
from model import load_vault
from quotes import PdfText, check_quotes

CLAIM = "kb/claims/HDX-MS constrains ensemble reweighting.md"
DRAFT = "kb/claims/Ensembles explain exchange.md"


def messages(repo, tmp_path, read_pdfs=True):
    vault = load_vault(repo)
    if read_pdfs:
        check_quotes(vault, PdfText(tmp_path / "cache"))
    return [i.message for i in check_ladder(vault) if i.check == 6 and i.severity == "error"]


def test_supported_claim_with_passing_quote_and_figure_is_fine(repo, tmp_path):
    assert messages(repo, tmp_path) == []


def test_unchecked_quote_cannot_support_a_claim(repo, tmp_path):
    # Without reading PDFs the recorded state (unchecked) is all the ladder can see.
    found = messages(repo, tmp_path, read_pdfs=False)
    assert found == ['status is supported but cited claim [[@smith2020#^c1]] has quote_check: unchecked']


def test_failed_quote_cannot_support_a_claim(repo, tmp_path):
    edit(repo, "kb/papers/@smith2020.md", '"reports on backbone amide protection factors"', '"never said"')
    assert any("has quote_check: fail" in m for m in messages(repo, tmp_path))


@pytest.mark.parametrize("old, new, expected", [
    ("figures:\n  - fig-hdx-uptake\ncites:\n  - \"[[@smith2020#^c1]]\"", "figures: []\ncites: []", "has no figures or cites"),
    ("needs_review: false\nreview_reason:", "needs_review: true\nreview_reason: check", "needs_review is true"),
    ("figures:\n  - fig-hdx-uptake\n", "figures: []\n", None),
])
def test_supported_claim_rules(repo, tmp_path, old, new, expected):
    edit(repo, CLAIM, old, new)
    found = messages(repo, tmp_path)
    if expected is None:
        assert found == []  # a passing cite alone is enough evidence
    else:
        assert any(expected in m for m in found)


def test_outdated_source_needs_a_figure(repo, tmp_path):
    edit(repo, CLAIM, "source_state: current", "source_state: outdated")
    assert messages(repo, tmp_path) == []  # has a figure
    edit(repo, CLAIM, "figures:\n  - fig-hdx-uptake\n", "figures: []\n")
    assert any("outdated source text cannot support a claim" in m for m in messages(repo, tmp_path))


def test_claim_citing_a_paper_without_pdf_cannot_be_supported(repo, tmp_path):
    edit(repo, DRAFT, "status: draft", "status: in-thesis")
    edit(repo, DRAFT, "needs_review: true\nreview_reason: Ambiguous wording in the confirmation report", "needs_review: false\nreview_reason:")
    assert messages(repo, tmp_path) == ["status is in-thesis but cited claim [[@jones2019#^c1]] has quote_check: unchecked"]
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `python3 -m pytest tools/kb-lint/tests/test_ladder.py -q`
Expected: collection error, `ModuleNotFoundError: No module named 'ladder'`.

- [ ] **Step 3: Write `tools/kb-lint/ladder.py`**

```python
"""Check 6: a claim only climbs the status ladder (draft -> supported -> in-thesis) on checked evidence."""

from model import Issue, parse_wikilink

EVIDENCE_STATUSES = {"supported", "in-thesis"}


def check_ladder(vault):
    issues = []
    for note in vault.notes:
        meta = note.meta or {}
        status = meta.get("status")
        if note.type != "claim" or status not in EVIDENCE_STATUSES:
            continue

        def error(message):
            issues.append(Issue("error", 6, note.rel, f"status is {status} but {message}"))

        figures = [f for f in meta.get("figures") or [] if isinstance(f, str)]
        cites = [c for c in meta.get("cites") or [] if isinstance(c, str)]
        if not figures and not cites:
            error("the claim has no figures or cites")
        if meta.get("needs_review") is True:
            error("needs_review is true")
        if meta.get("source_state") == "outdated" and not figures:
            error("outdated source text cannot support a claim on its own; add a current figure ID or keep status: draft")
        for entry in cites:
            link = parse_wikilink(entry)
            target = vault.find(link[0]) if link and link[1] else None
            block = target.block(link[1]) if target is not None and target.type == "paper" else None
            if block is not None and block.effective_quote_check != "pass":
                error(f"cited claim {entry} has quote_check: {block.effective_quote_check}")
    return issues
```

- [ ] **Step 4: Run the test to verify it passes**

Run: `python3 -m pytest tools/kb-lint/tests/test_ladder.py -q`
Expected: `8 passed`.

- [ ] **Step 5: Commit**

```bash
git add tools/kb-lint/ladder.py tools/kb-lint/tests/test_ladder.py
git commit -m "kb-lint: status ladder (check 6)"
```

---

### Task 7: CLI, review queue, end-to-end acceptance and documentation

**Files:**
- Create: `tools/kb-lint/review_queue.py`
- Create: `tools/kb-lint/lint.py`
- Create: `tools/kb-lint/README.md`
- Modify: `kb/README.md` (folders table and rules)
- Modify: `.gitignore` (Obsidian section, around line 239)
- Test: `tools/kb-lint/tests/test_lint.py`

**Interfaces:**
- Consumes: every `check_*` function above, plus `PdfText`, `write_quote_checks`, `load_vault`.
- Produces: `render_queue(vault) -> str`; `run(root, write=False, cache_dir=None) -> Result` with `.issues .written .errors .warnings`; `main(argv=None) -> int`. Spec step 2 (the ValDX seed) runs `python3 tools/kb-lint/lint.py --write`.

- [ ] **Step 1: Write the failing test**

`tools/kb-lint/tests/test_lint.py` holds the spec's acceptance criterion for step 1: the fixture vault passes, and one broken fixture per check fails with the expected message.

```python
"""End-to-end: the fixture vault passes and one broken fixture per check fails as expected."""

import os
from pathlib import Path
import subprocess
import sys

import pytest

from helpers import edit, write
from lint import run

LINT = Path(__file__).resolve().parents[1] / "lint.py"
CLAIM = "kb/claims/HDX-MS constrains ensemble reweighting.md"
PAPER = "kb/papers/@smith2020.md"
METHOD = "kb/methods/Protection factor model (2-jaxENT).md"


def test_fixture_repo_passes_with_no_warnings(repo):
    result = run(repo)
    assert [str(i) for i in result.issues] == []


def break_method_code(repo):
    path = repo / METHOD
    text = path.read_text(encoding="utf-8")
    path.write_text(text[: text.index("code:")] + "code: []\n---\n", encoding="utf-8")


def break_code_line_range(repo):
    edit(repo, METHOD, "model.py#L1-2", "model.py#L1-40")


def bump_submodule(repo):
    from helpers import MODEL_PY, commit_file, pin
    code = repo / "projects/demo/code"
    pin(repo, "projects/demo/code", commit_file(code, "model.py", MODEL_PY + "# changed\n"))


BROKEN = [
    (1, "error", CLAIM, lambda r: edit(r, CLAIM, "status: supported", "status: done"), "'status' must be one of"),
    (2, "error", PAPER, lambda r: edit(r, PAPER, '"reports on backbone amide protection factors"', '"never said"'), "^c1: quote not found on PDF page 1"),
    (3, "error", CLAIM, lambda r: edit(r, CLAIM, "  - fig-hdx-uptake", "  - fig-missing"), "figure 'fig-missing' not found"),
    (4, "error", CLAIM, lambda r: edit(r, CLAIM, "#^c1]]", "#^c7]]"), "block ^c7 not found in @smith2020"),
    (5, "error", CLAIM, lambda r: edit(r, CLAIM, '"[[@smith2020#^c1]]"', '"[[Gap framing]]"'), "example theses are never evidence"),
    (6, "error", CLAIM, lambda r: edit(r, CLAIM, "needs_review: false\nreview_reason:", "needs_review: true\nreview_reason: check"), "status is supported but needs_review is true"),
    (7, "error", METHOD, break_code_line_range, "lines 1-40 are out of range"),
    (8, "warning", METHOD, bump_submodule, "changed between"),
    (9, "error", METHOD, break_method_code, "method notes need at least one code entry"),
]


@pytest.mark.parametrize("check, severity, rel, breaker, expected", BROKEN, ids=[f"check-{b[0]}" for b in BROKEN])
def test_each_check_catches_its_broken_fixture(repo, check, severity, rel, breaker, expected):
    breaker(repo)
    result = run(repo)
    matches = [i for i in result.issues if i.check == check and i.path == rel and expected in i.message]
    assert matches, [str(i) for i in result.issues]
    assert matches[0].severity == severity


def test_read_only_run_writes_nothing(repo):
    before = {p: p.read_bytes() for p in (repo / "kb").rglob("*.md")}
    run(repo)
    after = {p: p.read_bytes() for p in (repo / "kb").rglob("*.md")}
    assert after == before
    assert not (repo / "kb/review-queue.md").exists()


def test_write_records_quote_checks_and_builds_review_queue(repo):
    result = run(repo, write=True)
    assert {p.relative_to(repo).as_posix() for p in result.written} == {PAPER, "kb/review-queue.md"}
    assert "quote_check: unchecked" not in (repo / PAPER).read_text(encoding="utf-8")
    queue = (repo / "kb/review-queue.md").read_text(encoding="utf-8")
    assert "## Ambiguous wording in the confirmation report\n\n- [[Ensembles explain exchange]]" in queue
    assert "## No PDF available\n\n- [[@jones2019]]" in queue
    assert "Do not edit by hand" in queue
    assert run(repo, write=True).written == []  # second run is a no-op


def test_review_queue_lists_failed_quotes(repo):
    edit(repo, PAPER, '"The effect carries over to the next page"', '"invented text"')
    run(repo, write=True)
    queue = (repo / "kb/review-queue.md").read_text(encoding="utf-8")
    assert "## Quote not found in PDF\n\n- [[@smith2020#^c2]] (PDF page 2)" in queue


def test_cli_exit_codes(repo):
    def cli(*args):
        return subprocess.run([sys.executable, str(LINT), "--root", str(repo), *args], capture_output=True, text=True)

    ok = cli()
    assert ok.returncode == 0, ok.stdout + ok.stderr
    assert ok.stdout.strip().endswith("0 errors, 0 warnings")
    edit(repo, CLAIM, "status: supported", "status: done")
    bad = cli()
    assert bad.returncode == 1
    assert "ERROR [check 1] kb/claims/HDX-MS constrains ensemble reweighting.md: 'status' must be one of" in bad.stdout
    assert cli("--root", str(repo / "nowhere")).returncode == 2
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `python3 -m pytest tools/kb-lint/tests/test_lint.py -q`
Expected: collection error, `ModuleNotFoundError: No module named 'lint'`.

- [ ] **Step 3: Write `tools/kb-lint/review_queue.py`**

```python
"""Render kb/review-queue.md: every note flagged needs_review, grouped by reason."""

HEADER = (
    "<!-- Generated by tools/kb-lint/lint.py --write. Do not edit by hand. -->\n"
    "# Review queue\n"
)


def render_queue(vault):
    groups = {}
    for note in vault.notes:
        meta = note.meta or {}
        if meta.get("needs_review") is True:
            reason = meta.get("review_reason") if isinstance(meta.get("review_reason"), str) else ""
            groups.setdefault(reason.strip() or "(no reason given)", []).append(
                f"- [[{note.name}]] (`{note.kb_rel}`)"
            )
    failures = [
        f"- [[{note.name}#^{block.id}]] (PDF page {block.page})"
        for note in vault.notes
        for block in note.blocks
        if block.effective_quote_check == "fail"
    ]
    parts = [HEADER]
    for reason in sorted(groups):
        parts.append(f"\n## {reason}\n\n" + "\n".join(sorted(groups[reason])) + "\n")
    if failures:
        parts.append("\n## Quote not found in PDF\n\n" + "\n".join(sorted(failures)) + "\n")
    if len(parts) == 1:
        parts.append("\nNothing to review.\n")
    return "".join(parts)
```

- [ ] **Step 4: Write `tools/kb-lint/lint.py`**

```python
#!/usr/bin/env python3
"""Check the thesis knowledge base (kb/) against its schema, sources and code. See README.md."""

import argparse
from dataclasses import dataclass
from pathlib import Path
import sys

from coderefs import check_code_refs
from ladder import check_ladder
from links import check_links
from model import load_vault
from quotes import PdfText, check_quotes, write_quote_checks
from review_queue import render_queue
from schema import check_schema

REPO = Path(__file__).resolve().parents[2]


@dataclass
class Result:
    issues: list
    written: list

    @property
    def errors(self):
        return [i for i in self.issues if i.severity == "error"]

    @property
    def warnings(self):
        return [i for i in self.issues if i.severity == "warning"]


def run(root, write=False, cache_dir=None):
    root = Path(root)
    vault = load_vault(root)
    pdf_text = PdfText(cache_dir or root / "kb" / ".cache" / "pdftext")
    issues = []
    issues += check_schema(vault)
    issues += check_links(vault)
    issues += check_quotes(vault, pdf_text)  # before the ladder, which reads its results
    issues += check_code_refs(vault)
    issues += check_ladder(vault)
    written = []
    if write:
        written += write_quote_checks(vault)
        queue = root / "kb" / "review-queue.md"
        text = render_queue(vault)
        if not queue.is_file() or queue.read_text(encoding="utf-8") != text:
            queue.write_text(text, encoding="utf-8")
            written.append(queue)
    issues.sort(key=lambda i: (i.path, i.check, i.message))
    return Result(issues, written)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=REPO, help="repository root (default: this repository)")
    parser.add_argument("--write", action="store_true", help="update quote_check fields and regenerate kb/review-queue.md")
    args = parser.parse_args(argv)
    if not (args.root / "kb").is_dir():
        print(f"no kb/ folder under {args.root}", file=sys.stderr)
        return 2
    result = run(args.root, write=args.write)
    for issue in result.issues:
        print(issue)
    for path in result.written:
        print(f"wrote {path.relative_to(args.root)}")
    print(f"{len(result.errors)} errors, {len(result.warnings)} warnings")
    return 1 if result.errors else 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 5: Run the whole suite**

Run: `python3 -m pytest tools/kb-lint/tests -q`
Expected: `83 passed`.

- [ ] **Step 6: Write `tools/kb-lint/README.md`**

````markdown
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
````

- [ ] **Step 7: Update `kb/README.md`**

In the folders table, insert these rows directly above the `_templates/` row:

```markdown
| `ref-theses/` | Notes generated from the example theses: hubs, rhetorical moves, concept candidates. Never evidence | `<author>/<note>` |
| `_pdf/` | Local PDFs for paper notes (gitignored) | `@<citekey>.pdf` |
```

After the table, add:

```markdown
`review-queue.md` is generated by `tools/kb-lint/lint.py --write`: every note with `needs_review: true`, grouped by reason, plus quotes not found in their PDF. Do not edit it by hand.
```

In the rules list, replace this line:

```markdown
- Every claim needs at least one `evidence` entry (a figure ID or a `[[@citekey]]`) before its status leaves `draft`.
```

with these:

```markdown
- A claim leaves `draft` only with evidence: a figure ID in `figures`, or a block link such as `"[[@smith2020#^c1]]"` in `cites` whose quote the lint has found in the PDF (`quote_check: pass`).
- Quote wikilinks in frontmatter: `- "[[@smith2020#^c1]]"`.
- `quote_check` is written only by the lint; `reviewed` only by me.
- Example-thesis notes (`ref-theses/`) are never cited as evidence; cite the primary paper.
- Method notes link to code as `<submodule>@<sha>:<file>#L<start>-<end>`.
- Run `python3 tools/kb-lint/lint.py` (from the repository root) before relying on a claim; see [tools/kb-lint](../tools/kb-lint/README.md).
```

- [ ] **Step 8: Update `.gitignore`**

Below the existing `kb/.trash/` line in the `# Obsidian` section, add:

```text
kb/_pdf/
kb/.cache/
```

- [ ] **Step 9: Run the lint on the real repository**

Run: `python3 tools/kb-lint/lint.py`
Expected: `0 errors, 0 warnings`, exit code 0. The vault has no notes yet, and templates are skipped. Then run `git status --short`: it must list only the files this plan touched, with no `kb/review-queue.md`, because nothing was run with `--write`.

- [ ] **Step 10: Commit**

```bash
git add tools/kb-lint kb/README.md .gitignore
git commit -m "kb-lint: CLI, review queue and documentation"
```
