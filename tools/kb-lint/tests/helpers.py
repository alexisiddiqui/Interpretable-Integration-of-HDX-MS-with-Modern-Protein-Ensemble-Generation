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
  - quote: "ensembles explain hydrogen exchange better"
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
sources: []
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
sources: []
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
