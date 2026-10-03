import urllib.request
import urllib.error
import json

signup_data = {
    "name": "Test Farmer",
    "age": 30,
    "email": "test@test.com",
    "password": "testpass123",
    "cropType": "Wheat",
    "landSize": 5.5
}
login_data = {
    "email": "test@test.com",
    "password": "testpass123"
}

print("--- POST /auth/signup ---")
try:
    req = urllib.request.Request("http://127.0.0.1:8000/auth/signup", data=json.dumps(signup_data).encode(), headers={'Content-Type': 'application/json'}, method='POST')
    with urllib.request.urlopen(req, timeout=10) as response:
        print(f"Status Code: {response.status}")
        print(f"Body: {response.read().decode()}")
except urllib.error.HTTPError as e:
    print(f"Status Code: {e.code}")
    print(f"Body: {e.read().decode()}")
except Exception as e:
    print(f"Error: {e}")

print("\n--- POST /auth/login ---")
try:
    req2 = urllib.request.Request("http://127.0.0.1:8000/auth/login", data=json.dumps(login_data).encode(), headers={'Content-Type': 'application/json'}, method='POST')
    with urllib.request.urlopen(req2, timeout=10) as response:
        print(f"Status Code: {response.status}")
        print(f"Body: {response.read().decode()}")
except urllib.error.HTTPError as e:
    print(f"Status Code: {e.code}")
    print(f"Body: {e.read().decode()}")
except Exception as e:
    print(f"Error: {e}")
