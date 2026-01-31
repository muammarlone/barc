import asyncio
import uuid
import logging
from datetime import datetime
from typing import Dict, Any, Callable

logger = logging.getLogger("Temporal-Sim")

class TemporalSimulation:
    """
    A simulation layer for Temporal Orchestration.
    Mimics Workflows, Activities, and Durable State.
    """
    def __init__(self):
        self.active_workflows = {}
        self.workflow_history = {}

    async def execute_workflow(self, workflow_name: str, input_data: Dict[str, Any]) -> str:
        workflow_id = f"WF-{uuid.uuid4().hex[:6].upper()}"
        self.active_workflows[workflow_id] = {
            "name": workflow_name,
            "status": "RUNNING",
            "start_time": datetime.now().isoformat(),
            "input": input_data,
            "current_step": "START"
        }
        self.workflow_history[workflow_id] = []
        logger.info(f"Temporal Workflow Started: {workflow_id} ({workflow_name})")
        return workflow_id

    async def run_activity(self, workflow_id: str, activity_name: str, activity_fn: Callable, *args, **kwargs):
        if workflow_id not in self.active_workflows:
            raise Exception(f"Workflow {workflow_id} not found.")
        
        wf = self.active_workflows[workflow_id]
        wf["current_step"] = activity_name
        
        logger.info(f"Temporal Activity Started: {activity_name} in {workflow_id}")
        
        try:
            # Handle both sync and async activity functions
            if asyncio.iscoroutinefunction(activity_fn):
                result = await activity_fn(*args, **kwargs)
            else:
                result = activity_fn(*args, **kwargs)
                
            self.workflow_history[workflow_id].append({

                "activity": activity_name,
                "status": "COMPLETED",
                "timestamp": datetime.now().isoformat(),
                "result_summary": str(result)[:100]
            })
            return result
        except Exception as e:
            logger.error(f"Activity {activity_name} Failed. Recording failure for retry.")
            self.workflow_history[workflow_id].append({
                "activity": activity_name,
                "status": "FAILED",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            })
            raise e

    def get_status(self, workflow_id: str) -> Dict[str, Any]:
        return {
            "workflow": self.active_workflows.get(workflow_id),
            "history": self.workflow_history.get(workflow_id)
        }

# Global Simulation Instance
temporal = TemporalSimulation()
