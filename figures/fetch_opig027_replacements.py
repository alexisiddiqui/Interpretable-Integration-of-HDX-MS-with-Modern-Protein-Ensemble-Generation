"""Read only the 376 selected matched records from the existing Modal volume. No jobs are launched."""
import modal,json,hashlib,concurrent.futures
from pathlib import Path
root=Path(__file__).resolve().parents[1]
stage=root/'.experiments/opig-adaptyv-027'
rows=json.loads((stage/'inputs/fold-check-foldcheck-2026-10-28.json').read_text())['rows']
rows=[r for r in rows if r['tier']=='matched' and r['arm']!='native']
out=stage/'replacement-records';out.mkdir(exist_ok=True)
v=modal.Volume.from_name('opig-design-runs')
def fetch(r):
 name=f"{r['backbone']}__{r['arm']}__lam{r['lam']:g}__t0.1__seed{r['seed']}.json"
 path=f"027-extremophile-vs-pka-surface/{r['tag']}/designs/{name}"
 dest=out/name
 raw=dest.read_bytes() if dest.exists() else b''.join(v.read_file(path))
 d=json.loads(raw)
 assert d['sequence'] and d['surface_idx']
 dest.write_bytes(raw)
 return {'path':path,'local':str(dest.relative_to(stage)),'sha256':hashlib.sha256(raw).hexdigest()}
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
 receipts=list(pool.map(fetch,rows))
(stage/'replacement-records-manifest.json').write_text(json.dumps({'volume':'opig-design-runs','files':receipts},indent=2)+'\n')
print(f'Retrieved and verified {len(receipts)} matched design records')
