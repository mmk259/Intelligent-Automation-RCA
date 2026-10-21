
# Backend Modules

This directory contains the FastAPI application, incident-processing pipeline, retrieval components, RCA generation modules, and verification experiments.

## Application and Data Processing

| File | Responsibility |
|---|---|
| `app/main.py` | Defines the FastAPI application and exposes the analysis endpoints. |
| `app/models.py` | Defines the Pydantic request and response models used by the API. |
| `app/parser.py` | Parses UiPath execution logs and extracts structured incident information. |
| `app/classifier.py` | Maps extracted incident information to the predefined incident taxonomy. |
| `app/knowledge_loader.py` | Loads the Excel-based incident taxonomy and knowledge libraries. |

## Retrieval and Generation

| File | Responsibility |
|---|---|
| `app/retriever.py` | Retrieves root-cause knowledge using the structured retrieval approach. |
| `app/recovery_engine.py` | Retrieves recovery actions using the structured approach. |
| `app/semantic_rca_generator.py` | Implements embedding-based semantic retrieval of root-cause entries and recovery actions. |
| `app/llm_integration.py` | Configures the Ollama client and provides the shared LLM-generation function. |
| `app/structured_rca_generator.py` | Formats structured RCA output using the incident, classification, retrieved knowledge, and generated content. |

## Verification Experiments

| File | Responsibility |
|---|---|
| `app/structured_verification.py` | Implements verification-assisted revision for the structured-retrieval configuration. |
| `app/semantic_verification.py` | Combines semantic retrieval with verification-assisted RCA revision. |

## Request Flow

The main API entry point is `app/main.py`. Depending on the endpoint, a request is parsed, classified, and processed using structured retrieval, semantic retrieval, or verification-assisted revision.

The semantic retrieval endpoint returns retrieved candidates; it should not be described as producing a complete RCA report unless its implementation is changed.

The verification components assess generated content and may request a revised report. Their presence does not guarantee that every statement in the final report is fully grounded in the available evidence.

## Dependencies and Configuration

Install the dependencies listed in `requirements.txt`.

LLM-based endpoints also require an appropriate Ollama connection and model configuration, as specified in `app/llm_integration.py`.

Do not commit credentials, API keys, environment files, or confidential production logs.
