Noise-averaged GQT surface maps

Run analyse.py with the hmask export selected by NOISE_MODEL and the installed pkanet/JAX GPU environment. The checked-in run.slurm records the Pegasus runtime. Four seeds each generate 8192 Gaussian vectors in batches of 256. Each is normalised by the trained aux_redge layer norm, then paired with the already-normalised target residue embedding. Sigmoid is applied before averaging. The same random stream is reset for each assembly. Uniform variance-one noise is an explicit distribution-sensitivity control.

The bound graph means the supplied intact assembly, with no external binder and no separation of internal chains. Original author chain IDs remain intact. No artificial covalent chain concatenation is performed.

Run render_pymol.py with PyMOL Python, then compose.py with NumPy and matplotlib. render.slurm reuses the existing opig-adaptyv PyMOL environment read-only. Scripts and outputs live in their own directory. frame-reference.json is a copied camera reference; no opig-adaptyv source code is modified.

Inputs derive from opig-adaptyv-2026/data/targets/challenge-5-kras-g12d-pmhc/structures/assembly1/7OW6.pdb, following experiment 043's matched-control construction. Output provenance contains input and checkpoint hashes. Rendering uses the opig structural house lighting and the thesis's shared-view comparison layout.

Primary outputs: groove.pdf / groove.png / groove.svg (peptide-visible groove comparison); fig.pdf / fig.png / fig.svg; differences.pdf / differences.png / differences.svg. Per-residue scores, paired differences, independent-seed variability and alternate-noise scores are retained in CSV and NPZ. provenance.json records convergence and distribution sensitivity; comparison.json records ranking stability, exposure correlation and paired-difference uncertainty.

Groove revision uses the floor-strand SVD normal and peptide N-to-C direction from experiment 080, with a 22-degree oblique tilt. Peptide sticks share the surface response scale, P6 is labelled, and the groove surface is 25% transparent. The dedicated groove figure includes peptide residue scores beneath each loaded-state panel. The model inputs and numerical scores are unchanged. Lower HLA and beta2m are hidden only in the close-up display.
