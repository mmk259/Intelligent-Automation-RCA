from app.llm_integration import client, MODEL_NAME


def build_verification_prompt(
    incident,
    classification,
    root_causes,
    recovery_actions,
    generated_rca
):
    return f"""
You are an RCA verification assistant for an enterprise automation
incident analysis system.

Your task is to verify whether the generated RCA is properly grounded
in the information provided to the system.

Do NOT generate a new RCA.
Do NOT introduce new evidence, root causes, recovery actions, or facts.

Evaluate the generated RCA ONLY against:

1. Observed incident information
2. Classification information
3. Retrieved root-cause knowledge
4. Retrieved recovery-action knowledge

====================
INCIDENT
====================
{incident}

====================
CLASSIFICATION
====================
{classification}

====================
RETRIEVED ROOT CAUSES
====================
{root_causes}

====================
RETRIEVED RECOVERY ACTIONS
====================
{recovery_actions}

====================
GENERATED RCA
====================
{generated_rca}

====================
VERIFICATION TASK
====================

Identify any problems in the generated RCA.

Check specifically for:

1. Unsupported claims
   - Claims that cannot be supported by the incident or retrieved
     knowledge.

2. Invented evidence
   - Details that do not appear in the incident information.

3. Incorrect evidence classification
   - Retrieved knowledge presented as observed evidence.
   - Model inference presented as observed evidence.

4. Unsupported root causes
   - Root causes presented as confirmed when the incident evidence
     does not verify them.

5. Unsupported recovery actions
   - Recovery actions that were not provided in the retrieved
     recovery-action knowledge.

6. Incorrect confidence
   - Confidence that is stronger than the available evidence supports.

7. Unsupported prevention recommendations
   - Recommendations presented as facts or based on information that
     is not available.

8. Other grounding problems
   - Any statement that could mislead an automation engineer about
     what is actually known versus inferred.

====================
OUTPUT FORMAT
====================

Return the verification result using exactly these sections:

VERIFICATION RESULT

Overall Assessment:
PASS / NEEDS_REVISION

Unsupported Claims:
- List each unsupported claim.
- If none exist, write "None identified."

Invented Evidence:
- List each invented detail.
- If none exist, write "None identified."

Evidence Classification Problems:
- List each problem.
- If none exist, write "None identified."

Root Cause Problems:
- List each problem.
- If none exist, write "None identified."

Recovery Action Problems:
- List each problem.
- If none exist, write "None identified."

Confidence Problems:
- List each problem.
- If none exist, write "None identified."

Prevention Recommendation Problems:
- List each problem.
- If none exist, write "None identified."

Required Revisions:
- List the specific changes required before the RCA can be considered
  sufficiently grounded.
- If no revisions are required, write "None."

IMPORTANT:
Do not treat knowledge-base confidence labels as incident-specific
confidence.
Do not invent missing information.
Do not assume that a plausible root cause has been verified.
"""


def verify_rca(
    incident,
    classification,
    root_causes,
    recovery_actions,
    generated_rca
):
    prompt = build_verification_prompt(
        incident,
        classification,
        root_causes,
        recovery_actions,
        generated_rca
    )

    response = client.chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.message.content


