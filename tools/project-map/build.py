#!/usr/bin/env python3
"""Build the research map from curated repository evidence; no PDF pipeline."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from urllib.parse import quote

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
OUT = ROOT / "research-map"


def latex_text(value: str) -> str:
    value = value.replace(r"{\o}", "ø").replace(r"\o ", "ø")
    value = value.replace("---", "—").replace("--", "–")
    return re.sub(r"\\[a-zA-Z]+\*?", "", value).replace("{", "").replace("}", "")


def headings(path: str) -> list[dict]:
    result = []
    counts = [0, 0, 0]
    for line_no, line in enumerate((ROOT / path).read_text().splitlines(), 1):
        match = re.match(r"\s*\\(section|subsection|subsubsection)(\*?)\{(.*)\}", line)
        if not match:
            continue
        # Section lines may also include a label; balance braces to isolate the title.
        rest = line[line.index("{") + 1:]
        depth, title = 1, []
        for character in rest:
            if character == "{":
                depth += 1
            elif character == "}":
                depth -= 1
            if depth == 0:
                break
            title.append(character)
        level = ["section", "subsection", "subsubsection"].index(match[1])
        counts[level] += 1
        for index in range(level + 1, 3):
            counts[index] = 0
        result.append({"title": latex_text("".join(title)), "level": level,
                       "number": ".".join(map(str, counts[:level + 1])), "line": line_no,
                       "path": path, "href": "../" + quote(path, safe="/")})
    return result


def main() -> None:
    data = json.loads((HERE / "content.json").read_text())
    evidence = {}
    for spec in data.pop("sources"):
        path = (ROOT / spec["path"]).resolve()
        if not path.is_relative_to(ROOT) or not path.is_file():
            raise ValueError(f"Missing or out-of-repository evidence: {spec['path']}")
        raw = path.read_bytes()
        lines = raw.decode().splitlines()
        hits = [index for index, line in enumerate(lines) if spec.get("anchor", "") in line]
        if not hits:
            raise ValueError(f"Evidence anchor not found: {spec['id']}: {spec.get('anchor')}")
        start = hits[spec.get("occurrence", 0)]
        end = min(len(lines), start + spec.get("length", 14))
        evidence[spec["id"]] = {**spec, "start": start + 1, "end": end,
            "excerpt": "\n".join(lines[start:end]), "sha256": hashlib.sha256(raw).hexdigest(),
            "href": "../" + quote(spec["path"], safe="/"), "uses": []}
    data["evidence"] = evidence

    project_ids = {project["id"] for project in data["projects"]}
    record_ids = set()
    for project in data["projects"]:
        for record in [project, *project["claims"], *project["experiments"], *project["modules"]]:
            if record["id"] in record_ids:
                raise ValueError(f"Duplicate record: {record['id']}")
            record_ids.add(record["id"])
            if not record.get("sources"):
                raise ValueError(f"Uncited record: {record['id']}")
            for source_id in record["sources"]:
                if source_id not in evidence:
                    raise ValueError(f"Missing evidence: {record['id']} / {source_id}")
                evidence[source_id]["uses"].append({"project": project["id"], "record": record["id"],
                                                    "title": record.get("title", project["name"])})
        if project.get("parent") and project["parent"] not in project_ids:
            raise ValueError(f"Missing parent for {project['id']}")
        for thesis in project.get("manuscripts", []):
            thesis["headings"] = headings(thesis["path"])
    for edge in data["connections"]:
        if edge["source"] not in project_ids or edge["target"] not in project_ids:
            raise ValueError(f"Broken connection: {edge['id']}")
        if edge["basis"] not in ("stated", "inferred"):
            raise ValueError(f"Missing connection basis: {edge['id']}")
        for source_id in edge["sources"]:
            if source_id not in evidence:
                raise ValueError(f"Missing connection evidence: {edge['id']}")
            evidence[source_id]["uses"].append({"project": edge["target"], "record": edge["id"],
                                                "title": edge["title"]})
    for stage in data["journey"]:
        if stage.get("project") and stage["project"] not in project_ids:
            raise ValueError(f"Missing journey project: {stage['id']}")
        for source_id in stage["sources"]:
            if source_id not in evidence:
                raise ValueError(f"Missing journey evidence: {stage['id']}")
            evidence[source_id]["uses"].append({"project": stage.get("project", "valdx"),
                "record": stage["id"], "title": stage["title"], "view": "journey"})
    for index, observation in enumerate(data["observations"]):
        for source_id in observation["sources"]:
            if source_id not in evidence:
                raise ValueError(f"Missing observation evidence: {observation['title']}")
            evidence[source_id]["uses"].append({"project": "valdx", "record": f"observation-{index}",
                                               "title": observation["title"], "view": "evidence"})

    # Extract the actual current thesis outline, including the newly agreed headings.
    chapters = []
    for chapter_no, include in enumerate(re.findall(r"^\\include\{(chapters/[^}]+)\}",
                                                  (ROOT / "thesis/main.tex").read_text(), re.M), 1):
        path = "thesis/" + include + ".tex"
        text = (ROOT / path).read_text()
        title = re.search(r"\\chapter\{([^}]+)\}", text)[1]
        matched = [p["id"] for p in data["projects"] if p["chapter"] == chapter_no]
        contents = headings(path)
        chapters.append({"number": chapter_no, "title": title, "path": path, "projects": matched,
                         "state": "Outline" if contents else "Chapter placeholder", "headings": contents,
                         "href": "../" + quote(path, safe="/")})
    data["chapters"] = chapters
    data["meta"]["source_method"] = "Curated interpretation of local READMEs, code, reports, and LaTeX; excerpts and headings extracted directly from files."
    data["meta"]["source_count"] = len(evidence)
    data["meta"]["claim_count"] = sum(len(p["claims"]) for p in data["projects"])
    data["meta"]["review_note"] = "Source records substantiate capabilities and reported findings. Research experiments and package test suites were not rerun to build this map."
    template = (HERE / "map_template.html").read_text()
    if template.count("__PROJECT_MAP_DATA__") != 1:
        raise ValueError("Expected exactly one data placeholder")
    embedded = json.dumps(data, ensure_ascii=False).replace("<", "\\u003c").replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")
    html = template.replace("__PROJECT_MAP_DATA__", embedded)
    OUT.mkdir(exist_ok=True)
    (OUT / "map.json").write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    (OUT / "map.html").write_text(html)
    print(f"Built research-map/map.html: {len(data['projects'])} project/workstream records, "
          f"{data['meta']['claim_count']} claims, {len(evidence)} evidence records, {len(chapters)} chapters.")


if __name__ == "__main__":
    main()
