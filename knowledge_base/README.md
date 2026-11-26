
# Knowledge Base

This directory contains the structured knowledge used by Intelligent Automation RCA for incident classification, root-cause retrieval, and recovery-action retrieval.

The current knowledge base focuses on UiPath automation incidents.

## 1. Knowledge Base Files

### incident_taxonomy.xlsx

Contains:

- **Taxonomy:** Defines incident categories, subcategories, and descriptions.
- **Incident Catalog:** Maps recognized exception patterns to incident identifiers and taxonomy labels.

### root_cause_library.xlsx

Contains possible root causes associated with incident categories and subcategories.

Entries include root-cause identifiers, descriptions, qualitative confidence labels, and suggested verification methods.

Knowledge-base confidence labels are qualitative and should not be interpreted as calibrated probabilities.

### recovery_library.xlsx

Contains suggested recovery actions associated with incident categories and subcategories.

Entries include recovery identifiers, recommended actions, automation levels, and additional notes.

Recovery actions should be reviewed against the actual incident context before execution.

## 2. Knowledge Base Usage

The knowledge base supports:

- Rule-based incident classification.
- Structured root-cause retrieval.
- Structured recovery-action retrieval.
- Embedding-based semantic retrieval.
- Context provision for LLM-assisted RCA generation.

Retrieved knowledge represents possible explanations and recovery strategies. It does not independently establish the actual cause of an incident.

## 3. Scope and Coverage

The current implementation focuses on UiPath incident patterns represented in the supplied workbooks.

Coverage is limited to the categories, exception patterns, root causes, and recovery actions currently included.

Incidents outside this coverage may remain unclassified or return weakly relevant semantic retrieval candidates.

Support for additional automation platforms is considered future work.

## 4. Provenance and Maintenance

New knowledge-base entries should have traceable sources and review information.

Recommended maintenance information includes:

- Entry identifier
- Source or reference
- Source type
- Whether the entry is manually authored or source-derived
- Validation status
- Last reviewed date

Entries should not be described as independently validated unless a defined validation process has been completed.

## 5. Limitations

- Knowledge-base coverage is finite.
- Root causes represent possible explanations, not confirmed diagnoses.
- Recovery actions may require human review.
- Semantic similarity does not guarantee incident-specific relevance.
- Retrieval quality depends on the coverage and quality of the knowledge base.
