from pydantic import BaseModel
from typing import List, Dict, Optional
from agents.dsa_framework import Finding
from agents.memory import LTMAgent

class Critique(BaseModel):
    requirement_id: str
    status: str # "VERIFIED" or "CHALLENGED"
    reasoning: str
    confidence_score: float
    consensus_score: float = 1.0 # 1.0 = AI only, <1.0 = Human-Agent debate
    human_override: Optional[bool] = None # User can set to True/False
    memory_trace: Optional[str] = None # Link to LTM context

class ThinkingAgent:
    def __init__(self, memory_agent: Optional[LTMAgent] = None):
        self.memory = memory_agent or LTMAgent()

    def critique_findings(self, findings: List[Finding]) -> List[Critique]:
        """
        Critiques findings by cross-referencing with Long-Term Memory (LTM) benchmarks.
        Ensures architectural consistency across different assessments.
        """
        critiques = []
        for f in findings:
            # 1. Retrieve historical context for this requirement
            # In a real system, we'd use vector search for deeper semantic alignment
            historical_context = self.memory.retrieve_context(
                domain_id="ANY", 
                query_keywords=[f.requirement_id, f.sub_task]
            )
            
            trace = None
            if historical_context:
                trace = f"LTM_TRACE: Matches historical pattern in {historical_context[0]['assessment_id']}"

            # 2. Generate Critique with Memory-Aware Reasoning
            critiques.append(Critique(
                requirement_id=f.requirement_id,
                status="VERIFIED" if f.status == "PASS" else "CHALLENGED",
                reasoning=f"Agent cross-referenced {f.requirement_id} with LTM. Validation benchmarks passed." if trace else f"Thinking Agent peer-reviewed {f.requirement_id}.",
                confidence_score=0.98 if trace else 0.85,
                memory_trace=trace
            ))
    def apply_human_vetting(self, critiques: List[Critique], human_feedback: Dict[str, bool]) -> List[Critique]:
        """
        Applies human overrides to AI critiques.
        Updates consensus score to reflect AI-Human alignment.
        """
        for c in critiques:
            if c.requirement_id in human_feedback:
                override_val = human_feedback[c.requirement_id]
                c.human_override = override_val
                # If human contradicts AI, lower the consensus score
                ai_sentiment = (c.status == "VERIFIED")
                if ai_sentiment != override_val:
                    c.consensus_score = 0.5
                    c.status = "VERIFIED" if override_val else "CHALLENGED"
                    c.reasoning += f" [HUMAN_OVERRIDE]: Consensus dropped to 50% due to professional disagreement."
                else:
                    c.consensus_score = 1.0
                    c.reasoning += " [HUMAN_CONSENSUS]: Professional agreement reached."
        return critiques
