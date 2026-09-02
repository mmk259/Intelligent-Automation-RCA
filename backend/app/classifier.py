from knowledge_loader import load_knowledge_base


def classify_incident(incident):
    """
    Classify a parsed automation incident using the Incident Catalog.

    Parameters:
        incident (dict): Normalized incident returned by parser.py.

    Returns:
        dict: Classified incident information.
    """

    if not isinstance(incident, dict):
        raise ValueError("Incident must be provided as a dictionary.")

    exception = incident.get("exception", {})

    exception_type = exception.get("type")
    exception_message = exception.get("message")

    exception_type = str(exception_type or "").strip()
    exception_message = str(exception_message or "").strip()

    if not exception_type and not exception_message:
        return {
            "incident_id": None,
            "category_id": None,
            "subcategory": None,
            "description": None,
            "confidence": 0.0
        }

    kb = load_knowledge_base()
    incident_catalog = kb["incident_catalog"]

    best_match = None
    best_score = 0

    for _, row in incident_catalog.iterrows():

        catalog_exception = str(row["Exception"]).strip()

        score = 0

        # Exact exception-type match
        if exception_type and catalog_exception.lower() == exception_type.lower():
            score = 100

        # Exception/message contained in catalog entry
        elif exception_message and catalog_exception.lower() in exception_message.lower():
            score = 80

        # Catalog exception contained in either exception type or message
        elif (
            exception_type
            and catalog_exception.lower() in exception_type.lower()
        ):
            score = 70

        elif (
            exception_message
            and catalog_exception.lower() in exception_message.lower()
        ):
            score = 60

        if score > best_score:
            best_score = score
            best_match = row

    if best_match is None:
        return {
            "incident_id": None,
            "category_id": None,
            "subcategory": None,
            "description": None,
            "confidence": 0.0
        }

    confidence = min(best_score / 100, 1.0)

    return {
        "incident_id": best_match["Incident ID"],
        "category_id": best_match["Category ID"],
        "subcategory": best_match["Subcategory"],
        "description": best_match["Short Description"],
        "confidence": confidence
    }


if __name__ == "__main__":

    test_incidents = [
        {
            "name": "UI Selector",
            "incident": {
                "exception": {
                    "type": "UiPath.Core.SelectorNotFoundException",
                    "message": "NodeNotFoundException"
                }
            }
        },
        {
            "name": "Missing File",
            "incident": {
                "exception": {
                    "type": "System.IO.FileNotFoundException",
                    "message": "FileNotFoundException"
                }
            }
        },
        {
            "name": "Network Path",
            "incident": {
                "exception": {
                    "type": "",
                    "message": "Network path not found"
                }
            }
        },
        {
            "name": "Terminal Connection",
            "incident": {
                "exception": {
                    "type": "",
                    "message": "Terminal not connected"
                }
            }
        },
        {
            "name": "Login Failure",
            "incident": {
                "exception": {
                    "type": "",
                    "message": "Login failed"
                }
            }
        },
        {
            "name": "Unknown Incident",
            "incident": {
                "exception": {
                    "type": "SomeRandomException",
                    "message": "Something completely unexpected happened"
                }
            }
        }
    ]

    for test in test_incidents:
        result = classify_incident(test["incident"])

        print(f"\n{test['name']}")
        print(result)

