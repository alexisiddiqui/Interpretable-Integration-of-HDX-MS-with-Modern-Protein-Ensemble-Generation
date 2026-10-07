"""Pure PDF-format adapter. Extraction I/O, schema assembly and validation live in the shared engine."""

import re
import collections
from collections import defaultdict, Counter
from types import SimpleNamespace


def _structure(pages, config):
    """Stage 1a: build the structural skeleton (nodes, pages, words, figures, tables) from the PDF text."""
    import re

    def norm(line):
        return re.sub("\\s+", " ", line).strip()

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
    ]

    def printed(idx):
        return str(idx - 22) if idx >= 23 else ROMAN[idx - 2] if idx >= 3 else "cover"

    def pdfidx(p):
        return ROMAN.index(p) + 2 if p in ROMAN else int(p) + 22

    raw = config["toc"]

    def build_nodes():
        nodes = []
        last = {}
        for l in raw:
            num, chap, title, pg = l.split("|")
            if num == "~":
                parent = None
                prev = [n for n in nodes if n["number"]][-1]
                nid = f"{prev['id']}~{re.sub('[^a-z0-9]+', '-', title.lower()).strip('-')}"
                n = dict(
                    id=nid,
                    number=None,
                    title=title,
                    start=pg,
                    parent=prev["id"],
                    kind="run-in",
                )
            else:
                depth = num.count(".")
                if re.fullmatch("\\d+", num):
                    nid = f"ch{num}"
                    parent = None
                elif re.fullmatch("[A-Z]", num):
                    nid = f"app{num}"
                    parent = "app"
                else:
                    nid = f"s{num}"
                    parent = (
                        "app" + num.split(".")[0]
                        if num[0].isalpha()
                        else (
                            f"ch{num.split('.')[0]}"
                            if depth == 1
                            else "s" + ".".join(num.split(".")[:-1])
                        )
                    )
                n = dict(
                    id=nid,
                    number=num,
                    title=title,
                    start=pg,
                    parent=parent,
                    kind=(
                        "chapter"
                        if depth == 0 and (not num.isalpha())
                        else "appendix" if num.isalpha() and depth == 0 else "section"
                    ),
                )
            nodes.append(n)
        return nodes

    def squash(s):
        return re.sub("[^a-z0-9.]", "", s.lower())

    def body_lines(idx):
        """lines of one PDF page, with running header / page number / contents-leader lines removed"""
        out = []
        for k, l in enumerate(pages[idx - 1].split("\n")):
            t = norm(l)
            if not t:
                continue
            if re.search("(\\. ){3,}", t):
                continue
            if re.fullmatch("\\d+|[ivx]+", t):
                continue
            out.append((k, t))
        return out

    def is_header(t):
        return bool(
            re.match("^\\d+ \\d+\\.(\\d+\\.)* ?[A-Z]", t)
            or re.match("^\\d+\\. .+ \\d+$", t)
            or re.match("^[A-Z]\\. .+ \\d+$", t)
            or re.match("^\\d+ [A-Z]\\.\\d+\\.", t)
            or re.match("^\\d+ (References|List of|Appendices?)", t)
            or re.match("^(References|List of Figures|Contents) \\d+$", t)
            or re.match("^\\d+ Contents$", t)
        )

    def locate(nodes):
        for n in nodes:
            idx = pdfidx(n["start"])
            n["pdf_start"] = idx
            want = (
                squash((n["number"] or "") + n["title"])[:34]
                if n["number"]
                else squash(n["title"])[:30]
            )
            n["heading_found"] = False
            n["pos"] = None
            for k, t in body_lines(idx):
                if is_header(t):
                    continue
                s = squash(t)
                if n["kind"] in ("chapter", "appendix"):
                    if squash(n["title"])[:20] in s or (
                        n["kind"] == "appendix" and squash(n["title"])[:14] in s
                    ):
                        n["pos"] = (idx, k)
                        n["heading_found"] = True
                        break
                elif s.startswith(want[: len(want)]) or s.startswith(want[:22]):
                    n["pos"] = (idx, k)
                    n["heading_found"] = True
                    break
            if n["pos"] is None:
                n["pos"] = (idx, 0)
        return nodes

    def words_between(a, b):
        """words from position a (idx,line) up to (not incl.) position b"""
        tot = 0
        for idx in range(a[0], b[0] + 1):
            for k, t in body_lines(idx):
                if is_header(t):
                    continue
                if (idx, k) < a or (idx, k) >= b:
                    continue
                tot += len(t.split())
        return tot

    CAP = re.compile("^(Figure|Table) ([A-Z]?\\d*\\.?\\d+[a-z]?):")

    def captions():
        caps = []
        for idx in range(23, 163):
            for k, t in body_lines(idx):
                m = CAP.match(t)
                if m:
                    caps.append(
                        dict(
                            kind=m.group(1).lower(),
                            label=m.group(2),
                            pdf=idx,
                            line=k,
                            printed=printed(idx),
                        )
                    )
        return caps

    def first_mention(kind, label, chapter_range):
        pat = re.compile(
            "\\b(?:Fig(?:ure)?s?\\.?|Tables?)\\s*" + re.escape(label) + "(?![\\d])"
        )
        pat = re.compile(
            ("\\bFig(?:ure)?s?\\.?\\s*" if kind == "figure" else "\\bTables?\\s*")
            + re.escape(label)
            + "(?!\\d)"
        )
        for idx in range(chapter_range[0], chapter_range[1] + 1):
            for k, t in body_lines(idx):
                if CAP.match(t):
                    continue
                if re.match("^(Figure|Table) \\S+:", t):
                    continue
                if pat.search(t):
                    return (idx, k)
        return None

    def node_at(nodes, pos):
        """deepest node whose own span contains pos"""
        srt = sorted([n for n in nodes if n["pos"]], key=lambda n: n["pos"])
        cur = None
        for n in srt:
            if n["pos"] <= pos:
                cur = n
            else:
                break
        return cur

    def finish():
        nodes = locate(build_nodes())
        byid = {n["id"]: n for n in nodes}
        srt = sorted(nodes, key=lambda n: n["pos"])
        END = (163, 0)
        for i, n in enumerate(srt):
            nxt = srt[i + 1]["pos"] if i + 1 < len(srt) else END
            n["own_words"] = words_between(n["pos"], nxt)
            n["own_end"] = nxt
        kids = {n["id"]: [] for n in nodes}
        for n in nodes:
            if n["parent"] in kids:
                kids[n["parent"]].append(n["id"])

        def total(nid):
            return byid[nid]["own_words"] + sum((total(c) for c in kids[nid]))

        for n in nodes:
            n["approx_words"] = total(n["id"])
        CHEND = {
            "ch1": "31",
            "ch2": "65",
            "ch3": "85",
            "ch4": "102",
            "ch5": "122",
            "ch6": "126",
            "appA": "136",
            "appB": "140",
        }
        for n in nodes:
            if n["id"] in CHEND:
                n["end"] = CHEND[n["id"]]

        def end_page(n):
            if "end" in n:
                return n["end"]
            kid_ends = [end_page(byid[c]) for c in kids[n["id"]]]
            i = srt.index(n)
            nxt = srt[i + 1] if i + 1 < len(srt) else None
            e = (
                printed(nxt["pos"][0])
                if nxt and nxt["kind"] not in ("chapter", "appendix")
                else None
            )
            if e is None:
                e = (
                    byid[n["parent"]]["end"]
                    if n["parent"] in byid and "end" in byid[n["parent"]]
                    else n["start"]
                )
            return max([e] + kid_ends, key=pdfidx)

        for n in srt:
            n["end"] = end_page(n) if "end" not in n else n["end"]
            if pdfidx(n["end"]) < pdfidx(n["start"]):
                n["end"] = n["start"]
        caps = captions()
        chap_rng = {
            "ch1": (23, 54),
            "ch2": (55, 88),
            "ch3": (89, 108),
            "ch4": (109, 124),
            "ch5": (125, 144),
            "ch6": (145, 148),
            "appA": (151, 158),
            "appB": (159, 162),
        }
        for n in nodes:
            n["figures"] = []
            n["tables"] = []
        unplaced = []
        for c in caps:
            ch = [k for k, (a, b) in chap_rng.items() if a <= c["pdf"] <= b][0]
            mp = first_mention(c["kind"], c["label"], chap_rng[ch])
            pos = (
                mp
                if mp and chap_rng[ch][0] <= mp[0] <= chap_rng[ch][1]
                else (c["pdf"], c["line"])
            )
            home = node_at(nodes, pos)
            c["home"] = home["id"]
            c["home_basis"] = (
                "first in-text mention" if mp and pos == mp else "caption location"
            )
            (home["figures"] if c["kind"] == "figure" else home["tables"]).append(
                dict(label=c["label"], page=c["printed"], basis=c["home_basis"])
            )

        def roll(nid, key):
            return len(byid[nid][key]) + sum((roll(c, key) for c in kids[nid]))

        for n in nodes:
            n["n_figures"] = roll(n["id"], "figures")
            n["n_tables"] = roll(n["id"], "tables")
        return (nodes, kids, caps)

    return SimpleNamespace(**locals())


