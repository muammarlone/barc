from agents.dsa_framework import BaseDSA, Finding
import logging

logger = logging.getLogger("Security-DSA")

class SecurityDSA(BaseDSA):
    """
    Cybersecurity Domain Specialist Agent.
    Focuses on Zero Trust, MFA, and threat boundary integrity.
    """
    async def analyze(self, evidence_data: str) -> list[Finding]:
        logger.info(f"Analyzing Security posture for evidence length: {len(evidence_data)}")
        findings = []
        for req in self.get_requirements():
            status = "PASS"
            reasoning = "Security controls align with KIW Golden Standards."
            is_hard = (req["id"] == "SEC-001") # MFA is mandatory
            
            if "mfa" not in evidence_data.lower() and req["id"] == "SEC-001":
                status = "FAIL"
                reasoning = "Critical security gap: MFA not explicitly mentioned in BPO evidence."
            
            findings.append(Finding(
                requirement_id=req["id"],
                sub_task=req.get("category", "Identity"),
                status=status,
                evidence_snippet=evidence_data[:100] + "...",
                reasoning=reasoning,
                severity=req["severity"],
                hard_constraint=is_hard
            ))
        return findings
