# Voice: examples

Passages to model sentences on, each with what makes it work. Read [[style]] and [[spag]] first. Quotations keep my wording with LaTeX commands, citations and figure references removed. Paths point to the source line.

Imitate the structure, not the content: do not reuse these sentences or their specific claims in new text.

## 1. Phrases that set up an analytical relationship

- "To distinguish relative protection-factor pattern changes from distributional reorganisation…"
- "Within a single ensemble…"
- "When comparing candidate ensembles at comparable predictive agreement…"
- "…within the limits of the available structural and experimental information."

Each specifies the purpose, comparison or scope of what follows, so the reader knows how to read it. Use phrases like these in place of generic transitions.
Source: `projects/1-ValDX/manuscript/report/7_results_omc.tex:50`, `:85`, `:279`

## 2. A control credited, then bounded

> Holding the starting ensemble fixed controls the comparison but does not exclude interactions between protocol choice and ensemble deficiencies.

The grammatical subject is the experimental action. Two coordinated predicates give its reach; "but" introduces a precise limitation without weakening the comparison. No emphatic adjective is needed.
Source: `projects/1-ValDX/manuscript/report/7_results_omc.tex:162`

## 3. A method as a sequence of actions

> Given a collection of candidate protein conformations from simulation, one can predict what HDX-MS uptake each conformation would produce, then adjust how much each conformation contributes to find the combination that best matches experiment.

The opening clause sets the input; the verbs (predict, adjust, find) carry the explanation; commas order the sequence. The reader understands the operation before meeting its formal name.
Source: `projects/1-ValDX/manuscript/report/1_introduction_omc.tex:17`

## 4. One quantity, two meanings, resolved by the comparison

> Within a single ensemble, greater Apparent Work reflects correction of biased starting populations as fitting strength increases. When comparing candidate ensembles at comparable predictive agreement, smaller Work Done instead indicates that the starting ensemble required less correction.

Each sentence opens with its governing condition. Parallel construction makes the change in interpretation easy to follow. The qualification sits in the grammar exactly where it is needed.
Source: `projects/1-ValDX/manuscript/report/7_results_omc.tex:50`

## 5. Short declaratives that close an argument

> An inadequate prior or forward model can drive fitted populations towards an incorrect structural interpretation. Reweighting cannot create conformational states that are absent from the prior ensemble. Conclusions therefore remain comparative across the candidate ensembles supplied.

Risk, underlying constraint, consequence. Sentences shorten; the final "therefore" is earned. The boundary of the conclusion is set without a long disclaimer.
Source: `projects/1-ValDX/manuscript/report/7_results_omc.tex:246`

## 6. A model discussion paragraph

> One concern is that clustering averages protection factors over structurally similar frames and could reduce sensitivity to forward-model error. Our data suggest this penalty is modest for the systems studied here. The discrimination retained by valid ensembles at a proportion of 0.1 to 0.2 was equivalent to the full trajectory, and the loss of forward-model sensitivity was smaller than the gain from changing conformational representation in AF2-MSAss. Whether this balance holds for more flexible systems, or when a more precise structure-uptake model is used, remains an open question.

One job per sentence: name the concern, give the bounded response, supply the comparison, name the unresolved extension. "For the systems studied here" limits the claim cheaply. The last sentence names the circumstances under which the answer might change.
Source: `projects/1-ValDX/manuscript/report/7_results_omc.tex:237`

## 7. Compressed, contribution-focused register

> We validate jaxENT across three regimes of decreasing ground-truth availability: a synthetic benchmark with exact populations, a real system with an orthogonal HDX-NMR reference, and an α-synuclein case study with no structural ground truth. We also compare runtime against competing methods on commodity hardware. Each regime tests a different claim: that the objective recovers known populations, that it beats a Lagrangian baseline on real data, and that its uncertainty estimates remain interpretable when no reference exists.

Two colons introduce matching structures: the evidence, then the claims it tests. Repeated "that" keeps the list parallel. The study is organised by decreasing access to ground truth, giving the reader an evidential map.
Source: `projects/2-jaxENT/manuscript/report/results.tex:29`

## 8. Broad explanatory register (introduction only)

> Connecting fast molecular motions to slow pathological processes requires understanding conformational dynamics that static structures simply cannot capture.

The parallel "fast molecular motions" / "slow pathological processes" makes the scale gap immediately clear; "requires" turns it into a research need. Suitable for motivating the programme in the introduction chapter. Drop "simply" in thesis prose.
Source: `milestones/2025-11-confirmation-of-status/introduction/biological_dynamics.tex:38`

## More short boundary sentences

- "It does not measure the distance to a ground truth structure." (`7_results_omc.tex:12`)
- "The metric does not by itself identify which cause is operating." (`7_results_omc.tex:18`)
- "Generating a consensus from multiple splits does not inherently produce a representative candidate ensemble." (`7_results_omc.tex:60`)
