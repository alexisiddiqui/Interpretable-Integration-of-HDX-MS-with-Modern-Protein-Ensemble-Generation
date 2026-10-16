# Voice: examples

Passages to model sentences on, each with what makes it work. Read [[style]] and [[spag]] first. Quotations keep my wording with LaTeX commands, citations and figure references removed. Paths point to the source line.

Imitate the structure, not the content: do not reuse these sentences or their specific claims in new text.

Examples 9 and 10 are counter-examples from the same manuscript. Read them for the failure they show, not as models.

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

The two sentences set up matching structures, the evidence and then the claims it tests. Repeated "that" keeps the list parallel. The study is organised by decreasing access to ground truth, giving the reader an evidential map. The draft uses colons here; in thesis prose end the sentence at each colon and open the list with its own subject ([[spag]], colons).
Source: `projects/2-jaxENT/manuscript/report/results.tex:29`

## 8. State the organising tension directly

> The crux is that interactions required for function can conflict locally with those that stabilise the fold.

"The crux" identifies the relationship organising the explanation. The sentence connects function to fold stability and gives the reader a reason to consider local frustration. Its authorial direction comes from stating the scientific tension directly.
Source: `thesis/chapters/01-introduction.tex:62`

## 12. A limitation leads to a scientific response

> Where candidate coverage fails, however, repeating the fit is insufficient. Experimental information must also be able to act during sampling or generation, so that the comparison can include states missing from the starting ensemble.

The first sentence names the condition under which the current approach is insufficient. The second gives the required response and its purpose. The limitation moves the argument towards a methodological question and explains why answering it matters.
Source: `thesis/chapters/01-introduction.tex:231`

## 11. Paragraphs that hand the problem forward

Four consecutive paragraphs of the ValDX introduction, by closing and opening sentence:

> …determining which conformational states give rise to an observed uptake pattern is fundamentally ambiguous.
> To address this ambiguity, researchers increasingly turn to molecular simulations for structural hypotheses. […] This fundamental degeneracy means that reweighting cannot prove a single structural hypothesis correct.
> Current implementations of ensemble reweighting face an additional validation problem that compounds this degeneracy. […] ensemble reweighting cannot reliably discriminate between competing structural hypotheses.
> A second, related problem is overfitting.

Each opening sentence names what it inherits (this ambiguity, this degeneracy, a second related problem) before adding its step, so ambiguity, degeneracy and validation overlap across paragraphs while the argument still moves. Read the four opening sentences alone and the section's argument is present. Drop "fundamentally" and "fundamental" in thesis prose.
Source: `projects/1-ValDX/manuscript/report/1_introduction_omc.tex:14`, `:17`, `:20`, `:23`

## More short boundary sentences

- "It does not measure the distance to a ground truth structure." (`7_results_omc.tex:12`)
- "The metric does not by itself identify which cause is operating." (`7_results_omc.tex:18`)
- "Generating a consensus from multiple splits does not inherently produce a representative candidate ensemble." (`7_results_omc.tex:60`)

## 9. Counter-example: one setup paragraph, eight jobs

The synthetic-benchmark setup paragraph runs to 14 sentences. Read it in place. By sentence, its jobs are:

- 1: purpose (controlled conditions for measuring accuracy)
- 2–3: data generation, and why known populations matter
- 4–7: the forward-model mismatch between generation and fitting
- 8–10: the two structural hypotheses and what each can recover
- 11: the γ sweep, with literature
- 12: split types, with colours
- 13: definition of training error
- 14: figure encoding (axes, point size)

The design decision the reader must retain sits in sentence 9. ISO-Bimodal contains only structures present in the target, so its populations can in principle be recovered, and ISO-Trimodal cannot. "Critically" is doing the work that position should do. Three paragraphs would serve: the synthetic design and why it gives a ground truth (1–7), the two hypotheses opening with sentence 9 (8–10), and the fitting protocol (11–13). Colours and point sizes go to the caption, and the colons in sentences 8 and 12 go with the split.
Source: `projects/1-ValDX/manuscript/report/7_results_omc.tex:44`

## 10. Counter-example: a conclusion under pressure

> These results establish that quantitative comparison across multiple ensembles enables robust structural hypothesis evaluation without requiring detailed prior system knowledge or direct pairwise ensemble comparisons.

The paragraph closes the BPTI section. It restates the section's result ("These results establish"), upgrades it (*robust, systematically, practical blueprint*), and lists every partition and metric again in a 69-word second sentence. The qualification that BPTI has a literature reference is present, but it sits inside a sentence whose main clause carries the claim to systems without ground truth. Compare example 6, which handles the same kind of claim with one job per sentence. The controlled form gives the finding, the condition it was shown under, and a short sentence bounding the extension.
Source: `projects/1-ValDX/manuscript/report/7_results_omc.tex:99`
