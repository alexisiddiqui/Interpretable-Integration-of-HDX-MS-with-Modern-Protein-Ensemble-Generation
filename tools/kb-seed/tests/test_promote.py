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


def test_medium_confidence_draft_is_not_promoted(repo):
    edit(repo, CLAIM, "confidence: high", "confidence: medium")
    assert promote(repo) == ([], [])
    assert status(repo, CLAIM) == "status: draft"
