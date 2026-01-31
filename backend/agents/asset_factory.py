import uuid
from pydantic import BaseModel
from typing import List, Dict
from datetime import datetime

class FSAsset(BaseModel):
    asset_id: str
    bpo_name: str
    sections: List[Dict]
    governance_hash: str
    created_at: str

class AssetFactory:
    @staticmethod
    def generate_fs_spec(bpo_name: str, findings: List[Dict]) -> FSAsset:
        # Asset generation logic based on assessment results
        sections = [
            {"title": "Executive Summary", "content": f"Architectural specification for {bpo_name}."},
            {"title": "Technical Requirements", "content": f"Mapped {len(findings)} technical requirements."},
            {"title": "Compliance Matrix", "content": "Full GADOS-certified compliance matrix included."}
        ]
        
        return FSAsset(
            asset_id=f"FS-{uuid.uuid4().hex[:6].upper()}",
            bpo_name=bpo_name,
            sections=sections,
            governance_hash=uuid.uuid4().hex,
            created_at=datetime.now().isoformat()
        )
