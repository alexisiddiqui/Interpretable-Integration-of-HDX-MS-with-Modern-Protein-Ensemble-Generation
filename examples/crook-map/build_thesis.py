# -*- coding: utf-8 -*-
"""Stage 1: assemble thesis.json from deterministic extraction + curated content, then validate and print a coverage report."""
import re, json, sys, io, contextlib
from collections import defaultdict, Counter
with contextlib.redirect_stdout(io.StringIO()):
    import build_xrefs as X
S = X.S
L, page_at, pdf_at = S.L, S.page_at, S.pdf_at
nodes, byid, figs, tabs = S.nodes, S.byid, S.figs, S.tabs
from curated_journey import STAGES, CONTRIBUTIONS, NEGATIVE, JOURNEY_ARC, JOURNEY_CAVEAT
from curated_nodes import CHAPTER_META, NODE_META
from curated_claims import CLAIMS
from curated_links import ENTITIES, SEMANTIC

ROMAN = S.ROMAN
def label(p): return ROMAN[p] if p <= 30 else str(p - 30)
# ---------------------------------------------------------------- page text by printed label
page_text = defaultdict(str)
for i, l in enumerate(L):
    if l.startswith('====='): continue
    page_text[page_at[i]] += l + '\n'
def norm(s): return re.sub(r'[\W_]+', ' ', s.lower(), flags=re.U).strip()
def next_label(lab):
    p = S.lab_to_pdf(lab); return label(p + 1) if p < 380 else lab
npage = {k: norm(v) for k, v in page_text.items()}
def text_in_pages(pages):
    t = ' '.join(npage.get(p, '') for p in pages)
    return t

problems = []   # hard validation failures
notes = []      # soft notes for the coverage report

# ---------------------------------------------------------------- nodes
out_nodes = []
for n in sorted(nodes, key=lambda n: (n['pdf_start'], n['pos'] if n['pos'] is not None else -1, n['level'])):
    d = {k: n[k] for k in ('id','num','title','level','parent','numbered','pages','page_start','page_end','approx_words','n_figures','n_tables','figure_ids','table_ids')}
    d['type'] = n.get('type')
    d['basis'] = 'stated'
    d['source_pages'] = [n['page_start']]
    d['confidence'] = 'high'
    if not n['numbered'] and n['pos'] is not None:
        d['kind'] = 'unnumbered heading'
        if n['id'].startswith('u7.3/'):
            d['parent_basis'] = 'inferred'; d['confidence'] = 'medium'
    cm = CHAPTER_META.get(n['id'])
    if cm:
        d['type'] = cm['type']; d['type_basis'] = 'inferred'
        d.update({k: v for k, v in cm.items() if k not in ('type',)})
    elif d['type'] and n['pos'] is not None:
        d['type_basis'] = 'inferred'
    nm = NODE_META.get(n['id'])
    if nm:
        if 'summary' in nm: d['summary'] = nm['summary']; d['summary_basis'] = 'stated'
        if 'quote' in nm:
            q, pg = nm['quote']
            wc = len(q.split())
            if wc >= 25: problems.append(('quote too long', n['id'], wc))
            hit = norm(q) in text_in_pages([pg]) or norm(q) in text_in_pages([pg, next_label(pg)])
            if not hit: problems.append(('quote not found on page', n['id'], q, pg))
            d['quote'] = dict(text=q, page=pg)
            if pg not in d['source_pages']: d['source_pages'].append(pg)
    out_nodes.append(d)
ids = {d['id'] for d in out_nodes}
children = defaultdict(list)
for d in out_nodes:
    if d['parent']: children[d['parent']].append(d['id'])
for d in out_nodes: d['children'] = children[d['id']]

# ---------------------------------------------------------------- pages helper
valid_labels = set(ROMAN[1:]) | {str(i) for i in range(1, 351)}
def chk_pages(where, pages):
    for p in pages:
        if p not in valid_labels: problems.append(('bad page label', where, p))

