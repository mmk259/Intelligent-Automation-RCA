# Backend Modules

| File | Purpose |
|------|---------|
| `main.py` | FastAPI application entry point. Handles API requests and returns AI-generated RCA reports. |
| `parser.py` | Parses UiPath execution logs and extracts structured information such as exceptions, workflows, activities, timestamps, and execution context. |
| `classifier.py` | Maps extracted exceptions to the Incident Catalog and identifies the corresponding Incident ID, Category, and Subcategory. |
| `knowledge_loader.py` | Loads the Incident Taxonomy, Incident Catalog, Root Cause Library, and Recovery Library from Excel into memory. |
| `retriever.py` | Retrieves relevant root causes and recovery actions based on the classified incident. |
| `rca_generator.py` | Builds the LLM prompt using retrieved knowledge and generates a professional Root Cause Analysis (RCA) report. |
| `models.py` | Defines the data models and schemas used throughout the backend (e.g., Incident, RCA Report, Recovery Action). |
| `utils.py` | Contains shared helper functions and utility methods used across multiple backend modules. |
