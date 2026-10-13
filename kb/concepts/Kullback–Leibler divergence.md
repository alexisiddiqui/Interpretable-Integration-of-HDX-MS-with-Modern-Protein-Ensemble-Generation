---
type: concept
aliases:
  - Kullback-Leibler divergence
  - KL divergence
  - KLD
  - relative entropy
  - D_KL
notation:
  - {symbol: 'D_\text{KL}', meaning: 'Kullback–Leibler divergence of a posterior from its prior', units: null}
  - {symbol: 'S[P \Vert P_0]', meaning: 'relative entropy of P with respect to P_0', units: null}
sources:
  - "[[@cesariUsingMaximumEntropy2018#^c10]]"
  - "[[@cesariUsingMaximumEntropy2018#^c12]]"
  - "[[@cesariUsingMaximumEntropy2018#^c9]]"
  - "[[@bradshawInterpretationHDXData2020#^c11]]"
  - "[[@bmsb2012ch4#^c3]]"
  - "[[@bmsb2012ch13#^c5]]"
  - "[[@bmsb2012ch12#^c19]]"
---

## Definition

The Kullback–Leibler divergence measures how much information is gained when a prior distribution is replaced by a posterior. It is zero only when the two are equal, and it is not symmetric. The relative entropy that the [[maximum entropy principle]] maximises is its negative, so maximising relative entropy means minimising the divergence from the prior. For reweighted ensembles it is computed over frame weights. With a uniform prior over $M$ frames, it reduces to $\ln M$ minus the entropy of the weights.

## Equations

$$ D_\text{KL}(P \Vert P_0) = \int P(x) \ln \frac{P(x)}{P_0(x)}\, dx = -S[P \Vert P_0] $$
^eq-kl

Source: [[@cesariUsingMaximumEntropy2018#^c10]], Eq. (1), p. 2; [[@cesariUsingMaximumEntropy2018#^c12]], p. 2.

$$ D_\text{KL}(w \Vert w^0) = \sum_{j=1}^{M} w_j \ln \frac{w_j}{w_j^0} \;\xrightarrow{\;w_j^0 = 1/M\;}\; \sum_j w_j \ln w_j + \ln M $$
^eq-kl-weights

Source: discrete form of the above (step ours); [[@bradshawInterpretationHDXData2020#^c11]], p. 9 (uniform-prior form, with $D_\text{KL} = W_\text{app}/k_BT$).
Manuscript form: projects/2-jaxENT/manuscript/report/methods/general_procedures.tex#L121 writes $\sum_i \omega_i \log(n\omega_i)$ (weights $\omega$ indexed by $i$; canonical $w_j$); milestones/2025-11-confirmation-of-status/introduction/connect_simulation_experiment.tex#L191 writes it as $W_\text{app}$ over frames $k$.

## Assumptions and limits

- The prior must be non-zero wherever the posterior is: reweighting cannot create states the prior lacks. A small $D_\text{KL}$ can therefore hide a missing state, which ValDX's Work Done metrics are designed to expose.
- **Direction.** $D_\text{KL}$ is not symmetric, so always state which distribution comes first. MaxEnt reweighting minimises $D_\text{KL}(P \Vert P_0)$. The reference ratio method is proved optimal for $D_\text{KL}(P_0 \Vert P)$ ([[@bmsb2012ch4#^c3]], Theorem 4.2). Under a full-marginal constraint the two directions agree ([[reference ratio method]], step 5).
- **Three places it appears.** As the prior side of reweighting (above). As the maximum-entropy regulariser of SAXS, which is a generalised KL divergence to a prior estimate ([[@bmsb2012ch13#^c5]]; [[regularisation#^eq-maxent-regulariser]]). And on the likelihood side: maximum likelihood minimises the cross-entropy, or equivalently the KL divergence, between the empirical distribution of the data and the model ([[@bmsb2012ch12#^c19]], Eqs. 12.5–12.6, p. 7).
- The divergence is measured in weight space, not structure space. Two ensembles with similar $D_\text{KL}$ can differ greatly in structure.

## Why it matters here

$D_\text{KL}$ is the "cost" side of every fit in the thesis. It appears as HDXer's apparent work, as the jaxENT MaxEnt loss, and as the baseline that ValDX's Work Done metrics extend.

Claims that use this term: [[Minimising apparent work and KL divergence gives a reweighted ensemble that satisfies the constraints with minimal deviation.]].
