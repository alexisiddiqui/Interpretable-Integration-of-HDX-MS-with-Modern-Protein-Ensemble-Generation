---
type: concept
aliases:
  - MaxEnt
  - maximum entropy
  - MaxEnt principle
  - MaxEnt reweighting
  - maximum entropy reweighting
  - apparent work
notation:
  - {symbol: 'P_0(x)', meaning: 'prior distribution over conformations', units: null}
  - {symbol: 'P_\text{ME}(x)', meaning: 'maximum-entropy posterior distribution over conformations', units: null}
  - {symbol: 's_i(x)', meaning: 'i-th constrained observable as a function of conformation', units: null}
  - {symbol: 's_i^\text{exp}', meaning: 'experimental value of the i-th constrained observable', units: null}
  - {symbol: '\lambda_i', meaning: 'Lagrange multiplier for the i-th constraint', units: null}
  - {symbol: 'w_j', meaning: 'weight of conformer j in the reweighted ensemble', units: null}
  - {symbol: 'w_j^0', meaning: 'prior weight of conformer j', units: null}
  - {symbol: 'W_\text{app}', meaning: 'apparent work of reweighting', units: 'kJ mol^-1'}
sources:
  - "[[@jaynesInformationTheoryStatistical1957#^c1]]"
  - "[[@cesariUsingMaximumEntropy2018#^c11]]"
  - "[[@cesariUsingMaximumEntropy2018#^c8]]"
  - "[[@cesariUsingMaximumEntropy2018#^c13]]"
  - "[[@cesariUsingMaximumEntropy2018#^c14]]"
  - "[[@cesariUsingMaximumEntropy2018#^c16]]"
  - "[[@cesariUsingMaximumEntropy2018#^c17]]"
  - "[[@cesariUsingMaximumEntropy2018#^c5]]"
  - "[[@bradshawInterpretationHDXData2020#^c17]]"
  - "[[@bradshawInterpretationHDXData2020#^c18]]"
  - "[[@bradshawInterpretationHDXData2020#^c19]]"
  - "[[@bradshawInterpretationHDXData2020#^c11]]"
  - "[[@bmsb2012ch1#^c7]]"
  - "[[@bmsb2012ch13#^c5]]"
---

## Definition

The maximum entropy principle is a recipe for choosing the least biased probability distribution that is compatible with constraints derived from data. Inference from partial information should use the distribution of maximum entropy subject to what is known. In its relative form, it gives the posterior closest to a prior, in the sense of minimum [[Kullback–Leibler divergence]], whose ensemble averages match the experimental observations. Applied to a simulated ensemble, the solution reweights each conformer by an exponential of a linear combination of its observables. This is equivalent to adding a linear bias to the potential energy, which tilts the free-energy landscape. The cost of the correction is the apparent work.

## Equations

$$ P_\text{ME} = \arg\max_P S[P \Vert P_0] \quad \text{s.t.} \quad \int s_i(x) P(x)\,dx = s_i^\text{exp},\ \ \int P(x)\,dx = 1 $$
^eq-maxent-problem

