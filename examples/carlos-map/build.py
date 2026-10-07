import json, re, collections
import extract as X
import content as K
from toc import TOC

node = X.node
order = X.order
children = collections.defaultdict(list)
for i in order:
    if node[i]['parent']:
        children[node[i]['parent']].append(i)

LEAF_PARENT = {}
def top_of(i):
    while i in LEAF_PARENT: i = LEAF_PARENT[i]
    while node[i]['parent']:
        i = node[i]['parent']
    return i

def descendants(i):
    out = []
    for c in children[i]:
        out.append(c); out += descendants(c)
    return out

# ---- figure / table counts
fig_own = collections.defaultdict(list); tab_own = collections.defaultdict(list)
for lab, nid in K.FIG_NODE.items(): fig_own[nid].append(f"Fig. {lab}")
for lab, nid in K.TAB_NODE.items(): tab_own[nid].append(f"Table {lab}")
for nid, n in K.PAPER_FIGS.items(): fig_own[nid] += [f"[journal Fig. {k}]" for k in range(1, n + 1)]
for nid, n in K.PAPER_TABS.items(): tab_own[nid] += [f"[journal Table {k}]" for k in range(1, n + 1)]

# ---- stage -> node coverage
NO_EXPAND = {"ch3", "ch4", "ch5", "ch1"}
stage_nodes = {}
for s in K.STAGES:
    cov = set()
    for n in s['chapters'] + [e['node'] for e in s['evidence']]:
        cov.add(n)
        if n not in NO_EXPAND:
            cov.update(descendants(n))
    stage_nodes[s['id']] = sorted(cov, key=order.index)

node_stages = collections.defaultdict(list)
for sid, ns in stage_nodes.items():
    for n in ns: node_stages[n].append(sid)

claims_by_node = collections.defaultdict(list)
for c in K.CLAIMS: claims_by_node[c['node']].append(c['id'])

nodes_out = []
for i in order:
    n = node[i]
    kids = children[i]
    sub = [i] + descendants(i)
    figs = []; tabs = []
    for j in sub: figs += fig_own.get(j, []); tabs += tab_own.get(j, [])
    t = K.TYPE.get(i)
    if t is None:
        p = n['parent']
        t = K.TYPE.get(p) or K.TYPE.get(top_of(i)) or 'background'
        if i.startswith('front'): t = 'front'
        if i.startswith('C.') or i.startswith('A.'): t = 'appendix'
    q = K.QUOTE.get(i)
    nodes_out.append(dict(
        id=i, number=n['number'], title=n['title'], parent=n['parent'], children=kids, level=n['level'],
        type=t, type_note=K.TYPE_NOTE.get(i),
        template=K.TEMPLATE.get(i),
        pages=[n['page_start'], n['page_end']], source_pages=[n['page_start'], n['page_end']],
        journal_pages=("5497-5529" if i in ("A.1",) else None),
        approx_words=n['approx_words'], approx_words_own=n['words_own'],
        n_figures=len(figs), n_tables=len(tabs), figures=figs, tables=tabs,
        n_figures_own=len(fig_own.get(i, [])), n_tables_own=len(tab_own.get(i, [])),
        publication=K.PUBLICATION.get(i),
        summary=K.SUMMARY[i], summary_basis='paraphrase of stated content', quote=(dict(text=q[0], page=q[1]) if q else None),
        stages=node_stages.get(i, []), claims=claims_by_node.get(i, []),
        basis="stated", confidence="high", chapter=top_of(i),
    ))

