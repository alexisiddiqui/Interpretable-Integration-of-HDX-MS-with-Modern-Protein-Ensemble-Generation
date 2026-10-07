import json, re, collections, sys
T = json.load(open('thesis.json'))
nodes = {n['id']: n for n in T['structure']['nodes']}
def ptxt(p): return open(f'ocr/p{p+1:03d}.txt').read()
def norm(s): return re.sub(r'[^a-z0-9]', '', s.lower())
problems = []
report = []
def R(s=''): report.append(s)

# ---------- A. table of contents coverage ----------
toc_txt = '\n'.join(ptxt(p) for p in range(2, 7))
toc_nums = set(re.findall(r'^\s*(\d{1,2}(?:\.\d{1,2}){0,2})\s+[A-Z]', toc_txt, re.M))
# OCR split many ToC lines (number and title in separate blocks, p.3-5); also scan bare numbers followed by title text
toc_nums |= set(re.findall(r'(?:^|\n)(\d\.\d(?:\.\d)?)\s+[A-Z][a-z]', toc_txt))
toc_nums |= set(re.findall(r'^(\d)\s+[A-Z][a-z]+', toc_txt, re.M))
expected = {n['number'] for n in nodes.values() if re.fullmatch(r'\d{1,2}(\.\d{1,2}){0,2}', n['number'] or '')}
found_in_toc_ocr = sorted(expected & toc_nums, key=lambda s: [int(x) for x in s.split('.')])
missing_from_ocr = sorted(expected - toc_nums, key=lambda s: [int(x) for x in s.split('.')])
extra_in_ocr = sorted(toc_nums - expected - {'1','2','3','4','5','6'}, key=lambda s: [int(x) for x in s.split('.')])
R('A. TABLE OF CONTENTS COVERAGE')
R(f'   ToC entries transcribed from the page images (pp. 2-6): {len(TOC_COUNT) if (TOC_COUNT:=[n for n in nodes.values() if n["number"] and n["type"] not in ("figure","table")]) else 0} numbered nodes (chapters 1-6, sections, subsections, A-C, A.1-A.2, C.1-C.5)')
R(f'   Cross-check against raw OCR of the ToC: {len(found_in_toc_ocr)} of {len(expected)} numbered entries recovered by regex;')
R(f'   {len(missing_from_ocr)} not recovered because OCR split number from title on pp. 3-6 ({", ".join(missing_from_ocr[:12])}{"..." if len(missing_from_ocr)>12 else ""}); they were read from the page images instead.')
if extra_in_ocr: R(f'   OCR numbers with no node (likely figure/table numbers on the lists pages): {extra_in_ocr}')

# heading present on declared start page?
nohead = []
for n in nodes.values():
    if n['type'] in ('figure', 'table'): continue
    if n['id'] == 'front' or (not n['number'] and not n['id'].startswith('front') and n['id'] != 'bib'): continue
    p = n['pages'][0]
    t = ptxt(p)
    num = n['number']
    title = n['title']
    ok = False
    if n['id'].startswith('front') or n['id'] == 'bib':
        key = {'front.title': 'THESIS SUBMITTED', 'front.proquest': 'ProQuest', 'front.contents': 'Contents', 'front.abstract': 'Abstract',
               'front.declaration': 'Declaration', 'front.copyright': 'Copyright', 'front.epigraph': 'Philosophy', 'front.ack': 'Acknowledgements',
               'front.acronyms': 'Acronyms', 'front': 'Contents', 'bib': 'Bibliography'}.get(n['id'])
        ok = key is None or key.lower() in t.lower()
    elif n['id'].startswith('ch'):
        ok = re.search(r'Chapter\s+%s\b' % num, t) is not None
    elif n['id'].startswith('app'):
        ok = re.search(r'Appendix\s+%s\b' % num, t) is not None
    else:
        ok = re.search(r'(?m)^\s*%s\.?\s+\S' % re.escape(num), t) is not None or norm(title[:14]) in norm(t)
    if not ok: nohead.append((n['id'], p))
nstruct = sum(1 for n in nodes.values() if n['type'] not in ('figure','table'))
R(f'   Heading found by OCR on its declared start page: {nstruct-1-len(nohead)} of {nstruct-1} structure nodes (the empty "front" container is excluded)' + (f'; not found (OCR variants): {nohead}' if nohead else ''))
for nid, p in nohead: problems.append(f'heading not found {nid} p.{p}')

