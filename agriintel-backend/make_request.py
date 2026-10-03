import requests
import json
import sys

base_url = "http://127.0.0.1:8000"

print("Step 1: Logging in with correct credentials...")
login_resp_1 = requests.post(f"{base_url}/auth/login", json={"email": "test3@test.com", "password": "testpass123"})
print(f"Status: {login_resp_1.status_code}")
if login_resp_1.status_code == 200:
    token = login_resp_1.json().get("access_token")
    print(f"Token length: {len(token) if token else 0} characters")
else:
    print(f"Response: {login_resp_1.text}")
    sys.exit(1)

print("\nStep 2: Logging in with incorrect credentials...")
login_resp_2 = requests.post(f"{base_url}/auth/login", json={"email": "test3@test.com", "password": "wrongpass123"})
print(f"Status: {login_resp_2.status_code}")
print(f"Response: {login_resp_2.text}")

print("\nStep 3: Fetching /security/events...")
headers = {"Authorization": f"Bearer {token}"}
sec_resp = requests.get(f"{base_url}/security/events", headers=headers)
print(f"Status: {sec_resp.status_code}")
try:
    print("Response (most recent 3 events):")
    events = sec_resp.json()
    for e in events[:3]:
        print(f"- {e.get('timestamp')} | email: {e.get('email')} | success: {e.get('success')} | ip: {e.get('ipAddress')}")
except Exception as e:
    print(f"Error parsing JSON: {e}")
    print(f"Raw response: {sec_resp.text}")
