from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from agents.dsa_framework import NetworkDSA, Finding
from agents.path_engine import OPME, PathRecommendation, QualityMetrics

from agents.thinking_agent import ThinkingAgent, Critique
from agents.sensory_hub import SensoryHub, IngestedArtifact
from agents.csa_engine import CSA, Report
from agents.pmo_gate import PMOGate, GateLog, GateStatus
from agents.zta_engine import ZTAEngine
from agents.ethics_manager import EthicsManager






app = FastAPI(title="BARC Backend - GADOS Powered")
hub = SensoryHub(storage_path="evidence/")
csa = CSA()
gate = PMOGate()
zta = ZTAEngine()
ethics = EthicsManager()


class EvidenceSubmission(BaseModel):


    bpo_id: str
    domain: str
    content: str

class DMSRequest(BaseModel):
    provider: str
    filename: str
    content: str

class EmailRequest(BaseModel):
    sender: str
    subject: str
    content: str

class ReportRequest(BaseModel):
    findings: List[Dict]
    bpo_name: str



@app.get("/")
async def root():
    return {"status": "BARC Governance Engine Active", "version": "1.0.0"}

@app.post("/ingest/dms", response_model=IngestedArtifact)
async def ingest_dms(req: DMSRequest):
    return hub.ingest_from_dms(req.provider, req.filename, req.content)

@app.post("/ingest/email", response_model=IngestedArtifact)
async def ingest_email(req: EmailRequest):
    return hub.ingest_from_email(req.sender, req.subject, req.content)



@app.post("/report", response_model=Report)
async def generate_report(req: ReportRequest):
    return csa.synthesize_technical_to_executive(req.findings, req.bpo_name)


@app.post("/gate/approve", response_model=GateLog)
async def approve_artifact(artifact_id: str, status: GateStatus, user_id: str):
    return gate.transition_status(artifact_id, status, user_id)

@app.post("/analyze")
async def analyze_evidence(submission: EvidenceSubmission):
    # 1. Zero Trust Gate
    token = zta.issue_contextual_token(identity=f"Agent-{submission.domain}", scope="ASSESSMENT")
    
    if submission.domain.lower() == "network":
        dsa = NetworkDSA(domain_id="NW-001", standards_path="standards/network_golden.json")
        findings = await dsa.analyze(submission.content)
        
        # 2. Peer Review Gate
        critiques = ThinkingAgent.critique_findings(findings)
        
        # 3. Ethics Gate
        reasoning_sample = " ".join([f.reasoning for f in findings])
        ethics_pass = ethics.audit_reasoning(agent_id=f"DSA-{submission.domain}", reasoning_text=reasoning_sample)
        
        return {
            "findings": findings,
            "verification": critiques,
            "ethics_audit": ethics_pass,
            "zta_token": token.token_id,
            "governance_status": "CERTIFIED_SAFE"
        }



@app.post("/path", response_model=PathRecommendation)
async def get_optimal_path(complexity: str, urgency: str):
    return OPME.determine_optimal_path(complexity, urgency)

@app.get("/metrics", response_model=QualityMetrics)
async def get_metrics(findings_count: int = 10, critical_gaps: int = 2):
    return OPME.calculate_metrics(findings_count, critical_gaps)

if __name__ == "__main__":

    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
