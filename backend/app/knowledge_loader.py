import pandas as pd
from pathlib import Path

# Project Root
BASE_DIR = Path(__file__).resolve().parents[2]

# Knowledge Base Directory
KB_DIR = BASE_DIR / "knowledge_base"


def load_knowledge_base():
    """
    Loads the Intelligent RPA RCA knowledge base.

    Returns:
        dict: Loaded knowledge base tables.
    """

    if not KB_DIR.exists():
        raise FileNotFoundError(
            f"Knowledge base directory not found: {KB_DIR}"
        )

    taxonomy_file = KB_DIR / "incident_taxonomy.xlsx"
    recovery_file = KB_DIR / "recovery_library.xlsx"
    rootcause_file = KB_DIR / "root_cause_library.xlsx"

    for file in [taxonomy_file, recovery_file, rootcause_file]:
        if not file.exists():
            raise FileNotFoundError(f"Missing knowledge base file: {file.name}")

    incident_taxonomy = pd.read_excel(
        taxonomy_file,
        sheet_name="Taxonomy"
    )

    incident_catalog = pd.read_excel(
        taxonomy_file,
        sheet_name="Incident Catalog"
    )

    recovery_library = pd.read_excel(
        recovery_file
    )

    root_cause_library = pd.read_excel(
        rootcause_file
    )

    return {
        "taxonomy": incident_taxonomy,
        "incident_catalog": incident_catalog,
        "root_causes": root_cause_library,
        "recovery": recovery_library,
    }


if __name__ == "__main__":

    try:

        kb = load_knowledge_base()

        print("Knowledge Base Loaded Successfully!\n")

        print("Taxonomy:", len(kb["taxonomy"]))
        print("Incident Catalog:", len(kb["incident_catalog"]))
        print("Root Causes:", len(kb["root_causes"]))
        print("Recovery Library:", len(kb["recovery"]))

    except Exception as e:
        print(f"Error: {e}")