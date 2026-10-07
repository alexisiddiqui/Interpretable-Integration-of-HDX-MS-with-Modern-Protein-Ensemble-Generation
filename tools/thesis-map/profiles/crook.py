"""Pure PDF-format adapter. Extraction I/O, schema assembly and validation live in the shared engine."""

import re
import collections
from collections import defaultdict, Counter
from types import SimpleNamespace
from page_labels import roman


def _base(pages, config):
    """Stage 1a: deterministic structure extraction (TOC, positions, words, figures/tables, explicit cross-refs)."""
    import re

    L = []
    for pdf_index, text in enumerate(pages, 1):
        label = roman(pdf_index) if pdf_index <= 30 else str(pdf_index - 30)
        L.extend([f"=====[PDF {pdf_index} | p. {label}]"] + text.split("\n"))
    page_at = []
    pdf_at = []
    cur = "?"
    curpdf = 0
    for l in L:
        m = re.match("=====\\[PDF (\\d+) \\| p\\. (\\w+)\\]", l)
        if m:
            cur = m.group(2)
            curpdf = int(m.group(1))
        page_at.append(cur)
        pdf_at.append(curpdf)
    pdf_first_line = {}
    for i, p in enumerate(pdf_at):
        pdf_first_line.setdefault(p, i)
    toc = [e for e in config["toc"] if e["num"] is not None]
    bynum = {e["num"]: e for e in toc}

    def patch(num, title=None, page=None):
        e = bynum[num]
        if title:
            e["title"] = title
        if page:
            e["page"] = page

    for entry in config["toc_patches"]:
        patch(entry["num"], title=entry.get("title"), page=entry.get("page"))
    extra = config["toc_insertions"]
    order = []
    for e in toc:
        if e["num"] == "Appendix A":
            order.append({"num": "References", "title": "References", "page": 235})
        order.append(e)
        for after, n, t, p in extra:
            if e["num"] == after and after in (
                "4.4.3",
                "7",
                "Appendix A",
                "Appendix B",
                "B.3",
                "Appendix C",
            ):
                if n == "4.5" or n == "B.4" or True:
                    pass
    final = []
    for e in order:
        final.append(e)
        for after, n, t, p in extra:
            if e["num"] == after:
                final.append({"num": n, "title": t, "page": p})
    seen = set()
    uniq = []
    for e in final:
        if e["num"] in seen:
            continue
        seen.add(e["num"])
        uniq.append(e)
    final = uniq

    def nid(num):
        if num == "References":
            return "refs"
        if num.startswith("Appendix "):
            return "app" + num[-1]
        if re.match("^\\d+$", num):
            return "ch" + num
        return "s" + num

    def level(num):
        if (
            num in ("References",)
            or num.startswith("Appendix ")
            or re.match("^\\d+$", num)
        ):
            return 0
        return num.count(".") + (1 if re.match("^[A-C]\\.", num) else 0)

    def parent(num):
        if (
            num == "References"
            or num.startswith("Appendix ")
            or re.match("^\\d+$", num)
        ):
            return None
        if re.match("^[A-C]\\.\\d+$", num):
            return "Appendix " + num[0]
        if re.match("^[A-C]\\.\\d+\\.\\d+$", num):
            return num.rsplit(".", 1)[0]
        p = num.rsplit(".", 1)[0]
        return p if "." in p else p

    def ntype(num, title):
        t = title.lower()
        ch = re.match("^(\\d+)", num)
        if num[0] in "AB C".replace(" ", "") and (not num[0].isdigit()):
            return "appendix"
        if num == "References":
            return "back matter"
        if re.match("^\\d+$", num):
            return None
        if (
            "motivation" in t
            or "abstract" in t
            or "introduction" in t
            or ("literature" in t)
            or ("previous methods" in t)
            or t.startswith("the post")
            or (t in ("proteomics", "mass spectrometry"))
            or ("workflows" in t)
            or ("spatial proteomics" == t)
            or ("statistical inference" == t)
            or ("thesis outline" in t)
            or ("fluorescent" in t)
            or ("proximity" in t)
            or ("fractionation coupled" in t)
            or ("functional data analysis" in t)
            or ("model development" in t)
        ):
            return "background"
        if (
            "discussion" in t
            or "limitations" in t
            or "main findings" in t
            or ("future work" in t)
            or re.match("^8\\.2\\.", num)
        ):
            return "discussion"
        if (
            "result" in t
            or "case study" in t
            or "comparison" in t
            or ("mapping the spatial" in t)
            or ("hyperlopit provides" in t)
            or ("resolution of subcellular" in t)
            or ("simulations" in t)
            or ("applications to" in t)
            or ("rewiring" in t)
            or ("validating experimental" in t)
            or ("uncovering" in t)
            or ("refining" in t)
            or ("improved annotation" in t)
            or ("workflow" in t.split())
            or ("assessing predictive" in t)
        ):
            return "result"
        return "method"

    start_line = 653
    pos = {}

    def find_heading(num, title, frm, to=None):
        to = to or len(L)
        if num == "References":
            pat = re.compile("^References\\s*$")
        elif re.match("^\\d+$", num):
            pat = re.compile("^Chapter %s\\s*$" % num)
        elif num.startswith("Appendix "):
            pat = re.compile("^Appendix %s\\s*$" % num[-1])
        else:
            pat = re.compile(
                "^\\s*%s\\s+%s"
                % (re.escape(num), re.escape(title[:18].replace("  ", " ")))
            )
        for i in range(frm, to):
            s = L[i].strip()
            top = (
                num == "References"
                or re.match("^\\d+$", num)
                or num.startswith("Appendix ")
            )
            if (
                pat.match(s)
                and (top or not re.search("\\s\\d+$", s))
                and (not (re.match("^\\d", s) and re.search("\\.\\s*\\.", s)))
            ):
                return i
        return None

    prev = start_line
    for e in final:
        p = find_heading(e["num"], e["title"], prev)
        if p is None and (not re.match("^[A-C]", e["num"])):
            p = find_heading(e["num"], e["title"], prev)
        e["pos"] = p
        if p is not None:
            prev = p
    missing = [e["num"] for e in final if e["pos"] is None]
    mism = [
        (e["num"], e["page"], page_at[e["pos"]])
        for e in final
        if str(e["page"]) != page_at[e["pos"]]
    ]
    SUBS = config["subheadings"]
    return SimpleNamespace(**locals())


