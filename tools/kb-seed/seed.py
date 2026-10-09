#!/usr/bin/env python3
"""Seed thesis/references.bib, thesis/citekey-map.tsv, kb/papers/ stubs and kb/_pdf/ from LaTeX and Zotero.

Zotero (Better BibTeX) citekeys are canonical. A cited key that is not a Zotero key is matched through
its entry in a source .bib, by DOI and then by title. Nothing is written unless every key resolves and
every canonical key has an entry in the library .bib. Existing notes, PDFs and bib entries are never
overwritten. See README.md.
"""

import argparse
from dataclasses import dataclass, field
from pathlib import Path
import shutil
import subprocess
import sys

from bibtex import find_citations, parse_bib, plain_title
from zotero import ZoteroLibrary

REPO = Path(__file__).resolve().parents[2]
MAP_HEADER = "source_key\tcanonical_key\tmatched_by\tfirst_cited_in\n"
# Reasons name no citekey, so kb/review-queue.md groups these papers under one heading each.
NO_PDF_REASON = "No PDF in Zotero; add kb/_pdf/@<citekey>.pdf, then set pdf and extraction: auto"
UNREADABLE_REASON = ("PDF in Zotero has no readable text (damaged or scanned); add a text PDF as "
                     "kb/_pdf/@<citekey>.pdf, then set pdf and extraction: auto")
MIN_WORDS = 20  # on the first three pages; a scanned or damaged PDF yields none


@dataclass
class Plan:
    mapping: dict = field(default_factory=dict)      # source key -> (canonical key, how, first citation)
    unresolved: list = field(default_factory=list)   # (source key, reason)
    missing_entries: list = field(default_factory=list)  # canonical keys absent from the library .bib
    new_entries: list = field(default_factory=list)
    new_stubs: list = field(default_factory=list)
    new_pdfs: list = field(default_factory=list)
    no_pdf: list = field(default_factory=list)
    unreadable: list = field(default_factory=list)  # Zotero has a PDF but pdftotext finds no text

    @property
    def canonical(self):
        return sorted({canonical for canonical, _, _ in self.mapping.values()})

    @property
    def ok(self):
        return not self.unresolved and not self.missing_entries


def resolve(citations, source_bibs, library):
    """Map each cited key to a canonical Zotero key. Returns (mapping, unresolved)."""
    mapping, unresolved = {}, []
    for citation in citations:
        key = citation.key
        if key in mapping or any(key == k for k, _ in unresolved):
            continue
        where = f"{citation.path}:{citation.line}"
        if key in library.keys:
            mapping[key] = (key, "key", where)
            continue
        entry = next((bib[key] for bib in source_bibs if key in bib), None)
        if entry is None:
            unresolved.append((key, f"not a Zotero key and not in any source bib (cited at {where})"))
            continue
        canonical, how = library.match(entry.doi, entry.title)
        if canonical:
            mapping[key] = (canonical, how, where)
        else:
            unresolved.append((key, f"{how} (cited at {where})"))
    return mapping, unresolved


def plan_seed(root, tex_paths, source_bib_paths, library_bib_path, library):
    citations = [c for path in tex_paths for c in find_citations(root / path, label=str(path))]
    source_bibs = [parse_bib(root / p) for p in source_bib_paths]
    library_bib = parse_bib(root / library_bib_path)
    plan = Plan()
    plan.mapping, plan.unresolved = resolve(citations, source_bibs, library)
    thesis_bib = root / "thesis" / "references.bib"
    existing = parse_bib(thesis_bib) if thesis_bib.is_file() else {}
    for key in plan.canonical:
        if key not in existing:
            (plan.new_entries if key in library_bib else plan.missing_entries).append(key)
        if not (root / "kb" / "papers" / f"@{key}.md").exists():
            plan.new_stubs.append(key)
        if not (root / "kb" / "_pdf" / f"@{key}.pdf").exists():
            if key not in library.pdf_by_key:
                plan.no_pdf.append(key)
            elif readable(library.pdf_by_key[key]):
                plan.new_pdfs.append(key)
            else:
                plan.unreadable.append(key)
    return plan, library_bib, existing


def readable(pdf):
    """True if pdftotext finds at least MIN_WORDS words on the first three pages."""
    try:
        result = subprocess.run(["pdftotext", "-q", "-l", "3", "-enc", "UTF-8", str(pdf), "-"],
                                capture_output=True, text=True, errors="replace")
    except FileNotFoundError:
        raise SystemExit("pdftotext not found; install Poppler (brew install poppler)")
    return result.returncode == 0 and len(result.stdout.split()) >= MIN_WORDS


