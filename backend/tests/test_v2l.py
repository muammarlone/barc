import requests
import json

BASE_URL = "http://127.0.0.1:8010"

def test_v2l_compliance():
    print("🚀 Initiating V2L Parser Verification Test...")
    
    # 1. Simulate a "Non-Compliant" Architecture (Only 1 circuit, high latency)
    fail_payload = {
        "primitives": [
            {"type": "node", "category": "Region", "name": "AWS-East-1", "coords": {"x": 100.0, "y": 100.0}},
            {"type": "node", "category": "BPO-Station", "name": "LATAM-Node-01", "coords": {"x": 200.0, "y": 200.0}},
            {
                "type": "edge", "from": "AWS-East-1", "to": "LATAM-Node-01", 
                "protocol": "WebRTC", "weight": {"latency_ms": 185.0}
            }
        ]
    }
    
    print("\n[SCENARIO A] Testing Non-Compliant Architecture (Single Circuit + 185ms Latency)...")
    response = requests.post(f"{BASE_URL}/analyze/v2l", json=fail_payload)
    try:
        data = response.json()
    except Exception as e:
        print(f"❌ JSON Decode Error: {e}")
        print(f"Raw Response: {response.text}")
        return
    
    print(f"Status: {data['governance_status']}")
    print(f"Verification: {data['verification']['status']}")
    for f in data['verification']['findings']:
        print(f"  - {f['req_id']}: {f['status']} | {f['finding']}")

    # 2. Simulate a "Compliant" Architecture (2 circuits, low latency)
    pass_payload = {
        "primitives": [
            {"type": "node", "category": "Region", "name": "AWS-East-1", "coords": {"x": 100.0, "y": 100.0}},
            {"type": "node", "category": "Cloud", "name": "Azure-Central", "coords": {"x": 150.0, "y": 100.0}},
            {"type": "node", "category": "BPO-Station", "name": "LATAM-Node-01", "coords": {"x": 250.0, "y": 200.0}},
            {
                "type": "edge", "from": "AWS-East-1", "to": "LATAM-Node-01", 
                "protocol": "WebRTC", "weight": {"latency_ms": 120.0}
            },
            {
                "type": "edge", "from": "Azure-Central", "to": "LATAM-Node-01", 
                "protocol": "WebRTC", "weight": {"latency_ms": 110.0}
            }
        ]
    }
    
    print("\n[SCENARIO B] Testing Compliant Architecture (Dual Circuit + <150ms Latency)...")
    response = requests.post(f"{BASE_URL}/analyze/v2l", json=pass_payload)
    data = response.json()
    
    print(f"Status: {data['governance_status']}")
    print(f"Verification: {data['verification']['status']}")
    print(f"Fingerprint: {data['graph']['metadata']['fingerprint']}")
    for f in data['verification']['findings']:
        print(f"  - {f['req_id']}: {f['status']} | {f['finding']}")

if __name__ == "__main__":
    try:
        test_v2l_compliance()
    except Exception as e:
        print(f"❌ Test Failed: {e}")
