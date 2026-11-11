Primary figure: groove.png / groove.pdf / groove.svg
Metric: hmask predicted exposure × noise-averaged contact-head response.
Exposure: 1 - sigmoid(burial_logit), evaluated on the intact pMHC.
No dRSA checkpoint, external partner, or internal chain-edge masking is used.
Inputs: ../jaxka-kras-noise-propensity/{g12d,wt,empty}.csv
Reproduce values: python3 analyse.py (requires the sibling source directory).
Reproduce render: submit render.slurm on Pegasus, srf_cpu_01.
Palette: white to blue, shared 0–0.30 range. Values are not normalised per panel.
Per-residue CSVs retain exposure, contact response, proxy, scaled seed SD and uniform-noise sensitivity.
Seed SD describes variation across the four noise draws, not model or structural uncertainty.
Original checkpoint and source hashes are recorded in provenance.json.
