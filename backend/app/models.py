from pydantic import BaseModel


class AnalyzeRequest(BaseModel):
    log: str


class AnalyzeResponse(BaseModel):
    incident: dict
    classification: dict
    root_causes: list
    recovery_actions: list
    generated_rca: str