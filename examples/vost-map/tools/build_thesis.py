"""Stage 1c: assemble thesis.json, validate it against the PDF text, and print/write a coverage report."""
import re, json, collections, datetime
from skeleton import *
import xrefs as X
from annotations_nodes import N, F
import annotations_story as A

OUT='../thesis.json'; REPORT='../coverage_report.txt'
nodes,kids,caps=X.nodes,X.kids,X.caps
byid={n['id']:n for n in nodes}

# ---------------------------------------------------------------- page text helpers
def page_text(label):
    return re.sub(r'\s+',' ',pages[pdfidx(label)-1])
def span_text(a,b):
    return ' '.join(page_text(printed(i)) for i in range(pdfidx(a),pdfidx(b)+1))
def squashed(s): return re.sub(r'[^a-z0-9%.]','',s.lower())

# ---------------------------------------------------------------- nodes
LV2={'Preface':'background','Contributions':'background','Introduction':'background','Methods':'method','Results':'result',
     'Results and discussion':'result','Conclusions':'discussion','Related Work':'discussion'}
order=sorted(nodes,key=lambda n:n['pos'])
out={}
def mk(n):
    ann=N.get(n['id'],{})
    parent=n['parent']
    ptype=out[parent]['type'] if parent in out else None
    typ=ann.get('type')
    if not typ:
        typ=LV2.get(n['title']) if (parent and parent.startswith('ch') and n['kind']=='section') else None
        typ=typ or ptype or 'background'
    q=ann.get('quote')
    rec=dict(id=n['id'],number=n['number'],title=n['title'],kind=n['kind'],parent=parent if parent else None,
             children=[],type=typ,
             pages=dict(start=n['start'],end=n['end'],pdf_start=pdfidx(n['start']),pdf_end=pdfidx(n['end'])),
             source_pages=[n['start'],n['end']] if n['start']!=n['end'] else [n['start']],
             approx_words=n['approx_words'],n_figures=n['n_figures'],n_tables=n['n_tables'],
             figures=n['figures'],tables=n['tables'],
             summary=ann.get('summary',''),quote=dict(text=q[0],page=q[1]) if q else None,
             template=ann.get('template'),publication_status=ann.get('pub'),collaboration=ann.get('collab'),
             basis='stated',confidence='high' if ann.get('summary') else 'low')
    return rec
# document order guarantees parents before children (parents start earlier or same page; sort stable by parent depth)
def depth(n):
    d=0;p=n['parent']
    while p and p in byid: d+=1;p=byid[p]['parent']
    return d
for n in sorted(nodes,key=lambda n:(n['pos'],depth(n))): out[n['id']]=mk(n)
# parts not in the TOC
def add_special(i,spec,parent=None):
    a,b=spec['start'],spec['end']
    wc=sum(len(' '.join(page_text(printed(k)).split()).split()) for k in range(pdfidx(a),pdfidx(b)+1))
    q=spec.get('quote')
    out[i]=dict(id=i,number=None,title=spec['title'],kind='front' if i.startswith('fm') else ('back' if i=='refs' else 'part'),parent=parent,children=[],type=spec['type'],
        pages=dict(start=a,end=b,pdf_start=pdfidx(a),pdf_end=pdfidx(b)),source_pages=[a,b] if a!=b else [a],approx_words=wc,n_figures=0,n_tables=0,figures=[],tables=[],
        summary=spec['summary'],quote=dict(text=q[0],page=q[1]) if q else None,template=None,publication_status=None,collaboration=None,basis='stated',confidence='high')
fm_total=0
for k in ['fm.title','fm.dedication','fm.ack','fm.abstract','fm.contents','fm.figures','fm.abbrev']:
    add_special(k,F[k],'fm')
add_special('fm',F['fm'],None); out['fm']['approx_words']=sum(out[k]['approx_words'] for k in out if k.startswith('fm.'))
# the abstract is unlabeled in text; label for tests
add_special('refs',F['refs'],None)
# Appendices part (p.127) – children are appA/appB
ann=N['app']; out['app']=dict(id='app',number=None,title='Appendices',kind='part',parent=None,children=[],type='appendix',pages=dict(start='127',end='140',pdf_start=149,pdf_end=162),
    source_pages=['127','140'],approx_words=len(page_text('127').split())+out['appA']['approx_words']+out['appB']['approx_words'],n_figures=out['appA']['n_figures']+out['appB']['n_figures'],
    n_tables=out['appA']['n_tables']+out['appB']['n_tables']+1,figures=[],tables=[],leaf_children=[],summary=ann['summary'],quote=None,template=None,publication_status=None,collaboration=None,basis='stated',confidence='high')
