"""Read-only view of a local Zotero 7 library: citation keys, DOIs, titles and stored PDFs."""

from pathlib import Path
import re
import shutil
import sqlite3
import tempfile

from bibtex import normalise_doi, normalise_title


class ZoteroLibrary:
    def __init__(self, home):
        self.home = Path(home)
        with tempfile.TemporaryDirectory() as tmp:
            # Work on a copy: a running Zotero holds a lock on the live database.
            copy = Path(tmp) / "zotero.sqlite"
            shutil.copyfile(self.home / "zotero.sqlite", copy)
            db = sqlite3.connect(copy)
            try:
                self._load(db)
            finally:
                db.close()

    def _load(self, db):
        deleted = {row[0] for row in db.execute("SELECT itemID FROM deletedItems")}

        def field(name):
            rows = db.execute(
                "SELECT d.itemID, v.value FROM itemData d JOIN itemDataValues v USING (valueID) "
                "JOIN fields f USING (fieldID) WHERE f.fieldName = ?", (name,))
            return {item: value for item, value in rows if item not in deleted}

        keys = field("citationKey")
        self.keys = set(keys.values())
        self.key_by_doi = _index(keys, field("DOI"), normalise_doi)
        self.key_by_title = _index(keys, field("title"), normalise_title)
        self.pdf_by_key = {}
        rows = db.execute(
            "SELECT a.itemID, a.parentItemID, i.key, a.path FROM itemAttachments a "
            "JOIN items i ON i.itemID = a.itemID "
            "WHERE a.contentType = 'application/pdf' AND a.path LIKE 'storage:%' ORDER BY a.itemID")
        for attachment, parent, folder, path in rows:
            if parent in keys and attachment not in deleted:
                pdf = self.home / "storage" / folder / path[len("storage:"):]
                if pdf.is_file():
                    self.pdf_by_key.setdefault(keys[parent], pdf)

    def match(self, doi, title):
        """(citekey, how) for a DOI or title, or (None, reason) when nothing matches unambiguously."""
        for how, index, value in (("doi", self.key_by_doi, normalise_doi(doi)),
                                  ("title", self.key_by_title, normalise_title(title))):
            keys = index.get(value) if value else None
            if not keys:
                continue
            if len(keys) == 1:
                return next(iter(keys)), how
            base = duplicate_base(keys)
            if base:
                others = ", ".join(sorted(keys - {base}))
                return base, f"{how}; Zotero duplicates {others}"
            return None, f"{how} {value} matches several Zotero items: {', '.join(sorted(keys))}"
        return None, "no Zotero item with this DOI or title"


def duplicate_base(keys):
    """The original key when the others are Better BibTeX's duplicate suffixes (key, keya, keyb, ...)."""
    shortest = min(keys, key=len)
    if all(k == shortest or re.fullmatch(re.escape(shortest) + "[a-z]", k) for k in keys):
        return shortest
    return None


def _index(keys, values, normalise):
    """Normalised value -> set of citekeys carrying it."""
    index = {}
    for item, value in values.items():
        norm = normalise(value) if item in keys else None
        if norm:
            index.setdefault(norm, set()).add(keys[item])
    return index
