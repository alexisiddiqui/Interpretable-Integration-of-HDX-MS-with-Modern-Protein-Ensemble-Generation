from model import load_vault, parse_blocks, parse_frontmatter, parse_wikilink


def lines(text):
    return text.splitlines(keepends=True)


def test_frontmatter_parses_fields_and_body_start():
    meta, error, body = parse_frontmatter(lines("---\ntype: claim\nfigures: []\n---\nBody\n"))
    assert meta == {"type": "claim", "figures": []}
    assert error is None
    assert body == 4


def test_unquoted_wikilink_in_frontmatter_gets_a_hint():
    meta, error, _ = parse_frontmatter(lines("---\ncites: [[@a#^c1]]\n---\n"))
    assert meta is None
    assert "quote wikilinks" in error


def test_note_without_frontmatter_has_no_meta_and_no_error():
    assert parse_frontmatter(lines("# Hub\n")) == (None, None, 0)


def test_wikilink_with_and_without_block():
    assert parse_wikilink("[[@smith2020#^c1]]") == ("@smith2020", "c1")
    assert parse_wikilink("[[Protection factor|PF]]") == ("Protection factor", None)
    assert parse_wikilink("@smith2020") is None


def test_blocks_parse_fields_and_skip_comments():
    text = (
        "## Claims\n\n<!--\n- Example. ^c9\n-->\n"
        "- A claim. ^c1\n  - page: 2\n  - quote: \"some words\"\n"
        "  - quote_check: unchecked\n  - reviewed: true\n\n## Other\n- Not a claim\n"
    )
    blocks, problems = parse_blocks(lines(text), 0)
    assert problems == []
    assert [b.id for b in blocks] == ["c1"]
    b = blocks[0]
    assert (b.text, b.page, b.quote, b.quote_check, b.reviewed) == ("A claim.", 2, "some words", "unchecked", True)
    assert b.quote_check_line == 8


def test_block_problems_are_reported():
    text = "## Claims\n- No id here\n- Fine. ^c1\n  - page: zero\n- Again. ^c1\n"
    _, problems = parse_blocks(lines(text), 0)
    assert any("no block ID" in p for p in problems)
    assert any("page must be a whole number" in p for p in problems)
    assert any("^c1 is used twice" in p for p in problems)
    assert any("missing 'quote'" in p for p in problems)


def test_load_vault_skips_templates_and_root_files(repo):
    vault = load_vault(repo)
    rels = {note.kb_rel for note in vault.notes}
    assert "papers/@smith2020.md" in rels
    assert not any(r.startswith("_templates/") for r in rels)
    assert "README.md" not in rels
    assert vault.bib_keys == {"smith2020", "jones2019"}
    assert [b.id for b in vault.find("@smith2020").blocks] == ["c1", "c2"]


def test_citations_map_blocks_to_citing_claims(repo):
    cited = load_vault(repo).citations()
    assert [n.name for n in cited[("@smith2020", "c1")]] == ["HDX-MS constrains ensemble reweighting"]
