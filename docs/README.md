
# Documentation

This directory contains the design and technical documentation for Intelligent Automation RCA.

## Architecture and Design

- [`system_architecture.md`](system_architecture.md) — Describes the system components, their responsibilities, and the distinction between the current UiPath-specific implementation and potential future extensions.
- [`ai_diagnosis_pipeline.md`](ai_diagnosis_pipeline.md) — Explains the incident-processing pipeline, from log parsing through retrieval and RCA generation.
- [`rca_report_template.md`](rca_report_template.md) — Defines the intended structure and content of an RCA report.
- [`existing_solutions.md`](existing_solutions.md) — Reviews existing automation-support capabilities and explains the motivation for the project.

## Research Documentation

The following research documents are maintained in the `research/` directory:

- [`Evaluation.md`](research/Evaluation.md) — Records the experimental configurations, test cases, evaluation results, and case-level observations.
- [`experimental_methodology.md`](research/experimental_methodology.md) — Documents the experiment design, configurations, evaluation criteria, and limitations.
- [`findings.md`](research/findings.md) — Summarizes the experimental findings, observed failure modes, limitations, and implications.

## Documentation Guidelines

Research documentation should reflect the saved experiment results and the behavior of the actual implementation.

- Clearly distinguish implemented and evaluated components from planned features.
- Ensure that reported results are consistent with the saved experiment outputs.
- Document limitations and failure cases alongside successful outcomes.
- Avoid claims of reliability or generalizability that are not supported by the experiments.
