---
type: concept
aliases:
  - experiment-guided diffusion
  - experimental guidance
  - guided generation
  - classifier guidance
  - classifier-free guidance
  - conditional generation
  - force-guided diffusion
  - ExEnDiff
  - ConfDiff
notation:
  - {symbol: '\hat x_0', meaning: 'posterior-mean estimate of the clean structure given a noisy one at diffusion time tau', units: null}
  - {symbol: '\eta', meaning: 'guidance strength', units: null}
sources:
  - "[[@liuExEnDiffExperimentGuidedDiffusion2025#^c1]]"
  - "[[@liuExEnDiffExperimentGuidedDiffusion2025#^c2]]"
  - "[[@liuExEnDiffExperimentGuidedDiffusion2025#^c3]]"
  - "[[@liuExEnDiffExperimentGuidedDiffusion2025#^c4]]"
  - "[[@liuExEnDiffExperimentGuidedDiffusion2025#^c5]]"
  - "[[@liuExEnDiffExperimentGuidedDiffusion2025#^c6]]"
  - "[[@liuExEnDiffExperimentGuidedDiffusion2025#^c7]]"
  - "[[@liuExEnDiffExperimentGuidedDiffusion2025#^c8]]"
  - "[[@liuExEnDiffExperimentGuidedDiffusion2025#^c10]]"
  - "[[@wangProteinConformationGeneration2024#^c1]]"
  - "[[@wangProteinConformationGeneration2024#^c2]]"
  - "[[@wangProteinConformationGeneration2024#^c4]]"
  - "[[@wangProteinConformationGeneration2024#^c6]]"
  - "[[@wangProteinConformationGeneration2024#^c7]]"
  - "[[@wangProteinConformationGeneration2024#^c10]]"
  - "[[@yimDiffusionModelsProtein2024#^c7]]"
---

## Definition

Guided diffusion steers a pretrained [[diffusion model]] at sampling time, without retraining, by adding a term to its score. The added term can be:
- a likelihood of experimental data, as in ExEnDiff;
- a force-field energy, as in ConfDiff.