def _references(S):
    finish, printed, pdfidx, body_lines, is_header, CAP, node_at = (
        getattr(S, key)
        for key in [
            "finish",
            "printed",
            "pdfidx",
            "body_lines",
            "is_header",
            "CAP",
            "node_at",
        ]
    )
    'Stage 1b: explicit cross-references ("see Section 3.2", "Chapter 4", "Fig 5.1", "Appendix A.2") -> resolved edges.'
    import re, collections

    nodes, kids, caps = finish()
    byid = {n["id"]: n for n in nodes}

    def ancestors(nid):
        out = []
        p = byid[nid]["parent"]
        while p:
            out.append(p)
            p = byid[p]["parent"] if p in byid else None
        return out

    figtab = {(c["kind"], c["label"]): c["home"] for c in caps}
    CH_RNG = {
        "ch1": (23, 54),
        "ch2": (55, 88),
        "ch3": (89, 108),
        "ch4": (109, 124),
        "ch5": (125, 144),
        "ch6": (145, 148),
        "appA": (151, 158),
        "appB": (159, 162),
    }
    PAT = [
        (
            "chapter",
            re.compile("\\b[Cc]hapters?\\s+(\\d)(?:\\s*(?:,|and|&)\\s*(\\d))?"),
        ),
        ("section", re.compile("\\b[Ss]ections?\\s+(\\d+(?:\\.\\d+)+)")),
        ("appendix", re.compile("\\bAppendix\\s+([A-Z](?:\\.\\d+)?)(?![\\w])")),
        (
            "figure",
            re.compile("\\bFig(?:ure)?s?\\.?\\s*(\\d+\\.\\d+|[A-Z]\\.\\d+)[a-z]?"),
        ),
        (
            "table",
            re.compile(
                "\\bTables?\\s*(\\d+\\.\\d+|[A-Z]\\.\\d+|\\d+)(?!\\d)(?!\\.\\d)"
            ),
        ),
        ("equation", re.compile("\\b[Ee]q(?:uation|\\.)?\\s*(\\d+\\.\\d+)")),
    ]
    raw = []
    unresolved = []
    for idx in range(23, 163):
        lines = [
            (k, t)
            for k, t in body_lines(idx)
            if not is_header(t) and (not t.startswith("Appendix: chapter"))
        ]
        flat = ""
        offs = []
        for k, t in lines:
            offs.append((len(flat), k))
            flat += t + " "
        for kind, pat in PAT:
            for m in pat.finditer(flat):
                ln = max((o for o in offs if o[0] <= m.start()))[1]
                if CAP.match(dict(lines)[ln]) if ln in dict(lines) else False:
                    continue
                src = node_at(nodes, (idx, ln))
                ctx = flat[max(0, m.start() - 40) : m.end() + 30].strip()
                labels = [g for g in m.groups() if g]
                for lab in labels:
                    if kind == "chapter":
                        tid = f"ch{lab}"
                    elif kind == "section":
                        tid = f"s{lab}"
                    elif kind == "appendix":
                        tid = f"app{lab}" if len(lab) == 1 else f"s{lab}"
                    elif kind in ("figure", "table"):
                        key = (kind, lab)
                        amb = False
                        if kind == "table" and "." not in lab:
                            ch = [c for c, (a, b) in CH_RNG.items() if a <= idx <= b][0]
                            key = (kind, f"{ch[2:]}.{lab}")
                            amb = True
                        if key == ("table", "3.4"):
                            key = ("table", "3.5")
                            amb = True
                        tid = (
                            ("fig" if kind == "figure" else "tab") + key[1]
                            if key in figtab
                            else None
                        )
                        if amb:
                            lab = lab + " (read as " + key[1] + ")"
                    else:
                        tid = None
                    conf = "high"
                    if kind == "equation":
                        tid = "s1.3.1"
                    if tid is None or (
                        tid not in byid and (not tid.startswith(("fig", "tab")))
                    ):
                        unresolved.append((kind, lab, printed(idx), ctx))
                        continue
                    if kind == "table" and ("." not in lab or "read as" in lab):
                        conf = "low"
                    raw.append(
                        dict(
                            src=src["id"],
                            tgt=tid,
                            ref_kind=kind,
                            label=lab,
                            page=printed(idx),
                            ctx=ctx,
                            conf=conf,
                        )
                    )
    agg = collections.OrderedDict()
    dropped = 0
    for r in raw:
        if r["src"] == r["tgt"] or r["tgt"] in ancestors(r["src"]):
            dropped += 1
            continue
        k = (r["src"], r["tgt"], r["ref_kind"])
        a = agg.setdefault(
            k,
            dict(
                source=r["src"],
                target=r["tgt"],
                type="xref-" + r["ref_kind"],
                kind="explicit",
                basis="stated",
                occurrences=[],
                confidence="high",
            ),
        )
        a["occurrences"].append(dict(page=r["page"], label=r["label"], text=r["ctx"]))
        if r["conf"] == "low":
            a["confidence"] = "low"
    edges = []
    for i, (k, a) in enumerate(agg.items()):
        a["id"] = f"x{i + 1}"
        a["source_pages"] = sorted(
            {o["page"] for o in a["occurrences"]}, key=lambda p: pdfidx(p)
        )
        a["reason"] = "Explicit cross-reference: " + ", ".join(
            sorted({f"{a['type'][5:]} {o['label']}" for o in a["occurrences"]})
        )
        edges.append(a)
    return SimpleNamespace(**locals())


