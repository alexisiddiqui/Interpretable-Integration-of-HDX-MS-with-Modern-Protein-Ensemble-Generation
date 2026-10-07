"""Stage 1a: structure ranges, word counts, explicit cross-reference edges.
Printed page = PDF index - 1 (verified on 244/266 pages, see pagemap.py)."""
import re, json, collections
from toc import TOC, END_PAGE

def ptxt(p):  # printed page -> OCR text
    return open(f'ocr/p{p+1:03d}.txt').read()

# ---------- 1. node ranges (pages) ----------
ids = [t[0] for t in TOC]
node = {t[0]: dict(id=t[0], parent=t[1], level=t[2], number=t[3], title=t[4], start=t[5]) for t in TOC}
order = [t[0] for t in TOC]

# 'main flow' = the sequence in which nodes appear in the document, used to find next start.
def doc_order_key(i):
    return (node[i]['start'], order.index(i))
flow = sorted(order, key=doc_order_key)

# heading offset on its start page (to split pages where two nodes begin)
def find_heading_offset(n):
    t = ptxt(n['start'])
    if n['number'] and n['level'] > 0 or n['id'].startswith('ch'):
        num = n['number']
        title = n['title'].split(':')[0]
        pats = []
        if n['id'].startswith('ch') and num.isdigit():
            pats = [r'Chapter\s+%s\b' % num]
        elif n['id'].startswith('app'):
            pats = [r'Appendix\s+%s\b' % num]
        else:
            pats = [r'^\s*%s\.?\s+%s' % (re.escape(num), re.escape(title[:12])), r'^\s*%s\.?\s' % re.escape(num)]
        for pat in pats:
            m = re.search(pat, t, re.M)
            if m:
                return m.start()
    return 0

for i in order:
    node[i]['heading_off'] = find_heading_offset(node[i])

# ends: next node in flow that is not a descendant
def descendants(i):
    out = []
    for j in order:
        p = node[j]['parent']
        while p:
            if p == i:
                out.append(j); break
            p = node[p]['parent']
    return out

# build global text with absolute offsets
page_off = {}
buf = []
pos = 0
for p in range(0, END_PAGE + 1):
    t = ptxt(p)
    page_off[p] = pos
    buf.append(t); pos += len(t) + 1
G = '\n'.join(buf)

for i in order:
    n = node[i]
    n['abs_start'] = page_off[n['start']] + n['heading_off']

# sort by absolute start; chapter-level nodes take precedence ties
flow = sorted(order, key=lambda i: (node[i]['abs_start'], node[i]['level'], order.index(i)))
# a node's own text = from its start to the next node's start (own text excludes children)
own = {}
for k, i in enumerate(flow):
    s = node[i]['abs_start']
    e = node[flow[k+1]]['abs_start'] if k + 1 < len(flow) else len(G)
    own[i] = (s, e)

def abs_to_page(a):
    ps = [p for p in page_off if page_off[p] <= a]
    return max(ps)

# subtree text range / pages
for i in order:
    n = node[i]
    ds = descendants(i)
    starts = [own[i][0]] + [own[d][0] for d in ds]
    ends = [own[i][1]] + [own[d][1] for d in ds]
    s, e = min(starts), max(ends)
    n['abs_range'] = (s, e)
    n['page_start'] = n['start']
    n['page_end'] = abs_to_page(max(s, e - 1))
    n['words_own'] = len(G[own[i][0]:own[i][1]].split())
    n['approx_words'] = len(G[s:e].split())

# chapters in flow: fix page_end of chapters: end at (next top-level start) - 1 pages
tops = [i for i in order if node[i]['parent'] is None]
tops_sorted = sorted(tops, key=lambda i: node[i]['start'])
for k, i in enumerate(tops_sorted):
    nxt = node[tops_sorted[k+1]]['start'] if k + 1 < len(tops_sorted) else END_PAGE + 1
    node[i]['page_end'] = nxt - 1 if node[i]['id'] != 'front' else 18
# the front matter and chapters: children end at next sibling/next flow start
for i in order:
    n = node[i]
    if n['parent'] is None: continue
    sibs = [j for j in order if node[j]['parent'] == n['parent']]
    idx = sibs.index(i)
    if idx + 1 < len(sibs):
        n['page_end'] = max(n['start'], node[sibs[idx+1]]['start'] - (0 if node[sibs[idx+1]]['heading_off'] > 50 else 1))
        # if next sibling starts mid-page this page is shared; page_end = its start page
        if node[sibs[idx+1]]['heading_off'] > 50:
            n['page_end'] = node[sibs[idx+1]]['start']
    else:
        n['page_end'] = node[n['parent']]['page_end']
# containers (2.1 etc.) end = last child end
for i in order:
    kids = [j for j in order if node[j]['parent'] == i]
    if kids and node[i]['level'] >= 1:
        node[i]['page_end'] = max(node[k]['page_end'] for k in kids)