Source: [[@cesariUsingMaximumEntropy2018#^c11]], Eq. (2), p. 2.

$$ P_\text{ME}(x) \propto e^{-\sum_i \lambda_i s_i(x)}\, P_0(x) $$
^eq-maxent-posterior

Source: [[@cesariUsingMaximumEntropy2018#^c14]], Eqs. (5)–(6), p. 3.

$$ w_j = \frac{w_j^0 \exp\!\left(-\sum_i \lambda_i q_i(j)\right)}{\sum_{j'} w_{j'}^0 \exp\!\left(-\sum_i \lambda_i q_i(j')\right)} $$
^eq-maxent-weights

Source: [[@bradshawInterpretationHDXData2020#^c18]], Eq. (4), p. 8, with the HDX observables $q_i(j)$ ([[Best–Vendruscolo model#^eq-bv-feature]]). Bradshaw's $\lambda_i$ has the opposite sign to the canonical one used here, which follows Cesari.
Manuscript form: milestones/2025-11-confirmation-of-status/introduction/connect_simulation_experiment.tex#L173 (same sign as here; frames indexed by $k$, observable $\phi_i$).

$$ U_\text{ME}(x) = U(x) + k_BT \sum_i \lambda_i s_i(x) $$
^eq-maxent-potential

Source: [[@cesariUsingMaximumEntropy2018#^c16]], Eq. (7), p. 3; [[@bradshawInterpretationHDXData2020#^c17]], Eq. (3), p. 8. The bias tilts the free-energy landscape along $s$: [[@cesariUsingMaximumEntropy2018#^c17]], Eq. (9), p. 4.

$$ W_\text{app} = k_BT\, D_\text{KL}(w \Vert w^0) = k_BT \ln \left\langle \exp\!\left\{\sum_i \lambda_i \left[q_i(j) - \langle q_i \rangle_w\right]\right\} \right\rangle_w $$
^eq-apparent-work

Source: [[@bradshawInterpretationHDXData2020#^c11]], Eq. (6), p. 9, which relates it to $D_\text{KL}$. The $\lambda$ sign is converted to the canonical convention.
Manuscript form: projects/1-ValDX/manuscript/report/6_methods_omc.tex#L418 (as $\Delta U_\text{corr}$, Bradshaw's sign); connect_simulation_experiment.tex#L191 (as $k_BT\sum_k \hat w_k \ln(\hat w_k/w_{0,k})$).

## Derivation

1. Maximise the relative entropy subject to $M$ ensemble-average constraints and normalisation ([[@cesariUsingMaximumEntropy2018#^c11]], Eq. 2).
2. Form the Lagrange function $\mathcal{L} = S[P\Vert P_0] - \sum_i \lambda_i\left(\int s_i P - s_i^\text{exp}\right) - \mu\left(\int P - 1\right)$ ([[@cesariUsingMaximumEntropy2018#^c8]], Eq. 3).
3. Take the functional derivative: $\delta\mathcal{L}/\delta P(x) = -\ln[P(x)/P_0(x)] - 1 - \sum_i \lambda_i s_i(x) - \mu$ ([[@cesariUsingMaximumEntropy2018#^c13]], Eq. 4).
4. Set it to zero, drop the normalisation, and obtain $P_\text{ME} \propto e^{-\lambda\cdot s} P_0$ ([[@cesariUsingMaximumEntropy2018#^c14]], Eqs. 5–6). Each $\lambda_i$ is then fixed by enforcing agreement with $s_i^\text{exp}$.
5. With a Boltzmann prior $P_0 \propto e^{-U/k_BT}$ ([[Boltzmann distribution#^eq-boltzmann]]), the posterior is the Boltzmann distribution of $U + k_BT\lambda\cdot s$ ([[@cesariUsingMaximumEntropy2018#^c16]], Eq. 7).
6. For a finite ensemble, restrict to the frames: $w_j \propto w_j^0 e^{-\lambda\cdot q(j)}$ (step ours; Bradshaw Eq. 4 up to sign).
7. Substitute step 6 into $D_\text{KL}(w\Vert w^0)$: $\ln(w_j/w_j^0) = -\lambda\cdot q(j) - \ln Z_\lambda$, so $D_\text{KL} = -\lambda\cdot\langle q\rangle_w - \ln Z_\lambda$. The same expression equals $\ln\langle e^{\lambda\cdot(q - \langle q\rangle_w)}\rangle_w$, which is Bradshaw's Eq. (6) divided by $k_BT$ (step ours; relation stated in [[@bradshawInterpretationHDXData2020#^c11]]).
8. With experimental error, the multipliers minimise $L = W_\text{app}/k_BT - \ln\rho_\text{err}$, a negative log-posterior ([[@bradshawInterpretationHDXData2020#^c19]], Eq. 5; see [[Bayes' theorem]]).

## Assumptions and limits

- Reweighting can only redistribute weight among states the prior contains. It is [[importance sampling]] from the prior, with the same overlap and effective-sample-size limits.
- The Boltzmann distribution is itself the maximum-entropy distribution under a single average-energy constraint ([[@bmsb2012ch1#^c7]], p. 28; [[Boltzmann distribution]], derivation).
- In SAXS, MaxEnt is used as a regulariser with a prior estimate ([[@bmsb2012ch13#^c5]], Eq. 13.16), which is the same relative-entropy prior ([[regularisation]], step 4).
- Constraining a whole coarse-grained marginal instead of a few averages turns the MaxEnt solution into the [[reference ratio method]] (step 6 there).
- Exact constraints overfit noisy data. Errors must enter through $\rho_\text{err}$ or a regulariser ([[@cesariUsingMaximumEntropy2018#^c2]]).
- The linear bias is in the forward-model features $q_i$, so forward-model error is absorbed into the weights.

## Why it matters here

MaxEnt reweighting is the prior-preserving fitting step. It lets an HDX-MS dataset adjust a simulated ensemble without overfitting, and it is the central operation of both ValDX and jaxENT. Those chapters' own formulations (ValDX Work Done, jaxENT's composable losses) are method notes that build on these equations.

Claims that use this term: [[HDXer implements a MaxEnt optimisation framework to reweight the simulated ensemble.]], [[MaxEnt reweighting avoids overfitting and ensures the resulting ensemble remains physically plausible.]], [[MaxEnt reweighting seeks new weights that minimise the discrepancy with experimental uptake while staying close to the prior.]], [[Maximum Entropy (MaxEnt) optimisation is one approach to fitting simulated ensembles to experimental data.]], [[Minimising apparent work and KL divergence gives a reweighted ensemble that satisfies the constraints with minimal deviation.]], [[Reweighting ensembles to fit experiment while minimising deviation from the original identifies the minimal changes needed.]], [[SAXS ensembles have been refined against scattering profiles using Bayesian inference and maximum entropy reweighting.]], [[SAXS with MD simulations and ensemble refinement gives minimal ensembles consistent with restraints, without overfitting.]], [[The MaxEnt reweighting optimisation problem is solved with the method of Lagrange multipliers.]].
