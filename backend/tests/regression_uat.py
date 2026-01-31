import requests
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("REGRESSION-UAT")

BASE_URL = "http://localhost:8003"

def run_regression():
    logger.info("Initializing Holistic Regression Test Suite...")
    
    tests = [
        {"name": "Health Check", "path": "/", "method": "GET"},
        {"name": "DMS Ingestion", "path": "/ingest/dms", "method": "POST", "body": {"provider": "Reprosense", "filename": "test.vsdx", "content": "test"}},
        {"name": "Full Assessment Pipe", "path": "/analyze", "method": "POST", "body": {"bpo_id": "REG-001", "domain": "network", "content": "test"}},
        {"name": "Executive Reporting", "path": "/report", "method": "POST", "body": {"findings": [{"id": "1"}], "bpo_name": "TestCorp"}},
        {"name": "Specialty Deep Dive", "path": "/lab/dive?domain=bcp&context=test", "method": "POST"},
        {"name": "FS Asset Generation", "path": "/factory/generate?bpo_name=TestCorp", "method": "POST", "body": [{"id": "1"}]}
    ]
    
    results = []
    for test in tests:
        try:
            if test["method"] == "GET":
                resp = requests.get(f"{BASE_URL}{test['path']}")
            else:
                resp = requests.post(f"{BASE_URL}{test['path']}", json=test.get("body", {}))
            
            status = "PASS" if resp.status_code == 200 else "FAIL"
            logger.info(f"Test: {test['name']} -> {status}")
            results.append({"test": test["name"], "status": status})
        except Exception as e:
            logger.error(f"Test: {test['name']} -> ERROR: {str(e)}")
            results.append({"test": test["name"], "status": "ERROR"})
            
    return results

if __name__ == "__main__":
    run_regression()
