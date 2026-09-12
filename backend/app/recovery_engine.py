from app.knowledge_loader import load_knowledge_base


def retrieve_recovery_actions(classification):
    """
    Retrieve recommended recovery actions for a classified incident.

    Parameters:
        classification (dict): Output returned by classify_incident().

    Returns:
        list: Recommended recovery actions.
    """

    if not isinstance(classification, dict):
        raise ValueError("Classification must be provided as a dictionary.")

    category_id = classification.get("category_id")
    subcategory = classification.get("subcategory")

    if not category_id or not subcategory:
        return []

    kb = load_knowledge_base()
    recovery_library = kb["recovery"]

    matches = recovery_library[
        (
            recovery_library["Category ID"]
            .astype(str)
            .str.strip()
            .str.upper()
            == str(category_id).strip().upper()
        )
        &
        (
            recovery_library["Subcategory"]
            .astype(str)
            .str.strip()
            .str.lower()
            == str(subcategory).strip().lower()
        )
    ].copy()

    if matches.empty:
        return []

    recovery_actions = []

    for _, row in matches.iterrows():
        recovery_actions.append({
            "recovery_id": row["Recovery ID"],
            "category_id": row["Category ID"],
            "subcategory": row["Subcategory"],
            "suggested_recovery": row["Suggested Recovery"],
            "automation_level": row["Automation Level"],
            "notes": row["Notes"]
        })

    return recovery_actions


if __name__ == "__main__":

    test_cases = [
        {
            "name": "UI Selector",
            "classification": {
                "incident_id": "UI-003",
                "category_id": "UI",
                "subcategory": "Selector"
            }
        },
        {
            "name": "File Missing",
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
            "name": "Terminal Session",
            "classification": {
                "incident_id": "TERM-002",
                "category_id": "TERM",
                "subcategory": "Session"
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

        results = retrieve_recovery_actions(test["classification"])

        if not results:
            print("No recovery actions found.")
        else:
            for action in results:
                print(action)

