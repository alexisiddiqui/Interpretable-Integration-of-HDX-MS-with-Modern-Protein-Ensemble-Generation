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


def test_generated_review_queue_is_not_linted(repo):
    run(repo, write=True)
    assert [str(i) for i in run(repo).errors] == []
