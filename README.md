# Intelligent RPA RCA

An AI-assisted Root Cause Analysis (RCA) platform for Robotic Process Automation (RPA) incidents. The system analyzes UiPath execution logs, identifies probable root causes, recommends recovery actions, and generates professional RCA reports using a structured knowledge base and Large Language Models (LLMs).

---

## Problem

Enterprise RPA developers spend significant time manually diagnosing production automation failures. Existing tools primarily focus on retries and self-healing but provide limited support for structured incident diagnosis and engineering-quality RCA reports.

---

## Project Goal

Build an intelligent assistant that can:

- Parse UiPath execution logs
- Classify automation incidents
- Retrieve similar historical incidents
- Identify probable root causes
- Recommend recovery actions
- Generate professional RCA reports
- Assist RPA developers during production support

---

## Features

- Knowledge Base Loader
- Log Parser
- Incident Classification Engine
- Root Cause Retrieval
- Recovery Recommendation Engine
- AI-assisted RCA Generation
- FastAPI Backend
- Extensible Knowledge Base

---

## Project Structure

```text
intelligent-rpa-rca/
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

## Technology Stack

- Python
- FastAPI
- Pandas
- OpenPyXL
- Git & GitHub
- Large Language Models (LLMs)

---

## Development Roadmap

### Sprint 1 — Knowledge Base Design (Completed)

- Incident Taxonomy
- Recovery Library
- Root Cause Library
- AI Diagnosis Pipeline
- RCA Report Template
- Research of Existing Solutions

### Sprint 2 — MVP Development

- Backend Setup
- Knowledge Base Loader 
- Log Parser (Currently working on)
- Incident Classification Engine
- Root Cause Retrieval
- Recovery Recommendation Engine
- LLM Integration
- RCA Report Generator
- REST API
- Testing

---

## Future Work

- Vector database integration
- Semantic incident retrieval
- Multi-agent reasoning
- Self-healing recommendations
- Web dashboard
- Enterprise deployment

---

## License

This project is currently under development.
