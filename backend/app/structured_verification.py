from app.llm_integration import client, MODEL_NAME


def build_verification_prompt(
    incident,
    classification,
    root_causes,
    recovery_actions,
    generated_rca,
):
    return f"""
You are the verification and correction-planning component of an
enterprise automation RCA system.

Your job is to critically evaluate the generated RCA against the supplied
incident evidence and retrieved knowledge, then produce a precise correction
plan for a separate revision model.

Do NOT write a new RCA.
Do NOT rewrite the RCA.
Do NOT invent evidence, root causes, recovery actions, or facts.

Your output is a CRITIQUE and CORRECTION PLAN only.

PERMITTED SOURCES
=================
The RCA may rely only on:

1. Observed incident information
2. Classification information
3. Retrieved root-cause knowledge
4. Retrieved recovery-action knowledge

General domain knowledge, common failure patterns, technical assumptions,
and plausible explanations are NOT evidence unless explicitly supported by
one of the permitted sources.

IMPORTANT DISTINCTIONS
======================

- Retrieved knowledge proves only that a possibility exists in the knowledge
  base. It does NOT prove that the possibility occurred in this incident.

- Knowledge-base confidence is NOT incident-specific confidence.

- Classifier confidence is NOT a statistical probability.

- Model inference may be included only when it is clearly labeled as
  inference and does not contradict the supplied evidence.

- Model inference must never be presented as observed evidence or as a
  confirmed root cause.

- Retrieval relevance is separate from grounding. A retrieved item can be
  valid KB knowledge and still be a poor match for this incident.

- A statement being labeled "possible", "likely", "plausible",
  "unverified", or "inferred" does NOT automatically make it acceptable.
  Determine whether the statement is useful and appropriately grounded.

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
EVALUATION TASK
====================

Evaluate the generated RCA claim-by-claim.

A. GROUNDING
===========

For every substantive factual or diagnostic statement, determine whether it
is:

- directly supported by observed incident information
- directly supported by classification information
- supported only as retrieved knowledge
- clearly labeled model inference
- unsupported

Flag:

- invented evidence
- environment details not supplied
- configuration details not supplied
- timestamp/timezone details not supplied
- diagnostic results not supplied
- retrieved knowledge presented as observed evidence
- inference presented as fact
- unsupported root causes
- unsupported recovery actions
- unsupported prevention recommendations
- confidence stronger than the incident evidence supports
- failure to preserve uncertainty
- failure to abstain when evidence is insufficient

B. RETRIEVAL RELEVANCE
======================

Evaluate whether the RCA's selected or preferred root causes and recovery
actions actually fit the incident.

For each preferred root cause or recovery action, classify it as:

- RELEVANT
  Directly matches the observed incident or classification.

- RELATED_BUT_UNCONFIRMED
  Semantically related and potentially useful, but not established by
  incident evidence.

- POOR_MATCH
  Retrieved item is meaningfully mismatched to the incident.

- UNSUPPORTED
  The item is not present in the supplied retrieved knowledge.

Do NOT mark an item RELEVANT merely because it exists in the knowledge base.

C. INSUFFICIENT EVIDENCE
========================

Determine whether the RCA appropriately handles uncertainty.

If the incident does not establish a specific root cause, the RCA should
identify the cause as unverified or undetermined.

If multiple retrieved candidates exist but none is confirmed, the RCA should
not select one as the confirmed cause.

If no evidence-grounded recovery action is available, the RCA must not invent
one.

D. CONFIDENCE
=============

Evaluate whether the final confidence reflects the actual incident evidence.

Do NOT allow:

- high KB confidence to become high incident confidence
- classifier confidence to become incident certainty
- semantic similarity score to become proof of a root cause

E. CORRECTION PLAN
==================

For every substantive problem, create a concrete correction that another
LLM can apply directly.

For each issue specify:

- Problem:
  What is wrong.

- Action:
  One of:
  REMOVE
  REWRITE
  QUALIFY
  OMIT

- Required Change:
  Exactly what the revision model should do.

- Source to Preserve:
  Which permitted source should remain in the revised RCA.

- Source/Content to Remove:
  What unsupported or incorrect content must be removed.

- Replacement Allowed:
  YES or NO

- Target Wording Guidance:
  Describe how the revised statement should be framed.

IMPORTANT ACTION RULES
======================

REMOVE:
Delete the unsupported content.

OMIT:
Delete the content and do not replace it with newly generated information.

REWRITE:
Rewrite the statement using only permitted sources.

QUALIFY:
Retain the underlying information only if it is explicitly framed with
appropriate uncertainty and does not imply confirmation.

IMPORTANT REPLACEMENT RULE
==========================

If Replacement Allowed is NO, the revision model MUST NOT replace the removed
content with another claim, assumption, recommendation, timestamp,
environment detail, or technical explanation.

If Replacement Allowed is YES, the replacement must be grounded in the
specified permitted source.

====================
DECISION RULE
====================

Return NEEDS_REVISION if there is any substantive issue involving:

- grounding
- retrieval relevance
- unsupported root-cause selection
- unsupported recovery selection
- inappropriate confidence
- insufficient-evidence handling
- unsupported prevention
- invented evidence
- unsupported model-generated content

PASS is allowed only when:

1. There are no substantive grounding violations.
2. No preferred root cause or recovery action is a POOR_MATCH or UNSUPPORTED.
3. Confidence is appropriate to the incident evidence.
4. Insufficient evidence is handled correctly.
5. No substantive unsupported content requires correction.

Do NOT return PASS merely because an unsupported statement is called
possible, plausible, likely, unverified, or inferred.

====================
OUTPUT FORMAT
====================

Return exactly these sections:

VERIFICATION RESULT

Overall Assessment:
PASS / NEEDS_REVISION

Grounding Problems:
- Each problem with a short quoted or paraphrased RCA claim and why it is
  unsupported.
- If none: None identified.

Retrieval Relevance Problems:
- Each preferred root cause or recovery action that is a poor or weak match,
  with the reason.
- If none: None identified.

Confidence Problems:
- Each confidence issue.
- If none: None identified.

Insufficient-Evidence Problems:
- Each failure to abstain, preserve uncertainty, or distinguish candidates
  from confirmed causes.
- If none: None identified.

Correction Plan:
For every substantive issue use exactly:

- Problem:
- Action:
- Required Change:
- Source to Preserve:
- Source/Content to Remove:
- Replacement Allowed:
- Target Wording Guidance:

If no corrections are required:
None.

Do not write a revised RCA.
Do not provide general best-practice advice.
Do not introduce any new domain knowledge.
"""


