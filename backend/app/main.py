from fastapi import FastAPI, HTTPException
from app.models import AnalyzeRequest, AnalyzeResponse
from app.parser import parse_uipath_log
from app.classifier import classify_incident
from app.retriever import retrieve_root_causes
from app.recovery_engine import retrieve_recovery_actions
from app.llm_integration import generate_rca
from app.structured_rca_generator import generate_rca_report
from app.semantic_rca_generator import (retrieve_semantic_root_causes,retrieve_semantic_recovery_actions)
from app.structured_verification import generate_verified_rca
from app.semantic_verification import generate_combined_rca

app = FastAPI(
    title="Intelligent Automation RCA",
    description="AI-assisted root cause analysis for automation incidents.",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "Intelligent Automation RCA API is running."
    }


@app.post("/analyze", response_model=AnalyzeResponse)
def analyze_incident(request: AnalyzeRequest):
    try:
        incident = parse_uipath_log(request.log)

        classification = classify_incident(incident)

        root_causes = retrieve_root_causes(classification)

        recovery_actions = retrieve_recovery_actions(classification)

        generated_rca = generate_rca(
            incident,
            classification,
            root_causes,
            recovery_actions
        )

        report = generate_rca_report(
            incident,
            classification,
            root_causes,
            recovery_actions,
            generated_rca
        )

        return report

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@app.post("/analyze/semantic")
def analyze_semantic(request: AnalyzeRequest):
    incident = parse_uipath_log(request.log)
    classification = classify_incident(incident)

    semantic_root_causes = retrieve_semantic_root_causes(
        incident,
        classification,
        top_k=3
    )

    semantic_recovery_actions = retrieve_semantic_recovery_actions(
        incident,
        classification,
        top_k=3
    )

    return {
        "incident": incident,
        "classification": classification,
        "root_causes": semantic_root_causes,
        "recovery_actions": semantic_recovery_actions
    }

@app.post("/analyze/verified")
def analyze_verified(request: AnalyzeRequest):
    try:
        incident = parse_uipath_log(request.log)
        classification = classify_incident(incident)

        root_causes = retrieve_root_causes(classification)
        recovery_actions = retrieve_recovery_actions(classification)

        # Generate the initial RCA using the exact same baseline LLM function.
        generated_rca = generate_rca(
            incident,
            classification,
            root_causes,
            recovery_actions
        )

        # Verify and revise the baseline-generated RCA.
        verified_result = generate_verified_rca(
            incident,
            classification,
            root_causes,
            recovery_actions,
            generated_rca
        )

        # Keep the initial RCA, verification findings, and revised RCA
        # separately so the experiment can compare them.
        return {
            "incident": incident,
            "classification": classification,
            "root_causes": root_causes,
            "recovery_actions": recovery_actions,
            "initial_rca": verified_result["initial_rca"],
            "verification_result": verified_result["verification_result"],
            "revised_rca": verified_result["revised_rca"]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze/combined")
def analyze_combined(request: AnalyzeRequest):
    try:
        incident = parse_uipath_log(request.log)
        classification = classify_incident(incident)

        result = generate_combined_rca(
            incident,
            classification,
            top_k=3
        )

        return {
            "incident": incident,
            **result
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@app.post("/analyze/combined")
def analyze_combined(request: AnalyzeRequest):
    try:
        incident = parse_uipath_log(request.log)
        classification = classify_incident(incident)

        result = generate_combined_rca(
            incident=incident,
            classification=classification,
            top_k=3
        )

        return {
            "incident": incident,
            "classification": classification,
            **result
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))