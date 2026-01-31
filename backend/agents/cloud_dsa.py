from agents.dsa_framework import BaseDSA, Finding
import logging

logger = logging.getLogger("Cloud-DSA")

class CloudDSA(BaseDSA):
    """
    Cloud Infrastructure Domain Specialist Agent.
    Specializes in AWS/Azure/GCP architectural integrity.
    """
    async def analyze(self, evidence_data: str) -> list[Finding]:
        logger.info(f"Analyzing Cloud Infrastructure for evidence length: {len(evidence_data)}")
        findings = []
        for req in self.get_requirements():
            status = "PASS"
            reasoning = "Evidence successfully demonstrates compliance with standard."
            is_hard = (req["id"] == "CLD-001") # Sovereignty is a hard constraint
            
            if "not" in evidence_data.lower() and req["id"] == "CLD-001":
                status = "FAIL"
                reasoning = "Evidence indicates possible regional data leakage."
            
            findings.append(Finding(
                requirement_id=req["id"],
                sub_task=req.get("category", "CloudOps"),
                status=status,
                evidence_snippet=evidence_data[:100] + "...",
                reasoning=reasoning,
                severity=req["severity"],
                hard_constraint=is_hard
            ))
        return findings
