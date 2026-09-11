def generate_rca_report(
    incident,
    classification,
    root_causes,
    recovery_actions,
    generated_rca
):
    if not isinstance(incident, dict):
        raise ValueError("Incident must be provided as a dictionary.")

    if not isinstance(classification, dict):
        raise ValueError("Classification must be provided as a dictionary.")

    if not isinstance(root_causes, list):
        raise ValueError("Root causes must be provided as a list.")

    if not isinstance(recovery_actions, list):
        raise ValueError("Recovery actions must be provided as a list.")

    if not isinstance(generated_rca, str) or not generated_rca.strip():
        raise ValueError("Generated RCA must be a non-empty string.")

    report = {
        "incident": incident,
        "classification": classification,
        "root_causes": root_causes,
        "recovery_actions": recovery_actions,
        "generated_rca": generated_rca.strip()
    }

    return report


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

    sample_generated_rca = """
RCA REPORT

1. Incident Summary
A UiPath process failed during a selector-based UI activity.

2. Failure Location
Process: Loan_Disbursal
Activity: Click Submit

3. Probable Root Cause
The selector may have changed after a UI update or may contain dynamic attributes.

4. Supporting Evidence
Observed Evidence: SelectorNotFoundException.
Retrieved Knowledge: RCA-001 and RCA-002.
Model Inference: Both causes are plausible but unverified.

5. Recommended Recovery Actions
REC-001: Validate the selector using UI Explorer.

6. Prevention Recommendations
Review selector robustness and avoid volatile attributes.

7. Confidence
Root-cause confidence: Low.
"""

    report = generate_rca_report(
        sample_incident,
        sample_classification,
        sample_root_causes,
        sample_recovery_actions,
        sample_generated_rca
    )

    print("RCA Report Generated Successfully:\n")
    print(report)
