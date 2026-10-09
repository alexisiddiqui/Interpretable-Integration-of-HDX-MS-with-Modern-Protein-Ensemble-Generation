import sys

import pytest

from seed import main, plan_seed
from seed_helpers import LIBRARY, SOURCE_BIBS, TEX
from zotero import ZoteroLibrary

TOOLS = __import__("pathlib").Path(__file__).resolve().parents[2]


def args(repo, zotero_home, *extra, tex=TEX):
    return ["--root", str(repo), "--zotero", str(zotero_home), "--tex", *tex,
            "--source-bib", *SOURCE_BIBS, "--library-bib", LIBRARY, *extra]


def test_plan_resolves_and_reports_unresolved(seed_repo, zotero_home):
    library = ZoteroLibrary(zotero_home)
    plan, _, _ = plan_seed(seed_repo, TEX, SOURCE_BIBS, LIBRARY, library)
    assert plan.mapping["anderson_hdx-ms_2022"][:2] == ("andersonHDXMSMDSimulations2022", "doi")
    assert plan.mapping["bradshaw_interpretation_2020"][:2] == ("bradshawInterpretationHDX2020", "title")
    assert plan.mapping["andersonHDXMSMDSimulations2022"][:2] == ("andersonHDXMSMDSimulations2022", "key")
    assert [k for k, _ in plan.unresolved] == ["masson_overview_2017"]  # not in the source bib
    assert not plan.ok


def test_unresolved_key_writes_nothing(seed_repo, zotero_home, capsys):
    assert main(args(seed_repo, zotero_home)) == 1
    out = capsys.readouterr().out
    assert "UNRESOLVED masson_overview_2017: not a Zotero key and not in any source bib" in out
    assert "Nothing written." in out
    assert not (seed_repo / "thesis").exists()
    assert not (seed_repo / "kb" / "papers").exists()


@pytest.fixture
def resolvable(seed_repo):
    bib = seed_repo / SOURCE_BIBS[0]
    bib.write_text(bib.read_text() + "@article{masson_overview_2017,\n  doi = {10.1000/masson},\n}\n")
    return seed_repo


def test_seed_writes_bib_map_stubs_and_pdfs(resolvable, zotero_home, capsys):
    assert main(args(resolvable, zotero_home)) == 0
    out = capsys.readouterr().out
    assert "5 cited keys -> 3 papers (3 remapped to Zotero keys)" in out
    assert "NO PDF bradshawInterpretationHDX2020" in out

    bib = (resolvable / "thesis/references.bib").read_text()
    assert bib.index("@article{andersonHDXMSMDSimulations2022,") < bib.index("@article{bradshawInterpretationHDX2020,")
    assert "@comment" not in bib

    rows = (resolvable / "thesis/citekey-map.tsv").read_text().splitlines()
    assert rows[0] == "source_key\tcanonical_key\tmatched_by\tfirst_cited_in"
    assert f"anderson_hdx-ms_2022\tandersonHDXMSMDSimulations2022\tdoi\t{TEX[0]}:2" in rows

    pdf = resolvable / "kb/_pdf/@andersonHDXMSMDSimulations2022.pdf"
    assert pdf.read_bytes() == (zotero_home / "storage/ATT00101/anderson.pdf").read_bytes()

    with_pdf = (resolvable / "kb/papers/@andersonHDXMSMDSimulations2022.md").read_text()
    assert with_pdf.startswith("---\ntype: paper\ncitekey: andersonHDXMSMDSimulations2022\nyear: 2022\n")
    assert "pdf: kb/_pdf/@andersonHDXMSMDSimulations2022.pdf\nextraction: auto\nneeds_review: false\n" in with_pdf
    assert "# HDX-MS and MD Simulations (2022)" in with_pdf
    assert "## Claims" in with_pdf  # body comes from the real template

    no_pdf = (resolvable / "kb/papers/@bradshawInterpretationHDX2020.md").read_text()
    assert 'pdf:\nextraction: none\nneeds_review: true\nreview_reason: "No PDF in Zotero; add kb/_pdf/@<citekey>.pdf' in no_pdf


def test_seed_output_passes_the_lint(resolvable, zotero_home):
    assert main(args(resolvable, zotero_home)) == 0
    sys.path.insert(0, str(TOOLS / "kb-lint"))
    from lint import run
    issues = [str(i) for i in run(resolvable).issues]
    assert issues == []


def test_rerun_overwrites_nothing(resolvable, zotero_home, capsys):
    assert main(args(resolvable, zotero_home)) == 0
    note = resolvable / "kb/papers/@andersonHDXMSMDSimulations2022.md"
    note.write_text(note.read_text() + "\nMy notes.\n")
    pdf = resolvable / "kb/_pdf/@andersonHDXMSMDSimulations2022.pdf"
    pdf.write_bytes(b"%PDF-1.4 my own copy")
    capsys.readouterr()
    assert main(args(resolvable, zotero_home)) == 0
    assert "0 new bib entries, 0 new paper notes, 0 PDFs to copy" in capsys.readouterr().out
    assert note.read_text().endswith("\nMy notes.\n")
    assert pdf.read_bytes() == b"%PDF-1.4 my own copy"


def test_existing_bib_entries_are_kept(resolvable, zotero_home):
    bib = resolvable / "thesis/references.bib"
    bib.parent.mkdir(parents=True)
    bib.write_text("@book{zzzMine2000,\n  title = {Kept},\n}\n")
    assert main(args(resolvable, zotero_home)) == 0
    text = bib.read_text()
    assert "@book{zzzMine2000," in text and text.index("andersonHDXMS") < text.index("zzzMine2000")


def test_missing_library_entry_writes_nothing(resolvable, zotero_home, capsys):
    lib = resolvable / LIBRARY
    lib.write_text(lib.read_text().replace("@article{bradshawInterpretationHDX2020,", "@article{renamedElsewhere2020,"))
    assert main(args(resolvable, zotero_home)) == 1
    assert "MISSING bradshawInterpretationHDX2020" in capsys.readouterr().out
    assert not (resolvable / "thesis").exists()


def test_unreadable_zotero_pdf_is_not_copied(resolvable, zotero_home, capsys):
    (zotero_home / "storage/ATT00101/anderson.pdf").write_bytes(b"%PDF-1.5 truncated download")
    assert main(args(resolvable, zotero_home)) == 0
    assert "UNREADABLE andersonHDXMSMDSimulations2022" in capsys.readouterr().out
    assert not (resolvable / "kb/_pdf/@andersonHDXMSMDSimulations2022.pdf").exists()
    note = (resolvable / "kb/papers/@andersonHDXMSMDSimulations2022.md").read_text()
    assert 'extraction: none\nneeds_review: true\nreview_reason: "PDF in Zotero has no readable text' in note


def test_dry_run_writes_nothing(resolvable, zotero_home, capsys):
    assert main(args(resolvable, zotero_home, "--dry-run")) == 0
    assert "Dry run: nothing written." in capsys.readouterr().out
    assert not (resolvable / "thesis").exists()
    assert not (resolvable / "kb/_pdf").exists()