def build_revision_prompt(
    incident,
    classification,
    root_causes,
    recovery_actions,
    generated_rca,
    verification_result
):
    return f"""
You are an enterprise automation RCA revision assistant.

Revise the generated RCA using the verification findings provided
below.

The revised RCA MUST remain grounded ONLY in:

- Observed incident information
- Classification information
- Retrieved root-cause knowledge
- Retrieved recovery-action knowledge

Do NOT introduce new evidence, root causes, recovery actions, or facts.

Do NOT remove uncertainty merely to make the RCA sound more confident.

Root causes from the knowledge base are possible causes unless the
incident evidence directly verifies them.

Clearly distinguish:
- Observed Evidence
- Retrieved Knowledge
- Model Inference

Do not present model inference as observed evidence.

Do not present retrieved knowledge as observed evidence.

Use only the provided recovery actions.

If evidence is insufficient to determine the root cause, explicitly
state that the root cause remains undetermined or unverified.

====================
INCIDENT
====================
{incident}

====================
CLASSIFICATION
====================
{classification}

====================
RETRIEVED ROOT CAUSES
====================
{root_causes}

====================
RETRIEVED RECOVERY ACTIONS
====================
{recovery_actions}

====================
INITIAL RCA
====================
{generated_rca}

====================
VERIFICATION FINDINGS
====================
{verification_result}

====================
REVISION TASK
====================

Produce a corrected RCA using these sections:

1. Incident Summary
2. Failure Location
3. Probable Root Cause
4. Supporting Evidence
5. Recommended Recovery Actions
6. Prevention Recommendations
7. Confidence

Apply every required revision identified by the verifier.

Do not add information that was not available to the initial RCA.

For Confidence, provide a qualitative incident-specific confidence
level: High, Medium, or Low.

Remember:
Knowledge-base confidence is NOT incident-specific confidence.
Classifier confidence is NOT a statistical probability.
Unverified root causes must not be presented as confirmed.
"""


def revise_rca(
    incident,
    classification,
    root_causes,
    recovery_actions,
    generated_rca,
    verification_result
):
    prompt = build_revision_prompt(
        incident,
        classification,
        root_causes,
        recovery_actions,
        generated_rca,
        verification_result
    )

    response = client.chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.message.content


def generate_verified_rca(
    incident,
    classification,
    root_causes,
    recovery_actions,
    generated_rca
):
    verification_result = verify_rca(
        incident,
        classification,
        root_causes,
        recovery_actions,
        generated_rca
    )

    revised_rca = revise_rca(
        incident,
        classification,
        root_causes,
        recovery_actions,
        generated_rca,
        verification_result
    )

    return {
        "initial_rca": generated_rca,
        "verification_result": verification_result,
        "revised_rca": revised_rca
    }

if __name__ == "__main__":
    sample_incident = {
        "platform": "UiPath",
        "status": "FAULTED",
        "process": "Loan_Disbursal",
        "exception": {
            "type": "UiPath.Core.SelectorNotFoundException",
            "message": "NodeNotFoundException"
        },
        "workflow": "Loan_Disbursal.xaml",
        "activity": "Click Submit"
    }

    sample_classification = {
        "incident_id": "UI-003",
        "category_id": "UI",
        "subcategory": "Selector",
        "description": "Target UI node could not be located.",
        "confidence": 0.8
    }

    sample_root_causes = [
        {
            "root_cause_id": "RCA-001",
            "possible_root_cause": "Selector changed after UI update",
            "confidence": "High",
            "verification_method": "Compare selector with current UI"
        },
        {
            "root_cause_id": "RCA-002",
            "possible_root_cause": "Dynamic attributes in selector",
            "confidence": "High",
            "verification_method": "Inspect selector attributes"
        }
    ]

    sample_recovery_actions = [
        {
            "recovery_id": "REC-001",
            "suggested_recovery": (
                "Validate selector using UI Explorer and update if required."
            ),
            "automation_level": "Semi-Automatic",
            "notes": "Human verification recommended."
        }
    ]

    initial_rca = """
1. Incident Summary
The Loan_Disbursal process failed during the Click Submit activity.

2. Failure Location
Process: Loan_Disbursal
Activity: Click Submit

3. Probable Root Cause
The selector may have changed after a UI update.

4. Supporting Evidence
Observed Evidence: NodeNotFoundException.
Retrieved Knowledge: RCA-001 and RCA-002.
Model Inference: A selector-related issue is plausible but unverified.

5. Recommended Recovery Actions
REC-001: Validate the selector using UI Explorer.

6. Prevention Recommendations
Review selector robustness and avoid volatile attributes.

7. Confidence
Root-cause confidence: Low.
"""

    result = generate_verified_rca(
        sample_incident,
        sample_classification,
        sample_root_causes,
        sample_recovery_actions,
        initial_rca
    )

    print("\n================ INITIAL RCA ================\n")
    print(result["initial_rca"])

    print("\n================ VERIFICATION ================\n")
    print(result["verification_result"])

    print("\n================ REVISED RCA ================\n")
    print(result["revised_rca"])