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


def test_path_that_is_not_a_submodule_is_an_error(repo):
    [(severity, check, message)] = entry_messages(repo, f"projects/demo/cdoe@{head(repo)[:7]}:model.py#L1-2")
    assert (severity, check) == ("error", 7)
    assert "projects/demo/cdoe is not a submodule or git repository" in message