# uncaptioned Table in B.2
out['sB.2']['tables'].append(dict(label='(uncaptioned)',page='138',basis='counted manually: full PoseBusters table has no caption'))
out['sB.2']['n_tables']+=1; out['appB']['n_tables']+=1
for k,v in out.items():
    p=v['parent']
    if p: out[p]['children'].append(k)
# keep document order of children
pos_of={k:(byid[k]['pos'] if k in byid else (pdfidx(out[k]['pages']['start']),0)) for k in out}
for v in out.values(): v['children'].sort(key=lambda c:pos_of[c])
# resolve levels in order
def lvl(i):
    p=out[i]['parent']; return 0 if not p else lvl(p)+1
for i in out: out[i]['level']=lvl(i)
roots=['fm','ch1','ch2','ch3','ch4','ch5','ch6','app','refs']

# ---------------------------------------------------------------- figure / table leaf nodes
def caption_words(c,n=22):
    ls=body_lines(c['pdf']); i=[j for j,(k,t) in enumerate(ls) if k==c['line']][0]
    txt=' '.join(t for k,t in ls[i:i+3]); txt=re.sub(r'^(Figure|Table) \S+:\s*','',txt)
    return ' '.join(txt.split()[:n])
fig_ids={}
for c in caps:
    nid=('fig' if c['kind']=='figure' else 'tab')+c['label']; fig_ids[(c['kind'],c['label'])]=nid
    cw=caption_words(c); short=re.split(r'[.;:(]',cw)[0]; sw=short.split()[:9]
    while sw and sw[-1].lower() in {'using','of','on','with','and','the','a','to','for','in','by','from','at','as','is','are'}: sw.pop()
    short=' '.join(sw)
    home=out[c['home']]
    lab=('Figure ' if c['kind']=='figure' else 'Table ')+c['label']
    out[nid]=dict(id=nid,number=c['label'],title=f"{lab} · {short}",kind=c['kind'],parent=c['home'],children=[],type=home['type'],
        pages=dict(start=c['printed'],end=c['printed'],pdf_start=c['pdf'],pdf_end=c['pdf']),source_pages=[c['printed']],approx_words=0,n_figures=0,n_tables=0,figures=[],tables=[],
        summary=f"{lab} is printed on p. {c['printed']}; placed under {home['title']} because that is where it is first cited ({c['home_basis']}).",
        quote=dict(text=cw,page=c['printed']),template=None,publication_status=None,collaboration=None,basis='stated',confidence='high',leaf=True)
    for lst,key in ((home['figures'],'figure'),(home['tables'],'table')):
        pass
# rebuild the figures/tables lists on sections as references to the new nodes
for v in list(out.values()):
    v['leaf_children']=[]
for (k,l),nid in fig_ids.items():
    home=out[out[nid]['parent']]; home['leaf_children'].append(nid)
# uncaptioned table in B.2
out['tabB.2-full']=dict(id='tabB.2-full',number='B.2 (uncaptioned)',title="Table · Full PoseBusters outputs (uncaptioned)",kind='table',parent='sB.2',children=[],type='appendix',
    pages=dict(start='138',end='138',pdf_start=160,pdf_end=160),source_pages=['138'],approx_words=0,n_figures=0,n_tables=0,figures=[],tables=[],
    summary="Full PoseBusters sub-test pass rates for every model and ablation; the thesis gives this table no caption or number.",quote=None,template=None,publication_status=None,collaboration=None,basis='stated',confidence='high',leaf=True,leaf_children=[])
out['sB.2']['leaf_children'].append('tabB.2-full')
for v in out.values():
    v['figures']=[i for i in v['leaf_children'] if i.startswith('fig')]
    v['tables']=[i for i in v['leaf_children'] if i.startswith('tab')]
for v in out.values():
    v['leaf_children'].sort(key=lambda i:(out[i]['kind'],pdfidx(out[i]['pages']['start']),i))
    v['figures']=[i for i in v['leaf_children'] if i.startswith('fig')]; v['tables']=[i for i in v['leaf_children'] if i.startswith('tab')]
