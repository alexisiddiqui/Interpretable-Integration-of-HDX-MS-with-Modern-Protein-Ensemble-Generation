---
type: paper
citekey: liuExEnDiffExperimentGuidedDiffusion2025
year: 2025
read: false
pdf: kb/_pdf/@liuExEnDiffExperimentGuidedDiffusion2025.pdf
extraction: auto
needs_review: false
review_reason:
---

# ExEnDiff: An Experiment-Guided Diffusion Model for Protein Conformational Ensemble Generation (2025)

## Main point

ExEnDiff steers a pretrained diffusion ensemble sampler (Str2Str) with experimental observables at inference time, without retraining. The guided score is the pretrained score plus a likelihood gradient. That gradient is approximated by a harmonic restraint between the measurement and the forward model applied to the posterior-mean clean structure. Guidance by end-to-end distance, radius of gyration and per-residue helicity improved agreement with long MD on two fast folders and eight IDPs, but every guiding measurement was synthetic and taken from that same MD.

## Claims

<!-- One bullet per claim, ending in a block ID. page is the 1-based PDF page index.
- The claim paraphrased in one sentence. ^c1
  - page: 1
  - quote: "verbatim text, 5 to 25 words"
  - quote_check: unchecked
  - reviewed: false
quote_check is written only by tools/kb-lint; reviewed only by me. -->
- Diffusion samplers trained on the PDB, which mostly holds folded states, generate ensembles of limited diversity and can produce physically unrealistic conformations. ^c1
  - page: 1
  - quote: "which primarily captures folded protein states, restricts the diversity of the generated ensembles and can result in physically unrealistic conformations"
  - quote_check: pass
  - reviewed: false
- The abstract claims that experiment-guided sampling captures configuration properties and the underlying Boltzmann distribution. ^c2
  - page: 1
  - quote: "configuration properties and the underlying Boltzmann distribution, paving the way for a next-generation molecular dynamics engine"
  - quote_check: pass
  - reviewed: false
- The guided score splits by Bayes' rule into the prior score and a likelihood gradient, but that gradient has no closed form because the data depend on the noisy coordinates only implicitly (Eqs. 6 and 7). ^c3
  - page: 9
  - quote: "is challenging due to the implicit dependency between y and xt"
  - quote_check: pass
  - reviewed: false
- The likelihood on noisy coordinates is approximated by evaluating it at the posterior-mean estimate of the clean structure, computed from the learned score (Eqs. 10 and 11). ^c4
  - page: 9
  - quote: "is the posterior mean estimate given by"
  - quote_check: pass
  - reviewed: false
- The exact likelihood is a Dirac delta on the forward-model output, which is replaced by a small-variance Gaussian for numerical stability (Eq. 12). ^c5
  - page: 9
  - quote: "In practice, to guarantee numerical stability, we approximate this function with a Gaussian distribution of small variance"
  - quote_check: pass
  - reviewed: false
- The likelihood gradient then becomes the gradient of a harmonic restraint, which is added to the pretrained score at inference time (Eqs. 13 and 14). ^c6
  - page: 9
  - quote: "the posterior term can be estimated with a harmonic restraint potential function"
  - quote_check: pass
  - reviewed: false
- Too small a restraint weight leaves samples inconsistent with the data, and too large a weight makes the sampling path noisy and the structures unphysical. ^c7
  - page: 10
  - quote: "an overly high weight will make the sampling path noisy and thus generate unphysical configurations"
  - quote_check: pass
  - reviewed: false
- All guiding measurements in the study were synthetic, computed from the ground-truth MD simulations. ^c8
  - page: 5
  - quote: "all experimental measurements used to guide the protein ensemble generation process in this study are synthetically derived from ground-truth MD simulations"
  - quote_check: pass
  - reviewed: false
- Success was scored by the discrepancy between observables from the generated ensembles and from ground-truth MD simulations. ^c9
  - page: 3
  - quote: "This score is calculated based on the discrepancy between the observables produced by the samplers and those from ground-truth MD simulations"
  - quote_check: pass
  - reviewed: false
- The authors concede that the method does not directly produce metastable states with accurate free-energy differences. ^c10
  - page: 8
  - quote: "it does not directly produce metastable states with highly accurate free energy differences"
  - quote_check: pass
  - reviewed: false

## Notation

