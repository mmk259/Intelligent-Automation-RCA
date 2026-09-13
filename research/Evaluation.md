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

- Structured incident classification
- Structured root-cause retrieval
- Structured recovery retrieval
- Single-pass LLM-based RCA generation

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

- Embedding model: `all-MiniLM-L6-v2`
- Similarity metric: cosine similarity
- Root-cause retrieval: top-k = 3
- Recovery retrieval: top-k = 3
- LLM generation: not included in this experiment

The six baseline cases were reused to enable direct comparison with
structured retrieval.

An additional paraphrased UI-selector case was introduced to test
robustness to changes in wording and exception type. This case is
treated as an additional robustness test rather than a direct
baseline comparison.

The complete semantic retrieval outputs are preserved in
`research/results/semantic_rag_results.json`.

---

## 3. Baseline vs Semantic Retrieval

| Incident         | Baseline Root Cause | Semantic Root Cause | Baseline Recovery | Semantic Recovery |
|------------------|---------------------|---------------------|-------------------|-------------------|
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
nearest neighbour retrieval. Because the system always returns the
top three results, it produces candidate knowledge even when no
sufficiently relevant knowledge exists.

---

## 4. Paraphrase Robustness

The additional paraphrased UI-selector case changed the wording of
the failure and used a different exception type while describing the
same underlying incident.

Structured classification did not identify the incident:

- Incident ID: None
- Category: None
- Confidence: 0

Semantic retrieval nevertheless returned UI-, configuration-, and
application-related knowledge. However, the retrieved results did
not contain the selector-specific root causes or recovery actions.

This indicates partial robustness to changed wording, but not
sufficient retrieval specificity for reliable diagnosis.

---

## 5. Failure Analysis

### 5.1 UI Selector Failure

The semantic retriever ranked configuration scope, UI input state,
and application state above selector-specific root causes.

This suggests that the embedding representation captures broad
semantic relationships between UI failures but does not reliably
distinguish closely related failure modes within the current
knowledge base.

### 5.2 Unknown Incident False Positives

The unknown incident produced three retrieved root causes and three
recovery actions despite having no known classification.

This is an important limitation of the current implementation:
semantic nearest neighbour retrieval does not inherently provide an
abstention mechanism.

A future controlled experiment may investigate similarity thresholds
or other abstention strategies. These mechanisms were intentionally
not introduced into the current experiment so that the initial
semantic retrieval results remain an uncontrolled baseline for that
future investigation.

---

## 6. Limitations

The current evaluation has several limitations:

- The evaluation set is small and manually constructed.
- The knowledge base is relatively small and manually authored.
- Similarity scores are retrieval scores and are not calibrated
  probabilities.
- The semantic experiment uses a fixed top-k value of 3.
- No similarity threshold or abstention mechanism was applied.
- The embedding model was not specifically fine-tuned for automation
  failure logs.
- The semantic retrieval experiment evaluates retrieval independently
  of LLM-generated RCA quality.
- The paraphrased test set currently contains a single additional
  paraphrased incident.

These limitations mean that the results should be interpreted as
an initial controlled engineering experiment rather than evidence
of general retrieval performance.

---

## 7. Current Findings

The semantic retrieval experiment shows that embedding-based
retrieval can successfully identify relevant knowledge for several
known automation incidents, while also introducing failure modes
that are not present in the structured retrieval baseline.

In particular:

1. Semantic retrieval correctly handled Missing File, Network Path,
   Terminal Session, and Timeout cases.
2. Semantic retrieval performed poorly on the exact UI-selector case.
3. Semantic retrieval showed partial robustness to a paraphrased
   UI-selector incident but did not retrieve sufficiently specific
   knowledge.
4. Semantic retrieval produced false-positive knowledge for an
   unknown incident.
5. Therefore, semantic similarity is useful as a retrieval mechanism
   but is not sufficient on its own for reliable automation RCA.

These findings motivate evaluation of additional mechanisms for
improving the reliability of the generated RCA rather than assuming
that semantic retrieval alone solves the diagnosis problem.