---
type: paper
citekey: bradshawInterpretationHDXData2020
year: 2020
read: false
pdf: kb/_pdf/@bradshawInterpretationHDXData2020.pdf
extraction: auto
needs_review: false
review_reason:
---

# Interpretation of HDX Data by Maximum-Entropy Reweighting of Simulated Structural Ensembles (2020)

## Main point

## Claims

<!-- One bullet per claim, ending in a block ID. page is the 1-based PDF page index.
- The claim paraphrased in one sentence. ^c1
  - page: 1
  - quote: "verbatim text, 5 to 25 words"
  - quote_check: unchecked
  - reviewed: false
quote_check is written only by tools/kb-lint; reviewed only by me. -->
- In the HDXer approach an ensemble of protein conformations is first generated, typically by molecular dynamics simulations. ^c1
  - page: 2
  - quote: "an ensemble of protein conformations is first generated, typically using molecular dynamics simulations"
  - quote_check: pass
  - reviewed: false
- HDXer provides a quantitative metric by which candidate structural ensembles can be ranked on their correspondence with target data, or shown to be inadequate. ^c2
  - page: 2
  - quote: "a quantitative metric with which candidate structural ensembles can be ranked based on their correspondence with target data, or revealed to be inadequate"
  - quote_check: pass
  - reviewed: false
- The mechanistic implications of HDX-MS observations are frequently difficult to interpret because of the technique's limited spatial resolution. ^c3
  - page: 3
  - quote: "the mechanistic implications of HDX-MS observations are frequently difficult to interpret, due to the limited spatial resolution of the technique"
  - quote_check: pass
  - reviewed: false
- The major challenge has been how to objectively translate HDX data into structural information. ^c4
  - page: 22
  - quote: "The major challenge, however, has been how to objectively translate the HDX data into structural information"
  - quote_check: pass
  - reviewed: false
- HDX-MS experiments measure deuteration averaged over peptide fragments rather than at single-residue level. ^c5
  - page: 5
  - quote: "In practice, HDX-MS experiments measure deuteration averaged over lengthy peptide fragments rather than at the single-residue level"
  - quote_check: pass
  - reviewed: false
- HDX data reflect the properties of an ensemble of conformations and might not be explained by a single structural state. ^c6
  - page: 5
  - quote: "HDX data reflect the properties of an ensemble of protein conformations and in some cases, therefore, might not be explained by a single structural state"
  - quote_check: pass
  - reviewed: false
- A reweighting method must up-weight the configurations most consistent with the data and down-weight those that are not. ^c7
  - page: 13
  - quote: "detect and up-weight the protein configurations that are most consistent with the data, but also to detect and down-weight those that are not"
  - quote_check: pass
  - reviewed: false
- There is no guarantee a priori that an observed set of HDX-MS peptides contains enough information for a clear structural interpretation. ^c8
  - page: 22
  - quote: "a priori there is no guarantee that an observed set of peptides will contain sufficient information to allow a clear structural interpretation"
  - quote_check: pass
  - reviewed: false
- HDXer calculates residue protection factors with the method of Best and Vendruscolo. ^c9
  - page: 7
  - quote: "using the method of Best and Vendruscolo"
  - quote_check: pass
  - reviewed: false
- To predict deuterium uptake from structural snapshots, HDXer first calculates the protection factor for each residue. ^c10
  - page: 7
  - quote: "To predict deuterium uptake based on structural snapshots (obtained from MD simulations or other molecular modeling method), we first calculate the protection factor"
  - quote_check: pass
  - reviewed: false
- Apparent work W_app is related to the Kullback-Leibler divergence between the initial and corrected ensembles, D_KL = W_app / k_e T. ^c11
  - page: 9
  - quote: "is related to the Kullback-Leibler divergence between the initial and corrected ensembles"
  - quote_check: pass
  - reviewed: false
- In the BV model, the free-energy difference between exchange-competent and non-competent states is a linear function of H-bond and contact counts (Eq. 1). ^c12
  - page: 7
  - quote: "the free-energy difference between exchange-competent and non-competent states of a residue is approximated by a linear function"
  - quote_check: pass
  - reviewed: false
- The optimal BV scaling factors depend on the protein or experimental conditions. ^c13
  - page: 7
  - quote: "their optimal value depends on the protein or experimental conditions"
  - quote_check: pass
  - reviewed: false
- Peptide deuterated fractions are computed from each residue's exchange rate constants with first-order kinetics (Eq. 2). ^c14
  - page: 7
  - quote: "using the exchange rate constants of each individual residue and according to first-order kinetics"
  - quote_check: pass
  - reviewed: false
- The first residue of each peptide is omitted because its N-terminal hydrogens are labile after digestion. ^c15
  - page: 7
  - quote: "hydrogens in the amine N-terminus are labile after proteolytic fragmentation"
  - quote_check: pass
  - reviewed: false
- Corrections for D2O fraction and back-exchange are made by normalising to maximally deuterated controls. ^c16
  - page: 8
  - quote: "Both corrections can be achieved by normalizing to deuterated fractions observed in identical control experiments performed under maximal deuteration conditions"
  - quote_check: pass
  - reviewed: false
- The minimal bias that corrects the mean of observables is a linear function of those observables added to the energy (Eq. 3). ^c17
  - page: 8
  - quote: "the minimal bias needed to correct the mean value of one or more observables of interest is provided by a linear function of those observables"
  - quote_check: pass
  - reviewed: false
- The weight adjustments are a Boltzmann factor of the linear bias term (Eq. 4). ^c18
  - page: 8
  - quote: "are therefore simply a Boltzmann factor of the linear term of Eq. 3"
  - quote_check: pass
  - reviewed: false
- The optimal multipliers minimise a Kullback-Leibler likelihood function (Eq. 5). ^c19
  - page: 8
  - quote: "is at the global minimum of the following (Kullback-Leibler) likelihood function"
  - quote_check: pass
  - reviewed: false

## What I use from it

## Disagreements / limitations
