"""Stage 1a: build the structural skeleton (nodes, pages, words, figures, tables) from the PDF text."""
import re, json
exec(open('toc_parse.py').read().split("# TOC lives")[0])   # reuse S, pages, norm
ROMAN=['','i','ii','iii','iv','v','vi','vii','viii','ix','x','xi','xii','xiii','xiv','xv','xvi','xvii','xviii','xix','xx']
def printed(idx):  # pdf index -> printed label
    return str(idx-22) if idx>=23 else (ROMAN[idx-2] if idx>=3 else 'cover')
def pdfidx(p):     # printed label -> pdf index
    return ROMAN.index(p)+2 if p in ROMAN else int(p)+22

# ---- TOC (parsed by toc_parse.py; three merged lines and one hyphenated title patched by hand) ----
raw=[l for l in """
1|1|Introduction|1
1.1|1|Background and motivation|1
1.2|1|Drug discovery|6
1.2.1|1|Small molecule drugs|6
1.2.2|1|The drug discovery pipeline|7
1.2.2.1|1|Target identification, validation, and structural characterisation|7
~|1|Cryo-EM|8
1.2.2.2|1|Hit identification|8
1.2.2.3|1|Hit-to-lead and lead optimisation|10
1.3|1|Machine learning|11
1.3.1|1|Supervised learning|12
1.3.2|1|Neural networks and deep learning|13
1.3.3|1|Convolutional neural networks|14
1.3.4|1|Graph neural networks|15
1.3.5|1|Diffusion models|16
1.4|1|Machine learning in early-stage drug discovery|17
1.4.1|1|Target structure resolution|18
1.4.1.1|1|In silico structure prediction|18
~|1|AlphaFold2|19
~|1|AlphaFold3|19
~|1|Open-source models and extensions|20
1.4.1.2|1|Cryo-EM model building|21
~|1|Direct map interpretation methods|22
~|1|AlphaFold-based methods|23
1.4.2|1|Virtual screening|24
1.4.3|1|Generative design|26
1.4.3.1|1|Unconditional generation|27
1.4.3.2|1|Conditional de novo generation|27
1.4.4|1|Fragment-based design|29
1.5|1|Thesis outline|30
2|2|Fragment elaboration with attribution-informed constraints|33
2.1|2|Preface|34
2.2|2|Contributions|35
2.3|2|Introduction|35
2.4|2|Methods|37
2.4.1|2|Model|37
2.4.2|2|Datasets|38
2.4.2.1|2|The Redocked set|40
2.4.2.2|2|PDBBind refined: gninaSetPose set|40
2.4.2.3|2|PDBBind General and Core sets|41
2.4.3|2|Training dataset filtering|41
2.4.4|2|Attribution|42
2.4.5|2|Fragment elaboration|45
2.4.5.1|2|Hotspot Extraction|45
2.4.5.2|2|Protein targets|45
2.4.5.3|2|Obtaining fragments|46
2.4.5.4|2|STRIFE: A generative model for elaboration|46
2.4.5.5|2|Assessing generated molecules|48
2.5|2|Results|48
2.5.1|2|Training and testing PointVS|48
2.5.1.1|2|Bias in the CASF16 test set|48
2.5.1.2|2|Performance as a scoring function|49
2.5.2|2|Attribution: identifying important interactions|52
2.5.2.1|2|Human Tankyrase-2 inhibitors|53
2.5.2.2|2|Large-scale attribution tests|56
2.5.3|2|Hotspot identification using PointVS|57
2.5.3.1|2|Impact of fragment screen similarity|58
2.5.3.2|2|Dependency on fragment screen size|60
2.5.4|2|Fragment elaboration|60
2.6|2|Conclusions|62
3|3|Improving Structural Plausibility in 3D Molecule Generation via Property-Conditioned Training with Distorted Molecules|67
3.1|3|Preface|68
3.2|3|Introduction|68
3.3|3|Methods|70
3.3.1|3|Generation of 3D molecules|70
3.3.2|3|Conditioning on conformer quality|72
3.3.3|3|Assessment metrics|73
3.3.4|3|Datasets|74
3.3.4.1|3|QM9|75
3.3.4.2|3|GEOM|75
3.3.4.3|3|ZINC|76
3.4|3|Results and discussion|76
3.4.1|3|Ablation tests|76
3.4.2|3|Conditioning on distortion factor|78
3.4.3|3|Conditioning on internal energy|80
3.4.4|3|Testing the conditioning method on additional models|82
3.5|3|Conclusions|83
4|4|Molecule diffusion with fragment blocks|87
4.1|4|Preface|87
4.2|4|Introduction|88
4.3|4|Methods|90
4.3.1|4|Model|90
4.3.1.1|4|Atom-based setup|90
4.3.1.2|4|Initial model adaptations|91
4.3.2|4|Data|92
4.3.2.1|4|Training datasets|92
4.3.2.2|4|Decomposition|92
~|4|Regular BRICS decomposition|92
~|4|Decomposition with standardised fragments|93
4.3.2.3|4|Rotational information|95
4.3.3|4|Assessment metrics|97
4.4|4|Results|97
4.4.1|4|Centroid-only method|97
4.4.2|4|Plane alignment method|98
4.4.3|4|Addition of rotational information|99
4.5|4|Related Work|99
4.6|4|Conclusions|101
5|5|Cryo-EM model building with AlphaFold|103
5.1|5|Preface|103
5.2|5|Introduction|104
5.3|5|Methods|106
5.3.1|5|Calculating and applying gradient-based optimisation|107
5.3.1.1|5|Alignment|107
5.3.1.2|5|Simulating a map from the prediction|108
5.3.1.3|5|Overlap and gradient calculation|108
5.3.1.4|5|Updating the prediction|108
5.3.1.5|5|Update scheduling|109
~|5|Block Scheduling|109
~|5|Global Scheduling|109
~|5|Block and Global Scheduling|109
5.3.2|5|MSA subsampling|110
5.3.3|5|Datasets and evaluation|110
5.4|5|Results|111
5.4.1|5|OpenFold conditioning|111
5.4.1.1|5|Direct conditioning with a constant scaling factor|111
5.4.1.2|5|Introducing gradient scaling schedules|112
5.4.1.3|5|Implementing iterative updates|115
5.4.2|5|Boltz-2 conditioning|116
5.4.2.1|5|Gradient-based optimisation alone|117
5.4.2.2|5|Adding MSA subsampling|119
~|5|Only MSA subsampling|119
~|5|Combining with gradient-based optimisation|120
5.5|5|Conclusions|121
6|6|Conclusions and outlook|123
6.1|6|Interpretability in virtual screening|123
6.2|6|Plausibility in diffusion-based generative design|124
6.3|6|AlphaFold for cryo-EM model building|125
6.4|6|Concluding remarks|126
A|A|Appendix: chapter 2|129
A.1|A|Equivariance and Invariance - written by Jack Scantlebury|129
A.2|A|Hotspots API: calculation and processing of hotspots|130
A.3|A|Structure IDs|133
A.4|A|FGFR1 Case Study|133
B|B|Appendix: chapter 3|137
B.1|B|Ablation test: sampling D = Dmax|137
B.2|B|Full PoseBusters outputs|137
B.3|B|Other metrics|139
""".strip().split('\n')]

