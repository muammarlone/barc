import json
import os
import logging
from typing import List, Dict, Optional
from datetime import datetime

logger = logging.getLogger("LTM-Agent")

class LTMAgent:
    """
    Manages the Long-Term Memory (LTM) of the BARC platform.
    Allows AI personas to retrieve historical context from previous assessments.
    """
    def __init__(self, memory_path: str = "gados-project/memory/assessment_history.json"):
        self.memory_path = memory_path
        self._ensure_storage()

    def _ensure_storage(self):
        os.makedirs(os.path.dirname(self.memory_path), exist_ok=True)
        if not os.path.exists(self.memory_path):
            with open(self.memory_path, 'w') as f:
                json.dump([], f)

    def store_assessment(self, assessment_id: str, findings: List[Dict], decisions: List[Dict]):
        """Stores a summarized version of the assessment for future retrieval."""
        try:
            with open(self.memory_path, 'r+') as f:
                history = json.load(f)
                history.append({
                    "assessment_id": assessment_id,
                    "timestamp": datetime.now().isoformat(),
                    "summary_findings": findings[:5], # Store top 5 key findings
                    "key_decisions": decisions
                })
                f.seek(0)
                json.dump(history, f, indent=2)
                f.truncate()
            logger.info(f"Assessment {assessment_id} successfully persisted to LTM.")
        except Exception as e:
            logger.error(f"Failed to store memory: {e}")

    def retrieve_context(self, domain_id: str, query_keywords: List[str]) -> List[Dict]:
        """Retrieves relevant historical findings based on domain and keywords."""
        try:
            with open(self.memory_path, 'r') as f:
                history = json.load(f)
                # Simple keyword matching for Pilot; would use vector embeddings in production
                relevant = [
                    h for h in history 
                    if any(k.lower() in str(h).lower() for k in query_keywords)
                ]
                return relevant[-3:] # Return last 3 relevant entries
        except Exception as e:
            logger.error(f"Failed to retrieve memory: {e}")
            return []
