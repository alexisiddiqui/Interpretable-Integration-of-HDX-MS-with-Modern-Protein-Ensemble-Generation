import pytest

from helpers import edit
from links import check_links
from model import load_vault

CLAIM = "kb/claims/HDX-MS constrains ensemble reweighting.md"


def messages(repo):
    return [(i.check, i.message) for i in check_links(load_vault(repo))]


def test_fixture_repo_passes(repo):
    assert messages(repo) == []


@pytest.mark.parametrize("old, new, check, expected", [
    ("  - fig-hdx-uptake", "  - fig-missing", 3, "figure 'fig-missing' not found under figures/"),
    ('"[[@smith2020#^c1]]"', '"[[@nobody2000#^c1]]"', 4, "no single note has that name"),
    ('"[[@smith2020#^c1]]"', '"[[@smith2020#^c7]]"', 4, "block ^c7 not found in @smith2020"),
    ('"[[@smith2020#^c1]]"', '"[[@smith2020]]"', 4, "without a block ID"),
    ('"[[@smith2020#^c1]]"', '"[[Protection factor#^c1]]"', 4, "which is not a paper note"),
    ('"[[@smith2020#^c1]]"', '"@smith2020"', 4, "is not a wikilink"),
    ('"[[@smith2020#^c1]]"', '"[[Gap framing]]"', 5, "example theses are never evidence"),
])
def test_claim_link_errors(repo, old, new, check, expected):
    edit(repo, CLAIM, old, new)
    assert any(c == check and expected in m for c, m in messages(repo))


def test_citekey_missing_from_bib(repo):
    edit(repo, "thesis/references.bib", "@book{jones2019,", "@book{jones2018,")
    assert (4, "citekey 'jones2019' is not in thesis/references.bib") in messages(repo)


def test_figure_note_id_must_exist(repo):
    edit(repo, "kb/figures/fig-hdx-uptake.md", "fig_id: fig-hdx-uptake", "fig_id: fig-gone")
    assert (3, "figure 'fig-gone' not found under figures/") in messages(repo)


@pytest.mark.parametrize("bad_id", ['""', '"."', '".."', '"a/b"'])
def test_figure_id_must_be_a_plain_folder_name(repo, bad_id):
    edit(repo, CLAIM, "  - fig-hdx-uptake", f"  - {bad_id}")
    assert any(c == 3 and "is not a valid figure ID" in m for c, m in messages(repo))


CONCEPT = "kb/concepts/Protection factor.md"


@pytest.mark.parametrize("entry, check, expected", [
    ('"[[@smith2020#^c7]]"', 4, "block ^c7 not found in @smith2020"),
    ('"[[@smith2020]]"', 4, "without a block ID"),
    ('"[[Gap framing]]"', 5, "example theses are never evidence"),
])
def test_concept_sources_resolve_like_cites(repo, entry, check, expected):
    edit(repo, CONCEPT, "sources: []", f"sources:\n  - {entry}")
    assert any(c == check and expected in m and m.startswith("sources") for c, m in messages(repo))


def test_concept_source_to_a_real_block_is_fine(repo):
    edit(repo, CONCEPT, "sources: []", 'sources:\n  - "[[@smith2020#^c2]]"')
    assert messages(repo) == []
