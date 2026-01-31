import requests
import json
import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ADVERSARIAL-RESILIENCE")

BASE_URL = "http://localhost:8003"

def run_adversarial_tests():
    logger.info("Initializing Adversarial Resilience & Chaos Test Suite...")
    
    # 1. Chaos Injection
    logger.info("TEST 1: Chaos Injection & Circuit Breaker Triggering")
    requests.post(f"{BASE_URL}/chaos/toggle?active=true")
    
    # Try 1: Should fail (Chaos)
    r1 = requests.post(f"{BASE_URL}/analyze", json={"bpo_id": "CHAOS-001", "domain": "network", "content": "test"})
    logger.info(f"Attempt 1 Result: {r1.status_code} ({r1.json().get('detail')})")
    
    # Try 2: Should fail (Chaos) and trigger Circuit Breaker
    r2 = requests.post(f"{BASE_URL}/analyze", json={"bpo_id": "CHAOS-001", "domain": "network", "content": "test"})
    logger.info(f"Attempt 2 Result: {r2.status_code} ({r2.json().get('detail')})")
    
    # Try 3: Should fail with 503 (Circuit Breaker OPEN)
    r3 = requests.post(f"{BASE_URL}/analyze", json={"bpo_id": "CHAOS-001", "domain": "network", "content": "test"})
    logger.info(f"Attempt 3 (OPEN) Result: {r3.status_code} ({r3.json().get('detail')})")
    
    # 2. Recovery Test
    logger.info("TEST 2: System Recovery & MFA Verification")
    requests.post(f"{BASE_URL}/chaos/toggle?active=false")
    logger.info("Waiting 10s for Circuit Breaker recovery...")
    time.sleep(11)
    
    # Recovery Attempt
    r4 = requests.post(f"{BASE_URL}/analyze", json={"bpo_id": "REC-001", "domain": "network", "content": "test"})
    token_id = r4.json().get("zta_token")
    logger.info(f"Recovery Result: {r4.status_code}. New ZTA Token: {token_id}")
    
    # 3. MFA Challenge
    logger.info("TEST 3: MFA Governance Challenge")
    r5 = requests.post(f"{BASE_URL}/zta/mfa?token_id={token_id}&code=KIW-2026")
    logger.info(f"MFA Challenge Result: {r5.status_code} ({r5.json().get('status')})")

if __name__ == "__main__":
    run_adversarial_tests()
