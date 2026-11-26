
# Experimental Methodology

## 1. Objective

The experiments investigate retrieval strategies and verification-assisted revision in the Intelligent Automation RCA system.

The evaluation focuses on three principal questions:

1. **Retrieval relevance:** Does the retrieval component return knowledge relevant to the incident?
2. **Evidence grounding:** Does the generated RCA distinguish observed evidence from retrieved knowledge and unverified hypotheses?
3. **Revision quality:** Does verification-assisted revision improve grounding and uncertainty handling without introducing new unsupported statements?

These questions are evaluated separately because relevant retrieval does not guarantee a grounded report, and a grounded report does not establish that the retrieved candidates were relevant.

## 2. Experimental Configurations

Four evaluation paths are documented. They do not represent four equivalent RCA-generation configurations because the standalone semantic retrieval experiment does not perform LLM generation.

| Evaluation Path | Retrieval Strategy | LLM Generation | Verification-Assisted Revision |
|---|---|---|---|
| Structured RCA Baseline | Structured retrieval | Enabled | Disabled |
| Semantic Retrieval Evaluation | Embedding-based semantic retrieval | Disabled | Disabled |
| Verified Structured RCA | Structured retrieval | Enabled | Enabled |
| Verified Semantic RCA (Combined) | Embedding-based semantic retrieval | Enabled | Enabled |

The evaluation paths serve different purposes:

- **Structured RCA Baseline:** Provides the baseline structured retrieval and single-pass RCA generation workflow.
- **Semantic Retrieval Evaluation:** Examines semantic retrieval relevance independently of LLM-based RCA generation.
- **Verified Structured RCA:** Examines verification-assisted revision following structured retrieval and initial RCA generation.
- **Verified Semantic RCA (Combined):** Examines semantic retrieval followed by LLM-based RCA generation and verification-assisted revision.

The saved experiments do not include a standalone semantic retrieval configuration with single-pass LLM generation and without verification.

Consequently, the effect of adding verification to semantic RCA generation cannot be isolated through a direct baseline comparison in the current experiments.

## 3. Test Cases

The shared evaluation set contains six incident cases:

1. Missing File
2. UI Selector
3. Network Path
4. Terminal Session
5. Timeout
6. Unknown Incident

The semantic retrieval experiment additionally includes one paraphrased UI-selector case.

This additional case examines whether semantic retrieval can identify related knowledge when the incident wording and exception type differ from the original test case.

It is treated as a retrieval robustness test rather than a seventh independent incident category.

The same six core cases are reused across the saved experiments wherever the corresponding evaluation path is supported.

## 4. Semantic Retrieval

The semantic retrieval implementation uses the `all-MiniLM-L6-v2` Sentence Transformers model and cosine similarity to rank knowledge-base entries.

The configured retrieval depth is `top_k = 3`.

Root-cause entries and recovery actions are embedded and ranked separately. The incident query incorporates available exception information, classification fields, workflow information, and activity information.

The standalone semantic retrieval experiment evaluates:

- Whether the top-ranked root-cause entries are relevant to known incidents.
- Whether the top-ranked recovery actions are appropriate for the incidents.
- Whether semantic retrieval returns weakly relevant candidates for an unknown incident.
- Whether retrieval remains useful when incident wording or exception types change.

No calibrated retrieval-abstention threshold is used in the reported experiment.

Similarity ranking is therefore not treated as proof that a candidate is relevant.

The semantic retrieval experiment does not perform LLM-based RCA generation. Its results are evaluated as retrieval outputs rather than generated diagnostic reports.

## 5. Verification-Assisted Revision

The verified configurations generate an initial RCA, submit it to a verification stage, and use the verification findings to request a revised report when required.

The verification process examines potential issues including:

- Unsupported claims and assumptions.
- Details presented as evidence that were not supplied.
- Root causes not supported by incident information or retrieved knowledge.
- Recovery actions not supported by retrieved knowledge.
- Incorrect confidence assessments.
- Unsupported prevention recommendations.
- Inadequate handling of insufficient evidence.

Three aspects are considered separately:

1. **Verifier assessment:** The recorded verification outcome, such as `PASS` or `NEEDS_REVISION`.
2. **Revision behaviour:** The changes made in response to verification findings.
3. **Final-report grounding:** Whether the revised report's substantive claims remain supported by the permitted evidence.

A verification result is an assessment produced by the implemented verifier. It is not an independent guarantee that the report is correct, that retrieved knowledge is relevant, or that every unsupported statement has been detected.

## 6. Evaluation Criteria

