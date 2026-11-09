"""default-evals-v1 copy (2026-10-21, user: "just do the cheap evals for now"): scores the default all-residue checkpoint and the previous relational default; outputs under audits/default-evals-v1; benchmark-v1 inputs and earlier predictions are read, never written.
Phase 2 (2026-10-14): experimental pKa benchmark, PKAD-3 entries from the KaML splits with RCSB structures.
Entries without an RCSB structure (PDB_ID given as a mutant label, mostly SNase P00644 variants) are excluded for every method.
Methods: GQT seed-17 (base A, relations, packed contacts: backbone + residue types; side chains); PROPKA 3.5.1, pKAI,
pKAI+, PypKa, jax-Ka (jaxpropka mean-field PROPKA surrogate, 1,024 steps; added 2026-10-16) (pkabench Adapter; deposited chain and FASPR-repacked chain); KaML-CBtree acid split models on their own
test split (base split models unusable); KaML-GAT published per-split test predictions (de-normalised as in the authors'
notebook; 'all folds' mean, and the authors' fold filter which uses test labels); null = KaML model pKa.
Protocols: (1) per split, test entries of that split, mean +- SD of RMSE over 20 splits (paper protocol); (2) pooled
unique entries. GQT/pKAI/pKAI+ were trained on PypKa-derived labels (pKPDB) that may include these proteins'
structures, never their experimental pKa; KaML was trained on the other PKAD entries of each split."""
import os,csv,json,collections
from pathlib import Path
import numpy as np
root=Path(os.environ['PKABENCH_RUNTIME']);CODE=Path(os.environ['CODE']);A=root/'audits/benchmark-v1/pkad';D=CODE/'data'
UNITS={u for u in os.listdir(A/'units') if (A/'units'/u/'deposited.cif').exists()}
ALL=json.loads((A/'entries.json').read_text());E=[e for e in ALL if f"{e['pdb']}_{e['chain']}" in UNITS]  # entries with a prepared RCSB chain
ACID={'ASP','GLU','CYS','TYR'};BASE={'HIS','LYS'}
site=lambda e:(f"{e['pdb']}_{e['chain']}",e['chain'],int(e['resnum']),e['group'])
P=collections.defaultdict(dict)  # method -> site -> pKa (single prediction per site)
OUT=root/'audits/default-evals-v1/pkad'
for path in (A/'gqt-predictions.csv',OUT/'gqt-predictions.csv'):
    for r in csv.DictReader(open(path)):P[r['model']][(r['unit'],r['chain'],int(r['resnum']),r['group'])]=float(r['predicted_pka'])
NAMES={'propka':'PROPKA 3.5.1','jaxka':'jax-Ka','pkai':'pKAI','pkai_plus':'pKAI+','pypka':'PypKa'}
for r in csv.DictReader(open(D/'ext-pkad.csv')):
    if r['pka'] in ('','None') or r['status']!='ok':continue
    P[f"{NAMES[r['method']]} [{r['input']}]"][(r['unit'],r['chain'],int(r['resnum']),r['group'])]=float(r['pka'])
for e in E:P['Null (model pKa)'][site(e)]=e['model_pka']
SPLIT=collections.defaultdict(dict)  # method -> (split, site) -> pKa
for r in csv.DictReader(open(D/'cbtree-split-predictions.csv')):SPLIT['KaML-CBtree (acid split models)'][(int(r['split']),f"{r['pdb']}_{r['chain']}",r['chain'],int(r['resnum']),r['group'])]=float(r['cbtree'])
for r in csv.DictReader(open(D/'gat-predictions.csv')):
    k=(int(r['split']),f"{r['pdb']}_{r['chain']}",r['chain'],int(r['resnum']),r['group'])
    SPLIT['KaML-GAT (all folds)'][k]=float(r['gat_all_folds'])
    if r['gat_authors_ensemble']!='nan':SPLIT['KaML-GAT (authors ensemble)'][k]=float(r['gat_authors_ensemble'])
def stats(y,p):
    y,p=np.asarray(y),np.asarray(p);r={'n':int(len(y))}
    if len(y)<2:return r
    r.update(rmse=float(np.sqrt(np.mean((p-y)**2))),mae=float(np.mean(abs(p-y))),pcc=float(np.corrcoef(y,p)[0,1]) if np.std(p)>0 else None);return r
def classify(y,p):
    y,p=np.asarray(y),np.asarray(p);far=abs(y-7)>=1
    return float(np.mean((p[far]>7)==(y[far]>7))) if far.any() else None
