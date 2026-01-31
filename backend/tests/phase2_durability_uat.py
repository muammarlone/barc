import requests
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("PHASE2-UAT")

BASE_URL = "http://localhost:8005"

def run_phase2_uat():
    logger.info("Initializing Phase 2 Durable Orchestration UAT...")
    
    # 1. Start Workflow (Tenant: KIW-UK)
    logger.info("STEP 1: Starting Durable Workflow...")
    headers = {"x-tenant-id": "KIW-UK"}
    payload = {
        "bpo_id": "UK-BPO-001",
        "domain": "network",
        "content": "Deep assessment required."
    }
    r1 = requests.post(f"{BASE_URL}/temporal/start", json=payload, headers=headers)
    wf_id = r1.json().get("workflow_id")
    logger.info(f"Workflow Started: {wf_id} for Tenant: KIW-UK")
    
    # 2. Check Status (Immediate)
    logger.info("STEP 2: Checking Workflow Status (Initial)...")
    time.sleep(1)
    r2 = requests.get(f"{BASE_URL}/temporal/status/{wf_id}")
    status = r2.json()["workflow"]["status"]
    progress = r2.json()["progress"]
    logger.info(f"Current Status: {status}, Progress: {progress}")
    
    # 3. Verify Tenant List
    logger.info("STEP 3: Verifying Tenant Workflow List...")
    r3 = requests.get(f"{BASE_URL}/temporal/tenant/KIW-UK")
    logger.info(f"Tenant 'KIW-UK' Workflows: {r3.json().get('workflows')}")
    
    # 4. Signal Approval (Human-in-the-Loop)
    logger.info("STEP 4: Signaling PMO Approval...")
    r4 = requests.post(f"{BASE_URL}/temporal/signal/{wf_id}?signal_name=PMO_GATE_DECISION", json={"user_id": "KIW-ARCHITECT-5"})
    logger.info(f"Signal Result: {r4.status_code}")
    
    # 5. Final Status Check
    logger.info("STEP 5: Checking Final Workflow Completion...")
    time.sleep(2)
    r5 = requests.get(f"{BASE_URL}/temporal/status/{wf_id}")
    final_status = r5.json()["workflow"]["status"]
    final_result = r5.json()["workflow"]["result"]
    logger.info(f"Final Status: {final_status}")
    logger.info(f"Final Result: {json.dumps(final_result, indent=2)}")

if __name__ == "__main__":
    import json
    run_phase2_uat()