# claims -> figure/table nodes
for cl in A.CLAIMS:
    ev=[]
    for kind,lab in re.findall(r'(Fig|Table) ([A-Z]?\d*\.?\d+)',cl['evidence'] or ''):
        nid=('fig' if kind=='Fig' else 'tab')+lab
        if nid in out: ev.append(nid)
    cl['evidence_nodes']=ev

# ---------------------------------------------------------------- edges
xr=json.load(open('xrefs.json'))
edges=[]
for e in xr['edges']:
    e=dict(e)
    if e['source']=='sA.3' and e['target']=='s3.4.2':
        e['confidence']='low'; e['reason']+=' (flagged: probably a typo for section 2.5.2.2, see anomaly a1)'
    edges.append(e)
edges+=A.SEMANTIC
ent_chap={}
# ---------------------------------------------------------------- entities
CH_KEYS=[('fm',(9,10)),('ch1',(23,54)),('ch2',(55,88)),('ch3',(89,108)),('ch4',(109,124)),('ch5',(125,144)),('ch6',(145,148)),('appA',(151,158)),('appB',(159,162))]
def chap_of(idx):
    for k,(a,b) in CH_KEYS:
        if a<=idx<=b: return k
ents=[]
for eid,name,cat,rx,desc in A.ENT:
    rg=re.compile(rx); chs=collections.OrderedDict(); first=None; total=0
    for idx in list(range(9,11))+list(range(23,163)):
        c=chap_of(idx)
        if c is None: continue
        lines=[(k,t) for k,t in body_lines(idx) if not is_header(t)] if idx>=23 else [(k,norm(l)) for k,l in enumerate(pages[idx-1].split('\n')) if norm(l)]
        flat=' '.join(t for k,t in lines)
        m=rg.findall(flat)
        if m:
            d=chs.setdefault(c,dict(count=0,pages=[]))
            d['count']+=len(m); total+=len(m)
            pl=printed(idx)
            if pl not in d['pages']: d['pages'].append(pl)
            if first is None:
                for k,t in lines:
                    if rg.search(t): first=(idx,k); break
    fn=None
    if first:
        fn=node_at(nodes,first)['id'] if first[0]>=23 else 'fm.abstract'
    for d in chs.values(): d['pages']=d['pages'][:12]
    ents.append(dict(id=eid,name=name,category=cat,description=desc,total_mentions=total,chapters=chs,first_node=fn,basis='stated',confidence='high' if total else 'low'))

# ---------------------------------------------------------------- journey
def pivot_list():
    ps=[]
    for s in A.STAGES:
        if s['outcome']=='pivot' or s.get('next') and s['id'] in('j3','j7','j9','j11'):
            ps.append(dict(from_stage=s['id'],to_stage=s['next'],why=s['why_next'],pages=s['evidence'][-3:],basis='stated'))
    return ps
journey=dict(order_note=A.ORDER_NOTE,origin=A.ORIGIN,stages=A.STAGES,destination=A.DESTINATION,arc=A.ARC,contribution=A.CONTRIBUTIONS,transitions=pivot_list())

doc=dict(
 meta=dict(title="Machine Learning for Molecular Modelling and Drug Discovery",author="Lucy Vost",institution="Green Templeton College, University of Oxford",
           degree="DPhil / PhD thesis",date="October 2025",source_pdf="dj67314964.pdf",pdf_pages=177,
           extraction=dict(tool="pdftotext -layout",ocr_used=False,text_layer="clean (about 54,000 words extracted)",generated=datetime.date.today().isoformat()),
           page_map=dict(rule="printed = pdf_index - 22 for body pages (pdf 23 = p. 1); front matter is roman: printed = roman(pdf_index - 2) (pdf 3 = i); pdf 1-2 are cover pages with no printed number",
                         pdf_index_to_printed={str(i):printed(i) for i in range(1,178)}),
           all_page_references_are="printed page numbers"),
 journey=journey,
 structure=dict(roots=roots,nodes=out,
   chapter_templates={k:out[k]['template'] for k in ['ch1','ch2','ch3','ch4','ch5','ch6'] },
   note="No chapter has a section called 'Limitations' or 'Discussion and limitations'; limitations sit inside the Preface and Conclusions sections. The thesis has a List of Figures but no List of Tables."),
 links=dict(edge_types=sorted({e['type'] for e in edges}),edges=edges,entities=ents,claims=A.CLAIMS),
 quality=dict(anomalies=A.ANOMALIES)
)

