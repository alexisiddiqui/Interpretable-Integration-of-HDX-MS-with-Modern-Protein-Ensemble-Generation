"""Check 10: one symbol, one meaning across concept notes; kb/notation.md collates them."""

from pathlib import Path

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
    assert "| $D_i(t)$ | deuterium uptake of residue i | — | [[Uptake]] | — |" in text
    assert "| $P_i$ | protection factor of residue i | — | [[Protection factor]], [[Uptake]] | — |" in text
    assert run(repo, write=True).written == []  # second run is a no-op


def test_read_only_run_does_not_write_notation(repo):
    run(repo)
    assert not (repo / NOTATION).exists()


def test_generated_notation_is_not_linted(repo):
    run(repo, write=True)
    assert [str(i) for i in run(repo).issues] == []


# Notation maps: a "## Notation" table in a paper note maps the source's symbols to canonical ones.

MAP_HEADER = "## Notation\n\n| Source | Meaning in this source | Canonical | Note |\n|---|---|---|---|\n"


def add_map(repo, rows, header=MAP_HEADER, key="smith2020"):
    rel = f"kb/papers/@{key}.md"
    path = repo / rel
    path.write_text(path.read_text(encoding="utf-8") + "\n" + header + "".join(rows), encoding="utf-8")
    return rel


def test_map_to_a_declared_canonical_symbol_is_clean(repo):
    add_map(repo, ["| $PF_i$ | protection factor | $P_i$ | |\n"])
    assert notation_issues(run(repo)) == []


def test_map_with_no_canonical_equivalent_is_clean(repo):
    add_map(repo, ["| $\\beta$ | inverse temperature | — | write 1/k_BT |\n"])
    assert notation_issues(run(repo)) == []


def test_map_to_an_undeclared_canonical_symbol_warns_on_the_paper(repo):
    rel = add_map(repo, ["| $E(x)$ | energy | $U(x)$ | |\n"])
    issues = notation_issues(run(repo))
    assert len(issues) == 1, [str(i) for i in issues]
    assert issues[0].severity == "warning"
    assert issues[0].path == rel
    assert "'$E(x)$' maps to canonical '$U(x)$', which no concept declares" in issues[0].message


def test_canonical_symbols_match_after_unwrapping(repo):
    add_concept(repo, "Exchange", [(r"k_\\text{int}", "intrinsic exchange rate")])
    add_map(repo, ["| $k_{rc}$ | random-coil rate | $k_{\\mathrm{int}}$ | |\n"])
    assert notation_issues(run(repo)) == []


def test_notation_heading_without_a_table_warns(repo):
    rel = add_map(repo, ["Symbols as in the source.\n"], header="## Notation\n\n")
    issues = notation_issues(run(repo))
    assert len(issues) == 1, [str(i) for i in issues]
    assert issues[0].path == rel
    assert "Notation section has no table" in issues[0].message


def test_map_row_with_wrong_column_count_warns(repo):
    rel = add_map(repo, ["| $E(x)$ | energy |\n"])
    issues = notation_issues(run(repo))
    assert len(issues) == 1, [str(i) for i in issues]
    assert issues[0].path == rel
    assert "needs 4 columns" in issues[0].message


def test_canonical_cell_must_be_one_symbol_or_dash(repo):
    rel = add_map(repo, ["| $\\beta$ | inverse temperature | 1/k_BT | |\n"])
    issues = notation_issues(run(repo))
    assert len(issues) == 1, [str(i) for i in issues]
    assert "canonical cell must be one $symbol$ or —" in issues[0].message


def test_notation_section_in_a_concept_is_not_a_map(repo):
    write(repo, "kb/concepts/Uptake.md", "---\ntype: concept\naliases: []\nnotation: []\nsources: []\n---\n\n## Notation\n\nProse.\n")
    assert notation_issues(run(repo)) == []


def test_write_lists_source_forms_against_canonical_symbols(repo):
    add_map(repo, ["| $PF_i$ | protection factor | $P_i$ | |\n", "| $\\beta$ | inverse temperature | — | |\n"])
    add_map(repo, ["| $\\mathrm{PF}(i)$ | protection factor | $P_i$ | |\n"], key="jones2019")
    run(repo, write=True)
    text = (repo / NOTATION).read_text(encoding="utf-8")
    assert "| Symbol | Meaning | Units | Defined in | Written in sources |" in text
    assert "| $P_i$ | protection factor of residue i | — | [[Protection factor]] | $\\mathrm{PF}(i)$ ([[@jones2019]]), $PF_i$ ([[@smith2020]]) |" in text
    assert "beta" not in text
    assert run(repo, write=True).written == []


def test_commented_out_map_is_ignored(repo):
    add_map(repo, ["<!-- example\n", MAP_HEADER.split("\n\n", 1)[1], "| $E(x)$ | energy | $V(x)$ | |\n", "-->\n"], header="## Notation\n\n")
    assert notation_issues(run(repo)) == []


def test_template_paper_note_with_an_unfilled_notation_stub_is_clean(repo):
    stub = (Path(__file__).resolve().parents[3] / "kb" / "_templates" / "paper.md").read_text(encoding="utf-8")
    section = stub[stub.index("## Notation"):stub.index("## What I use from it")]
    add_map(repo, [section], header="")
    assert notation_issues(run(repo)) == []
