from helpers import edit
from model import load_vault
from quotes import PdfText, check_quotes, normalise, write_quote_checks

PAPER = "kb/papers/@smith2020.md"


def run_quotes(repo, tmp_path):
    vault = load_vault(repo)
    issues = check_quotes(vault, PdfText(tmp_path / "cache"))
    return vault, [(i.severity, i.check, i.message) for i in issues]


def test_normalise_handles_ligatures_hyphens_quotes_and_spacing():
    assert normalise("ﬁeld  pro-\ntection “x”") == normalise('field protection "x"')
    assert normalise("force-field") == normalise("force‐\nfield")
    assert normalise("soft­hyphen") == "softhyphen"


def test_pdf_pages_split_and_cache(repo, tmp_path):
    pdf_text = PdfText(tmp_path / "cache")
    pages = pdf_text.pages(repo / "kb/_pdf/@smith2020.pdf")
    assert len(pages) == 3
    assert "protection factors" in pages[0]
    assert len(list((tmp_path / "cache").glob("*.txt"))) == 1


def test_quotes_found_including_across_a_page_break(repo, tmp_path):
    vault, issues = run_quotes(repo, tmp_path)
    assert issues == []
    assert [b.computed for b in vault.find("@smith2020").blocks] == ["pass", "pass"]
    assert [b.computed for b in vault.find("@jones2019").blocks] == [None]  # no PDF, not checked


def test_missing_quote_in_cited_block_is_an_error(repo, tmp_path):
    edit(repo, PAPER, '"reports on backbone amide protection factors"', '"words the paper never said"')
    _, issues = run_quotes(repo, tmp_path)
    assert ("error", 2, "^c1: quote not found on PDF page 1") in issues


def test_missing_quote_in_uncited_unreviewed_block_is_a_warning(repo, tmp_path):
    edit(repo, PAPER, '"The effect carries over to the next page"', '"invented text"')
    _, issues = run_quotes(repo, tmp_path)
    assert ("warning", 2, "^c2: quote not found on PDF page 2") in issues


def test_page_outside_pdf(repo, tmp_path):
    edit(repo, PAPER, "  - page: 2", "  - page: 9")
    _, issues = run_quotes(repo, tmp_path)
    assert ("warning", 2, "^c2: page 9 is outside the PDF (3 pages)") in issues


def test_pdf_not_present_locally_is_a_warning_and_keeps_recorded_state(repo, tmp_path):
    (repo / "kb/_pdf/@smith2020.pdf").unlink()
    vault, issues = run_quotes(repo, tmp_path)
    assert issues == [("warning", 2, "PDF kb/_pdf/@smith2020.pdf not found locally; quotes not checked")]
    assert [b.computed for b in vault.find("@smith2020").blocks] == [None, None]


def test_write_changes_only_quote_check_lines(repo, tmp_path):
    before = (repo / PAPER).read_text(encoding="utf-8")
    vault, _ = run_quotes(repo, tmp_path)
    assert write_quote_checks(vault) == [repo / PAPER]
    after = (repo / PAPER).read_text(encoding="utf-8")
    assert after == before.replace("quote_check: unchecked", "quote_check: pass")
    vault, _ = run_quotes(repo, tmp_path)
    assert write_quote_checks(vault) == []  # nothing left to change


def test_write_fills_an_empty_quote_check_without_eating_the_next_line(repo, tmp_path):
    edit(repo, PAPER, "  - quote_check: unchecked\n  - reviewed: false\n- Reweighting", "  - quote_check:\n  - reviewed: false\n- Reweighting")
    vault, _ = run_quotes(repo, tmp_path)
    write_quote_checks(vault)
    assert "  - quote_check: pass\n  - reviewed: false\n- Reweighting" in (repo / PAPER).read_text(encoding="utf-8")


def test_quote_must_match_whole_words(repo, tmp_path):
    edit(repo, PAPER, '"reports on backbone amide protection factors"', '"ports on backbone amide protection fact"')
    _, issues = run_quotes(repo, tmp_path)
    assert ("error", 2, "^c1: quote not found on PDF page 1") in issues


def test_quote_may_end_at_a_reference_number_glued_to_the_word():
    from quotes import contains_words
    page = normalise("a link between structure, conformational dynamics and function1. HDX-MS measures")
    assert contains_words(page, normalise("conformational dynamics and function"))
    assert not contains_words(page, normalise("conformational dynamics and funct"))


def test_digit_edges_do_not_match_inside_a_number():
    from quotes import contains_words

    assert not contains_words("only 95% of residues were covered", "5% of residues were covered")
    assert not contains_words("sampled 120 000 structures", "20 000 structures")
    assert not contains_words("labelled for 110 ms of labelling", "10 ms of labelling")


def test_reference_digit_after_a_word_and_digit_edge_quote_still_match():
    from quotes import contains_words

    assert contains_words("probes conformational dynamics and function1. hdx", "conformational dynamics and function")
    assert contains_words("only 95% of residues were", "95% of residues")