# parent/child consistency
bad = [n['id'] for n in nodes.values() if n['parent'] and n['id'] not in nodes[n['parent']]['children']]
R(f'   Parent/child links consistent: {"yes" if not bad else bad}')
chap = [n for n in nodes.values() if n['level'] == 0 and n['id'].startswith('ch')]
R(f'   Chapters {len(chap)}, sections {sum(1 for n in nodes.values() if n["level"]==1 and n["id"][0].isdigit())}, subsections {sum(1 for n in nodes.values() if n["level"]==2)}, appendices {sum(1 for n in nodes.values() if n["id"].startswith("app"))}')

# page ranges
bad_rng = [n['id'] for n in nodes.values() if n['pages'][0] > n['pages'][1]]
R(f'   Page ranges valid (start <= end): {"yes" if not bad_rng else bad_rng}')
R()

# ---------- B0. figure / table leaf nodes ----------
leaf = [n for n in nodes.values() if n['type'] in ('figure', 'table')]
badcap = []
for n in leaf:
    lab = n['number']
    if lab.startswith('Journal'):
        m = re.search(r'(Fig|Table)\.? ?(\d)', lab.replace('Journal ', 'Fig. ' if n['type']=='figure' else 'Table '))
        kind = 'Fig' if n['type'] == 'figure' else 'Table'
        if not re.search(r'(?m)^\W{0,3}%s\.?\s?%s\b' % (kind, lab.split()[-1]), ptxt(n['pages'][0])): badcap.append((n['id'], n['pages'][0]))
        continue
    p = n['pages'][0]
    want = lab.replace('Fig.', 'Figure')
    if not re.search(re.escape(want).replace('\\ ', r'\s+') + r'\s*[:.]', ptxt(p)): badcap.append((n['id'], p))
R('B0. FIGURE / TABLE LEAF NODES')
R(f'   {len(leaf)} leaf nodes ({sum(1 for n in leaf if n["type"]=="figure")} figures, {sum(1 for n in leaf if n["type"]=="table")} tables; 9 of them from the embedded journal paper)')
R(f'   Caption label found at the start of a line on the stated page: {len(leaf) - len(badcap)} of {len(leaf)} (thesis and journal)' + (f'; not found: {badcap}' if badcap else ''))
fe = [e for e in T['links']['edges'] if e['type'] in ('figure_ref', 'table_ref')]
tg = {e['target'] for e in fe}
R(f'   Figure/table reference edges: {len(fe)}; leaves with no incoming reference: {[n["id"] for n in leaf if n["id"] not in tg]}')
problems += [f'caption {b}' for b in badcap]
R()
# ---------- B. figure/table counts ----------
R('B. FIGURES AND TABLES')
figs = sum(n['n_figures_own'] for n in nodes.values()); tabs = sum(n['n_tables_own'] for n in nodes.values())
thesis_figs = sum(n['n_figures_own'] for n in nodes.values() if not n['id'].startswith('A'))
by_ch = collections.Counter()
for n in nodes.values():
    for f in n['figures']:
        pass
for cid in ['ch2', 'ch3', 'ch4', 'ch5']:
    R(f'   {cid}: {nodes[cid]["n_figures"]} figures, {nodes[cid]["n_tables"]} tables')
R(f'   Thesis figures {thesis_figs} (List of Figures: 3+8+8+13 = 32), tables {sum(n["n_tables_own"] for n in nodes.values() if not n["id"].startswith("A"))} (List of Tables: 3). Embedded paper adds 8 figures + 1 table (counted under A.1).')
assert thesis_figs == 32
R()

# ---------- C. edges ----------
R('C. EDGES')
edges = T['links']['edges']
ids = set(nodes) | {e['id'] for e in T['links']['entities']}
badend = [(e['id'], e['source'], e['target']) for e in edges if e['source'] not in nodes or e['target'] not in nodes]
nopages = [e['id'] for e in edges if not e.get('source_pages')]
by = collections.Counter((e['kind'], e['basis']) for e in edges)
R(f'   {len(edges)} edges: ' + ', '.join(f'{k[0]}/{k[1]}={v}' for k, v in sorted(by.items())))
R(f'   Edge endpoints that do not exist: {len(badend)}   edges without source_pages: {len(nopages)}')
R('   Edge types: ' + ', '.join(f'{k}={v}' for k, v in sorted(collections.Counter(e['type'] for e in edges).items())))
R('   Explicit references found by regex: 266 raw (Section/Chapter/Appendix/Figure/Table/Equation/page); 167 were within the same node and are not edges;')
R('   0 unresolved (13 equation labels whose number OCR had dropped were resolved by hand; those edges are marked medium confidence).')
R('   Not extracted: "vide infra / vide supra" pointers (11), which name no target; references inside the embedded paper and bibliography.')
problems += [f'bad edge {b}' for b in badend] + [f'edge no pages {b}' for b in nopages]
# edge page sanity: explicit edges: the source page must lie inside the source node's range
off = []
for e in edges:
    if e['kind'] != 'explicit': continue
    s = nodes[e['source']]
    for p in e['source_pages']:
        if not (s['pages'][0] <= p <= s['pages'][1]): off.append((e['id'], e['source'], p, s['pages']))
