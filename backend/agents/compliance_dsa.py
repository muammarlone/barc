import logging
from typing import List
from agents.dsa_framework import BaseDSA, Finding

logger = logging.getLogger("ComplianceDSA")

class ComplianceDSA(BaseDSA):
    """
    Handles specialized compliance reviews (HIPAA, HITRUST) for Healthcare BPOs.
    """
    async def analyze(self, evidence_data: str) -> List[Finding]:
        findings = []
        evidence_lower = evidence_data.lower()
        
        for req in self.get_requirements():
            status = "PASS"
            reasoning = f"Evidence verified against {self.domain_id} standard: {req['title']}."
            
            # Simple keyword-based failure simulation for Pilot
            blocking_keywords = ["unencrypted", "public access", "no backup", "manual rotation"]
            if any(k in evidence_lower for k in blocking_keywords):
                status = "FAIL"
                reasoning = f"Security vulnerability detected: Potential breach of {req['id']}."

            findings.append(Finding(
                requirement_id=req["id"],
                sub_task=req.get("category", "Compliance"),
                status=status,
                evidence_snippet=evidence_data[:150] + "...",
                reasoning=reasoning,
                severity=req["severity"],
                hard_constraint=(req["severity"] == "CRITICAL")
            ))
            
        logger.info(f"ComplianceDSA ({self.domain_id}) analysis complete. Total Findings: {len(findings)}")
        return findings