def build_nodes():
    nodes=[]; last={}   # depth -> id
    for l in raw:
        num,chap,title,pg=l.split('|')
        if num=='~':
            parent=nodes[-1]['id'] if False else None
            # run-in headings hang off the nearest preceding numbered node
            prev=[n for n in nodes if n['number']][-1]
            nid=f"{prev['id']}~{re.sub(r'[^a-z0-9]+','-',title.lower()).strip('-')}"
            n=dict(id=nid,number=None,title=title,start=pg,parent=prev['id'],kind='run-in')
        else:
            depth=num.count('.')
            if re.fullmatch(r'\d+',num): nid=f'ch{num}'; parent=None
            elif re.fullmatch(r'[A-Z]',num): nid=f'app{num}'; parent='app'
            else: nid=f's{num}'; parent='app'+num.split('.')[0] if num[0].isalpha() else (f'ch{num.split(".")[0]}' if depth==1 else 's'+'.'.join(num.split('.')[:-1]))
            n=dict(id=nid,number=num,title=title,start=pg,parent=parent,kind='chapter' if depth==0 and not num.isalpha() else ('appendix' if num.isalpha() and depth==0 else 'section'))
        nodes.append(n)
    return nodes
if __name__=='__main__':
    ns=build_nodes(); print(len(ns)); print(ns[:3], ns[-3:])