# ================================================================ VALIDATION
rep=[]; P=rep.append
fails=0
# a. TOC coverage ------------------------------------------------
tocflat=' '.join(norm(l) for idx in range(11,15) for l in pages[idx-1].split('\n') if norm(l))
tocflat=re.sub(r'(?:x|xi|xii|ix) Contents|Contents (?:x|xi|xii)','',tocflat)
# independent list of numbered entries as printed in the PDF contents
pdf_nums=set(m.group(1) for m in re.finditer(r'(?<![\w.])(\d+(?:\.\d+){1,}|[A-Z]\.\d+)\s+[A-Z]',tocflat))
pdf_nums|=set(m.group(1) for m in re.finditer(r'(?<![\w.])([1-6])\s+(?:Introduction|Fragment elaboration|Improving|Molecule diffusion|Cryo-EM model|Conclusions and)',tocflat))
pdf_nums|=set(m.group(1) for m in re.finditer(r'(?<![\w.])([AB])\s+Appendix:',tocflat))
mine={n['number'] for n in nodes if n['number']}
P("== TOC COVERAGE ==")
P(f"Numbered entries found in the PDF's own contents pages (ix-xii): {len(pdf_nums)}")
P(f"Nodes with a section number: {len(mine)}  | unnumbered run-in headings listed in the TOC: {sum(1 for n in nodes if n['kind']=='run-in')}")
missing=sorted(pdf_nums-mine); extra=sorted(mine-pdf_nums)
P(f"TOC entries without a node: {missing or 'none'}"); P(f"Nodes whose number is not in the TOC: {extra or 'none'}")
bad=[]
for n in nodes:
    if n['number']:
        pat=re.escape(n['number'])+r'\s+[^|]{0,150}?(?:\. ){1,}\.?\s*'+re.escape(n['start'])+r'(?!\d)' if n['kind']!='chapter' and n['kind']!='appendix' else re.escape(n['number'])+r'\s+[A-Z][^|]{0,150}?\s'+re.escape(n['start'])+r'(?!\d)'
        if not re.search('(?<![\\w.])'+pat,tocflat): bad.append((n['number'],n['start']))
    else:
        if not re.search(re.escape(n['title'])+r'[ .]*?'+re.escape(n['start'])+r'(?!\d)',tocflat): bad.append((n['title'],n['start']))
P(f"Nodes whose (number/title, start page) is not confirmed by the PDF contents pages: {bad or 'none'}  (checked {len(nodes)})")
if missing or bad: fails+=1
nf=[n['id'] for n in nodes if not n['heading_found']]
P(f"Headings located on their stated printed page in the body text: {len(nodes)-len(nf)}/{len(nodes)}  not found: {nf or 'none'}")
if nf: fails+=1
unsum=[k for k,v in out.items() if not v['summary']]
P(f"Nodes lacking a summary: {unsum or 'none'}")
leafs_all=[k for k,v in out.items() if v.get('leaf')]
P(f"Total nodes: {len(out)}  (front matter {sum(1 for v in out.values() if v['kind']=='front')}, TOC nodes {len(nodes)}, plus 'app' part, 'refs' and {len(leafs_all)} figure/table leaves)")
# figures / tables
P(f"Figures captured: {sum(1 for c in caps if c['kind']=='figure')} (List of Figures has 26)  | numbered table captions: {sum(1 for c in caps if c['kind']=='table')} + 1 uncaptioned (B.2)")
# b. edges ----------------------------------------------------------
P("\n== EDGES ==")
bad_e=[e['id'] for e in edges if e['source'] not in out or e['target'] not in out]
P(f"Edges: {len(edges)} total | explicit {sum(1 for e in edges if e['kind']=='explicit')} | semantic {sum(1 for e in edges if e['kind']=='semantic')} (stated {sum(1 for e in edges if e['kind']=='semantic' and e['basis']=='stated')}, inferred {sum(1 for e in edges if e['basis']=='inferred')})")
P(f"Edge endpoints missing from nodes: {bad_e or 'none'}")
nosrc=[e['id'] for e in edges if not e.get('source_pages')]; P(f"Edges without source_pages: {nosrc or 'none'}")
noreason=[e['id'] for e in edges if e['basis']=='inferred' and not e.get('reason')]; P(f"Inferred edges without a reason: {noreason or 'none'}")
P(f"Explicit references found: {xr['raw_count']} raw, {len(xr['edges'])} inter-node edges after merging, {xr['dropped_self_refs']} references inside their own node dropped, unresolved: {len(xr['unresolved'])} -> {[u[:3] for u in xr['unresolved']]}")
P(f"Low-confidence edges: {[e['id']+' ('+e['source']+'->'+e['target']+')' for e in edges if e['confidence']=='low']}")
sem_pages_bad=[]
for e in edges:
    for p in e['source_pages']:
        try: pdfidx(p)
        except Exception: sem_pages_bad.append((e['id'],p))
