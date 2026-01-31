import logging
from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict

# Core Agents
from agents.dsa_framework import NetworkDSA
from agents.path_engine import OPME
from agents.thinking_agent import ThinkingAgent
from agents.sensory_hub import SensoryHub
from agents.csa_engine import CSA
from agents.pmo_gate import PMOGate
from agents.zta_engine import ZTAEngine, KIWVault
from agents.ethics_manager import EthicsManager
from agents.specialty_lab import SpecialtyLab, LabFinding
from agents.asset_factory import AssetFactory, FSAsset
from agents.resilience import CircuitBreaker, CircuitBreakerOpenException
from temporal.workflows import bpo_onboarding_workflow
from temporal.worker import temporal





# Schemas
from schemas.assessments import (
    EvidenceSubmission, DMSRequest, EmailRequest, 
    ReportRequest, AssessmentResponse, IngestedArtifact, 
    Report, GateLog, GateStatus, PathRecommendation, QualityMetrics
)

# Logging Setup
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("BARC-Governance")

app = FastAPI(
    title="BARC Governance Engine",
    description="KIW-Certified BPO Architecture Review Engine",
    version="1.1.0"
)

# CORS for React Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global Instance Registry
hub = SensoryHub(storage_path="evidence/")
csa = CSA()
gate = PMOGate()
zta = ZTAEngine()
ethics = EthicsManager()
lab = SpecialtyLab()
factory = AssetFactory()
dsa_breaker = CircuitBreaker(failure_threshold=2, recovery_timeout=10)

# Chaos State
chaos_active = False

async def verify_zta_auth(x_zta_token: str = Header(None)):

    """Zero Trust Dependency to verify token presence and validity."""
    if not x_zta_token:
        logger.warning("Access denied: Missing ZTA Token")
        raise HTTPException(status_code=403, detail="ZT_TOKEN_MISSING")
    
    # Simple validation for the demo; in production, this checks ZTA registry
    if not x_zta_token.startswith("ZTA-"):
        logger.error(f"Access denied: Invalid ZTA Token format: {x_zta_token}")
        raise HTTPException(status_code=403, detail="ZT_TOKEN_INVALID")
    return x_zta_token

@app.get("/", tags=["Health"])
async def root():
    return {"status": "ACTIVE", "governance": "GADOS-Certified", "version": "1.1.0"}

@app.post("/ingest/dms", response_model=IngestedArtifact, tags=["Ingestion"])
async def ingest_dms(req: DMSRequest):
    logger.info(f"Ingesting DMS document: {req.filename}")
    return hub.ingest_from_dms(req.provider, req.filename, req.content)

@app.post("/ingest/email", response_model=IngestedArtifact, tags=["Ingestion"])
async def ingest_email(req: EmailRequest):
    logger.info(f"Ingesting Email from: {req.sender}")
    return hub.ingest_from_email(req.sender, req.subject, req.content)

@app.post("/analyze", response_model=AssessmentResponse, tags=["Orchestration"])
async def analyze_evidence(submission: EvidenceSubmission):
    logger.info(f"Starting Governed Assessment for BPO: {submission.bpo_id}")
    
    # 1. Zero Trust Identity Generation
    token = zta.issue_contextual_token(identity=f"Agent-{submission.domain}", scope="ASSESSMENT")
    
    if submission.domain.lower() == "network":
        @dsa_breaker
        async def primary_assess():
            # Chaos Testing Node inside the resilient block
            if chaos_active:
                logger.warning("CHAOS MODE ACTIVE: Injecting simulated failure.")
                raise Exception("SIMULATED_DSA_FAILURE")
                
            dsa = NetworkDSA(domain_id="NW-001", standards_path="standards/network_golden.json")
            return await dsa.analyze(submission.content)

            
        try:
            findings = await primary_assess()
        except CircuitBreakerOpenException:
            raise HTTPException(status_code=503, detail="SERVICE_UNAVAILABLE_RESILIENCE_GATE")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
        # 2. Peer Review (Thinking Agent)
        critiques = ThinkingAgent.critique_findings(findings)
        
        # 3. Ethics Audit
        reasoning_sample = " ".join([f.reasoning for f in findings])
        ethics_pass = ethics.audit_reasoning(agent_id=f"DSA-{submission.domain}", reasoning_text=reasoning_sample)
        
        return {
            "findings": findings,
            "verification": [c.dict() for c in critiques],
            "ethics_audit": ethics_pass,
            "zta_token": token.token_id,
            "governance_status": "CERTIFIED_HARDENED"
        }
    else:
        raise HTTPException(status_code=400, detail="DOMAIN_SPECIALIST_NOT_AVAILABLE")

