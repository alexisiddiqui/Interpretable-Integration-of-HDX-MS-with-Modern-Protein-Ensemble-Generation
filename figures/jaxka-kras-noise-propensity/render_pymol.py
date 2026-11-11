from pathlib import Path
import csv,json,math
import numpy as np
from pymol import cmd
root=Path(__file__).resolve().parent
names=['g12d','wt','empty']; tables={}
for n in names:
 with (root/f'{n}.csv').open() as f:tables[n]={(r['chain'],str(r['number']),r['insertion']):float(r['score']) for r in csv.DictReader(f)}
lo=min(min(t.values()) for t in tables.values());hi=max(max(t.values()) for t in tables.values())
lo=math.floor(lo*100)/100;hi=math.ceil(hi*100)/100
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
 t=i/255;cmd.set_color(f'p{i}',[1-t*(1-0.55),1-t*(1-0.04),1-t*(1-0.12)])
for n in names:
 for (chain,resi,ins),value in tables[n].items():
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
for view,camera in [('whole',whole),('groove',groove)]:
 for n in names:
  cmd.disable('all');cmd.enable(n);representation(n,view=='groove');cmd.set_view(camera)
  cmd.ray(1300,1100);cmd.png(str(root/f'{n}-{view}.png'),dpi=300,ray=0)
# Differences on common residues; absent peptide in the deletion contrast is grey.
deltas={n:{k:tables['g12d'][k]-v for k,v in tables[n].items()} for n in ['wt','empty']}
limit=max(abs(x) for d in deltas.values() for x in d.values());limit=max(0.001,math.ceil(limit*1000)/1000)
for i in range(257):
 t=(i-128)/128;c=np.array([0.1,0.35,0.7]) if t<0 else np.array([0.7,0.04,0.12]);cmd.set_color(f'd{i}',(1-abs(t)+abs(t)*c).tolist())
for n in ['wt','empty']:
 cmd.disable('all');cmd.enable('g12d');cmd.color('grey80','g12d')
 for (ch,res,ins),v in deltas[n].items():cmd.color(f'd{int(np.clip(v/limit,-1,1)*128+128)}',f'g12d and chain {ch} and resi {res}{ins}')
 representation('g12d',True)
 if n=='empty':cmd.hide('sticks','g12d and chain C');cmd.hide('spheres','g12d and chain C');cmd.hide('labels','g12d and chain C')
 cmd.set_view(groove);cmd.ray(1300,1100);cmd.png(str(root/f'delta-{n}.png'),dpi=300,ray=0)
(root/'render-provenance.json').write_text(json.dumps({'engine':cmd.get_version()[0],'settings':settings,'score_limits':[lo,hi],'difference_limits':[-limit,limit],'cameras':{'whole':whole,'groove':groove},'missing_peptide':'hidden in deletion contrast; not assigned zero','frame_basis':basis.tolist(),'frame_origin':origin.tolist(),'peptide':'opaque sticks on the same score scale as HLA; P6 labelled','reference_scripts':['experiments/080-kras-atlas-p6-edge-screen/target_mass_render.py','writeup/figures/c5-target-states/render_pymol.py']},indent=2))
cmd.save(str(root/'maps.pse'))