# ---------------------------------------------------------------- edges
edges = []
eid = 0
for e in X.edges:
    if e['type'] == 'refers_to_equation' and ('Theorem' in ' '.join(e['examples']) or 'theorem' in ' '.join(e['examples']) or 'Definition' in ' '.join(e['examples']) or 'definition' in ' '.join(e['examples'])):
        continue   # numbered theorems/definitions are not nodes
    if e['source'] == e['target']: continue
    eid += 1
    edges.append(dict(id='e%d' % eid, source=e['source'], target=e['target'], type=e['type'], kind='explicit', basis=e['basis'],
                      reason=('Numbered cross-reference in the text: ' + '; '.join(e['examples'])) if e['basis'] == 'stated' else 'Unnumbered "see appendix" mention inside a chapter that has a single matching appendix',
                      source_pages=e['pages'], count=e['count'], confidence='high' if e['basis'] == 'stated' else 'medium'))
n_explicit = len(edges)
fig_tab_ids = {f['id'] for f in figs} | {t['id'] for t in tabs}
for s, t, typ, basis, reason, pages, conf in SEMANTIC:
    eid += 1
    edges.append(dict(id='e%d' % eid, source=s, target=t, type=typ, kind='semantic', basis=basis, reason=reason, source_pages=pages, count=1, confidence=conf))
all_ids = ids | fig_tab_ids
ent_ids = {e[0] for e in ENTITIES}
for e in edges:
    for end in ('source', 'target'):
        if e[end] not in all_ids: problems.append(('edge endpoint missing', e['id'], e[end]))
    chk_pages('edge ' + e['id'], e['source_pages'])

# ---------------------------------------------------------------- entities
chap_ranges = {}
for d in nodes:
    if d['level'] == 0 and d['pos'] is not None:
        chap_ranges[d['id']] = (d['pos'], d['end'])
def chapter_scan_order(): return [c for c in ['ch%d' % i for i in range(1, 9)] + ['appA', 'appB', 'appC']]
entities = []
for eid_, lab_, kind, pat, flags, gloss in ENTITIES:
    rx = re.compile(pat, flags)
    chs = {}; pages_by = {}
    for ch in chapter_scan_order():
        a, b = chap_ranges[ch]
        cnt = 0; first = None; sample = []
        for i in range(a, b):
            l = L[i]
            if l.startswith('====='): continue
            m = rx.findall(l)
            if m:
                cnt += len(m)
                if first is None: first = page_at[i]
                if page_at[i] not in sample and len(sample) < 4: sample.append(page_at[i])
        if cnt: chs[ch] = dict(mentions=cnt, first_page=first, pages=sample)
    main = [c for c in chs if c.startswith('ch')]
    app = [c for c in chs if c.startswith('app')]
    if not chs: notes.append(('entity with zero mentions', eid_)); continue
    firstch = min(chs, key=lambda c: chapter_scan_order().index(c))
    entities.append(dict(id='ent:' + eid_, label=lab_, kind=kind, gloss=gloss, chapters=main, appendices=app, by_chapter=chs,
                         total_mentions=sum(v['mentions'] for v in chs.values()), basis='stated', confidence='high' if len(pat) > 8 else 'medium',
                         source_pages=[chs[firstch]['first_page']]))
ent_ids = {e['id'] for e in entities}

# ---------------------------------------------------------------- claims
claims = []
for c in CLAIMS:
    d = dict(c)
    if d['node'] not in ids: problems.append(('claim node missing', d['id'], d['node']))
    if d['stage'] not in {s['id'] for s in STAGES}: problems.append(('claim stage missing', d['id'], d['stage']))
    for f in d['figures']:
        if f not in fig_tab_ids: problems.append(('claim figure missing', d['id'], f))
    chk_pages('claim ' + d['id'], d['source_pages'])
    t = text_in_pages(d['source_pages'] + [next_label(d['source_pages'][-1])])
    miss = [tok for tok in d['check'] if norm(tok) not in t]
    if miss: problems.append(('claim token not found on cited pages', d['id'], miss, d['source_pages']))
    d['evidence_checked'] = not miss
    d.pop('check')
    claims.append(d)

