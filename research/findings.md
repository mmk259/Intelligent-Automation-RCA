
# Research Findings

## 1. Summary

The experiments examined structured retrieval, embedding-based semantic retrieval, and verification-assisted revision for AI-generated Root Cause Analysis (RCA) reports.

The findings indicate that **retrieval relevance, report grounding, and uncertainty handling are related but distinct requirements**. Improvements in one area do not automatically guarantee improvements in the others.

## 2. Semantic Retrieval

The semantic retrieval evaluation used the `all-MiniLM-L6-v2` embedding model, cosine similarity, and `top_k = 3`.

Across the five known incident cases, the expected root cause was ranked first in four cases, and the expected recovery action was ranked first in four cases.

The Missing File, Network Path, Terminal Session, and Timeout cases produced relevant top-ranked knowledge. The exact UI-selector case retrieved related but incorrect entries.

The paraphrased UI-selector case demonstrated partial robustness: semantic retrieval returned UI- and application-related candidates even though structured classification did not identify the incident. However, the retrieved entries were not sufficiently specific to establish a reliable selector diagnosis.

The Unknown Incident exposed a different failure mode. Semantic retrieval returned nearest-neighbour candidates despite the absence of a known incident classification. Similarity ranking alone did not provide reliable abstention.

**Finding:** Semantic retrieval can improve matching across some variations in incident wording, but it can also retrieve related yet unsuitable knowledge. Retrieval relevance must be assessed separately from similarity ranking.

## 3. Verification-Assisted Revision

The saved verification results indicate that the V2 verifier identified substantive grounding problems in all six structured RCA cases. The semantic verification experiment identified substantive problems in five of six cases and returned `PASS` for the Unknown Incident.

The revision stage generally improved aspects of grounding and uncertainty handling. It also removed unsupported prevention recommendations in several cases.

However, the revised reports sometimes retained or introduced technically plausible explanations and assumptions that were not directly traceable to the permitted incident information, classification, or retrieved knowledge.

### Unknown Incident: Retrieval and Verification Limitation

The Unknown Incident exposed a limitation in the combined semantic-retrieval and verification configuration. Semantic retrieval returned nearest-neighbour root-cause and recovery candidates despite the absence of a known incident classification. The verification stage returned `PASS` for the generated RCA in this case, even though the retrieved candidates were weakly relevant.

This result shows that verification of generated report content and evaluation of retrieval relevance are separate requirements. A report can pass the implemented verification check without establishing that the retrieved knowledge is sufficiently relevant to the incident.

The result should not be interpreted as evidence that the combined system reliably abstains on unknown incidents. Future evaluation should assess retrieval relevance explicitly and investigate a calibrated abstention mechanism.

**Finding:** Verification-assisted revision can help identify unsupported report content, but it does not guarantee that the revised report is fully grounded or that the retrieved knowledge is relevant. A verifier's `PASS` is its recorded assessment under the implemented criteria, not an independent guarantee of report correctness.

## 4. Combined System Implications

The combined configuration integrates semantic retrieval with verification-assisted revision, but the limitations of both components remain important.

- Semantic retrieval may return weak candidates for unknown incidents.
- A verifier may assess generated report content without detecting that the retrieval stage supplied unsuitable knowledge.
- A revision can remove one unsupported statement while introducing another.
- A plausible root cause is not necessarily a confirmed root cause.
- Knowledge-base confidence should not be treated as incident-specific confidence.
- A verifier's `PASS` should not be treated as proof of correctness.
- Retrieval relevance, report grounding, and uncertainty handling require separate evaluation.

These observations motivate explicit assessment of retrieval relevance, evidence grounding, uncertainty handling, and revision quality.

## 5. Limitations

The test set is small and uses manually assessed cases. The results do not establish statistical generalization or production-level reliability.

Additional limitations include:

- The knowledge base is relatively small and manually authored.
- The paraphrased UI-selector case is a limited robustness test, not a comprehensive paraphrase evaluation.
- The semantic retriever uses a fixed top-k value of three without a calibrated similarity threshold or abstention mechanism.
- The experiments do not establish that semantic retrieval will generalize to other automation platforms.
- The verifier is itself LLM-based and may produce false-positive or false-negative assessments.
- The revised reports have not been independently validated through a comprehensive human-expert evaluation.
- The limited test set does not establish the system's ability to resolve previously unseen production incidents.

The results should therefore be interpreted as exploratory engineering findings rather than evidence that the system can autonomously resolve production incidents.

## 6. Future Research Directions

1. **Evaluate retrieval relevance independently.** Assess whether retrieved root-cause and recovery candidates are appropriate for each incident, separately from the generated RCA report.
2. **Investigate calibrated abstention.** Determine when similarity scores and other retrieval signals are insufficient to support a diagnosis.
3. **Extend verification coverage.** Evaluate whether verification checks both report grounding and retrieval relevance.
4. **Measure revision quality.** Track which unsupported claims are removed, which are retained, and whether new unsupported statements are introduced.
5. **Expand the evaluation dataset.** Include more incident categories, paraphrases, ambiguous logs, and unknown incidents.
6. **Improve experimental reproducibility.** Record model configurations, prompt versions, retrieval settings, verifier decisions, and revision outputs for each experiment.
7. **Introduce independent assessment.** Use explicit evaluation criteria and, where feasible, expert-reviewed annotations to assess final-report grounding and diagnostic quality.

## 7. Conclusion

The central finding is that reliable AI-assisted RCA requires more than semantic matching or a verification step alone.

The system must retrieve relevant knowledge, distinguish observed evidence from hypotheses, communicate uncertainty accurately, and avoid introducing unsupported claims during report generation and revision.

The current experiments suggest that structured retrieval, semantic retrieval, and verification-assisted revision address different aspects of the problem. However, retrieval relevance, verifier assessment, and final-report correctness remain distinct concerns.

Further evaluation is needed before making broader claims about reliability, generalization, or production readiness.
