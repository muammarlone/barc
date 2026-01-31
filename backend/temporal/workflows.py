import asyncio
import logging
from temporal.worker import temporal
from agents.dsa_framework import NetworkDSA
from agents.thinking_agent import ThinkingAgent
from agents.ethics_manager import EthicsManager
from agents.zta_engine import ZTAEngine

logger = logging.getLogger("BPO-Workflow")

async def bpo_onboarding_workflow(bpo_id: str, domain: str, content: str):
    """
    Main Temporal Workflow for BPO Onboarding.
    Orchestrates multiple activities with durability.
    """
    wf_id = await temporal.execute_workflow("BPO_Onboarding_Workflow", {"bpo_id": bpo_id, "domain": domain})
    
    # Activity 1: Zero Trust Handshake
    zta = ZTAEngine()
    token = await temporal.run_activity(
        wf_id, 
        "ZTA_Handshake", 
        lambda: zta.issue_contextual_token(identity=f"Agent-{domain}", scope="ASSESSMENT")
    )
    
    # Activity 2: Domain Specialist Analysis
    if domain.lower() == "network":
        dsa = NetworkDSA(domain_id="NW-001", standards_path="standards/network_golden.json")
        findings = await temporal.run_activity(
            wf_id, 
            "DSA_Analysis", 
            lambda: dsa.analyze(content)
        )
        
        # Activity 3: Peer Review (Thinking Agent)
        critiques = await temporal.run_activity(
            wf_id, 
            "Peer_Review", 
            lambda: ThinkingAgent.critique_findings(findings)
        )
        
        # Activity 4: Ethical Audit
        ethics = EthicsManager()
        reasoning_sample = " ".join([f.reasoning for f in findings])
        ethics_pass = await temporal.run_activity(
            wf_id, 
            "Ethics_Audit", 
            lambda: ethics.audit_reasoning(agent_id=f"DSA-{domain}", reasoning_text=reasoning_sample)
        )
        
        # Mark Workflow as Complete
        temporal.active_workflows[wf_id]["status"] = "COMPLETED"
        temporal.active_workflows[wf_id]["result"] = {
            "findings_count": len(findings),
            "governance_status": "CERTIFIED_DURABLE"
        }
        
        return wf_id
    else:
        temporal.active_workflows[wf_id]["status"] = "FAILED"
        temporal.active_workflows[wf_id]["error"] = "DOMAIN_NOT_SUPPORTED"
        return wf_id
