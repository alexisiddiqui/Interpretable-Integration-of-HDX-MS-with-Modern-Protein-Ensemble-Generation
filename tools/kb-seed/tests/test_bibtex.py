from bibtex import find_citations, normalise_doi, normalise_title, parse_bib, plain_title
from seed_helpers import CONF_TEX, LIBRARY_BIB, VALDX_TEX


def test_citations_skip_comments_and_keep_lines(tmp_path):
    tex = tmp_path / "intro.tex"
    tex.write_text(VALDX_TEX, encoding="utf-8")
    found = [(c.key, c.line) for c in find_citations(tex, label="intro.tex")]
    assert found == [
        ("anderson_hdx-ms_2022", 2),
        ("masson_overview_2017", 2),
        ("bradshaw_interpretation_2020", 4),
    ]


def test_citation_spanning_lines(tmp_path):
    tex = tmp_path / "conf.tex"
    tex.write_text(CONF_TEX, encoding="utf-8")
    assert [(c.key, c.line) for c in find_citations(tex)] == [
        ("andersonHDXMSMDSimulations2022", 1),
        ("massonOverviewHydrogenDeuterium2017", 1),
    ]


def test_escaped_percent_is_not_a_comment(tmp_path):
    tex = tmp_path / "pct.tex"
    tex.write_text("Up 50\\% \\cite{a} % \\cite{b}\n", encoding="utf-8")
    assert [c.key for c in find_citations(tex)] == ["a"]


def test_parse_bib_fields_and_verbatim_text(tmp_path):
    bib = tmp_path / "lib.bib"
    bib.write_text(LIBRARY_BIB, encoding="utf-8")
    entries = parse_bib(bib)
    assert set(entries) == {"andersonHDXMSMDSimulations2022", "massonOverviewHydrogenDeuterium2017", "bradshawInterpretationHDX2020"}
    anderson = entries["andersonHDXMSMDSimulations2022"]
    assert (anderson.doi, anderson.year) == ("10.1000/anderson", 2022)
    assert anderson.text.startswith("@article{andersonHDXMSMDSimulations2022,") and anderson.text.endswith("}")
    assert entries["massonOverviewHydrogenDeuterium2017"].doi == "10.1000/masson"
    assert entries["bradshawInterpretationHDX2020"].year == 2020


def test_normalisers():
    assert normalise_doi("https://doi.org/10.1000/ABC ") == "10.1000/abc"
    assert normalise_doi("doi:10.1/x") == "10.1/x"
    assert normalise_title("{HDX}-{MS} and {MD} simulations") == normalise_title("HDX-MS and MD Simulations")
    assert normalise_title("Hydrogen--Deuterium") == normalise_title("Hydrogen–Deuterium")
    assert normalise_title("Caf\\'{e} r\u00e9sum\u00e9") == "caf e resume"
    assert plain_title("{HDX-MS} and {MD} Simulations") == "HDX-MS and MD Simulations"


def _parse_in_process(path, queue):
    try:
        parse_bib(path)
        queue.put("returned")
    except ValueError as err:
        queue.put(str(err))


def test_unclosed_entry_raises_instead_of_looping(tmp_path):
    import multiprocessing

    bib = tmp_path / "truncated.bib"
    bib.write_text("@article{good2020,\n  title = {Fine},\n  year = {2020}\n}\n\n@article{bad2021, title = {Unclosed,\n", encoding="utf-8")
    queue = multiprocessing.Queue()
    proc = multiprocessing.Process(target=_parse_in_process, args=(bib, queue))
    proc.start()
    proc.join(5)
    if proc.is_alive():
        proc.terminate()
        proc.join()
        raise AssertionError("parse_bib did not terminate on an unclosed entry")
    message = queue.get(timeout=2)
    assert "bad2021" in message and "no closing brace" in message
