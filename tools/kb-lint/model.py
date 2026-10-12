"""Load the vault: notes, frontmatter, paper claim blocks, wikilinks and bib keys."""

from dataclasses import dataclass, field
from pathlib import Path
import re

import yaml

SKIP_DIRS = {"_templates", "_pdf"}
ROOT_FILES = {"README.md", "review-queue.md"}  # kb/ files that are not notes
REF_THESES = "ref-theses"
QUOTE_STATES = ("pass", "fail", "unchecked")
BLOCK_FIELDS = ("page", "quote", "quote_check", "reviewed")
BLOCK_RE = re.compile(r"^- (?P<text>.*?)\s+\^(?P<id>[A-Za-z0-9-]+)\s*$")
FIELD_RE = re.compile(r"^\s+- (?P<key>\w+):\s*(?P<value>.*?)\s*$")
WIKILINK_RE = re.compile(
    r"^\[\[(?P<target>[^\]#|]+?)(?:#\^(?P<block>[A-Za-z0-9-]+))?(?:\|[^\]]*)?\]\]$"
)
BIB_RE = re.compile(r"@(?P<kind>\w+)\s*\{\s*(?P<key>[^,\s]+)\s*,")


@dataclass
class Issue:
    severity: str  # "error" or "warning"
    check: int     # check number in the spec, section 5
    path: str      # repository-relative path of the note
    message: str

    def __str__(self):
        label = "ERROR" if self.severity == "error" else "WARN "
        return f"{label} [check {self.check}] {self.path}: {self.message}"


@dataclass
class Block:
    """One attributed claim in a paper note's ## Claims section."""

    id: str
    text: str
    line: int                          # index into Note.lines of the bullet
    page: int | None = None
    quote: str | None = None
    quote_check: str | None = None
    reviewed: bool | None = None
    quote_check_line: int | None = None
    computed: str | None = None        # this run's quote check, when the PDF was read
    fields_seen: set = field(default_factory=set)

    @property
    def effective_quote_check(self):
        return self.computed or self.quote_check


@dataclass
class Note:
    path: Path
    rel: str                           # relative to the repository root
    kb_rel: str                        # relative to kb/
    lines: list                        # file lines, line endings kept
    meta: dict | None = None
    meta_error: str | None = None
    blocks: list = field(default_factory=list)
    block_problems: list = field(default_factory=list)

    @property
    def name(self):
        return self.path.stem

    @property
    def type(self):
        return (self.meta or {}).get("type")

    @property
    def folder(self):
        return self.kb_rel.split("/")[0]

    @property
    def in_ref_theses(self):
        return self.folder == REF_THESES

    def block(self, block_id):
        return next((b for b in self.blocks if b.id == block_id), None)


@dataclass
class Vault:
    root: Path
    notes: list
    bib_keys: set

    def __post_init__(self):
        self._by_name = {}
        for note in self.notes:
            self._by_name.setdefault(note.name, []).append(note)

    def find(self, name):
        """The note with this name, or None if there is no note or more than one."""
        matches = self._by_name.get(name, [])
        return matches[0] if len(matches) == 1 else None

    def duplicates(self):
        return {name: notes for name, notes in self._by_name.items() if len(notes) > 1}

    def citations(self):
        """Map (paper note name, block ID) to the notes that rely on it: claim cites, concept and method sources."""
        cited = {}
        fields = {"claim": "cites", "concept": "sources", "method": "sources"}
        for note in self.notes:
            if note.type not in fields:
                continue
            for entry in note.meta.get(fields[note.type]) or []:
                link = parse_wikilink(entry) if isinstance(entry, str) else None
                if link and link[1]:
                    cited.setdefault(link, []).append(note)
        return cited


def parse_wikilink(text):
    """'[[@smith2020#^c1]]' -> ('@smith2020', 'c1'); the block is None when absent."""
    m = WIKILINK_RE.match(text.strip())
    return (m["target"].strip(), m["block"]) if m else None


