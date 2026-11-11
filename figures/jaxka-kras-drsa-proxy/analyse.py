"""Derive noise-based burial proxy from saved intact-unit hmask outputs."""
from pathlib import Path
import csv,json,hashlib
r=Path(__file__).resolve().parent
s=r.parent/'jaxka-kras-noise-propensity'
source=json.loads((s/'provenance.json').read_text())
audit={};hashes={}
for n in ['g12d','wt','empty']:
 path=s/f'{n}.csv';hashes[n]=hashlib.sha256(path.read_bytes()).hexdigest()
 with path.open() as f:rows=list(csv.DictReader(f))
 out=[]
 for v in rows:
  e=float(v['exposure']);contact=float(v['score'])
  q={k:v[k] for k in ['chain','number','insertion']}
  q.update(score=e*contact,exposure=e,noise_contact=contact,seed_sd=e*float(v['seed_sd']),uniform_score=e*float(v['uniform_score']))
  assert 0<=q['score']<=e<=1
  out.append(q)
 with (r/f'{n}.csv').open('w') as f:
  w=csv.DictWriter(f,fieldnames=list(out[0]));w.writeheader();w.writerows(out)
 audit[n]={'residues':len(out),'range':[min(v['score'] for v in out),max(v['score'] for v in out)],'max_seed_sd':max(v['seed_sd'] for v in out),'peptide':[v for v in out if v['chain']=='C']}
(r/'provenance.json').write_text(json.dumps({'definition':'(1 - sigmoid(hmask burial_logit)) * mean_noise(sigmoid(hmask contact_logit))','interpretation':'Noise-based proxy for potential additional burial; not a measured RSA difference or calibrated delta-RSA prediction.','unit':'Entire pMHC graph retained, no external binding partner','source_provenance':source,'source_csv_sha256':hashes,'audit':audit},indent=2))
print(json.dumps(audit,indent=2))