def _structure(B, config):
    import re
    from collections import defaultdict

    L, page_at, pdf_at, final = (B.L, B.page_at, B.pdf_at, B.final)
    figtab = config["figtab"]
    ROMAN = [
        "",
        "i",
        "ii",
        "iii",
        "iv",
        "v",
        "vi",
        "vii",
        "viii",
        "ix",
        "x",
        "xi",
        "xii",
        "xiii",
        "xiv",
        "xv",
        "xvi",
        "xvii",
        "xviii",
        "xix",
        "xx",
        "xxi",
        "xxii",
        "xxiii",
        "xxiv",
        "xxv",
        "xxvi",
        "xxvii",
        "xxviii",
        "xxix",
        "xxx",
    ]

    def lab_to_pdf(lab):
        if lab in ROMAN:
            return ROMAN.index(lab)
        return int(lab) + 30

    nodes = []

    def mk(id, title, num, level, parent, pos, numbered=True, **kw):
        d = dict(
            id=id,
            num=num,
            title=title,
            level=level,
            parent=parent,
            pos=pos,
            numbered=numbered,
        )
        d.update(kw)
        nodes.append(d)
        return d

    FM = [
        ("fm-title", "Title page", 1, 2),
        ("fm-dedication", "Dedication", 3, 3),
        ("fm-declaration", "Declaration", 5, 5),
        ("fm-summary", "Summary", 6, 7),
        ("fm-ack", "Acknowledgements", 9, 9),
        ("fm-preface", "Preface", 10, 10),
        ("fm-toc", "Table of contents", 11, 15),
        ("fm-lof", "List of figures", 17, 21),
        ("fm-lot", "List of tables", 23, 26),
        ("fm-abbrev", "Abbreviations", 27, 29),
    ]
    for id, t, a, b in FM:
        mk(
            id,
            t,
            None,
            0,
            None,
            None,
            numbered=False,
            type="front matter",
            pdf_start=a,
            pdf_end=b,
        )
    numnode = {}
    for e in final:
        num = e["num"]
        i = B.nid(num)
        lv = B.level(num)
        pn = B.parent(num)
        par = B.nid(pn) if pn else None
        d = mk(i, e["title"], num, lv, par, e["pos"], type=B.ntype(num, e["title"]))
        numnode[num] = d
    idxpos = {e["num"]: e["pos"] for e in final}
    for pnum, names in B.SUBS.items():
        parent_node = numnode[pnum]
        a = parent_node["pos"]
        pl = parent_node["level"]
        for k, n in enumerate(names):
            found = None
            for q in range(a, min(a + 1600, len(L))):
                if L[q].strip() == n:
                    found = q
                    break
            assert found, n
            nm = "%s/%s" % (pnum, re.sub("[^a-z0-9]+", "-", n.lower()).strip("-"))
            lv = pl + 1 if pnum != "7.3" else 2
            par = B.nid(pnum)
            mk(
                "u" + nm,
                n,
                None,
                lv,
                par,
                found,
                numbered=False,
                type=parent_node["type"],
            )
    nodes_body = [n for n in nodes if n["pos"] is not None]
    nodes_body.sort(key=lambda n: n["pos"])
    end_of_body = len(L)
    for k, n in enumerate(nodes_body):
        e = end_of_body
        for m in nodes_body[k + 1 :]:
            if m["level"] <= n["level"]:
                e = m["pos"]
                break
        n["end"] = e

    def words(a, b):
        w = 0
        for l in L[a:b]:
            if l.startswith("====="):
                continue
            w += len(re.findall("[A-Za-z][A-Za-z\\-']+", l))
        return w

    byid = {n["id"]: n for n in nodes}
    for n in nodes_body:
        n["approx_words"] = words(n["pos"], n["end"])
        n["pdf_start"] = pdf_at[n["pos"]]
        q = n["end"] - 1
        while q > n["pos"] and (not L[q].strip() or L[q].startswith("=====")):
            q -= 1
        n["pdf_end"] = pdf_at[q]
    for n in nodes:
        if n["pos"] is None:
            a = B.pdf_first_line[n["pdf_start"]]
            b = B.pdf_first_line.get(n["pdf_end"] + 1, len(L))
            n["approx_words"] = words(a, b)
            n["pos"] = None

    def lab(p):
        return (
            B.pm_label(p)
            if hasattr(B, "pm_label")
            else ROMAN[p] if p <= 30 else str(p - 30)
        )

    for n in nodes:
        n["page_start"] = lab(n["pdf_start"])
        n["page_end"] = lab(n["pdf_end"])
        n["pages"] = "p. %s" % (
            n["page_start"]
            if n["page_start"] == n["page_end"]
            else n["page_start"] + "–" + n["page_end"]
        )

    def node_at(i):
        best = None
        for n in nodes_body:
            if n["pos"] <= i < n["end"] and (
                best is None
                or (n["level"] >= best["level"] and n["pos"] >= best["pos"])
            ):
                best = n
        return best

    def node_at_page_front(i):
        p = pdf_at[i]
        for n in nodes:
            if n["pos"] is None and n["pdf_start"] <= p <= n["pdf_end"]:
                return n
        return None

    def node_for_line(i):
        if i < B.start_line:
            return node_at_page_front(i)
        return node_at(i)

    cap_f = {}
    cap_t = {}
    for i, l in enumerate(L):
        if i < B.start_line:
            continue
        s = l.strip()
        m = re.match("^Fig\\. ([0-9A-C]+\\.\\d+)\\b", s)
        if m:
            cap_f.setdefault(m.group(1), i)
        m = re.match("^Table ([0-9A-C]+\\.\\d+)\\b", s)
        if m:
            cap_t.setdefault(m.group(1), i)
    figs = []
    tabs = []
    fallback = []
    for kind, lst, cap, out in (
        ("figure", figtab["figures"], cap_f, figs),
        ("table", figtab["tables"], cap_t, tabs),
    ):
        for f in lst:
            i = cap.get(f["id"])
            how = "caption"
            if i is None:
                i = B.pdf_first_line[lab_to_pdf(str(f["page"]))] + 1
                how = "lof-page"
                fallback.append((kind, f["id"]))
            n = node_at(i)
            out.append(
                dict(
                    id=("fig:" if kind == "figure" else "tab:") + f["id"],
                    label=("Fig. " if kind == "figure" else "Table ") + f["id"],
                    caption=f["title"],
                    page=str(f["page"]),
                    node=n["id"],
                    located=how,
                    source_pages=[str(f["page"])],
                    basis="stated",
                )
            )
    for n in nodes:
        n["figure_ids"] = [f["id"] for f in figs if f["node"] == n["id"]]
        n["table_ids"] = [t["id"] for t in tabs if t["node"] == n["id"]]
    children = defaultdict(list)
    for n in nodes:
        if n["parent"]:
            children[n["parent"]].append(n["id"])

    def tot(nid, key):
        n = byid[nid]
        s = len(n[key])
        for c in children[nid]:
            s += tot(c, key)
        return s

    for n in nodes:
        n["n_figures"] = tot(n["id"], "figure_ids")
        n["n_tables"] = tot(n["id"], "table_ids")
    return SimpleNamespace(**locals())


