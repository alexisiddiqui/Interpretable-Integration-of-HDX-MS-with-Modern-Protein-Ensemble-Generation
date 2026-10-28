# Voice: style

How to write prose for this thesis in my voice. Read this note, then [[spag]] for surface rules and [[examples]] for passages to model sentences on. These notes guide drafting; they are never evidence for a claim.

My voice is characterised by:
- **Explicit and Elegant Argumentation**: the reader should be able to follow the reasoning without needing to check the figures or methods. Each paragraph should make a clear argumentative move, and each section should end on a decision or consequence. Narrative should flow cleanly.
- **High entropy, Low Redundancy**: avoid repeating the same claim, explanation or interpretation. Each sentence should add new information. Leverage reptitiion, spacing and augmentation to make the argument clearer, not to repeat it.
- **Concise yet Cautious**: avoids fluffy, needless hedges. The prose should be dense with interwoven information, but the reader is always clear about argument position and direction. 
- **Literary Devices**: use parallelism, contrast, aliteration and other devices to add dynamism. I often play with language to improve clarity and rhythm, but avoid rhetorical and figurative flourish that distracts from the argument. The prose should be clear, not showy. Enjoyable and interesting to read, but gets to the point with minimal .


## Sources and their weight

Use the source that models the register being written. The current thesis introduction is the primary model for introduction prose; ValDX remains the default for results. These weights guide voice. The evidence trust order remains as specified in `AGENTS.md`. Where one of my manuscripts settles a point, reuse its wording and cite the file and line. For other sources, note what they show and express it in my voice, so the text is a new composition rather than a copy of the source.

| Source | What it shows | Weight |
|---|---|---|
| Current thesis introduction, `thesis/chapters/01-introduction.tex` | Biological motivation, explicit conceptual connections, authorial direction and limitations that motivate the next scientific task | Primary for introduction prose |
| ValDX, `projects/1-ValDX/manuscript/report/*_omc.tex` (PLOS, post-review) | Explicit definitions, explanation for experimental readers, bounded conclusions, practical recommendations | Primary: the mature manuscript voice |
| jaxENT, `projects/2-jaxENT/manuscript/report/` (draft, Nature Communications target) | Compressed motivation, quantitative results up front, comparative claims, movement towards biological application | How the voice sharpens for a broad contribution narrative |
| Confirmation introduction, `milestones/2025-11-confirmation-of-status/introduction/` | Breadth, foundational explanation, many examples, explicit research questions | Supporting evidence for explanatory instincts only; do not copy its promotional phrasing or draft roughness |

## The core move

Write towards the conditions under which an interpretation becomes defensible. The recurring shape of an argument, usually spread over two or three paragraphs, is:

1. State an observable result.
2. Give its possible explanations.
3. Say what prevents those explanations from being distinguished.
4. Introduce the comparison, measure or partition that makes the distinction meaningful.

This pattern matters more than any phrase or piece of vocabulary. It is the shape of a results argument, where competing explanations are developed and a comparison discriminates between them. An introduction first establishes the biological question and what answering it would show, and takes this shape only where it motivates a method.

## Let distinctions carry the argument

The central distinction is between **agreement with a measurement** and **confidence in the explanation producing it**. Others recur around it:

- structural plausibility vs population accuracy
- local vs global behaviour
- changes in model parameters vs changes in ensemble weights
- reproducibility vs representativeness

Build sentences on these distinctions. Begin with something the reader can reasonably accept, then say why it cannot carry the full inference ("Generating a consensus from multiple splits does not inherently produce a representative candidate ensemble."). Then give the result its narrower, legitimate purpose. Keep a result useful while restricting what it can be taken to mean: tell the reader which conclusion it supports and which further conclusion would exceed it.

## Structure results as successive diagnostic questions

Each analysis answers a deficiency exposed by the one before it:

1. Establish the comparison and why it matters.
2. Examine the conventional measure.
3. Identify what remains unresolved.
4. Introduce another measure or partition.
5. Interpret the joint behaviour.
6. State the remaining uncertainty or practical consequence.