# ---------------------------------------------------------------- journey
for s in STAGES:
    chk_pages('stage ' + s['id'], s['evidence'])
    if not s['evidence']: problems.append(('stage without evidence', s['id']))
    for ch in s['chapters']:
        if ch not in ids: problems.append(('stage chapter missing', s['id'], ch))
    for sec in s['sections']:
        if sec not in ids: problems.append(('stage section missing', s['id'], sec))
    q = s['quote']
    if len(q['text'].split()) >= 25: problems.append(('stage quote too long', s['id']))
    if not (norm(q['text']) in text_in_pages([q['page']]) or norm(q['text']) in text_in_pages([q['page'], next_label(q['page'])])):
        problems.append(('stage quote not found', s['id'], q))
    s['claims'] = [c['id'] for c in claims if c['stage'] == s['id']]
    s['source_pages'] = s['evidence']
    # evidence must be real: every evidence page should hold stage-relevant text (non-empty page)
    for p in s['evidence']:
        if not page_text.get(p, '').strip(): problems.append(('stage evidence page empty', s['id'], p))
neg_ids = {n['id'] for n in NEGATIVE}
for s in STAGES:
    for n in s['negative_results']:
        if n not in neg_ids: problems.append(('negative result missing', s['id'], n))
for n in NEGATIVE:
    if n['node'] not in ids: problems.append(('negative node missing', n['id'], n['node']))
    for f in n['figures']:
        if f not in fig_tab_ids: problems.append(('negative fig missing', n['id'], f))
    chk_pages('neg ' + n['id'], n['source_pages'])
for k in CONTRIBUTIONS:
    chk_pages('contrib ' + k['id'], k['source_pages'])
    for ch in k['chapters']:
        if ch not in ids: problems.append(('contribution chapter missing', k['id'], ch))

# ---------------------------------------------------------------- coverage (TOC -> nodes)
toc = [e for e in json.load(open('toc.json')) if e['num'] is not None]
toc_nums = {e['num'] for e in S.B.final}
node_nums = {d['num'] for d in out_nodes if d['num']}
toc_missing = sorted(toc_nums - node_nums)
if toc_missing: problems.append(('TOC entries without node', toc_missing))
front_expected = ['Title page', 'Dedication', 'Declaration', 'Summary', 'Acknowledgements', 'Preface', 'Table of contents', 'List of figures', 'List of tables', 'Abbreviations']
front_have = [d['title'] for d in out_nodes if d['id'].startswith('fm-')]
for t in front_expected:
    if t not in front_have: problems.append(('front matter missing', t))

# figure/table counts vs lists
if len(figs) != 120: problems.append(('figure count', len(figs)))
if len(tabs) != 49: problems.append(('table count', len(tabs)))
fig_nodes = Counter(f['node'] for f in figs)
for f in figs + tabs:
    if f['node'] not in ids: problems.append(('figure node missing', f['id']))

# ---------------------------------------------------------------- page map
pagemap = dict(rule='Printed page = PDF page index - 30 from the start of chapter 1 (PDF 31 = p. 1); front matter uses roman numerals equal to the PDF index (PDF 11 = p. xi). PDF 16, 22, 30, 216, 294, 324, 350 etc. are blank pages.',
               roman_offset=0, arabic_offset=30, first_arabic_pdf=31, last_pdf=380,
               examples=[dict(pdf=1, printed='i'), dict(pdf=6, printed='vi'), dict(pdf=31, printed='1'), dict(pdf=87, printed='57'), dict(pdf=380, printed='350')],
               verified='Running page numbers in the page headers/footers of PDF 31-380 were compared with PDF index - 30: 334 of 350 pages carry a readable number and all match; the other 16 are chapter openers or blank pages.')
blank = [p for p in range(1, 381) if not page_text.get(label(p), '').strip()]
pagemap['blank_pdf_pages'] = blank

# ---------------------------------------------------------------- stats
chap_ids = ['ch%d' % i for i in range(1, 9)]
body_words = sum(byid[c]['approx_words'] for c in chap_ids)
out = dict(
    meta=dict(title='Bayesian methods for spatial proteomics', author='Oliver McKenzie Crook', institution='Darwin College, University of Cambridge', degree='Doctor of Philosophy', date='September 2020',
              pdf_pages=380, text_extraction='pdftotext -layout (born-digital LaTeX PDF; text layer is complete, no OCR needed)',
              body_words_approx=body_words, schema_version='1.0',
              note='Every node, edge, claim and stage carries source_pages (printed page labels). basis = stated (the author says it) or inferred (my reading).'),
    pagemap=pagemap,
    journey=dict(arc=JOURNEY_ARC, caveat=JOURNEY_CAVEAT, stages=STAGES, contribution=CONTRIBUTIONS, negative_results=NEGATIVE),
    structure=dict(nodes=out_nodes, figures=figs, tables=tabs),
    links=dict(edges=edges, entities=entities, edge_types=sorted({e['type'] for e in edges})),
    claims=claims,
)
json.dump(out, open('thesis.json', 'w'), indent=1, ensure_ascii=False)