@app.post("/zta/mfa", tags=["Security"])
async def verify_mfa(token_id: str, code: str):
    """MFA Challenge for administrative actions."""
    success = zta.challenge_mfa(token_id, code)
    if not success:
        raise HTTPException(status_code=403, detail="MFA_VERIFICATION_FAILED")
    return {"status": "MFA_AUDITED_SUCCESS"}

@app.post("/chaos/toggle", tags=["Chaos Engineering"])
async def toggle_chaos(active: bool):
    global chaos_active
    chaos_active = active
    msg = "ENABLED" if active else "DISABLED"
    logger.critical(f"Chaos Monkey has been {msg}")
    return {"status": f"CHAOS_{msg}"}


@app.post("/report", response_model=Report, tags=["Reporting"])
async def generate_report(req: ReportRequest):
    logger.info(f"Generating Executive Report for {req.bpo_name}")
    return csa.synthesize_technical_to_executive(req.findings, req.bpo_name)

@app.post("/gate/approve", response_model=GateLog, tags=["Governance"])
async def approve_artifact(artifact_id: str, status: GateStatus, user_id: str):
    logger.info(f"Transitioning artifact {artifact_id} to {status} by {user_id}")
    return gate.transition_status(artifact_id, status, user_id)

@app.post("/path", response_model=PathRecommendation, tags=["Intelligence"])
async def get_optimal_path(complexity: str, urgency: str):
    return OPME.determine_optimal_path(complexity, urgency)

@app.post("/lab/dive", response_model=List[LabFinding], tags=["Specialty"])
async def specialty_deep_dive(domain: str, context: str):
    logger.info(f"Starting Specialty Lab deep-dive for: {domain}")
    return lab.run_deep_dive(domain, context)

@app.post("/factory/generate", response_model=FSAsset, tags=["Asset Factory"])
async def generate_fs_asset(bpo_name: str, findings: List[Dict]):
    logger.info(f"Generating FS Asset for: {bpo_name}")
    return factory.generate_fs_spec(bpo_name, findings)

@app.get("/metrics", response_model=QualityMetrics, tags=["Intelligence"])
async def get_metrics(findings_count: int = 10, critical_gaps: int = 2):
    return OPME.calculate_metrics(findings_count, critical_gaps)

# --- Temporal Phase 2 Endpoints ---

@app.post("/temporal/start", tags=["Temporal Phase 2"])
async def start_durable_assessment(submission: EvidenceSubmission):
    """Starts a durable, Temporal-managed assessment workflow."""
    logger.info(f"Starting Durable Assessment for BPO: {submission.bpo_id}")
    wf_id = await bpo_onboarding_workflow(submission.bpo_id, submission.domain, submission.content)
    return {"workflow_id": wf_id, "status": "DURABLE_ORCHESTRATION_STARTED"}

@app.get("/temporal/status/{workflow_id}", tags=["Temporal Phase 2"])
async def get_workflow_status(workflow_id: str):
    """Returns the current state and history of a Temporal workflow."""
    status = temporal.get_status(workflow_id)
    if not status["workflow"]:
        raise HTTPException(status_code=404, detail="WORKFLOW_NOT_FOUND")
    return status


if __name__ == "__main__":
    import uvicorn
    logger.info("Initializing BARC Governance Engine on port 8003...")
    uvicorn.run(app, host="0.0.0.0", port=8003)
