
# Experimental Methodology

## 1. Objective

The experiments investigate how retrieval strategy and verification-assisted revision affect AI-generated Root Cause Analysis (RCA) reports for automation incidents.

The evaluation focuses on three distinct questions:

1. **Retrieval relevance:** Does the retrieval component return knowledge relevant to the incident?
2. **Evidence grounding:** Does the generated RCA distinguish observed evidence from retrieved knowledge and unverified hypotheses?
3. **Revision quality:** Does verification-assisted revision improve grounding and uncertainty handling without introducing new unsupported statements?

These questions are evaluated separately because relevant retrieval does not guarantee a grounded report, and a grounded report does not establish that the retrieved candidates were relevant.

## 2. Experimental Configurations

Four configurations are evaluated.

| Configuration | Retrieval Strategy | Verification-Assisted Revision |
|---|---|---|
| Structured RCA | Structured retrieval | Disabled |
| Semantic RCA | Embedding-based semantic retrieval | Disabled |
| Verified Structured RCA | Structured retrieval | Enabled |
| Verified Semantic RCA (Combined) | Embedding-based semantic retrieval | Enabled |

The Structured RCA configuration serves as the baseline. Semantic RCA evaluates embedding-based retrieval, while the two verified configurations examine the effects of verification-assisted revision under each retrieval strategy.

The same six core incident cases are used across the configurations wherever the corresponding experiment is supported.

## 3. Test Cases

The shared test set contains six incident cases:

1. Missing File
2. UI Selector
3. Network Path
4. Terminal Session
5. Timeout
6. Unknown Incident

An additional paraphrased UI-selector case was used to examine whether semantic retrieval could return relevant knowledge when the wording differed from the exact UI-selector test.

This additional case is treated as a robustness test rather than a seventh independent incident category.

## 4. Semantic Retrieval

The semantic retrieval implementation uses the `all-MiniLM-L6-v2` Sentence Transformers model and cosine similarity to rank knowledge-base entries.

The configured retrieval depth is `top_k = 3`.

Root-cause entries and recovery actions are embedded and ranked separately. The incident query incorporates available exception information, classification fields, workflow information, and activity information.

The experiment examines:

- Whether the top-ranked root-cause entries are relevant to the known incident.
- Whether the top-ranked recovery actions are appropriate for the incident.
- Whether semantic retrieval returns weakly relevant candidates for an unknown incident.
- Whether retrieval remains useful when the wording or exception type changes.

No calibrated retrieval-abstention threshold is used in the reported experiment. Similarity ranking is therefore not treated as proof that a candidate is relevant.

Retrieval relevance is assessed separately from the quality of the generated RCA report.

## 5. Verification-Assisted Revision

The verified configurations generate an initial RCA, submit it to a verification stage, and use the verification findings to request a revised report when required.

The evaluation examines whether the process identifies or removes:

- Unsupported claims and assumptions
- Details presented as evidence that were not supplied
- Root causes not supported by incident information or retrieved knowledge
- Recovery actions not supported by retrieved knowledge
- Incorrect confidence assessments
- Unsupported prevention recommendations
- Inadequate handling of insufficient evidence

Three aspects are considered separately:

1. **Verifier assessment:** The recorded verification outcome, such as `PASS` or `NEEDS_REVISION`.
2. **Revision behaviour:** The changes made in response to verification findings.
3. **Final-report grounding:** Whether the revised report's substantive claims remain supported by the permitted evidence.

A verification result is an assessment produced by the implemented verifier. It is not an independent guarantee that the report is correct, that retrieved knowledge is relevant, or that every unsupported statement has been detected.

## 6. Evaluation Criteria

### 6.1 Retrieval Relevance

Assess whether the retrieved root-cause entries and recovery actions are relevant to the incident.

For known incidents, compare the retrieved entries with the expected knowledge. For the Unknown Incident, examine whether the system returns candidates despite insufficient relevance.

Retrieval relevance is evaluated independently of the verifier's assessment of the generated report.

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
- The system abstains from confirming a root cause when the evidence is insufficient.

A verifier `PASS` does not independently demonstrate successful unknown-incident handling or reliable retrieval abstention.

## 7. Comparison Strategy

The four configurations support the following comparisons:

| Comparison | Evaluation Purpose |
|---|---|
| Structured RCA vs. Semantic RCA | Examines the effect of retrieval strategy without verification-assisted revision. |
| Structured RCA vs. Verified Structured RCA | Examines the effect of verification-assisted revision with structured retrieval. |
| Semantic RCA vs. Verified Semantic RCA | Examines the effect of verification-assisted revision with semantic retrieval. |
| Verified Structured RCA vs. Verified Semantic RCA | Compares retrieval strategies when verification-assisted revision is enabled. |

These comparisons are controlled in design intent. Their interpretation still depends on the consistency of model settings, prompts, test inputs, and evaluation procedures across configurations.

The results should also be interpreted in light of the small test set and the qualitative nature of the case-level assessments.

## 8. Limitations

The evaluation uses a small set of manually assessed incident cases. The findings should therefore be interpreted as exploratory rather than as a general performance guarantee.

The principal limitations are:

- The test set is small and does not establish statistical generalization.
- The paraphrased UI-selector case tests one variation in wording and does not establish broad robustness to paraphrasing.
- Semantic similarity can rank related but irrelevant entries.
- The fixed top-k retrieval configuration does not include a calibrated abstention threshold.
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
- A report can appear grounded while relying on weakly relevant retrieved candidates.
- Verification can identify unsupported claims without identifying every retrieval-quality problem.
- Revision can remove unsupported statements while introducing new assumptions.
- A verifier's `PASS` does not guarantee that the report is correct or that the system has reliably handled an unknown incident.

Future evaluations should therefore assess retrieval relevance independently, track changes between initial and revised reports, and investigate calibrated abstention when the available knowledge is insufficient.

The current methodology provides an initial framework for comparing structured retrieval, semantic retrieval, and verification-assisted revision. Broader conclusions will require larger test sets, reproducible evaluation procedures, and independent assessment of final-report quality.
