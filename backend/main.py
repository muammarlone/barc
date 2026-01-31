from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from agents.dsa_framework import NetworkDSA, Finding
from agents.path_engine import OPME, PathRecommendation, QualityMetrics


app = FastAPI(title="BARC Backend - GADOS Powered")

class EvidenceSubmission(BaseModel):
    bpo_id: str
    domain: str
    content: str

@app.get("/")
async def root():
    return {"status": "BARC Governance Engine Active", "version": "1.0.0"}

@app.post("/analyze", response_model=List[Finding])
async def analyze_evidence(submission: EvidenceSubmission):
    if submission.domain.lower() == "network":
        dsa = NetworkDSA(domain_id="NW-001", standards_path="standards/network_golden.json")
        findings = await dsa.analyze(submission.content)
        return findings
@app.post("/path", response_model=PathRecommendation)
async def get_optimal_path(complexity: str, urgency: str):
    return OPME.determine_optimal_path(complexity, urgency)

@app.get("/metrics", response_model=QualityMetrics)
async def get_metrics(findings_count: int = 10, critical_gaps: int = 2):
    return OPME.calculate_metrics(findings_count, critical_gaps)

if __name__ == "__main__":

    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
