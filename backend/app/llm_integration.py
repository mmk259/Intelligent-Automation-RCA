import os
from ollama import Client

MODEL_NAME = "gpt-oss:20b-cloud"

API_KEY = os.getenv("OLLAMA_API_KEY")

if not API_KEY:
    raise RuntimeError("OLLAMA_API_KEY is not set.")

client = Client(
    host="https://ollama.com",
    headers={
        "Authorization": f"Bearer {API_KEY}"
    }
)

def build_rca_prompt(incident, classification, root_causes, recovery_actions):
    return f"""
You are an enterprise automation incident analysis assistant.

Analyze the automation incident using ONLY the provided incident
information and retrieved knowledge.

Do NOT invent evidence, facts, root causes, or recovery actions.

Do NOT state a root cause as confirmed unless the observed incident
evidence directly supports and verifies it.

Clearly distinguish between:
- Observed Evidence: information directly present in the incident.
- Retrieved Knowledge: information retrieved from the knowledge base.
- Model Inference: conclusions or hypotheses derived by reasoning over
  the observed evidence and retrieved knowledge.

IMPORTANT ROOT CAUSE RULES:
- Root causes from the knowledge base are POSSIBLE root causes, not
  confirmed causes.
- A root cause marked "High", "Medium", or "Low" in the knowledge base
  represents the knowledge base's confidence/relevance for that
  possible cause. It does NOT represent confidence that the cause is
  responsible for this specific incident.
- Do NOT convert knowledge-base confidence into incident-specific
  root-cause confidence.
- If the incident evidence does not verify a root cause, explicitly
  describe it as a plausible or suspected cause.
- Always include the verification method for an unverified root cause.
- If multiple root causes are possible and the evidence cannot
  distinguish between them, say so.
- If there is insufficient evidence to identify a root cause, explicitly
  state that the root cause remains undetermined.

IMPORTANT CLASSIFICATION CONFIDENCE RULE:
- The classifier confidence score represents a matching score from the
  classification engine.
- It is NOT a statistical probability and must not be presented as one.
- Do not use the classifier score alone to determine root-cause
  confidence.

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
RECOMMENDED RECOVERY ACTIONS
====================
{recovery_actions}

====================
RCA REPORT
====================

Generate the following sections:

1. Incident Summary
2. Failure Location
3. Probable Root Cause
4. Supporting Evidence
5. Recommended Recovery Actions
6. Prevention Recommendations
7. Confidence

For the Probable Root Cause section:
- Identify the most plausible causes from the retrieved knowledge.
- Explain why each cause is plausible based on the available evidence.
- Do not present a plausible cause as confirmed unless it is directly
  supported by observed evidence.
- Include the appropriate verification method.
- Clearly state when verification has not been performed.

For Supporting Evidence:
- Separate Observed Evidence from Retrieved Knowledge.
- Clearly identify Model Inference.
- Do not present retrieved knowledge as observed evidence.
- Do not present model inference as observed evidence.

For Recommended Recovery Actions:
- Use only the provided recommended recovery actions.
- Do not invent additional recovery actions.
- Preserve the provided automation level and notes where relevant.

For Prevention Recommendations:
- Base recommendations on the incident and retrieved knowledge.
- Do not claim that a recommendation was observed in the incident.
- Clearly distinguish recommendations from verified facts.

For Confidence:
- Give a qualitative incident-specific confidence level: High, Medium,
  or Low.
- Root-cause confidence must reflect the strength of evidence for THIS
  INCIDENT, not the confidence label in the knowledge base.
- If the root cause is only plausible and has not been verified, do not
  label the root-cause confidence as High solely because the knowledge
  base marks it as High.
- If evidence is insufficient, use Low confidence.
"""


def generate_rca(incident, classification, root_causes, recovery_actions):
    prompt = build_rca_prompt(
        incident,
        classification,
        root_causes,
        recovery_actions
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


if __name__ == "__main__":
    sample_incident = {
        "platform": "UiPath",
        "status": "FAULTED",
        "process": "Customer_Onboarding",
        "exception": {
            "type": "System.InvalidOperationException",
            "message": "The operation is not valid for the current state."
        },
        "workflow": "Customer_Onboarding.xaml",
        "activity": "Process Customer Record"
    }

    sample_classification = {
        "incident_id": None,
        "category_id": None,
        "subcategory": None,
        "description": None,
        "confidence": 0.0
    }

    sample_root_causes = []
    sample_recovery_actions = []

    result = generate_rca(
        sample_incident,
        sample_classification,
        sample_root_causes,
        sample_recovery_actions
    )

    print("\nGenerated RCA:\n")
    print(result)