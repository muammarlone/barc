import uuid
from datetime import datetime
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class GADOSNode(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    type: str
    label: str
    properties: Dict[str, Any] = Field(default_factory=dict)
    coordinates: Optional[Dict[str, float]] = None

class GADOSEdge(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    source: str
    target: str
    type: str
    weight: Optional[Dict[str, float]] = None
    properties: Dict[str, Any] = Field(default_factory=dict)

class GADOSMetadata(BaseModel):
    kiw_id: str
    version: str = "2.0"
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    fingerprint: str
    source_ref: Optional[str] = None

class GADOSGraph(BaseModel):
    nodes: List[GADOSNode]
    edges: List[GADOSEdge]
    metadata: GADOSMetadata

    def to_adjacency_matrix(self) -> List[List[int]]:
        pass
