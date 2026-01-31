import asyncio
import uuid
import logging
import inspect
from datetime import datetime
from typing import Dict, Any, Callable


logger = logging.getLogger("Temporal-Sim")

import json
import os

class TemporalSimulation:
    """
    Enhanced Simulation Layer for Temporal Orchestration.
    Supports: Multi-Tenancy, Signals, Queries, Durability (Persistence).
    """
    def __init__(self, persistence_path: str = "temporal_state.json"):
        self.persistence_path = persistence_path
        self.active_workflows = {}
        self.workflow_history = {}
        self.workflow_signals = {} # workflow_id -> queue of signals
        self.tenants = {} # tenant_id -> list of workflow_ids
        self._load_state()

    def _save_state(self):
        """Persists the current state to disk."""
        try:
            state = {
                "active_workflows": self.active_workflows,
                "workflow_history": self.workflow_history,
                "tenants": self.tenants
            }
            with open(self.persistence_path, "w") as f:
                json.dump(state, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save temporal state: {e}")

    def _load_state(self):
        """Loads state from disk if it exists."""
        if os.path.exists(self.persistence_path):
            try:
                with open(self.persistence_path, "r") as f:
                    state = json.load(f)
                    self.active_workflows = state.get("active_workflows", {})
                    self.workflow_history = state.get("workflow_history", {})
                    self.tenants = state.get("tenants", {})
                    # Signals cannot be persisted easily as they are queues
                    for wf_id in self.active_workflows:
                        self.workflow_signals[wf_id] = asyncio.Queue()
                logger.info("Temporal state loaded from persistence.")
            except Exception as e:
                logger.error(f"Failed to load temporal state: {e}")

    async def execute_workflow(self, workflow_name: str, input_data: Dict[str, Any], tenant_id: str = "DEFAULT", workflow_id: str = None) -> str:
        if not workflow_id:
            workflow_id = f"WF-{uuid.uuid4().hex[:6].upper()}"

        self.active_workflows[workflow_id] = {
            "name": workflow_name,
            "status": "RUNNING",
            "start_time": datetime.now().isoformat(),
            "input": input_data,
            "tenant": tenant_id,
            "current_step": "START",
            "queries": {} # Store queryable state
        }
        self.workflow_history[workflow_id] = []
        self.workflow_signals[workflow_id] = asyncio.Queue()
        
        if tenant_id not in self.tenants:
            self.tenants[tenant_id] = []
        self.tenants[tenant_id].append(workflow_id)
        
        self._save_state()
        logger.info(f"Temporal Workflow Started: {workflow_id} ({workflow_name}) for Tenant: {tenant_id}")
        return workflow_id

    async def wait_for_signal(self, workflow_id: str, signal_name: str, timeout: int = 600) -> Any:
        """Wait for an external signal (e.g. Human Approval)."""
        logger.info(f"Workflow {workflow_id} waiting for signal: {signal_name}")
        self.active_workflows[workflow_id]["status"] = "WAITING"
        self.active_workflows[workflow_id]["current_step"] = f"WAIT_SIGNAL:{signal_name}"
        self._save_state()
        
        try:
            # In simulation, we wait on the internal queue
            signal_data = await asyncio.wait_for(self.workflow_signals[workflow_id].get(), timeout=timeout)
            logger.info(f"Workflow {workflow_id} received signal: {signal_name}")
            self.active_workflows[workflow_id]["status"] = "RUNNING"
            return signal_data
        except asyncio.TimeoutError:
            logger.error(f"Signal {signal_name} TIMEOUT for workflow {workflow_id}")
            raise Exception("WORKFLOW_SIGNAL_TIMEOUT")

    def signal_workflow(self, workflow_id: str, signal_name: str, data: Any):
        """Send a signal to an active workflow."""
        if workflow_id in self.workflow_signals:
            self.workflow_signals[workflow_id].put_nowait(data)
            logger.info(f"Signal {signal_name} sent to workflow {workflow_id}")
        else:
            raise Exception(f"Workflow {workflow_id} not signalable.")

    def set_query(self, workflow_id: str, query_name: str, data: Any):
        """Update a queryable property of the workflow."""
        if workflow_id in self.active_workflows:
            self.active_workflows[workflow_id]["queries"][query_name] = data
            self._save_state()

    def query_workflow(self, workflow_id: str, query_name: str) -> Any:
        """Query state from an active workflow."""
        wf = self.active_workflows.get(workflow_id)
        if wf:
            return wf["queries"].get(query_name)
        return None


    async def run_activity(self, workflow_id: str, activity_name: str, activity_fn: Callable, *args, **kwargs):
        if workflow_id not in self.active_workflows:
            raise Exception(f"Workflow {workflow_id} not found.")
        
        wf = self.active_workflows[workflow_id]
        wf["current_step"] = activity_name
        
        logger.info(f"Temporal Activity Started: {activity_name} in {workflow_id}")
        
        try:
            # Execute the activity function
            result = activity_fn(*args, **kwargs)
            
            # If the result is a coroutine/awaitable (e.g. async def called via lambda), await it
            if inspect.isawaitable(result):
                result = await result

                
            self.workflow_history[workflow_id].append({


                "activity": activity_name,
                "status": "COMPLETED",
                "timestamp": datetime.now().isoformat(),
                "result_summary": str(result)[:100]
            })
            self._save_state()
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

    def complete_workflow(self, workflow_id: str, result: Any):
        """Marks a workflow as successfully completed."""
        if workflow_id in self.active_workflows:
            wf = self.active_workflows[workflow_id]
            wf["status"] = "COMPLETED"
            wf["result"] = result
            wf["end_time"] = datetime.now().isoformat()
            self._save_state()
            logger.info(f"Temporal Workflow Completed: {workflow_id}")

    def fail_workflow(self, workflow_id: str, error: str):
        """Marks a workflow as failed."""
        if workflow_id in self.active_workflows:
            wf = self.active_workflows[workflow_id]
            wf["status"] = "FAILED"
            wf["error"] = error
            wf["end_time"] = datetime.now().isoformat()
            self._save_state()
            logger.error(f"Temporal Workflow Failed: {workflow_id} - Error: {error}")

    def get_status(self, workflow_id: str) -> Dict[str, Any]:
        return {
            "workflow": self.active_workflows.get(workflow_id),
            "history": self.workflow_history.get(workflow_id)
        }

# Global Simulation Instance
temporal = TemporalSimulation()
