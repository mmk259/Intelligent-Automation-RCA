
# Existing Automation Capabilities

## Introduction

Enterprise automation platforms provide capabilities for handling execution failures, improving workflow resilience, and assisting developers in building and maintaining automations.

This project focuses on a related but distinct problem: analysing automation incidents, identifying potential root causes, and retrieving relevant recovery guidance from a structured knowledge base.

The following sections describe selected UiPath capabilities relevant to automation failure handling and explain how their scope relates to Intelligent Automation RCA.

## UiPath

UiPath provides several capabilities that help developers and organizations handle automation failures and improve workflow reliability.

### Healing Agent

UiPath Healing Agent provides AI-assisted capabilities for recovering from certain UI automation failures. It helps address changes in application interfaces and UI elements that can cause automations to fail.

**Relation to Intelligent Automation RCA:**

Healing Agent focuses on recovering automation execution. Intelligent Automation RCA instead investigates execution failures and produces structured diagnostic information. The two approaches address different aspects of automation reliability.

### Retry Scope

Retry Scope is a UiPath workflow activity that repeatedly executes specified activities until a configured condition is met or the retry limit is reached.

It is useful for handling temporary failures, such as operations that may succeed after another attempt.

**Relation to Intelligent Automation RCA:**

Retry Scope provides a mechanism for retrying workflow execution. It does not, by itself, provide the broader incident classification and knowledge-based root cause analysis implemented in this project.

### Check App State

Check App State checks the state of an application or UI element and allows a workflow to follow different execution paths depending on the observed state.

It helps automations handle variations in application behaviour and interface availability.

**Relation to Intelligent Automation RCA:**

Check App State supports runtime decision-making within an automation workflow. Intelligent Automation RCA focuses on analysing failures after they occur and retrieving relevant diagnostic and recovery information.


## Positioning of Intelligent Automation RCA

Intelligent Automation RCA explores an AI-assisted approach to diagnosing RPA execution failures.

The current implementation focuses on UiPath execution logs and investigates the combination of:

- Log parsing to extract incident information.
- Taxonomy-based incident classification.
- Structured knowledge retrieval.
- Semantic retrieval using embedding-based similarity.
- LLM-assisted generation of diagnostic reports.
- An experimental verification and revision stage.

The project evaluates both structured and semantic retrieval approaches for identifying relevant root causes and recovery actions. It also investigates how retrieved knowledge can support LLM-generated diagnoses and how an additional verification stage affects the resulting reports.

The current implementation is a research-oriented technical prototype focused on incident diagnosis rather than autonomous workflow repair or runtime recovery. Its evaluation examines retrieval relevance, generated diagnoses, and the limitations of the implemented approaches.

Unlike workflow retry or UI recovery mechanisms, the project's primary focus is incident diagnosis and the organization of reusable root cause and recovery knowledge.

The current implementation is a research-oriented prototype rather than a complete automation recovery or monitoring platform. Its evaluation investigates retrieval relevance and the behaviour of generated diagnoses under different configurations.

Support for additional automation platforms and more extensive evaluation remain potential future extensions.
