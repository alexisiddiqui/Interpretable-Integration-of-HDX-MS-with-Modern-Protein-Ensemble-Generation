Run analyse.py with NumPy to reproduce per-residue TCR contact calls from the three frozen crystal PDB files. Residue identity is checked before mapping onto the fixed display structures. Missing observations remain NaN and are rendered grey.

Source: opig-adaptyv experiment 075 native crystal panel. The subsequent RCSB API audit (pdb-search/) used exact and unanchored peptide queries plus a broader KRAS/HLA title search. It found no additional eligible partner-bound structures for these decamers on HLA-A*11:01. No predicted complexes or ATLAS screening scores enter this plot. The 7OW6/7PB2 TCRs are related, not independent biological replicates.

Render with render.slurm on Pegasus, using the same groove framing and representation as the GQT and PeSTo plots. Files in the opig-adaptyv repository are read-only.
