#!/usr/bin/env python3
"""Check the thesis knowledge base (kb/) against its schema, sources and code. See README.md."""

import argparse
from dataclasses import dataclass
from pathlib import Path
import sys

from coderefs import check_code_refs
from ladder import check_ladder
from links import check_links
from model import load_vault
from notation import check_notation, render_notation
from quotes import PdfText, check_quotes, write_quote_checks
from review_queue import render_queue
from schema import check_schema

REPO = Path(__file__).resolve().parents[2]


@dataclass
class Result:
    issues: list
    written: list

    @property
    def errors(self):
        return [i for i in self.issues if i.severity == "error"]

    @property
    def warnings(self):
        return [i for i in self.issues if i.severity == "warning"]


def run(root, write=False, cache_dir=None):
    root = Path(root)
    vault = load_vault(root)
    pdf_text = PdfText(cache_dir or root / "kb" / ".cache" / "pdftext")
    issues = []
    issues += check_schema(vault)
    issues += check_links(vault)
    issues += check_quotes(vault, pdf_text)  # before the ladder, which reads its results
    issues += check_code_refs(vault)
    issues += check_ladder(vault)
    issues += check_notation(vault)
    written = []
    if write:
        written += write_quote_checks(vault)
        for name, text in (("review-queue.md", render_queue(vault)), ("notation.md", render_notation(vault))):
            path = root / "kb" / name
            if not path.is_file() or path.read_text(encoding="utf-8") != text:
                path.write_text(text, encoding="utf-8")
                written.append(path)
    issues.sort(key=lambda i: (i.path, i.check, i.message))
    return Result(issues, written)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=REPO, help="repository root (default: this repository)")
    parser.add_argument("--write", action="store_true", help="update quote_check fields and regenerate kb/review-queue.md and kb/notation.md")
    args = parser.parse_args(argv)
    if not (args.root / "kb").is_dir():
        print(f"no kb/ folder under {args.root}", file=sys.stderr)
        return 2
    result = run(args.root, write=args.write)
    for issue in result.issues:
        print(issue)
    for path in result.written:
        print(f"wrote {path.relative_to(args.root)}")
    print(f"{len(result.errors)} errors, {len(result.warnings)} warnings")
    return 1 if result.errors else 0


if __name__ == "__main__":
    sys.exit(main())