# ---------------- positions, words, figures/tables ----------------
def squash(s): return re.sub(r'[^a-z0-9.]','',s.lower())
def body_lines(idx):
    """lines of one PDF page, with running header / page number / contents-leader lines removed"""
    out=[]
    for k,l in enumerate(pages[idx-1].split('\n')):
        t=norm(l)
        if not t: continue
        if re.search(r'(\. ){3,}',t): continue                       # dotted contents leaders
        if re.fullmatch(r'\d+|[ivx]+',t): continue                   # bare page number
        out.append((k,t))
    return out
def is_header(t):  # running header: "<page> <n.m.> Title" or "<n.>. Title <page>"
    return bool(re.match(r'^\d+ \d+\.(\d+\.)* ?[A-Z]',t) or re.match(r'^\d+\. .+ \d+$',t) or re.match(r'^[A-Z]\. .+ \d+$',t) or re.match(r'^\d+ [A-Z]\.\d+\.',t) or re.match(r'^\d+ (References|List of|Appendices?)',t) or re.match(r'^(References|List of Figures|Contents) \d+$',t) or re.match(r'^\d+ Contents$',t))

def locate(nodes):
    for n in nodes:
        idx=pdfidx(n['start']); n['pdf_start']=idx
        want=squash((n['number'] or '')+n['title'])[:34] if n['number'] else squash(n['title'])[:30]
        n['heading_found']=False; n['pos']=None
        for k,t in body_lines(idx):
            if is_header(t): continue
            s=squash(t)
            if n['kind'] in('chapter','appendix'):
                # chapter opener: title appears on first lines of the page
                if squash(n['title'])[:20] in s or (n['kind']=='appendix' and squash(n['title'])[:14] in s):
                    n['pos']=(idx,k); n['heading_found']=True; break
            elif s.startswith(want[:len(want)]) or s.startswith(want[:22]):
                n['pos']=(idx,k); n['heading_found']=True; break
        if n['pos'] is None: n['pos']=(idx,0)
    return nodes

def words_between(a,b):
    """words from position a (idx,line) up to (not incl.) position b"""
    tot=0
    for idx in range(a[0],b[0]+1):
        for k,t in body_lines(idx):
            if is_header(t): continue
            if (idx,k)<a or (idx,k)>=b: continue
            tot+=len(t.split())
    return tot

CAP=re.compile(r'^(Figure|Table) ([A-Z]?\d*\.?\d+[a-z]?):')
def captions():
    caps=[]
    for idx in range(23,163):
        for k,t in body_lines(idx):
            m=CAP.match(t)
            if m: caps.append(dict(kind=m.group(1).lower(),label=m.group(2),pdf=idx,line=k,printed=printed(idx)))
    return caps
def first_mention(kind,label,chapter_range):
    pat=re.compile(r'\b(?:Fig(?:ure)?s?\.?|Tables?)\s*'+re.escape(label)+r'(?![\d])') if True else None
    pat=re.compile((r'\bFig(?:ure)?s?\.?\s*' if kind=='figure' else r'\bTables?\s*')+re.escape(label)+r'(?!\d)')
    for idx in range(chapter_range[0],chapter_range[1]+1):
        for k,t in body_lines(idx):
            if CAP.match(t): continue
            if re.match(r'^(Figure|Table) \S+:',t): continue
            if pat.search(t): return (idx,k)
    return None

