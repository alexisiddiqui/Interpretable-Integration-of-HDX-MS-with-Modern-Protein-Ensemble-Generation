"""Read saved seed-17 PINDER scaling reports from Isambard; launches no jobs."""
from pathlib import Path
import subprocess, shlex, json, hashlib, datetime
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'.experiments/jaxka-pinder-2026-11-05'
REMOTE=r'''import pathlib,json,hashlib
root=pathlib.Path('/scratch/u6xq/hussain.u6xq/_runtime/jax-Ka/pkabench')
paths=[root/'audits/negatives-v1/sweep/residue/report.json']; missing=[]
for arm in ['w064','w128','e40-w064','e40-w128']:
 base=root/'audits/datascale-v1'/arm
 for name in ['residue/report.json','residue/report.md','masked2/report.json','masked2/report.md','train_resources.json']:
  p=base/name
  if p.is_file(): paths.append(p)
  else: missing.append(str(p))
 for p in (base/'abag').rglob('*.json'):
  if p.stat().st_size<3000000:paths.append(p)
 width=arm.split('-')[-1];prefix='drsa100e40-v1' if arm.startswith('e40') else 'drsa100-v1'
 run=root/'training/gqt-production-v2/runs'/f'{prefix}-asym50-{width}-s17'
 for name in ['protocol.json','selection.json','history.jsonl']:
  p=run/name
  if p.is_file():paths.append(p)
  else:missing.append(str(p))
files=[]
for p in paths:
 data=p.read_bytes();files.append({'path':str(p.relative_to(root)),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'content':data.decode()})
print(json.dumps({'remote_root':str(root),'files':files,'missing':missing}))'''
def main():
 r=subprocess.run(['ssh','-o','BatchMode=yes','-o','ConnectTimeout=15','hussain.u6xq@u6xq.aip2.isambard','python3 -c '+shlex.quote(REMOTE)],capture_output=True,text=True)
 if r.returncode:raise RuntimeError(r.stderr)
 d=json.loads(r.stdout)
 for row in d['files']:
  content=row.pop('content').encode();assert hashlib.sha256(content).hexdigest()==row['sha256']
  p=OUT/row['path'];p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(content)
 d.update(observed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),host='hussain.u6xq@u6xq.aip2.isambard',remote_checksums_verified=True)
 (OUT/'receipt.json').write_text(json.dumps(d,indent=2)+'\n')
 print('Retrieved',len(d['files']),'files; missing:',d['missing'])
if __name__=='__main__':main()
