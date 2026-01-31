import json
from abc import ABC, abstractmethod
from typing import List, Dict
from pydantic import BaseModel

class Finding(BaseModel):
    requirement_id: str
    sub_task: str # e.g. "Bandwidth", "Security", "Redundancy"
    status: str # "PASS" or "FAIL"
    evidence_snippet: str
    reasoning: str
    severity: str
    hard_constraint: bool = False # If True, failure blocks the gate automatically

class BaseDSA(ABC):
    """
    Abstract Base Class for Domain Specialist Agents (DSAs).
    Every domain (Network, Desktop, Cloud) must implement the 'analyze' method.
    """
    def __init__(self, domain_id: str, standards_path: str):
        """
        Initializes the agent with a domain ID and paths to the Golden Standards JSON.
        """
        self.domain_id = domain_id
        with open(standards_path, 'r') as f:
            self.standards = json.load(f)

    @abstractmethod
    async def analyze(self, evidence_data: str) -> List[Finding]:
        """
        Core analysis logic where the agent maps evidence against architectural standards.
        Returns a list of granular Findings.
        """
        pass

    def get_requirements(self) -> List[Dict]:
        """Returns the list of requirements from the loaded domain standard."""
        return self.standards.get("requirements", [])


# Specialist Implementation for Network
class NetworkDSA(BaseDSA):
    async def analyze(self, evidence_data: str) -> List[Finding]:
        findings = []
        for req in self.get_requirements():
            # Hard constraint logic: NW-REQ-01 is mandatory
            is_hard = (req["id"] == "NW-REQ-01")
            
            findings.append(Finding(
                requirement_id=req["id"],
                sub_task=req.get("category", "General"),
                status="PASS",
                evidence_snippet="Simulated evidence for " + req["title"],
                reasoning="Evidence matches standard benchmarks.",
                severity=req["severity"],
                hard_constraint=is_hard
            ))
        return findings
