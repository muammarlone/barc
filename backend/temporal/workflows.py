import asyncio
import logging
from temporal.worker import temporal
from agents.dsa_framework import NetworkDSA
from agents.thinking_agent import ThinkingAgent
from agents.ethics_manager import EthicsManager
from agents.zta_engine import ZTAEngine
from agents.pmo_gate import PMOGate, GateStatus
from agents.security_guard import AISecurityGuard


logger = logging.getLogger("BPO-Workflow")

async def bpo_onboarding_workflow(bpo_id: str, domain: str, content: str, tenant_id: str = "DEFAULT", wf_id: str = None):
    """
    Industrial-Scale Temporal Workflow for BPO Onboarding.
    Orchestrates the full lifecycle from Ingestion to Final Reporting.
    """
    wf_id = await temporal.execute_workflow("BPO_Onboarding_Workflow", {"bpo_id": bpo_id, "domain": domain}, tenant_id, workflow_id=wf_id)
    temporal.set_query(wf_id, "progress", 0.05)

    try:
        # --- Stage 1: Security & Identity ---
        from agents.governance import DRE
        dre = DRE()
        
        # 1.1. Define Dynamic RACI (Well-Architected Pillar)
        raci = await temporal.run_activity(
            wf_id, "Define_RACI",
            lambda: dre.get_raci_matrix(tenant_id, complexity="MEDIUM", risk_score=0.1)
        )
        temporal.set_query(wf_id, "raci_matrix", raci.dict())

        security = AISecurityGuard()
        sanitized_content = await temporal.run_activity(
            wf_id, "Security_Guard_Filter", 
            lambda: security.process_input(content)
        )
        temporal.set_query(wf_id, "progress", 0.15)

        zta = ZTAEngine()
        token = await temporal.run_activity(
            wf_id, "ZTA_Handshake", 
            lambda: zta.issue_contextual_token(identity=f"Agent-{domain}", scope="ASSESSMENT")
        )
        temporal.set_query(wf_id, "progress", 0.25)

        # --- Stage 2: Ingestion ---
        from agents.sensory_hub import SensoryHub
        hub = SensoryHub(storage_path="evidence/")
        artifact = await temporal.run_activity(
            wf_id, "Hub_Ingestion",
            lambda: hub.ingest_from_dms(provider="TEMPORAL_WF", filename=f"{bpo_id}_evidence.txt", content=sanitized_content)
        )
        temporal.set_query(wf_id, "progress", 0.35)

        # --- Stage 3: KIW Pipeline Pattern ---
        
        # 3.1. DECOMPOSE: Break domain into sub-tasks (simulated via requirement categories)
        temporal.set_query(wf_id, "current_step", "PIPELINE_DECOMPOSE")
        
        # 3.2. EXPLORE: Run specialized analyses in parallel
        temporal.set_query(wf_id, "current_step", "PIPELINE_EXPLORE")
        findings = []
        if domain.lower() == "network":
            dsa = NetworkDSA(domain_id="NW-001", standards_path="standards/network_golden.json")
            # In a real system, we might split the evidence and call multiple DSAs or the same DSA with sub-scopes
            findings = await temporal.run_activity(wf_id, "DSA_Explore_Domain", lambda: dsa.analyze(sanitized_content))
        elif domain.lower() == "cloud":
            from agents.cloud_dsa import CloudDSA
            dsa = CloudDSA(domain_id="CLD-001", standards_path="standards/cloud_golden.json")
            findings = await temporal.run_activity(wf_id, "DSA_Explore_Domain", lambda: dsa.analyze(sanitized_content))
        elif domain.lower() == "security":
            from agents.security_dsa import SecurityDSA
            dsa = SecurityDSA(domain_id="SEC-001", standards_path="standards/security_golden.json")
            findings = await temporal.run_activity(wf_id, "DSA_Explore_Domain", lambda: dsa.analyze(sanitized_content))

        else:
            temporal.fail_workflow(wf_id, "DOMAIN_NOT_SUPPORTED")
            return wf_id

        # 3.3. SYNTHESIZE: Combine findings (already combined in our mock, but we log it as a step)
        temporal.set_query(wf_id, "current_step", "PIPELINE_SYNTHESIZE")
        temporal.set_query(wf_id, "progress", 0.50)

        # 3.4. CRITIQUE: Peer review challenges the automated findings
        temporal.set_query(wf_id, "current_step", "PIPELINE_CRITIQUE")
        thinker = ThinkingAgent()
        critiques = await temporal.run_activity(
            wf_id, "Peer_Review", 
            lambda: thinker.critique_findings(findings)
        )

        
        # 3.5. VERIFY: check against hard constraints
        temporal.set_query(wf_id, "current_step", "PIPELINE_VERIFY")
        hard_violations = [f for f in findings if f.hard_constraint and f.status == "FAIL"]
        if hard_violations:
            logger.error(f"HARD_CONSTRAINT_VIOLATED in {wf_id}. Blocking Gate.")
            temporal.set_query(wf_id, "verification_error", "HARD_CONSTRAINT_VIOLATED")

        # --- Stage 4: Ethics & Security ---
        reasoning_sample = " ".join([f.reasoning for f in findings])
        ethics = EthicsManager()
        ethics_pass = await temporal.run_activity(
            wf_id, "Ethics_Audit", 
            lambda: ethics.audit_reasoning(agent_id=f"DSA-{domain}", reasoning_text=reasoning_sample)
        )
        temporal.set_query(wf_id, "progress", 0.70)

        # --- Stage 5: PMO Gate (Human-in-the-loop) ---
        # If hard violations exist, we still wait for signal, but pre-populate the rejection
        approval_data = await temporal.wait_for_signal(wf_id, "PMO_GATE_DECISION", timeout=3600)
        
        gate = PMOGate()
        gate_res = await temporal.run_activity(
            wf_id, "Finalize_Gate",
            lambda: gate.transition_status(artifact.id, GateStatus.PMO_CLEARED, approval_data.get("user_id", "KIW-LEAD"))
        )


        temporal.set_query(wf_id, "progress", 0.90)

        # --- Stage 6: Reporting & Synthesis ---
        from agents.csa_engine import CSA
        csa = CSA()
        report = await temporal.run_activity(
            wf_id, "Executive_Reporting",
            lambda: csa.synthesize_technical_to_executive(findings, bpo_id, critiques=critiques)
        )

        # --- Finalize ---
        temporal.complete_workflow(wf_id, {
            "report_id": report.report_id,
            "findings_count": len(findings),
            "governance_status": "KIW_CERTIFIED_DURABLE",
            "gate_log_artifact": gate_res.artifact_id
        })

        temporal.set_query(wf_id, "progress", 1.0)
        
        return wf_id

    except Exception as e:
        logger.error(f"Workflow {wf_id} failed: {e}")
        temporal.fail_workflow(wf_id, str(e))
        return wf_id

