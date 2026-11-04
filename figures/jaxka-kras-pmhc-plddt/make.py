"""Regenerate the aligned PyMOL renders and the five-panel figure.

python3 figures/jaxka-kras-pmhc-plddt/make.py
python3 figures/jaxka-kras-pmhc-plddt/make.py --assemble-only
Override PyMOL's Python with --pymol-python or PYMOL_PYTHON.
"""
from pathlib import Path
import argparse,os,subprocess,shutil,sys
root=Path(__file__).resolve().parent
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--pymol-python',default=os.environ.get('PYMOL_PYTHON','/Applications/PyMOL.app/Contents/bin/python'))
p.add_argument('--assemble-only',action='store_true');a=p.parse_args()
if not a.assemble_only:
 if not Path(a.pymol_python).is_file():p.error('Set --pymol-python to a Python executable with pymol installed.')
 driver='import pymol; pymol.finish_launching(["pymol","-cq"]); import runpy; runpy.run_path('+repr(str(root/'render_pymol.py'))+',run_name="__main__"); pymol.cmd.quit()'
 subprocess.run([a.pymol_python,'-c',driver],check=True)
 for name in ['mutant','wt','empty']:
  for suffix in ['-pymol.png']+(['-groove.png'] if name!='empty' else []):
   if not (root/(name+suffix)).is_file():raise RuntimeError('PyMOL did not produce '+name+suffix)
subprocess.run([sys.executable,str(root/'compose.py')],check=True)
