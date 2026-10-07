"""Stage 1a: deterministic structure extraction (TOC, positions, words, figures/tables, explicit cross-refs)."""
import re,json
L=open('tagged.txt').read().split('\n')
page_at=[];pdf_at=[];cur='?';curpdf=0
for l in L:
    m=re.match(r'=====\[PDF (\d+) \| p\. (\w+)\]',l)
    if m: cur=m.group(2);curpdf=int(m.group(1))
    page_at.append(cur);pdf_at.append(curpdf)
pdf_first_line={}
for i,p in enumerate(pdf_at): pdf_first_line.setdefault(p,i)

# ------------------------------------------------------------------ TOC
toc=[e for e in json.load(open('toc.json')) if e['num'] is not None]
bynum={e['num']:e for e in toc}
def patch(num,title=None,page=None):
    e=bynum[num]
    if title:e['title']=title
    if page:e['page']=page
patch('4.4.3','Resolution of subcellular proteomes constitutes massive knowledge expansion',117)
patch('7','Inferring differential subcellular localisation in comparative spatial proteomics using BANDLE',187)
patch('Appendix A','Appendix to chapter 2',269);patch('Appendix B','Appendix to chapter 6',295);patch('Appendix C','Appendix to chapter 7',321)
patch('B.3','Appendix 3: Tensor decompositions for derivatives of the marginal likelihood',297)
extra=[('4.4.3','4.5','Discussion and limitations',121),('7','7.1','Motivation',187),('Appendix A','A.1','Appendix 1: Derivation of EM algorithm for TAGM model',269),
       ('Appendix B','B.1','Appendix 1: Matrix algorithms',295),('B.3','B.4','Appendix 4: Further sensitivity analysis',302),('Appendix C','C.1','Appendix 1: Additional simulations',321)]
order=[]
for e in toc:
    if e['num']=='Appendix A': order.append({'num':'References','title':'References','page':235})
    order.append(e)
    for after,n,t,p in extra:
        if e['num']==after and after in ('4.4.3','7','Appendix A','Appendix B','B.3','Appendix C'):
            if n=='4.5' or n=='B.4' or True: pass
    # inserted below to retain order
final=[]
for e in order:
    final.append(e)
    for after,n,t,p in extra:
        if e['num']==after: final.append({'num':n,'title':t,'page':p})
# B.4: toc had B.3 merged with B.4 -> 'B.4' absent in toc so inserted after B.3 (ok); but A.1 etc follow their appendix header (ok)
seen=set();uniq=[]
for e in final:
    if e['num'] in seen: continue
    seen.add(e['num']);uniq.append(e)
final=uniq

def nid(num):
    if num=='References':return 'refs'
    if num.startswith('Appendix '):return 'app'+num[-1]
    if re.match(r'^\d+$',num):return 'ch'+num
    return 's'+num
def level(num):
    if num in('References',) or num.startswith('Appendix ') or re.match(r'^\d+$',num):return 0
    return num.count('.')+ (1 if re.match(r'^[A-C]\.',num) else 0)  # 2.3->1, 2.3.1->2, A.1->1, C.15.1->2
def parent(num):
    if num=='References' or num.startswith('Appendix ') or re.match(r'^\d+$',num):return None
    if re.match(r'^[A-C]\.\d+$',num):return 'Appendix '+num[0]
    if re.match(r'^[A-C]\.\d+\.\d+$',num):return num.rsplit('.',1)[0]
    p=num.rsplit('.',1)[0]
    return p if '.' in p else p
