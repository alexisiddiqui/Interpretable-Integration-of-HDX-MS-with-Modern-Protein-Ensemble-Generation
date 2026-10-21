---
type: paper
citekey: nguyenReferenceParametersProtein2018
year: 2018
read: false
pdf: kb/_pdf/@nguyenReferenceParametersProtein2018.pdf
extraction: auto
needs_review: true
review_reason: "The jaxENT SI (si_figures.tex L225) cites wuConformationalHeterogeneitySavinase2020 for the Nguyen et al. reference parameters; it should cite this paper."
---

# Reference Parameters for Protein Hydrogen Exchange Rates (2018)

## Main point

A short application note that makes minor adjustments to the Bai et al. (1993) and Connelly et al. (1993) intrinsic exchange parameters. The Ala-Ala reference rate is raised by a factor of 1.35 and the left-neighbour factors for deprotonated Asp and Glu and for Gly are revised, and the adjusted set is tested against HX-MS data on unstructured apolipoprotein C3.

## Claims

- Raising the previously used Ala-Ala reference rate by a factor of 1.35 brings the predicted exchange into agreement with HX-MS data for unstructured apolipoprotein C3; Table 1 gives the Connelly et al. reference parameters with this adjustment, corrected to 20 °C. ^c1
  - page: 2
  - quote: "of the reference rate previously used by the small factor of 1.35 brings the predicted rate into excellent agreement with the apoC3 data"
  - quote_check: pass
  - reviewed: false
- In calculating pD for samples in 90% D2O, the authors added 0.36 to the pH meter reading instead of the usual 0.40. ^c2
  - page: 2
  - quote: "In calculating pD, we added 0.36 to the pH meter reading rather than 0.40 [12] to account for the 90% D2O present."
  - quote_check: pass
  - reviewed: false
- The note does not restate the temperature correction; detailed methods for computing free-peptide rates, including temperature effects, are deferred to Bai et al. and Connelly et al. ^c3
  - page: 4
  - quote: "Detailed methods for calculating free peptide HX rates using these parameters including temperature effects are given in Bai et al."
  - quote_check: pass
  - reviewed: false
- Relative to the Bai et al. factors, and in the context of the revised alanine reference rate, the left-neighbour (L) effect of deprotonated Glu and Asp should be 1.85-fold faster and that of Gly 2.0-fold slower (Table 2). ^c4
  - page: 2
  - quote: "the L effect of deprotonated Glu and Asp should be faster by a factor of 1.85 and Gly slower by a factor of 2.0"
  - quote_check: pass
  - reviewed: false
- Apart from short peptides affected by His18, the average deviation between predicted and measured apoC3 exchange with the adjusted parameters is 7%. ^c5
  - page: 2
  - quote: "the average deviation is very small, 7%"
  - quote_check: pass
  - reviewed: false

## What I use from it

The current reference values for intrinsic exchange rates (Ala-Ala rate ×1.35 and the revised Asp, Glu and Gly neighbour factors) and the pD correction for 90% D2O, cited wherever the thesis computes k_int.

## Disagreements / limitations

The adjusted reference rate is calibrated on one unstructured protein at pD_read 4.10 and 5 °C; the authors note that disordered regions of real proteins can still show low-level protection.
