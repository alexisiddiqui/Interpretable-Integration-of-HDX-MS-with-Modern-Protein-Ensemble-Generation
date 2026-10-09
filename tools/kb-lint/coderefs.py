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
