# KRAS pMHC radial comparisons

Four comparisons retain the Challenge 5 dashboard's radial renderer and fixed colour scales. Each uses the same arrangement, with experimental TCR complexes above the screened lead and G12D to the left of WT. The default `fig.pdf` combines electrostatics above hydrophobicity, with columns for crystal G12D, crystal WT, screened G12D and screened WT. `shape.pdf`, `hydrophobicity.pdf` and `size.pdf` provide the other dashboard properties. SVG and PNG versions accompany each PDF.

Run `python3 figures/jaxka-kras-pmhc-radial/make.py` from the thesis root. The build uses Node and `rsvg-convert` and performs no scientific calculations. `dashboard-radial-maps.js` is an unchanged copy of the upstream renderer. `make.mjs` calls its drawing function through a small SVG DOM adapter and composes four panels. `radial-data.json` preserves the four complete upstream records and method description. `source.json` records source paths and hashes; `provenance.json` records the render inputs and outputs.

## Coordinates for structural views

The structures below retain the exact coordinates used for the radial calculations. Predicted CIFs are decompressed without changing their contents. All four hashes match the upstream radial records. Coordinates remain in their original frames; the radial projection aligns the HLA groove for display only. Use the first model of the deposited biological assembly for the crystal structures.

| File | Context | Chain roles |
|---|---|---|
| `structures/7OW6-mutant.pdb` | Experimental JDIa41b1 TCR with G12D pMHC | A HLA, B β2m, C peptide, D/E TCR |
| `structures/7OW5-wt.pdb` | Experimental JDIa41b1 TCR with WT pMHC | A HLA, B β2m, C peptide, D/E TCR |
| `structures/ID_1457932-mutant.cif` | Predicted screened lead with G12D pMHC | A HLA, B β2m, C peptide, D candidate |
| `structures/ID_1457932-wt.cif` | Predicted screened lead with WT pMHC | A HLA, B β2m, C peptide, D candidate |

The mutation site is peptide C:6. The lead's original patch uses candidate positions 100, 290 and 291 in one-based numbering. The stored source indices are 99, 289 and 290 in zero-based numbering. The aligned pLDDT structural views and their PyMOL regeneration script are in [jaxka-kras-pmhc-plddt](../jaxka-kras-pmhc-plddt/README.md).
