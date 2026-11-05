---
type: method
project: 4-jax-Ka
status: draft
needs_review: false
review_reason:
code:
  - projects/4-jax-Ka/code@95091c0b6cdd334c49b43375eda3f29270bd6ef3:src/pkatrain/gqt_multitask_replay.py#L112-L162
  - projects/4-jax-Ka/code@95091c0b6cdd334c49b43375eda3f29270bd6ef3:src/pkatrain/pkai_joint_scale.py#L655-L656
  - projects/4-jax-Ka/code@95091c0b6cdd334c49b43375eda3f29270bd6ef3:src/pkatrain/pkai_joint_scale.py#L825-L843
  - projects/4-jax-Ka/code@95091c0b6cdd334c49b43375eda3f29270bd6ef3:src/pkabench/site_weights.py#L14-L27
  - projects/4-jax-Ka/code@95091c0b6cdd334c49b43375eda3f29270bd6ef3:src/pkatrain/production_ph.py#L126-L142
sources: []
---

# Loss functions and training recipes (jax-Ka)

## Scope and implementation sources

This note supplies the loss definitions for the appendix to [[06-jax-ka]]. It covers the joint pKAI baseline, GQT state prediction, the run4/hmask/dRSA objectives, negative-training and ANM ablations, the experimental-pH auxiliary and the design objectives in [[027-extremophile-vs-pka-surface]]. Performance comparisons remain in [[jaxka-edge-binder]] and [[028-poisk-free-monomer]].

The all-residue definitions below were checked against frozen Isambard `_submission` sources, rather than inferred from a later checkout. [Source receipts][receipt] and [archive receipts][archive-receipt] record remote paths and SHA-256 hashes. The training-driver and other available recorded-source hashes match the three exported model records and the retrieved negative/ANM run protocols in all 48 comparisons ([hash checks][hash-checks]). This verifies source identity for the files named by those records. Files absent from a run's hash map are identified by their retrieved snapshot and checksum. The original negative-training snapshots are archived as `decoy-rank-v1.tar.zst` and `negatives-v1.tar.zst`.

The [dRSA training driver][train] contains the common retained objective. [Residue targets and sampling][residue], [gate targets][gate] and [ANM consistency][alt] define its components. The local shared pKa implementation is byte-identical to the retrieved copy. The mathematical expressions below transcribe these implementations; they are project methods, with code as their source.

## Notation and reductions

For structure or complex $c$, site $i$ and state $s\in\{B,F\}$, write the labelled pKa as $k^s_{ci}$ and prediction as $\hat{k}^s_{ci}$. The free state removes the partner at the supplied conformation. The network predicts a bounded model-compound shift, $\hat{\delta}_{ci}=8\tanh h_{ci}$, and $\hat{k}_{ci}=k^{\mathrm{ref}}_{ci}+\hat{\delta}_{ci}$. A binding shift is $k^B-k^F$, distinct from the model-compound shift in [[pKa shift]].

Two reductions must be distinguished. For nonnegative weights $w_{ci}$, let $N_c=\sum_iw_{ci}$ and let $V$ be the set of real, unpadded structures. Define a within-structure weighted mean as $\bar e_c=\sum_iw_{ci}e_{ci}/N_c$ when $N_c>0$, and zero otherwise. Then

