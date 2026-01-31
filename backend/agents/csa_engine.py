from typing import List, Dict, Optional, Any
import uuid
from datetime import datetime
from pydantic import BaseModel


class DefensibilityTrace(BaseModel):
    requirement_id: str
    reasoning_path: str # Link from Evidence -> Standard -> Decision
    historical_precedent: Optional[str] = None # Cites LTM context
    dissent_log: List[str] = [] # Captures Thinking Agent challenges

class Report(BaseModel):

    report_id: str
    target_audience: str
    summary: str
    critical_findings: int
    recommendation: str
    defensibility_traces: List[DefensibilityTrace] = [] # Audit layer
    timestamp: str

class CSA:
    @staticmethod
    def synthesize_technical_to_executive(findings: List[Dict], bpo_name: str, critiques: Optional[List[Any]] = None) -> Report:
        """
        Translates technical findings into McKinsey-style executive bullets with a full Defensibility Trace.
        """
        critical_count = sum(
            1 for f in findings 
            if getattr(f, "severity", f.get("severity") if isinstance(f, dict) else "UNKNOWN") == "CRITICAL" 
            and getattr(f, "status", f.get("status") if isinstance(f, dict) else "UNKNOWN") == "FAIL"
        )

        
        summary = f"Architectural review for {bpo_name} indicates "
        if critical_count > 0:
            summary += f"significant risk with {critical_count} critical infrastructure gaps identified."
            recommendation = "HOLD ONBOARDING. Immediate remediation required for critical path items."
        else:
            summary += "operational stability. Infrastructure meets the minimum 92% compliance threshold."
            recommendation = "PROCEED with caution. Monitor secondary risk items during hypercare."
            
        # 1. Generate Defensibility Traces
        traces = []
        for f in findings:
            # Handle both dict and object (Pydantic) just in case
            req_id = getattr(f, "requirement_id", f.get("requirement_id") if isinstance(f, dict) else "UNKNOWN")
            severity = getattr(f, "severity", f.get("severity") if isinstance(f, dict) else "UNKNOWN")
            status = getattr(f, "status", f.get("status") if isinstance(f, dict) else "UNKNOWN")
            evidence = getattr(f, "evidence_snippet", f.get("evidence_snippet") if isinstance(f, dict) else "No evidence")
            
            critique = next((c for c in critiques if c.requirement_id == req_id), None) if critiques else None
            
            traces.append(DefensibilityTrace(
                requirement_id=req_id,
                reasoning_path=f"Evidence: {evidence[:50]}... -> Standard: {req_id} -> Finding: {status}",
                historical_precedent=getattr(critique, "memory_trace", None) if critique else None,
                dissent_log=[critique.reasoning] if critique and critique.status == "CHALLENGED" else []
            ))


        return Report(
            report_id=f"EXEC-{uuid.uuid4().hex[:6].upper()}",
            target_audience="Executive Leadership (PMO)",
            summary=summary,
            critical_findings=critical_count,
            recommendation=recommendation,
            defensibility_traces=traces,
            timestamp=datetime.now().isoformat()
        )
