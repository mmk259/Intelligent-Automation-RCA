from app.knowledge_loader import load_knowledge_base


def retrieve_root_causes(classification):
    """
    Retrieve possible root causes for a classified incident.

    Parameters:
        classification (dict): Output returned by classify_incident().

    Returns:
        list: Ranked list of possible root causes.
    """

    if not isinstance(classification, dict):
        raise ValueError("Classification must be provided as a dictionary.")

    category_id = classification.get("category_id")
    subcategory = classification.get("subcategory")

    if not category_id or not subcategory:
        return []

    kb = load_knowledge_base()
    root_cause_library = kb["root_causes"]

    # First try an exact Category + Subcategory match.
    matches = root_cause_library[
        (root_cause_library["Category ID"].astype(str).str.strip().str.upper()
         == str(category_id).strip().upper())
        &
        (root_cause_library["Subcategory"].astype(str).str.strip().str.lower()
         == str(subcategory).strip().lower())
    ].copy()

    if matches.empty:
        return []

    # Rank High > Medium > Low.
    confidence_rank = {
        "High": 3,
        "Medium": 2,
        "Low": 1
    }

    matches["rank"] = (
        matches["Confidence"]
        .astype(str)
        .str.strip()
        .map(confidence_rank)
        .fillna(0)
    )

    matches = matches.sort_values(
        by="rank",
        ascending=False
    )

    root_causes = []

    for _, row in matches.iterrows():
        root_causes.append({
            "root_cause_id": row["Root Cause ID"],
            "category_id": row["Category ID"],
            "subcategory": row["Subcategory"],
            "possible_root_cause": row["Possible Root Cause"],
            "confidence": row["Confidence"],
            "verification_method": row["Verification Method"]
        })

    return root_causes

if __name__ == "__main__":

    test_cases = [
        {
            "name": "Missing File",
            "classification": {
                "incident_id": "FILE-004",
                "category_id": "FILE",
                "subcategory": "Missing File"
            }
        },
        {
            "name": "Network Path",
            "classification": {
                "incident_id": "NET-001",
                "category_id": "NET",
                "subcategory": "Path"
            }
        },
        {
            "name": "Performance Timeout",
            "classification": {
                "incident_id": "PERF-001",
                "category_id": "PERF",
                "subcategory": "Timeout"
            }
        },
        {
            "name": "UI Timing",
            "classification": {
                "incident_id": "UI-005",
                "category_id": "UI",
                "subcategory": "Timing"
            }
        },
        {
            "name": "Unknown Incident",
            "classification": {
                "incident_id": "XYZ-999",
                "category_id": "XYZ",
                "subcategory": "Unknown"
            }
        }
    ]

    for test in test_cases:

        print(f"\n{'=' * 50}")
        print(test["name"])
        print(f"{'=' * 50}")

        results = retrieve_root_causes(test["classification"])

        if not results:
            print("No root causes found.")
        else:
            for cause in results:
                print(cause)

