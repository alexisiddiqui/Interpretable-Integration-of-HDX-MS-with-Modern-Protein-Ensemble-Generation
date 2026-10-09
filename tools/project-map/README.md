# Repository research map

This independent builder maps the PhD projects from their local repositories,
READMEs, source code, reports, and LaTeX manuscripts. It does not invoke the
PDF thesis-map pipeline, use its schema, or invent thesis pagination.

From the repository root:

```sh
python3 tools/project-map/build.py
```

Open [the map](../../research-map/map.html) directly in a browser. It is a
single offline HTML file with embedded data, search, project details,
connections, thesis headings, and line-numbered source excerpts. The companion
`research-map/map.json` makes the evidence and interpretation reusable.
Relative source-file links work while the HTML remains in `research-map/`.
The embedded excerpts remain available if the HTML is shared on its own.

`content.json` holds curated scientific summaries, claims, questions, and
connections. A source record identifies a repository-relative file, an anchor,
and the length of the excerpt to include. The builder checks references,
extracts actual LaTeX headings, and records source-file SHA-256 fingerprints.
Rebuild after changing sources; curation still requires scientific review.
Output is deterministic for identical source files and curation.

Evidence labels distinguish manuscript findings, visible implementations,
reported checks, research plans, and narrative inference. Historical jaxENT
manuscript results and superseded guidance findings are explicitly qualified.
The map is not an independent validation of the research results.
