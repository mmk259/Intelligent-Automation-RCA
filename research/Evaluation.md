# Evaluation

## 1. Evaluation Objective

The evaluation assesses the Intelligent Automation RCA system across
classification, knowledge retrieval, recovery recommendation, RCA
generation, evidence grounding, and handling of unknown incidents.

The evaluation is conducted incrementally as new system configurations
are introduced. The initial structured-retrieval system serves as the
baseline for subsequent experimental comparisons.

---

## 2. Evaluation Configurations

### 2.1 Baseline

The baseline system uses:

* Structured incident classification
* Structured root-cause retrieval
* Structured recovery retrieval
* Single-pass LLM-based RCA generation

The baseline was evaluated using six representative incident cases:

1. Missing File
2. UI Selector
3. Network Path
4. Terminal Session
5. Timeout
6. Unknown Incident

The complete baseline outputs and case-level observations are preserved
in `research/results/baseline_results.json`.

### 2.2 Semantic Retrieval

The semantic retrieval experiment extends the knowledge retrieval
stage using:

* Embedding model: `all-MiniLM-L6-v2`
* Similarity metric: cosine similarity
* Root-cause retrieval: top-k = 3
* Recovery retrieval: top-k = 3
* LLM generation: not included in this experiment

The six baseline cases were reused to enable direct comparison with
structured retrieval.

An additional paraphrased UI-selector case was introduced to test
robustness to changes in wording and exception type. This case is
treated as an additional robustness test rather than a direct
baseline comparison.

The complete semantic retrieval outputs are preserved in
`research/results/semantic_rag_results.json`.

### 2.3 Iterative RCA Verification

The iterative verification experiment evaluates whether an explicit
verification and revision loop can improve the reliability and
grounding of LLM-generated RCA reports.

The experiment uses the same underlying structured classification and
knowledge retrieval pipeline as the baseline. The existing single-pass
RCA generation function is also retained unchanged.

The experimental flow is:

```text
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
RCA Verification
    ↓
Verification Findings
    ↓
RCA Revision
    ↓
Verified RCA
```

The verification stage evaluates the generated RCA for:

* Unsupported claims
* Invented evidence
* Incorrect evidence classification
* Unsupported root-cause claims
* Unsupported recovery actions
* Inappropriate confidence
* Unsupported prevention recommendations
* Other grounding problems

The revision stage is instructed to revise the RCA using only the
original incident, classification, retrieved knowledge, and
verification findings.

The same LLM model, `gpt-oss:20b-cloud`, is used for both RCA
generation and verification/revision.

The complete iterative verification outputs are preserved in
`research/results/iterative_verification_results.json`.

---

## 3. Baseline vs Semantic Retrieval

| Incident         | Baseline Root Cause | Semantic Root Cause | Baseline Recovery | Semantic Recovery |
| ---------------- | ------------------- | ------------------- | ----------------- | ----------------- |
| Missing File     | Correct             | Correct             | Correct           | Correct           |
| UI Selector      | Correct             | Incorrect           | Correct           | Incorrect         |
| Network Path     | Correct             | Correct             | Correct           | Correct           |
| Terminal Session | Correct             | Correct             | Correct           | Correct           |
| Timeout          | Correct             | Correct             | Correct           | Correct           |
| Unknown Incident | No retrieval        | False positive      | No retrieval      | False positive    |

For the five known incidents shared between the experiments, semantic
retrieval correctly identified the top root cause and recovery action
in four cases. The UI-selector case was a failure, where semantically
similar but incorrect knowledge was ranked above selector-specific
root causes and recovery actions.

The unknown incident also exposed a limitation of unrestricted
nearest-neighbour retrieval. Because the system always returns the
top three results, it produces candidate knowledge even when no
sufficiently relevant knowledge exists.

---

## 4. Paraphrase Robustness

The additional paraphrased UI-selector case changed the wording of
the failure and used a different exception type while describing the
same underlying incident.

Structured classification did not identify the incident:

* Incident ID: None
* Category: None
* Confidence: 0

Semantic retrieval nevertheless returned UI-, configuration-, and
application-related knowledge. However, the retrieved results did
not contain the selector-specific root causes or recovery actions.

This indicates partial robustness to changed wording, but not
sufficient retrieval specificity for reliable diagnosis.

---

## 5. Failure Analysis

### 5.1 UI Selector Failure in Semantic Retrieval

The semantic retriever ranked configuration scope, UI input state,
and application state above selector-specific root causes.

This suggests that the embedding representation captures broad
semantic relationships between UI failures but does not reliably
distinguish closely related failure modes within the current
knowledge base.

### 5.2 Unknown Incident False Positives in Semantic Retrieval

