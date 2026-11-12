"""Headless PyMOL: all six existing 12-frame basin ensembles, one common core-aligned camera.
PDB numbering starts at PrP 122; selection residue numbers therefore add 121.
Usage: <pymol-environment>/bin/python render_moprp.py <frames> <output>
"""
from pathlib import Path
import sys,json
import pymol
pymol.finish_launching(['pymol','-cq'])
from pymol import cmd
src,out=map(Path,sys.argv[1:]);out.mkdir(exist_ok=True,parents=True)
bs=json.load(open(src/'basins.json'));cmd.load(str(src/'ph4_minimised_101.pdb'),'anchor');cmd.remove('hydro');cmd.orient('anchor');cmd.zoom('anchor',12);view=cmd.get_view()
# Common core alignment uses analysis residues 175–187 and 201–216 (file indices 54–66 and 80–95).
core='name CA and resi 54-66+80-95'
for b in bs:
 cmd.delete('ens');cmd.delete('ref');cmd.delete('labels');cmd.load(str(src/b['file']),'ens');tag=b['ph'].replace(' ','').lower();cmd.load(str(src/f'{tag}_minimised_101.pdb'),'ref')
 if tag=='ph7':
  # Apply the same core-fit rigid transformation to the reference and every frame.
  cmd.align('ref and '+core,'anchor and '+core,cycles=0,transform=1)
  matrix=cmd.get_object_matrix('ref');cmd.transform_object('ens',matrix)
 cmd.hide('everything');cmd.show('cartoon','ens or ref');cmd.set('all_states',1);cmd.cartoon('tube','ref');cmd.set('cartoon_tube_radius',.35,'ref');cmd.color('grey65','ref');cmd.set('cartoon_transparency',.6,'ref')
 cmd.cartoon('putty','ens');cmd.set('cartoon_putty_scale_min',.3);cmd.set('cartoon_putty_scale_max',1.5);cmd.set('cartoon_putty_transform',0);cmd.set('cartoon_putty_radius',.2);cmd.spectrum('b','paleyellow orange pink red black','ens',minimum=.5,maximum=8);cmd.set('cartoon_transparency',.45,'ens')
 # Labels are attached to the common reference, so every panel teaches the same orientation.
 for name,res in [('β1',9),('α1',27),('β2',40),('core',88)]:
  pos=cmd.get_atom_coords(f'ref and name CA and resi {res}');cmd.pseudoatom('labels',pos=pos,label=name)
 cmd.hide('everything','labels');cmd.show('labels','labels');cmd.set('label_color','black');cmd.set('label_size',22);cmd.set('label_font_id',7);cmd.set('label_outline_color','white');cmd.set('label_position',(2,2,2))
 cmd.bg_color('white');cmd.set('opaque_background',1);cmd.set('ray_opaque_background',1);cmd.set('orthoscopic',1);cmd.set('antialias',2);cmd.set('ray_shadows',0);cmd.set('ambient',.65);cmd.set('specular',.15);cmd.set('max_threads',4);cmd.set_view(view)
 cmd.png(str(out/(Path(b['file']).stem+'.png')),width=1200,height=1050,dpi=200,ray=1);print(b['file'],flush=True)
(out/'camera.json').write_text(json.dumps(list(view)))
cmd.quit()