# special: front pages
node['front.title']['page_end'] = 0
node['front.proquest']['page_end'] = 1
node['front.contents']['page_end'] = 10
node['front.abstract']['page_end'] = 11
node['front.declaration']['page_end'] = 12
node['front.copyright']['page_end'] = 14
node['front.epigraph']['page_end'] = 15
node['front.ack']['page_end'] = 16
node['front.acronyms']['page_end'] = 18

# ---------- 2. resolve a text position to the deepest node ----------
def node_at(a):
    best = None
    for i in flow:
        if own[i][0] <= a < own[i][1]:
            best = i
    return best

# ---------- 3. explicit references ----------
BODY_PAGES = list(range(19, 186)) + list(range(211, 232))   # main text + appendices B, C (not the embedded paper/bib)
num = r'(\d{1,2}(?:\.\d{1,2}){1,2}|[A-C]\.\d)'
def parse_list(s):
    return re.findall(num, s)

patterns = {
 'section': re.compile(r'\b[Ss]ections?\s+((?:\d{1,2}(?:\.\d{1,2}){0,2}|[A-C]\.\d)(?:\s*(?:,|and|&)\s*(?:\d{1,2}(?:\.\d{1,2}){0,2}|[A-C]\.\d))*)'),
 'chapter': re.compile(r'\bChapters?\s+(\d(?:\s*(?:,|and)\s*\d)*)'),
 'appendix': re.compile(r'\bAppendi(?:x|ces)\s+([A-C](?:\.\d)?(?:\s*(?:,|and)\s*[A-C](?:\.\d)?)*)'),
 'figure': re.compile(r'\b[Ff]ig(?:ure|ures|\.)\s+(\d\.\d{1,2}(?:\s*(?:,|and)\s*\d\.\d{1,2})*)'),
 'table': re.compile(r'\b[Tt]able\s+(\d\.\d{1,2})'),
 'equation': re.compile(r'\b[Ee]q(?:uation|uations|n\.|\.)\s*s?\s*((?:\d\.\d{1,3}|[A-C]\.\d{1,3})(?:\s*(?:,|and)\s*(?:\d\.\d{1,3}|[A-C]\.\d{1,3}))*)'),
 'page': re.compile(r'\bpage\s+(\d{1,3})\b'),
}

def valid_section(label):
    return label in node

# figure / table / equation resolution
fig_node = {  # caption page -> hand-assigned (semantic) node; see notes in thesis.json
 '2.1':'2.1.3','2.2':'2.2.4','2.3':'2.2.4',
 '3.1':'3.1.1','3.2':'3.1.2','3.3':'3.3','3.4':'3.4.2','3.5':'3.4.2','3.6':'3.4.2','3.7':'3.4.3','3.8':'3.4.3',
 '4.1':'4.2.4','4.2':'4.2.4','4.3':'4.2.5','4.4':'4.2.5','4.5':'4.3.1','4.6':'4.3.1','4.7':'4.3.2','4.8':'4.3.3',
 '5.1':'ch5','5.2':'5.3.1','5.3':'5.3.1','5.4':'5.3.2','5.5':'5.4.1','5.6':'5.4.1',
 '5.7':'5.4.2','5.8':'5.4.2','5.9':'5.4.2','5.10':'5.4.2','5.11':'5.4.2','5.12':'5.4.2','5.13':'5.4.2'}
fig_page = {'2.1':33,'2.2':45,'2.3':46,'3.1':88,'3.2':91,'3.3':99,'3.4':107,'3.5':108,'3.6':108,'3.7':110,'3.8':111,
            '4.1':132,'4.2':134,'4.3':136,'4.4':136,'4.5':138,'4.6':139,'4.7':140,'4.8':142,
            '5.1':147,'5.2':163,'5.3':165,'5.4':166,'5.5':169,'5.6':170,'5.7':171,'5.8':172,'5.9':174,'5.10':175,
            '5.11':177,'5.12':178,'5.13':179}
tab_node = {'2.1':'2.4.1','3.1':'3.4.1','4.1':'4.2.2'}
tab_page = {'2.1':59,'3.1':103,'4.1':128}

# equation label -> node (first page where "(N.M)" appears at end of a line as a label)
eq_node = {}
eq_page = {}
def chap_of_page(p):
    if p >= 221: return 'C'
    if p >= 211: return 'B'
    for t in reversed(tops_sorted):
        if node[t]['start'] <= p and t.startswith('ch'): return t[2:]
    return '?'
for p in BODY_PAGES:
    t = ptxt(p)
    for m in re.finditer(r'\(((?:\d|[A-C])\.\d{1,3})\)\s*$', t, re.M):
        lab = m.group(1)
        if lab.split('.')[0] != chap_of_page(p): continue
        if lab not in eq_node:
            a = page_off[p] + m.start()
            eq_node[lab] = node_at(a)
            eq_page[lab] = p

