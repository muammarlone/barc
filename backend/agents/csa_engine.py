from pydantic import BaseModel
from typing import List, Dict
from datetime import datetime
import uuid

class Report(BaseModel):

    report_id: str
    target_audience: str
    summary: str
    critical_findings: int
    recommendation: str
    timestamp: str

class CSA:
    @staticmethod
    def synthesize_technical_to_executive(findings: List[Dict], bpo_name: str) -> Report:
        # Mock logic to translate technical findings to McKinsey-style executive bullets
        critical_count = sum(1 for f in findings if f.get("severity") == "CRITICAL" and f.get("status") == "FAIL")
        
        summary = f"Architectural review for {bpo_name} indicates "
        if critical_count > 0:
            summary += f"significant risk with {critical_count} critical infrastructure gaps identified."
            recommendation = "HOLD ONBOARDING. Immediate remediation required for critical path items."
        else:
            summary += "operational stability. Infrastructure meets the minimum 92% compliance threshold."
            recommendation = "PROCEED with caution. Monitor secondary risk items during hypercare."
            
        return Report(
            report_id=f"EXEC-{uuid.uuid4().hex[:6].upper()}",
            target_audience="Executive Leadership (PMO)",
            summary=summary,
            critical_findings=critical_count,
            recommendation=recommendation,
            timestamp=datetime.now().isoformat()
        )
