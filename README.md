# Intelligent Automation RCA

An AI-assisted Root Cause Analysis (RCA) platform for enterprise automation incidents. The system analyzes automation execution logs, identifies probable root causes, recommends recovery actions, and generates professional RCA reports using a structured knowledge base and Large Language Models (LLMs).

**Initial implementation:** Integration with UiPath automation logs and incident knowledge.
The architecture is designed to support additional enterprise automation platforms through patform-specific connectors.

**Long-term vision:** A platform-independent AI-assisted incident diagnosis framework for enterprise automation systems, supporting platforms such as UiPath, Automation Anywhere, Microsoft Power Automate, Blue Prism, and future automation technologies.

---

# Problem

Enterprise automation teams spend significant time manually diagnosing production automation failures. Existing platforms primarily focus on monitoring, retries, and self-healing but provide limited support for structured AI-assisted incident diagnosis, root cause reasoning, and engineering-quality RCA report generation.

---

# Project Goal

Build an intelligent assistant that can:

- Parse automation execution logs
- Classify automation incidents
- Retrieve similar historical incidents
- Identify probable root causes
- Recommend recovery actions
- Generate professional RCA reports
- Accelerate incident diagnosis and production support across enterprise automation platforms

---

# Features

- Knowledge Base Loader
- Automation Log Parser
- Incident Classification Engine
- Root Cause Retrieval
- Recovery Recommendation Engine
- AI-assisted RCA Generation
- FastAPI Backend
- Extensible Knowledge Base

---

# Project Structure

```text
intelligent-automation-rca/
│
├── backend/
├── dataset/
├── knowledge_base/
├── docs/
├── tests/
├── frontend/
├── README.md
└── LICENSE
```

---

# Technology Stack

- Python
- FastAPI
- Pandas
- OpenPyXL
- Git & GitHub
- Large Language Models (LLMs)

---

# Development Roadmap

## Sprint 1 — Knowledge Base Design (Completed)

- Incident Taxonomy
- Recovery Library
- Root Cause Library
- AI Diagnosis Pipeline
- RCA Report Template
- Research of Existing Solutions
- Iterative Development Plan

## Sprint 2 — MVP Development

- Backend Setup
- Knowledge Base Loader
- Automation Log Parser *(Current)*
- Incident Classification Engine
- Root Cause Retrieval
- Recovery Recommendation Engine
- LLM Integration
- RCA Report Generator
- REST API
- Testing

---

# Future Work

- Multi-platform log parsing
- Vector database integration
- Semantic incident retrieval
- Multi-agent reasoning
- AI-assisted recovery recommendations
- Web dashboard
- Enterprise deployment
- Support for additional enterprise automation platforms

---

# License

This project is currently under active development.
