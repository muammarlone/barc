from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from agents.dsa_framework import Finding
from agents.path_engine import PathRecommendation, QualityMetrics
from agents.sensory_hub import IngestedArtifact
from agents.csa_engine import Report
from agents.pmo_gate import GateLog, GateStatus
from agents.zta_engine import SecurityToken
from agents.ethics_manager import EthicsAssessment

class EvidenceSubmission(BaseModel):
    bpo_id: str = Field(..., description="Unique ID of the BPO")
    domain: str = Field(..., description="Technical domain (e.g., network, desktop)")
    content: str = Field(..., description="Evidence payload")

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

class AssessmentResponse(BaseModel):
    findings: List[Finding]
    verification: List[Dict]
    ethics_audit: EthicsAssessment
    zta_token: str
    governance_status: str
