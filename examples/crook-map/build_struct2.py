import re,json,sys
from collections import defaultdict
import build_struct as B
L,page_at,pdf_at,final=B.L,B.page_at,B.pdf_at,B.final
figtab=json.load(open('figtab.json'))
ROMAN=['','i','ii','iii','iv','v','vi','vii','viii','ix','x','xi','xii','xiii','xiv','xv','xvi','xvii','xviii','xix','xx','xxi','xxii','xxiii','xxiv','xxv','xxvi','xxvii','xxviii','xxix','xxx']
def lab_to_pdf(lab):
    if lab in ROMAN: return ROMAN.index(lab)
    return int(lab)+30

nodes=[]  # dict list
def mk(id,title,num,level,parent,pos,numbered=True,**kw):
    d=dict(id=id,num=num,title=title,level=level,parent=parent,pos=pos,numbered=numbered); d.update(kw); nodes.append(d); return d
# front matter (pdf ranges, no body position)
FM=[('fm-title','Title page',1,2),('fm-dedication','Dedication',3,3),('fm-declaration','Declaration',5,5),('fm-summary','Summary',6,7),('fm-ack','Acknowledgements',9,9),
    ('fm-preface','Preface',10,10),('fm-toc','Table of contents',11,15),('fm-lof','List of figures',17,21),('fm-lot','List of tables',23,26),('fm-abbrev','Abbreviations',27,29)]
for id,t,a,b in FM:
    mk(id,t,None,0,None,None,numbered=False,type='front matter',pdf_start=a,pdf_end=b)
numnode={}
for e in final:
    num=e['num'];i=B.nid(num);lv=B.level(num);pn=B.parent(num)
    par=B.nid(pn) if pn else None
    d=mk(i,e['title'],num,lv,par,e['pos'],type=B.ntype(num,e['title']))
    numnode[num]=d
# unnumbered subheads
idxpos={e['num']:e['pos'] for e in final}
for pnum,names in B.SUBS.items():
    parent_node=numnode[pnum]
    a=parent_node['pos']
    pl=parent_node['level']
    for k,n in enumerate(names):
        found=None
        for q in range(a,min(a+1600,len(L))):
            if L[q].strip()==n: found=q;break
        assert found,n
        nm='%s/%s'%(pnum,re.sub(r'[^a-z0-9]+','-',n.lower()).strip('-'))
        # for the 7.3 children use sibling level of 7.3.1 and parent 7.3
        lv=pl+1 if pnum!='7.3' else 2
        par=B.nid(pnum)
        mk('u'+nm,n,None,lv,par,found,numbered=False,type=B.ntype('x.y.z',n) if False else parent_node['type'])
nodes_body=[n for n in nodes if n['pos'] is not None]
nodes_body.sort(key=lambda n:n['pos'])
# end positions
end_of_body=len(L)
for k,n in enumerate(nodes_body):
    e=end_of_body
    for m in nodes_body[k+1:]:
        if m['level']<=n['level']: e=m['pos'];break
    n['end']=e
# the chapter 8 / appendix C / refs end; refs ends at appendix A start (level 0) ok.
def words(a,b):
    w=0
    for l in L[a:b]:
        if l.startswith('====='): continue
        w+=len(re.findall(r"[A-Za-z][A-Za-z\-']+",l))
    return w
byid={n['id']:n for n in nodes}
for n in nodes:
    if n['pos'] is not None:
        # own words: from heading to next node of ANY level (excluding children)
        pass
for n in nodes_body:
    n['approx_words']=words(n['pos'],n['end'])
    n['pdf_start']=pdf_at[n['pos']]
    # last line before end that is non-blank
    q=n['end']-1
    while q>n['pos'] and (not L[q].strip() or L[q].startswith('=====')): q-=1
    n['pdf_end']=pdf_at[q]
# front matter words
for n in nodes:
    if n['pos'] is None:
        a=B.pdf_first_line[n['pdf_start']]; b=B.pdf_first_line.get(n['pdf_end']+1,len(L))
        n['approx_words']=words(a,b)
        n['pos']=None
def lab(p): return B.pm_label(p) if hasattr(B,'pm_label') else (ROMAN[p] if p<=30 else str(p-30))
for n in nodes:
    n['page_start']=lab(n['pdf_start']);n['page_end']=lab(n['pdf_end'])
    n['pages']='p. %s'%(n['page_start'] if n['page_start']==n['page_end'] else n['page_start']+'–'+n['page_end'])
# ---------------- deepest node containing a line
def node_at(i):
    best=None
    for n in nodes_body:
        if n['pos']<=i<n['end'] and (best is None or n['level']>=best['level'] and n['pos']>=best['pos']): best=n
    return best
def node_at_page_front(i):
    p=pdf_at[i]
    for n in nodes:
        if n['pos'] is None and n['pdf_start']<=p<=n['pdf_end']: return n
    return None
def node_for_line(i):
    if i<B.start_line: return node_at_page_front(i)
    return node_at(i)
# ---------------- figures / tables captions
cap_f={};cap_t={}
for i,l in enumerate(L):
    if i<B.start_line: continue
    s=l.strip()
    m=re.match(r'^Fig\. ([0-9A-C]+\.\d+)\b',s)
    if m: cap_f.setdefault(m.group(1),i)
    m=re.match(r'^Table ([0-9A-C]+\.\d+)\b',s)
    if m: cap_t.setdefault(m.group(1),i)
figs=[];tabs=[];fallback=[]
for kind,lst,cap,out in (('figure',figtab['figures'],cap_f,figs),('table',figtab['tables'],cap_t,tabs)):
    for f in lst:
        i=cap.get(f['id'])
        how='caption'
        if i is None:
            # fallback: first line of the page listed in LoF (+1 to skip marker)
            i=B.pdf_first_line[lab_to_pdf(str(f['page']))]+1;how='lof-page'
            fallback.append((kind,f['id']))
        n=node_at(i)
        out.append(dict(id=('fig:' if kind=='figure' else 'tab:')+f['id'],label=('Fig. ' if kind=='figure' else 'Table ')+f['id'],caption=f['title'],page=str(f['page']),node=n['id'],located=how,source_pages=[str(f['page'])],basis='stated'))
print('captions not found in body (assigned by LoF page):',fallback)
for n in nodes:
    n['figure_ids']=[f['id'] for f in figs if f['node']==n['id']]
    n['table_ids']=[t['id'] for t in tabs if t['node']==n['id']]
# totals including descendants
children=defaultdict(list)
for n in nodes:
    if n['parent']: children[n['parent']].append(n['id'])
def tot(nid,key):
    n=byid[nid]; s=len(n[key])
    for c in children[nid]: s+=tot(c,key)
    return s
for n in nodes:
    n['n_figures']=tot(n['id'],'figure_ids'); n['n_tables']=tot(n['id'],'table_ids')
json.dump(dict(nodes=[{k:v for k,v in n.items() if k not in('pos','end')} for n in nodes],figures=figs,tables=tabs),open('struct.json','w'),indent=1,ensure_ascii=False)
print(len(nodes),'nodes;',len(figs),'figures;',len(tabs),'tables')
import pickle;pickle.dump(dict(nodes=nodes,figs=figs,tabs=tabs),open('struct.pkl','wb'))
