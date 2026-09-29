Evaluation

1. Evaluation Objective

The evaluation assesses the Intelligent Automation RCA system across
classification, knowledge retrieval, recovery recommendation, RCA
generation, evidence grounding, uncertainty handling, and handling of
unknown incidents.

The evaluation uses four controlled system configurations:

Structured RCA (baseline)

Semantic RCA

Verified Structured RCA

Verified Semantic RCA (Combined)

The same six representative incident cases are used across the four
configurations wherever the pipeline supports the corresponding
experiment:

Missing File

UI Selector

Network Path

Terminal Session

Timeout

Unknown Incident

The semantic retrieval experiment additionally includes one paraphrased
UI-selector case as a robustness test. This additional case is not
included in the six-case four-condition comparison.

The evaluation is designed so that the configurations can be compared
without changing the underlying LLM model. The baseline RCA generation
function is retained as the common generation component, while semantic
retrieval and iterative verification are introduced as separate
experimental components.

2. Evaluation Configurations

2.1 Structured RCA Baseline

The baseline system uses:

Structured incident classification

Structured root-cause retrieval

Structured recovery retrieval

Single-pass LLM-based RCA generation

The pipeline is:

Incident
    ↓
Structured Classification
    ↓
Structured Root-Cause Retrieval
    ↓
Structured Recovery Retrieval
    ↓
Single-Pass RCA Generation

The baseline is the reference configuration for the subsequent
experiments.

The complete baseline outputs and case-level observations are preserved
in:

research/results/baseline_results.json

2.2 Semantic RCA

The semantic RCA experiment replaces the structured knowledge retrieval
stage with embedding-based semantic retrieval.

The semantic retrieval component uses:

Embedding model: all-MiniLM-L6-v2

Similarity metric: cosine similarity

Root-cause retrieval: top-k = 3

Recovery retrieval: top-k = 3

LLM generation: baseline single-pass RCA generation

The pipeline is:

Incident
    ↓
Structured Classification
    ↓
Semantic Root-Cause Retrieval
    ↓
Semantic Recovery Retrieval
    ↓
Single-Pass RCA Generation

Semantic retrieval is performed independently of whether structured
classification succeeds. This allows semantically similar knowledge to
be retrieved even when the incident cannot be assigned a structured
category.

The six baseline cases were reused to enable direct comparison with
structured retrieval.

An additional paraphrased UI-selector case was introduced to evaluate
robustness to changes in wording and exception type. This case is
treated as a robustness test rather than part of the main six-case
comparison.

The semantic retrieval results showed that semantic similarity can
retrieve relevant knowledge for several known incidents, but the current
unrestricted top-k implementation can also retrieve related or
irrelevant knowledge.

The complete semantic retrieval outputs are preserved in:

research/results/semantic_rag_results.json

2.3 Verified Structured RCA

The verified structured RCA experiment retains the baseline structured
classification and retrieval pipeline and adds the V2 iterative
verification and revision loop.

The pipeline is:

Incident
    ↓
Structured Classification
    ↓
Structured Root-Cause Retrieval
    ↓
Structured Recovery Retrieval
    ↓
Initial RCA Generation
    ↓
V2 RCA Verification
    ↓
Verification Findings
    ↓
RCA Revision
    ↓
Verified Structured RCA

The verification stage evaluates the generated RCA against the permitted
evidence sources:

Observed incident information

Structured classification

Retrieved root-cause knowledge

Retrieved recovery-action knowledge

The verifier checks for:

Unsupported claims

Invented evidence

Incorrect evidence classification

Unsupported root-cause claims

Unsupported recovery actions

Unsupported model-generated content

Incorrect confidence

Unsupported prevention recommendations

Insufficient-evidence handling

Other grounding problems

The verifier uses a strict decision rule: substantive unsupported claims
or unsupported evidence are sufficient to require revision.

The revision stage is instructed to use only the original incident,
classification, retrieved knowledge, and verification findings.

The same LLM model, gpt-oss:20b-cloud, is used for RCA generation,
verification, and revision.

The V2 verifier was frozen before the Combined experiment so that the
Combined results do not reflect further prompt tuning.

The complete verified structured outputs are preserved in:

research/results/iterative_verification_results.json

2.4 Verified Semantic RCA (Combined)

The Combined configuration integrates semantic retrieval with the frozen
V2 verification and revision mechanism.

It is therefore not treated as a fifth experimental method. It is the
combination of the two experimental components:

Semantic retrieval

V2 iterative verification and revision

The pipeline is:

Incident
    ↓
Structured Classification
    ↓
Semantic Root-Cause Retrieval
    ↓
Semantic Recovery Retrieval
    ↓
Initial Semantic RCA
    ↓
V2 RCA Verification
    ↓
Verification Findings
    ↓
RCA Revision
    ↓
Verified Semantic RCA

The same all-MiniLM-L6-v2 semantic retrieval configuration and the
same frozen V2 verifier are used.

The same baseline LLM, gpt-oss:20b-cloud, is used for generation,
verification, and revision.

This configuration allows two important comparisons:

Semantic RCA vs Verified Semantic RCA: effect of verification after
semantic retrieval.

Verified Structured RCA vs Verified Semantic RCA: effect of
structured versus semantic retrieval after verification.

The complete Combined outputs are preserved in:

research/results/verified_semantic_rca_cumulative_results.json

3. Four-Configuration Experimental Design

The four configurations can be represented as follows:

Configuration   Classification   Retrieval    RCA           Verification   Revision
Generation

Structured RCA  Structured       Structured   Single-pass   None           None
LLM

Semantic RCA    Structured       Semantic     Single-pass   None           None
LLM

Verified        Structured       Structured   Single-pass   V2 LLM         V2 LLM
Structured RCA                                LLM           verifier       revision

The comparisons are interpreted as:

Comparison                   Primary Question

Structured RCA vs Semantic   What is the effect of replacing structured
RCA                          retrieval with semantic retrieval?

Structured RCA vs Verified   What is the effect of adding V2
Structured RCA               verification and revision?

Semantic RCA vs Verified     Does verification remain useful when
Semantic RCA                 retrieval is semantic rather than
structured?

This design separates the effects of retrieval and verification rather
than attributing all changes between the systems to a single component.

4. Structured vs Semantic Retrieval

For the five known incidents shared between the structured and semantic
retrieval experiments, semantic retrieval correctly ranked the
corresponding top root cause and recovery action in four cases.

Incident     Structured Root  Semantic Root    Structured     Semantic
Cause            Cause            Recovery       Recovery

Missing File Correct          Correct          Correct        Correct

UI Selector  Correct          Incorrect        Correct        Incorrect

Network Path Correct          Correct          Correct        Correct

Terminal     Correct          Correct          Correct        Correct
Session

Timeout      Correct          Correct          Correct        Correct

The UI-selector case was the main known-incident retrieval failure.
Semantic similarity ranked related UI/application/configuration
knowledge above selector-specific knowledge.

The Unknown Incident also exposed a limitation of unrestricted
nearest-neighbour retrieval. The semantic retriever always returns the
top three results and therefore produces candidate knowledge even when
the incident has no sufficiently relevant known classification or
knowledge match.

The semantic results therefore demonstrate broader matching behaviour
but also introduce retrieval ambiguity and false positives.

5. Paraphrase Robustness

An additional paraphrased UI-selector incident was evaluated using
semantic retrieval.

The paraphrased case changed the wording and exception type while
describing the same underlying failure.

Structured classification did not identify the incident:

Incident ID: None

Category: None

Confidence: 0

Semantic retrieval nevertheless returned UI-, configuration-, and
application-related knowledge.

However, the retrieved results did not contain the selector-specific
root causes or recovery actions required for a reliable diagnosis.

This indicates partial robustness to changed wording, but not sufficient
retrieval specificity for reliable diagnosis.

The result is therefore treated as evidence of partial semantic matching
rather than successful paraphrase-level diagnosis.

6. Four-Configuration Failure Analysis

6.1 Missing File

The semantic retriever returned relevant primary candidates including
the incorrect file path root cause and directory-related knowledge. It
also returned an unrelated locked-file recovery action.

The initial Verified Semantic RCA contained:

An unsupported UTC timestamp

An invented prevention recommendation

An irrelevant recovery action

Root-cause statements that were stronger than the available evidence

The V2 verifier classified the output as NEEDS_REVISION.

The revision:

Removed the unsupported timestamp

Removed the invented prevention recommendation

Removed the irrelevant recovery action

Preserved root causes as candidates rather than confirmed causes

Lowered root-cause confidence appropriately

A residual domain-derived inference remained in the revised RCA.

This case demonstrates that verification can correct both generation
grounding problems and retrieval-related relevance problems, although
the revision stage can still introduce softer domain-derived inferences.