Each step is usually its own paragraph. Make the dependency between analyses explicit in the transition: "We therefore examined", "To distinguish", "Given the limitations of", "Having established". A transition must say *why* the next analysis is needed. Do not use transitions that carry no logical obligation ("Importantly", "Furthermore", "Additionally", "Notably").

## One finding per results paragraph

A results paragraph can take on several jobs. It can motivate a comparison, define a metric, decode a figure, report statistics, explain the result and qualify the explanation. Each job is legitimate, and they are connected. Done together in one paragraph, they bury the finding the paragraph exists to report.

Give each job a home.

| Job | Home |
|---|---|
| Motivate the comparison | The transition that opens the paragraph, or the end of the previous one |
| Define the metric | Methods or background; in results, a one-clause reminder |
| Decode the figure | The caption |
| Report statistics | Parentheses after the claim they support |
| Explain the result | The body of the paragraph |
| Qualify the explanation | One qualification, the one that changes the advice; others go to the discussion |

The paragraph keeps its finding, the explanation and one bound. Before keeping a paragraph, state its finding in one sentence. That sentence should appear near the start, and nothing before it except the transition should be needed to understand it. Setup and methods paragraphs follow the same rule, with the design decision as the finding ([[examples]] 9).

Draft the accumulation if that is how the reasoning arrives. Separate the jobs on revision.

## Give every method an interpretive purpose

Do not just name a procedure and report its output. Say what choosing it lets the experiment test, and put that purpose before the algorithm. (The peptide-splitting methods first explain how overlapping peptides create apparent knowledge, give the example of one residue appearing in five peptides, then distinguish what each split asks; the algorithm comes last.)

Around a single finding, move between three levels:

- **Operation**: what is calculated or changed.
- **Physical interpretation**: what that operation corresponds to in the system.
- **Inferential consequence**: what its outcome lets the reader conclude.

These are three sentences about one finding, not three findings.

## State the level at which a statement is true

Use scale words deliberately: *residue-wise, peptide-level, ensemble-average, individual-frame, local, global*. They say where information exists, where it has been averaged away, and where a conclusion may legitimately apply. Where possible, explain a limitation by the level of representation that causes it (parameter optimisation acts at the ensemble-average level, so it cannot say anything at the individual-frame level).

## Caution is specific and changes the advice

A qualification names a concrete condition: the starting ensemble, the forward model, the partition, whether a reference exists, the mismatch built into a benchmark. Credit exactly what a control achieves, then name the uncertainty it leaves:

> Holding the starting ensemble fixed controls the comparison but does not exclude interactions between protocol choice and ensemble deficiencies.

Let qualifications change the recommendation (e.g. different fitting-order advice depending on the expected source of mismatch). A caveat is part of the result's practical meaning, not a disclaimer bolted on the end.

Avoid unconditional verbs and adjectives: *ensures, successfully resolves, fundamental, robust, novel, powerful*. Attach every claim to the conditions that support it. "For the systems studied here" is often all that is needed.

A sentence is never stronger than its claim note's Caveats, and an example supports only the distinction its source states. Do not carry one case's mechanism to the next, or close on a general claim the example did not establish.

## Rhythm: accumulate, then interrupt

Elegant sentences assemble the object, comparison, qualification and interpretation. Then a short declarative settles the meaning or draws a boundary:

> It does not measure the distance to a ground truth structure.

Use the short sentence after dense explanation, not as a habit. Prose made only of long sentences, or only of short ones, is not this voice. Accumulate within a sentence, not across a paragraph.

## Carry the narrative through paragraphs

In the introduction, background and conclusions a paragraph opens on what the previous one left unresolved, so the same concepts recur from paragraph to paragraph while the argument moves. Results chapters can have clearer boundaries. A check that works for both: read only the first sentence of each paragraph, and the section's argument should be there ([[examples]] 11). The last sentence of a paragraph should hint at the next, or what the reader should be thinking.

