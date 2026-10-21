
# AI Diagnosis Pipeline

## 1. Objective

The AI Diagnosis Pipeline analyzes UiPath execution logs using structured incident parsing, classification, knowledge-base retrieval, and LLM-based Root Cause Analysis (RCA) generation.

The implementation supports structured retrieval, semantic retrieval, and experimental verification-assisted revision. These capabilities are exposed through separate API endpoints and should not be treated as a single identical processing sequence.

The pipeline provides candidate root causes and recovery recommendations based on the available incident evidence and predefined knowledge base. It does not independently confirm that a proposed root cause actually occurred.

---

## 2. Pipeline Workflow

### 2.1 Shared Input Processing

The main processing paths begin with the following steps:

```text
UiPath Execution Log
        |
        v
FastAPI Application
        |
        v
Automation Log Parser
        |
        v
Incident Classification
        |
        v
Structured Incident Context
```

The parser extracts available incident information, such as exception details and execution context. The classifier maps the incident to the predefined taxonomy when possible.

The quality of the resulting context depends on the information available in the input log and the capabilities of the implemented parser and classifier.

### 2.2 Processing Configurations

The system exposes four configurations for different retrieval and RCA-generation experiments.

```text
Structured Incident Context
        |
        v
   API Endpoint
        |
        +-------------------------------+
        |               |               |
        v               v               v
   /analyze         /analyze/       /analyze/
                    semantic        verified
        |               |               |
        v               v               v
 Structured         Semantic        Structured
 Retrieval          Retrieval       Retrieval
        |               |               |
        v               v               v
 LLM-Based          Return          LLM-Based
 RCA Generation     Candidates      RCA Generation
        |                               |
        v                               v
 Format RCA                        Verification
 Report                            and Revision
                                        |
                                        v
                                   Revised RCA

                 /analyze/combined
                         |
                         v
                 Semantic Retrieval
                         |
                         v
                 LLM-Based RCA
                   Generation
                         |
                         v
                 Verification
                   and Revision
                         |
                         v
                   Revised RCA
```

### 2.3 Endpoint Responsibilities

| Endpoint | Processing Path | Output |
|---|---|---|
| `/analyze` | Structured retrieval followed by LLM-based RCA generation and report formatting. | Structured RCA report. |
| `/analyze/semantic` | Embedding-based semantic retrieval. | Ranked root-cause and recovery knowledge candidates; not a complete RCA report. |
| `/analyze/verified` | Structured retrieval followed by RCA generation and verification-assisted revision. | Verification-assisted RCA report. |
| `/analyze/combined` | Semantic retrieval followed by RCA generation and verification-assisted revision. | Verification-assisted RCA report using semantic retrieval. |

The semantic retrieval endpoint is primarily a retrieval experiment. It should not be described as generating a complete RCA report.

---

## 3. Example: UiPath UI Automation Incident

**Example input:** The following is an illustrative incident, not evidence of a particular production incident.

### Input Exception

```text
Exception : NodeNotFoundException
Workflow  : Loan_Disbursal.xaml
Activity  : Click Submit
Timestamp : 2026-07-16 10:42
```

### Step 1 — Parse Execution Log

The parser extracts the available incident information, which may include:

- Exception message
- Workflow
- Activity
- Timestamp
- Other available execution context

### Step 2 — Classify Incident

The classifier attempts to map the extracted information to the predefined incident taxonomy.

Illustrative classification:

```text
UI-003
```

The classification depends on the implemented rules and the information in the input. Unrecognized or ambiguous incidents may not receive a reliable classification.

### Step 3 — Retrieve Diagnostic Knowledge

The selected retrieval method identifies relevant knowledge-base entries.

For a selector-related incident, candidate root causes might include:

- A selector has changed.
- The selector depends on dynamic attributes.
- The target application or UI element was not ready.

Candidate recovery actions might include:

- Inspecting and validating the selector.
- Checking whether the target application is ready.
- Inspecting the UI element using UiPath UI Explorer.

These are illustrative candidates, not confirmed findings about the example incident.

### Step 4 — Generate RCA Content

For endpoints that generate an RCA, the LLM receives the available incident context and retrieved diagnostic knowledge.

Depending on the pipeline and report format, the generated content may include:

- Incident summary
- Probable root-cause explanation
- Supporting evidence
- Recovery recommendations
- Prevention recommendations
- Confidence or uncertainty information, where supported by the implementation

The report should distinguish facts available in the log from hypotheses suggested by the knowledge base.

### Step 5 — Verification-Assisted Revision

