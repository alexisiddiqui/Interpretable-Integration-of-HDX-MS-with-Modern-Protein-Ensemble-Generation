"""Check 6: a claim only climbs the status ladder (draft -> supported -> in-thesis) on checked evidence."""

from model import Issue, parse_wikilink

EVIDENCE_STATUSES = {"supported", "in-thesis"}


def check_ladder(vault):
    issues = []
    for note in vault.notes:
        meta = note.meta or {}
        status = meta.get("status")
        if note.type != "claim" or status not in EVIDENCE_STATUSES:
            continue

        def error(message):
            issues.append(Issue("error", 6, note.rel, f"status is {status} but {message}"))

        figures = [f for f in meta.get("figures") or [] if isinstance(f, str)]
        cites = [c for c in meta.get("cites") or [] if isinstance(c, str)]
        if not figures and not cites:
            error("the claim has no figures or cites")
        if meta.get("needs_review") is True:
            error("needs_review is true")
        if meta.get("source_state") == "outdated" and not figures:
            error("outdated source text cannot support a claim on its own; add a current figure ID or keep status: draft")
        for entry in cites:
            link = parse_wikilink(entry)
            target = vault.find(link[0]) if link and link[1] else None
            block = target.block(link[1]) if target is not None and target.type == "paper" else None
            if block is None or block.computed == "pass":
                continue
            if block.computed == "fail":
                error(f"cited claim {entry} has quote_check: fail")
            else:  # PDF absent or not checkable: a recorded value is not evidence
                error(f"cited claim {entry} was not verified against its PDF in this run "
                      f"(recorded quote_check: {block.quote_check}); add the PDF under kb/_pdf/")
    return issues