def _annotations(S, X, config):
    pages, norm, printed, pdfidx, body_lines, is_header, node_at = (
        getattr(S, key)
        for key in [
            "pages",
            "norm",
            "printed",
            "pdfidx",
            "body_lines",
            "is_header",
            "node_at",
        ]
    )
    N, F, A = (config["N"], config["F"], SimpleNamespace(**config))
    "Stage 1c: assemble thesis.json, validate it against the PDF text, and print/write a coverage report."
    import re, collections

    nodes, kids, caps = (X.nodes, X.kids, X.caps)
    byid = {n["id"]: n for n in nodes}

    def page_text(label):
        return re.sub("\\s+", " ", pages[pdfidx(label) - 1])

    def span_text(a, b):
        return " ".join(
            (page_text(printed(i)) for i in range(pdfidx(a), pdfidx(b) + 1))
        )

    def squashed(s):
        return re.sub("[^a-z0-9%.]", "", s.lower())

    LV2 = {
        "Preface": "background",
        "Contributions": "background",
        "Introduction": "background",
        "Methods": "method",
        "Results": "result",
        "Results and discussion": "result",
        "Conclusions": "discussion",
        "Related Work": "discussion",
    }
    order = sorted(nodes, key=lambda n: n["pos"])
    out = {}

    def mk(n):
        ann = N.get(n["id"], {})
        parent = n["parent"]
        ptype = out[parent]["type"] if parent in out else None
        typ = ann.get("type")
        if not typ:
            typ = (
                LV2.get(n["title"])
                if parent and parent.startswith("ch") and (n["kind"] == "section")
                else None
            )
            typ = typ or ptype or "background"
        q = ann.get("quote")
        rec = dict(
            id=n["id"],
            number=n["number"],
            title=n["title"],
            kind=n["kind"],
            parent=parent if parent else None,
            children=[],
            type=typ,
            pages=dict(
                start=n["start"],
                end=n["end"],
                pdf_start=pdfidx(n["start"]),
                pdf_end=pdfidx(n["end"]),
            ),
            source_pages=(
                [n["start"], n["end"]] if n["start"] != n["end"] else [n["start"]]
            ),
            approx_words=n["approx_words"],
            n_figures=n["n_figures"],
            n_tables=n["n_tables"],
            figures=n["figures"],
            tables=n["tables"],
            summary=ann.get("summary", ""),
            quote=dict(text=q[0], page=q[1]) if q else None,
            template=ann.get("template"),
            publication_status=ann.get("pub"),
            collaboration=ann.get("collab"),
            basis="stated",
            confidence="high" if ann.get("summary") else "low",
        )
        return rec

    def depth(n):
        d = 0
        p = n["parent"]
        while p and p in byid:
            d += 1
            p = byid[p]["parent"]
        return d

    for n in sorted(nodes, key=lambda n: (n["pos"], depth(n))):
        out[n["id"]] = mk(n)

    def add_special(i, spec, parent=None):
        a, b = (spec["start"], spec["end"])
        wc = sum(
            (
                len(" ".join(page_text(printed(k)).split()).split())
                for k in range(pdfidx(a), pdfidx(b) + 1)
            )
        )
        q = spec.get("quote")
        out[i] = dict(
            id=i,
            number=None,
            title=spec["title"],
            kind="front" if i.startswith("fm") else "back" if i == "refs" else "part",
            parent=parent,
            children=[],
            type=spec["type"],
            pages=dict(start=a, end=b, pdf_start=pdfidx(a), pdf_end=pdfidx(b)),
            source_pages=[a, b] if a != b else [a],
            approx_words=wc,
            n_figures=0,
            n_tables=0,
            figures=[],
            tables=[],
            summary=spec["summary"],
            quote=dict(text=q[0], page=q[1]) if q else None,
            template=None,
            publication_status=None,
            collaboration=None,
            basis="stated",
            confidence="high",
        )

    fm_total = 0
    for k in [
        "fm.title",
        "fm.dedication",
        "fm.ack",
        "fm.abstract",
        "fm.contents",
        "fm.figures",
        "fm.abbrev",
    ]:
        add_special(k, F[k], "fm")
    add_special("fm", F["fm"], None)
    out["fm"]["approx_words"] = sum(
        (out[k]["approx_words"] for k in out if k.startswith("fm."))
    )
    add_special("refs", F["refs"], None)
    ann = N["app"]
    out["app"] = dict(
        id="app",
        number=None,
        title="Appendices",
        kind="part",
        parent=None,
        children=[],
        type="appendix",
        pages=dict(start="127", end="140", pdf_start=149, pdf_end=162),
        source_pages=["127", "140"],
        approx_words=len(page_text("127").split())
        + out["appA"]["approx_words"]
        + out["appB"]["approx_words"],
        n_figures=out["appA"]["n_figures"] + out["appB"]["n_figures"],
        n_tables=out["appA"]["n_tables"] + out["appB"]["n_tables"] + 1,
        figures=[],
        tables=[],
        leaf_children=[],
        summary=ann["summary"],
        quote=None,
        template=None,
        publication_status=None,
        collaboration=None,
        basis="stated",
        confidence="high",
    )
    out["sB.2"]["tables"].append(
        dict(
            label="(uncaptioned)",
            page="138",
            basis="counted manually: full PoseBusters table has no caption",
        )
    )
    out["sB.2"]["n_tables"] += 1
    out["appB"]["n_tables"] += 1
    for k, v in out.items():
        p = v["parent"]
        if p:
            out[p]["children"].append(k)
    pos_of = {
        k: byid[k]["pos"] if k in byid else (pdfidx(out[k]["pages"]["start"]), 0)
        for k in out
    }
    for v in out.values():
        v["children"].sort(key=lambda c: pos_of[c])

    def lvl(i):
        p = out[i]["parent"]
        return 0 if not p else lvl(p) + 1

    for i in out:
        out[i]["level"] = lvl(i)
    roots = ["fm", "ch1", "ch2", "ch3", "ch4", "ch5", "ch6", "app", "refs"]

    def caption_words(c, n=22):
        ls = body_lines(c["pdf"])
        i = [j for j, (k, t) in enumerate(ls) if k == c["line"]][0]
        txt = " ".join((t for k, t in ls[i : i + 3]))
        txt = re.sub("^(Figure|Table) \\S+:\\s*", "", txt)
        return " ".join(txt.split()[:n])

    fig_ids = {}
    for c in caps:
        nid = ("fig" if c["kind"] == "figure" else "tab") + c["label"]
        fig_ids[c["kind"], c["label"]] = nid
        cw = caption_words(c)
        short = re.split("[.;:(]", cw)[0]
        sw = short.split()[:9]
        while sw and sw[-1].lower() in {
            "using",
            "of",
            "on",
            "with",
            "and",
            "the",
            "a",
            "to",
            "for",
            "in",
            "by",
            "from",
            "at",
            "as",
            "is",
            "are",
        }:
            sw.pop()
        short = " ".join(sw)
        home = out[c["home"]]
        lab = ("Figure " if c["kind"] == "figure" else "Table ") + c["label"]
        out[nid] = dict(
            id=nid,
            number=c["label"],
            title=f"{lab} · {short}",
            kind=c["kind"],
            parent=c["home"],
            children=[],
            type=home["type"],
            pages=dict(
                start=c["printed"],
                end=c["printed"],
                pdf_start=c["pdf"],
                pdf_end=c["pdf"],
            ),
            source_pages=[c["printed"]],
            approx_words=0,
            n_figures=0,
            n_tables=0,
            figures=[],
            tables=[],
            summary=f"{lab} is printed on p. {c['printed']}; placed under {home['title']} because that is where it is first cited ({c['home_basis']}).",
            quote=dict(text=cw, page=c["printed"]),
            template=None,
            publication_status=None,
            collaboration=None,
            basis="stated",
            confidence="high",
            leaf=True,
        )
    for v in list(out.values()):
        v["leaf_children"] = []
    for (k, l), nid in fig_ids.items():
        home = out[out[nid]["parent"]]
        home["leaf_children"].append(nid)
    out["tabB.2-full"] = dict(
        id="tabB.2-full",
        number="B.2 (uncaptioned)",
        title="Table · Full PoseBusters outputs (uncaptioned)",
        kind="table",
        parent="sB.2",
        children=[],
        type="appendix",
        pages=dict(start="138", end="138", pdf_start=160, pdf_end=160),
        source_pages=["138"],
        approx_words=0,
        n_figures=0,
        n_tables=0,
        figures=[],
        tables=[],
        summary="Full PoseBusters sub-test pass rates for every model and ablation; the thesis gives this table no caption or number.",
        quote=None,
        template=None,
        publication_status=None,
        collaboration=None,
        basis="stated",
        confidence="high",
        leaf=True,
        leaf_children=[],
    )
    out["sB.2"]["leaf_children"].append("tabB.2-full")
    for v in out.values():
        v["figures"] = [i for i in v["leaf_children"] if i.startswith("fig")]
        v["tables"] = [i for i in v["leaf_children"] if i.startswith("tab")]
    for v in out.values():
        v["leaf_children"].sort(
            key=lambda i: (out[i]["kind"], pdfidx(out[i]["pages"]["start"]), i)
        )
        v["figures"] = [i for i in v["leaf_children"] if i.startswith("fig")]
        v["tables"] = [i for i in v["leaf_children"] if i.startswith("tab")]
    for cl in A.CLAIMS:
        ev = []
        for kind, lab in re.findall(
            "(Fig|Table) ([A-Z]?\\d*\\.?\\d+)", cl["evidence"] or ""
        ):
            nid = ("fig" if kind == "Fig" else "tab") + lab
            if nid in out:
                ev.append(nid)
        cl["evidence_nodes"] = ev
    xr = dict(edges=X.edges)
    edges = []
    for e in xr["edges"]:
        e = dict(e)
        if e["source"] == "sA.3" and e["target"] == "s3.4.2":
            e["confidence"] = "low"
            e[
                "reason"
            ] += " (flagged: probably a typo for section 2.5.2.2, see anomaly a1)"
        edges.append(e)
    edges += A.SEMANTIC
    ent_chap = {}
    CH_KEYS = [
        ("fm", (9, 10)),
        ("ch1", (23, 54)),
        ("ch2", (55, 88)),
        ("ch3", (89, 108)),
        ("ch4", (109, 124)),
        ("ch5", (125, 144)),
        ("ch6", (145, 148)),
        ("appA", (151, 158)),
        ("appB", (159, 162)),
    ]

    def chap_of(idx):
        for k, (a, b) in CH_KEYS:
            if a <= idx <= b:
                return k

    ents = []
    for eid, name, cat, rx, desc in A.ENT:
        rg = re.compile(rx)
        chs = collections.OrderedDict()
        first = None
        total = 0
        for idx in list(range(9, 11)) + list(range(23, 163)):
            c = chap_of(idx)
            if c is None:
                continue
            lines = (
                [(k, t) for k, t in body_lines(idx) if not is_header(t)]
                if idx >= 23
                else [
                    (k, norm(l))
                    for k, l in enumerate(pages[idx - 1].split("\n"))
                    if norm(l)
                ]
            )
            flat = " ".join((t for k, t in lines))
            m = rg.findall(flat)
            if m:
                d = chs.setdefault(c, dict(count=0, pages=[]))
                d["count"] += len(m)
                total += len(m)
                pl = printed(idx)
                if pl not in d["pages"]:
                    d["pages"].append(pl)
                if first is None:
                    for k, t in lines:
                        if rg.search(t):
                            first = (idx, k)
                            break
        fn = None
        if first:
            fn = node_at(nodes, first)["id"] if first[0] >= 23 else "fm.abstract"
        for d in chs.values():
            d["pages"] = d["pages"][:12]
        ents.append(
            dict(
                id=eid,
                name=name,
                category=cat,
                description=desc,
                total_mentions=total,
                chapters=chs,
                first_node=fn,
                basis="stated",
                confidence="high" if total else "low",
            )
        )

    def pivot_list():
        ps = []
        for s in A.STAGES:
            if s["outcome"] == "pivot" or (
                s.get("next") and s["id"] in ("j3", "j7", "j9", "j11")
            ):
                ps.append(
                    dict(
                        from_stage=s["id"],
                        to_stage=s["next"],
                        why=s["why_next"],
                        pages=s["evidence"][-3:],
                        basis="stated",
                    )
                )
        return ps

    journey = dict(
        order_note=A.ORDER_NOTE,
        origin=A.ORIGIN,
        stages=A.STAGES,
        destination=A.DESTINATION,
        arc=A.ARC,
        contribution=A.CONTRIBUTIONS,
        transitions=pivot_list(),
    )
    doc = dict(
        journey=journey,
        structure=dict(
            roots=roots,
            nodes=out,
            chapter_templates={
                k: out[k]["template"]
                for k in ["ch1", "ch2", "ch3", "ch4", "ch5", "ch6"]
            },
            note="No chapter has a section called 'Limitations' or 'Discussion and limitations'; limitations sit inside the Preface and Conclusions sections. The thesis has a List of Figures but no List of Tables.",
        ),
        links=dict(
            edge_types=sorted({e["type"] for e in edges}),
            edges=edges,
            entities=ents,
            claims=A.CLAIMS,
        ),
        quality=dict(anomalies=A.ANOMALIES),
    )
    return doc


def parse(pages, config):
    import copy

    config = copy.deepcopy(config)
    S = _structure(pages, config)
    X = _references(S)
    document = _annotations(S, X, config)
    positions = {n["id"]: {"pdf": n["pos"][0], "line": n["pos"][1]} for n in X.nodes}
    return (
        document,
        {"failures": [], "unresolved": X.unresolved, "positions": positions},
    )
