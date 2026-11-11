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
# Matched controls are in identical coordinates; use the established crystal groove orientation.
frame=json.loads((root/'frame-reference.json').read_text())
cmd.set_view(frame['view']);cmd.set('orthoscopic',1)
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
cmd.disable('all');cmd.enable('g12d')
cmd.turn('x',65);cmd.zoom('g12d',buffer=5,complete=1);whole=list(cmd.get_view())
cmd.set_view(frame['view']);cmd.zoom('g12d and ((chain A and resi 1-180) or chain C)',buffer=7,complete=1);groove=list(cmd.get_view())
for view,camera in [('whole',whole),('groove',groove)]:
 for n in names:
  cmd.disable('all');cmd.enable(n);cmd.set_view(camera)
  cmd.ray(1300,1100);cmd.png(str(root/f'{n}-{view}.png'),dpi=300,ray=0)
# Differences on common residues; absent peptide in the deletion contrast is grey.
deltas={n:{k:tables['g12d'][k]-v for k,v in tables[n].items()} for n in ['wt','empty']}
limit=max(abs(x) for d in deltas.values() for x in d.values());limit=max(0.001,math.ceil(limit*1000)/1000)
for i in range(257):
 t=(i-128)/128;c=np.array([0.1,0.35,0.7]) if t<0 else np.array([0.7,0.04,0.12]);cmd.set_color(f'd{i}',(1-abs(t)+abs(t)*c).tolist())
for n in ['wt','empty']:
 cmd.disable('all');cmd.enable('g12d');cmd.color('grey80','g12d')
 for (ch,res,ins),v in deltas[n].items():cmd.color(f'd{int(np.clip(v/limit,-1,1)*128+128)}',f'g12d and chain {ch} and resi {res}{ins}')
 cmd.set_view(groove);cmd.ray(1300,1100);cmd.png(str(root/f'delta-{n}.png'),dpi=300,ray=0)
(root/'render-provenance.json').write_text(json.dumps({'engine':cmd.get_version()[0],'settings':settings,'score_limits':[lo,hi],'difference_limits':[-limit,limit],'cameras':{'whole':whole,'groove':groove},'missing_peptide':'grey; not assigned zero'},indent=2))
cmd.save(str(root/'maps.pse'))