In explanatory prose, open on the relationship that makes the next concept necessary. A compact sentence such as "Folding permits function by constraining conformational freedom" gives the reader the relationship before developing it. State the central tension directly, and use "we" where it makes the reasoning or proposed response clearer. A paragraph can establish a relationship, motivate a question or explain a response without reporting a finding ([[examples]] 8, 13 and 15).

Let a concrete example develop the idea before introducing all its terminology. The introduction uses prion memory to make the functional role of conformational change explicit before explaining local frustration. A case can return later when it answers a different question. End a sequence by naming the next task in plain language, as in "The first hurdle is a way to generate them" ([[examples]] 14).

A limitation stated in its home section returns elsewhere only as a clause naming its consequence for the current step. Compose the argument from the hub rather than expanding every bullet into a sentence. Hub section-structure and group-lead sentences are instructions to the writer; open the paragraph on the scientific relationship they point to, never on the instruction or on a count of what follows ("Two cautions follow", "The kinds combine").

## Introduce concepts through actions

Explain the physical operation before the technical label. Ensemble reweighting is first "predict what each conformation would produce, then adjust how much each contributes"; the name follows. Accessibility comes from making relationships explicit (what changes, relative to what, with what consequence). A developed analogy can explain those relationships by connecting the states, the applied condition and the response in two systems.

Metaphors describe operations: *work, distance, shape, scale, landscape*. When one is used (Wasserstein distance as the effort to morph one distribution into another), reconnect it immediately to the quantity measured. Developed scientific analogies can carry an explanation wherever it is needed. The prion–memristor analogy is complete in the introduction and explains prion memory through condition-dependent switching and retained history. Preserve that explanatory role when revising. Decorative images ("freeze proteins in time", "hide in plain sight") belong sparingly in broad motivational framing.

## Vocabulary

Start from the current claim Argument or concept Definition, preserving its technical nouns and governing conditions. Adapt the surrounding syntax to the paragraph.

Preferred verbs: *compare, distinguish, assess, quantify, constrain, recover, redistribute, reveal, diagnose*. Preferred nouns: *hypothesis, representativeness, uncertainty, agreement, modification, distribution, interpretation*.

The typical sentence describes something being changed, measures that change, and asks what it reveals about the starting explanation. "Success" always needs elaborating: by which measure, against which reference, at which level?

Choose clean, standard terms that the target audience already uses, never an abstract or decorative phrase standing in for one (word list in [[spag]]). How tightly a term is fixed scales with how often it is reused. A quantity mentioned once can be described in plain words. A quantity reused across a section or chapter earns a short fixed name, built from standard terminology so its meaning is still obvious on first reading (*validation error*, *candidate ensemble*, *Work Done*).

Keep a technical noun once introduced. Write "validation error", "Work Done", "candidate ensemble" again in the next sentence rather than switching to a synonym; a stable referent matters more than variety. If repetition becomes heavy, restructure the sentence rather than introducing a synonym.

Repetition of construction is different from repetition of a noun. *Provides*, *offers* or *supplies* as the main verb of consecutive paragraphs, and "rather than" or "not X but Y" in consecutive sentences, are drafting habits; vary the construction. Cite the one or two sources that carry a sentence. Three or more keys usually means the sentence carries several claims, so split it.

## Authorial presence

- "We" for choices, tests and interpretations: *we investigated, we compared, we hypothesised*.
- Results and metrics as grammatical subjects when reporting behaviour: a metric *revealed*, an ensemble *required*, a comparison *supported*.
- An inclusive "we" ("we rely", "we need", "we can") makes the reasoning or proposed response explicit in explanatory prose. "Our strategy" can connect the scientific problem to the approach taken. Keep this authorial direction when revising the introduction ([[examples]] 15).
- Declarative contribution statements and declarative subsection titles (jaxENT style) suit contribution-focused chapters; keep them bounded.

