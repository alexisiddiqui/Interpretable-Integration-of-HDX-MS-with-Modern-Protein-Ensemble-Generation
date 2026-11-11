import csv, gzip, hashlib, json, math, os, sys, tarfile
from pathlib import Path
ROOT = Path('/scratch/bulk/hussain/poisk-protenix-control-20261110')
SOURCE = Path('/scratch/bulk/hussain/opig-adaptyv-2026-writeup/experiments/028-poisk-free-monomer/results')
RUNTIME = Path('/scratch/bulk/hussain/_runtime/opig-adaptyv-2026/force-refold/protenix')
ARCHIVE = Path('/scratch/bulk/hussain/_archive/modal-2026-11-07/opig-eval-runs/_archive/bench/bench__028-poisk-free-monomer-pilots.tar')
MODEL = 'protenix_base_20250630_v1.0.0'
def prepare():
    from Bio.Align import PairwiseAligner
    for sub in ('msa', 'inputs', 'logs', 'out'):
        (ROOT/sub).mkdir(parents=True, exist_ok=True)
    baseline = json.loads((SOURCE/'template_pilot_protenix_msa.json').read_text())
    names = set(baseline['protenix_msa']['confidence'])
    with gzip.open(SOURCE/'records.csv.gz', 'rt') as f:
        recs = [r for r in csv.DictReader(f) if r['record'] in names]
    assert len(recs) == 50
    groups = {}
    for r in recs:
        groups.setdefault(r['group'], []).append(r)
    assert len(groups) == 25 and all(len(v)==2 for v in groups.values())
    needed = {hashlib.sha1(r[c].encode()).hexdigest(): r[c] for r in recs for c in ('antigen','vh','vl')}
    with tarfile.open(ARCHIVE) as t:
        for m in t:
            if m.isfile() and '/mol1-pilot/msa/' in m.name and m.name.endswith('.a3m'):
                dest = ROOT/'msa'/Path(m.name).name
                if dest.stem in needed:
                    content = t.extractfile(m).read()
                    dest.write_bytes(content)
    for h, seq in needed.items():
        lines = (ROOT/'msa'/(h+'.a3m')).read_text().splitlines()
        query = []
        for line in lines[1:]:
            if line.startswith('>'): break
            query.append(line.strip())
        assert ''.join(query).replace('-','') == seq, h
    aligner = PairwiseAligner(mode='global', match_score=1, mismatch_score=0, open_gap_score=-1, extend_gap_score=-0.1)
    donors = {}
    for group, pair in sorted(groups.items()):
        q = pair[0]['antigen']
        assert pair[1]['antigen'] == q
        candidates = []
        for other, values in sorted(groups.items()):
            s = values[0]['antigen']
            if s == q: continue
            aln = aligner.align(q,s)[0]
            identity = aln.counts().identities/min(len(q),len(s))
            if identity < 0.30:
                candidates.append((abs(math.log(len(q)/len(s))), other, identity))
        assert candidates, group
        distance, other, identity = min(candidates)
        donors[group] = dict(donor_group=other, identity_over_shorter=identity, original_length=len(q), donor_length=len(groups[other][0]['antigen']))
    jobs = []
    for r in sorted(recs, key=lambda r:r['record']):
        for arm in ('correct','wrong'):
            antigen = r['antigen'] if arm=='correct' else groups[donors[r['group']]['donor_group']][0]['antigen']
            name = arm+'_'+r['record']
            chains = [{'proteinChain':{'sequence':seq,'count':1,'unpairedMsaPath':str(ROOT/'msa'/(hashlib.sha1(seq.encode()).hexdigest()+'.a3m'))}} for seq in (antigen,r['vh'],r['vl'])]
            (ROOT/'inputs'/(name+'.json')).write_text(json.dumps([{'name':name,'sequences':chains}]))
            jobs.append(dict(name=name,arm=arm,record=r['record'],group=r['group'],binder=r['binder']=='True'))
    (ROOT/'jobs.json').write_text(json.dumps(jobs,indent=2))
    (ROOT/'donors.json').write_text(json.dumps(donors,indent=2))
    (ROOT/'baseline.json').write_text(json.dumps(baseline))
    hashes = {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((ROOT/'msa').glob('*.a3m'))}
    (ROOT/'provenance.json').write_text(json.dumps(dict(source=str(SOURCE),archive=str(ARCHIVE),model=MODEL,seed=101,n_cycle=10,n_step=200,n_sample=5,scored_sample=0,msa_sha256=hashes),indent=2))
    print('PREPARED',len(jobs),'jobs;',len(needed),'validated MSAs',flush=True)
    print(json.dumps(donors,indent=2),flush=True)
def run():
    os.environ['PROTENIX_ROOT_DIR'] = str(RUNTIME/'data')
    os.environ['LAYERNORM_TYPE'] = 'torch'
    import importlib.metadata
    assert importlib.metadata.version('protenix') == '2.0.0'
    import torch
    assert torch.cuda.is_available()
    print('GPU',torch.cuda.get_device_name(),flush=True)
    import shutil
    shard = int(os.environ['SLURM_ARRAY_TASK_ID'])
    jobs = json.loads((ROOT/'jobs.json').read_text())
    group = sorted({j['group'] for j in jobs})[shard]
    selected = [j for j in jobs if j['group']==group]
    assert len(selected)==4
    inputs = ROOT/'shards'/str(shard)
    inputs.mkdir(parents=True,exist_ok=True)
    for j in selected: shutil.copyfile(ROOT/'inputs'/(j['name']+'.json'),inputs/(j['name']+'.json'))
    from runner.batch_inference import inference_jsons
    inference_jsons(str(inputs),out_dir=str(ROOT/'out'/str(shard)),use_msa=True,use_template=False,seeds=[101],n_cycle=10,n_step=200,n_sample=5,dtype='bf16',model_name=MODEL,need_atom_confidence=True)
    score(require_complete=True,shard=shard)
def score(require_complete=False,shard=None):
    jobs = json.loads((ROOT/'jobs.json').read_text())
    all_groups=sorted({j['group'] for j in jobs})
    if shard is not None:
        group=sorted({j['group'] for j in jobs})[shard]
        jobs=[j for j in jobs if j['group']==group]
    rows=[]
    for job in jobs:
        files=list((ROOT/'out'/str(all_groups.index(job['group']))/job['name']).rglob('*summary_confidence*sample_0*.json'))
        if not files: continue
        assert len(files)==1, files
        d=json.loads(files[0].read_text()); cp=d['chain_pair_iptm']
        iface=sum(cp[i][j] for i,j in ((0,1),(1,0),(0,2),(2,0)))/4
        rows.append(job|dict(iptm=d['iptm'],iface=iface))
    (ROOT/('scores.json' if shard is None else 'scores-shard-'+str(shard)+'.json')).write_text(json.dumps(rows,indent=2))
    print('COMPLETED',len(rows),'/',len(jobs),flush=True)
    if require_complete: assert len(rows)==len(jobs), 'Missing predictions'
    for arm in ('correct','wrong'):
        pairs={}
        for r in rows:
            if r['arm']==arm: pairs.setdefault(r['group'],{})[r['binder']]=r
        pairs=[p for p in pairs.values() if len(p)==2]
        if pairs:
            print(arm,len(pairs),{metric:sum((p[True][metric]>p[False][metric])+0.5*(p[True][metric]==p[False][metric]) for p in pairs)/len(pairs) for metric in ('iptm','iface')},flush=True)
if __name__=='__main__':
    {'prepare':prepare,'run':run,'score':score}[sys.argv[1]]()