P(f"Edge page labels that are not valid printed pages: {sem_pages_bad or 'none'}")
if bad_e or nosrc or noreason: fails+=1
# c. entities ----------------------------------------------------------
leafs=[k for k,v in out.items() if v.get('leaf')]
tgt_ids={e['target'] for e in edges}
P(f"Figure/table leaf nodes: {sum(1 for k in leafs if k.startswith('fig'))} figures + {sum(1 for k in leafs if k.startswith('tab'))} tables; with an incoming reference edge: {sum(1 for k in leafs if k in tgt_ids)}")
P(f"Figure/table nodes never cited in the text: {[k for k in leafs if k not in tgt_ids] or 'none'}")
P(f"Edges into figure/table nodes: {sum(1 for e in edges if e['target'] in leafs)} (hidden by default in the Links view)")
P(f"Claims whose figure/table evidence did not resolve to a node: {[c['id'] for c in A.CLAIMS if c['evidence'] and not c['evidence_nodes']] or 'none'}")
P("\n== ENTITIES ==")
P(f"{len(ents)} entities; with zero mentions: {[e['id'] for e in ents if e['total_mentions']==0] or 'none'}")
P("by category: "+str(dict(collections.Counter(e['category'] for e in ents))))
# d. quotes --------------------------------------------------------------
P("\n== QUOTES ==")
qbad=[];nq=0
def quote_ok(text,page):
    return squashed(text) in squashed(page_text(page))
for k,v in out.items():
    q=v['quote']
    if q:
        nq+=1
        words=len(q['text'].split())
        if words>=25 or not quote_ok(q['text'],q['page']): qbad.append((k,q['page'],words))
P(f"{nq} node quotes; failing (not verbatim on stated page or >=25 words): {qbad or 'none'}")
if qbad: fails+=1
# e. journey -------------------------------------------------------------
P("\n== JOURNEY ==")
allst=[A.ORIGIN]+A.STAGES+[A.DESTINATION]
noev=[s['id'] for s in allst if not s.get('evidence')]
P(f"Stages: {len(A.STAGES)} (+ start and end markers). Stages without evidence pages: {noev or 'none'}")
P("Outcomes: "+str(dict(collections.Counter(s['outcome'] for s in A.STAGES)))+f" | negative results flagged: {[s['id'] for s in A.STAGES if s.get('negative_result')]}")
bn=[(s['id'],n) for s in allst for n in s['nodes'] if n not in out]; P(f"Stage nodes that do not exist: {bn or 'none'}")
bch=[]
for s in A.STAGES:
    lo=min(pdfidx(out[c]['pages']['start']) for c in s['chapters']); hi=max(pdfidx(out[c]['pages']['end']) for c in s['chapters'])
    # evidence may sit in an appendix for this chapter
    for p in s['evidence']:
        if not(lo<=pdfidx(p)<=hi) and not any(pdfidx(out[a]['pages']['start'])<=pdfidx(p)<=pdfidx(out[a]['pages']['end']) for a in ('appA','appB')): bch.append((s['id'],p))
