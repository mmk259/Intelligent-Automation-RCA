
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

## Project Positioning and Motivation

Existing automation platforms provide capabilities for monitoring automation execution, handling exceptions, retrying failed activities, and assisting with workflow development and recovery. These capabilities address important aspects of automation reliability.

Intelligent Automation RCA explores a complementary approach focused on diagnosing RPA execution failures and organizing reusable diagnostic knowledge.

The current implementation investigates a hybrid architecture combining:

- **Incident parsing:** Extracting relevant information from UiPath execution logs.
- **Taxonomy-based classification:** Identifying known incident categories and subcategories.
- **Structured retrieval:** Retrieving root causes and recovery actions using incident classification.
- **Semantic retrieval:** Using embedding-based similarity to retrieve potentially relevant root causes and recovery actions from the knowledge base.
- **LLM-assisted RCA generation:** Generating structured diagnostic reports using incident information and retrieved knowledge.
- **Verification-assisted revision:** Evaluating generated reports for unsupported claims and revising them to improve evidence grounding and uncertainty handling.

The experiments examine structured and semantic retrieval independently, including their ability to identify relevant knowledge for known incidents and their limitations when handling unfamiliar incidents. Further experiments investigate LLM-generated diagnoses and the effect of verification-assisted revision under both retrieval approaches.

The initial results show that semantic retrieval can identify relevant root causes and recovery actions for several known incident types. However, it can also retrieve weakly related candidates, particularly when the incident is unfamiliar or the available knowledge does not contain a sufficiently relevant match. Verification-assisted revision can improve aspects of generated reports, although it does not eliminate all unsupported reasoning or independently guarantee retrieval relevance.

The current implementation is a research-oriented technical prototype targeting UiPath execution logs. It does not aim to replace existing platform monitoring, troubleshooting, or self-healing capabilities. Instead, it investigates how structured knowledge, semantic retrieval, and language-model reasoning can be combined to support more systematic automation incident diagnosis.

The evaluation remains exploratory and is limited by the size and composition of the current test set.
