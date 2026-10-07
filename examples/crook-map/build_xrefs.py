import re,json
from collections import defaultdict
import build_struct2 as S
L,page_at,pdf_at=S.L,S.page_at,S.pdf_at
nodes=S.nodes; byid=S.byid
sec_ids={n['num']:n['id'] for n in nodes if n['num']}
fig_ids={f['id'][4:] for f in S.figs}; tab_ids={t['id'][4:] for t in S.tabs}
# scan range: PDF 5 .. end, excluding references block and the toc/lof/lot front pages
ref=S.byid['refs']; ref_a,ref_b=ref['pos'],ref['end']
scan=[]
for i,l in enumerate(L):
    if i<B_start if False else False: pass
for i,l in enumerate(L):
    p=pdf_at[i]
    if p<5 or (11<=p<=29) or ref_a<=i<ref_b: continue   # skip toc/lof/lot/abbrev, references
    scan.append(i)
def expand(s):
    nums=[int(x) for x in re.findall(r'\d+',s)]
    if re.search(r'[-–]',s) and len(nums)==2: return list(range(nums[0],nums[1]+1))
    return nums
rx_ch=re.compile(r'\b[Cc]hapters?\s+(\d+(?:\s*(?:,|and|&|,\s*and)\s*\d+)*)')
rx_sec=re.compile(r'\b[Ss]ections?\s+((?:\d+|[A-C])(?:\.\d+)+)')
rx_app=re.compile(r'\b[Aa]ppendi(?:x|ces)\s+([A-C](?:\.\d+)*)\b')
rx_appvague=re.compile(r'\b(?:in|see|to) the (?:supplementary |)appendix\b|\bin the appendix\b|\bappendix\b(?!\s+[A-C])',re.I)
rx_fig=re.compile(r'\b[Ff]ig(?:ure|\.)s?\s+([0-9A-C]+\.\d+)')
rx_tab=re.compile(r'\b[Tt]able\s+([0-9A-C]+\.\d+)')
rx_eq=re.compile(r'\b[Ee]quations?\s*\(?([0-9A-C]+\.\d+)\)?')
rx_thm=re.compile(r'\b(?:[Tt]heorem|[Dd]efinition)\s+(\d+)\b')
raw=[];unresolved=[];stats=defaultdict(int);intra_skipped=defaultdict(int)
def chapter_of(nid):
    n=byid[nid]
    while n['parent']: n=byid[n['parent']]
    return n['id']
def add(src,tgt,typ,line,txt,basis='stated'):
    raw.append(dict(source=src,target=tgt,type=typ,page=page_at[line],text=txt,basis=basis))
for i in scan:
    l0=L[i]; s=l0.strip()
    if l0.startswith('====='): continue
    nxt=L[i+1] if i+1<len(L) and not L[i+1].startswith('=====') else ''
    l=l0+' '+nxt.strip()
    _L0=len(l0)
    src=S.node_for_line(i)
    if src is None: continue
    # skip caption lines (figure/table captions) to avoid self-reference noise
    iscap=bool(re.match(r'^(Fig\.|Table)\s',s))
    # skip running heads: 'Chapter' mention rarely there
    for m in [x for x in rx_ch.finditer(l) if x.start()<_L0]:
        for n in expand(m.group(1)):
            stats['chapter']+=1
            t='ch%d'%n
            if t in byid:
                if chapter_of(src['id'])!=t: add(src['id'],t,'refers_to_chapter',i,m.group(0))
                else: intra_skipped['chapter']+=1
            else: unresolved.append(('chapter',n,page_at[i],s[:80]))
    for m in [x for x in rx_sec.finditer(l) if x.start()<_L0]:
        stats['section']+=1
        k=m.group(1); t=sec_ids.get(k)
        if t:
            if t!=src['id'] and not (byid[t]['parent']==src['id'] and False): add(src['id'],t,'refers_to_section',i,m.group(0))
        else: unresolved.append(('section',k,page_at[i],s[:80]))
    for m in [x for x in rx_app.finditer(l) if x.start()<_L0]:
        stats['appendix']+=1
        k=m.group(1)
        t='app'+k if len(k)==1 else sec_ids.get(k)
        if t and t in byid: add(src['id'],t,'refers_to_appendix',i,m.group(0))
        else: unresolved.append(('appendix',k,page_at[i],s[:80]))
    if not iscap:
        for m in [x for x in rx_fig.finditer(l) if x.start()<_L0]:
            stats['figure']+=1
            k=m.group(1)
            if k in fig_ids:
                home=[f for f in S.figs if f['id']=='fig:'+k] if False else None
                add(src['id'],'fig:'+k,'refers_to_figure',i,m.group(0))
            else: unresolved.append(('figure',k,page_at[i],s[:80]))
        for m in [x for x in rx_tab.finditer(l) if x.start()<_L0]:
            stats['table']+=1
            k=m.group(1)
            if k in tab_ids: add(src['id'],'tab:'+k,'refers_to_table',i,m.group(0))
            else: unresolved.append(('table',k,page_at[i],s[:80]))
    for m in [x for x in rx_eq.finditer(l) if x.start()<_L0]:
        stats['equation']+=1
        k=m.group(1); c='ch'+k.split('.')[0] if k[0].isdigit() else 'app'+k[0]
        if c in byid and chapter_of(src['id'])!=c: add(src['id'],c,'refers_to_equation',i,m.group(0))
        elif c not in byid: unresolved.append(('equation',k,page_at[i],s[:80]))
        else: intra_skipped['equation']+=1
    for m in [x for x in rx_thm.finditer(l) if x.start()<_L0]:
        stats['theorem/definition']+=1
        if chapter_of(src['id'])!='ch2': add(src['id'],'ch2','refers_to_equation',i,m.group(0))
        else: intra_skipped['theorem/definition']+=1
    if rx_appvague.search(l0) and not rx_app.search(l) and chapter_of(src['id']) not in ('appA','appB','appC','refs'):
        c=chapter_of(src['id']); tgt={'ch2':'appA','ch3':'appA','ch6':'appB','ch7':'appC'}.get(c)
        stats['appendix-vague']+=1
        if tgt and src['id'] not in ('appA','appB','appC') and not src['id'].startswith(('sA','sB','sC')): add(src['id'],tgt,'refers_to_appendix',i,'(unnumbered "appendix")',basis='inferred')
        elif not tgt: unresolved.append(('appendix-vague',c,page_at[i],s[:80]))
# aggregate
agg={}
for r in raw:
    k=(r['source'],r['target'],r['type'])
    a=agg.setdefault(k,dict(source=r['source'],target=r['target'],type=r['type'],kind='explicit',basis=r['basis'],pages=[],count=0,examples=[]))
    a['count']+=1
    if r['page'] not in a['pages']: a['pages'].append(r['page'])
    if len(a['examples'])<2 and r['text'] not in a['examples']: a['examples'].append(r['text'])
    if r['basis']=='inferred': a['basis']='inferred'
edges=list(agg.values())
print('regex mentions:',dict(stats))
print('intra-chapter chapter/equation mentions not turned into edges:',dict(intra_skipped))
print('raw refs:',len(raw),'-> aggregated explicit edges:',len(edges))
from collections import Counter
print(Counter(e['type'] for e in edges))
print('UNRESOLVED:',len(unresolved)); 
for u in unresolved[:40]: print(u)
json.dump(dict(edges=edges,unresolved=unresolved,stats=dict(stats),intra=dict(intra_skipped),raw_n=len(raw)),open('xrefs.json','w'),indent=1,ensure_ascii=False)
