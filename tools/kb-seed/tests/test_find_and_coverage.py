from cite_coverage import main as coverage_main
from cite_coverage import missing
from find import main as find_main
from find import search
from seed_helpers import make_pdf

TEX = "intro.tex"


def test_search_reports_pdf_page_index(tmp_path):
    pdf = tmp_path / "p.pdf"
    pdf.write_bytes(make_pdf(["First page.", "Exchange reports on\nprotein dynamics here."]))
    hits = list(search(pdf, r"protein dynamics", tmp_path / "cache", context=20))
    assert [page for page, _ in hits] == [2]
    assert "reports on protein dynamics here" in hits[0][1]  # line breaks collapsed


def test_find_cli(tmp_path, capsys):
    (tmp_path / "kb" / "_pdf").mkdir(parents=True)
    (tmp_path / "kb" / "_pdf" / "@k2020.pdf").write_bytes(make_pdf(["Alpha beta gamma."]))
    assert find_main(["@k2020", "beta", "--root", str(tmp_path)]) == 0
    assert "page 1: ...Alpha beta gamma...." in capsys.readouterr().out
    assert find_main(["@k2020", "delta", "--root", str(tmp_path)]) == 1
    assert find_main(["@missing", "x", "--root", str(tmp_path)]) == 2


def write(root, rel, text):
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def claim(origin, cites=(), body=""):
    cite_lines = "".join(f'  - "{c}"\n' for c in cites)
    return (f"---\ntype: claim\norigin: {origin}\ncites:\n{cite_lines or '  []'}\n---\n\n{body}\n"
            .replace("cites:\n  []", "cites: []"))


def setup(root):
    write(root, TEX, "Intro.\nA sentence.\\cite{old_key,keyB}\nAnother.\\cite{keyC}\n")
    write(root, "thesis/citekey-map.tsv",
          "source_key\tcanonical_key\tmatched_by\tfirst_cited_in\nold_key\tkeyA2020\tdoi\tintro.tex:2\n")


def test_uncovered_citations_are_listed_with_canonical_keys(tmp_path):
    setup(tmp_path)
    assert missing(tmp_path, TEX) == [(2, "old_key", "keyA2020"), (2, "keyB", "keyB"), (3, "keyC", "keyC")]


def test_claims_cover_by_cites_or_body_link_on_the_same_line(tmp_path):
    setup(tmp_path)
    write(tmp_path, "kb/claims/One.md", claim(f"{TEX}#L2", cites=["[[@keyA2020#^c1]]"],
                                              body="Unverified citations: [[@keyB]] (no PDF)"))
    write(tmp_path, "kb/claims/Two.md", claim(f"{TEX}#L9", cites=["[[@keyC#^c1]]"]))  # wrong line
    assert missing(tmp_path, TEX) == [(3, "keyC", "keyC")]


def test_key_prefix_does_not_count(tmp_path):
    setup(tmp_path)
    write(tmp_path, "kb/claims/One.md", claim(f"{TEX}#L3", cites=["[[@keyCa#^c1]]"]))
    assert (3, "keyC", "keyC") in missing(tmp_path, TEX)


def test_coverage_cli(tmp_path, capsys):
    setup(tmp_path)
    assert coverage_main(["--root", str(tmp_path), "--tex", TEX]) == 1
    out = capsys.readouterr().out
    assert "MISSING intro.tex:2 old_key (@keyA2020)" in out
    assert "0 of 3 citations covered" in out


def test_also_stated_in_covers_a_second_location(tmp_path):
    setup(tmp_path)
    write(tmp_path, "kb/claims/One.md", claim("other.tex#L5", cites=["[[@keyC#^c1]]"],
                                              body=f"Also stated in: {TEX}#L3"))
    write(tmp_path, "kb/claims/Two.md", claim(f"{TEX}#L30", cites=["[[@keyA2020#^c1]]", "[[@keyB#^c1]]"]))
    assert missing(tmp_path, TEX) == [(2, "old_key", "keyA2020"), (2, "keyB", "keyB")]  # L30 is not L3 or L2
