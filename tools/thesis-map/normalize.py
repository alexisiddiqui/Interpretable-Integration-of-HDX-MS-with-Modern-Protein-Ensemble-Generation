"""Assemble the single public schema from format-adapter records."""

import copy
import re
from page_labels import page_index

SCHEMA_VERSION = "2.0.0"
LEAVES = {"figure", "table"}
TYPE_ALIASES = {
    "front matter": "front-matter",
    "front": "front-matter",
    "back matter": "references",
}


def labels(values):
    return list(dict.fromkeys(str(v) for v in values))


def provenance(record):
    return {
        k: record[k]
        for k in (
            "basis",
            "confidence",
            "summary_basis",
            "type_basis",
            "parent_basis",
            "outcome_basis",
        )
        if k in record
    }


def quote(record):
    q = record.get("quote")
    if not q:
        return None
    if isinstance(q, (list, tuple)):
        q = {"text": q[0], "page": q[1]}
    return dict(text=q["text"], page=str(q["page"]))


def make_pagemap(profile, count):
    mapping = copy.deepcopy(profile["pagemap"])
    if len(mapping["pages"]) != count:
        raise ValueError("Profile page map does not match the PDF page count.")
    return mapping


def normalize(native, profile, extraction, diagnostics):
    native = copy.deepcopy(native)
    meta = profile["meta"]
    count = len(diagnostics["pages"])
    result = dict(
        schema_version=SCHEMA_VERSION,
        meta={
            k: v
            for k, v in meta.items()
            if k
            not in (
                "schema_version",
                "page_map",
                "extraction",
                "text_extraction",
                "generated_from",
                "all_page_references_are",
                "convention",
                "source_pdf",
                "pdf_pages",
            )
        },
        pagemap=make_pagemap(profile, count),
    )
    result["meta"].update(
        source_pdf=profile["source_pdf"], pdf_pages=count, extraction=extraction
    )
    for key in ("word_count_source_page",):
        if key in result["meta"]:
            result["meta"][key] = str(result["meta"][key])
    result["meta"]["profile"] = profile["name"]
    result["meta"]["profile_sha256"] = profile["profile_sha256"]
    index = page_index(result)
    by_pdf = {p["pdf_index"]: p["label"] for p in result["pagemap"]["pages"]}

    def span(start, end):
        a, b = str(start), str(end)
        return dict(start=a, end=b, pdf_start=index[a], pdf_end=index[b])

    raw = native["structure"]["nodes"]
    raw = list(raw.values()) if isinstance(raw, dict) else raw
    nodes = {}
    for n in raw:
        p = n["pages"]
        if isinstance(p, dict):
            pages = span(p["start"], p["end"])
        elif isinstance(p, list):
            pages = span(*p)
        else:
            pages = span(n["page_start"], n["page_end"])
        number = n.get("number", n.get("num")) or None
        kind = n.get("kind")
        if kind == "unnumbered heading":
            kind = "run-in"
        if not kind:
            if n["type"] in LEAVES:
                kind = n["type"]
            elif n["type"] in ("front", "front matter", "front-matter"):
                kind = "front"
            elif n["type"] in ("back matter", "references") or n["id"] in (
                "refs",
                "bib",
            ):
                kind = "back"
            elif number and re.fullmatch(r"\d+", str(number)) and n["parent"] is None:
                kind = "chapter"
            elif n["parent"] is None and n["id"].startswith("app"):
                kind = "appendix"
            else:
                kind = "section"
        template = n.get("template")
        if isinstance(template, str):
            template = template.split(" → ")
        publication = copy.deepcopy(n.get("publication"))
        if publication and "pages" in publication:
            publication["source_pages"] = labels(publication.pop("pages"))
        node = dict(
            id=n["id"],
            number=str(number) if number is not None else None,
            title=n["title"],
            kind=kind,
            type=TYPE_ALIASES.get(n["type"], n["type"]),
            parent=n["parent"],
            children=[],
            level=0,
            pages=pages,
            own_pages=copy.deepcopy(pages),
            approx_words=n["approx_words"],
            approx_words_own=n.get("approx_words_own"),
            n_figures=0,
            n_tables=0,
            figures=[],
            tables=[],
            summary=n.get("summary"),
            quote=quote(n),
            template=template,
            publication_status=n.get(
                "publication_status", publication.get("status") if publication else None
            ),
            publication=publication,
            collaboration=n.get("collaboration"),
            journal_pages=str(n["journal_pages"]) if n.get("journal_pages") else None,
            source_pages=labels(n["source_pages"]),
            **provenance(n)
        )
        if kind == "back":
            node["type"] = "references"
        node["annotations"] = {
            k: n[k] for k in ("also", "type_note", "located") if n.get(k) is not None
        }
        nodes[node["id"]] = node
    # Crook's separately stored captions become ordinary leaf nodes.
    for kind, collection in (
        ("figure", native["structure"].get("figures", [])),
        ("table", native["structure"].get("tables", [])),
    ):
        for f in collection:
            nodes[f["id"]] = dict(
                id=f["id"],
                number=f["id"].split(":", 1)[-1],
                title=f["label"] + " · " + f["caption"],
                kind=kind,
                type=nodes[f["node"]]["type"],
                parent=f["node"],
                children=[],
                level=0,
                pages=span(f["page"], f["page"]),
                own_pages=span(f["page"], f["page"]),
                approx_words=0,
                approx_words_own=0,
                n_figures=0,
                n_tables=0,
                figures=[],
                tables=[],
                summary=f["caption"],
                quote=None,
                template=None,
                publication_status=None,
                publication=None,
                collaboration=None,
                journal_pages=None,
                source_pages=labels(f["source_pages"]),
                annotations={"located": f.get("located")},
                **provenance(f)
            )

    def depth(i, trail=()):
        if i in trail:
            raise ValueError("Hierarchy cycle: " + " → ".join(trail + (i,)))
        p = nodes[i]["parent"]
        return 0 if p is None else depth(p, trail + (i,)) + 1

    for n in nodes.values():
        n["level"] = depth(n["id"])
        if n["parent"] is not None:
            nodes[n["parent"]]["children"].append(n["id"])
        if n["kind"] in LEAVES:
            n["type"] = nodes[n["parent"]]["type"]
            if n["kind"] == "figure" and n["number"]:
                n["number"] = re.sub(
                    r"^(?:Journal )?(?:Fig\.|Figure)\s+", "", n["number"]
                )
            if n["kind"] == "table" and n["number"]:
                n["number"] = re.sub(r"^(?:Journal )?Table\s+", "", n["number"])
            if n["journal_pages"]:
                result["pagemap"]["pages"][n["pages"]["pdf_start"] - 1][
                    "alternate_labels"
                ].append(
                    {
                        "label": n["journal_pages"],
                        "source": "Chem. Sci. embedded article",
                    }
                )
    # Exact heading positions distinguish own text from the inclusive subtree span.
    positions = diagnostics.get("positions", {})
    ordered = sorted(
        (i for i in positions if i in nodes),
        key=lambda i: (
            positions[i]["pdf"],
            positions[i].get("offset", positions[i].get("line", 0)),
            nodes[i]["level"],
        ),
    )
    for k, i in enumerate(ordered):
        n = nodes[i]
        pos = positions[i]
        a = pos["pdf"]
        next_pos = positions[ordered[k + 1]] if k + 1 < len(ordered) else None
        b = min(
            n["pages"]["pdf_end"],
            next_pos["pdf"] if next_pos else n["pages"]["pdf_end"],
        )
        if by_pdf.get(a) is not None and by_pdf.get(b) is not None:
            n["own_pages"] = span(by_pdf[a], by_pdf[max(a, b)])

    def roll(i):
        n = nodes[i]
        for c in n["children"]:
            roll(c)
        textual = [nodes[c] for c in n["children"] if nodes[c]["kind"] not in LEAVES]
        if textual:
            b = max([n["pages"]["pdf_end"]] + [c["pages"]["pdf_end"] for c in textual])
            n["pages"] = span(n["pages"]["start"], by_pdf[b])
        n["figures"] = [c for c in n["children"] if nodes[c]["kind"] == "figure"]
        n["tables"] = [c for c in n["children"] if nodes[c]["kind"] == "table"]
        n["n_figures"] = len(n["figures"]) + sum(
            nodes[c]["n_figures"] for c in n["children"]
        )
        n["n_tables"] = len(n["tables"]) + sum(
            nodes[c]["n_tables"] for c in n["children"]
        )
        if n["approx_words_own"] is None:
            n["approx_words_own"] = max(
                0, n["approx_words"] - sum(c["approx_words"] for c in textual)
            )

    roots = native["structure"].get(
        "roots", [i for i, n in nodes.items() if n["parent"] is None]
    )
    for i in roots:
        roll(i)
    result["structure"] = dict(
        roots=roots, nodes=nodes, note=native["structure"].get("note")
    )
    stages = []
    journey = native["journey"]
    source_stages = (
        ([journey["origin"]] if journey.get("origin") else [])
        + journey["stages"]
        + ([journey["destination"]] if journey.get("destination") else [])
    )
    for s in source_stages:
        role = (
            "origin"
            if s is journey.get("origin")
            else "destination" if s is journey.get("destination") else "research"
        )
        evidence = []
        for e in s.get("evidence", []):
            if isinstance(e, dict):
                evidence.append(
                    dict(node=e["node"], pages=span(e["pages"][0], e["pages"][-1]))
                )
            else:
                evidence.append(dict(node=None, pages=span(e, e)))
        source_pages = labels(
            [p for e in evidence for p in (e["pages"]["start"], e["pages"]["end"])]
        )
        stages.append(
            dict(
                id=s["id"],
                role=role,
                title=s["title"],
                question=s.get("question"),
                approach=s.get("approach"),
                outcome=s.get("outcome"),
                outcome_note=s.get("outcome_note"),
                why_next=s.get("why_next"),
                next=s.get("next"),
                chapters=s["chapters"],
                nodes=s.get(
                    "nodes",
                    s.get("sections", [e["node"] for e in evidence if e["node"]]),
                ),
                evidence=evidence,
                source_pages=source_pages,
                quote=quote(s),
                negative_result=s.get(
                    "negative_result", bool(s.get("negative_results"))
                ),
                negative_results=s.get("negative_results", []),
                **provenance(s)
            )
        )
    for a, b in zip(stages, stages[1:]):
        if a["next"] is None:
            a["next"] = b["id"]
    contributions = []
    for k, c in enumerate(journey["contribution"], 1):
        contributions.append(
            dict(
                id=c.get("id", "contribution-" + str(k)),
                text=c["text"],
                stage=c.get("stage"),
                nodes=c.get("nodes", c.get("chapters", [])),
                source_pages=labels(c.get("source_pages", c.get("pages", []))),
                **provenance(c)
            )
        )
    negative = []
    for n in journey.get("negative_results", []):
        negative.append(
            dict(
                id=n["id"],
                stage=n["stage"],
                node=n["node"],
                kind=n["kind"],
                text=n["text"],
                evidence_nodes=n["figures"],
                source_pages=labels(n["source_pages"]),
                **provenance(n)
            )
        )
    transitions = []
    for t in journey.get("transitions", []):
        transitions.append(
            dict(
                from_stage=t["from_stage"],
                to_stage=t["to_stage"],
                why=t["why"],
                source_pages=labels(t["pages"]),
                **provenance(t)
            )
        )
    result["journey"] = dict(
        arc=journey["arc"],
        caveat=journey.get("caveat"),
        order_note=journey.get("order_note"),
        stages=stages,
        contributions=contributions,
        negative_results=negative,
        transitions=transitions,
    )
    claims = []
    for c in native.get("claims", native["links"].get("claims", [])):
        rec = dict(
            id=c["id"],
            text=c["text"],
            node=c["node"],
            stage=c["stage"],
            source_pages=labels(c.get("source_pages", c.get("pages", []))),
            evidence_nodes=c.get(
                "evidence_nodes", c.get("figure_ids", c.get("figures", []))
            ),
            evidence=c.get("evidence", c.get("figure")),
            quote=quote(c),
            **provenance(c)
        )
        if "evidence_checked" in c:
            rec["evidence_checked"] = c["evidence_checked"]
        claims.append(rec)
    edges = []
    for e in native["links"]["edges"]:
        typ = e["type"]
        if typ.startswith("xref-"):
            typ = "refers_to_" + typ[5:]
        elif typ.endswith("_ref"):
            typ = "refers_to_" + typ[:-4]
        edges.append(
            dict(
                id=e["id"],
                source=e["source"],
                target=e["target"],
                type=typ,
                kind="explicit" if e["kind"] == "explicit" else "semantic",
                reason=e.get("reason")
                or ("Explicit cross-reference: " + "; ".join(e.get("refs") or [])),
                source_pages=labels(e["source_pages"]),
                count=e.get(
                    "count",
                    len(e.get("occurrences", [])) or len(e.get("refs") or []) or 1,
                ),
                references=e.get("refs") or [],
                occurrences=[
                    {**o, "page": str(o["page"])} for o in e.get("occurrences", [])
                ],
                **provenance(e)
            )
        )
    entities = []
    for e in native["links"]["entities"]:
        raw_chapters = e["chapters"]
        if isinstance(raw_chapters, dict):
            chapters = raw_chapters
        elif "by_chapter" in e:
            chapters = {
                c: dict(count=v["mentions"], pages=v["pages"])
                for c, v in e["by_chapter"].items()
            }
        else:
            chapters = {c: dict(count=None, pages=[]) for c in e["chapters"]}
        chapters = {
            c: dict(count=v.get("count"), pages=labels(v.get("pages", [])))
            for c, v in chapters.items()
        }
        rec = dict(
            id=e["id"],
            name=e.get("name", e.get("label")),
            category=e.get("category", e.get("kind", e.get("type"))),
            description=e.get("description", e.get("gloss")),
            total_mentions=e.get("total_mentions", e.get("n_mentions")),
            chapters=chapters,
            sections=e.get("sections", []),
            first_node=e.get("first_node"),
            source_pages=labels(
                e.get(
                    "source_pages", [p for v in chapters.values() for p in v["pages"]]
                )
            ),
            **provenance(e)
        )
        entities.append(rec)
    edge_types = {}
    for typ in sorted({e["type"] for e in edges}):
        family = (
            "ref"
            if typ.startswith("refers_to_")
            else (
                "flow"
                if typ in ("motivates", "answers_limitation", "builds_on_result")
                else "reuse"
            )
        )
        edge_types[typ] = dict(label=typ.replace("_", " "), family=family)
    result["links"] = dict(
        edges=edges, entities=entities, claims=claims, edge_types=edge_types
    )
    observations = []
    for o in native.get("notes", native.get("quality", {}).get("anomalies", [])):
        observations.append(
            dict(
                id=o["id"],
                kind=o.get("kind", "source anomaly"),
                text=o.get("text", o.get("what")),
                where=o.get("where"),
                source_pages=labels(o["pages"]),
            )
        )
    result["quality"] = dict(
        observations=observations,
        coverage={},
        validation=dict(failures=[], warnings=[]),
    )
    return result
