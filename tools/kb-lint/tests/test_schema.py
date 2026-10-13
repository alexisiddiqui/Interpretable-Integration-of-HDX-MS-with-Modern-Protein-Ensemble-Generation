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
    write(repo, "kb/voice/style.md", "Just text\n")
    found = messages(repo)
    assert any(m[2] == "kb/concepts/Loose note.md" and "missing frontmatter type" in m[3] for m in found)
    assert not any(m[2] in ("kb/inbox/Idea.md", "kb/voice/style.md") for m in found)


def test_duplicate_note_names(repo):
    write(repo, "kb/inbox/Protection factor.md", "Duplicate\n")
    assert any("also named 'Protection factor'" in m[3] for m in messages(repo))


def test_method_without_code_is_check_9(repo):
    path = repo / "kb/methods/Protection factor model (2-jaxENT).md"
    text = path.read_text(encoding="utf-8")
    start = text.index("code:")
    path.write_text(text[:start] + "code: []\n---\n", encoding="utf-8")
    assert ("error", 9) in {(m[0], m[1]) for m in messages(repo)}


def test_recorded_pass_on_paper_without_pdf_is_an_error(repo):
    edit(repo, "kb/papers/@jones2019.md", "quote_check: unchecked", "quote_check: pass")
    assert any("^c1: quote_check is pass, but this paper has no PDF" in m[3] for m in messages(repo))


def test_pdf_path_must_match_citekey(repo):
    edit(repo, PAPER, "pdf: kb/_pdf/@smith2020.pdf", "pdf: kb/_pdf/@jones2019.pdf")
    assert any("pdf must be empty or kb/_pdf/@smith2020.pdf" in m[3] for m in messages(repo))


def test_short_quote_is_rejected(repo):
    edit(repo, PAPER, '"reports on backbone amide protection factors"', '"protection factors"')
    assert any("^c1: quote is 2 words; use at least 5" in m[3] for m in messages(repo))


def test_note_at_vault_root_is_linted(repo):
    write(repo, "kb/Untitled.md", "Just text\n")
    assert any(m[2] == "kb/Untitled.md" and "missing frontmatter type" in m[3] for m in messages(repo))


def test_concept_sources_must_be_a_list(repo):
    edit(repo, "kb/concepts/Protection factor.md", "sources: []", "sources: oops")
    assert any("'sources' must be a list" in m[3] for m in messages(repo))
