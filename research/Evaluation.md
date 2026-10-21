
# Evaluation

## 1. Evaluation Objective

This evaluation examines the Intelligent Automation RCA system across incident classification, knowledge retrieval, recovery recommendation, RCA generation, evidence grounding, uncertainty handling, and unknown-incident handling.

Four controlled configurations are evaluated:

1. **Structured RCA** — structured retrieval with single-pass LLM generation.
2. **Semantic RCA** — semantic retrieval with single-pass LLM generation.
3. **Verified Structured RCA** — structured retrieval with V2 verification and revision.
4. **Verified Semantic RCA (Combined)** — semantic retrieval with V2 verification and revision.

The same six representative incident cases are used across the four configurations wherever the corresponding experiment is supported:

- Missing File
- UI Selector
- Network Path
- Terminal Session
- Timeout
- Unknown Incident

The semantic retrieval experiment additionally includes one paraphrased UI-selector case as a robustness test. This additional case is not included in the main six-case comparison.

The experimental design keeps the underlying LLM model consistent across configurations. Structured retrieval, semantic retrieval, and verification-assisted revision are evaluated as separate components to help distinguish their respective effects.

The evaluation is an initial controlled engineering study, not a statistically representative benchmark.

## 2. Evaluation Configurations

### 2.1 Structured RCA Baseline

The baseline configuration uses:

- Structured incident classification
- Structured root-cause retrieval
- Structured recovery retrieval
- Single-pass LLM-based RCA generation

**Pipeline:**

```text
Incident
   ↓
Structured Classification
   ↓
Structured Root-Cause Retrieval
   ↓
Structured Recovery Retrieval
   ↓
Single-Pass RCA Generation
```

This configuration serves as the reference for the subsequent experiments.

The saved baseline outputs should be identified using the actual result files in the repository. Do not use the legacy filename `baseline_results.json` unless that file exists.

### 2.2 Semantic RCA

The semantic RCA configuration replaces structured knowledge retrieval with embedding-based semantic retrieval.

The retrieval configuration uses:

| Parameter | Configuration |
|---|---|
| Embedding model | `all-MiniLM-L6-v2` |
| Similarity metric | Cosine similarity |
| Root-cause retrieval | Top-k = 3 |
| Recovery retrieval | Top-k = 3 |
| RCA generation | Baseline single-pass LLM generation |

**Pipeline:**

```text
Incident
   ↓
Structured Classification
   ↓
Semantic Root-Cause Retrieval
   ↓
Semantic Recovery Retrieval
   ↓
Single-Pass RCA Generation
```

Semantic retrieval can return candidates even when structured classification fails. However, returning candidates does not establish that those candidates are relevant or sufficient for diagnosis.

The six core cases are reused for comparison with structured retrieval. The additional paraphrased UI-selector case assesses whether semantic retrieval can identify relevant knowledge when the wording and exception type change.

The experiment demonstrates that semantic retrieval can identify relevant knowledge for several known incidents. However, the unrestricted top-k approach can also return weakly related or irrelevant candidates.

The saved semantic retrieval outputs are located at:

- `research/results/semantic_retrieval_results.json`

### 2.3 Verified Structured RCA

The verified structured configuration retains the baseline classification and retrieval pipeline and adds the V2 verification and revision process.

**Pipeline:**

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
V2 RCA Verification
   ↓
Verification Findings
   ↓
RCA Revision
   ↓
Revised Structured RCA
```

The verifier assesses the generated RCA against the permitted evidence sources:

- Observed incident information
- Structured classification
- Retrieved root-cause knowledge
- Retrieved recovery-action knowledge

The verification process checks for issues including:

- Unsupported claims
- Invented evidence
- Incorrect evidence classification
- Unsupported root-cause claims
- Unsupported recovery actions
- Unsupported model-generated content
- Incorrect confidence assessments
- Unsupported prevention recommendations
- Inadequate handling of insufficient evidence
- Other grounding problems

Substantive unsupported claims or evidence can trigger a `NEEDS_REVISION` outcome under the verifier's decision criteria.

The revision stage is instructed to use the original incident information, classification, retrieved knowledge, and verification findings.

The same configured LLM, `gpt-oss:20b-cloud`, is used for generation, verification, and revision.

The V2 verifier was frozen before the Combined experiment to avoid further prompt tuning specifically for that configuration.

The saved structured verification results are located at:

- `research/results/structured_verification_results.json`

### 2.4 Verified Semantic RCA (Combined)

The Combined configuration integrates semantic retrieval with the V2 verification and revision process.

It is not a fifth experimental method. It combines the two experimental components:

1. Semantic retrieval
2. V2 verification and revision

**Pipeline:**

```text
Incident
   ↓