The verified configurations evaluate generated report content against the available incident context and retrieved information.

If the verifier identifies issues, the system can request a revision. This is an experimental verification-assisted process, not a guarantee that every statement in the final report is correct.

---

## 4. Structured and Semantic Retrieval

### 4.1 Structured Retrieval

Structured retrieval uses the incident context and the implemented knowledge-base matching logic to identify diagnostic entries.

Its performance depends on factors such as:

- The quality of incident parsing and classification
- The coverage of the predefined taxonomy
- The structure and completeness of the knowledge base
- The ability of the matching logic to identify relevant entries

### 4.2 Semantic Retrieval

The current semantic retrieval experiment uses the `all-MiniLM-L6-v2` embedding model and cosine similarity to rank knowledge-base entries. The configured retrieval process returns the top three candidates.

Semantic similarity is a **ranking signal, not confirmation of a root cause**. A high-ranked candidate may be related in meaning without accurately explaining the incident.

Semantic retrieval may also return weakly relevant candidates for unfamiliar incidents. The current retrieval behavior should not be interpreted as reliable automatic rejection of unknown incidents.

### 4.3 Retrieval Relevance and Verification Are Different

Retrieval relevance and generated-report verification assess different aspects of the pipeline.

- **Retrieval relevance:** Are the selected knowledge-base entries appropriate for the incident and its evidence?
- **Report verification:** Is the generated RCA content adequately supported by the context and retrieved information available to the verifier?

Verification of report content does not guarantee that the retrieved candidates are relevant. A report may receive a `PASS` outcome even when retrieval quality remains a concern.

For this reason, retrieval relevance, report grounding, uncertainty handling, and verifier outcomes should be evaluated separately.

---

## 5. Why This Design?

The pipeline separates deterministic processing from generative reasoning while allowing different retrieval and verification configurations to be compared.

### 5.1 Deterministic Components

Python modules handle tasks such as:

- Parsing supported UiPath execution-log formats
- Extracting available incident context
- Classifying incidents using the predefined taxonomy
- Retrieving knowledge-base entries through the implemented retrieval methods
- Preparing structured inputs for RCA generation and verification

Deterministic processing improves consistency for supported inputs, but its effectiveness depends on the implemented logic and the quality of the input data.

### 5.2 Generative Components

The LLM integration and RCA-generation modules support tasks such as:

- Explaining probable causes in natural language
- Summarizing diagnostic context
- Generating structured RCA content
- Producing recovery and prevention recommendations
- Revising generated content when the verification process identifies issues

LLM-generated explanations remain subject to error. Retrieved knowledge and verification can support grounding, but they do not independently establish the actual cause of an incident.

### 5.3 Benefits and Trade-offs

- Separates incident parsing and classification from natural-language report generation.
- Enables structured and semantic retrieval approaches to be evaluated independently.
- Allows verification-assisted revision to be compared with single-pass RCA generation.
- Makes diagnostic knowledge easier to update independently of the LLM.
- Provides a basis for future extensions while keeping current capabilities distinct from planned work.

---

## 6. Limitations

The current implementation has several important limitations:

- **Platform scope:** The parser is UiPath-specific; additional automation-platform connectors are not current capabilities unless separately implemented and evaluated.
- **Knowledge-base dependence:** The quality of candidate causes and recovery actions depends on the available diagnostic knowledge.
- **Semantic retrieval:** Similarity rankings do not guarantee incident-specific relevance.
- **Classification:** Unfamiliar or ambiguous incidents may not be classified correctly.
- **Verification:** A verifier outcome does not guarantee factual correctness or relevant retrieval.
- **Evaluation scope:** Experimental results apply to the tested incidents and configurations and do not establish production-level diagnostic reliability.
- **Autonomous repair:** The pipeline does not demonstrate autonomous production-code modification, deployment, or repair.

---

## 7. Future Work

Potential future extensions include:

- Platform-specific connectors for Automation Anywhere, Microsoft Power Automate, Blue Prism, and other automation systems.
- Broader incident datasets and evaluation across additional log formats.
- Improved handling of paraphrased incidents and previously unseen failure types.
- Explicit retrieval-relevance evaluation and calibrated abstention when the evidence is insufficient.
- Stronger verification procedures that separately assess factual grounding, retrieval relevance, and uncertainty.
- Investigation of multi-agent reasoning, if supported by a concrete design and evaluated implementation.
- Exploration of code-repair recommendations or automated repair workflows, with appropriate safeguards and testing before any production use.

These items describe possible future directions. They should not be presented as implemented features until they have been built and evaluated.