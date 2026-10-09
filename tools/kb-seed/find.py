#!/usr/bin/env python3
"""Search a paper's PDF text by page, to find a verbatim quote and its 1-based PDF page index.

    python3 tools/kb-seed/find.py @citekey "regex" [--context 200]

Uses the same pdftotext extraction and cache as tools/kb-lint, so a passage found here is
the text the lint will check the quote against.
"""

import argparse
from pathlib import Path
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "kb-lint"))
from quotes import PdfText  # noqa: E402

REPO = Path(__file__).resolve().parents[2]


def search(pdf, pattern, cache_dir, context=200):
    """Yield (page index, snippet) for every match; snippets have line breaks collapsed."""
    regex = re.compile(pattern, re.I)
    for number, page in enumerate(PdfText(cache_dir).pages(pdf), start=1):
        flat = " ".join(page.split())
        for m in regex.finditer(flat):
            start, end = max(0, m.start() - context), min(len(flat), m.end() + context)
            yield number, flat[start:end]


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("paper", help="paper note name, e.g. @smith2020")
    parser.add_argument("pattern", help="case-insensitive regular expression")
    parser.add_argument("--context", type=int, default=200, help="characters shown either side")
    parser.add_argument("--root", type=Path, default=REPO)
    args = parser.parse_args(argv)
    pdf = args.root / "kb" / "_pdf" / f"{args.paper}.pdf"
    if not pdf.is_file():
        print(f"no PDF at {pdf.relative_to(args.root)}", file=sys.stderr)
        return 2
    hits = 0
    for number, snippet in search(pdf, args.pattern, args.root / "kb" / ".cache" / "pdftext", args.context):
        hits += 1
        print(f"page {number}: ...{snippet}...\n")
    print(f"{hits} matches")
    return 0 if hits else 1


if __name__ == "__main__":
    sys.exit(main())
