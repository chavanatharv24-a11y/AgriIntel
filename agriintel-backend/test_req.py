import urllib.request
import urllib.error
import json

def make_request(url, method="GET", data=None, headers=None):
    if headers is None:
        headers = {}
    
    if data is not None:
        data = json.dumps(data).encode('utf-8')
        headers['Content-Type'] = 'application/json'
        
    req = urllib.request.Request(url, data=data, method=method, headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            status = response.status
            body = response.read().decode('utf-8')
            return status, body
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8')
        return e.code, body
    except Exception as e:
        return 0, str(e)

print("--- LOGIN ---")
status, body = make_request(
    "http://127.0.0.1:8000/auth/login",
    method="POST",
    data={"email": "test3@test.com", "password": "testpass123"}
)
print(f"Status Code: {status}")
print(f"Response Body: {body}")
print()

if status == 200:
    token = json.loads(body).get("access_token")
    print("--- RECOMMENDATIONS GENERATE ---")
    status2, body2 = make_request(
        "http://127.0.0.1:8000/recommendations/generate",
        method="POST",
        headers={"Authorization": f"Bearer {token}"}
    )
    print(f"Status Code: {status2}")
    print(f"Response Body: {body2}")
else:
    print("Login failed, skipping recommendations request.")
