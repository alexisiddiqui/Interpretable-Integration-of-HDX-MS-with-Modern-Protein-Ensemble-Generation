"""Find \\cite keys in LaTeX and parse BibTeX entries (key, verbatim text, DOI, title, year)."""

from dataclasses import dataclass
from pathlib import Path
import re
import unicodedata

CITE = re.compile(r"\\[A-Za-z]*cite[A-Za-z]*\*?(?:\[[^\]]*\]){0,2}\{([^}]*)\}")
COMMENT = re.compile(r"(?<!\\)%.*")
ENTRY_START = re.compile(r"@(\w+)\s*\{\s*([^,\s]+)\s*,")
SKIP_TYPES = {"comment", "string", "preamble"}


@dataclass
class Citation:
    key: str
    path: str   # as given, repository-relative
    line: int   # 1-based line of the \cite command


@dataclass
class BibEntry:
    key: str
    text: str   # the entry verbatim, from @ to its closing brace
    doi: str | None
    title: str | None
    year: int | None


def find_citations(path, label=None):
    """Every cited key in a .tex file, in order, ignoring commented-out text."""
    lines = Path(path).read_text(encoding="utf-8", errors="replace").split("\n")
    text = "\n".join(COMMENT.sub("", line) for line in lines)
    found = []
    for m in CITE.finditer(text):
        line = text.count("\n", 0, m.start()) + 1
        for key in m.group(1).split(","):
            if key.strip():
                found.append(Citation(key.strip(), label or str(path), line))
    return found


def parse_bib(path):
    """Map citekey -> BibEntry for every real entry in a .bib file."""
    text = Path(path).read_text(encoding="utf-8", errors="replace")
    entries = {}
    pos = 0
    while (m := ENTRY_START.search(text, pos)):
        end = _closing_brace(text, text.index("{", m.start()))
        if end < 0:
            raise ValueError(f"{path}: entry {m.group(2)} has no closing brace")
        pos = end + 1
        if m.group(1).lower() in SKIP_TYPES:
            continue
        body = text[m.start():end + 1]
        year = _field(body, "year") or (_field(body, "date") or "")[:4]
        entries[m.group(2)] = BibEntry(
            key=m.group(2),
            text=body,
            doi=normalise_doi(_field(body, "doi")),
            title=_field(body, "title"),
            year=int(year) if year and year.isdigit() else None,
        )
    return entries


def normalise_doi(doi):
    if not doi:
        return None
    doi = doi.strip().lower()
    doi = re.sub(r"^(https?://(dx\.)?doi\.org/|doi:)", "", doi)
    return doi or None


def normalise_title(title):
    """Lower-case words only: drops braces, LaTeX accents, punctuation and diacritics."""
    if not title:
        return ""
    title = unicodedata.normalize("NFKD", title)
    title = "".join(c for c in title if not unicodedata.combining(c))
    title = re.sub(r"\\[A-Za-z]+|\\.", " ", title)
    return " ".join(re.sub(r"[^\w\s]|_", " ", title.lower()).split())


def plain_title(title):
    return " ".join(re.sub(r"[{}]", "", title or "").split())


def _closing_brace(text, start):
    depth = 0
    for i in range(start, len(text)):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return i
    return -1


def _field(body, name):
    m = re.search(r"(?:^|[,\s])" + name + r"\s*=\s*", body, re.I)
    if not m:
        return None
    i = m.end()
    if i < len(body) and body[i] == "{":
        end = _closing_brace(body, i)
        return body[i + 1:end].strip() if end > 0 else None
    if i < len(body) and body[i] == '"':
        end = body.find('"', i + 1)
        return body[i + 1:end].strip() if end > 0 else None
    bare = re.match(r"[^,\n}]+", body[i:])
    return bare.group(0).strip() if bare else None
