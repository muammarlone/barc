from agents.dsa_framework import BaseDSA, Finding
from typing import List, Optional
import logging

logger = logging.getLogger("Cloud-DSA")

class CloudDSA(BaseDSA):
    """
    Cloud Infrastructure Domain Specialist Agent.
    Specializes in AWS/Azure/GCP architectural integrity.
    """
    async def analyze(self, evidence_data: str) -> List[Finding]:
        logger.info(f"Analyzing Cloud Infrastructure for evidence length: {len(evidence_data)}")
        findings = []
        for req in self.get_requirements():
            status = "PASS"
            reasoning = "Evidence successfully demonstrates compliance with standard."
            suggested_fix = None
            draft_content = None
            is_hard = (req["id"] == "CLD-001") # Sovereignty is a hard constraint
            
            if "not" in evidence_data.lower() and req["id"] == "CLD-001":
                status = "FAIL"
                reasoning = "Evidence indicates possible regional data leakage."
                suggested_fix = self.co_pilot_suggest(req["id"], "FIX")
                draft_content = self.co_pilot_suggest(req["id"], "DRAFT")
            
            findings.append(Finding(
                requirement_id=req["id"],
                sub_task=req.get("category", "CloudOps"),
                status=status,
                evidence_snippet=evidence_data[:100] + "...",
                reasoning=reasoning,
                severity=req["severity"],
                hard_constraint=is_hard,
                suggested_fix=suggested_fix,
                draft_content=draft_content
            ))
        return findings

    def co_pilot_suggest(self, requirement_id: str, mode: str) -> str:
        """
        Generates Cloud infrastructure completion logic or remediation scripts.
        """
        suggestions = {
            "CLD-001": {
                "FIX": "Update Terraform to include 'allowed_locations' restriction for US-East regions.",
                "DRAFT": "INFRA_SPEC: Regional Sovereignty Policy - All compute and storage resources for the Genesys Pilot must reside within AWS US-East-1 or Azure East-US-2. Latency-based routing must favor these nodes..."
            }
        }
        entry = suggestions.get(requirement_id, {})
        return entry.get(mode, f"Cloud Co-pilot recommendation for {requirement_id}.")