## Figures are part of the argument

Teach the reader how to read the encoding before asking them to accept the interpretation. The caption does most of this decoding: what a colour represents, what a reference structure means, why a distribution is normalised, how a panel relates to an earlier comparison. In the body, decode only what the interpretation depends on, in a clause, then interpret. Describe what a successful outcome should look like (in jaxENT MoPrP: structural position and weight).

Captions are compact arguments: name the comparison, decode the panels, give the numbers, state the implication, so the figure can be read on its own. Keep the body text from simply repeating the caption; the body interprets, the caption decodes.

## Order examples by what they can establish

Each system or case has an evidential job: a controlled reference, a subtle comparison, a test of a methodological extension, an application with unresolved ambiguity. Present them as a sequence of decreasing certainty and say which claim each one tests ("three regimes of decreasing ground-truth availability"). The narrative then asks whether the method remains informative as the problem becomes less controlled.

Breadth examples (several disease cases showing that static structures leave questions unresolved) are for motivating a research programme, as in the introduction chapter. Do not use that pattern in results chapters.

## End on a better decision

Sections should end with what the reader should compare, investigate, retain, reject or test next. A paragraph ends on its finding or the boundary of that finding. Interpretability matters because it makes those decisions possible. Return computational results to the choices that matter in an experimental investigation. A result earns its place by changing how a hypothesis can be assessed.

## When a passage carries weight

Contribution statements, section conclusions and recommendations are where the wish to secure both the significance of a result and the conditions of its validity runs ahead of the argument. The excess takes three forms.

- Extra explanation. A method or metric already defined is explained again.
- Repetition. The result just reported returns as "These results establish that…", or one sentence lists every component of the analysis again.
- Stronger wording. *robust, systematically, critically, blueprint, adequately*.

State the claim and the condition under which it holds. Add a separate boundary sentence where it changes the interpretation ([[examples]] 5, 6 and 10). When the limitation motivates further work, carry the argument through to the comparison, measurement or methodological response it requires ([[examples]] 12).

## Registers in the thesis

| Where | Register |
|---|---|
| Introduction (ch. 1), opening of background | Current thesis introduction. Biological motivation, explicit conceptual connections and direct statements of the scientific problem. Use its compact conceptual openings, examples that develop an idea, direct authorial reasoning and concrete handoffs to the next scientific task. |
| Background (ch. 2) | ValDX explanatory register: actions before labels, explicit definitions |
| Results chapters (ch. 3–6) | ValDX register by default; jaxENT compression for contribution statements and chapter openings |
| Discussion and conclusions | ValDX discussion paragraphs: concern, bounded response, comparison, open extension |

## Revising without losing the voice

Splitting paragraphs and cutting excess must not remove the features that make the reasoning recognisable.

- Explicit analytical transitions that say why the next analysis is needed
- Stable technical vocabulary
- Movement between physical and statistical interpretations of the same quantity
- Short sentences that bound a conclusion

If a revision loses one of these, restore it and cut something else.

## Before handing back a draft

- Does each paragraph make one clear argumentative move, established near its start?
- Is any sentence stronger than its claim note's Caveats?
- Does any sentence describe the chapter's organisation instead of making the argument?
- Does the caption decode the figure, leaving the body to interpret?
- Does every transition say why the next analysis or scientific task is needed?
- In introduction prose, do the conceptual opening, example and authorial direction carry the explanation forward?
- Is every methodological choice given a purpose before its mechanics?
- Is the level (residue, peptide, ensemble-average, frame) stated wherever it changes what can be known?
- Does each caveat name a concrete condition, and does it change any advice?
- Is there a short declarative where a boundary needs settling, and not elsewhere?
- Are technical nouns kept constant across adjacent sentences, and are they standard terms the audience will recognise?
- Does the section end on a decision or consequence, not a summary?
- In conclusions, contribution statements and recommendations, is anything re-explained, restated or upgraded?
- Does it pass [[spag]]?
