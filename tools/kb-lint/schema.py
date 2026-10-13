"""Check 1 (frontmatter matches the schema for its type) and check 9 (methods need code)."""

import datetime
import re

from model import Issue

STATUSES = ("draft", "supported", "in-thesis")
MIN_QUOTE_WORDS = 5   # long enough to identify one passage
MAX_QUOTE_WORDS = 25
ANY_TYPE_KEYS = {"tags", "aliases", "cssclasses"}  # Obsidian's own properties
UNTYPED_FOLDERS = {"chapters", "inbox", "voice"}
FOLDER_TYPES = {
    "papers": {"paper"},
    "claims": {"claim"},
    "concepts": {"concept"},
    "methods": {"method"},
    "decisions": {"decision"},
    "ref-theses": {"ref-thesis", "move", "concept-candidate"},
}


def one_of(*values):
    def check(value):
        if value not in values:
            return "must be one of " + ", ".join(values)
    return check


def text(value):
    if not isinstance(value, str) or not value.strip():
        return "must be non-empty text"


def optional_text(value):
    if value is not None and not isinstance(value, str):
        return "must be text or empty"


def boolean(value):
    if not isinstance(value, bool):
        return "must be true or false"


def whole_number(value):
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        return "must be a whole number from 1"


def optional_year(value):
    if value is not None and (isinstance(value, bool) or not isinstance(value, int)):
        return "must be a year such as 2020, or empty"


def text_list(value):
    if value is None:
        return None
    if not isinstance(value, list):
        return "must be a list"
    for item in value:
        if isinstance(item, list):
            return 'contains an unquoted wikilink; write it as "[[...]]"'
        if not isinstance(item, str):
            return "must be a list of text"


def iso_date(value):
    if isinstance(value, datetime.date):
        return None
    if isinstance(value, str) and re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        return None
    return "must be a date, YYYY-MM-DD"


def notation(value):
    if value is None:
        return None
    if not isinstance(value, list):
        return "must be a list of {symbol, meaning, units}"
    for entry in value:
        if (
            not isinstance(entry, dict)
            or text(entry.get("symbol"))
            or text(entry.get("meaning"))
            or optional_text(entry.get("units"))
        ):
            return "each entry needs text symbol and meaning, and optional units"


def locator_quote(value):
    if value is None:
        return None
    if not isinstance(value, str):
        return "must be text or empty"
    if len(value.split()) > MAX_QUOTE_WORDS:
        return f"must be {MAX_QUOTE_WORDS} words or fewer"


REVIEW = {"needs_review": boolean, "review_reason": optional_text}

# Every key listed here must be present; the validator decides which values are allowed.
SCHEMAS = {
    "paper": {
        "citekey": text, "year": optional_year, "read": boolean, "pdf": optional_text,
        "extraction": one_of("auto", "manual", "none"), **REVIEW,
    },
    "claim": {
        "chapter": optional_text, "project": optional_text,
        "basis": one_of("stated", "inferred"), "confidence": one_of("high", "medium", "low"),
        "status": one_of(*STATUSES), "origin": text, "source_state": one_of("current", "outdated"),
        **REVIEW, "figures": text_list, "cites": text_list, "code": text_list,
    },
    "concept": {"aliases": text_list, "notation": notation, "sources": text_list},
    "method": {"project": text, "status": one_of(*STATUSES), **REVIEW, "code": text_list, "sources": text_list},
    "figure": {
        "fig_id": text, "chapter": optional_text, "source": one_of("script", "reused"),
        "code": text_list,
    },
    "decision": {"date": iso_date, "project": optional_text, "status": one_of("active", "superseded")},
    "ref-thesis": {"thesis": text, "generated": boolean},
    "move": {
        "thesis": text, "page": whole_number, "move_type": text, "locator_quote": locator_quote,
        "generated": boolean, **REVIEW,
    },
    "concept-candidate": {"thesis": text, "aliases": text_list, "generated": boolean, **REVIEW},
}


def check_schema(vault):
    issues = []
    for name, notes in sorted(vault.duplicates().items()):
        for note in notes:
            issues.append(Issue("error", 1, note.rel, f"another note is also named '{name}'; links to it are ambiguous"))
    for note in vault.notes:
        issues += check_note(note)
    return issues


def check_note(note):
    def error(message, check=1):
        return Issue("error", check, note.rel, message)

    if note.meta_error:
        return [error(note.meta_error)]
    if not note.type:
        if note.folder in UNTYPED_FOLDERS:
            return []
        return [error("missing frontmatter type; start the note from a template in kb/_templates/")]
    kind = note.type
    if kind not in SCHEMAS:
        return [error(f"unknown type '{kind}'")]
    issues = []
    allowed = FOLDER_TYPES.get(note.folder)
    if allowed and kind not in allowed:
        issues.append(error(f"notes in {note.folder}/ must have type {' or '.join(sorted(allowed))}, not '{kind}'"))
    schema = SCHEMAS[kind]
    for key, validate in schema.items():
        if key not in note.meta:
            issues.append(error(f"missing field '{key}'"))
            continue
        problem = validate(note.meta[key])
        if problem:
            issues.append(error(f"'{key}' {problem}"))
    for key in note.meta:
        if key != "type" and key not in schema and key not in ANY_TYPE_KEYS:
            issues.append(Issue("warning", 1, note.rel, f"unexpected field '{key}'"))
    reason = note.meta.get("review_reason")
    if note.meta.get("needs_review") is True and not (isinstance(reason, str) and reason.strip()):
        issues.append(error("review_reason is required when needs_review is true"))
    if kind == "paper":
        issues += _check_paper(note, error)
    if kind == "method" and not note.meta.get("code"):
        issues.append(error("method notes need at least one code entry (<submodule>@<sha>:<file>#L<start>-<end>)", check=9))
    return issues


def _check_paper(note, error):
    meta = note.meta
    issues = []
    citekey = meta.get("citekey") if isinstance(meta.get("citekey"), str) else None
    if citekey and note.name != "@" + citekey:
        issues.append(error(f"note name must be @{citekey} to match its citekey"))
    if citekey and meta.get("pdf") and meta["pdf"] != f"kb/_pdf/@{citekey}.pdf":
        issues.append(error(f"pdf must be empty or kb/_pdf/@{citekey}.pdf"))
    no_pdf = meta.get("extraction") == "none" or not meta.get("pdf")
    if no_pdf and meta.get("needs_review") is not True:
        issues.append(error("papers without a PDF must set needs_review: true with a review_reason"))
    issues += [error(problem) for problem in note.block_problems]
    for block in note.blocks:
        words = len(block.quote.split()) if block.quote else 0
        if words > MAX_QUOTE_WORDS:
            issues.append(error(f"^{block.id}: quote is {words} words; keep it to {MAX_QUOTE_WORDS} or fewer"))
        elif 0 < words < MIN_QUOTE_WORDS:
            issues.append(error(f"^{block.id}: quote is {words} words; use at least {MIN_QUOTE_WORDS} so it identifies one passage"))
        if no_pdf and block.quote_check in ("pass", "fail"):
            issues.append(error(f"^{block.id}: quote_check is {block.quote_check}, but this paper has no PDF and only the lint sets it; use unchecked"))
    return issues