### 6.1 Retrieval Relevance

Assess whether retrieved root-cause entries and recovery actions are relevant to the incident.

For known incidents, compare retrieved entries with the expected knowledge.

For the Unknown Incident, examine whether the system returns candidates despite insufficient relevance.

Retrieval relevance is evaluated independently of the verifier's assessment of generated reports.

### 6.2 Classification

Assess whether the incident classifier identifies the expected category and subcategory or appropriately returns no known classification for an unknown incident.

### 6.3 Evidence Grounding

Assess whether substantive RCA statements can be traced to the supplied incident information, classification, or retrieved knowledge permitted by the experimental configuration.

Distinguish directly observed evidence from retrieved knowledge, hypotheses, and domain-derived inferences.

### 6.4 Uncertainty Handling

Assess whether the report:

- Distinguishes confirmed observations from possible but unverified causes.
- Avoids presenting retrieved candidates as confirmed diagnoses without sufficient evidence.
- Communicates uncertainty when the available evidence is insufficient.
- Avoids treating knowledge-base confidence or similarity scores as calibrated incident-specific confidence.

### 6.5 Revision Behaviour

Assess whether the revised report removes unsupported content and whether it introduces new unsupported claims, assumptions, or domain-derived explanations.

The assessment considers both improvements and residual problems rather than assuming that revision necessarily improves every aspect of the report.

### 6.6 Unknown-Incident Handling

Assess whether the system appropriately handles incidents that cannot be matched confidently to the existing taxonomy or knowledge base.

In particular, examine whether:

- Semantic retrieval returns weakly relevant nearest-neighbour candidates.
- The system distinguishes candidate knowledge from incident-specific evidence.
- The verifier identifies grounding problems in the generated report.
- The system abstains from confirming a root cause when evidence is insufficient.

A verifier `PASS` does not independently demonstrate successful unknown-incident handling or reliable retrieval abstention.

## 7. Comparison Strategy

The available results support the following comparisons:

| Comparison | Evaluation Purpose |
|---|---|
| Structured retrieval vs. Semantic retrieval | Compares retrieval relevance for the shared incident cases. |
| Structured RCA Baseline vs. Verified Structured RCA | Examines verification-assisted revision under structured retrieval. |
| Verified Structured RCA vs. Verified Semantic RCA | Compares the two retrieval strategies when LLM generation and verification-assisted revision are enabled. |

The standalone semantic retrieval evaluation cannot be directly compared with Verified Semantic RCA to isolate the effect of verification on generated report quality because the standalone retrieval experiment does not generate RCA reports.

The current experiments therefore do not establish a complete controlled comparison of verification effects under both retrieval strategies.

The comparisons should also be interpreted in light of the consistency of model settings, prompts, test inputs, and evaluation procedures.

## 8. Limitations

The evaluation uses a small set of manually assessed incident cases. The findings should therefore be interpreted as exploratory rather than as a general performance guarantee.

The principal limitations are:

- The test set is small and does not establish statistical generalization.
- The paraphrased UI-selector case tests one variation in wording and does not establish broad robustness to paraphrasing.
- Semantic similarity can rank related but irrelevant entries.
- The fixed top-k retrieval configuration does not include a calibrated abstention threshold.
- The standalone semantic retrieval experiment does not include an unverified LLM-generation baseline.
- Verification-assisted revision can improve some aspects of a report while introducing new unsupported reasoning.
- The verifier is LLM-based and may fail to identify grounding or retrieval-quality problems.
- A verifier's `PASS` does not independently establish report correctness.
- The experiments do not establish production-level reliability.
- Generalization to other automation platforms has not been demonstrated.
- The evaluation does not constitute a comprehensive independent human-expert assessment.

These limitations constrain the conclusions that can be drawn from the current experiments.

## 9. Methodological Implications

The experimental design treats retrieval relevance, evidence grounding, uncertainty handling, and revision quality as distinct evaluation dimensions.

This separation is important because:

- Relevant retrieved knowledge can still be used incorrectly in a generated report.
- A report can contain unsupported statements even when retrieval is relevant.
- Semantic similarity can return candidates for incidents that have no sufficiently relevant knowledge-base match.
- Verification can identify some grounding problems without guaranteeing that the revised report is fully grounded.
- Unknown incidents require explicit consideration of retrieval relevance and uncertainty.

Future experiments should include an unverified semantic RCA generation baseline to isolate the effect of verification under semantic retrieval.

A calibrated retrieval-abstention mechanism and independent human assessment would also strengthen the evaluation.