methods=sorted(P,key=lambda n:(not n.startswith('GQT'),n))+sorted(SPLIT)
def pred(m,e,split=None):
    return SPLIT[m].get((split,*site(e))) if m in SPLIT else P[m].get(site(e))
# (1) split protocol
split_res={}
for m in methods:
    per={'all':[],'acid':[],'base':[]};cov=0;tot=0
    for i in range(20):
        test=[e for e in E if i in e['test_splits']];tot+=len(test)
        for grp,sel in (('all',lambda g:True),('acid',lambda g:g in ACID),('base',lambda g:g in BASE)):
            ys=[(e['expt_pka'],pred(m,e,i)) for e in test if sel(e['group']) and pred(m,e,i) is not None]
            if grp=='all':cov+=len(ys)
            if len(ys)>=5:per[grp].append(float(np.sqrt(np.mean([(p-y)**2 for y,p in ys]))))
    split_res[m]={g:{'mean':float(np.mean(v)),'sd':float(np.std(v)),'splits':len(v)} if v else None for g,v in per.items()};split_res[m]['coverage']=cov/tot if tot else 0
# (1b) per-residue offset calibration inside the split protocol: for split i, one offset per residue type = mean
# (prediction - experiment) over that split's TRAINING entries; applied to its test entries. Same data KaML trains on,
# at the coarsest level: separates systematic per-residue bias (e.g. PB lineage) from site-level information.
cal_res={}
for m in [x for x in methods if x not in SPLIT]:
    per={'all':[],'acid':[],'base':[]}
    for i in range(20):
        train=[e for e in E if i in e['train_splits'] and pred(m,e) is not None];off={}
        for g in ('ASP','GLU','HIS','CYS','TYR','LYS'):
            d=[pred(m,e)-e['expt_pka'] for e in train if e['group']==g];off[g]=float(np.mean(d)) if d else 0.0
        test=[e for e in E if i in e['test_splits'] and pred(m,e) is not None]
        for grp,sel in (('all',lambda g:True),('acid',lambda g:g in ACID),('base',lambda g:g in BASE)):
            ys=[(e['expt_pka'],pred(m,e)-off[e['group']]) for e in test if sel(e['group'])]
            if len(ys)>=5:per[grp].append(float(np.sqrt(np.mean([(q-y)**2 for y,q in ys]))))
    cal_res[m]={g:{'mean':float(np.mean(v)),'sd':float(np.std(v))} if v else None for g,v in per.items()}
# (2) pooled unique entries
pooled={}
for m in [x for x in methods if x not in SPLIT]:
    ys=[(e,P[m][site(e)]) for e in E if site(e) in P[m]];y=[e['expt_pka'] for e,_ in ys];p=[v for _,v in ys]
    r={'all':stats(y,p),'acid':stats([a for (e,_),a in zip(ys,y) if e['group'] in ACID],[b for (e,_),b in zip(ys,p) if e['group'] in ACID]),
       'base':stats([a for (e,_),a in zip(ys,y) if e['group'] in BASE],[b for (e,_),b in zip(ys,p) if e['group'] in BASE]),'pH7_acc':classify(y,p),
       'by_group':{g:stats([a for (e,_),a in zip(ys,y) if e['group']==g],[b for (e,_),b in zip(ys,p) if e['group']==g]) for g in ('ASP','GLU','HIS','CYS','TYR','LYS')},
       'by_shift':{f'[{lo},{hi})':stats([a for (e,_),a in zip(ys,y) if lo<=abs(e['expt_pka']-e['model_pka'])<hi],[b for (e,_),b in zip(ys,p) if lo<=abs(e['expt_pka']-e['model_pka'])<hi]) for lo,hi in ((0,1),(1,2),(2,99))}}
    pooled[m]=r
common=[e for e in E if all(site(e) in P[m] for m in P if not m.startswith('jax-Ka'))];cm={}  # jax-Ka kept out (phase-2 set unchanged)
for m in [x for x in P if not x.startswith('jax-Ka')]:
    y=[e['expt_pka'] for e in common];p=[P[m][site(e)] for e in common];cm[m]=stats(y,p)
res={'split_protocol_offset_calibrated':cal_res,'entries':len(E),'excluded_without_rcsb_structure':len(ALL)-len(E),'split_protocol':split_res,'pooled':pooled,'common_entries':len(common),'common':cm,'test_data_included':'experimental benchmark'}
out=OUT;(out/'benchmark.json').write_text(json.dumps(res,indent=1)+'\n')
f=lambda d,k='rmse':'-' if not d or d.get(k) is None else f"{d[k]:.2f}"
L=['# Experimental pKa benchmark (PKAD-3 via KaML splits, RCSB structures)','',__doc__.split('\n',1)[1].strip(),'',f'{len(E):,} entries with RCSB structures; {len(common):,} predicted by every single-prediction method.','',
   '## Paper protocol: RMSE over the 20 test splits (mean +- SD)','','| method | all | acid | base | coverage |','|---|---:|---:|---:|---:|']
