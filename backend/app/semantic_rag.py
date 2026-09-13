from functools import lru_cache
from sentence_transformers import SentenceTransformer, util
from app.knowledge_loader import load_knowledge_base
from app.parser import parse_uipath_log
from app.classifier import classify_incident

MODEL_NAME = "all-MiniLM-L6-v2"


@lru_cache(maxsize=1)
def _load_embedding_model():
    return SentenceTransformer(MODEL_NAME)


@lru_cache(maxsize=1)
def _load_knowledge_embeddings():
    kb = load_knowledge_base()

    root_cause_library = kb["root_causes"]
    recovery_library = kb["recovery"]

    root_cause_texts = [
        (
            f"Category: {row['Category ID']}. "
            f"Subcategory: {row['Subcategory']}. "
            f"Possible root cause: {row['Possible Root Cause']}. "
            f"Verification method: {row['Verification Method']}."
        )
        for _, row in root_cause_library.iterrows()
    ]

    recovery_texts = [
        (
            f"Category: {row['Category ID']}. "
            f"Subcategory: {row['Subcategory']}. "
            f"Suggested recovery: {row['Suggested Recovery']}. "
            f"Automation level: {row['Automation Level']}. "
            f"Notes: {row['Notes']}."
        )
        for _, row in recovery_library.iterrows()
    ]

    model = _load_embedding_model()

    root_cause_embeddings = model.encode(
        root_cause_texts,
        convert_to_tensor=True,
        normalize_embeddings=True
    )

    recovery_embeddings = model.encode(
        recovery_texts,
        convert_to_tensor=True,
        normalize_embeddings=True
    )

    return (
        root_cause_library,
        recovery_library,
        root_cause_embeddings,
        recovery_embeddings
    )


def _build_incident_query(incident, classification=None):
    exception = incident.get("exception", {}) if isinstance(incident, dict) else {}

    exception_type = str(exception.get("type") or "").strip()
    exception_message = str(exception.get("message") or "").strip()

    classification = classification or {}

    category_id = str(
        classification.get("category_id") or ""
    ).strip()

    subcategory = str(
        classification.get("subcategory") or ""
    ).strip()

    description = str(
        classification.get("description") or ""
    ).strip()

    workflow = str(
        incident.get("workflow") or ""
    ).strip()

    activity = str(
        incident.get("activity") or ""
    ).strip()

    query_parts = []

    if exception_type:
        query_parts.append(f"Exception type: {exception_type}.")

    if exception_message:
        query_parts.append(f"Exception message: {exception_message}.")

    if category_id:
        query_parts.append(f"Category: {category_id}.")

    if subcategory:
        query_parts.append(f"Subcategory: {subcategory}.")

    if description:
        query_parts.append(f"Incident description: {description}.")

    if workflow:
        query_parts.append(f"Workflow: {workflow}.")

    if activity:
        query_parts.append(f"Activity: {activity}.")

    return " ".join(query_parts)


def retrieve_semantic_root_causes(
    incident,
    classification,
    top_k=3,
    similarity_threshold=None
):
    if not isinstance(incident, dict):
        raise ValueError("Incident must be provided as a dictionary.")

    if not isinstance(classification, dict):
        raise ValueError("Classification must be provided as a dictionary.")

    (
        root_cause_library,
        _,
        root_cause_embeddings,
        _
    ) = _load_knowledge_embeddings()

    model = _load_embedding_model()

    query = _build_incident_query(incident, classification)

    query_embedding = model.encode(
        query,
        convert_to_tensor=True,
        normalize_embeddings=True
    )

    similarities = util.cos_sim(
        query_embedding,
        root_cause_embeddings
    )[0]

    ranked_indices = similarities.argsort(
        descending=True
    )[:top_k]

    results = []

    for index in ranked_indices:
        score = float(similarities[index])

        if (
            similarity_threshold is not None
            and score < similarity_threshold
        ):
            continue

        row = root_cause_library.iloc[int(index)]

        results.append({
            "root_cause_id": row["Root Cause ID"],
            "category_id": row["Category ID"],
            "subcategory": row["Subcategory"],
            "possible_root_cause": row["Possible Root Cause"],
            "confidence": row["Confidence"],
            "verification_method": row["Verification Method"],
            "similarity_score": round(score, 4)
        })

    return results


def retrieve_semantic_recovery_actions(
    incident,
    classification,
    top_k=3,
    similarity_threshold=None
):
    if not isinstance(incident, dict):
        raise ValueError("Incident must be provided as a dictionary.")

    if not isinstance(classification, dict):
        raise ValueError("Classification must be provided as a dictionary.")

    (
        _,
        recovery_library,
        _,
        recovery_embeddings
    ) = _load_knowledge_embeddings()

    model = _load_embedding_model()

    query = _build_incident_query(incident, classification)

    query_embedding = model.encode(
        query,
        convert_to_tensor=True,
        normalize_embeddings=True
    )

    similarities = util.cos_sim(
        query_embedding,
        recovery_embeddings
    )[0]

    ranked_indices = similarities.argsort(
        descending=True
    )[:top_k]

    results = []

    for index in ranked_indices:
        score = float(similarities[index])

        if (
            similarity_threshold is not None
            and score < similarity_threshold
        ):
            continue

        row = recovery_library.iloc[int(index)]

        results.append({
            "recovery_id": row["Recovery ID"],
            "category_id": row["Category ID"],
            "subcategory": row["Subcategory"],
            "suggested_recovery": row["Suggested Recovery"],
            "automation_level": row["Automation Level"],
            "notes": row["Notes"],
            "similarity_score": round(score, 4)
        })

    return results

