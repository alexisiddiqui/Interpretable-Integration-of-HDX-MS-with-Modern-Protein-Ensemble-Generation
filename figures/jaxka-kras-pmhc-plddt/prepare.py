"""Export pLDDT-coloured cartoon geometry from unchanged saved predictions."""
from pathlib import Path
import json,hashlib,re
import numpy as np
import pymol
pymol.finish_launching(['pymol','-cq'])
from pymol import cmd
root=Path(__file__).resolve().parent
states=['mutant','wt','empty'];receipt={'structures':{},'alignment':{},'palette':{'0–50':'#ff7d45','50–70':'#ffdb13','70–90':'#65cbf3','90–100':'#0053d6'}}
for name in states:
 path=root/'structures'/f'{name}.cif';cmd.load(str(path),name)
 atoms=cmd.get_model(name).atom;bs=[a.b for a in atoms]
 assert all(0<=b<=100 for b in bs)
 receipt['structures'][name]={'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'atoms':len(atoms),'plddt_range':[min(bs),max(bs)],'chain_roles':{'A':'HLA','B':'beta2m',**({'C':'peptide','D':'hit'} if name!='empty' else {'C':'hit'})}}
 if name!='mutant':
  result=cmd.align(f'{name} and chain A and name CA and resi 1-180','mutant and chain A and name CA and resi 1-180',cycles=0)
  receipt['alignment'][name]={'HLA_CA_RMSD':result[0],'aligned_atoms':result[1]}
# Common display frame: peptide N-to-C horizontal and hit above HLA.
ca=cmd.get_coords('mutant and chain C and name CA');origin=ca.mean(axis=0)
x=ca[-1]-ca[0];x/=np.linalg.norm(x)
y=cmd.get_coords('mutant and chain D and name CA').mean(axis=0)-cmd.get_coords('mutant and chain A and name CA').mean(axis=0)
y-=x*np.dot(x,y);y/=np.linalg.norm(y);z=np.cross(x,y);basis=np.array([x,y,z]).T
receipt['display_frame']={'origin_angstrom':origin.tolist(),'basis_columns':basis.tolist(),'determinant':float(np.linalg.det(basis))}
for name in states:
 xyz=cmd.get_coords(name);new=(xyz-origin)@basis
 assert np.allclose(np.linalg.norm(xyz[1:]-xyz[:-1],axis=1),np.linalg.norm(new[1:]-new[:-1],axis=1),atol=1e-4)
 cmd.load_coords(new,name)
cmd.hide('everything');cmd.show('cartoon');cmd.dss()
cmd.set('cartoon_fancy_helices',1);cmd.set('cartoon_flat_sheets',1);cmd.set('cartoon_sampling',7);cmd.set('cartoon_loop_radius',0.22)
for color,hexcol in [('verylow','#ff7d45'),('low','#ffdb13'),('confident','#65cbf3'),('veryhigh','#0053d6')]:cmd.set_color(color,[int(hexcol[i:i+2],16)/255 for i in (1,3,5)])
cmd.color('verylow','all');cmd.color('low','b > 49.999');cmd.color('confident','b > 69.999');cmd.color('veryhigh','b > 89.999')
# A thicker peptide trace preserves its position in the groove without changing colour.
cmd.set('cartoon_loop_radius',0.45,'(mutant or wt) and chain C')
cmd.save(str(root/'structures.pse'))
for name in states:
 cmd.disable('all');cmd.enable(name)
 wrl=root/(name+'.wrl');cmd.save(str(wrl))
 s=wrl.read_text()
 def vals(pattern):return np.fromstring(re.search(pattern,s,re.S).group(1).replace(',',' '),sep=' ')
 xyz=vals(r'coord Coordinate\s*\{\s*point\s*\[(.*?)\]') .reshape(-1,3)
 rgba=vals(r'color Color\s*\{\s*color\s*\[(.*?)\]').reshape(-1,3)
 ix=vals(r'coordIndex\s*\[(.*?)\]').astype(int).reshape(-1,4)
 assert np.all(ix[:,-1]==-1) and len(xyz)==len(rgba)
 np.savez_compressed(root/(name+'-mesh.npz'),vertices=xyz,colors=rgba,triangles=ix[:,:3]);wrl.unlink()
receipt['pymol_version']=cmd.get_version()[0]
(root/'source.json').write_text(json.dumps(receipt,indent=2)+'\n')
cmd.quit()