# ---- figure / table leaf nodes
def add_leaf(fid, kind, label, title, parent, page, journal=None, jlabel=None):
    LEAF_PARENT[fid] = parent
    nodes_out.append(dict(id=fid, number=label, title=title, parent=parent, children=[], level=3, type=kind, type_note=None, template=None,
        pages=[page, page], source_pages=[page, page], journal_pages=(str(journal) if journal else None),
        approx_words=0, approx_words_own=0, n_figures=0, n_tables=0, figures=[], tables=[], n_figures_own=0, n_tables_own=0,
        publication=None, summary=title, summary_basis='caption title (shortened)', quote=None,
        stages=node_stages.get(parent, []), claims=[], basis='stated', confidence='high', chapter=top_of(parent)))
    for n in nodes_out:
        if n['id'] == parent: n['children'] = n['children'] + [fid]
for lab, ttl in K.FIG_TITLE.items():
    add_leaf('fig.'+lab, 'figure', 'Fig. '+lab, ttl, K.FIG_NODE[lab], K.FIG_PAGE[lab])
for lab, ttl in K.TAB_TITLE.items():
    add_leaf('tab.'+lab, 'table', 'Table '+lab, ttl, K.TAB_NODE[lab], K.TAB_PAGE[lab])
for lab, (ttl, pg, jp) in K.PAPER_FIG.items():
    add_leaf('fig.'+lab, 'figure', 'Journal Fig. '+lab[1:], ttl, 'A.1', pg, jp)
for lab, (ttl, pg, jp) in K.PAPER_TAB.items():
    add_leaf('tab.'+lab, 'table', 'Journal Table '+lab[1:], ttl, 'A.1', pg, jp)
node_ids = {n['id'] for n in nodes_out}

# figure / table references (captions excluded). Same-node references are kept now that the target is its own node.
figpat = re.compile(r'\b[Ff]ig(?:ure|ures|\.)\s+(\d\.\d{1,2}(?:\s*(?:,|and)\s*\d\.\d{1,2})*)')
tabpat = re.compile(r'\b[Tt]able\s+(\d\.\d{1,2})')
figrefs = collections.OrderedDict()
def add_fref(src, tgt, ref, page, typ):
    e = figrefs.setdefault((src, tgt), dict(source=src, target=tgt, type=typ, refs=[], source_pages=[]))
    if ref not in e['refs']: e['refs'].append(ref)
    if page not in e['source_pages']: e['source_pages'].append(page)
for p in X.BODY_PAGES:
    t = X.ptxt(p)
    for pat, typ, pre in ((figpat, 'figure_ref', 'fig.'), (tabpat, 'table_ref', 'tab.')):
        for m in pat.finditer(t):
            if t[m.end():m.end()+1] == ':': continue
            src = X.node_at(X.page_off[p] + m.start())
            for lab in re.findall(r'\d\.\d{1,2}', m.group(1)):
                if pre+lab in node_ids and src:
                    add_fref(src, pre+lab, ('Figure ' if typ == 'figure_ref' else 'Table ')+lab, p, typ)
# references inside the embedded paper ("Fig. 4", "Table 1"); mid-line only, so captions are skipped
for p in range(188, 201):
    t = X.ptxt(p)
    for m in re.finditer(r'(?<![\n])(?<!^)\b(Fig\.|Table)\s?(\d)\b', t):
        ls = t.rfind('\n', 0, m.start()) + 1
        if m.start() - ls < 3: continue
        pre = 'fig.J' if m.group(1) == 'Fig.' else 'tab.J'
        tid = pre + m.group(2)
        if tid in node_ids:
            add_fref('A.1', tid, f"{m.group(1)} {m.group(2)}", p, 'figure_ref' if m.group(1) == 'Fig.' else 'table_ref')

# ---- edges
edges = []
k = 0
for e in X.edges.values():
    if e['type'] in ('figure_ref', 'table_ref'): continue
    k += 1
    edges.append(dict(id=f"x{k:03d}", source=e['source'], target=e['target'], kind='explicit', basis='stated',
                      type=e['type'], reason=None, refs=e['refs'], source_pages=sorted(e['source_pages']),
                      confidence=e['confidence'],
                      source_chapter=top_of(e['source']), target_chapter=top_of(e['target'])))