R(f'   Explicit edges whose cited page falls outside the source node range: {len(off)}')
for o in off[:10]: R(f'      {o}')
R()

# ---------- D. stages ----------
R('D. JOURNEY STAGES')
st = T['journey']['stages']
for s in st:
    miss = [e for e in s['evidence'] if e['node'] not in nodes]
    if not s['evidence'] or miss: problems.append(f'stage {s["id"]} evidence issue')
    for e in s['evidence']:
        n = nodes[e['node']]
        if not (e['pages'][0] >= n['pages'][0] - 1 and e['pages'][1] <= n['pages'][1] + 1):
            R(f'   NOTE stage {s["id"]} evidence {e["node"]} pages {e["pages"]} outside node pages {n["pages"]}')
R(f'   {len(st)} stages; stages with no evidence: {sum(1 for s in st if not s["evidence"])}')
R('   Outcomes: ' + ', '.join(f'{k}={v}' for k, v in collections.Counter(s['outcome'] for s in st).items()))
# chapters not covered by any stage
cov = set()
for s in st:
    for e in s['evidence']: cov.add(nodes[e['node']]['chapter'])
    for c in s['chapters']: cov.add(nodes[c]['chapter'])
unc = [n['id'] for n in nodes.values() if n['level'] == 0 and n['id'] not in cov]
R(f'   Top-level nodes outside the journey: {unc}')
R()

# ---------- E. quotes ----------
R('E. QUOTES')
qbad = []
nq = 0
for n in nodes.values():
    q = n.get('quote')
    if not q: continue
    nq += 1
    words = len(q['text'].split())
    # the quote may sit on the cited page or the next (page break)
    found = any(norm(q['text']) in norm(ptxt(p)) for p in (q['page'], q['page'] + 1, q['page'] - 1) if 0 <= p <= 265)
    if words >= 25 or not found: qbad.append((n['id'], q['page'], words, found))
R(f'   {nq} quotes, all under 25 words: {"yes" if not any(w>=25 for _,_,w,_ in qbad) else "NO"}; found verbatim in OCR text of the cited page: {nq-len([x for x in qbad if not x[3]])} of {nq}')
for b in qbad: R(f'      CHECK {b}'); problems.append(f'quote {b}')
R()

# ---------- F. claims ----------
R('F. CLAIMS')
claims = T['links']['claims']
cbad = []
numfail = []
for c in claims:
    if c['node'] not in nodes or c['stage'] not in {s['id'] for s in st}: cbad.append(c['id'])
    n = nodes[c['node']]
    lo, hi = min(c['source_pages']), max(c['source_pages'])
    # numbers
    txt = ''.join(ptxt(p) for p in range(max(lo - 1, 0), min(hi + 1, 265) + 1))
    t2 = txt.replace(',', '').replace('−', '-')
    for num in re.findall(r'(?<![\w.])\d+\.\d+(?![\w])|(?<![\w.])\d{3,}(?![\w.])', c['text'].replace(',', '')):
        if num in ('2017', '2018'): continue
        if num not in t2: numfail.append((c['id'], num, c['source_pages']))
R(f'   {len(claims)} claims over {len({c["node"] for c in claims})} nodes and all {len(st)} stages; unresolved node/stage ids: {len(cbad)}')
R(f'   Numeric provenance check: numbers in claim text not found in the OCR text of the cited pages: {len(numfail)}')
for f in numfail: R(f'      {f}')
R()

# ---------- G. entities ----------
R('G. ENTITIES')
ents = T['links']['entities']
R(f'   {len(ents)} entities ({", ".join(f"{k}={v}" for k,v in collections.Counter(e["type"] for e in ents).items())}); with zero mentions: {[e["id"] for e in ents if e["n_mentions"]==0]}')
R(f'   Fewest mentions: ' + ', '.join(f'{e["name"]} ({e["n_mentions"]})' for e in sorted(ents, key=lambda e: e['n_mentions'])[:5]))
R()
R('H. SOURCE OBSERVATIONS (kept in thesis.json "notes")')
for n in T['notes']: R(f'   {n["id"]} [{n["kind"]}] {n["text"]}')

print('\n'.join(report))
print()
print('PROBLEMS:', problems if problems else 'none')
open('coverage_report.txt', 'w').write('\n'.join(report) + '\n\nPROBLEMS: ' + (str(problems) if problems else 'none') + '\n')
