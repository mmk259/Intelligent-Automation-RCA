# AI Diagnosis Pipeline


## Objective

The AI Diagnosis Pipeline transforms raw UiPath execution logs into a structured Root Cause Analysis (RCA) report by combining deterministic knowledge retrieval with LLM-based reasoning.


## Pipeline Workflow


UiPath Execution Log

        │
        ▼
Log Parser
(Extract Exception, Workflow, Activity, Timestamp)

        │
        ▼
Incident Classification
(Search Incident Catalog)

        │
        ▼
Incident Identified
(UI-003)

        │
        ▼
Retrieve Incident Taxonomy
(Category, Subcategory)

        │
        ▼
Retrieve Possible Root Causes
(Root Cause Library)

        │
        ▼
Retrieve Recovery Actions
(Recovery Library)

        │
        ▼
Build Structured Context
(Exception + Incident + Root Causes + Recovery + Execution Context)

        │
        ▼
LLM Reasoning Engine

        │
        ▼
Generate Professional RCA Report


## Example

* Input
Exception:
NodeNotFoundException

Workflow:
Loan_Disbursal.xaml

Activity:
Click Submit

Timestamp:
2026-07-16 10:42

* Step 1
Extract Exception
NodeNotFoundException

* Step 2
Search Incident Catalog
UI-003

* Step 3
Retrieve Taxonomy
Category:
UI Automation

Subcategory:
Selector

* Step 4
Retrieve Root Causes
• Selector changed
• Dynamic selector
• Application not loaded

* Step 5
Retrieve Recovery Actions
• Validate selector
• Retry activity
• Inspect selector using UI Explorer

* Step 6
Provide Context to the LLM
The LLM receives:
Exception
Workflow
Activity
Category
Subcategory
Possible Root Causes
Recovery Actions
Execution Context

* Step 7
Generate RCA Report
The LLM produces:
Incident Summary
Root Cause Analysis
Supporting Evidence
Recommended Recovery
Prevention Recommendations
Confidence Score


## Why This Design?

The AI Diagnosis Pipeline separates deterministic reasoning from generative reasoning.

* Deterministic Components (Python)

Python is responsible for tasks that require consistent and repeatable results, including:
Parsing UiPath execution logs
Extracting exceptions and execution context
Classifying incidents using the Incident Catalog
Retrieving relevant root causes from the Root Cause Library
Retrieving recovery actions from the Recovery Library

* Generative Component (LLM)

The Large Language Model (LLM) is responsible for tasks that benefit from natural language understanding and generation, including:
Explaining the incident in human-readable language
Summarizing probable root causes
Generating professional RCA reports
Providing clear recovery and prevention recommendations

* Benefits of This Design

Reduces LLM hallucinations by grounding responses in a structured knowledge base.
Ensures consistent incident classification through deterministic logic.
Improves reliability and explainability of AI-generated reports.
Enables independent updates to the knowledge base without modifying the AI model.
Provides a scalable architecture for future enterprise RPA incident management systems.
