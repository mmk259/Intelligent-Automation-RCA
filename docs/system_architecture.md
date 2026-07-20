
# System Architecture

## Project Objective

**Intelligent Automation RCA** is an AI-assisted incident diagnosis platform for enterprise automation systems. The platform analyzes automation failures, classifies incidents, identifies probable root causes, recommends recovery actions, and generates professional Root Cause Analysis (RCA) reports to accelerate production support and incident resolution.

The initial implementation targets UiPath, while the overall architecture is designed to remain platform-independent through platform-specific connectors.

---

# High-Level System Workflow

```text
Enterprise Automation Platform
(UiPath / Automation Anywhere /
Power Automate / ...)
            │
(API / Log Export / Webhook)
            │
            ▼
Platform Connector
            │
            ▼
Automation Log Parser
            │
            ▼
Incident Classification
            │
            ▼
Knowledge Base Retrieval
            │
     ┌──────────────┬──────────────┐
     ▼              ▼              ▼
Incident       Root Cause      Recovery
Catalog         Library         Library
     └──────────────┬──────────────┘
                    ▼
           LLM Reasoning Engine
                    │
                    ▼
      Professional RCA Report
```

---

# System Components

## 1. Platform Connector

Connects the platform to enterprise automation systems by collecting execution data through APIs, exported logs, or monitoring interfaces.

**Initial implementation:**

- UiPath execution logs

**Future support:**

- Automation Anywhere
- Microsoft Power Automate
- Blue Prism
- Other enterprise automation platforms

---

## 2. Automation Log Parser

Extracts structured execution information from automation logs, including:

- Exception
- Workflow
- Activity
- Timestamp
- Execution Context

Example:

```
NodeNotFoundException
```

---

## 3. Incident Classification Engine

Maps extracted exceptions to standardized incidents using the Incident Catalog.

Example:

```
NodeNotFoundException
        ↓
     UI-003
        ↓
Category: UI Automation
Subcategory: Selector
```

---

## 4. Knowledge Base

The knowledge base stores structured diagnostic information, including:

- Incident Taxonomy
- Incident Catalog
- Root Cause Library
- Recovery Library

---

## 5. LLM Reasoning Engine

The LLM receives structured context retrieved from the knowledge base, including:

- Incident information
- Execution context
- Probable root causes
- Recovery actions

Instead of generating responses solely from its internal knowledge, the model reasons over retrieved enterprise knowledge to produce explainable and consistent diagnoses.

---

## 6. RCA Report Generator

Produces a standardized Root Cause Analysis (RCA) report containing:

- Incident Summary
- Root Cause Analysis
- Supporting Evidence
- Recovery Recommendations
- Prevention Recommendations
- Confidence Score