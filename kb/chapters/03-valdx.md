# 03 ValDX

Chapter hub for `thesis/chapters/03-valdx.tex`. Moved from the §1.7 hub on 2026-10-14. The seven sections follow the plan in `03-valdx.tex` L4–40, which follows the manuscript's results argument (`7_results_omc.tex` L4). The chapter's contribution claims are the §1.5 claims listed under [[01-introduction]] §1.7 paragraph 3. The ValDX results that §1.5 no longer states are listed below. The introduction (§1.4, §1.5) states the principle in general terms. This chapter carries the ValDX evidence for each.

Status sentence: complete. Manuscript post-review; preprint v1 posted ([[@siddiquiFrameworkTestingStructural2026]]).

Porting order: methods and appendix (§2, Appendix A) → results (§3–6: manuscript results, then the promoted supplementary analyses) → introduction (§1) → discussion (§7).

Paths below are in `projects/1-ValDX/manuscript/report/` (the revised manuscript).

## 1 Introduction and objectives

- Result. Across 22 ensembles of six proteins (58 to 480 residues), conventional error did not establish population accuracy on its own, and Work Done ranked candidate hypotheses.

Sources: `1_introduction_omc.tex` L11–37.

## 2 Validation framework and methods

- Tools. Overlap-aware splits and replicate fits give a validation error that reflects prediction beyond the training peptides, and reduce rather than remove dependence between splits.
- Splits. [[Random and sequential splits gave no discrimination between candidate ensembles beyond training error.]] The result that led ValDX to partition by sequence coverage and by structural region, in the introduction's argument that partitions must follow peptide dependence.
- Work Done measures how much the ensemble was modified to reach agreement, independent of uptake error, and is a distance from the prior rather than from the truth.
- Work Done. [[Work Done quantifies changes in the ensemble-average protection-factor profile during fitting.]] This is ValDX's definition of the general idea in §1.5 group 4. It is independent of uptake, as HDXer's apparent work (a KL divergence over frame weights) is, but a different quantity.
  - [[Low validation error with high Work Done shows agreement reached by substantial modification of the prior.]]
  - [[Work Done measures distance from the prior, not from the true ensemble, and small values can also mean too little fitting.]]
- BICePs beside Work Done (`6_methods_omc.tex` L464): a full Bayesian score as the comparison.
- Cost. 3 replicates × 2 or 4 split types per ensemble across 22 ensembles, with a γ sweep in each. This is the figure behind the §1.5 group 6 claim that repeated assessment is expensive ([[04-jaxent]] and [[05-biofeaturisers]] answer it).

Sources: `7_results_omc.tex` L4–30 (the Work Done framework); `6_methods_omc.tex` L52, L70, L473, L510, L619. Method notes for ValDX splitting and consensus ([[02-background]] §2.5).

### Methods port: sources and appendix destinations

Ranges run heading to heading.

| Thesis section | Chapter text from | Appendix destination (from) | Method note |
|---|---|---|---|
| `sec:valdx-inputs` | `6_methods_omc.tex` L19–53 (data, `tab:HDX-MS`, BPTI uptake Eq. L50), L83–106 (ensemble summary, `tab:ensemble_summary`) | `app:valdx-hdx-data` (L54–67); `app:valdx-af2` (L164–188; `Extended_SI.tex` L125–146, L339–363, L557–579); `app:valdx-md-setup` (L189–242); `app:valdx-md-protocols` (L243–255) | — |
| `sec:valdx-splits` | L68–81; L473 (replicate design); `7_results_omc.tex` L27–30 | `app:valdx-case-studies` (replicate counts, L612–717) | [[Peptide splitting and consensus (ValDX)]] |
| `sec:valdx-fitting` | L356–460 (protocols, `tab:optimisation_protocols`, HDXer loss), L461 (γ), L468–483 (flow, knee, failures) | `app:valdx-case-studies` (L612–717; knee algorithm `Extended_SI.tex` L611–666) | [[Peptide splitting and consensus (ValDX)]] |
| `sec:valdx-work` | L485–603 (`tab:metrics_summary`; Work Done L508–577, distinction from apparent work L508; ΔMSE and z-score L579–603); L464 (BICePs); L295–355 (structural metrics, summary only); `7_results_omc.tex` L11–26 | `app:valdx-mathematics` (`Extended_SI.tex` L248–336 Work definitions; L449–486 pair-distance RMS and W1; L580–610 LCC; `9_Supplementary_information.tex` L304 weighted RMSF) | [[Work Done (ValDX)]], [[Structural comparison metrics (ValDX)]] |
| `sec:valdx-synthetic` | L107–125 (Iso-Validation), L126–163 (kinetic misspecification), L661–694 (kinetic protocol) | `app:valdx-synthetic` (L131–163 rate equations and noise; `9_Supplementary_information.tex` L5–40 simulator validation and digestion) | — |
| `sec:valdx-decoys` | L256–283 (poisoning, `tab:poisoning_types`); L695–717 (cluster sweep, poisoning protocol) | `app:valdx-perturbations` (`Extended_SI.tex` L364–448) | — |
| `sec:valdx-statistics` | L604–611 | `app:valdx-mathematics` (`Extended_SI.tex` L667–729 regression, ΔR², η²) | — |
| — | — | `app:valdx-implementation` (L719–781; `Extended_SI.tex` L487–556) | — |

## 3 Uptake agreement and population recovery

- Decoys (TeaA ISO-Trimodal). A candidate ensemble with intermediates absent from the target reached training agreement similar to one without them, yet the intermediates absorbed weight and prevented accurate population recovery. Carries [[Plausible but unpopulated candidate structures can absorb weight and prevent population recovery even when uptake matches.]] and [[Similar uptake agreement can coexist with different population recovery, so training error cannot verify populations.]]

Sources: `7_results_omc.tex` L42–60 (TeaA).

## 4 Comparing structural hypotheses

Sources: `7_results_omc.tex` L64–100 (BPTI reweighting), L101–131 (HOIP parameter fitting).

## 5 Population fitting and forward-model calibration

- Protocol. Under an imposed kinetic mismatch, fitting forward-model parameters before reweighting limited population distortion. The advice is conditional on the suspected mismatch, not a general fitting order.
- Kinetic mismatch. In a benchmark with an imposed kinetic mismatch, population changes compensated for incorrect exchange assumptions after calibration restored uptake agreement. Carries [[Fitted populations can compensate for errors in assumed exchange kinetics, and restoring uptake agreement by calibration does not validate kinetics or populations.]]

Sources: `7_results_omc.tex` L132–188 (protocol comparison), L189–211 and L248 (kinetic misspecification).

## 6 Clustering and diagnostic perturbations

- Representation. Clustering to 10 to 20% of the parent ensemble preserved performance, and smaller sets aid interpretation when the conclusion survives a change of cluster size.
- Decoys. Artificial and decoy conformations probe what the BV model can and cannot distinguish.

Sources: `7_results_omc.tex` L235–248 (clustering and limitations).

## 7 Discussion and chapter conclusions

- Boundary, handed to ch. 4 and 5. Conclusions are comparative across the candidates supplied, reweighting cannot add states, and replicate uncertainty does not name its cause.

Sources: `7_results_omc.tex` L235–248 (clustering and limitations).

## Gaps
- Settle median against mean for the consensus BV constants, the peptide dropout wording and the overlap handling (`hard_intersection`) used in each benchmark, before citing [[Peptide splitting and consensus (ValDX)]].
- Confirm whether trajectories were superposed before the dynamical LCC, before porting [[Structural comparison metrics (ValDX)]] to `app:valdx-mathematics`.
