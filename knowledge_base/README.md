# Knowledge Base

This folder contains the structured knowledge used by the **Intelligent Automation RCA** platform.

The knowledge base enables deterministic reasoning before AI-assisted Root Cause Analysis (RCA) generation.

---

# Contents

## incident_taxonomy.xlsx

Contains:

- Taxonomy
- Incident Catalog

Defines the standardized classification of enterprise automation incidents.

---

## recovery_library.xlsx

Maps incident categories to recommended recovery actions.

Examples include:

- Retry strategies
- Selector validation
- Application restart
- Terminal reconnection
- File verification

Additional recovery strategies will be added as support for more enterprise automation platforms is introduced.

---

## root_cause_library.xlsx

Maps incident categories to probable root causes.

Examples include:

- Dynamic selectors
- Missing files
- Session expiration
- Network failures
- Invalid configuration

The library is designed to grow continuously as new incident patterns are identified.

---

# Purpose

The knowledge base enables the platform to:

- Classify automation incidents
- Retrieve structured incident knowledge
- Recommend recovery actions
- Ground AI reasoning in validated knowledge
- Reduce LLM hallucinations
- Improve the consistency and explainability of generated RCA reports

The initial implementation focuses on UiPath incident knowledge. The overall knowledge base architecture is designed to support multiple enterprise automation platforms through a common incident taxonomy and extensible platform-specific knowledge.
``