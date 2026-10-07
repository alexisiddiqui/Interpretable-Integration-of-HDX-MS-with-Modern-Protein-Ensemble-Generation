"""Stage 1b: explicit cross-references ("see Section 3.2", "Chapter 4", "Fig 5.1", "Appendix A.2") -> resolved edges."""
import re, json, collections
from skeleton import *
nodes,kids,caps=finish(); byid={n['id']:n for n in nodes}
def ancestors(nid):
    out=[]; p=byid[nid]['parent']
    while p: out.append(p); p=byid[p]['parent'] if p in byid else None
    return out
figtab={(c['kind'],c['label']):c['home'] for c in caps}
CH_RNG={'ch1':(23,54),'ch2':(55,88),'ch3':(89,108),'ch4':(109,124),'ch5':(125,144),'ch6':(145,148),'appA':(151,158),'appB':(159,162)}

PAT=[('chapter',re.compile(r'\b[Cc]hapters?\s+(\d)(?:\s*(?:,|and|&)\s*(\d))?')),
     ('section',re.compile(r'\b[Ss]ections?\s+(\d+(?:\.\d+)+)')),
     ('appendix',re.compile(r'\bAppendix\s+([A-Z](?:\.\d+)?)(?![\w])')),
     ('figure',re.compile(r'\bFig(?:ure)?s?\.?\s*(\d+\.\d+|[A-Z]\.\d+)[a-z]?')),
     ('table',re.compile(r'\bTables?\s*(\d+\.\d+|[A-Z]\.\d+|\d+)(?!\d)(?!\.\d)')),
     ('equation',re.compile(r'\b[Ee]q(?:uation|\.)?\s*(\d+\.\d+)'))]
raw=[]; unresolved=[]
for idx in range(23,163):
    lines=[(k,t) for k,t in body_lines(idx) if not is_header(t) and not t.startswith('Appendix: chapter')]
    flat=''; offs=[]
    for k,t in lines:
        offs.append((len(flat),k)); flat+=t+' '
    for kind,pat in PAT:
        for m in pat.finditer(flat):
            ln=max(o for o in offs if o[0]<=m.start())[1]
            if CAP.match(dict(lines)[ln]) if ln in dict(lines) else False: continue   # skip text inside captions' own label
            src=node_at(nodes,(idx,ln))
            ctx=flat[max(0,m.start()-40):m.end()+30].strip()
            labels=[g for g in m.groups() if g]
            for lab in labels:
                if kind=='chapter': tid=f'ch{lab}'
                elif kind=='section': tid=f's{lab}'
                elif kind=='appendix': tid=('sA.%s'%lab[2:] if False else (f'app{lab}' if len(lab)==1 else f's{lab}'))
                elif kind in('figure','table'):
                    key=(kind,lab); amb=False
                    if kind=='table' and '.' not in lab:       # "Table 1": resolve inside the current chapter, flag low confidence
                        ch=[c for c,(a,b) in CH_RNG.items() if a<=idx<=b][0]; key=(kind,f'{ch[2:]}.{lab}'); amb=True
                    if key==('table','3.4'): key=('table','3.5'); amb=True   # text says 'Tables 3.4a/b', only Table 3.5 exists
                    tid=(('fig' if kind=='figure' else 'tab')+key[1]) if key in figtab else None
                    if amb: lab=lab+' (read as '+key[1]+')'
                else: tid=None
                conf='high'
                if kind=='equation': tid='s1.3.1'      # (1.1) is defined in 1.3.1 on printed p.12
                if tid is None or (tid not in byid and not tid.startswith(('fig','tab'))):
                    unresolved.append((kind,lab,printed(idx),ctx)); continue
                if kind=='table' and ('.' not in lab or 'read as' in lab): conf='low'
                raw.append(dict(src=src['id'],tgt=tid,ref_kind=kind,label=lab,page=printed(idx),ctx=ctx,conf=conf))
# aggregate
agg=collections.OrderedDict()
dropped=0
for r in raw:
    if r['src']==r['tgt'] or r['tgt'] in ancestors(r['src']): dropped+=1; continue   # figure/table targets are leaf nodes, so same-section references are kept
    k=(r['src'],r['tgt'],r['ref_kind'])
    a=agg.setdefault(k,dict(source=r['src'],target=r['tgt'],type='xref-'+r['ref_kind'],kind='explicit',basis='stated',occurrences=[],confidence='high'))
    a['occurrences'].append(dict(page=r['page'],label=r['label'],text=r['ctx']))
    if r['conf']=='low': a['confidence']='low'
edges=[]
for i,(k,a) in enumerate(agg.items()):
    a['id']=f'x{i+1}'; a['source_pages']=sorted({o['page'] for o in a['occurrences']},key=lambda p:pdfidx(p))
    a['reason']='Explicit cross-reference: '+', '.join(sorted({f"{a['type'][5:]} {o['label']}" for o in a['occurrences']}))
    edges.append(a)
json.dump(dict(edges=edges,unresolved=unresolved,dropped_self_refs=dropped,raw_count=len(raw)),open('xrefs.json','w'),indent=1)
print('raw refs',len(raw),'edges',len(edges),'dropped intra',dropped,'unresolved',len(unresolved))
for u in unresolved: print('UNRESOLVED',u)
c=collections.Counter(e['type'] for e in edges); print(c)
