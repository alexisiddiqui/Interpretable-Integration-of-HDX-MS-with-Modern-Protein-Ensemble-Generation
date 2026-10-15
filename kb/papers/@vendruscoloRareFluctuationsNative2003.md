---
type: paper
citekey: vendruscoloRareFluctuationsNative2003
year: 2003
read: false
pdf: kb/_pdf/@vendruscoloRareFluctuationsNative2003.pdf
extraction: auto
needs_review: false
review_reason:
---

# Rare Fluctuations of Native Proteins Sampled by Equilibrium Hydrogen Exchange (2003)

## Main point

Protection factors are modelled phenomenologically as ln P = βc·Nc + βh·Nh (contacts and amide hydrogen bonds), averaged over replicas, and used as restraints in Monte Carlo sampling. Applied to native α-lactalbumin, this gives an ensemble of rarely populated, partly unfolded structures (mean rmsd about 4 Å) that account for the measured exchange.

## Claims

- Equilibrium hydrogen exchange is used to determine the structures populated during the rare fluctuations of the native state that exchange requires. ^c1
  - page: 1
  - quote: "determine the structures of species populated during the rare fluctuations of the native state that are required for the exchange"
  - quote_check: pass
  - reviewed: false
- Under the EX2 (local unfolding) mechanism, the free energy difference between a fully closed and a fully open state of residue i is ΔG_HX = RT ln P_i. ^c2
  - page: 1
  - quote: "The experimental free energy difference between a fully closed state (no hydrogen exchange) and a fully open state"
  - quote_check: pass
  - reviewed: false
- The ensemble is obtained by Monte Carlo sampling biased by experimental protection factors, with a pseudo-energy on the squared difference between replica-averaged ln P_sim and ln P_exp (M = 10 replicas). ^c3
  - page: 1
  - quote: "The method is based on an exploration of conformational space using Monte Carlo sampling biased by experimental data."
  - quote_check: pass
  - reviewed: false
- Protection factors are the ratios of amide exchange rates in unstructured polypeptides to those of the same residues in the native protein. ^c4
  - page: 1
  - quote: "which represent the ratios of the exchange rates of amide hydrogens in unstructured polypeptides to those of the same residues in the native protein"
  - quote_check: pass
  - reviewed: false
- Equilibrium protection factors are a property of a Boltzmann ensemble, so no single conformation is expected to satisfy all of them; the calculated values are therefore averaged over replicas. ^c5
  - page: 1
  - quote: "Equilibrium protection factors are a property of a Boltzmann ensemble of conformations, and no single conformation is required"
  - quote_check: pass
  - reviewed: false
- Fitting native structures of six proteins gave βc = 1 and βh = 5 (correlation 0.91); contacts alone or hydrogen bonds alone gave correlations of only 0.5 and 0.4, so both terms are needed. ^c6
  - page: 1
  - quote: "These results indicate that the nonbonded contacts and hydrogen-bonding terms are both required for a meaningful analysis of the protection factors."
  - quote_check: pass
  - reviewed: false
- Rarely populated unfolded conformations are sampled at equilibrium, and HX is described as unique in reporting on them because they are needed for exchange of otherwise solvent-inaccessible amides. ^c7
  - page: 2
  - quote: "HX techniques are unique in providing information concerning such species"
  - quote_check: pass
  - reviewed: false

## What I use from it

The origin of the contact-plus-hydrogen-bond protection-factor model (βc = 1, βh = 5) used as the HDX forward model, its statement that ΔG = RT ln P under EX2, and its argument that protection factors are ensemble averages and are best used as restraints on an ensemble.

## Disagreements / limitations

The model is phenomenological and coarse-grained (main chain plus Cβ, hard-sphere sterics). The fit uses native crystal structures, and the α-lactalbumin correlation (0.80, or 0.89 without Thr86 and Asp87) depends on excluding Ca2+ contributions.