6.2 UI Selector

Semantic retrieval returned several related UI/application candidates,
but also returned unrelated recovery actions.

The initial Verified Semantic RCA:

Overstated the relevance of one root-cause candidate

Included generalized UiPath/domain claims

Included unrelated recovery actions

Added unsupported prevention recommendations

Overstated confidence

The V2 verifier classified the output as NEEDS_REVISION.

The revision:

Removed unrelated recovery actions

Reframed root causes as unverified candidates

Removed unsupported prevention recommendations

Lowered root-cause confidence

Preserved uncertainty around the diagnosis

A residual qualified domain inference remained in the revised RCA.

This case demonstrates that verification can detect both generation
grounding errors and semantic retrieval relevance problems.

6.3 Network Path

Semantic retrieval returned relevant network-share and network-outage
root-cause candidates and relevant network recovery actions. One
additional recovery action was weakly related.

The initial Verified Semantic RCA contained:

An unsupported UTC timestamp

An invented prevention recommendation

An unjustified Medium confidence level

A strong interpretation of the network path evidence

The V2 verifier classified the output as NEEDS_REVISION.

The revision:

Removed the unsupported timestamp

Removed the prevention recommendation

Reduced confidence

Preserved the retrieved causes as unverified candidates

A residual technical inference remained in the revised output.

This case demonstrates improved grounding after verification while also
showing that the revision model may introduce general technical
knowledge even when the verifier has correctly identified the original
problem.

6.4 Terminal Session

Semantic retrieval returned relevant session-expiry and terminal
disconnection candidates. It also retrieved invalid-credential knowledge
that was not directly supported by the incident.

The initial Verified Semantic RCA:

Treated session expiry as evidence rather than a hypothesis

Presented invalid credentials as a possible cause without supporting
evidence

Included unsupported credential-related recovery

Added generic prevention recommendations

Overstated confidence

The V2 verifier classified the output as NEEDS_REVISION.

The revision:

Removed the unsupported credential cause

Removed the unsupported credential recovery action

Removed prevention recommendations

Reframed remaining causes as unverified candidates

Lowered root-cause and overall confidence

A residual qualified domain inference remained.

This demonstrates that verification can reduce unsupported diagnosis and
recovery claims while preserving uncertainty.

6.5 Timeout

Semantic retrieval returned the expected slow-application-response
candidate as the top root cause and the timeout/retry recovery action as
the top recovery result. Weaker network and application-state candidates
were also retrieved.

The initial Verified Semantic RCA:

Treated the observed five-minute duration as a configured timeout

Inferred the absence of diagnostics that were not present in the
incident payload

Presented slow application response too strongly

Added unsupported prevention recommendations

The V2 verifier classified the output as NEEDS_REVISION.

The revision:

Removed the unsupported timeout interpretation

Removed the inferred absence of diagnostics

Reframed the root cause as an unverified candidate

Removed prevention recommendations

Lowered root-cause confidence

A residual inference about the absence of explicit network or
application-state messages remained.

This case provides evidence that the verification loop can correct
specific unsupported interpretations of observed incident data.

6.6 Unknown Incident

The Unknown Incident had:

No structured classification

No structured root-cause retrieval

No structured recovery retrieval

Semantic retrieval nevertheless returned three root-cause candidates and
three recovery candidates with relatively weak similarity scores.

The initial Verified Semantic RCA included unsupported domain
assumptions and an invented UTC timestamp.

The V2 verifier classified the generated RCA as PASS.

The verified revision preserved the appropriate uncertainty:

No confirmed root cause

Candidate causes explicitly treated as unverified

Observed evidence separated from model inference

Recovery actions retained without claiming that they had been tested

No incident-specific prevention recommendation

Low confidence

However, the verifier did not flag the weak semantic retrieval
candidates themselves as a retrieval-relevance problem.

This case demonstrates an important distinction between generation
grounding and retrieval quality: the verifier can preserve uncertainty
in the generated RCA without providing an abstention mechanism for the
semantic retriever.

7. Verification Results Across Structured and Semantic Retrieval

The V2 verification loop produced the following outcomes:

Incident        Verified          Verified         Combined
Structured        Semantic         Interpretation

Missing File    NEEDS_REVISION    NEEDS_REVISION   Verification
identified
substantive grounding
problems in both
configurations.

UI Selector     NEEDS_REVISION    NEEDS_REVISION   V2 detected
unsupported claims
and retrieval-related
relevance problems.

