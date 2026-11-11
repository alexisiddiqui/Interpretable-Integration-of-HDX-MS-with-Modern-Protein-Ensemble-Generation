from pathlib import Path
import csv,json,math
import numpy as np
from pymol import cmd
root=Path(__file__).resolve().parent
names=['g12d','wt','empty']; tables={}
for n in names:
 with (root/f'{n}.csv').open() as f:tables[n]={(r['chain'],str(r['number']),r['insertion']):float(r['score']) for r in csv.DictReader(f)}
lo,hi=0.0,1.0
cmd.reinitialize()
for n in names:cmd.load(str(root/'structures'/f'{n}.pdb'),n)
# Peptide-aligned groove frame, following experiment 080 target_mass_render.py.
cmd.dss()
floor=cmd.get_coords('g12d and chain A and resi 1-180 and name CA and ss S')
centre=floor.mean(0); normal=np.linalg.svd(floor-centre)[2][2]
pep=cmd.get_coords('g12d and chain C and name CA')
if np.dot(pep.mean(0)-centre,normal)<0:normal=-normal
x=pep[-1]-pep[0];x-=np.dot(x,normal)*normal;x/=np.linalg.norm(x)
y=np.cross(normal,x);basis=np.stack([x,y,normal],axis=1)
origin=pep.mean(0)
for n in names:cmd.load_coords((cmd.get_coords(n)-origin)@basis,n)
identity=(1,0,0,0,1,0,0,0,1,0,0,-150,0,0,0,1,400,0)
cmd.set_view(identity);cmd.set('orthoscopic',1)
settings={'bg_rgb':[1,1,1],'ray_opaque_background':1,'antialias':2,'max_threads':4,'surface_quality':1,'two_sided_lighting':1,'ambient':0.45,'direct':0.38,'reflect':0.22,'specular':0.15,'shininess':18,'ray_trace_mode':1,'ray_trace_gain':0.10,'ray_shadows':0,'depth_cue':0,'cartoon_fancy_helices':1,'cartoon_flat_sheets':1,'cartoon_side_chain_helper':1}
for k,v in settings.items():cmd.set(k,v)
cmd.hide('everything');cmd.show('surface');cmd.set('surface_solvent',0)
# Continuous white-to-dark-red map; all components share the score colours.
for i in range(256):
 t=i/255;palette=np.array([[int(h[j:j+2],16)/255 for j in (1,3,5)] for h in ['#ffffff','#e5f5e0','#c7e9c0','#a1d99b','#74c476','#31a354','#006d2c']]);cmd.set_color(f'p{i}',[float(np.interp(t,np.linspace(0,1,7),palette[:,j])) for j in range(3)])
for n in names:
 for (chain,resi,ins),value in tables[n].items():
  if not np.isfinite(value):
   cmd.color('grey80',f'{n} and chain {chain} and resi {resi}{ins}');continue
  idx=int(np.clip((value-lo)/(hi-lo),0,1)*255)
  cmd.color(f'p{idx}',f'{n} and chain {chain} and resi {resi}{ins}')
cmd.set_color('peptide_orange',[1,0.59,0.12]);cmd.set_color('p6_red',[0.86,0.08,0.08])
cmd.set('stick_radius',0.45);cmd.set('sphere_scale',0.38)
def representation(n,detail):
 cmd.hide('everything',n)
 cmd.show('surface',f'{n} and '+('(chain A and resi 1-180)' if detail else 'chain A+B'))
 cmd.set('transparency',0.25 if detail else 0.0,n)
 if n!='empty':
  cmd.show('sticks',f'{n} and chain C')
  cmd.show('spheres',f'{n} and chain C and resi 6 and name CA')
  cmd.set('label_color','black');cmd.set('label_outline_color','white');cmd.set('label_size',20);cmd.set('float_labels',1)
  cmd.set('label_position',(1.5,-2.0,2.0))
  cmd.label(f'{n} and chain C and resi 6 and name CA',repr('P6'))
cmd.disable('all');cmd.enable('g12d')
cmd.set_view(identity);cmd.turn('x',65);cmd.zoom('g12d',buffer=5,complete=1);whole=list(cmd.get_view())
cmd.set_view(identity);cmd.turn('x',22)
cmd.zoom('g12d and ((chain A and resi 1-180) or chain C)',buffer=5,complete=1);groove=list(cmd.get_view())
for view,camera in [('groove',groove)]:
 for n in names:
  cmd.disable('all');cmd.enable(n);representation(n,view=='groove');cmd.set_view(camera)
  cmd.ray(1300,1100);cmd.png(str(root/f'{n}-{view}.png'),dpi=300,ray=0)

(root/'render-provenance.json').write_text(json.dumps({'engine':cmd.get_version()[0],'settings':settings,'score_limits':[lo,hi],'cameras':{'groove':groove},'frame_basis':basis.tolist(),'frame_origin':origin.tolist(),'peptide':'same observed contact-frequency scale as HLA; P6 labelled'},indent=2))
