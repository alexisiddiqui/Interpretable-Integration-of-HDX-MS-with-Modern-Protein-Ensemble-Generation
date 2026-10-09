"""Fixtures for kb-seed: a minimal Zotero 7 database and a small repository with LaTeX and .bib files."""

from pathlib import Path
import shutil
import sqlite3
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "kb-lint" / "tests"))
from helpers import make_pdf  # noqa: E402  (kb-lint's minimal text PDF)

SCHEMA = """
CREATE TABLE items (itemID INTEGER PRIMARY KEY, key TEXT);
CREATE TABLE fields (fieldID INTEGER PRIMARY KEY, fieldName TEXT);
CREATE TABLE itemDataValues (valueID INTEGER PRIMARY KEY, value TEXT);
CREATE TABLE itemData (itemID INTEGER, fieldID INTEGER, valueID INTEGER);
CREATE TABLE itemAttachments (itemID INTEGER PRIMARY KEY, parentItemID INTEGER, contentType TEXT, path TEXT);
CREATE TABLE deletedItems (itemID INTEGER PRIMARY KEY);
"""

# itemID: (citationKey, DOI, title, PDF file name or None)
ITEMS = {
    1: ("andersonHDXMSMDSimulations2022", "10.1000/anderson", "HDX-MS and MD Simulations", "anderson.pdf"),
    2: ("massonOverviewHydrogenDeuterium2017", "10.1000/masson", "An Overview of Hydrogen–Deuterium Exchange", "masson.pdf"),
    3: ("bradshawInterpretationHDX2020", None, "Interpretation of {HDX} Data", None),
    4: ("trashedPaper2019", "10.1000/trashed", "A Trashed Paper", "trashed.pdf"),
    5: ("duplicateTitleA2021", None, "Same Title", None),
    6: ("duplicateTitleB2021", None, "Same Title", None),
}
DELETED = {4}

LIBRARY_BIB = """@article{andersonHDXMSMDSimulations2022,
  title = {{HDX-MS} and {MD} Simulations},
  doi = {10.1000/anderson},
  date = {2022-03-01},
}

@article{massonOverviewHydrogenDeuterium2017,
  title = {An Overview of Hydrogen--Deuterium Exchange},
  year = {2017},
  doi = {10.1000/MASSON},
}

@article{bradshawInterpretationHDX2020,
  title = {Interpretation of {HDX} Data},
  year = 2020,
}

@comment{jabref-meta: ignored}
"""

SOURCE_BIB = """@article{anderson_hdx-ms_2022,
  title = {{HDX}-{MS} and {MD} simulations},
  doi = {https://doi.org/10.1000/Anderson},
  year = {2022},
}
@article{bradshaw_interpretation_2020,
  title = "Interpretation of {HDX} data",
  year = {2020},
}
@article{same_title_2021,
  title = {Same Title},
}
@article{unknown_paper_2001,
  title = {Nothing Like This In Zotero},
}
"""

VALDX_TEX = """\\section{Introduction}
HDX-MS measures dynamics.\\cite{anderson_hdx-ms_2022,masson_overview_2017}
% Old text \\cite{unknown_paper_2001}
Simulations help.\\citep[see][p.~3]{bradshaw_interpretation_2020}
"""

CONF_TEX = """Ensembles matter \\cite{
  andersonHDXMSMDSimulations2022,
  massonOverviewHydrogenDeuterium2017}.
"""


def make_zotero(home, items=ITEMS, deleted=DELETED):
    """Create a Zotero data directory with the tables and PDFs kb-seed reads."""
    home.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(home / "zotero.sqlite")
    db.executescript(SCHEMA)
    db.executemany("INSERT INTO fields VALUES (?, ?)", [(1, "title"), (58, "DOI"), (92, "citationKey")])
    value_id = 0
    for item_id, (key, doi, title, pdf) in items.items():
        db.execute("INSERT INTO items VALUES (?, ?)", (item_id, f"ITEM{item_id:04d}"))
        for field_id, value in ((92, key), (58, doi), (1, title)):
            if value is None:
                continue
            value_id += 1
            db.execute("INSERT INTO itemDataValues VALUES (?, ?)", (value_id, value))
            db.execute("INSERT INTO itemData VALUES (?, ?, ?)", (item_id, field_id, value_id))
        if pdf:
            attachment = 100 + item_id
            folder = f"ATT{attachment:05d}"
            db.execute("INSERT INTO items VALUES (?, ?)", (attachment, folder))
            db.execute("INSERT INTO itemAttachments VALUES (?, ?, ?, ?)",
                       (attachment, item_id, "application/pdf", f"storage:{pdf}"))
            (home / "storage" / folder).mkdir(parents=True)
            text = f"{title}. This stored article has enough words on its first page to count as readable text. " * 2
            ascii_text = text.encode("ascii", "replace").decode()  # the minimal PDF uses a Latin-1 font
            (home / "storage" / folder / pdf).write_bytes(make_pdf([ascii_text]))
    db.executemany("INSERT INTO deletedItems VALUES (?)", [(i,) for i in deleted])
    db.commit()
    db.close()
    return home


def make_repo(root, kb_lint_templates):
    """A repository with two introductions, a source bib, a library bib and the real paper template."""
    files = {
        "projects/1-ValDX/manuscript/report/1_introduction_omc.tex": VALDX_TEX,
        "projects/1-ValDX/manuscript/report/_references.bib": SOURCE_BIB,
        "milestones/conf/introduction/ensembles.tex": CONF_TEX,
        "milestones/conf/zotero_library.bib": LIBRARY_BIB,
    }
    for rel, text in files.items():
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    shutil.copytree(kb_lint_templates, root / "kb" / "_templates")
    return root


TEX = ["projects/1-ValDX/manuscript/report/1_introduction_omc.tex", "milestones/conf/introduction/ensembles.tex"]
SOURCE_BIBS = ["projects/1-ValDX/manuscript/report/_references.bib"]
LIBRARY = "milestones/conf/zotero_library.bib"
