# Intelligent Automation RCA

An AI-assisted Root Cause Analysis (RCA) system for diagnosing automation failures from execution logs. The project combines structured incident classification, knowledge-base retrieval, LLM-generated RCA reports, semantic retrieval experiments, and verification-assisted report revision.

**Current implementation:** UiPath execution-log parsing and a knowledge base containing incident taxonomy, root-cause entries, and recovery actions.

**Research focus:** Evaluating how semantic retrieval and verification-assisted revision affect the relevance, grounding, and uncertainty handling of generated RCA reports.

## Problem

Automation engineers often need to investigate execution logs, identify possible causes, locate recovery procedures, and communicate findings. This project explores how an AI-assisted system can support that process while distinguishing observed evidence, retrieved knowledge, and unverified hypotheses.

## Features

- UiPath log parsing into structured incident information
- Incident classification using a predefined taxonomy
- Structured root-cause and recovery-action retrieval
- Embedding-based semantic retrieval using Sentence Transformers
- LLM-assisted RCA report generation
- Verification-assisted revision of generated RCA reports
- FastAPI endpoints for the implemented analysis configurations
- Evaluation using six shared incident cases and an additional paraphrased UI-selector case

## System Overview

The implemented pipeline is:

1. Parse the UiPath execution log.
2. Classify the incident using the incident taxonomy.
3. Retrieve root-cause knowledge and recovery actions.
4. Generate an RCA report using the retrieved information and an LLM.
5. In experimental configurations, use semantic retrieval and/or verification-assisted revision.

The semantic retrieval and verification components are experimental. Semantic similarity does not guarantee that a retrieved entry is relevant, and verification-assisted revision does not guarantee that every statement in the final report is fully grounded.

## Experimental Configurations

| Configuration | Retrieval | Verification-Assisted Revision |
|---|---|---|
| Structured RCA | Structured | No |
| Semantic RCA | Semantic | No |
| Verified Structured RCA | Structured | Yes |
| Verified Semantic RCA | Semantic | Yes |

The configurations are compared to examine retrieval behavior, report grounding, uncertainty handling, and the limitations of combining semantic retrieval with verification.

## Technology Stack

- Python
- FastAPI
- Pandas and OpenPyXL
- Sentence Transformers
- Ollama Python client
- Large Language Models (LLMs)
- Excel-based knowledge libraries

## Repository Structure

```text
Intelligent-Automation-RCA/
├── backend/
│   ├── app/
│   ├── tests/
│   ├── README.md
│   └── requirements.txt
├── knowledge_base/
│   ├── incident_taxonomy.xlsx
│   ├── root_cause_library.xlsx
│   └── recovery_library.xlsx
├── docs/
├── research/
│   ├── Evaluation.md
│   └── results/
├── dataset/
├── frontend/
├── tests/
└── README.md