def _references(S):
    import re
    from collections import defaultdict

    L, page_at, pdf_at = (S.L, S.page_at, S.pdf_at)
    nodes = S.nodes
    byid = S.byid
    sec_ids = {n["num"]: n["id"] for n in nodes if n["num"]}
    fig_ids = {f["id"][4:] for f in S.figs}
    tab_ids = {t["id"][4:] for t in S.tabs}
    ref = S.byid["refs"]
    ref_a, ref_b = (ref["pos"], ref["end"])
    scan = []
    for i, l in enumerate(L):
        p = pdf_at[i]
        if p < 5 or 11 <= p <= 29 or ref_a <= i < ref_b:
            continue
        scan.append(i)

    def expand(s):
        nums = [int(x) for x in re.findall("\\d+", s)]
        if re.search("[-–]", s) and len(nums) == 2:
            return list(range(nums[0], nums[1] + 1))
        return nums

    rx_ch = re.compile("\\b[Cc]hapters?\\s+(\\d+(?:\\s*(?:,|and|&|,\\s*and)\\s*\\d+)*)")
    rx_sec = re.compile("\\b[Ss]ections?\\s+((?:\\d+|[A-C])(?:\\.\\d+)+)")
    rx_app = re.compile("\\b[Aa]ppendi(?:x|ces)\\s+([A-C](?:\\.\\d+)*)\\b")
    rx_appvague = re.compile(
        "\\b(?:in|see|to) the (?:supplementary |)appendix\\b|\\bin the appendix\\b|\\bappendix\\b(?!\\s+[A-C])",
        re.I,
    )
    rx_fig = re.compile("\\b[Ff]ig(?:ure|\\.)s?\\s+([0-9A-C]+\\.\\d+)")
    rx_tab = re.compile("\\b[Tt]able\\s+([0-9A-C]+\\.\\d+)")
    rx_eq = re.compile("\\b[Ee]quations?\\s*\\(?([0-9A-C]+\\.\\d+)\\)?")
    rx_thm = re.compile("\\b(?:[Tt]heorem|[Dd]efinition)\\s+(\\d+)\\b")
    raw = []
    unresolved = []
    stats = defaultdict(int)
    intra_skipped = defaultdict(int)

    def chapter_of(nid):
        n = byid[nid]
        while n["parent"]:
            n = byid[n["parent"]]
        return n["id"]

    def add(src, tgt, typ, line, txt, basis="stated"):
        raw.append(
            dict(
                source=src,
                target=tgt,
                type=typ,
                page=page_at[line],
                text=txt,
                basis=basis,
            )
        )

    for i in scan:
        l0 = L[i]
        s = l0.strip()
        if l0.startswith("====="):
            continue
        nxt = L[i + 1] if i + 1 < len(L) and (not L[i + 1].startswith("=====")) else ""
        l = l0 + " " + nxt.strip()
        _L0 = len(l0)
        src = S.node_for_line(i)
        if src is None:
            continue
        iscap = bool(re.match("^(Fig\\.|Table)\\s", s))
        for m in [x for x in rx_ch.finditer(l) if x.start() < _L0]:
            for n in expand(m.group(1)):
                stats["chapter"] += 1
                t = "ch%d" % n
                if t in byid:
                    if chapter_of(src["id"]) != t:
                        add(src["id"], t, "refers_to_chapter", i, m.group(0))
                    else:
                        intra_skipped["chapter"] += 1
                else:
                    unresolved.append(("chapter", n, page_at[i], s[:80]))
        for m in [x for x in rx_sec.finditer(l) if x.start() < _L0]:
            stats["section"] += 1
            k = m.group(1)
            t = sec_ids.get(k)
            if t:
                if t != src["id"] and (not (byid[t]["parent"] == src["id"] and False)):
                    add(src["id"], t, "refers_to_section", i, m.group(0))
            else:
                unresolved.append(("section", k, page_at[i], s[:80]))
        for m in [x for x in rx_app.finditer(l) if x.start() < _L0]:
            stats["appendix"] += 1
            k = m.group(1)
            t = "app" + k if len(k) == 1 else sec_ids.get(k)
            if t and t in byid:
                add(src["id"], t, "refers_to_appendix", i, m.group(0))
            else:
                unresolved.append(("appendix", k, page_at[i], s[:80]))
        if not iscap:
            for m in [x for x in rx_fig.finditer(l) if x.start() < _L0]:
                stats["figure"] += 1
                k = m.group(1)
                if k in fig_ids:
                    home = None
                    add(src["id"], "fig:" + k, "refers_to_figure", i, m.group(0))
                else:
                    unresolved.append(("figure", k, page_at[i], s[:80]))
            for m in [x for x in rx_tab.finditer(l) if x.start() < _L0]:
                stats["table"] += 1
                k = m.group(1)
                if k in tab_ids:
                    add(src["id"], "tab:" + k, "refers_to_table", i, m.group(0))
                else:
                    unresolved.append(("table", k, page_at[i], s[:80]))
        for m in [x for x in rx_eq.finditer(l) if x.start() < _L0]:
            stats["equation"] += 1
            k = m.group(1)
            c = "ch" + k.split(".")[0] if k[0].isdigit() else "app" + k[0]
            if c in byid and chapter_of(src["id"]) != c:
                add(src["id"], c, "refers_to_equation", i, m.group(0))
            elif c not in byid:
                unresolved.append(("equation", k, page_at[i], s[:80]))
            else:
                intra_skipped["equation"] += 1
        for m in [x for x in rx_thm.finditer(l) if x.start() < _L0]:
            stats["theorem/definition"] += 1
            if chapter_of(src["id"]) != "ch2":
                add(src["id"], "ch2", "refers_to_equation", i, m.group(0))
            else:
                intra_skipped["theorem/definition"] += 1
        if (
            rx_appvague.search(l0)
            and (not rx_app.search(l))
            and (chapter_of(src["id"]) not in ("appA", "appB", "appC", "refs"))
        ):
            c = chapter_of(src["id"])
            tgt = {"ch2": "appA", "ch3": "appA", "ch6": "appB", "ch7": "appC"}.get(c)
            stats["appendix-vague"] += 1
            if (
                tgt
                and src["id"] not in ("appA", "appB", "appC")
                and (not src["id"].startswith(("sA", "sB", "sC")))
            ):
                add(
                    src["id"],
                    tgt,
                    "refers_to_appendix",
                    i,
                    '(unnumbered "appendix")',
                    basis="inferred",
                )
            elif not tgt:
                unresolved.append(("appendix-vague", c, page_at[i], s[:80]))
    agg = {}
    for r in raw:
        k = (r["source"], r["target"], r["type"])
        a = agg.setdefault(
            k,
            dict(
                source=r["source"],
                target=r["target"],
                type=r["type"],
                kind="explicit",
                basis=r["basis"],
                pages=[],
                count=0,
                examples=[],
            ),
        )
        a["count"] += 1
        if r["page"] not in a["pages"]:
            a["pages"].append(r["page"])
        if len(a["examples"]) < 2 and r["text"] not in a["examples"]:
            a["examples"].append(r["text"])
        if r["basis"] == "inferred":
            a["basis"] = "inferred"
    edges = list(agg.values())
    from collections import Counter

    return SimpleNamespace(**locals())