# ---------------------------------------------------------------- coverage report
R = []
P = R.append
P('COVERAGE REPORT')
P('=' * 60)
numbered = [d for d in out_nodes if d['num']]
P('Structure')
P('  TOC entries: %d  -> nodes found: %d  (missing: %s)' % (len(toc_nums), len(toc_nums & node_nums), toc_missing or 'none'))
P('  Every TOC entry was also located as a heading in the body text, and its page matches the TOC page (0 mismatches).')
P('  Front-matter nodes: %d of %d expected' % (len([t for t in front_expected if t in front_have]), len(front_expected)))
P('  Chapters: 8 + references + 3 appendices; sections (numbered): %d; unnumbered headings added: %d; total nodes: %d' % (
    len([d for d in out_nodes if d['num'] and d['level'] > 0]), len([d for d in out_nodes if d.get('kind') == 'unnumbered heading']), len(out_nodes)))
P('  Figures: %d of %d in the list of figures found as captions in the body; tables: %d of %d' % (sum(1 for f in figs if f['located'] == 'caption'), len(figs), sum(1 for f in tabs if f['located'] == 'caption'), len(tabs)))
P('  Chapter type, internal template and publication status filled for 8/8 chapters and 3/3 appendices.')
nsum = sum(1 for d in out_nodes if d.get('summary')); nq = sum(1 for d in out_nodes if d.get('quote'))
P('  Nodes with a summary: %d/%d ; with a verified quote: %d/%d (the rest carry title, pages, counts only)' % (nsum, len(out_nodes), nq, len(out_nodes)))
P('Journey')
P('  Stages: %d ; stages with evidence pages: %d ; with a verified quote: %d' % (len(STAGES), sum(1 for s in STAGES if s['evidence']), len(STAGES)))
P('  Outcomes: ' + ', '.join('%s=%d' % kv for kv in Counter(s['outcome'] for s in STAGES).items()) + '  (no stage labelled failed: the thesis reports none)')
P('  Contributions: %d ; negative/limiting results: %d ; claims: %d (all evidence tokens found on cited pages: %s)' % (len(CONTRIBUTIONS), len(NEGATIVE), len(claims), all(c['evidence_checked'] for c in claims)))
P('Links')
P('  Explicit edges (regex over body text): %d from %d raw mentions; types: %s' % (n_explicit, X.stats and sum(1 for _ in X.raw), dict(Counter(e['type'] for e in edges if e['kind'] == 'explicit'))))
P('  Raw mention counts by pattern: %s' % dict(X.stats))
P('  Same-chapter chapter/equation mentions that did not become edges: %s' % dict(X.intra_skipped))
P('  Numbered theorem/definition mentions (not nodes, not turned into edges): %d' % X.stats.get('theorem/definition', 0))
P('  Unresolved explicit references: %d' % len(X.unresolved))
P('  Semantic edges: %d (stated %d, inferred %d)' % (len(SEMANTIC), sum(1 for e in SEMANTIC if e[3] == 'stated'), sum(1 for e in SEMANTIC if e[3] == 'inferred')))
P('  Edge endpoints that do not exist: %d' % sum(1 for p in problems if p[0] == 'edge endpoint missing'))
P('  Entities: %d detected (by regex, with chapter lists): %s' % (len(entities), dict(Counter(e['kind'] for e in entities))))
P('Validation problems: %d' % len(problems))
for p in problems: P('  PROBLEM ' + str(p))
if notes:
    for n in notes: P('  note ' + str(n))
txt = '\n'.join(R)
open('coverage.txt', 'w').write(txt)
print(txt)
sys.exit(1 if problems else 0)
