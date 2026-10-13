"""Check 10: one symbol, one meaning across concept notes; kb/notation.md collates them."""

from helpers import write
from lint import run

NOTATION = "kb/notation.md"


def add_concept(repo, name, entries):
    rows = "".join(f'  - {{symbol: "{s}", meaning: "{m}", units: null}}\n' for s, m in entries)
    write(repo, f"kb/concepts/{name}.md", f"---\ntype: concept\naliases: []\nnotation:\n{rows}sources: []\n---\n")
    return f"kb/concepts/{name}.md"


def notation_issues(result):
    return [i for i in result.issues if i.check == 10]


def test_symbol_with_two_meanings_warns_on_the_note_later_in_path_order(repo):
    rel = add_concept(repo, "Site pressure", [("P_i", "pressure at site i")])
    issues = notation_issues(run(repo))
    assert len(issues) == 1, [str(i) for i in issues]
    assert issues[0].severity == "warning"
    assert issues[0].path == rel
    assert "'P_i' means 'pressure at site i' here but 'protection factor of residue i' in [[Protection factor]]" in issues[0].message


def test_same_meaning_ignoring_case_and_punctuation_is_not_a_clash(repo):
    add_concept(repo, "Uptake", [("P_i", "Protection factor of residue i.")])
    assert notation_issues(run(repo)) == []


def test_text_and_mathrm_wrappers_and_braces_are_the_same_symbol(repo):
    add_concept(repo, "Exchange", [(r"k_\\text{int}", "intrinsic exchange rate")])
    add_concept(repo, "Kinetics", [(r"k_{\\mathrm{int}}", "observed exchange rate")])
    issues = notation_issues(run(repo))
    assert len(issues) == 1, [str(i) for i in issues]
    assert issues[0].path == "kb/concepts/Kinetics.md"


def test_write_renders_notation_table(repo):
    add_concept(repo, "Uptake", [("P_i", "protection factor of residue i"), ("D_i(t)", "deuterium uptake of residue i")])
    result = run(repo, write=True)
    assert repo / NOTATION in result.written
    text = (repo / NOTATION).read_text(encoding="utf-8")
    assert "Do not edit by hand" in text
    assert "| $D_i(t)$ | deuterium uptake of residue i | — | [[Uptake]] |" in text
    assert "| $P_i$ | protection factor of residue i | — | [[Protection factor]], [[Uptake]] |" in text
    assert run(repo, write=True).written == []  # second run is a no-op


def test_read_only_run_does_not_write_notation(repo):
    run(repo)
    assert not (repo / NOTATION).exists()


def test_generated_notation_is_not_linted(repo):
    run(repo, write=True)
    assert [str(i) for i in run(repo).issues] == []