def parse_frontmatter(lines):
    """Return (meta, error, index of the first body line)."""
    if not lines or lines[0].rstrip("\r\n") != "---":
        return None, None, 0
    for end in range(1, len(lines)):
        if lines[end].rstrip("\r\n") == "---":
            break
    else:
        return None, "frontmatter has no closing ---", 0
    text = "".join(lines[1:end])
    try:
        meta = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        hint = ' (quote wikilinks in frontmatter, e.g. - "[[@key#^c1]]")' if "[[" in text else ""
        problem = getattr(exc, "problem", None) or "parse error"
        return None, f"frontmatter is not valid YAML: {problem}{hint}", end + 1
    if meta is None:
        meta = {}
    if not isinstance(meta, dict):
        return None, "frontmatter must be a mapping of field: value", end + 1
    return meta, None, end + 1


def parse_blocks(lines, start):
    """Parse the ## Claims section of a paper note. Returns (blocks, problems)."""
    blocks, problems = [], []
    in_claims = in_comment = False
    current = None
    for i in range(start, len(lines)):
        line = lines[i].rstrip("\r\n")
        if in_comment:
            in_comment = "-->" not in line
            continue
        if line.lstrip().startswith("<!--"):
            in_comment = "-->" not in line
            continue
        if line.startswith("#"):
            in_claims = line.strip() == "## Claims"
            current = None
            continue
        if not in_claims or not line.strip():
            continue
        if line.startswith("- "):
            m = BLOCK_RE.match(line)
            current = Block(id=m["id"], text=m["text"], line=i) if m else None
            if current:
                blocks.append(current)
            else:
                problems.append(f"line {i + 1}: claim bullet has no block ID; end it with ^c<N>")
            continue
        m = FIELD_RE.match(line)
        if m and current is not None:
            _set_field(current, m["key"], m["value"], i, problems)
    seen = set()
    for block in blocks:
        if block.id in seen:
            problems.append(f"block ID ^{block.id} is used twice")
        seen.add(block.id)
        for name in BLOCK_FIELDS:
            if name not in block.fields_seen:
                problems.append(f"^{block.id}: missing '{name}'")
    return blocks, problems


def _set_field(block, key, value, index, problems):
    block.fields_seen.add(key)
    where = f"^{block.id}"
    if key == "page":
        if value.isdigit() and int(value) >= 1:
            block.page = int(value)
        else:
            problems.append(f"{where}: page must be a whole number from 1 (the PDF page index), got '{value}'")
    elif key == "quote":
        if len(value) >= 2 and value[0] == value[-1] == '"' and value[1:-1].strip():
            block.quote = value[1:-1]
        else:
            problems.append(f"{where}: quote must be non-empty text in double quotes")
    elif key == "quote_check":
        block.quote_check_line = index
        if value in QUOTE_STATES:
            block.quote_check = value
        else:
            problems.append(f"{where}: quote_check must be one of {', '.join(QUOTE_STATES)}")
    elif key == "reviewed":
        if value.lower() in ("true", "false"):
            block.reviewed = value.lower() == "true"
        else:
            problems.append(f"{where}: reviewed must be true or false")


def read_bib_keys(path):
    if not path.is_file():
        return set()
    text = path.read_text(encoding="utf-8", errors="replace")
    skip = {"comment", "string", "preamble"}
    return {m["key"] for m in BIB_RE.finditer(text) if m["kind"].lower() not in skip}


def load_vault(root):
    root = Path(root)
    kb = root / "kb"
    notes = []
    for path in sorted(kb.rglob("*.md")):
        parts = path.relative_to(kb).parts
        if (len(parts) == 1 and parts[0] in ROOT_FILES) or any(p.startswith(".") or p in SKIP_DIRS for p in parts[:-1]):
            continue  # templates, PDFs, Obsidian state
        note = Note(path=path, rel=path.relative_to(root).as_posix(), kb_rel="/".join(parts), lines=[])
        try:
            note.lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
        except UnicodeDecodeError:
            note.meta_error = "file is not valid UTF-8"
            notes.append(note)
            continue
        note.meta, note.meta_error, body = parse_frontmatter(note.lines)
        if note.type == "paper":
            note.blocks, note.block_problems = parse_blocks(note.lines, body)
        notes.append(note)
    return Vault(root=root, notes=notes, bib_keys=read_bib_keys(root / "thesis" / "references.bib"))
