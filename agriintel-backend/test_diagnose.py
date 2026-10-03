import requests
import sys
import json

# 1. Login
login_url = "http://127.0.0.1:8000/auth/login"
login_data = {
    "email": "test3@test.com",
    "password": "testpass123"
}
try:
    login_res = requests.post(login_url, json=login_data)
    if login_res.status_code != 200:
        print(f"Login failed: Status Code {login_res.status_code}")
        print(login_res.text)
        sys.exit(1)
    
    token = login_res.json()["access_token"]
except Exception as e:
    print(f"Error during login: {e}")
    sys.exit(1)

# 2. Upload Image
upload_url = "http://127.0.0.1:8000/recommendations/diagnose"
headers = {
    "Authorization": f"Bearer {token}"
}
file_path = r"C:\Users\athar\Downloads\plant-disease-2-1.jpg"

try:
    with open(file_path, "rb") as f:
        files = {"image": ("plant-disease-2-1.jpg", f, "image/jpeg")}
        upload_res = requests.post(upload_url, headers=headers, files=files)

    print(f"Status Code: {upload_res.status_code}")
    print("Response Body:")
    try:
        # Try to pretty print json
        parsed = upload_res.json()
        print(json.dumps(parsed, indent=2))
    except ValueError:
        print(upload_res.text)
except Exception as e:
    print(f"Error during upload: {e}")
