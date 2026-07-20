# Knowledge Base

This folder contains the structured knowledge used by the Intelligent RPA RCA platform.

The knowledge base enables deterministic reasoning before AI-assisted report generation.
___

## Contents
___

### incident_taxonomy.xlsx

Contains:

- Taxonomy
- Incident Catalog

Defines the standardized classification of enterprise RPA incidents.

---

### recovery_library.xlsx

Maps incident categories to recommended recovery actions.

Examples include:

- Retry strategies
- Selector validation
- Application restart
- Terminal reconnection
- File verification

---

### root_cause_library.xlsx

Maps incident categories to probable root causes.

Examples include:

- Dynamic selectors
- Missing files
- Session expiration
- Network failures
- Invalid configuration

---

## Purpose

The knowledge base allows the system to:

- Classify automation failures
- Retrieve historical knowledge
- Recommend recovery actions
- Reduce LLM hallucinations
- Improve consistency of generated RCA reports

The knowledge base will continue expanding as new enterprise RPA incidents are collected.