Network Path    NEEDS_REVISION    NEEDS_REVISION   V2 detected
unsupported
interpretations and
confidence problems.

Terminal        NEEDS_REVISION    NEEDS_REVISION   V2 detected
Session                                            unsupported causes,
recovery, prevention,
and confidence
issues.

Timeout         NEEDS_REVISION    NEEDS_REVISION   V2 detected
unsupported timeout
interpretation and
confidence problems.

The Verified Structured and Verified Semantic experiments therefore show
a substantially different pattern from the earlier verifier evaluation.

Under V2, all six structured cases required revision, while five of the
six semantic cases required revision.

The semantic Unknown Incident was the only case that received a PASS.
The final output nevertheless preserved low confidence and explicit
uncertainty.

This means that the verification result itself should not be treated as
a direct measure of RCA quality. A PASS indicates that the V2 verifier
did not identify a substantive grounding violation under its evaluation
criteria; it does not independently prove that the retrieved knowledge
is relevant or that the RCA is factually correct.

8. Effect of Verification

The primary verification comparisons are:

8.1 Structured RCA vs Verified Structured RCA

Adding V2 verification and revision changed the behaviour of all six
structured cases.

The V2 verifier identified substantive grounding problems in each case.
Revisions generally:

Removed unsupported timestamps

Removed unsupported prevention recommendations

Reduced unjustified confidence

Reframed root causes as candidates when they were not established

Removed unsupported recovery actions where identified

However, the revision stage repeatedly introduced softer domain-derived
explanations or inferences.

Therefore, verification substantially improves grounding behaviour in
many cases, but the revision stage is not guaranteed to produce a
perfectly source-grounded output.

8.2 Semantic RCA vs Verified Semantic RCA

Verification also improved the semantic configuration.

Across the six cases, the V2 verifier:

Detected substantive grounding problems in five cases

Removed or corrected several irrelevant recovery actions

Reduced unsupported confidence

Preserved uncertainty for weakly supported causes

Removed unsupported prevention recommendations in the revised
outputs

The Unknown Incident received PASS, but the final RCA still maintained
low confidence and did not confirm any root cause.

The semantic experiment therefore indicates that verification can
partially compensate for weaknesses introduced by semantic retrieval,
but it does not replace retrieval-quality controls.

9. Retrieval vs Verification Comparison

The four configurations allow retrieval and verification to be
considered as separate system components.

Retrieval effect without verification

The comparison:

Structured RCA
        vs
Semantic RCA

shows that semantic retrieval:

Correctly retrieves the top root cause and recovery action for four
of five known incidents

Fails on the UI-selector case

Produces false-positive retrieval for the Unknown Incident

Provides partial robustness to changed wording

Does not currently abstain when similarity is weak

Verification effect under structured retrieval

The comparison:

Structured RCA
        vs
Verified Structured RCA

shows that V2 verification can identify and correct grounding errors
that remain in single-pass generation.

The verifier identified substantive problems in all six structured
cases.

Verification effect under semantic retrieval

The comparison:

Semantic RCA
        vs
Verified Semantic RCA

shows that verification remains useful after semantic retrieval.

It can identify:

Unsupported claims

Overstated root causes

Unsupported recovery actions

Unsupported prevention

Incorrect confidence

Some retrieval relevance problems

However, it does not provide semantic retrieval abstention.

Retrieval effect after verification

The comparison:

Verified Structured RCA
        vs
Verified Semantic RCA

shows that verification does not eliminate the differences between the
retrieval methods.

Semantic retrieval continues to introduce:

Weak or neighbouring root-cause candidates

Irrelevant recovery candidates

False-positive retrieval for unknown incidents

The verifier can remove some of these from the generated RCA, but it
does not independently guarantee retrieval relevance.

10. Evaluation Summary

The four experiments can be summarized as follows:

Dimension        Structured RCA             Semantic RCA     Verified Structured Verified Semantic
RCA                 RCA

Classification   Structured                 Structured       Structured          Structured

Root-cause       Structured                 Semantic top-k   Structured          Semantic top-k
retrieval

Recovery         Structured                 Semantic top-k   Structured          Semantic top-k
retrieval

Single-pass      Yes                        Yes              Yes, as initial RCA Yes, as initial
generation                                                                       RCA

Verification     None                       None             V2                  V2

Revision         None                       None             V2                  V2

Unknown          Abstains through           False-positive   Structured          False-positive
retrieval        classification/retrieval   candidates       abstention          candidates
path

