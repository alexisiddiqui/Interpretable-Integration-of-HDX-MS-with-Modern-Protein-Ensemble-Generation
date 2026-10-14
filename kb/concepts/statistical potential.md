---
type: concept
aliases:
  - statistical potentials
  - statistical energy
  - learned energy
  - implied energy
notation:
  - {symbol: 'p_\text{model}(x)', meaning: 'probability density over conformations defined by a statistical or learned model', units: null}
  - {symbol: 'E_\text{stat}(x)', meaning: 'statistical potential of conformation x, -k_BT ln p_model(x) up to a constant', units: 'kJ mol^-1'}
sources:
  - "[[@bmsb2012ch1#^c8]]"
  - "[[@bmsb2012ch2#^c2]]"
  - "[[@bmsb2012ch3#^c14]]"
  - "[[@bmsb2012ch4#^c5]]"
---

## Definition

A statistical potential is the energy-like quantity obtained by writing a probability density in Boltzmann form. Any probability distribution can be cast this way ([[@bmsb2012ch1#^c8]], p. 29), by defining a suitable energy ([[@bmsb2012ch2#^c2]], Eq. 2.3, p. 3). For a model that assigns a density $p_\text{model}(x)$ to conformations, the statistical potential is minus $k_BT$ times its logarithm. Low statistical potential means high model probability, and nothing more.

The model can be empirical or learned. A [[knowledge-based potential]] is the special case built from counts in a structure database against a reference state. A generator such as a [[diffusion model]] or a [[Boltzmann generator]] defines one implicitly through its sampling distribution.

## Equations

$$ E_\text{stat}(x) = -k_BT \ln p_\text{model}(x) + \text{const} $$
^eq-statistical-potential

Source: [[@bmsb2012ch1#^c8]], p. 29 (unnumbered); [[@bmsb2012ch2#^c2]], Eq. (2.3), p. 3. Step 3 of [[Boltzmann distribution]] gives the same inversion. The constant is $-k_BT \ln Z$ for a normalised density and can be dropped when only differences between conformations are compared.

## Assumptions and limits

- **Not a physical energy.** Writing a density as an energy does not make it a free energy or potential of mean force. Knowledge-based potentials are in general neither ([[@bmsb2012ch3#^c14]], p. 28), and the reference ratio method explains them as statistical constructs ([[@bmsb2012ch4#^c5]]). $E_\text{stat}$ coincides with the physical $U(x)$ only if $p_\text{model}$ is the equilibrium distribution of the true [[force field]] (ours).
- **It needs a density.** AlphaFold2 returns structures and confidence scores, not a normalised density over conformations. ValDX's phrase "AF2 generates structures according to a statistical potential" (`projects/1-ValDX/manuscript/report/6_methods_omc.tex` L176) is therefore an analogy. It holds as a description of learned, data-derived preferences, but no $E_\text{stat}$ can be computed from AF2 output (ours).
- **Confidence is not $E_\text{stat}$.** pLDDT measures expected accuracy and is not a free energy ([[protein structure predictor]]).
- **A score is not a density.** A diffusion model learns $\nabla_x \log p_\tau(x)$, the gradient of the log density ([[diffusion model]]). Differences in $E_\text{stat}$ need the density itself, which requires integration or a model with tractable likelihood.
- **Population follows the model, not the protein.** Sampling frequencies from a generator reflect $p_\text{model}$. They are a prior to be checked against experiment, not equilibrium populations ([[importance sampling]]).

## Why it matters here

Chapter 2, "Learned Structure Predictors and Ensemble Generators", answers the `.tex` stub "Discuss statistical potentials where relevant" (`thesis/chapters/02-background.tex` L41). The term lets the thesis say what learned generators share with physics-based models (a preference over conformations that can be written as an energy) and where they differ (no defined reference, no guarantee of equilibrium). That is why their ensembles enter reweighting as priors.

Claims that use this term: [[A knowledge-based potential is not a thermodynamic free energy unless its probabilistic model and reference distribution are defined.]], [[A generator's sampling distribution is a reference distribution, not automatically the physical equilibrium distribution.]], [[A structure predictor's confidence score measures expected accuracy, not the free energy or population of a conformation.]].
