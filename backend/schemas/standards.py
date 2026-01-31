from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

class Severity(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"

class AtomicRequirement(BaseModel):
    id: str
    title: str
    description: str
    severity: Severity
    category: str
    metric: Optional[str] = None
    threshold: Optional[str] = None

class DomainStandard(BaseModel):
    domain_id: str
    domain_name: str
    version: str
    requirements: List[AtomicRequirement]