Grounding audit  None                       None             Explicit            Explicit

The experiments show that each component addresses a different part of
the RCA problem:

Structured retrieval provides deterministic constraints.

Semantic retrieval broadens matching beyond exact taxonomy terms.

Verification audits generated RCA content against permitted
evidence.

Revision can reduce unsupported claims and improve uncertainty
handling.

Semantic retrieval still requires a mechanism for deciding when a
similarity match is insufficient.

Verification does not eliminate the need for retrieval-quality
controls.

11. Limitations

The current evaluation has several limitations:

The evaluation set is small and manually constructed.

The knowledge base is relatively small and manually authored.

Similarity scores are retrieval scores and are not calibrated
probabilities.

The semantic experiment uses a fixed top-k value of 3.

No similarity threshold or abstention mechanism was applied.

The embedding model was not specifically fine-tuned for automation
failure logs.

The semantic retrieval experiment includes only one additional
paraphrased robustness case.

The semantic retrieval evaluation is based on a small number of
manually selected incidents.

The four-condition comparison uses the same six core incidents,
limiting statistical generalization.

The same LLM model, gpt-oss:20b-cloud, is used for generation,
verification, and revision.

LLM generation, verification, and revision may be stochastic, so
differences in generated text cannot always be attributed solely to
the experimental component.

The verifier's judgments are themselves generated by an LLM and may
contain false positives, false negatives, or internally inconsistent
assessments.

Verification does not constitute independent human evaluation.

No human expert annotation has yet been used as an independent
ground-truth evaluation of RCA quality.

The revision model can introduce new domain-derived inferences even
when the verifier correctly identifies the original grounding
problem.

Retrieval relevance and RCA grounding are related but distinct
evaluation dimensions; the current verifier does not independently
score semantic retrieval quality.

The Unknown Incident case demonstrates that semantic
nearest-neighbour retrieval can return weak candidates without an
abstention mechanism.

These limitations mean that the results should be interpreted as initial
controlled engineering experiments rather than evidence of general
system or model performance.

12. Current Findings

The evaluation across the four configurations produces the following
findings:

Structured retrieval provides reliable deterministic behaviour for
the current manually defined incident taxonomy and knowledge base
when an incident can be classified successfully.

Semantic retrieval correctly ranks the corresponding top root cause
and recovery action for four of five known incidents in the shared
six-case evaluation, with the UI-selector case being the primary
known-incident retrieval failure.

Semantic retrieval provides partial robustness to changed wording
and exception type, but the additional paraphrased UI-selector case
did not retrieve sufficiently specific selector knowledge.

Unrestricted semantic nearest-neighbour retrieval produces
false-positive candidates for the Unknown Incident because the
current implementation always returns the top three results.

V2 verification identifies substantive grounding problems in all six
structured cases evaluated in the Verified Structured configuration.

V2 verification identifies substantive grounding problems in five of
six semantic cases. The semantic Unknown Incident received PASS,
while its final RCA still preserved low confidence and uncertainty.

Verification can detect not only unsupported generation claims but
also some retrieval relevance problems, as demonstrated by the
removal of unrelated recovery actions in the Missing File and
UI-selector semantic cases.

Verification substantially improves uncertainty handling by
converting unsupported or overstated causes into candidates or
undetermined conclusions and by reducing unsupported confidence in
many cases.

The revision stage is not perfectly source-grounded. Several revised
RCAs introduced softer domain-derived explanations or inferences
even after the verifier identified the original grounding problem.

The Unknown Incident demonstrates that generation grounding and
retrieval abstention are separate problems. The V2 verifier can
preserve uncertainty in the final RCA while the semantic retriever
still returns weak candidate knowledge.

Semantic retrieval and verification therefore address different
failure modes. Semantic retrieval broadens matching, while
verification constrains generated explanations against permitted
evidence.

The four-condition design provides a controlled basis for
distinguishing retrieval effects from verification effects rather
than treating the final system as a single undifferentiated
configuration.

Overall, the experiments indicate that reliable automation RCA
requires multiple complementary mechanisms: structured knowledge
provides deterministic constraints, semantic retrieval provides
broader matching, and verification provides an explicit grounding
audit. None of the individual mechanisms is sufficient on its own
for reliable RCA across both known and unknown incidents.

These findings form the current evaluation record for the Intelligent
Automation RCA system. They should be interpreted as findings from the
current controlled six-case evaluation rather than as generalized
performance claims.