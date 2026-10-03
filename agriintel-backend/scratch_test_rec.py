import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def main():
    print("Logging in...")
    login_response = requests.post(f"{BASE_URL}/auth/login", json={
        "email": "test3@test.com",
        "password": "testpass123"
    })
    
    if login_response.status_code != 200:
        print(f"Login failed! Status: {login_response.status_code}")
        print(login_response.text)
        return
        
    token = login_response.json().get("access_token")
    if not token:
        print("No access token in response.")
        return
        
    print("Login successful! Got token.")
    
    print("Requesting recommendations...")
    rec_response = requests.post(f"{BASE_URL}/recommendations/generate", headers={
        "Authorization": f"Bearer {token}"
    })
    
    print(f"Status Code: {rec_response.status_code}")
    print("Response Body:")
    try:
        print(json.dumps(rec_response.json(), indent=2))
    except Exception:
        print(rec_response.text)

if __name__ == "__main__":
    main()
