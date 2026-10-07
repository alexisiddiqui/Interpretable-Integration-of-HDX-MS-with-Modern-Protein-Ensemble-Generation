"""Pure PDF-format adapter. Extraction I/O, schema assembly and validation live in the shared engine."""

import re
import collections
from collections import defaultdict, Counter
from types import SimpleNamespace


def _structure(pages, config):
    TOC, END_PAGE = (config["TOC"], config["END_PAGE"])
    "Stage 1a: structure ranges, word counts, explicit cross-reference edges.\n    Printed page = PDF index - 1 (verified on 244/266 pages, see pagemap.py)."
    import re, collections

    def ptxt(p):
        return pages[p]

    ids = [t[0] for t in TOC]
    node = {
        t[0]: dict(
            id=t[0], parent=t[1], level=t[2], number=t[3], title=t[4], start=t[5]
        )
        for t in TOC
    }
    order = [t[0] for t in TOC]

    def doc_order_key(i):
        return (node[i]["start"], order.index(i))

    flow = sorted(order, key=doc_order_key)

    def find_heading_offset(n):
        t = ptxt(n["start"])
        if n["number"] and n["level"] > 0 or n["id"].startswith("ch"):
            num = n["number"]
            title = n["title"].split(":")[0]
            pats = []
            if n["id"].startswith("ch") and num.isdigit():
                pats = ["Chapter\\s+%s\\b" % num]
            elif n["id"].startswith("app"):
                pats = ["Appendix\\s+%s\\b" % num]
            else:
                pats = [
                    "^\\s*%s\\.?\\s+%s" % (re.escape(num), re.escape(title[:12])),
                    "^\\s*%s\\.?\\s" % re.escape(num),
                ]
            for pat in pats:
                m = re.search(pat, t, re.M)
                if m:
                    return m.start()
        return 0

    for i in order:
        node[i]["heading_off"] = find_heading_offset(node[i])

    def descendants(i):
        out = []
        for j in order:
            p = node[j]["parent"]
            while p:
                if p == i:
                    out.append(j)
                    break
                p = node[p]["parent"]
        return out

    page_off = {}
    buf = []
    pos = 0
    for p in range(0, END_PAGE + 1):
        t = ptxt(p)
        page_off[p] = pos
        buf.append(t)
        pos += len(t) + 1
    G = "\n".join(buf)
    for i in order:
        n = node[i]
        n["abs_start"] = page_off[n["start"]] + n["heading_off"]
    flow = sorted(
        order, key=lambda i: (node[i]["abs_start"], node[i]["level"], order.index(i))
    )
    own = {}
    for k, i in enumerate(flow):
        s = node[i]["abs_start"]
        e = node[flow[k + 1]]["abs_start"] if k + 1 < len(flow) else len(G)
        own[i] = (s, e)

    def abs_to_page(a):
        ps = [p for p in page_off if page_off[p] <= a]
        return max(ps)

    for i in order:
        n = node[i]
        ds = descendants(i)
        starts = [own[i][0]] + [own[d][0] for d in ds]
        ends = [own[i][1]] + [own[d][1] for d in ds]
        s, e = (min(starts), max(ends))
        n["abs_range"] = (s, e)
        n["page_start"] = n["start"]
        n["page_end"] = abs_to_page(max(s, e - 1))
        n["words_own"] = len(G[own[i][0] : own[i][1]].split())
        n["approx_words"] = len(G[s:e].split())
    tops = [i for i in order if node[i]["parent"] is None]
    tops_sorted = sorted(tops, key=lambda i: node[i]["start"])
    for k, i in enumerate(tops_sorted):
        nxt = (
            node[tops_sorted[k + 1]]["start"]
            if k + 1 < len(tops_sorted)
            else END_PAGE + 1
        )
        node[i]["page_end"] = nxt - 1 if node[i]["id"] != "front" else 18
    for i in order:
        n = node[i]
        if n["parent"] is None:
            continue
        sibs = [j for j in order if node[j]["parent"] == n["parent"]]
        idx = sibs.index(i)
        if idx + 1 < len(sibs):
            n["page_end"] = max(
                n["start"],
                node[sibs[idx + 1]]["start"]
                - (0 if node[sibs[idx + 1]]["heading_off"] > 50 else 1),
            )
            if node[sibs[idx + 1]]["heading_off"] > 50:
                n["page_end"] = node[sibs[idx + 1]]["start"]
        else:
            n["page_end"] = node[n["parent"]]["page_end"]
    for i in order:
        kids = [j for j in order if node[j]["parent"] == i]
        if kids and node[i]["level"] >= 1:
            node[i]["page_end"] = max((node[k]["page_end"] for k in kids))
    node["front.title"]["page_end"] = 0
    node["front.proquest"]["page_end"] = 1
    node["front.contents"]["page_end"] = 10
    node["front.abstract"]["page_end"] = 11
    node["front.declaration"]["page_end"] = 12
    node["front.copyright"]["page_end"] = 14
    node["front.epigraph"]["page_end"] = 15
    node["front.ack"]["page_end"] = 16
    node["front.acronyms"]["page_end"] = 18

    def node_at(a):
        best = None
        for i in flow:
            if own[i][0] <= a < own[i][1]:
                best = i
        return best

    BODY_PAGES = list(range(19, 186)) + list(range(211, 232))
    num = "(\\d{1,2}(?:\\.\\d{1,2}){1,2}|[A-C]\\.\\d)"

    def parse_list(s):
        return re.findall(num, s)

    patterns = {
        "section": re.compile(
            "\\b[Ss]ections?\\s+((?:\\d{1,2}(?:\\.\\d{1,2}){0,2}|[A-C]\\.\\d)(?:\\s*(?:,|and|&)\\s*(?:\\d{1,2}(?:\\.\\d{1,2}){0,2}|[A-C]\\.\\d))*)"
        ),
        "chapter": re.compile("\\bChapters?\\s+(\\d(?:\\s*(?:,|and)\\s*\\d)*)"),
        "appendix": re.compile(
            "\\bAppendi(?:x|ces)\\s+([A-C](?:\\.\\d)?(?:\\s*(?:,|and)\\s*[A-C](?:\\.\\d)?)*)"
        ),
        "figure": re.compile(
            "\\b[Ff]ig(?:ure|ures|\\.)\\s+(\\d\\.\\d{1,2}(?:\\s*(?:,|and)\\s*\\d\\.\\d{1,2})*)"
        ),
        "table": re.compile("\\b[Tt]able\\s+(\\d\\.\\d{1,2})"),
        "equation": re.compile(
            "\\b[Ee]q(?:uation|uations|n\\.|\\.)\\s*s?\\s*((?:\\d\\.\\d{1,3}|[A-C]\\.\\d{1,3})(?:\\s*(?:,|and)\\s*(?:\\d\\.\\d{1,3}|[A-C]\\.\\d{1,3}))*)"
        ),
        "page": re.compile("\\bpage\\s+(\\d{1,3})\\b"),
    }

    def valid_section(label):
        return label in node

    fig_node = {
        "2.1": "2.1.3",
        "2.2": "2.2.4",
        "2.3": "2.2.4",
        "3.1": "3.1.1",
        "3.2": "3.1.2",
        "3.3": "3.3",
        "3.4": "3.4.2",
        "3.5": "3.4.2",
        "3.6": "3.4.2",
        "3.7": "3.4.3",
        "3.8": "3.4.3",
        "4.1": "4.2.4",
        "4.2": "4.2.4",
        "4.3": "4.2.5",
        "4.4": "4.2.5",
        "4.5": "4.3.1",
        "4.6": "4.3.1",
        "4.7": "4.3.2",
        "4.8": "4.3.3",
        "5.1": "ch5",
        "5.2": "5.3.1",
        "5.3": "5.3.1",
        "5.4": "5.3.2",
        "5.5": "5.4.1",
        "5.6": "5.4.1",
        "5.7": "5.4.2",
        "5.8": "5.4.2",
        "5.9": "5.4.2",
        "5.10": "5.4.2",
        "5.11": "5.4.2",
        "5.12": "5.4.2",
        "5.13": "5.4.2",
    }
    fig_page = {
        "2.1": 33,
        "2.2": 45,
        "2.3": 46,
        "3.1": 88,
        "3.2": 91,
        "3.3": 99,
        "3.4": 107,
        "3.5": 108,
        "3.6": 108,
        "3.7": 110,
        "3.8": 111,
        "4.1": 132,
        "4.2": 134,
        "4.3": 136,
        "4.4": 136,
        "4.5": 138,
        "4.6": 139,
        "4.7": 140,
        "4.8": 142,
        "5.1": 147,
        "5.2": 163,
        "5.3": 165,
        "5.4": 166,
        "5.5": 169,
        "5.6": 170,
        "5.7": 171,
        "5.8": 172,
        "5.9": 174,
        "5.10": 175,
        "5.11": 177,
        "5.12": 178,
        "5.13": 179,
    }
    tab_node = {"2.1": "2.4.1", "3.1": "3.4.1", "4.1": "4.2.2"}
    tab_page = {"2.1": 59, "3.1": 103, "4.1": 128}
    eq_node = {}
    eq_page = {}

    def chap_of_page(p):
        if p >= 221:
            return "C"
        if p >= 211:
            return "B"
        for t in reversed(tops_sorted):
            if node[t]["start"] <= p and t.startswith("ch"):
                return t[2:]
        return "?"

    for p in BODY_PAGES:
        t = ptxt(p)
        for m in re.finditer("\\(((?:\\d|[A-C])\\.\\d{1,3})\\)\\s*$", t, re.M):
            lab = m.group(1)
            if lab.split(".")[0] != chap_of_page(p):
                continue
            if lab not in eq_node:
                a = page_off[p] + m.start()
                eq_node[lab] = node_at(a)
                eq_page[lab] = p
    EQ_MANUAL = config["EQ_MANUAL"]
    for k, (nd, pg) in EQ_MANUAL.items():
        if k not in eq_node:
            eq_node[k] = nd
            eq_page[k] = pg
    edges = collections.OrderedDict()
    unresolved = []
    selfrefs = 0

    def add_edge(src, dst, rtype, ref_text, page, conf="high"):
        nonlocal selfrefs
        if src == dst:
            selfrefs += 1
            return
        key = (src, dst, rtype)
        e = edges.setdefault(
            key,
            dict(
                source=src,
                target=dst,
                kind="explicit",
                basis="stated",
                type=rtype,
                refs=[],
                source_pages=[],
                confidence=conf,
            ),
        )
        if ref_text not in e["refs"]:
            e["refs"].append(ref_text)
        if page not in e["source_pages"]:
            e["source_pages"].append(page)
        if conf != "high":
            e["confidence"] = conf

    raw_refs = 0
    for p in BODY_PAGES:
        t = ptxt(p)
        for kind, pat in patterns.items():
            for m in pat.finditer(t):
                a = page_off[p] + m.start()
                src = node_at(a)
                if src is None:
                    continue
                raw = m.group(1)
                if kind in ("figure", "table") and t[m.end() : m.end() + 1] == ":":
                    continue
                if kind == "section":
                    labels = re.findall("\\d{1,2}(?:\\.\\d{1,2}){0,2}|[A-C]\\.\\d", raw)
                    for lab in labels:
                        raw_refs += 1
                        tgt = "ch" + lab if "." not in lab and lab.isdigit() else lab
                        if lab in node:
                            tgt = lab
                        if tgt in node:
                            add_edge(src, tgt, "section_ref", f"Section {lab}", p)
                        else:
                            unresolved.append((p, f"Section {lab}"))
                elif kind == "chapter":
                    for lab in re.findall("\\d", raw):
                        raw_refs += 1
                        tgt = "ch" + lab
                        if tgt in node:
                            add_edge(src, tgt, "chapter_ref", f"Chapter {lab}", p)
                        else:
                            unresolved.append((p, f"Chapter {lab}"))
                elif kind == "appendix":
                    for lab in re.findall("[A-C](?:\\.\\d)?", raw):
                        raw_refs += 1
                        tgt = lab if "." in lab else "app" + lab
                        if tgt in node:
                            add_edge(src, tgt, "appendix_ref", f"Appendix {lab}", p)
                        else:
                            unresolved.append((p, f"Appendix {lab}"))
                elif kind == "figure":
                    for lab in re.findall("\\d\\.\\d{1,2}", raw):
                        raw_refs += 1
                        tgt = fig_node.get(lab)
                        if tgt:
                            add_edge(
                                src, tgt, "figure_ref", f"Figure {lab}", p, "medium"
                            )
                        else:
                            unresolved.append((p, f"Figure {lab}"))
                elif kind == "table":
                    lab = raw
                    raw_refs += 1
                    tgt = tab_node.get(lab)
                    if tgt:
                        add_edge(src, tgt, "table_ref", f"Table {lab}", p, "medium")
                    else:
                        unresolved.append((p, f"Table {lab}"))
                elif kind == "equation":
                    for lab in re.findall("(?:\\d|[A-C])\\.\\d{1,3}", raw):
                        raw_refs += 1
                        tgt = eq_node.get(lab)
                        if tgt:
                            add_edge(
                                src, tgt, "equation_ref", f"Eq. {lab}", p, "medium"
                            )
                        else:
                            unresolved.append((p, f"Eq. {lab}"))
                elif kind == "page":
                    raw_refs += 1
                    pg = int(raw)
                    if 0 <= pg <= END_PAGE:
                        cand = [
                            i
                            for i in flow
                            if node[i]["abs_range"][0]
                            <= page_off[pg] + 1
                            < node[i]["abs_range"][1]
                        ]
                        tgt = node_at(page_off[pg] + len(ptxt(pg)) // 2)
                        if tgt:
                            add_edge(src, tgt, "page_ref", f"page {pg}", p, "medium")
                    else:
                        unresolved.append((p, f"page {pg}"))
    return SimpleNamespace(**locals())


def _annotations(X, K, TOC):
    import re, collections

    node = X.node
    order = X.order
    children = collections.defaultdict(list)
    for i in order:
        if node[i]["parent"]:
            children[node[i]["parent"]].append(i)
    LEAF_PARENT = {}

    def top_of(i):
        while i in LEAF_PARENT:
            i = LEAF_PARENT[i]
        while node[i]["parent"]:
            i = node[i]["parent"]
        return i

    def descendants(i):
        out = []
        for c in children[i]:
            out.append(c)
            out += descendants(c)
        return out

    fig_own = collections.defaultdict(list)
    tab_own = collections.defaultdict(list)
    for lab, nid in K.FIG_NODE.items():
        fig_own[nid].append(f"Fig. {lab}")
    for lab, nid in K.TAB_NODE.items():
        tab_own[nid].append(f"Table {lab}")
    for nid, n in K.PAPER_FIGS.items():
        fig_own[nid] += [f"[journal Fig. {k}]" for k in range(1, n + 1)]
    for nid, n in K.PAPER_TABS.items():
        tab_own[nid] += [f"[journal Table {k}]" for k in range(1, n + 1)]
    NO_EXPAND = {"ch3", "ch4", "ch5", "ch1"}
    stage_nodes = {}
    for s in K.STAGES:
        cov = set()
        for n in s["chapters"] + [e["node"] for e in s["evidence"]]:
            cov.add(n)
            if n not in NO_EXPAND:
                cov.update(descendants(n))
        stage_nodes[s["id"]] = sorted(cov, key=order.index)
    node_stages = collections.defaultdict(list)
    for sid, ns in stage_nodes.items():
        for n in ns:
            node_stages[n].append(sid)
    claims_by_node = collections.defaultdict(list)
    for c in K.CLAIMS:
        claims_by_node[c["node"]].append(c["id"])
    nodes_out = []
    for i in order:
        n = node[i]
        kids = children[i]
        sub = [i] + descendants(i)
        figs = []
        tabs = []
        for j in sub:
            figs += fig_own.get(j, [])
            tabs += tab_own.get(j, [])
        t = K.TYPE.get(i)
        if t is None:
            p = n["parent"]
            t = K.TYPE.get(p) or K.TYPE.get(top_of(i)) or "background"
            if i.startswith("front"):
                t = "front"
            if i.startswith("C.") or i.startswith("A."):
                t = "appendix"
        q = K.QUOTE.get(i)
        nodes_out.append(
            dict(
                id=i,
                number=n["number"],
                title=n["title"],
                parent=n["parent"],
                children=kids,
                level=n["level"],
                type=t,
                type_note=K.TYPE_NOTE.get(i),
                template=K.TEMPLATE.get(i),
                pages=[n["page_start"], n["page_end"]],
                source_pages=[n["page_start"], n["page_end"]],
                journal_pages="5497-5529" if i in ("A.1",) else None,
                approx_words=n["approx_words"],
                approx_words_own=n["words_own"],
                n_figures=len(figs),
                n_tables=len(tabs),
                figures=figs,
                tables=tabs,
                n_figures_own=len(fig_own.get(i, [])),
                n_tables_own=len(tab_own.get(i, [])),
                publication=K.PUBLICATION.get(i),
                summary=K.SUMMARY[i],
                summary_basis="paraphrase of stated content",
                quote=dict(text=q[0], page=q[1]) if q else None,
                stages=node_stages.get(i, []),
                claims=claims_by_node.get(i, []),
                basis="stated",
                confidence="high",
                chapter=top_of(i),
            )
        )

    def add_leaf(fid, kind, label, title, parent, page, journal=None, jlabel=None):
        LEAF_PARENT[fid] = parent
        nodes_out.append(
            dict(
                id=fid,
                number=label,
                title=title,
                parent=parent,
                children=[],
                level=3,
                type=kind,
                type_note=None,
                template=None,
                pages=[page, page],
                source_pages=[page, page],
                journal_pages=str(journal) if journal else None,
                approx_words=0,
                approx_words_own=0,
                n_figures=0,
                n_tables=0,
                figures=[],
                tables=[],
                n_figures_own=0,
                n_tables_own=0,
                publication=None,
                summary=title,
                summary_basis="caption title (shortened)",
                quote=None,
                stages=node_stages.get(parent, []),
                claims=[],
                basis="stated",
                confidence="high",
                chapter=top_of(parent),
            )
        )
        for n in nodes_out:
            if n["id"] == parent:
                n["children"] = n["children"] + [fid]

    for lab, ttl in K.FIG_TITLE.items():
        add_leaf(
            "fig." + lab, "figure", "Fig. " + lab, ttl, K.FIG_NODE[lab], K.FIG_PAGE[lab]
        )
    for lab, ttl in K.TAB_TITLE.items():
        add_leaf(
            "tab." + lab, "table", "Table " + lab, ttl, K.TAB_NODE[lab], K.TAB_PAGE[lab]
        )
    for lab, (ttl, pg, jp) in K.PAPER_FIG.items():
        add_leaf("fig." + lab, "figure", "Journal Fig. " + lab[1:], ttl, "A.1", pg, jp)
    for lab, (ttl, pg, jp) in K.PAPER_TAB.items():
        add_leaf("tab." + lab, "table", "Journal Table " + lab[1:], ttl, "A.1", pg, jp)
    node_ids = {n["id"] for n in nodes_out}
    figpat = re.compile(
        "\\b[Ff]ig(?:ure|ures|\\.)\\s+(\\d\\.\\d{1,2}(?:\\s*(?:,|and)\\s*\\d\\.\\d{1,2})*)"
    )
    tabpat = re.compile("\\b[Tt]able\\s+(\\d\\.\\d{1,2})")
    figrefs = collections.OrderedDict()

    def add_fref(src, tgt, ref, page, typ):
        e = figrefs.setdefault(
            (src, tgt), dict(source=src, target=tgt, type=typ, refs=[], source_pages=[])
        )
        if ref not in e["refs"]:
            e["refs"].append(ref)
        if page not in e["source_pages"]:
            e["source_pages"].append(page)

    for p in X.BODY_PAGES:
        t = X.ptxt(p)
        for pat, typ, pre in (
            (figpat, "figure_ref", "fig."),
            (tabpat, "table_ref", "tab."),
        ):
            for m in pat.finditer(t):
                if t[m.end() : m.end() + 1] == ":":
                    continue
                src = X.node_at(X.page_off[p] + m.start())
                for lab in re.findall("\\d\\.\\d{1,2}", m.group(1)):
                    if pre + lab in node_ids and src:
                        add_fref(
                            src,
                            pre + lab,
                            ("Figure " if typ == "figure_ref" else "Table ") + lab,
                            p,
                            typ,
                        )
    for p in range(188, 201):
        t = X.ptxt(p)
        for m in re.finditer("\\b(Fig\\.|Table)\\s?(\\d)\\b", t):
            ls = t.rfind("\n", 0, m.start()) + 1
            catalogue = K.PAPER_FIG if m.group(1) == "Fig." else K.PAPER_TAB
            caption = catalogue.get("J" + m.group(2))
            if m.start() - ls < 3 and caption and (caption[1] == p):
                continue
            pre = "fig.J" if m.group(1) == "Fig." else "tab.J"
            tid = pre + m.group(2)
            if tid in node_ids:
                add_fref(
                    "A.1",
                    tid,
                    f"{m.group(1)} {m.group(2)}",
                    p,
                    "figure_ref" if m.group(1) == "Fig." else "table_ref",
                )
    edges = []
    k = 0
    for e in X.edges.values():
        if e["type"] in ("figure_ref", "table_ref"):
            continue
        k += 1
        edges.append(
            dict(
                id=f"x{k:03d}",
                source=e["source"],
                target=e["target"],
                kind="explicit",
                basis="stated",
                type=e["type"],
                reason=None,
                refs=e["refs"],
                source_pages=sorted(e["source_pages"]),
                confidence=e["confidence"],
                source_chapter=top_of(e["source"]),
                target_chapter=top_of(e["target"]),
            )
        )
    for e in figrefs.values():
        k += 1
        edges.append(
            dict(
                id=f"x{k:03d}",
                source=e["source"],
                target=e["target"],
                kind="explicit",
                basis="stated",
                type=e["type"],
                reason=None,
                refs=e["refs"],
                source_pages=sorted(e["source_pages"]),
                confidence="high",
                source_chapter=top_of(e["source"]),
                target_chapter=top_of(e["target"]),
            )
        )
    for e in K.EXTRA_EXPLICIT:
        k += 1
        edges.append(
            dict(
                id=f"x{k:03d}",
                source=e["source"],
                target=e["target"],
                kind="explicit",
                basis="stated",
                type=e["type"],
                reason=None,
                refs=e["refs"],
                source_pages=e["source_pages"],
                confidence="high",
                source_chapter=top_of(e["source"]),
                target_chapter=top_of(e["target"]),
            )
        )
    k = 0
    for e in K.INFERRED_EDGES:
        k += 1
        d = dict(e)
        d["id"] = f"i{k:03d}"
        d["refs"] = None
        d["source_chapter"] = top_of(e["source"])
        d["target_chapter"] = top_of(e["target"])
        edges.append(d)

    def fig_ids(s):
        if not s:
            return []
        out = []
        for m in re.finditer(
            "(Fig\\.|Table)\\s+(\\d)\\.(\\d+)(?:-(?:(\\d)\\.)?(\\d+))?", s
        ):
            pre = "fig." if m.group(1) == "Fig." else "tab."
            a, c, e = (int(m.group(3)), m.group(2), m.group(5))
            for q in range(a, int(e) + 1 if e else a + 1):
                out.append(f"{pre}{c}.{q}")
        return [x for x in out if x in node_ids]

    for c in K.CLAIMS:
        c["figure_ids"] = fig_ids(c["figure"])
    for n in nodes_out:
        for c in K.CLAIMS:
            if n["id"] in c["figure_ids"]:
                n["claims"] = n["claims"] + [c["id"]]
    BODY = [11] + list(range(19, 186)) + list(range(211, 232))
    BROAD = {
        "e.multipole",
        "e.polar",
        "e.hf",
        "e.dft",
        "k.bondorder",
        "d.glycine",
        "e.kabsch",
        "d.methanol",
    }
    entities = []
    for eid, typ, name, rx, desc in K.ENTITIES:
        pat = re.compile(rx)
        pages = collections.Counter()
        secs = collections.Counter()
        for p in BODY:
            t = X.ptxt(p)
            for m in pat.finditer(t):
                pages[p] += 1
                nid = X.node_at(X.page_off[p] + m.start())
                if nid:
                    secs[nid] += 1
        plist = sorted(pages)
        chaps = sorted({top_of(s) for s in secs}, key=order.index)
        entities.append(
            dict(
                id=eid,
                type=typ,
                name=name,
                description=desc,
                chapters=chaps,
                sections=sorted(secs, key=order.index),
                n_mentions=sum(pages.values()),
                source_pages=plist[:24],
                n_pages=len(plist),
                basis="stated",
                confidence="medium" if eid in BROAD else "high",
            )
        )
    thesis = dict(
        journey=dict(
            arc=K.ARC,
            contribution=K.CONTRIBUTIONS,
            stages=K.STAGES,
            outcome_values=["worked", "partial", "failed", "pivot"],
        ),
        structure=dict(
            nodes=nodes_out, roots=[i for i in order if not node[i]["parent"]]
        ),
        links=dict(
            edges=edges,
            entities=entities,
            claims=K.CLAIMS,
            edge_types=sorted({e["type"] for e in edges}),
        ),
        notes=K.NOTES,
    )
    return thesis


def parse(pages, config):
    import copy

    config = copy.deepcopy(config)
    X = _structure(pages, config)
    document = _annotations(X, SimpleNamespace(**config), config["TOC"])
    positions = {
        n["id"]: {"pdf": n["start"] + 1, "offset": n["heading_off"]}
        for n in X.node.values()
    }
    return (
        document,
        {"failures": [], "unresolved": X.unresolved, "positions": positions},
    )
