---
type: decision
date: 2026-10-13
project:
status: active
---

## Decision

The thesis uses one notation for HDX kinetics, forward models and reweighting. Each symbol is declared in the `notation:` field of the concept that defines it, and `kb/notation.md` collates them.

| Quantity | Canonical | ValDX writes | jaxENT writes |
|---|---|---|---|
| Residue index, conformer index | $i = 1..N$, $j = 1..M$ | $i$, $x$ | $i$ for both residues and frames |
| Intrinsic, observed exchange rate | $k_{\text{int},i}$, $k_{\text{obs},i}$ | same | same |
| Opening, closing rate; opening equilibrium constant | $k_\text{op}$, $k_\text{cl}$, $K_\text{op} = k_\text{op}/k_\text{cl}$ | — | same (SI) |
| Protection factor | $P_{f,i}$ | $P_f$, $P_f(i)$ | $\text{PF}_i$ |
| Free energy of opening | $\Delta G_\text{op} = RT \ln P_f$ (kJ mol⁻¹) | $\Delta G_\text{open} \approx RT\ln P_f$ | $\Delta G_\text{op} = k_BT \log P_f$ (SI) |
| BV coefficients and counts | $\beta_C, \beta_H$; $N_C(i), N_H(i)$; per conformer $N_C(i,j)$ | $\beta_\text{C}, \beta_\text{H}$; $N_\text{C}(i,x)$ | $\beta_c, \beta_h$; $N_i^C, N_i^H$ |
| BV feature (ln protection) of residue $i$ in conformer $j$ | $q_i(j)$ | $q_i(x)$ | — |
| Residue, peptide fractional uptake | $D_i(t)$, $D_p(t)$ | $D_i(t)$ | $D_i(t)$, $D_\text{peptide}(t)$ |
| Ensemble weights, prior weights | $w_j$, $w_j^0$ | weights of $\hat X$ | $\omega_i$ |
| Lagrange multipliers | $\lambda_i$ | $\hat\lambda(i)$ | — |
| KL divergence | $D_\text{KL}(w \Vert w^0)$ | — | $D_{KL}(\omega \Vert U)$ |
| Acid, base and water catalysis constants (Bai 1993) | $k_\text{acid}$, $k_\text{base}$, $k_\text{water}$ | — | $k_a, k_b, k_w$ (SI) |
| Potential energy, thermal energy | $U(x)$, $k_BT$ (per molecule) or $RT$ (per mole) | $k_BT$ | — |

Inference and reference-distribution terms come mostly from BMSB (Hamelryck et al. 2012), whose chapters disagree with each other. Each source's own symbols are mapped in its paper note's `## Notation` table.

| Quantity | Canonical | BMSB writes |
|---|---|---|
| Forward model: predicted observable $i$ | $s_i(x;\theta)$, extending MaxEnt's $s_i(x)$ | $f_i(x;\alpha)$ (ch12), $Tp$ (ch13) |
| Measured value, its error scale | $s_i^\text{exp}$, $\sigma_i$ | $y_i$, $\sigma$ (ch12); $D$, $\sigma_i$ (ch13) |
| Forward-model parameters | $\theta$ | $\alpha$ (ch12; ch12's $\theta$ collects all nuisance parameters) |
| Error model | $\rho_\text{err}$ (Bradshaw's symbol) | $g(y\mid\hat y,\sigma)$ (ch12) |
| Weight of the data relative to the prior | $\gamma$ (as in HDXer) | $w_\text{data} = 1/\sigma^2$ (ch12); ch13 weights the prior by $\alpha$, i.e. $1/\gamma$ |
| Prior, reference or generator distribution | $P_0(x)$, marginal $P_0(\xi)$ | $\pi$ (ch2, ch12), $q$ and $\tilde q$ (ch3), $g$ and $g_1$ (ch4) |
| Target distribution | $P(x)$ | $p$ (ch2, ch3), $f$ (ch4) |
| Coarse-grained variable | $\xi(x)$ | $y = f(x)$ (ch2), $\xi$ (ch3), $Y = m(X)$ (ch4) |
| Target and reference-ratio distributions | $P^*(\xi)$, $\hat P(x)$ | $f_1(y)$, $\hat f(x)$ (ch4) |
| Free energy along $\xi$ relative to a reference state | $\Delta F(\xi)$, reference $\tilde P(\xi)$ | $\Delta F$, $\tilde p$ (ch3) |
| Markov-chain transition kernel | $\mathcal{T}(x'\mid x)$ | $W(x'\mid x)$ (ch2) |
| Model, evidence, Bayes factor | $\mathcal{M}$, $p(s^\text{exp}\mid\mathcal{M})$, $B_{12}$ | $M$ or $H_i$, $p(d)$, $B$ (ch1, ch13) |
| Importance weights | $w_j$ (they are the reweighting weights) | $r_i$ (ch2) |
| Inverse temperature | written $1/k_BT$ | $\beta$ (ch1, ch2, ch3, ch12) |
| Energy | $U(x)$ | $E(x)$ (ch2, ch3, ch12); ch1's $U$ is the *average* energy |

KL direction: MaxEnt reweighting minimises $D_\text{KL}(P \Vert P_0)$. The reference ratio method minimises $D_\text{KL}(P_0 \Vert P)$ (BMSB ch4, Theorem 4.2), the reverse direction. This is one reason the reference ratio is a precedent for MaxEnt, not its derivation.

Logarithms are natural (`\ln`) unless base 10 is written (`\log_{10}`).

## Alternatives considered

- Keep each project's own notation and translate at chapter boundaries. Rejected: Chapter 2 defines the symbols once for Chapters 3 to 6.
- Keep Bai's $k_A, k_B, k_W$. Rejected: $k_B$ is the Boltzmann constant. Lint check 10 caught the clash.
- Name the forward model $f_i(x;\theta)$ as Habeck does. Rejected: $f(x,\tau)$ is the diffusion drift, and MaxEnt already writes the observable as $s_i(x)$.
- Write the reference distribution as $q$ or $g$, as BMSB ch3 and ch4 do. Rejected: $q_i(j)$ is the BV feature, and $g$ means four different things across BMSB. The thesis point is that the generator *is* the prior, so both are $P_0$.
- Write data as $d$ or $D$. Rejected: $D_i(t)$ and $D_p(t)$ are uptake.
- Use $\beta = 1/k_BT$. Rejected: $\beta_C$ and $\beta_H$ already use $\beta$ for the BV coefficients, so inverse temperature is written as $1/k_BT$.

## Why

The ValDX and jaxENT manuscripts disagree on $\Delta G$ (open vs op, $RT$ vs $k_BT$, ln vs log), on PF vs $P_f$, and on BV subscripts. The jaxENT weights $\omega_i$ also share their index with residues. One table removes these clashes before the chapters are written, and lint check 10 keeps them out.

## Consequences

- Concept notes give equations in this notation. A `Manuscript form:` line records where a manuscript differs.
- Chapters 3 and 4 adapt manuscript equations to this notation when text moves into the thesis.
- Open: the jaxENT loss weights $\lambda_\omega, \lambda_\beta$ clash with the Lagrange multipliers $\lambda_i$. Rename them (for example $\gamma_w, \gamma_\beta$) when the jaxENT method notes are written.
