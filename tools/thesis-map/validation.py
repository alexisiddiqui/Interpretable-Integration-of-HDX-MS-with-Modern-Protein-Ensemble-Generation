"""Schema, graph, pagination and source-evidence checks shared by every profile."""

from collections import Counter
import json
from pathlib import Path
import re

from normalize import SCHEMA_VERSION, LEAVES
from page_labels import page_index


def normalized(text):
    return re.sub(r"[^a-z0-9]", "", text.lower())


def validate(document, pages=None, diagnostics=None):
    if not isinstance(document, dict):
        return ["A thesis map must be a JSON object."], []
    if document.get("schema_version") != SCHEMA_VERSION:
        return [
            f'Unsupported schema_version {document.get("schema_version")!r}; expected {SCHEMA_VERSION}.'
        ], []
    try:
        from jsonschema import Draft202012Validator
    except ImportError as exc:
        raise ValueError(
            "Missing jsonschema. Install tools/thesis-map/requirements.txt with your Python interpreter."
        ) from exc
    schema = json.loads(Path(__file__).with_name("schema.json").read_text())
    failures = [
        f'{"/".join(map(str, e.absolute_path)) or "document"}: {e.message}'
        for e in Draft202012Validator(schema).iter_errors(document)
    ]
    warnings = []
    if failures:
        return failures, warnings
    diagnostics = diagnostics or {}
    failures.extend(str(x) for x in diagnostics.get("failures", []))
    failures.extend(
        "Unresolved cross-reference: " + str(x)
        for x in diagnostics.get("unresolved", [])
    )
    index = page_index(document)
    mapping = document["pagemap"]["pages"]
    if [p["pdf_index"] for p in mapping] != list(
        range(1, document["meta"]["pdf_pages"] + 1)
    ):
        failures.append("pagemap must cover every PDF page once, in PDF order.")
    used_labels = [p["label"] for p in mapping if p["label"] is not None]
    if len(used_labels) != len(set(used_labels)):
        failures.append("pagemap contains duplicate thesis page labels.")
    for p in mapping:
        if (p["label"] is None) != (p["status"] == "unnumbered"):
            failures.append(
                f'Inconsistent numbering status for PDF page {p["pdf_index"]}.'
            )
    nodes = document["structure"]["nodes"]
    stages = document["journey"]["stages"]
    stage_ids = {s["id"] for s in stages}

    def unique(records, name):
        duplicates = [i for i, n in Counter(r["id"] for r in records).items() if n > 1]
        if duplicates:
            failures.append(f"Duplicate {name} IDs: {duplicates}")

    for name, records in [
        ("stages", stages),
        ("claims", document["links"]["claims"]),
        ("edges", document["links"]["edges"]),
        ("entities", document["links"]["entities"]),
        ("contributions", document["journey"]["contributions"]),
        ("negative results", document["journey"]["negative_results"]),
        ("observations", document["quality"]["observations"]),
    ]:
        unique(records, name)

    def references(ids, valid, where):
        for i in ids:
            if i is not None and i not in valid:
                failures.append(f"{where}: missing reference {i!r}.")

    def check_pages(values, where):
        references(values, index, where + " page")

    def check_span(span, where):
        for k in ("start", "end"):
            label = span[k]
            if index.get(label) != span["pdf_" + k]:
                failures.append(f"{where}: inconsistent {k} page mapping.")
        if span["pdf_start"] > span["pdf_end"]:
            failures.append(f"{where}: reversed page range.")

    roots = document["structure"]["roots"]
    references(roots, nodes, "roots")
    if set(roots) != {i for i, n in nodes.items() if n["parent"] is None}:
        failures.append("roots must include exactly the parentless nodes.")
    for i, n in nodes.items():
        if i != n["id"]:
            failures.append(f"Node dictionary key {i!r} does not match node ID.")
        references([n["parent"]] + n["children"] + n["figures"] + n["tables"], nodes, i)
        check_pages(n["source_pages"], i)
        check_span(n["pages"], i)
        check_span(n["own_pages"], i + " own text")
        if (
            not n["pages"]["pdf_start"]
            <= n["own_pages"]["pdf_start"]
            <= n["own_pages"]["pdf_end"]
            <= n["pages"]["pdf_end"]
        ):
            failures.append(f"{i}: own text lies outside section range.")
        seen = {i}
        parent = n["parent"]
        expected_depth = 0
        while parent in nodes:
            if parent in seen:
                failures.append(f"Hierarchy cycle at {i}.")
                break
            seen.add(parent)
            expected_depth += 1
            parent = nodes[parent]["parent"]
        if n["level"] != expected_depth:
            failures.append(f"{i}: level does not match ancestry.")
        for c in n["children"]:
            if c in nodes and nodes[c]["parent"] != i:
                failures.append(f"{i}: child {c} has a different parent.")
        p = nodes.get(n["parent"])
        if p:
            if i not in p["children"]:
                failures.append(f"{i}: missing from parent children.")
            if (
                n["kind"] not in LEAVES
                and not p["pages"]["pdf_start"]
                <= n["pages"]["pdf_start"]
                <= n["pages"]["pdf_end"]
                <= p["pages"]["pdf_end"]
            ):
                failures.append(f"{i}: textual section lies outside parent range.")
        for kind, key in [("figure", "figures"), ("table", "tables")]:
            expected = [
                c for c in n["children"] if c in nodes and nodes[c]["kind"] == kind
            ]
            if n[key] != expected:
                failures.append(f"{i}: {key} must identify direct {kind} children.")
        for key in ("n_figures", "n_tables"):
            own_key = "figures" if key == "n_figures" else "tables"
            expected = len(n[own_key]) + sum(
                nodes[c][key] for c in n["children"] if c in nodes
            )
            if n[key] != expected:
                failures.append(f"{i}: inconsistent {key}.")
    negative_ids = {n["id"] for n in document["journey"]["negative_results"]}
    for s in stages:
        references(s["chapters"] + s["nodes"], nodes, s["id"])
        references([s["next"]], stage_ids, s["id"])
        references(s["negative_results"], negative_ids, s["id"])
        check_pages(s["source_pages"], s["id"])
        if not s["evidence"]:
            failures.append(f'{s["id"]}: stage lacks evidence.')
        if s["role"] == "research" and s["outcome"] is None:
            failures.append(f'{s["id"]}: research stage lacks an outcome.')
        for e in s["evidence"]:
            references([e["node"]], nodes, s["id"] + " evidence")
            check_span(e["pages"], s["id"] + " evidence")
    for c in document["links"]["claims"] + document["journey"]["negative_results"]:
        references([c["node"]], nodes, c["id"])
        references([c["stage"]], stage_ids, c["id"])
        references(c["evidence_nodes"], nodes, c["id"])
        check_pages(c["source_pages"], c["id"])
    for c in document["journey"]["contributions"]:
        references(c["nodes"], nodes, c["id"])
        references([c["stage"]], stage_ids, c["id"])
        check_pages(c["source_pages"], c["id"])
    for t in document["journey"]["transitions"]:
        references([t["from_stage"], t["to_stage"]], stage_ids, "transition")
        check_pages(t["source_pages"], "transition")
    for e in document["links"]["edges"]:
        references([e["source"], e["target"]], nodes, e["id"])
        check_pages(e["source_pages"], e["id"])
        references([e["type"]], document["links"]["edge_types"], e["id"])
        if not e["source_pages"]:
            failures.append(f'{e["id"]}: edge lacks evidence pages.')
        if not e["reason"].strip():
            failures.append(f'{e["id"]}: edge lacks a reason.')
        for occurrence in e["occurrences"]:
            check_pages([occurrence["page"]], e["id"])
    if set(document["links"]["edge_types"]) != {
        e["type"] for e in document["links"]["edges"]
    }:
        failures.append("edge_types must describe exactly the types present in edges.")
    for e in document["links"]["entities"]:
        references(
            list(e["chapters"]) + e["sections"] + [e["first_node"]], nodes, e["id"]
        )
        check_pages(e["source_pages"], e["id"])
        for v in e["chapters"].values():
            check_pages(v["pages"], e["id"])
        if not e["total_mentions"]:
            failures.append(f'{e["id"]}: entity has zero mentions.')
    for o in document["quality"]["observations"]:
        check_pages(o["source_pages"], o["id"])
    # Every quote is checked, including short caption excerpts and journey quotes.
    quoted = list(nodes.values()) + stages + document["links"]["claims"]
    for record in quoted:
        q = record.get("quote")
        if not q:
            continue
        check_pages([q["page"]], record["id"] + " quote")
        if len(q["text"].split()) >= 25:
            failures.append(f'{record["id"]}: quote must be under 25 words.')
        if pages is not None and q["page"] in index:
            i = index[q["page"]] - 1
            evidence = pages[i] + (" " + pages[i + 1] if i + 1 < len(pages) else "")
            if normalized(q["text"]) not in normalized(evidence):
                failures.append(
                    f'{record["id"]}: quote not found on cited page (or its continuation).'
                )
    if pages is not None:
        for check in diagnostics.get("source_checks", []):
            check_pages(check["source_pages"], check["record"] + " source check")
            selected = [index[p] - 1 for p in check["source_pages"] if p in index]
            if check.get("continuation"):
                selected += [i + 1 for i in selected if i + 1 < len(pages)]
            body = normalized(" ".join(pages[i] for i in selected))
            missing = [
                alts[0]
                for alts in check["tokens"]
                if not any(normalized(a) in body for a in alts)
            ]
            if missing:
                failures.append(
                    f'{check["record"]}: evidence tokens not found on cited pages: {missing}.'
                )
    if pages is None:
        warnings.append(
            "Source-text checks were not run; supply --pdf and --profile to validate evidence."
        )
    if document["quality"]["validation"]["failures"]:
        failures.extend(
            "Stored validation failure: " + x
            for x in document["quality"]["validation"]["failures"]
        )
    return list(dict.fromkeys(failures)), list(dict.fromkeys(warnings))


def coverage(document):
    nodes = document["structure"]["nodes"]
    return dict(
        nodes=len(nodes),
        node_kinds=dict(Counter(n["kind"] for n in nodes.values())),
        summaries=sum(bool(n["summary"]) for n in nodes.values()),
        quotes=sum(bool(n["quote"]) for n in nodes.values()),
        stages=len(document["journey"]["stages"]),
        research_stages=sum(
            s["role"] == "research" for s in document["journey"]["stages"]
        ),
        claims=len(document["links"]["claims"]),
        edges=len(document["links"]["edges"]),
        edge_kinds=dict(Counter(e["kind"] for e in document["links"]["edges"])),
        entities=len(document["links"]["entities"]),
        observations=len(document["quality"]["observations"]),
    )
