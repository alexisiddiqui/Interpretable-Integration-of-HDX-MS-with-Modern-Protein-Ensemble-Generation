from pathlib import Path
import shutil
import sqlite3

import pytest

from seed_helpers import make_zotero
from zotero import ZoteroLibrary


def test_keys_exclude_trashed_items(zotero_home):
    library = ZoteroLibrary(zotero_home)
    assert "andersonHDXMSMDSimulations2022" in library.keys
    assert "trashedPaper2019" not in library.keys


def test_pdfs_found_in_storage(zotero_home):
    library = ZoteroLibrary(zotero_home)
    pdf = library.pdf_by_key["andersonHDXMSMDSimulations2022"]
    assert pdf == zotero_home / "storage" / "ATT00101" / "anderson.pdf"
    assert "bradshawInterpretationHDX2020" not in library.pdf_by_key
    assert "trashedPaper2019" not in library.pdf_by_key


def test_pdf_missing_on_disk_is_ignored(zotero_home):
    (zotero_home / "storage" / "ATT00102" / "masson.pdf").unlink()
    assert "massonOverviewHydrogenDeuterium2017" not in ZoteroLibrary(zotero_home).pdf_by_key


def test_match_by_doi_then_title(zotero_home):
    library = ZoteroLibrary(zotero_home)
    assert library.match("https://doi.org/10.1000/ANDERSON", None) == ("andersonHDXMSMDSimulations2022", "doi")
    assert library.match(None, "Interpretation of HDX data") == ("bradshawInterpretationHDX2020", "title")
    assert library.match("10.9/none", "nothing at all") == (None, "no Zotero item with this DOI or title")


def test_unrelated_keys_sharing_a_title_are_ambiguous(zotero_home):
    assert ZoteroLibrary(zotero_home).match(None, "Same Title") == (
        None, "title same title matches several Zotero items: duplicateTitleA2021, duplicateTitleB2021")


def test_better_bibtex_duplicate_resolves_to_the_original_key(tmp_path):
    items = {
        1: ("massonRecommendations2019", "10.1/masson", "Recommendations", "a.pdf"),
        2: ("massonRecommendations2019a", "10.1/MASSON", "Recommendations", "b.pdf"),
    }
    library = ZoteroLibrary(make_zotero(tmp_path / "Z", items=items, deleted=set()))
    assert library.match("10.1/masson", None) == ("massonRecommendations2019", "doi; Zotero duplicates massonRecommendations2019a")


def test_reads_a_copy_while_the_live_database_is_locked(zotero_home):
    lock = sqlite3.connect(zotero_home / "zotero.sqlite")
    lock.execute("PRAGMA journal_mode=WAL")
    lock.execute("BEGIN IMMEDIATE")
    try:
        assert "andersonHDXMSMDSimulations2022" in ZoteroLibrary(zotero_home).keys
    finally:
        lock.rollback()
        lock.close()


def test_reads_committed_wal_edits_but_not_uncommitted_edits(zotero_home):
    writer = sqlite3.connect(zotero_home / "zotero.sqlite")
    try:
        writer.execute("PRAGMA journal_mode=WAL")
        writer.execute("PRAGMA wal_autocheckpoint=0")
        writer.execute("UPDATE itemDataValues SET value=? WHERE value=?",
                       ("committedKey2026", "andersonHDXMSMDSimulations2022"))
        writer.commit()
        writer.execute("UPDATE itemDataValues SET value=? WHERE value=?",
                       ("uncommittedKey2026", "massonOverviewHydrogenDeuterium2017"))

        library = ZoteroLibrary(zotero_home)

        assert "committedKey2026" in library.keys
        assert "andersonHDXMSMDSimulations2022" not in library.keys
        assert "massonOverviewHydrogenDeuterium2017" in library.keys
        assert "uncommittedKey2026" not in library.keys
    finally:
        writer.rollback()
        writer.close()


def test_checkpoint_between_file_copies_cannot_lose_committed_edits(zotero_home, monkeypatch):
    database = zotero_home / "zotero.sqlite"
    writer = sqlite3.connect(database)
    try:
        writer.execute("PRAGMA journal_mode=WAL")
        writer.execute("PRAGMA wal_autocheckpoint=0")
        writer.execute("PRAGMA wal_checkpoint(TRUNCATE)")
        # Keep the two edits on different pages so the later WAL cannot restore
        # the earlier change to the citation-key table after a checkpoint.
        writer.execute("UPDATE itemDataValues SET value=? WHERE value=?",
                       ("earlierKey2026", "andersonHDXMSMDSimulations2022"))
        writer.commit()

        original_copyfile = shutil.copyfile

        def checkpoint_after_database_copy(src, dst, *args, **kwargs):
            result = original_copyfile(src, dst, *args, **kwargs)
            if Path(src) == database:
                writer.execute("PRAGMA wal_checkpoint(TRUNCATE)")
                writer.execute("INSERT INTO items VALUES (999, 'LATEREDIT')")
                writer.commit()
            return result

        # Reproduce the checkpoint race if separate file copies are reintroduced.
        monkeypatch.setattr(shutil, "copyfile", checkpoint_after_database_copy)
        assert "earlierKey2026" in ZoteroLibrary(zotero_home).keys
    finally:
        writer.close()


def test_missing_database_is_not_created(tmp_path):
    with pytest.raises(sqlite3.OperationalError):
        ZoteroLibrary(tmp_path)
    assert not (tmp_path / "zotero.sqlite").exists()
