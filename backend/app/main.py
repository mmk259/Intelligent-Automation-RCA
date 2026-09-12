from fastapi import FastAPI, HTTPException
from app.models import AnalyzeRequest, AnalyzeResponse
from app.parser import parse_uipath_log
from app.classifier import classify_incident
from app.retriever import retrieve_root_causes
from app.recovery_engine import retrieve_recovery_actions
from app.llm_integration import generate_rca
from app.rca_generator import generate_rca_report


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