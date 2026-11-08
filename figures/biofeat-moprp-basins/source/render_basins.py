"""Headless PyMOL render of the basin ensembles, using JAX-ENT's RMSD_by_res render settings.

Each basin PDB (from extract_basins.py) holds superposed frames whose B-factors are per-residue
backbone RMSD (A) from the minimised start structure; the minimised structure is drawn as a
transparent white tube.

Usage: pymol -cq render_basins.py -- <frames_dir> <out_dir> <rmsd_min> <rmsd_max> [reference_suffix]
"""
import json
import sys
from pathlib import Path

from pymol import cmd

JAXENT_PYMOL = Path.home() / "JAX-ENT/jaxent/src/analysis/pymol"
sys.path.insert(0, str(JAXENT_PYMOL))
from config import load_config  # noqa: E402
from utils import (apply_bfactor_spectrum, apply_putty_settings,  # noqa: E402
                   apply_render_settings, set_background_white)

frames_dir, out_dir = Path(sys.argv[1]), Path(sys.argv[2])
lo, hi = float(sys.argv[3]), float(sys.argv[4])
ref_suffix = sys.argv[5] if len(sys.argv) > 5 else ""  # "_101" for the HDX-residue set
out_dir.mkdir(parents=True, exist_ok=True)

# MoPrP per-residue RMSD style from the JAX-ENT examples; range rescaled to these deviations
render = load_config(str(Path.home() / "JAX-ENT/jaxent/examples/3_CrossValidationBV/analysis/"
                         "pymol_viz_configs/rmsd_by_res_MoPrP.yaml")).render
render.spectrum_range = (lo, hi)
render.view = None  # that camera was set for the 2L39 crop numbering
render.putty_range = (0.25, 1.6)  # thinner than the example: these deviations run to >8 A

basins = json.loads((frames_dir / "basins.json").read_text())
views = {}
for b in basins:
    tag = b["ph"].replace(" ", "").lower()
    cmd.reinitialize()
    set_background_white()
    cmd.load(str(frames_dir / f"{tag}_minimised{ref_suffix}.pdb"), "minimised")
    cmd.load(str(frames_dir / b["file"]), "ens")
    cmd.split_states("ens", prefix="frm_")
    cmd.delete("ens")
    cmd.hide("everything")
    cmd.remove("hydro")

    cmd.alter("frm_*", f"b=min(b, {hi})")  # cap so putty width and colour saturate at the top of the scale
    cmd.show("cartoon", "frm_*")
    cmd.cartoon("putty", "frm_*")
    apply_putty_settings("frm_*", render)
    apply_bfactor_spectrum("frm_*", render)
    cmd.set("cartoon_transparency", render.trajectory_transparency, "frm_*")

    cmd.alter("minimised", "b=0.5")
    cmd.show("cartoon", "minimised")
    cmd.cartoon("tube", "minimised")
    cmd.set("cartoon_tube_radius", 0.5, "minimised")
    cmd.color("grey80", "minimised")
    cmd.set("cartoon_transparency", 0.55, "minimised")

    apply_render_settings(render)
    if tag not in views:  # one camera per pH, set on the minimised structure
        cmd.orient("minimised and name CA")
        cmd.zoom("minimised", 12)
        views[tag] = cmd.get_view()
    cmd.set_view(views[tag])

    png = out_dir / b["file"].replace(".pdb", ".png")
    cmd.png(str(png), width=1400, height=1100, dpi=200, ray=1)
    print("wrote", png)
