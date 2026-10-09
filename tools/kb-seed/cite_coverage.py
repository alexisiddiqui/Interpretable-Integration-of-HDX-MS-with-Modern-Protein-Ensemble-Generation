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
