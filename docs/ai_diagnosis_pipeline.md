# AI Diagnosis Pipeline

## Objective

The AI Diagnosis Pipeline transforms raw automation execution logs into a structured Root Cause Analysis (RCA) report by combining deterministic knowledge retrieval with LLM-based reasoning.

---

# Pipeline Workflow

```text
Enterprise Automation Platform
        │
(API / Log Export/ Webhook)
        ▼
Platform Connector
        │
        ▼
Automation Log Parser
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
(Exception + Incident + Root Causes +
Recovery + Execution Context)
        │
        ▼
LLM Reasoning Engine
        │
        ▼
Generate Professional RCA Report
```

---

# Example

**Initial implementation:** UiPath

### Input Exception

```
Exception : NodeNotFoundException
Workflow  : Loan_Disbursal.xaml
Activity  : Click Submit
Timestamp : 2026-07-16 10:42
```

### Step 1 — Parse Execution Log

Extract:

- Exception
- Workflow
- Activity
- Timestamp

### Step 2 — Classify Incident

Search Incident Catalog

```
UI-003
```

### Step 3 — Retrieve Taxonomy

Category

```
UI Automation
```

Subcategory

```
Selector
```

### Step 4 — Retrieve Root Causes

- Selector changed
- Dynamic selector
- Application not loaded

### Step 5 — Retrieve Recovery Actions

- Validate selector
- Retry activity
- Inspect selector using UI Explorer

### Step 6 — Build AI Context

The LLM receives:

- Exception
- Workflow
- Activity
- Incident ID
- Category
- Subcategory
- Possible Root Causes
- Recovery Actions
- Execution Context

### Step 7 — Generate RCA Report

The system generates:

- Incident Summary
- Root Cause Analysis
- Supporting Evidence
- Recovery Recommendations
- Prevention Recommendations
- Confidence Score

---

# Why This Design?

The AI Diagnosis Pipeline separates **deterministic reasoning** from **generative reasoning**.

## Deterministic Components (Python)

Python is responsible for tasks that require consistent and repeatable results, including:

- Parsing automation execution logs
- Extracting exceptions and execution context
- Classifying incidents using the Incident Catalog
- Retrieving relevant root causes from the Root Cause Library
- Retrieving recovery actions from the Recovery Library

## Generative Component (LLM)

The Large Language Model (LLM) is responsible for tasks that benefit from natural language understanding and generation, including:

- Explaining incidents in human-readable language
- Summarizing probable root causes
- Generating professional RCA reports
- Providing clear recovery and prevention recommendations

## Benefits of This Design

- Grounds AI responses in a structured knowledge base, reducing hallucinations.
- Ensures consistent incident classification through deterministic logic.
- Improves the reliability and explainability of AI-generated reports.
- Enables independent updates to the knowledge base without modifying the AI model.
- Provides a scalable architecture capable of supporting multiple enterprise automation platforms beyond the initial UiPath implementation.