for e in figrefs.values():
    k += 1
    edges.append(dict(id=f"x{k:03d}", source=e['source'], target=e['target'], kind='explicit', basis='stated', type=e['type'], reason=None,
                      refs=e['refs'], source_pages=sorted(e['source_pages']), confidence='high',
                      source_chapter=top_of(e['source']), target_chapter=top_of(e['target'])))
for e in K.EXTRA_EXPLICIT:
    k += 1
    edges.append(dict(id=f"x{k:03d}", source=e['source'], target=e['target'], kind='explicit', basis='stated',
                      type=e['type'], reason=None, refs=e['refs'], source_pages=e['source_pages'], confidence='high',
                      source_chapter=top_of(e['source']), target_chapter=top_of(e['target'])))
k = 0
for e in K.INFERRED_EDGES:
    k += 1
    d = dict(e); d['id'] = f"i{k:03d}"; d['refs'] = None
    d['source_chapter'] = top_of(e['source']); d['target_chapter'] = top_of(e['target'])
    edges.append(d)

# ---- claim -> figure/table ids
def fig_ids(s):
    if not s: return []
    out = []
    for m in re.finditer(r'(Fig\.|Table)\s+(\d)\.(\d+)(?:-(?:(\d)\.)?(\d+))?', s):
        pre = 'fig.' if m.group(1) == 'Fig.' else 'tab.'
        a, c, e = int(m.group(3)), m.group(2), m.group(5)
        for q in range(a, int(e) + 1 if e else a + 1): out.append(f'{pre}{c}.{q}')
    return [x for x in out if x in node_ids]
for c in K.CLAIMS: c['figure_ids'] = fig_ids(c['figure'])
for n in nodes_out:
    for c in K.CLAIMS:
        if n['id'] in c['figure_ids']: n['claims'] = n['claims'] + [c['id']]

# ---- entities
BODY = [11] + list(range(19, 186)) + list(range(211, 232))
BROAD = {"e.multipole", "e.polar", "e.hf", "e.dft", "k.bondorder", "d.glycine", "e.kabsch", "d.methanol"}
entities = []
for eid, typ, name, rx, desc in K.ENTITIES:
    pat = re.compile(rx)
    pages = collections.Counter(); secs = collections.Counter()
    for p in BODY:
        t = X.ptxt(p)
        for m in pat.finditer(t):
            pages[p] += 1
            nid = X.node_at(X.page_off[p] + m.start())
            if nid: secs[nid] += 1
    plist = sorted(pages)
    chaps = sorted({top_of(s) for s in secs}, key=order.index)
    # drop chapter-less bleed: bibliography/front only
    entities.append(dict(id=eid, type=typ, name=name, description=desc,
                         chapters=chaps, sections=sorted(secs, key=order.index),
                         n_mentions=sum(pages.values()), source_pages=plist[:24], n_pages=len(plist),
                         basis="stated", confidence=("medium" if eid in BROAD else "high")))

thesis = dict(
    meta=dict(**K.THESIS, generated_from="carlos-thesis.pdf (266 PDF pages)", page_map=K.PAGE_MAP,
              convention="All page numbers are printed page numbers (PDF index - 1)."),
    journey=dict(arc=K.ARC, contribution=K.CONTRIBUTIONS, stages=K.STAGES,
                 outcome_values=["worked", "partial", "failed", "pivot"]),
    structure=dict(nodes=nodes_out, roots=[i for i in order if not node[i]['parent']]),
    links=dict(edges=edges, entities=entities, claims=K.CLAIMS,
               edge_types=sorted({e['type'] for e in edges})),
    notes=K.NOTES,
)
json.dump(thesis, open('thesis.json', 'w'), ensure_ascii=False, indent=1)
print('wrote thesis.json', len(nodes_out), 'nodes', len(edges), 'edges', len(entities), 'entities', len(K.CLAIMS), 'claims')
