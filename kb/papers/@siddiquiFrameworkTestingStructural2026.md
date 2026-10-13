---
type: paper
citekey: siddiquiFrameworkTestingStructural2026
year: 2026
read: false
pdf: kb/_pdf/@siddiquiFrameworkTestingStructural2026.pdf
extraction: manual
needs_review: false
review_reason:
---

# A Framework for Testing Structural Hypotheses of Protein Dynamics against Experimental HDX-MS Data (2026)

ValDX preprint (bioRxiv, version posted 4 March 2026; doi 10.64898/2026.03.02.709114). The jaxENT manuscript cites it as `Siddiqui2026.03.02.709114`. Quotes and pages are from the posted v1 PDF, not from the revised manuscript in `projects/1-ValDX/manuscript/report/` (`main_omc.pdf`, October 2026).

## Main point

Agreement with HDX-MS uptake does not show that a fitted ensemble has the right populations. ValDX tests ensembles as structural hypotheses with three tools:
- overlap-aware data splitting;
- replicate fits;
- "Work Done" metrics, which measure how much the ensemble had to change to match experiment.

In the TeaA Iso-Validation benchmark, training error fails to tell correct ensembles from incorrect ones. Clustering gives compact, interpretable ensembles.

## Claims

<!-- One bullet per claim, ending in a block ID. page is the 1-based PDF page index.
- The claim paraphrased in one sentence. ^c1
  - page: 1
  - quote: "verbatim text, 5 to 25 words"
  - quote_check: unchecked
  - reviewed: false
quote_check is written only by tools/kb-lint; reviewed only by me. -->
- Because uptake is averaged over peptides, one uptake curve has many possible structural explanations. ^c1
  - page: 2
  - quote: "a single uptake curve can arise from many different underlying structural scenarios"
  - quote_check: pass
  - reviewed: false
- In the TeaA benchmark, ensembles with similar training error differed in population recovery, so uptake agreement alone cannot verify populations. ^c2
  - page: 12
  - quote: "uptake agreement alone cannot verify population recovery"
  - quote_check: pass
  - reviewed: false
- With intermediate structures present, open-state recovery stayed below the 40% target for three of four split types despite low training error. ^c3
  - page: 12
  - quote: "Open State Recovery struggled to exceed 40% for three of four split-types despite achieving low training error"
  - quote_check: pass
  - reviewed: false
- Plausible intermediate conformations absent from the target ensemble prevented population recovery even when uptake matched. ^c4
  - page: 12
  - quote: "The presence of intermediate structures, plausible conformations absent from the true ensemble, prevented accurate population recovery even when uptake curves matched experimental targets"
  - quote_check: pass
  - reviewed: false
- An ensemble of incorrect structures can reach low training error through the flexibility of the fit. ^c5
  - page: 3
  - quote: "An ensemble containing entirely incorrect structures can achieve low training error simply by exploiting the flexibility of the fitting procedure"
  - quote_check: pass
  - reviewed: false
- Experimental agreement alone cannot separate a representative ensemble from one forced into agreement by overfitting. ^c6
  - page: 6
  - quote: "experimental agreement alone cannot distinguish an ensemble that genuinely represents solution-state dynamics from one that has been forced into agreement through overfitting"
  - quote_check: pass
  - reviewed: false
- The BV parameters mainly compensate for differences between the experimental conditions and those the model was calibrated under. ^c7
  - page: 6
  - quote: "These parameters primarily compensate for systematic differences between experimental conditions (pH, temperature, quench efficiency) and the conditions under which"
  - quote_check: pass
  - reviewed: false
- Because peptides overlap, a random split puts peptides in the validation set whose uptake is predictable from training peptides. ^c8
  - page: 5
  - quote: "a random split will include peptides in the validation set whose uptake is predictable from training peptides covering similar regions"
  - quote_check: pass
  - reviewed: false
- Work Done metrics quantify how much an ensemble must be modified to match experiment. ^c9
  - page: 2
  - quote: "quantify how much an ensemble must be modified to match experiment"
  - quote_check: pass
  - reviewed: false
- v1 reads small Work Done as a sign that the ensemble was already representative. The revised manuscript qualifies this (`7_results_omc.tex` L12). ^c10
  - page: 4
  - quote: "when small adjustments suffice, this suggests the ensemble was already representative of solution behaviour"
  - quote_check: pass
  - reviewed: false
- Low validation error with high Work Done means agreement was reached by excessive modification, a signature of overfitting. ^c11
  - page: 8
  - quote: "When low validation error accompanies high Work Done, the ensemble achieved experimental agreement through excessive modification"
  - quote_check: pass
  - reviewed: false
- Fitting outcomes depend on which peptides and time points are used; replicate fits quantify this. ^c12
  - page: 44
  - quote: "Optimisation outcomes depend strongly on which peptides and time points are used for fitting; replicates quantify this uncertainty"
  - quote_check: pass
  - reviewed: false
- Clustering gives compact, interpretable ensembles with little loss of accuracy. ^c13
  - page: 2
  - quote: "clustering yields compact, interpretable ensembles with minimal loss of accuracy"
  - quote_check: pass
  - reviewed: false
- ValDX frames HDX-MS ensemble integration as structural hypothesis testing. ^c14
  - page: 2
  - quote: "establishes HDX-MS ensemble integration as a quantitative structural hypothesis-testing problem"
  - quote_check: pass
  - reviewed: false
- A Work Done pattern pointing to calibration mismatch calls for recalibrating the model before rejecting the ensemble. ^c15
  - page: 7
  - quote: "model parameter recalibration should be considered before rejecting the ensemble hypothesis"
  - quote_check: pass
  - reviewed: false

## What I use from it

Introduction §1.5 is built on this paper:
- non-uniqueness (^c1);
- candidate coverage and decoys (^c2–^c4);
- compensation by forward-model parameters (^c7, ^c15);
- overfitting and leakage (^c5, ^c6, ^c8);
- Work Done (^c9, ^c11);
- replicates and clustering (^c12, ^c13);
- the hypothesis-testing framing (^c14).

Concepts: [[overfitting]], [[data splitting]], [[Work Done]], [[model misspecification]], [[replicate uncertainty]], [[sampling coverage]].

## Disagreements / limitations

The revised manuscript (October 2026) differs from v1 on several points that §1.5 relies on. Until a revised version is posted, these stay draft with manuscript origins:
- **Kinetic misspecification:** v1 has no such benchmark (`7_results_omc.tex` L189–211, L248).
- **Splits:** v1 says structured splits "ensure that validation error reflects true predictive performance" and give "genuinely withheld" regions. The revision says they reduce dependence "without guaranteeing statistical independence" (`1_introduction_omc.tex` L37).
- **Work Done:** v1 reads small Work Done as representative (^c10) and says Work Done allows "precise statements" about hypotheses. The revision says it measures distance from the prior, not to the truth (`7_results_omc.tex` L12).
- **Causes of failure:** the revision says the causes of failure are "not fully separable" (`7_results_omc.tex` L242).
- **Clustering:** the revision says conclusions need checking across cluster sizes (`7_results_omc.tex` L235).