The unknown incident produced three retrieved root causes and three
recovery actions despite having no known classification.

This is an important limitation of the current implementation:
semantic nearest-neighbour retrieval does not inherently provide an
abstention mechanism.

A future controlled experiment may investigate similarity thresholds
or other abstention strategies. These mechanisms were intentionally
not introduced into the current experiment so that the initial
semantic retrieval results remain an uncontrolled baseline for that
future investigation.

### 5.3 Iterative Verification: Missing File

The verification stage identified an unsupported claim concerning
the runtime environment in the initial RCA.

The verifier classified the output as `NEEDS_REVISION`. The revised
RCA removed the unsupported runtime claim and clarified that the
actual file path was not provided and therefore could not be directly
verified.

This represents a clear case where the verification loop improved
the grounding of the generated RCA.

### 5.4 Iterative Verification: UI Selector

The verifier classified the UI-selector RCA as `PASS` and did not
identify unsupported claims.

However, the initial RCA contained several claims that were not
directly supported by the incident data or retrieved knowledge,
including generalized statements about recent UI changes, screenshot
comparison, and interpretation of the short execution duration.

The revised RCA therefore did not provide a substantive correction.

This represents a verifier false negative and demonstrates that the
verification stage does not consistently identify unsupported
domain-specific or generalized claims.

### 5.5 Iterative Verification: Network Path

The verifier classified the Network Path RCA as `PASS`.

The generated RCA contained some interpretations that went beyond
the directly observed incident evidence, including statements about
the absence of other diagnostics and the likely level of the network
failure. The output also used timezone information that was not
explicitly provided by the incident.

The verification stage did not flag these issues.

The revised RCA therefore did not provide a clearly demonstrated
grounding improvement.

This indicates that the verifier may be sensitive to some unsupported
claims while overlooking others of a similar type.

### 5.6 Iterative Verification: Terminal Session

The verifier classified the Terminal Session RCA as `PASS`.

The initial RCA included a timezone-qualified timestamp even though
the incident data did not specify a timezone. The revised RCA removed
this unsupported detail while otherwise preserving the RCA structure.

Although the final output was cleaner, the verification stage did
not explicitly identify the unsupported timestamp as a problem.

Therefore, this case demonstrates an output change without clear
evidence that the verification mechanism itself caused the
improvement.

### 5.7 Iterative Verification: Timeout

The verifier identified an unsupported assumption that the observed
five-minute execution period represented a configured timeout.

The verifier classified the output as `NEEDS_REVISION`. The revised
RCA correctly described the five-minute period as an observed
execution duration rather than evidence of a configured timeout.

The revised output also preserved the uncertainty associated with
the retrieved root cause.

This represents a clear successful application of the verification
loop.

### 5.8 Iterative Verification: Unknown Incident

The Unknown Incident produced no structured classification, root
causes, or recovery actions.

Despite this lack of retrieved knowledge, the initial LLM-generated
RCA proposed several plausible root causes, including input problems,
activity-state mismatch, package incompatibility, and runtime or
environment issues.

The verification stage classified the RCA as `PASS`, even though its
own output explicitly identified several of these claims as
unsupported.

The revised RCA preserved the unsupported hypotheses rather than
abstaining from diagnosis.

This is the most significant failure observed in the iterative
verification experiment. The verifier was unable to enforce the
system's intended behaviour for unknown incidents: when sufficient
evidence is unavailable, the system should state that the root cause
is undetermined rather than inventing plausible explanations.

The case also exposes an internal inconsistency in the verifier:
unsupported claims were identified in the verification output, but
the overall assessment was still `PASS` and no revisions were
required.

---

## 6. Iterative Verification Results

The six iterative verification cases produced the following outcomes:

| Incident         | Verification Result | Substantive Improvement | Interpretation                                                  |
| ---------------- | ------------------- | ----------------------- | --------------------------------------------------------------- |
| Missing File     | NEEDS_REVISION      | Yes                     | Unsupported runtime claim was removed.                          |
| UI Selector      | PASS                | No                      | Verifier missed unsupported/generalized claims.                 |
| Network Path     | PASS                | Unclear                 | Unsupported interpretations were not reliably detected.         |
| Terminal Session | PASS                | Limited                 | Output became cleaner, but verifier did not identify the issue. |
| Timeout          | NEEDS_REVISION      | Yes                     | Unsupported timeout assumption was corrected.                   |
| Unknown Incident | PASS                | No                      | Major verifier failure; unsupported root causes were preserved. |

Two of the six cases produced clear evidence of successful
verification and revision: Missing File and Timeout.

However, the four remaining cases demonstrate that a `PASS` result
does not necessarily indicate that an RCA is fully grounded.

