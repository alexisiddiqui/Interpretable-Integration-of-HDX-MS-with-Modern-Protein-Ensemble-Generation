# 03 ValDX

Chapter hub for `thesis/chapters/03-valdx.tex`. Moved from the §1.7 hub on 2026-10-14; argument order not yet set. The chapter's contribution claims are the §1.5 claims listed under [[01-introduction]] §1.7 paragraph 3. The ValDX results that §1.5 no longer states are listed below.

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

## Results moved from §1.5

The introduction (§1.4, §1.5) states the principle in general terms. This chapter carries the ValDX evidence for each.

- Splits. [[Random and sequential splits gave no discrimination between candidate ensembles beyond training error.]] The result that led ValDX to partition by sequence coverage and by structural region, in the introduction's argument that partitions must follow peptide dependence.
- Work Done. [[Work Done quantifies changes in the ensemble-average protection-factor profile during fitting.]] This is ValDX's definition of the general idea in §1.5 group 5. It is independent of uptake, as HDXer's apparent work (a KL divergence over frame weights) is, but a different quantity.
  - [[Low validation error with high Work Done shows agreement reached by substantial modification of the prior.]]
  - [[Work Done measures distance from the prior, not from the true ensemble, and small values can also mean too little fitting.]]
- Kinetic mismatch. In a benchmark with an imposed kinetic mismatch, population changes compensated for incorrect exchange assumptions after calibration restored uptake agreement. Carries [[Fitted populations can compensate for errors in assumed exchange kinetics, and restoring uptake agreement by calibration does not validate kinetics or populations.]]
- Decoys (TeaA ISO-Trimodal). A candidate ensemble with intermediates absent from the target reached training agreement similar to one without them, yet the intermediates absorbed weight and prevented accurate population recovery. Carries [[Plausible but unpopulated candidate structures can absorb weight and prevent population recovery even when uptake matches.]] and [[Similar uptake agreement can coexist with different population recovery, so training error cannot verify populations.]]
- Cost. 3 replicates × 2 or 4 split types per ensemble across 22 ensembles, with a γ sweep in each. This is the figure behind the §1.5 group 6 claim that repeated assessment is expensive ([[04-jaxent]] and [[05-biofeaturisers]] answer it).

## Drafting sources

- ValDX revised manuscript (`projects/1-ValDX/manuscript/report/`): `1_introduction_omc.tex` L11–37; `7_results_omc.tex` L4–30 (the Work Done framework), L42–60 (TeaA), L189–211 and L248 (kinetic misspecification), L235–248 (clustering and limitations); `6_methods_omc.tex` L52, L70, L473, L510, L619.
- Method notes for ValDX splitting and consensus ([[02-background]] §2.5).

## Gaps
- Define the Work metrics, HDXer apparent work and the BICePs score side by side (`thesis/chapters/03-valdx.tex` L9).
- Settle median against mean for the consensus BV constants, and the peptide dropout wording, before citing [[Peptide splitting and consensus (ValDX)]].