for m in methods:
    s=split_res[m];g=lambda k:'-' if not s[k] else f"{s[k]['mean']:.2f} +- {s[k]['sd']:.2f}"
    L.append(f"| {m} | {g('all')} | {g('acid')} | {g('base')} | {s['coverage']:.2f} |")
L+=['','Paper (KaML-CBtree, 20 splits): acid 0.76, base 0.79; PROPKA3 acid 1.28, base 0.95.','','## Paper protocol after per-residue offset calibration (fitted on each split\'s training entries)','','| method | all | acid | base |','|---|---:|---:|---:|']
for m,c in cal_res.items():
    g=lambda k:'-' if not c[k] else f"{c[k]['mean']:.2f} +- {c[k]['sd']:.2f}";L.append(f"| {m} | {g('all')} | {g('acid')} | {g('base')} |")
L+=['','## Pooled unique entries','',
    '| method | n | RMSE | MAE | PCC | acid RMSE | base RMSE | pH 7 acc | RMSE |shift| 0-1 | 1-2 | >=2 |','|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|']
for m,r in pooled.items():
    a=r['all'];L.append(f"| {m} | {a['n']} | {f(a)} | {f(a,'mae')} | {f(a,'pcc')} | {f(r['acid'])} | {f(r['base'])} | {'-' if r['pH7_acc'] is None else format(r['pH7_acc'],'.3f')} | {f(r['by_shift']['[0,1)'])} | {f(r['by_shift']['[1,2)'])} | {f(r['by_shift']['[2,99)'])} |")
L+=['','n per |experimental shift| bin: '+', '.join(f"{k} {pooled['Null (model pKa)']['by_shift'][k]['n']}" for k in ('[0,1)','[1,2)','[2,99)')),'',
    '## Pooled RMSE by residue type','','| method | '+' | '.join(('ASP','GLU','HIS','CYS','TYR','LYS'))+' |','|---|'+'---:|'*6]
for m,r in pooled.items():L.append(f'| {m} | '+' | '.join(f(r['by_group'][g]) for g in ('ASP','GLU','HIS','CYS','TYR','LYS'))+' |')
L+=['','n per residue type: '+', '.join(f"{g} {pooled['Null (model pKa)']['by_group'][g]['n']}" for g in ('ASP','GLU','HIS','CYS','TYR','LYS')),'',f'## Common entries ({len(common):,})','','| method | RMSE | MAE | PCC |','|---|---:|---:|---:|']
for m,r in cm.items():L.append(f"| {m} | {f(r)} | {f(r,'mae')} | {f(r,'pcc')} |")
JK=[m for m in P if m.startswith('jax-Ka')]
if JK:
    L+=['','## jax-Ka coverage and agreement with PROPKA 3.5.1 (same input)','','| input | entries with jax-Ka | of PROPKA entries | MAE jax-Ka vs PROPKA | PCC | jax-Ka RMSE vs expt | PROPKA RMSE vs expt (same entries) |','|---|---:|---:|---:|---:|---:|---:|']
    agree={}
    for v in ('deposited','repacked'):
        a,b=P.get(f'jax-Ka [{v}]',{}),P.get(f'PROPKA 3.5.1 [{v}]',{})
        ks=[e for e in E if site(e) in a and site(e) in b];kb=[e for e in E if site(e) in b]
        if len(ks)<3:continue
        x=np.array([a[site(e)] for e in ks]);y=np.array([b[site(e)] for e in ks]);t=np.array([e['expt_pka'] for e in ks])
        agree[v]={'n':len(ks),'propka_n':len(kb),'mae':float(np.mean(abs(x-y))),'pcc':float(np.corrcoef(x,y)[0,1]),'jaxka_rmse':float(np.sqrt(np.mean((x-t)**2))),'propka_rmse':float(np.sqrt(np.mean((y-t)**2)))}
        g=agree[v];L.append(f"| {v} | {g['n']} | {g['propka_n']} | {g['mae']:.2f} | {g['pcc']:.2f} | {g['jaxka_rmse']:.2f} | {g['propka_rmse']:.2f} |")
    res['jaxka_vs_propka']=agree;(out/'benchmark.json').write_text(json.dumps(res,indent=1)+'\n')
(out/'report.md').write_text('\n'.join(L)+'\n');print('\n'.join(L),flush=True)