Structured Classification
   ↓
Semantic Root-Cause Retrieval
   ↓
Semantic Recovery Retrieval
   ↓
Initial RCA Generation
   ↓
V2 RCA Verification
   ↓
Verification Findings
   ↓
RCA Revision
   ↓
Revised Semantic RCA
```

The configuration uses the same `all-MiniLM-L6-v2` retrieval setup and frozen V2 verifier.

The same configured LLM, `gpt-oss:20b-cloud`, is used for generation, verification, and revision.

This configuration supports two principal comparisons:

- **Semantic RCA vs. Verified Semantic RCA:** Examines the effect of adding verification and revision to semantic retrieval.
- **Verified Structured RCA vs. Verified Semantic RCA:** Examines differences between structured and semantic retrieval when verification is applied.

The saved semantic verification results are located at:

- `research/results/semantic_verification.json`

## 3. Four-Configuration Experimental Design

| Configuration | Classification | Retrieval | Initial generation | Verification | Revision |
|---|---|---|---|---|---|
| Structured RCA | Structured | Structured | Single-pass LLM | None | None |
| Semantic RCA | Structured | Semantic | Single-pass LLM | None | None |
| Verified Structured RCA | Structured | Structured | Single-pass LLM | V2 verifier | V2 revision |
| Verified Semantic RCA (Combined) | Structured | Semantic | Single-pass LLM | V2 verifier | V2 revision |

The principal comparisons are:

| Comparison | Primary question |
|---|---|
| Structured RCA vs. Semantic RCA | What changes when structured retrieval is replaced by semantic retrieval? |
| Structured RCA vs. Verified Structured RCA | What changes when V2 verification and revision are added to structured retrieval? |
| Semantic RCA vs. Verified Semantic RCA | Does verification remain useful when retrieval is semantic? |
| Verified Structured RCA vs. Verified Semantic RCA | How do the retrieval methods differ when both use verification? |

This design helps separate retrieval effects from verification effects rather than attributing every observed change to a single component.

## 4. Structured vs. Semantic Retrieval

For the five known incidents shared between the structured and semantic retrieval experiments, semantic retrieval correctly ranked the corresponding root-cause and recovery-action entries first in four cases.

| Incident | Structured root cause | Semantic root cause | Structured recovery | Semantic recovery |
|---|---|---|---|---|
| Missing File | Correct | Correct | Correct | Correct |
| UI Selector | Correct | Incorrect | Correct | Incorrect |
| Network Path | Correct | Correct | Correct | Correct |
| Terminal Session | Correct | Correct | Correct | Correct |
| Timeout | Correct | Correct | Correct | Correct |

The UI-selector case was the principal known-incident retrieval failure. Semantic similarity ranked related UI, application, or configuration knowledge above selector-specific knowledge.

The Unknown Incident exposed another limitation: unrestricted nearest-neighbour retrieval returns the top three candidates even when no sufficiently relevant knowledge match has been established.

Consequently, semantic retrieval can broaden matching beyond exact taxonomy terms, but it can also introduce ambiguity and false-positive candidates.

These results describe performance on the current manually selected cases; they should not be interpreted as a general accuracy estimate.

## 5. Paraphrase Robustness

An additional paraphrased UI-selector incident was evaluated using semantic retrieval.

The case changed the wording and exception type while describing the same underlying failure.

Structured classification did not identify the incident:

- **Incident ID:** None
- **Category:** None
- **Confidence:** 0

Semantic retrieval nevertheless returned UI-, configuration-, and application-related knowledge.

However, the retrieved results did not contain sufficiently specific selector-related root causes and recovery actions for a reliable diagnosis.

This indicates partial robustness to changed wording, but not sufficient retrieval specificity for reliable diagnosis.

The result is therefore treated as evidence of partial semantic matching rather than successful paraphrase-level diagnosis.

## 6. Case-Level Failure Analysis

### 6.1 Missing File

Semantic retrieval returned relevant candidates related to incorrect file paths and directory issues. It also returned an unrelated locked-file recovery action.

The initial Verified Semantic RCA contained:

- An unsupported UTC timestamp
- An invented prevention recommendation
- An irrelevant recovery action
- Root-cause statements stronger than the available evidence supported

The V2 verifier returned `NEEDS_REVISION`.

The revised report:

- Removed the unsupported timestamp.
- Removed the invented prevention recommendation.
- Removed the irrelevant recovery action.
- Presented root causes as candidates rather than confirmed causes.
- Reduced root-cause confidence.

A residual domain-derived inference remained in the revised report.

This case illustrates that verification-assisted revision can improve grounding and remove some retrieval-related relevance problems. However, revision does not guarantee that every remaining statement is directly supported by the available evidence.

### 6.2 UI Selector

Semantic retrieval returned related UI and application candidates, together with some unrelated recovery actions.

The initial Verified Semantic RCA:

- Overstated the relevance of a root-cause candidate.
- Included generalized UiPath or domain-related claims.
- Included unrelated recovery actions.
- Added unsupported prevention recommendations.
- Overstated confidence.

The V2 verifier returned `NEEDS_REVISION`.

The revised report:

- Removed unrelated recovery actions.
- Reframed root causes as unverified candidates.
- Removed unsupported prevention recommendations.
- Reduced root-cause confidence.
- Preserved uncertainty around the diagnosis.

A residual qualified domain inference remained in the revised report.

This case illustrates that verification can identify grounding problems and that revision can reduce some consequences of irrelevant semantic retrieval. It also demonstrates that a revised report may retain inferences that are not directly established by the evidence.

### 6.3 Network Path

Semantic retrieval returned relevant candidates associated with network shares and network outages, along with relevant network recovery actions. One additional recovery action was weakly related.

The initial Verified Semantic RCA contained:

- An unsupported UTC timestamp
- An invented prevention recommendation
- An unjustified Medium confidence level
- An overly strong interpretation of the network-path evidence

The V2 verifier returned `NEEDS_REVISION`.

The revised report:

- Removed the unsupported timestamp.
- Removed the prevention recommendation.
- Reduced confidence.
- Preserved retrieved causes as unverified candidates.

A residual technical inference remained in the revised report.

The case illustrates improved grounding after verification while demonstrating that revision may introduce general technical knowledge beyond what the evidence directly establishes.

### 6.4 Terminal Session

Semantic retrieval returned relevant session-expiry and terminal-disconnection candidates. It also retrieved invalid-credential knowledge that was not directly supported by the incident.

The initial Verified Semantic RCA:

- Treated session expiry as established evidence rather than a hypothesis.
- Presented invalid credentials as a possible cause without supporting evidence.
- Included unsupported credential-related recovery.
- Added generic prevention recommendations.
- Overstated confidence.

The V2 verifier returned `NEEDS_REVISION`.

The revised report:

- Removed the unsupported credential cause.
- Removed the unsupported credential recovery action.
- Removed prevention recommendations.
- Reframed remaining causes as unverified candidates.
- Reduced root-cause and overall confidence.

A residual qualified domain inference remained.

This case demonstrates that verification-assisted revision can reduce unsupported diagnostic and recovery claims while preserving uncertainty.

### 6.5 Timeout

Semantic retrieval ranked the expected slow-application-response candidate first and returned a timeout/retry recovery action as the top recovery result. Weaker network and application-state candidates were also retrieved.

The initial Verified Semantic RCA:

- Treated the observed five-minute duration as evidence of a configured timeout.
- Inferred the absence of diagnostics not present in the incident payload.
- Presented slow application response too strongly.
- Added unsupported prevention recommendations.

The V2 verifier returned `NEEDS_REVISION`.

The revised report:

- Removed the unsupported timeout interpretation.
- Removed the inferred absence of diagnostics.
- Reframed the root cause as an unverified candidate.
- Removed prevention recommendations.
- Reduced root-cause confidence.

A residual inference about the absence of explicit network or application-state messages remained.

This case provides evidence that the verification loop can correct specific unsupported interpretations of observed incident data, although the revision may still retain residual inferences.

### 6.6 Unknown Incident: Retrieval and Verification Limitation

The Unknown Incident exposed a limitation in the combined semantic-retrieval and verification configuration. Semantic retrieval returned nearest-neighbour root-cause and recovery candidates despite the absence of a known incident classification. The verification stage returned `PASS` for the generated RCA in this case, even though the retrieved candidates were weakly relevant.

This result shows that verification of generated report content and evaluation of retrieval relevance are separate requirements. A report can pass the implemented verification check without establishing that the retrieved knowledge is sufficiently relevant to the incident.

The result should not be interpreted as evidence that the combined system reliably abstains on unknown incidents. Future evaluation should assess retrieval relevance explicitly and investigate a calibrated abstention mechanism.

The structured and semantic configurations should also be distinguished:

- **Structured retrieval:** The Unknown Incident did not produce a structured classification or corresponding structured root-cause and recovery retrieval.
- **Semantic retrieval:** The retriever still returned nearest-neighbour candidates despite the absence of a known incident classification.
- **Verification:** The V2 verifier returned `PASS` for the semantic Unknown Incident.
- **Interpretation:** The verifier's `PASS` is its assessment under the implemented checks. It is not an independent guarantee of report correctness or retrieval relevance.

The Unknown Incident is therefore an important failure case for evaluating retrieval quality, uncertainty handling, and abstention separately.

## 7. Verification Results Across the Two Retrieval Methods

The recorded V2 verification outcomes are summarized below.

| Incident | Verified Structured RCA | Verified Semantic RCA (Combined) |
|---|---|---|
| Missing File | `NEEDS_REVISION` | `NEEDS_REVISION` |
| UI Selector | `NEEDS_REVISION` | `NEEDS_REVISION` |
| Network Path | `NEEDS_REVISION` | `NEEDS_REVISION` |
| Terminal Session | `NEEDS_REVISION` | `NEEDS_REVISION` |
| Timeout | `NEEDS_REVISION` | `NEEDS_REVISION` |
| Unknown Incident | `NEEDS_REVISION` | `PASS` |

Under the recorded V2 results, all six structured cases required revision, while five of the six semantic cases required revision.

The semantic Unknown Incident was the only case that received `PASS`.

This distinction matters because a verifier outcome is not itself a complete measure of RCA quality:

- `NEEDS_REVISION` indicates that the verifier identified issues under its implemented criteria.
- `PASS` indicates that the verifier did not identify a qualifying violation under those criteria.
- Neither outcome independently establishes factual correctness.
- Neither outcome independently establishes that the retrieved knowledge is relevant.
- A revised report may still contain domain-derived inferences or other residual problems.

Verifier outcomes must therefore be interpreted alongside the retrieved candidates, the initial report, the revised report, and an independent assessment of the evidence.

The recorded verification outcome should not be changed to imply that the verifier caught the Unknown Incident retrieval problem. In that case, it returned `PASS`.

## 8. Effect of Verification

### 8.1 Structured RCA vs. Verified Structured RCA

Adding V2 verification and revision changed the handling of all six structured cases.

The verifier identified substantive grounding problems in each case. Revisions generally:

- Removed unsupported timestamps.
- Removed unsupported prevention recommendations.
- Reduced unjustified confidence.
- Reframed unconfirmed root causes as candidates.
- Removed unsupported recovery actions where identified.

However, the revised reports sometimes introduced softer domain-derived explanations or inferences.

The results therefore suggest that verification-assisted revision can improve grounding behaviour, but do not establish that every revised output is fully evidence-grounded.

### 8.2 Semantic RCA vs. Verified Semantic RCA

Verification also affected the semantic configuration.

Across the six cases, the V2 verifier:

- Returned `NEEDS_REVISION` for five cases.
- Removed or corrected some irrelevant recovery actions through revision.
- Reduced unsupported confidence in several reports.
- Preserved uncertainty around weakly supported causes.
- Removed unsupported prevention recommendations in revised reports.

The Unknown Incident received `PASS`. Its retrieved candidates nevertheless remained weakly relevant, demonstrating that the implemented verification process did not reliably identify the retrieval-quality problem in this case.

Verification can therefore help constrain generated content after semantic retrieval, but it does not replace explicit retrieval-quality evaluation or an abstention mechanism.

### 8.3 Verifier Assessment vs. Revised-Report Evaluation

The verifier's decision and the quality of the revised report are separate evaluation dimensions.

A verifier may identify problems that a revision subsequently corrects, but the revised report can still contain residual unsupported inferences. Conversely, a `PASS` does not prove that every claim is correct or that the retrieval stage supplied sufficiently relevant knowledge.

The case-level observations in this document should therefore be interpreted as qualitative assessments of recorded experiment outputs, not as an independent human-expert validation study.

Future evaluation should explicitly distinguish:

1. **Verifier assessment:** The recorded `PASS` or `NEEDS_REVISION` outcome.
2. **Revision behaviour:** The changes made after verification findings.
3. **Final-report grounding:** Whether each substantive final claim is supported by the permitted evidence.
4. **Retrieval relevance:** Whether retrieved root-cause and recovery candidates are relevant to the incident.
5. **Uncertainty handling:** Whether the system appropriately communicates insufficient evidence and refrains from confirming an unsupported diagnosis.

## 9. Retrieval vs. Verification

The four configurations allow retrieval and verification to be examined as separate components.

### 9.1 Retrieval Effect Without Verification

The Structured RCA vs. Semantic RCA comparison indicates that semantic retrieval:

- Correctly ranked the corresponding top root cause and recovery action in four of five known incidents.
- Failed on the UI-selector case.
- Returned false-positive candidates for the Unknown Incident.
- Demonstrated partial robustness to changed wording.
- Did not apply a similarity threshold or abstention mechanism.

### 9.2 Verification Effect Under Structured Retrieval

The Structured RCA vs. Verified Structured RCA comparison indicates that V2 verification can identify grounding errors in single-pass generation.

The verifier identified substantive issues in all six structured cases. Revision generally reduced unsupported claims and improved uncertainty handling, although residual inferences remained.

### 9.3 Verification Effect Under Semantic Retrieval

The Semantic RCA vs. Verified Semantic RCA comparison indicates that verification can remain useful after semantic retrieval.

It identified issues involving:

- Unsupported claims
- Overstated root causes
- Unsupported recovery actions
- Unsupported prevention recommendations
- Incorrect confidence
- Some retrieval-related relevance problems

However, the Unknown Incident received `PASS` despite weakly relevant retrieved candidates. Verification therefore did not consistently identify retrieval-quality problems.

### 9.4 Retrieval Effect After Verification

The Verified Structured RCA vs. Verified Semantic RCA comparison shows that verification does not eliminate the differences between retrieval methods.

Semantic retrieval can still introduce:

- Weak or neighbouring root-cause candidates
- Irrelevant recovery candidates
- False-positive candidates for unknown incidents

Revision can remove some of these from the generated report, but it does not independently guarantee retrieval relevance.

## 10. Evaluation Summary

| Dimension | Structured RCA | Semantic RCA | Verified Structured RCA | Verified Semantic RCA (Combined) |
|---|---|---|---|---|
| Classification | Structured | Structured | Structured | Structured |
| Root-cause retrieval | Structured | Semantic top-k | Structured | Semantic top-k |
| Recovery retrieval | Structured | Semantic top-k | Structured | Semantic top-k |
| Initial single-pass generation | Yes | Yes | Yes | Yes |
| Verification | None | None | V2 | V2 |
| Revision | None | None | V2 | V2 |
| Unknown-incident retrieval behaviour | No structured match | Returns top-k candidates | No structured match | Returns top-k candidates |
| Verification outcome for Unknown Incident | Not applicable | Not applicable | `NEEDS_REVISION` | `PASS` |
| Explicit grounding audit | None | None | Yes | Yes |
| Retrieval abstention mechanism | Not applicable to structured no-match behaviour | No calibrated abstention | Not applicable to structured no-match behaviour | No calibrated abstention |

The experiments suggest that the components address different parts of the RCA problem:

- **Structured retrieval** provides deterministic matching against the current taxonomy and knowledge base.
- **Semantic retrieval** broadens matching beyond exact taxonomy terms.
- **Verification** audits generated RCA content against the permitted evidence.
- **Revision** can reduce unsupported claims and improve uncertainty handling.
- **Retrieval-quality controls** are still required to determine when semantic candidates are insufficiently relevant.

The Unknown Incident demonstrates why retrieval relevance, verifier assessment, and final-report correctness must be evaluated separately.

## 11. Limitations

The current evaluation has several limitations:

- The evaluation set is small and manually constructed.
- The knowledge base is relatively small and manually authored.
- Similarity scores are retrieval scores, not calibrated probabilities.
- Semantic retrieval uses a fixed top-k value of three.
- No similarity threshold or calibrated abstention mechanism was applied.
- The embedding model was not specifically fine-tuned for automation failure logs.
- The semantic retrieval experiment includes only one additional paraphrased robustness case.
- The evaluation uses a small number of manually selected incidents.
- The four-configuration comparison uses the same six core cases, limiting statistical generalization.
- The same configured LLM, `gpt-oss:20b-cloud`, is used for generation, verification, and revision.
- LLM outputs may be stochastic, so differences in generated text cannot always be attributed solely to the experimental component.
- The verifier's judgments are themselves LLM-generated and may contain false positives, false negatives, or inconsistent assessments.
- Verification does not constitute independent human evaluation.
- No human expert annotation has yet been used as an independent ground-truth assessment of RCA quality.
- The revision model can introduce new domain-derived inferences even when the verifier correctly identifies an initial grounding problem.
- Retrieval relevance and RCA grounding are related but distinct evaluation dimensions.
- The current verifier does not independently guarantee semantic retrieval relevance.
- The Unknown Incident demonstrates that semantic nearest-neighbour retrieval can return weak candidates without abstention.
- The verifier's `PASS` outcome for the semantic Unknown Incident shows that the implemented checks do not reliably detect every retrieval-quality problem.

These limitations mean that the results should be interpreted as initial controlled engineering experiments rather than evidence of general system performance.

## 12. Current Findings

The evaluation across the four configurations supports the following findings:

1. **Structured retrieval provides deterministic behaviour** for the current manually defined incident taxonomy and knowledge base when an incident can be classified successfully.

2. **Semantic retrieval broadened matching but was not consistently reliable.** It correctly ranked the corresponding top root cause and recovery action for four of five known incidents in the shared evaluation. The UI-selector case was the primary known-incident retrieval failure.

3. **Paraphrase robustness was partial.** The additional paraphrased UI-selector case retrieved related UI and application knowledge but did not retrieve sufficiently specific selector-related information for a reliable diagnosis.

4. **Unrestricted semantic retrieval produced false-positive candidates.** The Unknown Incident received nearest-neighbour root-cause and recovery candidates despite lacking a known incident classification.

5. **V2 verification identified substantive grounding problems in all six structured cases.** The verifier returned `NEEDS_REVISION` for each case in the Verified Structured configuration.

6. **V2 verification identified substantive grounding problems in five of six semantic cases.** The semantic Unknown Incident received `PASS`, despite weakly relevant retrieved candidates.

7. **Verification-assisted revision improved several reports.** It removed or corrected some unsupported claims, recovery actions, prevention recommendations, and confidence assessments.

8. **Revision was not perfectly source-grounded.** Some revised reports retained or introduced domain-derived explanations that were not directly established by the available evidence.

9. **Verifier assessment is not equivalent to report correctness.** A `PASS` records the verifier's decision under the implemented criteria; it does not independently establish factual correctness, retrieval relevance, or reliable abstention.

10. **Retrieval relevance and generation grounding require separate evaluation.** The Unknown Incident showed that a report can receive `PASS` even when the retrieved knowledge is weakly relevant to the incident.

11. **Semantic retrieval and verification address different failure modes.** Semantic retrieval broadens matching, while verification audits generated explanations against permitted evidence. Neither mechanism independently guarantees reliable diagnosis.

12. **The four-configuration design supports component-level comparisons.** It provides an initial basis for examining retrieval and verification separately, rather than treating the complete system as a single undifferentiated configuration.

Overall, the experiments indicate that reliable automation RCA requires complementary mechanisms: structured knowledge for deterministic constraints, semantic retrieval for broader matching, explicit verification for grounding checks, and retrieval-quality controls for handling insufficiently relevant candidates.

These findings apply to the current controlled evaluation and should not be generalized beyond the tested cases without further validation.
