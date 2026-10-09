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
    assert found == ['status is supported but cited claim [[@smith2020#^c1]] was not verified against its PDF in this run (recorded quote_check: unchecked); add the PDF under kb/_pdf/']


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
    assert messages(repo, tmp_path) == ["status is in-thesis but cited claim [[@jones2019#^c1]] was not verified against its PDF in this run (recorded quote_check: unchecked); add the PDF under kb/_pdf/"]


def test_recorded_pass_without_the_pdf_cannot_support_a_claim(repo, tmp_path):
    edit(repo, "kb/papers/@smith2020.md", "quote_check: unchecked", "quote_check: pass")
    (repo / "kb/_pdf/@smith2020.pdf").unlink()
    assert any("[[@smith2020#^c1]] was not verified against its PDF in this run (recorded quote_check: pass)" in m
               for m in messages(repo, tmp_path))
