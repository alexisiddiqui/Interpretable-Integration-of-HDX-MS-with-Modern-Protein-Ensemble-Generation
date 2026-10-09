import sqlite3

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
    lock.execute("BEGIN EXCLUSIVE")
    try:
        assert "andersonHDXMSMDSimulations2022" in ZoteroLibrary(zotero_home).keys
    finally:
        lock.rollback()
        lock.close()
