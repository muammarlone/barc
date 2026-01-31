from enum import Enum
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class GateStatus(str, Enum):
    DRAFT = "DRAFT"
    INTERNAL_APPROVED = "INTERNAL_APPROVED"
    PMO_CLEARED = "PMO_CLEARED"
    DISTRIBUTED = "DISTRIBUTED"

class GateLog(BaseModel):
    artifact_id: str
    current_status: GateStatus
    updated_by: str
    timestamp: str

class PMOGate:
    def __init__(self):
        self.registry = {}

    def transition_status(self, artifact_id: str, new_status: GateStatus, user_id: str) -> GateLog:
        # State Machine Logic
        # e.g., Cannot go to DISTRIBUTED unless PMO_CLEARED
        self.registry[artifact_id] = new_status
        return GateLog(
            artifact_id=artifact_id,
            current_status=new_status,
            updated_by=user_id,
            timestamp=datetime.now().isoformat()
        )

    def is_locked(self, artifact_id: str) -> bool:
        status = self.registry.get(artifact_id, GateStatus.DRAFT)
        return status != GateStatus.DISTRIBUTED
