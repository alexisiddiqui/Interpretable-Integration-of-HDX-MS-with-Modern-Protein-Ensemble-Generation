"""Check 2: each paper claim's quote appears on its cited PDF page."""

import hashlib
import re
import subprocess
import unicodedata

from model import Issue

QUOTE_CHARS = str.maketrans({"‘": "'", "’": "'", "“": '"', "”": '"'})
LINE_BREAK_HYPHEN = re.compile("[-‐­]\\s*\\n\\s*")
DASHES = re.compile("[-‐‒–—­]")


def normalise(text):
    """Make PDF text and typed quotes comparable: ligatures, hyphenation, quotes, dashes, case, spacing."""
    text = unicodedata.normalize("NFKC", text)
    text = LINE_BREAK_HYPHEN.sub("", text)
    text = text.translate(QUOTE_CHARS)
    text = DASHES.sub("", text)
    return " ".join(text.split()).lower()


def contains_words(text, quote):
    """True if quote occurs in text without starting or ending inside a word.

    Only letters count as "inside a word": PDFs glue reference numbers to the preceding word
    ("function1."), and a quote ending at "function" must still match.
    """
    return re.search(r"(?<![^\W\d_])" + re.escape(quote) + r"(?![^\W\d_])", text) is not None


class PdfText:
    """Per-page PDF text from pdftotext, cached by the PDF's SHA-256."""

    def __init__(self, cache_dir):
        self.cache_dir = cache_dir

    def pages(self, pdf):
        digest = hashlib.sha256(pdf.read_bytes()).hexdigest()
        cached = self.cache_dir / (digest + ".txt")
        if cached.is_file():
            text = cached.read_text(encoding="utf-8")
        else:
            # Without -layout, pdftotext keeps two-column text in reading order.
            text = subprocess.run(
                ["pdftotext", "-q", "-enc", "UTF-8", str(pdf), "-"],
                capture_output=True, text=True, check=True,
            ).stdout
            self.cache_dir.mkdir(parents=True, exist_ok=True)
            cached.write_text(text, encoding="utf-8")
        pages = text.split("\f")  # pdftotext ends every page with a form feed
        return pages[:-1] if text.endswith("\f") else pages


def check_quotes(vault, pdf_text):
    """Set Block.computed for every quote it can check and report failures."""
    issues = []
    cited = vault.citations()
    for note in vault.notes:
        meta = note.meta or {}
        if note.type != "paper" or not note.blocks:
            continue
        if meta.get("extraction") == "none" or not isinstance(meta.get("pdf"), str) or not meta["pdf"]:
            continue
        pdf = vault.root / meta["pdf"]
        if not pdf.is_file():
            issues.append(Issue("warning", 2, note.rel, f"PDF {meta['pdf']} not found locally; quotes not checked"))
            continue
        try:
            pages = pdf_text.pages(pdf)
        except FileNotFoundError:
            issues.append(Issue("error", 2, note.rel, "pdftotext not found; install Poppler (brew install poppler)"))
            continue
        except subprocess.CalledProcessError:
            issues.append(Issue("error", 2, note.rel, f"pdftotext could not read {meta['pdf']}"))
            continue
        for block in note.blocks:
            if block.page is None or block.quote is None:
                continue  # reported by check 1
            if block.page > len(pages):
                found, detail = False, f"page {block.page} is outside the PDF ({len(pages)} pages)"
            else:
                # A quote may run onto the next page.
                window = pages[block.page - 1] + "\n" + (pages[block.page] if block.page < len(pages) else "")
                found = contains_words(normalise(window), normalise(block.quote))
                detail = f"quote not found on PDF page {block.page}"
            block.computed = "pass" if found else "fail"
            if not found:
                serious = block.reviewed or (note.name, block.id) in cited
                issues.append(Issue("error" if serious else "warning", 2, note.rel, f"^{block.id}: {detail}"))
    return issues


def write_quote_checks(vault):
    """Write each computed result into its quote_check line. Returns the paths changed."""
    changed = []
    for note in vault.notes:
        edits = [
            b for b in note.blocks
            if b.computed and b.computed != b.quote_check and b.quote_check_line is not None
        ]
        for block in edits:
            line = note.lines[block.quote_check_line]
            note.lines[block.quote_check_line] = re.sub(
                r"quote_check:[^\r\n]*", lambda m: "quote_check: " + block.computed, line, count=1
            )
            block.quote_check = block.computed
        if edits:
            note.path.write_text("".join(note.lines), encoding="utf-8")
            changed.append(note.path)
    return changed
