import os
import uuid
from datetime import datetime
from typing import List, Dict
from pydantic import BaseModel

class IngestedArtifact(BaseModel):

    id: str
    source: str
    filename: str
    category: str
    timestamp: str

class SensoryHub:
    def __init__(self, storage_path: str):
        self.storage_path = storage_path
        os.makedirs(storage_path, exist_ok=True)

    def ingest_from_dms(self, provider: str, filename: str, content: str) -> IngestedArtifact:
        # Mocking DMS Ingestion
        artifact_id = f"TRC-{uuid.uuid4().hex[:8].upper()}"
        file_path = os.path.join(self.storage_path, f"{artifact_id}_{filename}")
        
        with open(file_path, 'w') as f:
            f.write(content)
            
        return IngestedArtifact(
            id=artifact_id,
            source=provider,
            filename=filename,
            category="DMS_SYNC",
            timestamp=datetime.now().isoformat()
        )

    def ingest_from_email(self, sender: str, subject: str, attachment_content: str) -> IngestedArtifact:
        # Mocking Email Ingestion & Auto-Categorization
        artifact_id = f"EML-{uuid.uuid4().hex[:8].upper()}"
        
        # Simple rule-based categorization for the mock
        category = "GOV_RISK" if "risk" in subject.lower() else "TECH_EVIDENCE"
        
        return IngestedArtifact(
            id=artifact_id,
            source="OUTLOOK_INGEST",
            filename=f"EMAIL_ATTACHMENT_{artifact_id}.txt",
            category=category,
            timestamp=datetime.now().isoformat()
        )