def ntype(num,title):
    t=title.lower()
    ch=re.match(r'^(\d+)',num)
    if num[0] in 'AB C'.replace(' ','') and not num[0].isdigit(): return 'appendix'
    if num=='References': return 'back matter'
    if re.match(r'^\d+$',num): return None  # chapter type set curated
    if 'motivation' in t or 'abstract' in t or 'introduction' in t or 'literature' in t or 'previous methods' in t or t.startswith('the post') or t in('proteomics','mass spectrometry') or 'workflows' in t or 'spatial proteomics'==t or 'statistical inference'==t or 'thesis outline' in t or 'fluorescent' in t or 'proximity' in t or 'fractionation coupled' in t or 'functional data analysis' in t or 'model development' in t:
        return 'background'
    if 'discussion' in t or 'limitations' in t or 'main findings' in t or 'future work' in t or re.match(r'^8\.2\.',num):return 'discussion'
    if 'result' in t or 'case study' in t or 'comparison' in t or 'mapping the spatial' in t or 'hyperlopit provides' in t or 'resolution of subcellular' in t or 'simulations' in t or 'applications to' in t or 'rewiring' in t or 'validating experimental' in t or 'uncovering' in t or 'refining' in t or 'improved annotation' in t or 'workflow' in t.split() or 'assessing predictive' in t:
        return 'result'
    return 'method'

# ------------------------------------------------------------------ positions
start_line=653  # first line of PDF 31
pos={}
def find_heading(num,title,frm,to=None):
    to=to or len(L)
    if num=='References': pat=re.compile(r'^References\s*$')
    elif re.match(r'^\d+$',num): pat=re.compile(r'^Chapter %s\s*$'%num)
    elif num.startswith('Appendix '): pat=re.compile(r'^Appendix %s\s*$'%num[-1])
    else:
        pat=re.compile(r'^\s*%s\s+%s'%(re.escape(num),re.escape(title[:18].replace('  ',' '))))
    for i in range(frm,to):
        s=L[i].strip()
        top=num=='References' or re.match(r'^\d+$',num) or num.startswith('Appendix ')
        if pat.match(s) and (top or not re.search(r'\s\d+$',s)) and not (re.match(r'^\d',s) and re.search(r'\.\s*\.',s)):
            return i
    return None
prev=start_line
for e in final:
    p=find_heading(e['num'],e['title'],prev)
    if p is None and not re.match(r'^[A-C]',e['num']): p=find_heading(e['num'],e['title'],prev)
    e['pos']=p
    if p is not None: prev=p
missing=[e['num'] for e in final if e['pos'] is None]
print('headings not located in text:',missing)

mism=[(e['num'],e['page'],page_at[e['pos']]) for e in final if str(e['page'])!=page_at[e['pos']]]
print('TOC page vs body page mismatches:',mism)

SUBS={ '2.3.1':['Kernel Machines','K-Nearest Neighbours','Mixture models for clustering','Robust mixture models','Bayesian mixture models'],
 '2.3.4':['Maximum a posteriori prediction','Uncertainty in the posterior localisation probabilities'],
 '3.6.1':['Applying the Gelman diagnostic','Applying the Geweke diagnostic'],
 '3.6.4':['Visualising global uncertainty','Uncertainty in mean of organelle localisation','Spatial variation of localisation probabilities'],
 '5.3.1':['Frequentist approaches','Bayesian approaches','Bayesian non-parametric approaches'],
 '6.3.1':['Gaussian processes','Prediction with Gaussian processes','Covariance functions'],
 '7.3.1':['The Movement-Reproducibility method','Integrative mixture models'],
 '7.3':['A model for differential localisation','Likelihood Model','Penalised Complexity Priors','Modelling outliers and hyperparameter inference','Calibration of Dirichlet prior','Differential localisation probability'],
}
if __name__=='__main__':
    idx={e['num']:i for i,e in enumerate(final)}
    for parent_num,names in SUBS.items():
        i=idx[parent_num]; a=final[i]['pos']
        # end = next final entry whose level<=this level (or +big)
        for n in names:
            found=None
            for k in range(a,min(a+1600,len(L))):
                if L[k].strip()==n: found=k;break
            print(parent_num,'|',n,'|',page_at[found] if found else None, found)
