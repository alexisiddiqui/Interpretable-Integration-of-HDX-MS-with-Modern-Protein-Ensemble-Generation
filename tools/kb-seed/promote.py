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