if __name__ == "__main__":
    test_cases = [
        {
            "name": "UI Selector - Exact",
            "log": """
            State
            Faulted

            Process: Loan_Disbursal
            Package: UiPath.UIAutomation.ActIVITIES
            Package version: 23.10.6

            Workflow: Loan_Disbursal.xaml
            Activity: Click Submit

            Raw message: NodeNotFoundException
            Exception: UiPath.Core.SelectorNotFoundException

            Start Time: 09/05/2026, 11:20:10 AM
            End Time: 09/05/2026, 11:20:12 AM

            Robot: TestRobot
            Hostname: TEST-MACHINE
            Account: test_account

            Input Values: Submit Button
            Output Values: None
            Has Recording: False
            """
        },
        {
            "name": "UI Selector - Paraphrased",
            "log": """
            State
            Faulted

            Process: Loan_Disbursal
            Package: UiPath.UIAutomation.Activities
            Package version: 23.10.6

            Workflow: Loan_Disbursal.xaml
            Activity: Click Submit

            Raw message: The automation could not locate the Submit button on the page.
            Exception: UiPath.Core.SelectorNotFoundException

            Start Time: 09/05/2026, 11:20:10 AM
            End Time: 09/05/2026, 11:20:12 AM

            Robot: TestRobot
            Hostname: TEST-MACHINE
            Account: test_account

            Input Values: Submit Button
            Output Values: None
            Has Recording: False
            """
        },
        {
            "name": "Missing File",
            "log": """
            State
            Faulted

            Process: Invoice_Processing
            Package: UiPath.Excel.Activities
            Package version: 2.24.2

            Workflow: Invoice_Processing.xaml
            Activity: Read Workbook

            Raw message: Workbook does not exist
            Exception: System.IO.FileNotFoundException

            Start Time: 09/05/2026, 12:00:00 PM
            End Time: 09/05/2026, 12:00:02 PM

            Robot: TestRobot
            Hostname: TEST-MACHINE
            Account: test_account

            Input Values: Invoice Workbook
            Output Values: None
            Has Recording: False
            """
        },
        {
            "name": "Network Path",
            "log": """
            State
            Faulted

            Process: Invoice_Processing
            Package: UiPath.System.Activities
            Package version: 24.10.3

            Workflow: Invoice_Processing.xaml
            Activity: Read File

            Raw message: Network path not found
            Exception: System.IO.IOException

            Start Time: 09/05/2026, 01:00:00 PM
            End Time: 09/05/2026, 01:00:03 PM

            Robot: TestRobot
            Hostname: TEST-MACHINE
            Account: test_account

            Input Values: Shared Invoice Folder
            Output Values: None
            Has Recording: False
            """
        },
        {
            "name": "Terminal Session",
            "log": """
            State
            Faulted

            Process: Payment_Processing
            Package: UiPath.Terminal.Activities
            Package version: 2.10.0

            Workflow: Payment_Processing.xaml
            Activity: Enter Payment Details

            Raw message: Terminal session not found
            Exception: System.Exception

            Start Time: 09/05/2026, 01:30:00 PM
            End Time: 09/05/2026, 01:30:03 PM

            Robot: TestRobot
            Hostname: TEST-MACHINE
            Account: test_account

            Input Values: Payment Details
            Output Values: None
            Has Recording: False
            """
        },
        {
            "name": "Unknown Incident",
            "log": """
            State
            Faulted

            Process: Customer_Onboarding
            Package: UiPath.System.Activities
            Package version: 24.10.3

            Workflow: Customer_Onboarding.xaml
            Activity: Process Customer Record

            Raw message: The operation is not valid for the current state.
            Exception: System.InvalidOperationException

            Start Time: 09/05/2026, 03:15:20 PM
            End Time: 09/05/2026, 03:15:22 PM

            Robot: TestRobot
            Hostname: TEST-MACHINE
            Account: test_account

            Input Values: Customer Record
            Output Values: None
            Has Recording: False
            """
        }
    ]

    for test_case in test_cases:
        print("\n" + "=" * 70)
        print(test_case["name"])
        print("=" * 70)

        incident = parse_uipath_log(test_case["log"])
        classification = classify_incident(incident)

        print("\nClassification:")
        print(classification)

        print("\nSemantic Root Causes:")
        root_causes = retrieve_semantic_root_causes(
            incident,
            classification,
            top_k=3
        )

        for result in root_causes:
            print(
                result["root_cause_id"],
                "|",
                result["category_id"],
                "|",
                result["subcategory"],
                "|",
                result["possible_root_cause"],
                "| score:",
                result["similarity_score"]
            )

        print("\nSemantic Recovery Actions:")
        recovery_actions = retrieve_semantic_recovery_actions(
            incident,
            classification,
            top_k=3
        )

        for result in recovery_actions:
            print(
                result["recovery_id"],
                "|",
                result["category_id"],
                "|",
                result["subcategory"],
                "|",
                result["suggested_recovery"],
                "| score:",
                result["similarity_score"]
            )