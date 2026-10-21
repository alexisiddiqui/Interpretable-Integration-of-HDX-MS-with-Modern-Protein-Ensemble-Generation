# 03 ValDX

Chapter hub for `thesis/chapters/03-valdx.tex`. Moved from the §1.7 hub on 2026-10-14; argument order not yet set. The chapter's contribution claims are the §1.5 claims listed under [[01-introduction]] §1.7 paragraph 3, and they are not repeated here.

Status sentence: complete. Manuscript post-review; preprint v1 posted ([[@siddiquiFrameworkTestingStructural2026]]).

## Detail moved from §1.7

- Tools. Overlap-aware splits and replicate fits give a validation error that reflects prediction beyond the training peptides, and reduce rather than remove dependence between splits.
- Work Done measures how much the ensemble was modified to reach agreement, independent of uptake error, and is a distance from the prior rather than from the truth.
- Result. Across 22 ensembles of six proteins (58 to 480 residues), conventional error did not establish population accuracy on its own, and Work Done ranked candidate hypotheses.
- Representation. Clustering to 10 to 20% of the parent ensemble preserved performance, and smaller sets aid interpretation when the conclusion survives a change of cluster size.
- Protocol. Under an imposed kinetic mismatch, fitting forward-model parameters before reweighting limited population distortion. The advice is conditional on the suspected mismatch, not a general fitting order.
- Decoys. Artificial and decoy conformations probe what the BV model can and cannot distinguish.
- BiCePs beside Work Done (`03-valdx.tex` comment): a full Bayesian score as the comparison. Not in the preprint; stub.
- Boundary, handed to ch. 4 and 5. Conclusions are comparative across the candidates supplied, reweighting cannot add states, and replicate uncertainty does not name its cause.
- The five "revised ValDX only" claims in §1.5 become supported once the revision is posted.

## Drafting sources

- ValDX revised manuscript (`projects/1-ValDX/manuscript/report/`): `1_introduction_omc.tex` L11–37; `7_results_omc.tex` L4–30 (the Work Done framework), L42–60 (TeaA), L189–211 and L248 (kinetic misspecification), L235–248 (clustering and limitations); `6_methods_omc.tex` L52, L70, L473, L510, L619.
- Method notes for ValDX splitting and consensus ([[02-background]] §2.5).
