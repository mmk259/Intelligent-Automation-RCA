from app.semantic_rca_generator import (
    retrieve_semantic_root_causes,
    retrieve_semantic_recovery_actions
)

from app.llm_integration import generate_rca
from app.structured_verification import generate_verified_rca

def generate_combined_rca(
    incident,
    classification,
    top_k=3
):
    """
    Generate a verified semantic-RAG RCA.

    Pipeline:
        Incident
            ↓
        Semantic Retrieval
            ↓
        Semantic RCA
            ↓
        V2 Verification
            ↓
        V2 Revision
            ↓
        Verified Semantic RCA
    """

    # ---------------------------------------------------------
    # 1. Semantic retrieval
    # ---------------------------------------------------------

    semantic_root_causes = retrieve_semantic_root_causes(
        incident=incident,
        classification=classification,
        top_k=top_k
    )

    semantic_recovery_actions = retrieve_semantic_recovery_actions(
        incident=incident,
        classification=classification,
        top_k=top_k
    )

    # ---------------------------------------------------------
    # 2. Generate the baseline Semantic RCA
    # ---------------------------------------------------------

    semantic_rca = generate_rca(
        incident=incident,
        classification=classification,
        root_causes=semantic_root_causes,
        recovery_actions=semantic_recovery_actions
    )

    # ---------------------------------------------------------
    # 3. Verify and revise the Semantic RCA
    # ---------------------------------------------------------

    verified_result = generate_verified_rca(
        incident=incident,
        classification=classification,
        root_causes=semantic_root_causes,
        recovery_actions=semantic_recovery_actions,
        generated_rca=semantic_rca
    )

    # ---------------------------------------------------------
    # 4. Return both the unverified and verified versions
    # ---------------------------------------------------------

    return {
        "semantic_root_causes": semantic_root_causes,
        "semantic_recovery_actions": semantic_recovery_actions,

        # Baseline semantic condition
        "semantic_rca": verified_result["initial_rca"],

        # Verification output
        "verification_result": verified_result["verification_result"],

        # Verified semantic condition
        "verified_semantic_rca": verified_result["revised_rca"]
    }