def _annotations(X, config):
    STAGES, CONTRIBUTIONS, NEGATIVE = (
        config["STAGES"],
        config["CONTRIBUTIONS"],
        config["NEGATIVE"],
    )
    JOURNEY_ARC, JOURNEY_CAVEAT = (config["JOURNEY_ARC"], config["JOURNEY_CAVEAT"])
    CHAPTER_META, NODE_META = (config["CHAPTER_META"], config["NODE_META"])
    CLAIMS, ENTITIES, SEMANTIC = (
        config["CLAIMS"],
        config["ENTITIES"],
        config["SEMANTIC"],
    )
    "Stage 1: assemble thesis.json from deterministic extraction + curated content, then validate and print a coverage report."
    import re
    from collections import defaultdict, Counter

    S = X.S
    L, page_at, pdf_at = (S.L, S.page_at, S.pdf_at)
    nodes, byid, figs, tabs = (S.nodes, S.byid, S.figs, S.tabs)
    ROMAN = S.ROMAN

    def label(p):
        return ROMAN[p] if p <= 30 else str(p - 30)

    page_text = defaultdict(str)
    for i, l in enumerate(L):
        if l.startswith("====="):
            continue
        page_text[page_at[i]] += l + "\n"

    def norm(s):
        return re.sub("[\\W_]+", " ", s.lower(), flags=re.U).strip()

    def next_label(lab):
        p = S.lab_to_pdf(lab)
        return label(p + 1) if p < 380 else lab

    npage = {k: norm(v) for k, v in page_text.items()}

    def text_in_pages(pages):
        t = " ".join((npage.get(p, "") for p in pages))
        return t

    problems = []
    notes = []
    out_nodes = []
    for n in sorted(
        nodes,
        key=lambda n: (
            n["pdf_start"],
            n["pos"] if n["pos"] is not None else -1,
            n["level"],
        ),
    ):
        d = {
            k: n[k]
            for k in (
                "id",
                "num",
                "title",
                "level",
                "parent",
                "numbered",
                "pages",
                "page_start",
                "page_end",
                "approx_words",
                "n_figures",
                "n_tables",
                "figure_ids",
                "table_ids",
            )
        }
        d["type"] = n.get("type")
        d["basis"] = "stated"
        d["source_pages"] = [n["page_start"]]
        d["confidence"] = "high"
        if not n["numbered"] and n["pos"] is not None:
            d["kind"] = "unnumbered heading"
            if n["id"].startswith("u7.3/"):
                d["parent_basis"] = "inferred"
                d["confidence"] = "medium"
        cm = CHAPTER_META.get(n["id"])
        if cm:
            d["type"] = cm["type"]
            d["type_basis"] = "inferred"
            d.update({k: v for k, v in cm.items() if k not in ("type",)})
        elif d["type"] and n["pos"] is not None:
            d["type_basis"] = "inferred"
        nm = NODE_META.get(n["id"])
        if nm:
            if "summary" in nm:
                d["summary"] = nm["summary"]
                d["summary_basis"] = "stated"
            if "quote" in nm:
                q, pg = nm["quote"]
                wc = len(q.split())
                if wc >= 25:
                    problems.append(("quote too long", n["id"], wc))
                hit = norm(q) in text_in_pages([pg]) or norm(q) in text_in_pages(
                    [pg, next_label(pg)]
                )
                if not hit:
                    problems.append(("quote not found on page", n["id"], q, pg))
                d["quote"] = dict(text=q, page=pg)
                if pg not in d["source_pages"]:
                    d["source_pages"].append(pg)
        out_nodes.append(d)
    ids = {d["id"] for d in out_nodes}
    children = defaultdict(list)
    for d in out_nodes:
        if d["parent"]:
            children[d["parent"]].append(d["id"])
    for d in out_nodes:
        d["children"] = children[d["id"]]
    valid_labels = set(ROMAN[1:]) | {str(i) for i in range(1, 351)}

    def chk_pages(where, pages):
        for p in pages:
            if p not in valid_labels:
                problems.append(("bad page label", where, p))

    edges = []
    eid = 0
    for e in X.edges:
        if e["type"] == "refers_to_equation" and (
            "Theorem" in " ".join(e["examples"])
            or "theorem" in " ".join(e["examples"])
            or "Definition" in " ".join(e["examples"])
            or ("definition" in " ".join(e["examples"]))
        ):
            continue
        if e["source"] == e["target"]:
            continue
        eid += 1
        edges.append(
            dict(
                id="e%d" % eid,
                source=e["source"],
                target=e["target"],
                type=e["type"],
                kind="explicit",
                basis=e["basis"],
                reason=(
                    "Numbered cross-reference in the text: " + "; ".join(e["examples"])
                    if e["basis"] == "stated"
                    else 'Unnumbered "see appendix" mention inside a chapter that has a single matching appendix'
                ),
                source_pages=e["pages"],
                count=e["count"],
                confidence="high" if e["basis"] == "stated" else "medium",
            )
        )
    n_explicit = len(edges)
    fig_tab_ids = {f["id"] for f in figs} | {t["id"] for t in tabs}
    for s, t, typ, basis, reason, pages, conf in SEMANTIC:
        eid += 1
        edges.append(
            dict(
                id="e%d" % eid,
                source=s,
                target=t,
                type=typ,
                kind="semantic",
                basis=basis,
                reason=reason,
                source_pages=pages,
                count=1,
                confidence=conf,
            )
        )
    all_ids = ids | fig_tab_ids
    ent_ids = {e[0] for e in ENTITIES}
    for e in edges:
        for end in ("source", "target"):
            if e[end] not in all_ids:
                problems.append(("edge endpoint missing", e["id"], e[end]))
        chk_pages("edge " + e["id"], e["source_pages"])
    chap_ranges = {}
    for d in nodes:
        if d["level"] == 0 and d["pos"] is not None:
            chap_ranges[d["id"]] = (d["pos"], d["end"])

    def chapter_scan_order():
        return [c for c in ["ch%d" % i for i in range(1, 9)] + ["appA", "appB", "appC"]]

    entities = []
    for eid_, lab_, kind, pat, flags, gloss in ENTITIES:
        rx = re.compile(pat, flags)
        chs = {}
        pages_by = {}
        for ch in chapter_scan_order():
            a, b = chap_ranges[ch]
            cnt = 0
            first = None
            sample = []
            for i in range(a, b):
                l = L[i]
                if l.startswith("====="):
                    continue
                m = rx.findall(l)
                if m:
                    cnt += len(m)
                    if first is None:
                        first = page_at[i]
                    if page_at[i] not in sample and len(sample) < 4:
                        sample.append(page_at[i])
            if cnt:
                chs[ch] = dict(mentions=cnt, first_page=first, pages=sample)
        main = [c for c in chs if c.startswith("ch")]
        app = [c for c in chs if c.startswith("app")]
        if not chs:
            notes.append(("entity with zero mentions", eid_))
            continue
        firstch = min(chs, key=lambda c: chapter_scan_order().index(c))
        entities.append(
            dict(
                id="ent:" + eid_,
                label=lab_,
                kind=kind,
                gloss=gloss,
                chapters=main,
                appendices=app,
                by_chapter=chs,
                total_mentions=sum((v["mentions"] for v in chs.values())),
                basis="stated",
                confidence="high" if len(pat) > 8 else "medium",
                source_pages=[chs[firstch]["first_page"]],
            )
        )
    ent_ids = {e["id"] for e in entities}
    claims = []
    for c in CLAIMS:
        d = dict(c)
        if d["node"] not in ids:
            problems.append(("claim node missing", d["id"], d["node"]))
        if d["stage"] not in {s["id"] for s in STAGES}:
            problems.append(("claim stage missing", d["id"], d["stage"]))
        for f in d["figures"]:
            if f not in fig_tab_ids:
                problems.append(("claim figure missing", d["id"], f))
        chk_pages("claim " + d["id"], d["source_pages"])
        t = text_in_pages(d["source_pages"] + [next_label(d["source_pages"][-1])])
        miss = [tok for tok in d["check"] if norm(tok) not in t]
        if miss:
            problems.append(
                (
                    "claim token not found on cited pages",
                    d["id"],
                    miss,
                    d["source_pages"],
                )
            )
        d["evidence_checked"] = not miss
        d.pop("check")
        claims.append(d)
    for s in STAGES:
        chk_pages("stage " + s["id"], s["evidence"])
        if not s["evidence"]:
            problems.append(("stage without evidence", s["id"]))
        for ch in s["chapters"]:
            if ch not in ids:
                problems.append(("stage chapter missing", s["id"], ch))
        for sec in s["sections"]:
            if sec not in ids:
                problems.append(("stage section missing", s["id"], sec))
        q = s["quote"]
        if len(q["text"].split()) >= 25:
            problems.append(("stage quote too long", s["id"]))
        if not (
            norm(q["text"]) in text_in_pages([q["page"]])
            or norm(q["text"]) in text_in_pages([q["page"], next_label(q["page"])])
        ):
            problems.append(("stage quote not found", s["id"], q))
        s["claims"] = [c["id"] for c in claims if c["stage"] == s["id"]]
        s["source_pages"] = s["evidence"]
        for p in s["evidence"]:
            if not page_text.get(p, "").strip():
                problems.append(("stage evidence page empty", s["id"], p))
    neg_ids = {n["id"] for n in NEGATIVE}
    for s in STAGES:
        for n in s["negative_results"]:
            if n not in neg_ids:
                problems.append(("negative result missing", s["id"], n))
    for n in NEGATIVE:
        if n["node"] not in ids:
            problems.append(("negative node missing", n["id"], n["node"]))
        for f in n["figures"]:
            if f not in fig_tab_ids:
                problems.append(("negative fig missing", n["id"], f))
        chk_pages("neg " + n["id"], n["source_pages"])
    for k in CONTRIBUTIONS:
        chk_pages("contrib " + k["id"], k["source_pages"])
        for ch in k["chapters"]:
            if ch not in ids:
                problems.append(("contribution chapter missing", k["id"], ch))
    toc = [e for e in config["toc"] if e["num"] is not None]
    toc_nums = {e["num"] for e in S.B.final}
    node_nums = {d["num"] for d in out_nodes if d["num"]}
    toc_missing = sorted(toc_nums - node_nums)
    if toc_missing:
        problems.append(("TOC entries without node", toc_missing))
    front_expected = [
        "Title page",
        "Dedication",
        "Declaration",
        "Summary",
        "Acknowledgements",
        "Preface",
        "Table of contents",
        "List of figures",
        "List of tables",
        "Abbreviations",
    ]
    front_have = [d["title"] for d in out_nodes if d["id"].startswith("fm-")]
    for t in front_expected:
        if t not in front_have:
            problems.append(("front matter missing", t))
    if len(figs) != 120:
        problems.append(("figure count", len(figs)))
    if len(tabs) != 49:
        problems.append(("table count", len(tabs)))
    fig_nodes = Counter((f["node"] for f in figs))
    for f in figs + tabs:
        if f["node"] not in ids:
            problems.append(("figure node missing", f["id"]))
    pagemap = dict(
        rule="Printed page = PDF page index - 30 from the start of chapter 1 (PDF 31 = p. 1); front matter uses roman numerals equal to the PDF index (PDF 11 = p. xi). PDF 16, 22, 30, 216, 294, 324, 350 etc. are blank pages.",
        roman_offset=0,
        arabic_offset=30,
        first_arabic_pdf=31,
        last_pdf=380,
        examples=[
            dict(pdf=1, printed="i"),
            dict(pdf=6, printed="vi"),
            dict(pdf=31, printed="1"),
            dict(pdf=87, printed="57"),
            dict(pdf=380, printed="350"),
        ],
        verified="Running page numbers in the page headers/footers of PDF 31-380 were compared with PDF index - 30: 334 of 350 pages carry a readable number and all match; the other 16 are chapter openers or blank pages.",
    )
    blank = [p for p in range(1, 381) if not page_text.get(label(p), "").strip()]
    pagemap["blank_pdf_pages"] = blank
    chap_ids = ["ch%d" % i for i in range(1, 9)]
    body_words = sum((byid[c]["approx_words"] for c in chap_ids))
    out = dict(
        journey=dict(
            arc=JOURNEY_ARC,
            caveat=JOURNEY_CAVEAT,
            stages=STAGES,
            contribution=CONTRIBUTIONS,
            negative_results=NEGATIVE,
        ),
        structure=dict(nodes=out_nodes, figures=figs, tables=tabs),
        links=dict(
            edges=edges,
            entities=entities,
            edge_types=sorted({e["type"] for e in edges}),
        ),
        claims=claims,
    )
    return (out, problems)


def parse(pages, config):
    import copy

    config = copy.deepcopy(config)
    S = _structure(_base(pages, config), config)
    X = _references(S)
    X.S = S
    document, failures = _annotations(X, config)
    positions = {
        n["id"]: {
            "pdf": n["pdf_start"],
            "line": sum((1 for i in range(n["pos"]) if S.pdf_at[i] == n["pdf_start"]))
            - 1,
        }
        for n in S.nodes
        if n["pos"] is not None
    }
    return (
        document,
        {"failures": failures, "unresolved": X.unresolved, "positions": positions},
    )