def node_at(nodes,pos):
    """deepest node whose own span contains pos"""
    srt=sorted([n for n in nodes if n['pos']],key=lambda n:n['pos'])
    cur=None
    for n in srt:
        if n['pos']<=pos: cur=n
        else: break
    return cur

def finish():
    nodes=locate(build_nodes())
    byid={n['id']:n for n in nodes}
    srt=sorted(nodes,key=lambda n:n['pos'])
    END=(163,0)   # references start
    for i,n in enumerate(srt):
        nxt=srt[i+1]['pos'] if i+1<len(srt) else END
        n['own_words']=words_between(n['pos'],nxt)
        n['own_end']=nxt
    kids={n['id']:[] for n in nodes}
    for n in nodes:
        if n['parent'] in kids: kids[n['parent']].append(n['id'])
    def total(nid): return byid[nid]['own_words']+sum(total(c) for c in kids[nid])
    for n in nodes: n['approx_words']=total(n['id'])
    # end pages (printed): chapters/appendix chapters use fixed ends read off the PDF (blank verso pages excluded)
    CHEND={'ch1':'31','ch2':'65','ch3':'85','ch4':'102','ch5':'122','ch6':'126','appA':'136','appB':'140'}
    for n in nodes:
        if n['id'] in CHEND: n['end']=CHEND[n['id']]
    # sections: end = page of next node start (inclusive, since sections share pages) unless last in chapter
    def end_page(n):
        if 'end' in n: return n['end']
        kid_ends=[end_page(byid[c]) for c in kids[n['id']]]
        i=srt.index(n); nxt=srt[i+1] if i+1<len(srt) else None
        # this node ends on the page where the next node (in doc order) starts, unless that page is a new chapter
        e=printed(nxt['pos'][0]) if nxt and nxt['kind'] not in('chapter','appendix') else None
        if e is None: e=byid[n['parent']]['end'] if n['parent'] in byid and 'end' in byid[n['parent']] else n['start']
        return e
    for n in srt:
        n['end']=end_page(n) if 'end' not in n else n['end']
        if pdfidx(n['end'])<pdfidx(n['start']): n['end']=n['start']
    # figures & tables
    caps=captions(); chap_rng={'ch1':(23,54),'ch2':(55,88),'ch3':(89,108),'ch4':(109,124),'ch5':(125,144),'ch6':(145,148),'appA':(151,158),'appB':(159,162)}
    for n in nodes: n['figures']=[]; n['tables']=[]
    unplaced=[]
    for c in caps:
        ch=[k for k,(a,b) in chap_rng.items() if a<=c['pdf']<=b][0]
        # figure 1.x etc. in chapter 1: chapter number == label prefix
        mp=first_mention(c['kind'],c['label'],chap_rng[ch]) if True else None
        pos=mp if mp and chap_rng[ch][0]<=mp[0]<=chap_rng[ch][1] else (c['pdf'],c['line'])
        home=node_at(nodes,pos)
        c['home']=home['id']; c['home_basis']='first in-text mention' if mp and pos==mp else 'caption location'
        (home['figures'] if c['kind']=='figure' else home['tables']).append(dict(label=c['label'],page=c['printed'],basis=c['home_basis']))
    # roll up counts
    def roll(nid,key):
        return len(byid[nid][key])+sum(roll(c,key) for c in kids[nid])
    for n in nodes:
        n['n_figures']=roll(n['id'],'figures'); n['n_tables']=roll(n['id'],'tables')
    return nodes,kids,caps

if __name__=='__main__':
    nodes,kids,caps=finish()
    miss=[n['id'] for n in nodes if not n['heading_found']]
    print('headings not found on stated page:',miss)
    for n in nodes:
        if n['kind'] in('chapter','appendix'):
            print(n['id'],n['start'],n['end'],n['approx_words'],'figs',n['n_figures'],'tabs',n['n_tables'])
    print('captions',len(caps),'figures',sum(c['kind']=='figure' for c in caps),'tables',sum(c['kind']=='table' for c in caps))
    print(sorted((c['kind'][0]+c['label'],c['printed'],c['home']) for c in caps))
