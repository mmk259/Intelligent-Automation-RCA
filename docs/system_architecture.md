## Project Objective

Intelligent RPA RCA is an AI-assisted incident diagnosis system for enterprise robotic process automation. The system analyzes automation failures, classifies incidents, identifies likely root causes, recommends recovery actions, and generates professional Root Cause Analysis (RCA) reports to assist RPA developers.


## System Workflow

RPA Execution Log

        │
        ▼
Exception Extraction

        │
        ▼
Incident Classification

        │
        ▼
Knowledge Base Retrieval

        │
        ├───────────────┐
        ▼               ▼
Root Cause Library   Recovery Library

        │               │
        └───────┬───────┘
                ▼
        LLM Reasoning Engine
        
                │
                ▼
      Professional RCA Report


## Components

1. Log Parser
Extracts the important exception from UiPath execution logs.
Example:
NodeNotFoundException

2. Incident Classifier
Maps the exception to the Incident Catalog.
Example:
NodeNotFoundException
↓
UI-003
↓
UI → Selector

3. Knowledge Base
Contains
Incident Taxonomy
Incident Catalog
Root Cause Library
Recovery Library

4. LLM Reasoning
The LLM receives:
incident
possible causes
recovery actions
and writes an RCA instead of inventing one.

5. RCA Generator
Produces a structured report.
Example sections:
Incident Summary
Probable Root Cause
Supporting Evidence
Recommended Recovery
Prevention Suggestions