Most importantly, the Unknown Incident case shows that the
verification loop does not yet reliably enforce abstention when no
supporting knowledge is available.

The results therefore provide evidence that iterative verification
can improve RCA grounding in some cases, but that its effectiveness
is inconsistent across incident types.

---

## 7. Baseline vs Iterative Verification

The iterative verification experiment uses the same structured
classification and knowledge retrieval pipeline as the baseline and
adds verification and revision around the existing RCA generation
stage.

The comparison should therefore focus on whether the additional
verification loop identifies and corrects grounding problems rather
than treating every difference in generated wording as an improvement.

| Aspect                    | Baseline          | Iterative Verification            |
| ------------------------- | ----------------- | --------------------------------- |
| Classification            | Structured        | Structured                        |
| Root-cause retrieval      | Structured        | Structured                        |
| Recovery retrieval        | Structured        | Structured                        |
| Initial RCA               | Single-pass LLM   | Same single-pass generation       |
| Verification              | None              | LLM-based verification            |
| Revision                  | None              | LLM-based revision                |
| Grounding correction      | No explicit audit | Corrected some unsupported claims |
| Unknown-incident handling | Undetermined      | Failed to reliably abstain        |
| Additional LLM calls      | None              | Verification + revision           |

The experiment provides evidence that adding an explicit verification
stage can detect and correct certain grounding errors that survive
single-pass generation.

However, the verifier does not consistently detect unsupported
claims, and its behaviour is particularly weak for unknown incidents.

Therefore, the iterative loop should not yet be considered a
reliable guarantee of RCA correctness. Its value is better
characterized as a potentially useful reliability mechanism whose
effectiveness depends on the type of failure and the verifier's
ability to enforce the grounding constraints.

The frozen baseline results remain the reference point for the
single-pass system, while the complete iterative experiment is
preserved separately in
`research/results/iterative_verification_results.json`.

---

## 8. Limitations

The current evaluation has several limitations:

* The evaluation set is small and manually constructed.
* The knowledge base is relatively small and manually authored.
* Similarity scores are retrieval scores and are not calibrated
  probabilities.
* The semantic experiment uses a fixed top-k value of 3.
* No similarity threshold or abstention mechanism was applied.
* The embedding model was not specifically fine-tuned for automation
  failure logs.
* The semantic retrieval experiment evaluates retrieval independently
  of LLM-generated RCA quality.
* The paraphrased test set currently contains a single additional
  paraphrased incident.
* The iterative verification experiment uses a single LLM model for
  generation, verification, and revision.
* LLM generation and verification may be stochastic, so differences
  in generated text cannot always be attributed solely to the
  verification loop.
* The iterative verification evaluation contains only six incident
  cases.
* The verifier's judgments are themselves generated by an LLM and
  may contain false positives, false negatives, or internally
  inconsistent assessments.
* No human expert annotation has yet been used as an independent
  ground-truth evaluation of RCA quality.

These limitations mean that the results should be interpreted as
initial controlled engineering experiments rather than evidence of
general system or model performance.

---

## 9. Current Findings

The evaluation across the structured baseline, semantic retrieval,
and iterative verification configurations produces several findings.

1. Structured retrieval provides reliable behaviour for the current
   manually defined incident taxonomy and knowledge base when the
   incident can be classified successfully.

2. Semantic retrieval improves top-ranked retrieval for several known
   incidents but can confuse closely related failure modes, as shown
   by the UI-selector case.

3. Unrestricted semantic nearest-neighbour retrieval produces
   false-positive knowledge for unknown incidents because the current
   implementation lacks an abstention mechanism.

4. The semantic retrieval experiment showed partial robustness to
   changed wording and exception type, but the paraphrased
   UI-selector case did not retrieve sufficiently specific knowledge.

5. Iterative verification successfully identified and corrected
   unsupported claims in the Missing File and Timeout cases.

6. The verification stage also produced false negatives. In
   particular, unsupported or generalized claims in the UI-selector
   and Network Path cases were not reliably detected.

7. The Unknown Incident case exposed a major weakness in the
   verification loop. The verifier identified unsupported claims in
   its own analysis but still returned `PASS` and allowed unsupported
   root-cause hypotheses to remain in the revised RCA.

8. Therefore, iterative verification can improve RCA grounding in
   individual cases but cannot currently be treated as a guarantee
   of reliable grounding or correct abstention.

9. Overall, the experiments indicate that reliable automation RCA
   requires more than a single retrieval or generation mechanism.
   Structured knowledge provides useful constraints, semantic
   retrieval provides broader matching, and verification can improve
   generation quality in some cases, but each mechanism introduces
   distinct failure modes.

These findings provide the basis for the next controlled comparison
of the evaluated system configurations.
