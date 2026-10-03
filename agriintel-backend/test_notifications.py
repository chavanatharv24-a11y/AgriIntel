import requests
import sys
import json
import time

# Give the server a moment to start
time.sleep(2)

base_url = "http://127.0.0.1:8000"

# 1. Login
login_data = {
    "email": "test3@test.com",
    "password": "testpass123"
}
try:
    login_res = requests.post(f"{base_url}/auth/login", json=login_data)
    if login_res.status_code != 200:
        print(f"Login failed: Status {login_res.status_code}\n{login_res.text}")
        sys.exit(1)
    token = login_res.json()["access_token"]
except Exception as e:
    print(f"Login error: {e}")
    sys.exit(1)

headers = {"Authorization": f"Bearer {token}"}

# 2. POST /notifications
print("=== POST /notifications ===")
post_data = {"message": "Soil moisture critically low"}
post_res = requests.post(f"{base_url}/notifications", headers=headers, json=post_data)
print(f"Status: {post_res.status_code}")
try:
    post_json = post_res.json()
    print(json.dumps(post_json, indent=2))
    notif_id = post_json.get("id")
except:
    print(post_res.text)
    sys.exit(1)
print("\n")

if not notif_id:
    print("Failed to get ID from POST")
    sys.exit(1)

# 3. GET /notifications
print("=== GET /notifications ===")
get_res = requests.get(f"{base_url}/notifications", headers=headers)
print(f"Status: {get_res.status_code}")
try:
    print(json.dumps(get_res.json(), indent=2))
except:
    print(get_res.text)
print("\n")

# 4. PATCH /notifications/{id}/read
print("=== PATCH /notifications/{id}/read ===")
patch_res = requests.patch(f"{base_url}/notifications/{notif_id}/read", headers=headers)
print(f"Status: {patch_res.status_code}")
try:
    print(json.dumps(patch_res.json(), indent=2))
except:
    print(patch_res.text)
print("\n")

