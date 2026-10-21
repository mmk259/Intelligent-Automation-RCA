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

| Configuration | Retrieval | Verification-assisted revision |
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
```

## Setup

Use Python 3.11 or another Python version compatible with the dependencies in `backend/requirements.txt`.

### 1. Create a Virtual Environment

Run the following command from the repository root:

```bash
python -m venv .venv
```

### 2. Activate the Virtual Environment

**Windows PowerShell:**

```powershell
.venv\Scripts\Activate.ps1
```

**macOS/Linux:**

```bash
source .venv/bin/activate
```

### 3. Install Dependencies

From the repository root, run:

```bash
python -m pip install -r backend/requirements.txt
```

### 4. Start the API

Navigate to the backend directory:

```bash
cd backend
```

Start the FastAPI development server:

```bash
uvicorn app.main:app --reload
```

Once the server is running, access the following URLs:

- **API root:** http://127.0.0.1:8000/
- **Interactive API documentation:** http://127.0.0.1:8000/docs

**LLM configuration:** Check `backend/app/llm_integration.py` for the configured model and Ollama connection requirements. Configure the required connection and model access before using endpoints that generate RCA reports.

Do not commit API keys, credentials, environment files, or confidential production logs.

> **Note:** Python 3.11 is a suggested environment, not a verified compatibility guarantee. Test installation and execution in a clean environment before treating a Python version as officially supported.

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Check whether the API is running |
| POST | `/analyze` | Structured retrieval and RCA generation |
| POST | `/analyze/semantic` | Return semantic retrieval candidates |
| POST | `/analyze/verified` | Structured retrieval with verification-assisted revision |
| POST | `/analyze/combined` | Semantic retrieval with verification-assisted revision |

Submit requests through the interactive API documentation at `/docs`, using the request schema defined in `backend/app/models.py`.

The semantic retrieval endpoint returns retrieval candidates; it should not be described as generating a complete RCA report unless its implementation supports that behavior.

## Research and Evaluation

The evaluation artifacts are stored in `research/results/`.

The shared test set contains six incident cases:

1. Missing File
2. UI Selector
3. Network Path
4. Terminal Session
5. Timeout
6. Unknown Incident

An additional paraphrased UI-selector case was used to examine robustness to changed wording.

The experiments investigate:

- Whether semantic retrieval retrieves relevant knowledge for known incidents
- Whether semantic retrieval produces false-positive candidates for unknown incidents
- Whether verification identifies unsupported statements
- Whether report revision improves grounding and uncertainty handling
- Whether verification detects retrieval-relevance failures

The experiments compare four configurations: Structured RCA, Semantic RCA, Verified Structured RCA, and Verified Semantic RCA.

See [Evaluation](research/Evaluation.md) and the [Documentation](docs/README.md) for further details.

## Limitations

- The current log parser is UiPath-specific.
- The evaluation uses a small, manually assessed test set.
- Semantic retrieval can return weakly related candidates when no sufficiently relevant entry exists.
- Verification-assisted revision may introduce new unsupported domain reasoning.
- The experiments do not establish production-level reliability or generalization to other automation platforms.
- The system supports diagnosis and report generation; it is not an autonomous production-code repair system.

## Future Work

- Add retrieval abstention and relevance evaluation.
- Evaluate on a larger and more diverse incident set.
- Improve grounding checks across both retrieved knowledge and generated reports.
- Evaluate repeatability across model runs and configurations.
- Investigate additional automation platforms through dedicated log connectors.
- Explore a user interface and controlled enterprise deployment.

## License

No license has been specified in this repository. Unless a license is added, others should not assume that they have permission to reuse, modify, or redistribute the code.