P(f"Evidence pages outside the stage's chapters (and appendices): {bch or 'none'}")
claims_by_stage=collections.Counter(c['stage'] for c in A.CLAIMS)
P("Claims per stage: "+str(dict(sorted(claims_by_stage.items(),key=lambda kv:int(kv[0][1:])))))
P(f"Stages with no claim attached: {[s['id'] for s in A.STAGES if claims_by_stage[s['id']]==0] or 'none'}")
# f. claims / numbers -------------------------------------------------------
P("\n== CLAIMS ==")
bc=[(c['id'],c['node']) for c in A.CLAIMS if c['node'] not in out]; P(f"{len(A.CLAIMS)} claims; unknown nodes: {bc or 'none'}")
WORDS={'1':'one','2':'two','3':'three','4':'four','5':'five','6':'six','7':'seven','8':'eight','9':'nine','10':'ten'}
def numbers(text):
    t=re.sub(r'ΔSLE20|Mac1|NSP14|MolFM|GEOM|QM9|GCDM|HierDiff|CMD-GEN|Cα|Å|Ch \d|Chapter \d|Appendix [A-Z]\.\d|Table \d\.\d|Fig \d\.\d|p\. \d+|pp\. [\d-]+',' ',text)
    t=re.sub(r'\b\d[A-Z0-9]{3}\b',' ',t)     # PDB codes
    return re.findall(r'(?<![\w.])\d{1,3}(?:,\d{3})+(?![\w])|(?<![\w.])-?\d+(?:\.\d+)?(?![\w])',t)
def check_numbers(label,text,pgs):
    body=' '.join(page_text(p) for p in pgs)
    miss=[]
    for tok in numbers(text):
        tok=tok.lstrip('-')
        alts=[tok]+([WORDS[tok]] if tok in WORDS else [])
        if not any(re.search(r'(?<![\d.])'+re.escape(a)+r'(?![\d])',body,re.I) for a in alts): miss.append(tok)
    return miss
nm=[]
for c in A.CLAIMS:
    m=check_numbers(c['id'],c['text'],c['pages'])
    if m: nm.append((c['id'],m))
P(f"Claim numbers not found on the cited pages (to review): {nm or 'none'}")
nm2=[]
for s in A.STAGES:
    m=check_numbers(s['id'],s['outcome_note']+' '+s['approach'],s['evidence'])
    if m: nm2.append((s['id'],m))
P(f"Stage numbers not found on evidence pages (to review): {nm2 or 'none'}")
# g. appendix list checks ----------------------------------------------------------
t133=page_text('133')+' '+page_text('134')
ids=re.search(r'PDB IDs of the randomly selected subset of 20 structures.*?are (.*?)\. A\.4',page_text('133'))
n28=len(re.findall(r'\b[0-9][A-Z0-9]{3}\b',ids.group(1))) if ids else None
fg=re.search(r'following PDB codes: (.*?)\. We found',page_text('134')); nf16=len(re.findall(r'\b[0-9][A-Z0-9]{3}\b',fg.group(1))) if fg else None
P(f"Anomaly checks: PDB IDs listed in A.3 for the '20 structures': {n28}; FGFR1 codes listed in A.4 for '18 structures': {nf16}")
# h. page coverage ---------------------------------------------------------------------
covered=set()
for v in out.values():
    if v['kind'] in('chapter','appendix','front','back') or v['id'] in ('fm','app'):
        for i in range(v['pages']['pdf_start'],v['pages']['pdf_end']+1): covered.add(i)
unc=[printed(i) for i in range(3,178) if i not in covered]
P(f"\nPrinted pages not inside any top-level part (blank versos / dividers): {unc}")
tot_words=len(' '.join(pages).split())
P(f"Words: extracted text {tot_words}; sum of top-level node words {sum(out[k]['approx_words'] for k in roots)}")
p138=page_text('138')
rows=re.findall(r'GEOMno h baseline (.*?) GEOMno h conditioned',p138)
P(f"Anomaly a5 check: Appendix B.2 MolFM GEOM baseline row identical to GCDM GEOM baseline row: {len(rows)==2 and rows[0]==rows[1]}")
P("\n== ANOMALIES FOUND IN THE THESIS ==")
for a in A.ANOMALIES: P(f"- [{a['id']}] {a['where']}: {a['what']}")
doc['quality']['coverage_report']='\n'.join(rep)
doc['quality']['validation_failures']=fails
json.dump(doc,open(OUT,'w'),ensure_ascii=False,indent=1)
open(REPORT,'w').write('\n'.join(rep)+'\n')
print('\n'.join(rep))
print('\nthesis.json bytes',len(open(OUT).read()),'validation_failures',fails)
