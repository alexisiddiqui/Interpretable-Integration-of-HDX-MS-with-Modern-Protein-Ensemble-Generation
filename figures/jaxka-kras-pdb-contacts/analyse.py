from pathlib import Path
import csv,json,hashlib
import numpy as np
r=Path(__file__).resolve().parent

def read(p):
 residues={}
 for l in p.read_text().splitlines():
  if not l.startswith('ATOM') or l[16] not in ' A' or l[76:78].strip() in ['H','D']:continue
  key=(l[21],l[22:26].strip(),l[26].strip())
  v=residues.setdefault(key,{'name':l[17:20],'xyz':[]});v['xyz'].append([float(l[a:b]) for a,b in [(30,38),(38,46),(46,54)]])
 return residues
contacts={};summary={}
for pdb in ['7OW6','7PB2','7OW5']:
 atoms=read(r/'source'/f'{pdb}.pdb');partner=np.concatenate([v['xyz'] for k,v in atoms.items() if k[0] in 'DE']);obs={}
 for k,v in atoms.items():
  if k[0] not in 'ABC':continue
  dist=float(np.linalg.norm(np.asarray(v['xyz'])[:,None,:]-partner[None,:,:],axis=-1).min());obs[k]=(v['name'],dist)
 contacts[pdb]=obs;summary[pdb]={'observed_residues':len(obs),'contact_residues':sum(d<=4.5 for _,d in obs.values()),'peptide_contact_residues':sum(d<=4.5 for k,(_,d) in obs.items() if k[0]=='C'),'sha256':hashlib.sha256((r/'source'/f'{pdb}.pdb').read_bytes()).hexdigest()}
 with (r/f'{pdb}-contacts.csv').open('w') as f:
  w=csv.writer(f);w.writerow(['chain','number','insertion','name','minimum_TCR_distance_A','contact'])
  for k,(aa,d) in obs.items():w.writerow([*k,aa,d,int(d<=4.5)])
for name,pdbs in [('g12d',['7OW6','7PB2']),('wt',['7OW5']),('empty',[])]:
 target=read(r/'structures'/f'{name}.pdb')
 with (r/f'{name}.csv').open('w') as f:
  w=csv.writer(f);w.writerow(['chain','number','insertion','score','n_observed','n_contacts'])
  for k,v in target.items():
   observations=[contacts[p][k] for p in pdbs if k in contacts[p]]
   assert all(aa==v['name'] for aa,d in observations),(name,k,v,observations)
   n=len(observations);count=sum(d<=4.5 for aa,d in observations)
   w.writerow([*k,count/n if n else 'nan',n,count])
(r/'provenance.json').write_text(json.dumps({'cutoff_angstrom':4.5,'partner':'TCR chains D/E; all internal pMHC contacts excluded','aggregation':'contact structures / structures in which residue is observed','scope':'local native crystal comparison, not an exhaustive PDB search','g12d':['7OW6','7PB2'],'wt':['7OW5'],'empty':[],'structures':summary},indent=2))
print(json.dumps(summary,indent=2))
