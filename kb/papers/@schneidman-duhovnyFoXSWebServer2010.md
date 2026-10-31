---
type: paper
citekey: schneidman-duhovnyFoXSWebServer2010
year: 2010
read: false
pdf: kb/_pdf/@schneidman-duhovnyFoXSWebServer2010.pdf
extraction: auto
needs_review: false
review_reason:
---

# FoXS: A Web Server for Rapid Computation and Fitting of SAXS Profiles (2010)

## Main point

## Claims

<!-- One bullet per claim, ending in a block ID. page is the 1-based PDF page index.
- The claim paraphrased in one sentence. ^c1
  - page: 1
  - quote: "verbatim text, 5 to 25 words"
  - quote_check: unchecked
  - reviewed: false
quote_check is written only by tools/kb-lint; reviewed only by me. -->
- FoXS computes a SAXS profile from atomic coordinates using the Debye formula, a double sum over all atom pairs of form-factor products weighted by sin(q d_ij)/(q d_ij). ^c1
  - page: 2
  - quote: "The method for computing SAXS profiles is based on the Debye formula"
  - quote_check: pass
  - reviewed: false
- Each atom's form factor in FoXS combines the in-vacuo factor, the displaced-solvent (dummy atom) factor and a hydration-layer factor weighted by the atom's solvent-accessible fraction. ^c2
  - page: 2
  - quote: "takes into account the displaced solvent as well as the hydration layer"
  - quote_check: pass
  - reviewed: false
- The parameter c1 scales the total excluded volume (default 1.0) and c2 scales the water density of the hydration layer (default 0.0). ^c3
  - page: 2
  - quote: "The parameter c1 is used to adjust the total excluded volume of the atoms"
  - quote_check: pass
  - reviewed: false
- The first solvation layer is modelled from the atomic solvent-accessible areas, so hydration depends on the coordinates. ^c4
  - page: 2
  - quote: "models the first solvation layer based on the atomic solvent accessible areas"
  - quote_check: pass
  - reviewed: false
- The computed profile is fitted to the experimental profile by minimising a chi function over a scale factor c and the hydration parameters c1 and c2, each weighted by the experimental error. ^c5
  - page: 2
  - quote: "is fitted to a given experimental SAXS profile by minimizing the function with respect to c, c1 and c2"
  - quote_check: pass
  - reviewed: false
- The fit searches c1 over 0.95 to 1.12 and c2 over 0 to 4.0 on a grid, solving the scale factor c by linear least squares at each grid point. ^c6
  - page: 2
  - quote: "performing the linear least-squares minimization to find the value of c that minimizes"
  - quote_check: pass
  - reviewed: false
- FoXS recommends supplying an accurate error estimate on each intensity because the error is used in the profile fitting. ^c7
  - page: 2
  - quote: "recommended to provide an accurate error estimate"
  - quote_check: pass
  - reviewed: false
- Hydrogen atoms are treated implicitly for proteins by adding their form factors to the bound heavy atom. ^c8
  - page: 2
  - quote: "Hydrogen atoms are considered implicitly for proteins and nucleic acids by adding their form factors to that of their bound heavy atom"
  - quote_check: pass
  - reviewed: false
- CRYSOL, the most popular alternative, calculates the spherically averaged profile by multipole expansion instead of explicit pairwise distances. ^c9
  - page: 1
  - quote: "uses multipole expansion for fast calculation of the spherically averaged scattering"
  - quote_check: pass
  - reviewed: false

## Notation

<!-- Only for sources whose equations a concept uses. One row per symbol the concepts rely on or that clashes with the thesis notation.
| Source | Meaning in this source | Canonical | Note |
|---|---|---|---|
| $E(x)$ | force-field energy | $U(x)$ | |
| $\beta$ | inverse temperature | — | write 1/k_BT |
Canonical is one $symbol$ declared by a concept, or —. Delete this section if unused. -->

## What I use from it

## Disagreements / limitations