$$
\mathcal M_0(e,w)=\frac{1}{\#V}\sum_{c\in V}\bar e_c,
\qquad
\mathcal M_+(e,w)=\frac{1}{\#V_+}\sum_{c\in V_+}\bar e_c,
\qquad V_+=\{c\in V:N_c>0\}.
$$
^eq-jaxka-reductions

An empty outer set contributes zero. Primary pKa losses use $\mathcal M_0$, so a real structure with no eligible sites contributes zero but remains in the outer denominator. Auxiliary losses use $\mathcal M_+$ and omit structures without eligible targets. Both give structures equal weight after the inner reduction. They do not pool all residues across the batch. Source [training driver][train], lines 477–490 and 589–599.

For a logit $\ell$ and target $t\in[0,1]$, write binary cross-entropy as $b(\ell,t)=\operatorname{softplus}(\ell)-t\ell$. Write $\sigma$ for the sigmoid and $\operatorname{sg}$ for a stop-gradient operation.

## pKa state and binding-shift supervision

With pKPDB eligibility mask $m^P$ and the shared PINDER site mask $m$, the GQT primary losses are

$$
\begin{aligned}
\mathcal L_P&=\mathcal M_0((\hat{k}-k)^2,m^P),\\
\mathcal L_{\mathrm{state}}&=\tfrac12\mathcal M_0((\hat{k}^{B}-k^{B})^2,m)
 +\tfrac12\mathcal M_0((\hat{k}^{F}-k^{F})^2,m),\\
\mathcal L_{\mathrm{shift}}&=\mathcal M_0(((\hat{k}^{B}-\hat{k}^{F})-(k^{B}-k^{F}))^2,m).
\end{aligned}
$$
^eq-jaxka-pka-losses

The reference pKa cancels in each error, making these equivalent to the implementation's shift-space regression. Both branches receive gradients from the binding-shift term. The retained recipes add the three losses with unit coefficients and no burial, interface or shift-magnitude weighting of the pKa errors. Source [shared pKa implementation](../../projects/4-jax-Ka/code/src/pkatrain/gqt_multitask_replay.py:118) and [all-residue driver][train], lines 589–599 and 684–699.

pKPDB uses its `train_mask`. PINDER uses the paired loader's site mask. Training excludes bonded-Cys pKa queries from both PINDER branches using the bound disulfide flag, and from pKPDB. Arginine has no pKa labels. These are target eligibility rules. The predicted titratability gate never multiplies the pKa training loss. Validation is not changed by the bonded-Cys training exclusion; the clean-Cys score is a separate reported evaluation. Source [gate definition][gate], lines 1–18, and [loader][loader], lines 170–176.

The earlier frozen relational model uses the same three primary pKa terms, plus burial BCE at eligible query sites on the PINDER free branch and pKPDB, each with coefficient 1. Its objective has no all-residue gate, contact distillation or residue-level burial-change term. Source `projects/4-jax-Ka/code/models/ogqt-relational-50-frozen/model.json`, `protocol.objective` and `protocol.auxiliary`.

### The pKAI baseline has a different reduction

Experiment 48 uses site-batched weighted MSE,

$$
\mathcal W(e,w)=\frac{\sum_i w_i e_i}{\max(\sum_iw_i,10^{-8})},
\qquad
\mathcal L_{\mathrm{pKAI,joint}}=
\tfrac13\left[\mathcal W(e_P,w_b)+\tfrac12\{\mathcal W(e_B,w_b)+\mathcal W(e_F,w_b)\}
+\mathcal W(e_{\mathrm{shift}},w_I)\right].
$$
^eq-jaxka-pkai-loss

Here each $e$ is the corresponding squared error above. Burial weights are $w_b=0.4+0.6(1-\operatorname{clip}(\mathrm{RSA}_F,0,1))$. Interface weights are $w_I=\max(0.05,\min(1,\exp[-(d-4)/3]))$, with minimum partner heavy-atom distance $d$ in Å. The pKPDB-only arm uses its single weighted loss without the factor $1/3$. Source `pkai_joint_scale.py` lines 655–656 and 835–839 and `site_weights.py` lines 14–27, pinned above. These training reductions differ from both GQT training and the unweighted validation errors.

## Titratability and burial losses

**Titratability.** Each residue supplies side-chain, N-terminal and C-terminal token outputs. Side-chain labels are positive for D/E/H/C/Y/K/R except disulfide-bonded cysteine; terminal labels follow the prepared graph. Cysteine side-chain rows receive weight 10, and other real rows weight 1. Padded rows receive zero. Gate loss is the weighted BCE mean per structure, averaged equally between PINDER branches, plus the pKPDB gate loss. The external coefficient is 0.1. Bound and free gate labels use their respective disulfide flags. Source [gate targets][gate], lines 65–76; [driver][train], lines 486–490, 629 and 693.

**Burial.** Let $r_i^s=\operatorname{clip}(\mathrm{RSA}_i^s,0,1)$ and let $u_i^s$ be the burial logit. On PINDER, all residues with known RSA contribute to

$$
\begin{aligned}
\mathcal L_{\mathrm{bur},I}={}&\tfrac12\mathcal M_+(b(u^B,1-r^B),m_B^{\mathrm{RSA}})
+\tfrac12\mathcal M_+(b(u^F,1-r^F),m_F^{\mathrm{RSA}})\\
&+\mathcal M_+((\sigma(u^B)-\sigma(u^F)-(r^F-r^B))^2,
 m_B^{\mathrm{RSA}}m_F^{\mathrm{RSA}}).
\end{aligned}
$$
^eq-jaxka-burial-loss

The two BCE terms have their own known-RSA masks; the change term requires RSA in both states. The change target can be negative because clipping is applied to each RSA separately. This differs from the nonnegative dRSA ranking target below. Both branches receive gradients. pKPDB retains query-site burial BCE on eligible pKa sites with known RSA, $\mathcal L_{\mathrm{bur},P}$. Each dataset's burial loss has external coefficient 1. Source [driver][train], lines 607–614 and 684–693. Missing RSA and padding use the negative sentinel installed by [residue attachment][residue], lines 168–171.

## Contact BCE and bound-to-free distillation

For minimum inter-residue heavy-atom distance $d$ in Å, the contact target is

$$
t(d)=\begin{cases}
\min(1,\exp[-(d-4)/3]),&d\leq10,\\
0,&d>10.
\end{cases}
$$
^eq-jaxka-contact-target

Each complex supplies 256 sampled cross-chain pairs with free RSA at least 0.1 at both endpoints. Half are sampled with replacement from contacts, and half from surface pairs on different chains. The random half can also contain contacts; it is not a set of 128 guaranteed negatives. Without contacts, all slots use random surface pairs. Without two surface-containing chains, all pair weights are zero. Valid sampled slots have weight 1. Source [pair sampler][residue], lines 137–155.

For bound and free edge logits $\ell^B,\ell^F$ on those same pairs,

$$
\mathcal L_{\mathrm{edge}}=
\tfrac12\mathcal M_+(b(\ell^B,t),w_E)
+\tfrac12\mathcal M_+(b(\ell^F,t),w_E)
+\mathcal M_+(b(\ell^F,\sigma(\operatorname{sg}(\ell^B))),w_E).
$$
^eq-jaxka-edge-loss

The coefficient 0.1 multiplies the whole expression. Thus the effective coefficients are 0.05 for each supervised branch and 0.1 for distillation. Distillation trains the free prediction towards the current bound probability with no gradient through that probability. The bound branch still receives its own supervised gradient, and both passes share parameters. Source [driver][train], lines 631–641.

## Within-complex ranking and dRSA targets

Anchors are exposed interface residues on either chain, with at least one contact and one noncontact among the opposite chain's interface residues. Sampling uses at most 64 anchors and 32 candidates per anchor, without replacement. Up to eight slots are reserved for noncontacts before contacts are subsampled. A candidate is an interface residue globally but can be a noncontact of the particular anchor. Source [within sampler][residue], lines 388–438.

For sampled candidates $j$ of anchor $a$, let $q_{aj}=t_{aj}/\sum_jt_{aj}$ and let $p_{aj}$ be the softmax of the free pair logits over the unpadded candidates. Then

$$
\mathcal L_{\mathrm{within}}=
\mathcal M_+\left(-\sum_j q_{aj}\log p_{aj},m_{\mathrm{anchor}}\right).
$$
^eq-jaxka-within-loss

The inner reduction averages eligible anchors per complex; the outer reduction averages complexes with at least one. There is no additional softmax temperature. Distance targets use $t_{aj}=t(d_{aj})$. dRSA targets instead use

$$
t_{aj}^{\mathrm{dRSA}}=t(d_{aj})\min(\rho_a,\rho_j),
\qquad \rho_i=\operatorname{clip}(\mathrm{RSA}_{F,i}-\mathrm{RSA}_{B,i},0,1).
$$
^eq-jaxka-drsa-target

Missing RSA differences give zero. Anchors whose target sum is below $10^{-6}$ are omitted. Candidate draws and distance-based eligibility stay the same between target modes; dRSA changes the relative target mass and can remove anchors. The coefficient remains 0.3 in hmask and dRSA. Source [target weighting][residue], lines 394–438, and `within_loss`, lines 487–496.

## Negative-training variants

Retyped and swapped-partner training use the same margin loss on sampled contacts whose soft target exceeds 0.5,

$$
\mathcal L_{\mathrm{neg}}=
\mathcal M_+\left(\operatorname{softplus}[1-(\ell_{\mathrm{true}}-\ell_{\mathrm{decoy}})],
 m_{\mathrm{contact,decoy}}\right).
$$
^eq-jaxka-negative-loss

All eligible pair/decoy slots are averaged within a complex before averaging complexes. Gradients enter true and decoy logits. Retyping chooses one chain and changes half its eligible interface residues, rounded up and capped at 32, requiring at least three changes. Interface eligibility uses 6 Å; G/P/C are excluded. Charged types switch sign, and other types are drawn from a fixed composition outside their chemistry class. Source [archived negative implementation][neg-residue], `retype` and `margin_loss`.

Unrestricted batch swaps use four cyclic partner indices, excluding self and partners without contacts. Same-stratum swaps take up to four eligible partners and exclude homomers from training anchors and decoys. The curvature variant chooses a partner residue with the closest geometric proxy. These are assumed nonbinding partners. The evaluation's five swapped partners per complex are a separate protocol. Source [archived sampler][neg-residue], `batch_decoy_index` and `swap_decoy_index`; [[jaxka-edge-binder#Negative construction distinguishes contacts from sequence compatibility]].

The recorded early within-ranking arms retain retyped-decoy weight 0.1. Increasing their within coefficient is not an isolated comparison with run4. Hmask removes that retyped term. The [saved negative run protocols][protocols] and recipe table below preserve this distinction.

## Hotspot masking and ANM routing

Hotspot masking changes the input to existing losses and introduces no separate penalty. On half of PINDER visits, one chain is chosen uniformly. Its retained identities are the top half of exposed residues by PeSTo, rounded to the nearest integer with at least one retained when the surface is nonempty. Other identities on that chain, including buried ones, are zeroed; coordinates and the other chain remain intact. Missing oracle records use random surface selection. Only free contact BCE, distillation and within ranking use this pass. pKa, burial and gate losses use unmasked inputs. Source [hotspot implementation][residue], lines 617–700, and [driver][train], lines 635–640 and 662–671.

For an alternative free conformation $A$ and the crystal free conformation $X$, the consistency penalties are

$$
\mathcal L_{\mathrm{cons},E}=\mathcal M_+((\ell^A-\ell^X)^2,w_E m_{\mathrm{alt}}),
\qquad
\mathcal L_{\mathrm{cons},K}=\mathcal M_+((\hat{k}^A-\hat{k}^X)^2,m m_{\mathrm{alt}}).
$$
^eq-jaxka-consistency-loss

These terms average only visits that actually used an alternative view and have eligible edges or sites. They compare unmasked predictions with the same per-complex dropout key. Both sides receive gradients in the executed consistency recipes; their saved `stop_gradient_crystal` flag is false. Full consistency uses coefficients 0.3 for edges and 1.0 for pKa. Source [consistency functions][alt], lines 317–332, and [saved ANM protocols][anm-receipt].

On half the visits, augmentation requests a minimised, approximately 1 Å ANM or approximately 2 Å ANM view, uniformly across the three sources. Missing or incompatible records fall through to the next source and then to crystal. The full augmentation replaces the free geometry for the primary and auxiliary predictions while retaining the native pKa/contact labels. Its free RSA comes from the side store. Edge-only augmentation retains crystal free inputs for pKa, burial and gate, and uses alternative geometry only for contact and ranking losses. The dRSA-plus-ANM recipe retains crystal-defined dRSA targets and adds no explicit consistency penalty. Source [alternative-view implementation][alt], [driver][train], lines 577–588 and 643–661, and the recorded ANM launch definitions in [[jaxka-edge-binder]].

## Complete retained objective and recipe coefficients

Define the run4 objective as

$$
\mathcal L_0=\mathcal L_P+\mathcal L_{\mathrm{state}}+\mathcal L_{\mathrm{shift}}
+\mathcal L_{\mathrm{bur},P}+\mathcal L_{\mathrm{bur},I}
+0.1(\mathcal L_{\mathrm{gate},P}+\mathcal L_{\mathrm{gate},I})
+0.1\mathcal L_{\mathrm{edge}}.
$$
^eq-jaxka-total-loss

All rows below retain these coefficients. Entries add terms to $\mathcal L_0$, with masking and geometry changes applied as described above. Zero denotes an inactive term.

| Recipe | Within target / coefficient | Retyped | Batch swap | Same-stratum swap | Edge consistency | pKa consistency | Input change |
|---|---|---:|---:|---:|---:|---:|---|
| Run4 | None / 0 | 0 | 0 | 0 | 0 | 0 | None |
| Decoy both | None / 0 | 0.1 | 0.1 | 0 | 0 | 0 | Retyped free pass |
| Early within sweep | Distance / 0.1, 0.3 or 1.0 | 0.1 | 0 | 0 | 0 | 0 | Retyped free pass |
| Within + class/curvature swaps | Distance / 0.1 | 0.1 | 0 | 0.1 | 0 | 0 | Retyped free pass |
| Hmask | Distance / 0.3 | 0 | 0 | 0 | 0 | 0 | Asymmetric identity masking |
| dRSA | dRSA / 0.3 | 0 | 0 | 0 | 0 | 0 | Asymmetric identity masking |
| ANM tie | Distance / 0.3 | 0 | 0 | 0 | 0 | 0 | Hmask + alternative free geometry |
| ANM consistency | Distance / 0.3 | 0 | 0 | 0 | 0.3 | 1.0 | Hmask + alternative free geometry |
| Edge-only tie | Distance / 0.3 | 0 | 0 | 0 | 0 | 0 | Hmask + edge-only geometry |
| Edge-only consistency | Distance / 0.3 | 0 | 0 | 0 | 0.3 | 0 | Hmask + edge-only geometry |
| dRSA + ANM | dRSA / 0.3 | 0 | 0 | 0 | 0 | 0 | Hmask + edge-only geometry |

Sources are the run4, hmask and dRSA exports under `projects/4-jax-Ka/code/models/`, and the [negative][archive-receipt] and [ANM][anm-receipt] runtime protocols. The term called “Siamese” therefore needs its object specified. Binding-shift regression, burial-change regression, contact distillation and view consistency are distinct losses with different gradient paths.

Each retained-model update sums the gradients from one PINDER batch and one pKPDB batch before global-norm clipping at 1 and an AdamW update with weight decay $10^{-4}$. The pKPDB stream continues across epochs while each epoch traverses the selected PINDER fraction. Dropout is 0.1, with a shared per-complex key for paired passes. Checkpoint selection uses validation state MAE plus interface binding-shift MAE; contact ranking does not select the checkpoint. Source [driver][train], lines 361–362, 695–699 and 1402–1439, and exported protocols. AdamW decay is an optimiser operation, not an extra squared-error term in the displayed objective.

## Experimental-pH auxiliary

The discarded experimental-pH head uses ordinal BCE at thresholds 4.75, 5.75, 6.75, 7.75 and 8.25. For deposited pH $h_c$, its labels are $\mathbf1[h_c>t_j]$. BCE is averaged across the five thresholds and then across structures with weights equal to target eligibility times inverse parent-entry multiplicity. A batch with no eligible targets contributes zero. PINDER uses the bound structure. The probe variant detaches site tokens and uses a separate optimiser. Source `production_ph.py`, lines 1–18, 81–86 and 136–142, pinned above; experimental comparisons in `experiments/4_backbone/07_handoff.md`. This auxiliary is absent from all rows of the retained-recipe table.

## Sequence-design objectives

These objectives score candidate sequences with a trained predictor. They do not retrain GQT.

**Surface charge.** For surface residues $S$, sequence-dependent gate $g_i$, charge sign $s_i\in\{-1,0,+1\}$ and ionised fraction $f_i(k_i,h)$ at pH $h$, the score is

$$
J_Q=\epsilon\sum_{i\in S}g_i s_i f_i(k_i,h).
$$
^eq-jaxka-charge-score

The direction is $\epsilon=+1$ at pH 3 and $-1$ at pH 10. Surface membership is fixed by the backbone RSA threshold 0.25. Acid and base fractions follow the residue's charge sign and Henderson–Hasselbalch relation ([[pKa]]). GQT supplies soft gates, while pKAI supplies binary availability. Missing pKas receive zero weight, except arginine contributes fixed positive charge with unit weight. Terminal sites are excluded. The sampler adds the scaled score to its sequence proposal log-probabilities. Source [surface guide][guide], lines 1–26 and 53–98; [[027-extremophile-vs-pka-surface]].

**Binding linkage.** With $h_{\mathrm{on}}=7.4$ and $h_{\mathrm{off}}=6.0$, define

$$
G(k)=\log_{10}(1+10^{k-h_{\mathrm{on}}})-\log_{10}(1+10^{k-h_{\mathrm{off}}}),
\qquad
J_{\mathrm{link}}=\sum_i\min(g_i^B,g_i^F)[G(k_i^B)-G(k_i^F)].
$$
^eq-jaxka-linkage-score

Under the implemented proton-linkage calculation, positive $J_{\mathrm{link}}$ corresponds to a larger predicted $K_D$ at pH 6 than at pH 7.4. Both binder and target sites enter the design objective. The target's free prediction is fixed; its bound prediction changes with the candidate binder. A site requires finite predictions in both states. The fixed arginine-charge override used for surface steering is absent here. Independent evaluation of binder-site contributions must remain distinct from this total design score. Source [linkage guide][linkage], lines 1–76 and 109–129; [[027-extremophile-vs-pka-surface]].

[receipt]: ../../.experiments/jaxka-loss-audit/receipt.json
[archive-receipt]: ../../.experiments/jaxka-loss-audit/archive-receipt.json
[anm-receipt]: ../../.experiments/jaxka-loss-audit/anm-protocol-receipt.json
[hash-checks]: ../../.experiments/jaxka-loss-audit/hash-checks.json
[train]: ../../.experiments/jaxka-loss-audit/source/drsa-within-v1/src/pkatrain/production_train.py
[residue]: ../../.experiments/jaxka-loss-audit/source/drsa-within-v1/src/pkatrain/production_residue.py
[gate]: ../../.experiments/jaxka-loss-audit/source/drsa-within-v1/src/pkatrain/production_gate.py
[loader]: ../../.experiments/jaxka-loss-audit/source/drsa-within-v1/src/pkatrain/production_loading.py
[alt]: ../../.experiments/jaxka-loss-audit/source/anm-aug-v1/src/pkatrain/production_alt.py
[neg-residue]: ../../.experiments/jaxka-loss-audit/source/negatives-v1/negatives-v1/src/pkatrain/production_residue.py
[protocols]: ../../.experiments/jaxka-loss-audit/source/protocols/
[guide]: /Users/alexi/Documents/opig-adaptyv-2026/experiments/027-extremophile-vs-pka-surface/guide.py
[linkage]: /Users/alexi/Documents/opig-adaptyv-2026/experiments/027-extremophile-vs-pka-surface/selectivity.py