# labels whose number OCR dropped; resolved by hand against the page images / text (printed page in comment)
EQ_MANUAL = {'2.46':('2.2.2',40),'2.49':('2.2.2',40),'2.58':('2.2.3',42),'2.75':('2.2.4',48),
             '3.17':('3.2.1',93),'3.14':('3.1.2',92),'4.13':('4.1.2',122),'4.8':('4.1.1',120),'5.5':('5.1.2',150),
             'C.1':('C.1',221),'C.16':('C.2',225),'C.5':('C.1',222),'C.25':('C.3',227)}
for k,(nd,pg) in EQ_MANUAL.items():
    if k not in eq_node: eq_node[k]=nd; eq_page[k]=pg
edges = collections.OrderedDict()
unresolved = []
selfrefs = 0
def add_edge(src, dst, rtype, ref_text, page, conf='high'):
    global selfrefs
    if src == dst:
        selfrefs += 1; return
    key = (src, dst, rtype)
    e = edges.setdefault(key, dict(source=src, target=dst, kind='explicit', basis='stated', type=rtype,
                                   refs=[], source_pages=[], confidence=conf))
    if ref_text not in e['refs']: e['refs'].append(ref_text)
    if page not in e['source_pages']: e['source_pages'].append(page)
    if conf != 'high': e['confidence'] = conf

raw_refs = 0
for p in BODY_PAGES:
    t = ptxt(p)
    for kind, pat in patterns.items():
        for m in pat.finditer(t):
            a = page_off[p] + m.start()
            src = node_at(a)
            if src is None: continue
            raw = m.group(1)
            if kind in ('figure', 'table') and t[m.end():m.end()+1] == ':':
                continue   # a caption, not a reference
            if kind == 'section':
                labels = re.findall(r'\d{1,2}(?:\.\d{1,2}){0,2}|[A-C]\.\d', raw)
                for lab in labels:
                    raw_refs += 1
                    tgt = 'ch'+lab if '.' not in lab and lab.isdigit() else lab
                    if lab in node: tgt = lab
                    if tgt in node:
                        add_edge(src, tgt, 'section_ref', f'Section {lab}', p)
                    else:
                        unresolved.append((p, f'Section {lab}'))
            elif kind == 'chapter':
                for lab in re.findall(r'\d', raw):
                    raw_refs += 1
                    tgt = 'ch'+lab
                    if tgt in node: add_edge(src, tgt, 'chapter_ref', f'Chapter {lab}', p)
                    else: unresolved.append((p, f'Chapter {lab}'))
            elif kind == 'appendix':
                for lab in re.findall(r'[A-C](?:\.\d)?', raw):
                    raw_refs += 1
                    tgt = lab if '.' in lab else 'app'+lab
                    if tgt in node: add_edge(src, tgt, 'appendix_ref', f'Appendix {lab}', p)
                    else: unresolved.append((p, f'Appendix {lab}'))
            elif kind == 'figure':
                for lab in re.findall(r'\d\.\d{1,2}', raw):
                    raw_refs += 1
                    tgt = fig_node.get(lab)
                    if tgt: add_edge(src, tgt, 'figure_ref', f'Figure {lab}', p, 'medium')
                    else: unresolved.append((p, f'Figure {lab}'))
            elif kind == 'table':
                lab = raw; raw_refs += 1
                tgt = tab_node.get(lab)
                if tgt: add_edge(src, tgt, 'table_ref', f'Table {lab}', p, 'medium')
                else: unresolved.append((p, f'Table {lab}'))
            elif kind == 'equation':
                for lab in re.findall(r'(?:\d|[A-C])\.\d{1,3}', raw):
                    raw_refs += 1
                    tgt = eq_node.get(lab)
                    if tgt: add_edge(src, tgt, 'equation_ref', f'Eq. {lab}', p, 'medium')
                    else: unresolved.append((p, f'Eq. {lab}'))
            elif kind == 'page':
                raw_refs += 1
                pg = int(raw)
                if 0 <= pg <= END_PAGE:
                    # deepest node containing the page start
                    cand = [i for i in flow if node[i]['abs_range'][0] <= page_off[pg] + 1 < node[i]['abs_range'][1]]
                    # use own-range node at the middle of page
                    tgt = node_at(page_off[pg] + len(ptxt(pg)) // 2)
                    if tgt: add_edge(src, tgt, 'page_ref', f'page {pg}', p, 'medium')
                else:
                    unresolved.append((p, f'page {pg}'))

if __name__ == '__main__':
    print('nodes', len(node))
    for i in order:
        n = node[i]
        print(f"{i:10s} p.{n['page_start']:>3}-{n['page_end']:<3} words~{n['approx_words']:>6} own~{n['words_own']:>5} head_off={n['heading_off']}")
    print('raw refs', raw_refs, 'edges', len(edges), 'self refs', selfrefs, 'unresolved', len(unresolved))
    print(collections.Counter(e['type'] for e in edges.values()))
    print('unresolved sample', unresolved[:60])
    print(len(eq_node), 'equation labels found')
