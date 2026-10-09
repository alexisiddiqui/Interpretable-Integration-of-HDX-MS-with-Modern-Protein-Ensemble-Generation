"""Checks 3 (figure IDs exist), 4 (cites and citekeys resolve) and 5 (example theses are never cited)."""

from model import Issue, parse_wikilink


def check_links(vault):
    issues = []
    for note in vault.notes:
        meta = note.meta or {}

        def error(check, message):
            issues.append(Issue("error", check, note.rel, message))

        if note.type == "claim":
            for fig_id in _strings(meta.get("figures")):
                if not (vault.root / "figures" / fig_id).is_dir():
                    error(3, f"figure '{fig_id}' not found under figures/")
            for entry in _strings(meta.get("cites")):
                _check_cite(vault, note, entry, error)
        if note.type == "figure" and isinstance(meta.get("fig_id"), str):
            if not (vault.root / "figures" / meta["fig_id"]).is_dir():
                error(3, f"figure '{meta['fig_id']}' not found under figures/")
        if note.type == "paper" and isinstance(meta.get("citekey"), str):
            if meta["citekey"] not in vault.bib_keys:
                error(4, f"citekey '{meta['citekey']}' is not in thesis/references.bib")
    return issues


def _check_cite(vault, note, entry, error):
    link = parse_wikilink(entry)
    if not link:
        error(4, f"cites entry '{entry}' is not a wikilink like [[@key#^c1]]")
        return
    target_name, block_id = link
    target = vault.find(target_name)
    if target is None:
        error(4, f"cites [[{target_name}]] but no single note has that name")
    elif target.in_ref_theses and not note.in_ref_theses:
        error(5, f"cites example-thesis note [[{target_name}]]; example theses are never evidence, cite the primary paper")
    elif target.type != "paper":
        error(4, f"cites [[{target_name}]], which is not a paper note")
    elif block_id is None:
        error(4, f"cites [[{target_name}]] without a block ID; link one claim, e.g. [[{target_name}#^c1]]")
    elif target.block(block_id) is None:
        error(4, f"block ^{block_id} not found in {target_name}")


def _strings(value):
    return [item for item in value if isinstance(item, str)] if isinstance(value, list) else []