Conditioning a pretrained unconditional model without retraining was shown earlier for motif scaffolding, by sequential Monte Carlo ([[@yimDiffusionModelsProtein2024#^c7]]).

The motivation is the training data. Samplers trained on the PDB, which mostly holds folded states, give ensembles of limited diversity and can produce unrealistic conformations ([[@liuExEnDiffExperimentGuidedDiffusion2025#^c1]]). The training distribution is not the equilibrium distribution: it holds a few points near energy minima ([[@wangProteinConformationGeneration2024#^c2]]), so unguided samples deviate from equilibrium ([[@wangProteinConformationGeneration2024#^c1]]).

## Equations

$$ \nabla_x \log p_\tau(x \mid s^\text{exp}) = \nabla_x \log p_\tau(x) + \nabla_x \log p_\tau(s^\text{exp} \mid x) $$
^eq-guided-score

Source: [[@liuExEnDiffExperimentGuidedDiffusion2025#^c3]], Eq. (7), p. 9. ExEnDiff writes $\mathbf{x}_t$, $t$ and $\mathbf{y}$. Canonical: $x$, $\tau$, and $s^\text{exp}$ for the vector of measured observables $s_i^\text{exp}$ (notation: [[@liuExEnDiffExperimentGuidedDiffusion2025#Notation]]). The guided score replaces the score in the reverse SDE [[diffusion model#^eq-diffusion-reverse]] (ExEnDiff Eq. 6).

$$ \nabla_x \log p_\tau(s^\text{exp} \mid x) \approx -\nabla_x \sum_i \frac{\left(s_i^\text{exp} - s_i(\hat x_0)\right)^2}{2\sigma_i^2} $$
^eq-guidance-restraint

Source: [[@liuExEnDiffExperimentGuidedDiffusion2025#^c4]] (evaluate at $\hat x_0$, Eqs. 10–11), [[@liuExEnDiffExperimentGuidedDiffusion2025#^c5]] (Gaussian replaces the delta, Eq. 12), [[@liuExEnDiffExperimentGuidedDiffusion2025#^c6]] (harmonic restraint, Eqs. 13–14), p. 9. This is the gradient of the Gaussian in Eq. 12. ExEnDiff's Eq. 13 sets $k_i = 2/\sigma_i^2$, which doubles it; the factor is a known inconsistency in the source (paper note).

$$ P(x) \propto P_0(x)\, e^{-U(x)/k_BT} $$
^eq-energy-tilt

Source: [[@wangProteinConformationGeneration2024#^c4]], Eq. (3), p. 4. ConfDiff writes $p_0(\mathbf{x}_0) = q_0(\mathbf{x}_0) e^{-k\mathcal{E}_0(\mathbf{x}_0)}/Z$ and calls it "the equilibrium distribution". Canonical: $P_0$ is the unguided generator, $U$ the force-field energy. The guided score subtracts $\eta$ times the gradient of an intermediate energy defined on noisy coordinates ([[@wangProteinConformationGeneration2024#^c6]], Eq. 6, p. 5).

## Derivation

1. Eq. ^eq-guided-score is Bayes' theorem for the score: $\log p(x \mid s^\text{exp}) = \log p(x) + \log p(s^\text{exp} \mid x) - \log p(s^\text{exp})$, and the last term has no $x$-gradient ([[Bayes' theorem#^eq-bayes]]; step ours).
2. The likelihood is defined on clean structures, but sampling sees noisy ones, so it has no closed form ([[@liuExEnDiffExperimentGuidedDiffusion2025#^c3]]). ExEnDiff evaluates it at the posterior mean $\hat x_0$ ([[@liuExEnDiffExperimentGuidedDiffusion2025#^c4]]).
3. With a Gaussian likelihood the guidance term is the gradient of a harmonic restraint ([[@liuExEnDiffExperimentGuidedDiffusion2025#^c6]]). That is the form of [[restrained simulation#^eq-replica-restraint]] for a single structure. Eq. ^eq-energy-tilt has the form of the maximum-entropy tilt [[maximum entropy principle#^eq-maxent-posterior]], with energy in place of the Lagrange term (step ours).

## Assumptions and limits

- **The forward model must be differentiable.** The guidance needs $\nabla_x s_i(\hat x_0)$ (ours; ExEnDiff Eq. 13). See [[forward model]].
- **The guidance weight is a choice.** Too weak leaves samples inconsistent with the data; too strong makes the sampling path noisy and the structures unphysical ([[@liuExEnDiffExperimentGuidedDiffusion2025#^c7]]). In ConfDiff, guidance repairs clashes but contracts structures towards local minima ([[@wangProteinConformationGeneration2024#^c10]]).
- **The restraint is on single structures.** Unlike [[restrained simulation]] it restrains each sample, not an ensemble average (ours). Ensemble-averaged data such as HDX uptake therefore do not fit this form directly.
- **No equilibrium guarantee.** ExEnDiff's abstract claims the samples capture the underlying Boltzmann distribution ([[@liuExEnDiffExperimentGuidedDiffusion2025#^c2]]), but the authors concede the method does not give accurate free-energy differences ([[@liuExEnDiffExperimentGuidedDiffusion2025#^c10]]). ConfDiff describes force guidance as "reweighting" ([[@wangProteinConformationGeneration2024#^c7]]), but no importance weights are computed. Its target equals Boltzmann only if the generator's own distribution is flat. Correcting the populations needs [[importance sampling]].
- **Evaluation is weak.** Every ExEnDiff guiding measurement was synthetic, computed from the same MD used as ground truth ([[@liuExEnDiffExperimentGuidedDiffusion2025#^c8]]). Both papers test small proteins only (paper notes).

## Why it matters here

Chapter 2, "Experimental Guidance of Diffusion Models". It reviews existing approaches; the project's own formulation stays in its research chapter. Guidance is the generative counterpart of [[restrained simulation]] and the [[maximum entropy principle]]: a bias added to a learned score instead of a force field.

Claims that use this term: [[Experimental guidance adds the gradient of a data likelihood to a pretrained diffusion score at sampling time.]], [[Guided diffusion samples are not equilibrium-weighted unless a correction such as reweighting is applied.]], [[Diffusion models trained on PDB structures learn a distribution concentrated on folded, low-energy states rather than the equilibrium distribution.]], [[Too strong an experimental guidance term makes diffusion sampling noisy and produces unphysical structures.]].