def paper_stub(key, entry, has_pdf, template, reason=NO_PDF_REASON):
    body = template.split("\n---\n", 1)[1]
    year = entry.year if entry and entry.year else ""
    title = plain_title(entry.title) if entry else key
    lines = [
        "---",
        "type: paper",
        f"citekey: {key}",
        f"year: {year}",
        "read: false",
        f"pdf: kb/_pdf/@{key}.pdf" if has_pdf else "pdf:",
        f"extraction: {'auto' if has_pdf else 'none'}",
        f"needs_review: {'false' if has_pdf else 'true'}",
        "review_reason:" if has_pdf else f'review_reason: "{reason}"',  # quoted: the text contains ": "
        "---",
        "",
        f"# {title} ({year})" if year else f"# {title}",
    ]
    return "\n".join(lines) + "\n" + body


def apply_seed(root, plan, library_bib, existing, library):
    bib_path = root / "thesis" / "references.bib"
    entries = {key: e.text for key, e in existing.items()}
    entries.update({key: library_bib[key].text for key in plan.new_entries})
    bib_path.parent.mkdir(parents=True, exist_ok=True)
    bib_path.write_text("\n\n".join(entries[k] for k in sorted(entries)) + "\n", encoding="utf-8")

    map_path = root / "thesis" / "citekey-map.tsv"
    rows = {}
    if map_path.is_file():
        for line in map_path.read_text(encoding="utf-8").splitlines()[1:]:
            if line.strip():
                rows[line.split("\t")[0]] = line
    for source, (canonical, how, where) in plan.mapping.items():
        rows.setdefault(source, f"{source}\t{canonical}\t{how}\t{where}")
    map_path.write_text(MAP_HEADER + "".join(rows[k] + "\n" for k in sorted(rows)), encoding="utf-8")

    pdf_dir = root / "kb" / "_pdf"
    for key in plan.new_pdfs:
        pdf_dir.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(library.pdf_by_key[key], pdf_dir / f"@{key}.pdf")

    template = (root / "kb" / "_templates" / "paper.md").read_text(encoding="utf-8")
    for key in plan.new_stubs:
        has_pdf = (pdf_dir / f"@{key}.pdf").is_file()
        note = root / "kb" / "papers" / f"@{key}.md"
        note.parent.mkdir(parents=True, exist_ok=True)
        reason = UNREADABLE_REASON if key in plan.unreadable else NO_PDF_REASON
        note.write_text(paper_stub(key, library_bib.get(key), has_pdf, template, reason), encoding="utf-8")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--tex", nargs="+", required=True, type=Path, help="LaTeX files whose citations to seed")
    parser.add_argument("--source-bib", nargs="*", default=[], type=Path, help=".bib files that define non-Zotero keys")
    parser.add_argument("--library-bib", required=True, type=Path, help="Better BibTeX export of the Zotero library")
    parser.add_argument("--zotero", type=Path, default=Path.home() / "Zotero", help="Zotero data directory")
    parser.add_argument("--root", type=Path, default=REPO, help="repository root (default: this repository)")
    parser.add_argument("--dry-run", action="store_true", help="report what would be written; write nothing")
    args = parser.parse_args(argv)

    library = ZoteroLibrary(args.zotero)
    plan, library_bib, existing = plan_seed(args.root, args.tex, args.source_bib, args.library_bib, library)
    remapped = sum(1 for source, (canonical, _, _) in plan.mapping.items() if source != canonical)
    print(f"{len(plan.mapping) + len(plan.unresolved)} cited keys -> {len(plan.canonical)} papers ({remapped} remapped to Zotero keys)")
    for source, (canonical, how, _) in sorted(plan.mapping.items()):
        if "duplicates" in how:
            print(f"DUPLICATE {source} -> {canonical} ({how}); merge these items in Zotero")
    for key, reason in plan.unresolved:
        print(f"UNRESOLVED {key}: {reason}")
    for key in plan.missing_entries:
        print(f"MISSING {key}: not in {args.library_bib}; re-export the Zotero library")
    if not plan.ok:
        print("Nothing written.")
        return 1
    print(f"{len(plan.new_entries)} new bib entries, {len(plan.new_stubs)} new paper notes, "
          f"{len(plan.new_pdfs)} PDFs to copy, {len(plan.no_pdf)} papers without a PDF, "
          f"{len(plan.unreadable)} unreadable")
    for key in plan.no_pdf:
        print(f"NO PDF {key}")
    for key in plan.unreadable:
        print(f"UNREADABLE {key}: {library.pdf_by_key[key]}")
    if args.dry_run:
        print("Dry run: nothing written.")
        return 0
    apply_seed(args.root, plan, library_bib, existing, library)
    print("Written: thesis/references.bib, thesis/citekey-map.tsv, kb/papers/, kb/_pdf/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
