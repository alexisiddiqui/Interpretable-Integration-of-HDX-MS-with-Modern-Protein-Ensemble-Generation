"""Select a weighted medoid from closed refined structures after Fiedler-lobe-I fitting.
Distances are all-CA RMSD in the common closed-reference frame (not pairwise refits).
The candidate minimising sum_j w_j RMSD(i,j) represents the weighted closed pool.
Usage: python render_teaa.py <structures-root> <scores-csv> <output-folder>
"""
import csv,json,sys
from pathlib import Path
import numpy as np
root,csvpath,out=map(Path,sys.argv[1:]);out.mkdir(parents=True,exist_ok=True)
axis=json.load(open(next(root.rglob('blind_axis_fiedler.json'))));fit=np.array(axis['lobe_I'])-1
ref=next(root.rglob('TeaA_ref_closed_boltznames.pdb'))
def coords(p):
 return np.array([[float(l[30:38]),float(l[38:46]),float(l[46:54])] for l in p.read_text().splitlines() if l.startswith('ATOM') and l[12:16].strip()=='CA'])
reference=coords(ref);rows=[r for r in csv.DictReader(csvpath.open()) if r['ensemble']=='refined_a025' and float(r['theta'])>5]
aligned=[]
for r in rows:
 p=root/r['path'].lstrip('/');x=coords(p);assert x.shape==reference.shape==(309,3)
 xc=x[fit].mean(0);rc=reference[fit].mean(0);u,s,vh=np.linalg.svd((x[fit]-xc).T@(reference[fit]-rc));rot=u@np.diag([1,1,np.linalg.det(u@vh)])@vh
 aligned.append((x-xc)@rot+rc)
X=np.array(aligned);w=np.array([float(r['weight_l1000']) for r in rows]);w/=w.sum();dist=np.sqrt(np.mean(np.sum((X[:,None]-X[None,:])**2,axis=-1),axis=-1));scores=dist@w;j=int(scores.argmin());chosen=rows[j];p=root/chosen['path'].lstrip('/')
# Refit all atoms of the chosen PDB with its CA-derived rigid transformation.
x=coords(p);xc=x[fit].mean(0);rc=reference[fit].mean(0);u,s,vh=np.linalg.svd((x[fit]-xc).T@(reference[fit]-rc));rot=u@np.diag([1,1,np.linalg.det(u@vh)])@vh
lines=[]
for line in p.read_text().splitlines():
 if line.startswith(('ATOM','HETATM')):
  v=(np.array([float(line[30:38]),float(line[38:46]),float(line[46:54])])-xc)@rot+rc;line=line[:30]+''.join(f'{q:8.3f}' for q in v)+line[54:]
 lines.append(line)
rep=out/'closed_weighted_medoid.pdb';rep.write_text('\n'.join(lines)+'\n')
audit={'rule':'theta > 5 degrees; minimum weighted mean all-CA RMSD after common Fiedler-lobe-I fit','n_closed':len(rows),'path':chosen['path'],'theta':float(chosen['theta']),'pool_weight':float(chosen['weight_l1000']),'weighted_mean_RMSD_A':float(scores[j]),'lobe_II_RMSD_to_closed_A':float(np.sqrt(np.mean(np.sum((X[j][np.array(axis['lobe_II'])-1]-reference[np.array(axis['lobe_II'])-1])**2,axis=-1))))}
(out/'closed_medoid.json').write_text(json.dumps(audit,indent=2));print(json.dumps(audit,indent=2),flush=True)
import pymol
pymol.finish_launching(['pymol','-cq'])
from pymol import cmd
cmd.load(str(ref),'reference');cmd.load(str(rep),'refined');cmd.hide('everything');cmd.show('cartoon');cmd.color('marine','reference');cmd.set_color('teal',[0,.475,.42]);cmd.color('teal','refined');cmd.set('cartoon_transparency',.2,'reference');cmd.orient('all');cmd.zoom('all',5);cmd.bg_color('white');cmd.set('orthoscopic',1);cmd.set('ray_shadows',0);cmd.set('antialias',2);cmd.set('ambient',.6);cmd.set('max_threads',4);cmd.png(str(out/'closed_overlay.png'),width=1200,height=1000,dpi=200,ray=1);cmd.quit()