def verify_rca(
    incident,
    classification,
    root_causes,
    recovery_actions,
    generated_rca,
):
    prompt = build_verification_prompt(
        incident,
        classification,
        root_causes,
        recovery_actions,
        generated_rca,
    )

    response = client.chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    return response.message.content


def build_revision_prompt(
    incident,
    classification,
    root_causes,
    recovery_actions,
    generated_rca,
    verification_result,
):
    return f"""
You are the RCA correction and revision component of an enterprise
automation incident analysis system.

Your task is to produce an improved version of the generated RCA by applying
the verifier's Correction Plan.

The verifier's Correction Plan is the authoritative instruction for what must
be corrected.

Do NOT mention the verifier or the revision process in the final RCA.

GROUNDING CONTRACT
==================

The revised RCA may use ONLY:

1. Observed incident information
2. Classification information
3. Retrieved root-cause knowledge
4. Retrieved recovery-action knowledge

Do NOT introduce:

- new facts
- new technical assumptions
- new root causes
- new recovery actions
- new timestamps
- new timezones
- new environment details
- new configuration details
- new diagnostic results
- unsupported prevention recommendations

RETRIEVAL CONTRACT
==================

A retrieved KB item is not automatically the incident's root cause.

If the verifier identifies an item as:

RELEVANT:
It may be used as retrieved knowledge when appropriate.

RELATED_BUT_UNCONFIRMED:
It may be retained only as an unverified candidate if useful.

POOR_MATCH:
Do not use it as the selected root cause or recommended recovery action.

UNSUPPORTED:
Do not use it.

Do not convert retrieval similarity into certainty.

UNCERTAINTY CONTRACT
====================

If the evidence does not establish a root cause:

- explicitly state that the root cause is unverified or undetermined
- distinguish candidate causes from confirmed causes
- do not select a candidate merely because it has high KB confidence
- do not derive incident confidence from KB confidence
- do not derive incident confidence from classifier confidence
- do not derive incident confidence from semantic similarity

EVIDENCE CONTRACT
=================

Clearly distinguish:

- Observed Evidence
- Retrieved Knowledge
- Model Inference

Observed Evidence must contain only information actually supplied by the
incident.

Retrieved Knowledge must contain only information retrieved from the supplied
knowledge base.

Model Inference must be clearly identified as inference.

Never present retrieved knowledge or model inference as observed evidence.

RECOVERY CONTRACT
=================

Use only recovery actions contained in the supplied retrieved recovery-action
knowledge.

Do not invent recovery actions.

Only retain actions that the verifier considers relevant or appropriate to
retain.

If no appropriate recovery action is supported, state that no
evidence-grounded recovery action can be established from the available
sources.

PREVENTION CONTRACT
===================

Do not invent incident-specific prevention recommendations.

If the supplied sources do not support a prevention recommendation:

- do not generate a generic best-practice recommendation
- do not replace the missing recommendation with domain knowledge
- state that no incident-specific prevention recommendation can be
  established from the available evidence

CORRECTION PLAN CONTRACT
========================

Apply EVERY substantive correction in the verifier's Correction Plan.

The Action field has the following meaning:

REMOVE:
Remove the identified content.

OMIT:
Remove the content and DO NOT replace it with a newly generated claim.

REWRITE:
Rewrite the content using only the permitted sources.

QUALIFY:
Retain the information only with the uncertainty framing specified by the
verifier.

Replacement Allowed:
If the verifier says NO, do not replace the removed content with another
claim, assumption, recommendation, timestamp, environment detail, or technical
explanation.

If the verifier says YES, any replacement must be grounded in the permitted
sources and follow the Target Wording Guidance.

Do not independently undo a verifier correction.

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
VERIFIER RESULT + CORRECTION PLAN
====================
{verification_result}

====================
REVISION TASK
====================

Produce the corrected RCA using exactly these sections:

1. Incident Summary
2. Failure Location
3. Probable Root Cause
4. Supporting Evidence
5. Recommended Recovery Actions
6. Prevention Recommendations
7. Confidence

SECTION REQUIREMENTS
====================

1. Incident Summary
-------------------
Summarize only the observed incident information.

Do not add environment details or technical assumptions.

2. Failure Location
-------------------
Identify the workflow/activity/location only when supported by the supplied
incident or classification information.

Otherwise state that the failure location is not established.

3. Probable Root Cause
----------------------
Distinguish clearly between:

- confirmed cause
- candidate/unverified cause
- undetermined cause

If no cause is established, say that the root cause remains unverified or
undetermined.

Do not present a retrieved KB cause as confirmed merely because it is a strong
semantic match.

4. Supporting Evidence
----------------------
Include only:

- supplied incident evidence
- classification information when relevant
- clearly labeled retrieved knowledge
- clearly labeled model inference where appropriate

Never place inference under observed evidence.

5. Recommended Recovery Actions
--------------------------------
Use only appropriate recovery actions from the supplied retrieved knowledge.

Do not invent actions.

Do not use a POOR_MATCH or UNSUPPORTED retrieved action.

6. Prevention Recommendations
-----------------------------
Use only prevention guidance explicitly supported by the supplied sources.

If no incident-specific prevention recommendation can be established,
explicitly state that.

Do not replace missing prevention evidence with generic best practices.

7. Confidence
-------------
Provide incident-specific:

High
Medium
Low

Low is appropriate when the root cause is not verified.

Do not derive incident confidence directly from:

- KB confidence
- classifier confidence
- semantic similarity

====================
FINAL REQUIREMENTS
====================

The revised RCA must:

- preserve observed evidence exactly
- preserve retrieved knowledge as retrieved knowledge
- preserve appropriate uncertainty
- distinguish candidates from confirmed causes
- use only appropriate retrieved recovery actions
- avoid unsupported prevention recommendations
- apply every verifier correction
- avoid introducing new facts
- avoid introducing domain knowledge as evidence
- avoid replacing removed unsupported content when replacement is prohibited

Do not mention the verifier.
Do not mention the revision process.
Do not explain your reasoning.
Return only the revised RCA.
"""


def revise_rca(
    incident,
    classification,
    root_causes,
    recovery_actions,
    generated_rca,
    verification_result,
):
    prompt = build_revision_prompt(
        incident,
        classification,
        root_causes,
        recovery_actions,
        generated_rca,
        verification_result,
    )

    response = client.chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    return response.message.content


def generate_verified_rca(
    incident,
    classification,
    root_causes,
    recovery_actions,
    generated_rca,
):
    verification_result = verify_rca(
        incident,
        classification,
        root_causes,
        recovery_actions,
        generated_rca,
    )

    revised_rca = revise_rca(
        incident,
        classification,
        root_causes,
        recovery_actions,
        generated_rca,
        verification_result,
    )

    return {
        "initial_rca": generated_rca,
        "verification_result": verification_result,
        "revised_rca": revised_rca,
    }