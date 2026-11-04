# Screened KRAS hit coloured by pLDDT

The overview panels show ID_1457932 with G12D pMHC, WT pMHC and peptide-free MHC. The hit uses pLDDT colours, HLA is light grey, β2m is darker grey and the peptide is magenta. The HLA chains share an orientation, origin and scale across panels.

## Regenerate

From the thesis root, run

```sh
python3 figures/jaxka-kras-pmhc-plddt/make.py
```

The script uses the installed PyMOL Python at `/Applications/PyMOL.app/Contents/bin/python` and `rsvg-convert`. On another machine, pass `--pymol-python /path/to/python` or set `PYMOL_PYTHON` to an interpreter with PyMOL and NumPy installed. There is no Blender dependency.

`render_pymol.py` loads the three local CIFs, explicitly fits HLA residues 1–180 by Cα using Kabsch alignment, applies a single shared display transform, checks the final alignment, colours the saved pLDDT values and ray-traces each panel. It saves `aligned.pse`, with scenes named `mutant`, `wt` and `empty`. The source coordinates remain unchanged. Only rigid transformations affect display coordinates.

Open `aligned.pse` in PyMOL to inspect the three scenes. To change the camera, rotate the model and save the view from PyMOL's Python console

```python
import json
open('/tmp/kras-camera.json', 'w').write(json.dumps(cmd.get_view()))
```

Then regenerate with that view

```sh
KRAS_CAMERA_JSON=/tmp/kras-camera.json python3 figures/jaxka-kras-pmhc-plddt/make.py
```

`KRAS_RENDER_WIDTH` and `KRAS_RENDER_HEIGHT` set the individual render resolution, defaulting to 1200 × 1200. Keep them equal for the square panel layout. `make.py --assemble-only` rebuilds the composite from existing PNGs. `render_pymol.py` can also be run directly inside PyMOL with `run /absolute/path/render_pymol.py`.

## Outputs and provenance

`fig.pdf`, `fig.svg` and `fig.png` contain the three-panel comparison. The SVG has editable headings and legend over embedded molecular images. Individual `*-pymol.png` files have transparent backgrounds; `*-white.png` are white previews. `camera.json` records the common camera, and `provenance.json` records the source hashes, verified alignment, rendering version and output hashes.

Chain A is HLA and B is β2m in every structure. In mutant and WT, C is peptide and D is the hit. In the peptide-free model, C is the hit. pLDDT is read directly from `B_iso_or_equiv` on its stored 0–100 scale, with bins below 50, 50–70, 70–90 and at least 90. High local confidence does not establish binding or correct relative chain placement.

The lower row uses a second shared camera tilted towards the peptide groove. It shows HLA residues 1–180 and, for the peptide-loaded complexes, hit residues 280–305 as cartoons, the peptide as sticks and hit residues within 4.5 Å of that peptide as sticks. Other hit regions are omitted from the close-up. The peptide-free panel shows the same HLA site without adding a peptide or a hypothetical hit loop. The six views are stored as overview scenes and `*_groove` scenes in `aligned.pse`; the detail camera is saved as `groove-camera.json`.