| Source | Meaning in this source | Canonical | Note |
|---|---|---|---|
| $t$ | diffusion time, $t \in [0,T]$ | $\tau$ | $t$ is labelling time |
| $\mathbf{x}_t$ | noisy coordinates at diffusion time $t$ | — | bold in source |
| $\nabla_{\mathbf{x}_t} \log p_t(\mathbf{x}_t)$ | score of the marginal density | $\nabla_x \log p_\tau(x)$ | Eq. 7 writes $p_t(\mathbf{x}_t, t)$ |
| $\mathbf{s}_\theta(\mathbf{x}_t, t)$ | pretrained score network | — | write $\hat\nabla_x \log p_\tau(x)$, as for Yim |
| $\mathbf{y} = [y_1, \dots, y_m]$ | measured observables, $m$ one-dimensional features | $s^\text{exp}$ | synthetic from MD in every test |
| $A(\mathbf{x}_0)$, $A_i(\mathbf{x}_0)$ | forward model from clean structure to observable | $s_i(x)$ | calligraphic $\mathcal{A}$ in Eq. 12 |
| $\hat{\mathbf{x}}_0 = \mathbb{E}[\mathbf{x}_0 \mid \mathbf{x}_t]$ | posterior-mean estimate of the clean structure (Eq. 11) | — | |
| $\sigma$, $\sigma_i$ | standard deviation of the Gaussian likelihood | $\sigma_i$ | sets restraint strength, not measured error |
| $\mathbf{k} = [k_1, \dots, k_i]$ | restraint constants, $k_i = 2/\sigma_i^2$ | — | renormalised by the residual in practice (p. 10) |
| $\mathbf{s}_\text{rest}(\mathbf{x}_t, t)$ | guided (restrained) score (Eq. 14) | — | |
| $\beta(t)$, $\bar\alpha_t$ | DDPM variance schedule and its cumulative product | — | $\beta$ is not inverse temperature |

## What I use from it

Chapter 2, "Experimental Guidance of Diffusion Models":
- Guided score as prior score plus likelihood gradient, with the intractable likelihood on noisy coordinates (^c3). Eqs. 6, 7 and 14 on p. 9 are the cleanest displayed form of [[guided diffusion]] with experimental data.
- Handling the noisy intermediate by a posterior-mean plug-in (^c4) and a Gaussian surrogate for a Dirac-delta [[forward model]] likelihood (^c5, ^c6). The forward model is differentiated through $\hat{\mathbf{x}}_0$, so it has to be differentiable (our reading; the paper does not say so).
- Guidance strength trade-off and unphysical structures (^c7).
- Motivation, the PDB bias of [[diffusion model]] ensemble samplers (^c1).
- Equilibrium claims to set against the evaluation (^c2, ^c8, ^c9, ^c10); contrast with [[importance sampling]] and the [[maximum entropy principle]], which correct populations explicitly.

## Disagreements / limitations

- **Boltzmann claim without correction.** The abstract claims the samples capture "the underlying Boltzmann distribution" (^c2). No reweighting or acceptance step corrects the guided samples, and the method matches measurement distributions, not the [[Boltzmann distribution]]. The authors concede it does not give accurate free-energy differences between metastable states (^c10).
- **Circular, synthetic evaluation.** Every guiding measurement was computed from the ground-truth MD (^c8), and success was scored against that same MD (^c9). Real data enter only as a preliminary supplementary discussion.
- **Distributions assumed known.** The method samples targets from a measurement distribution; "In all experiments of this paper, we assume the ground-truth probability distribution" of the observables is exactly known (p. 10). Ensemble averages, as from HDX-MS, are turned into a Gaussian of hand-set variance.
- **Processed, low-dimensional observables.** Guidance used end-to-end distance, radius of gyration and helicity, which are derived quantities. The authors note that raw data would be more informative (p. 8). The harmonic restraint also "ignores covariance between dimensions" (p. 8).
- **Unphysical structures.** A mischosen restraint "may generate unphysical protein configurations with bond breaks" (p. 10), patched with an extra 3.8 Å Cα–Cα restraint. The restraint constant is renormalised by the residual and tuned per operator.
- **Factor of two.** Eq. 12 gives $U_\text{cons} = \|\mathbf{y} - \mathcal{A}(\hat{\mathbf{x}}_0)\|_2^2 / 2\sigma^2$, whose gradient carries $1/2\sigma^2$, but Eq. 13 with $k_i = 2/\sigma_i^2$ gives $1/\sigma^2$. Cite the form of Eq. 14, not its constant.
- **Scale.** Systems were 24 to 234 residues, with 100 samples each.
