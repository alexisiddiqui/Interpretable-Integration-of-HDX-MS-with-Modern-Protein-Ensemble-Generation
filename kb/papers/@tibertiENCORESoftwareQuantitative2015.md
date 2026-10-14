---
type: paper
citekey: tibertiENCORESoftwareQuantitative2015
year: 2015
read: false
pdf: kb/_pdf/@tibertiENCORESoftwareQuantitative2015.pdf
extraction: manual
needs_review: false
review_reason:
---

# ENCORE: Software for Quantitative Ensemble Comparison (2015)

The PDF is the publisher's open-access version (PLoS Comput Biol 11(10): e1004415), not a Zotero copy, and the paper still has to be added to Zotero.

## Main point

ENCORE is an MDAnalysis-based implementation of the three ensemble similarity scores of Lindorff-Larsen and Ferkinghoff-Borg (2009). Each estimates a probability distribution from an ensemble and compares distributions with a symmetrised Kullback–Leibler divergence. HES fits a multivariate normal, CES uses cluster populations from Affinity Propagation, and DRES uses kernel densities in a Stochastic Proximity Embedding. The examples compare force fields, track simulation convergence and compare NMR-refined ubiquitin ensembles, and the scores are best read relative to one another.

## Claims

<!-- One bullet per claim, ending in a block ID. page is the 1-based PDF page index.
- The claim paraphrased in one sentence. ^c1
  - page: 1
  - quote: "verbatim text, 5 to 25 words"
  - quote_check: unchecked
  - reviewed: false
quote_check is written only by tools/kb-lint; reviewed only by me. -->
- Once a state is represented by an ensemble, comparing states means comparing ensembles rather than single conformations. ^c1
  - page: 2
  - quote: "comparing molecular states now becomes a question of comparing structural ensembles, rather than individual conformations"
  - quote_check: pass
  - reviewed: false
- All three ENCORE methods compare the distributions estimated from ensembles with symmetrised versions of the Kullback–Leibler divergence. ^c2
  - page: 3
  - quote: "quantify the similarity of two derived probability distributions using symmetrized versions of the Kullback-Leibler divergence measure"
  - quote_check: pass
  - reviewed: false
- The three methods differ mainly in how the probability distributions are derived from the ensembles. ^c3
  - page: 3
  - quote: "which mostly differ in how the probability distributions are derived"
  - quote_check: pass
  - reviewed: false
- A harmonic assumption may be justified for molecules with only small structural fluctuations. ^c4
  - page: 3
  - quote: "For molecules undergoing minor structural fluctuations, a harmonic assumption might be justified"
  - quote_check: pass
  - reviewed: false
- The Jensen–Shannon divergence used by CES and DRES takes values between zero and ln 2. ^c5
  - page: 6
  - quote: "the Jensen-Shannon divergence used in DRES and CES may take on values between zero and ln(2)"
  - quote_check: pass
  - reviewed: false
- Because the scores compare equilibrium distributions, changes in dynamics or in transition rates between states are not captured. ^c6
  - page: 6
  - quote: "(e.g. changes in the dynamics or rates of transitions between states) will not be captured"
  - quote_check: pass
  - reviewed: false
- PCA-based overlap measures such as the root mean square inner product are less directly affected by how conformations are distributed within the spanned space. ^c7
  - page: 7
  - quote: "such methods are less directly affected by variations in the distributions of conformations within these spaces"
  - quote_check: pass
  - reviewed: false
- Some ensembles are only approximately normal, which may explain why HES disagrees in part with the clustering and projection scores. ^c8
  - page: 7
  - quote: "one can only approximately describe these ensembles as normally distributed, which can explain some of the differences between the harmonic ensemble similarity method"
  - quote_check: pass
  - reviewed: false
- For intrinsically disordered proteins, a similarity score other than RMSD may be more appropriate. ^c9
  - page: 13
  - quote: "for intrinsically disordered proteins it may, however, be more appropriate to use other similarity scores than the RMSD"
  - quote_check: pass
  - reviewed: false
- Because the scores lack a simple geometric interpretation, the authors suggest reading them in a relative way for now. ^c10
  - page: 13
  - quote: "as it is difficult to provide a simple geometric interpretation of the scores, we suggest they are currently best interpreted in a relative fashion"
  - quote_check: pass
  - reviewed: false

## What I use from it

- The framing that ensemble states call for ensemble comparison (^c1). [[ensemble comparison]]
- The shared recipe and the three density estimates, in a citable software form (^c2, ^c3). [[Kullback–Leibler divergence]], [[clustering]]
- Limits for the Chapter 2 section: harmonic only for small fluctuations (^c4, ^c8); JSD is bounded by ln 2 while HES can in principle reach infinity (p. 6), so their scales differ (^c5); equilibrium-only, so kinetics are invisible (^c6); and PCA overlap can hide population differences (^c7).
- The RMSD dependence of CES and DRES (^c9) and the advice to read scores relatively (^c10) support reporting interpretable, relative comparisons rather than absolute divergences.

## Disagreements / limitations

- The paper has no displayed equations. It refers back to Lindorff-Larsen and Ferkinghoff-Borg (2009) for the definitions, so equations should be cited from there.
- No per-residue measure such as RMSF is offered, and the scores are global.
- CES and DRES need the full pairwise RMSD matrix. The authors call this the main bottleneck and found it "prohibitively costly for large ensembles" before parallelising (p. 11).
- The bootstrap uncertainties (average relative error 6%, maximum 19%, p. 7) are for 1000-frame subsamples of 10 μs simulations. Relative error grew about 3.6-fold for ten times smaller ensembles, which matters for small, clustered HDX ensembles.
- The CES clustering resolution is a user setting (the Affinity Propagation preference), and the paper does not test how the force-field ranking changes with it.
