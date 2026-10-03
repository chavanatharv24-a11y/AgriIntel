# Note: The FastAPI server must already be running on http://127.0.0.1:8000 for these tests to pass.
import pytest
import requests

BASE_URL = "http://127.0.0.1:8000"

@pytest.fixture(scope="module")
def auth_token():
    resp = requests.post(f"{BASE_URL}/auth/login", json={"email": "test3@test.com", "password": "testpass123"})
    assert resp.status_code == 200, f"Failed to get initial auth token: {resp.text}"
    return resp.json()["access_token"]

@pytest.fixture(scope="module")
def headers(auth_token):
    return {"Authorization": f"Bearer {auth_token}"}

def test_signup_duplicate_email_rejected():
    payload = {
        "name": "Test User",
        "age": 30,
        "email": "test3@test.com",
        "password": "testpass123"
    }
    resp = requests.post(f"{BASE_URL}/auth/signup", json=payload)
    assert resp.status_code == 400

def test_login_wrong_password_rejected():
    resp = requests.post(f"{BASE_URL}/auth/login", json={"email": "test3@test.com", "password": "wrongpass123"})
    assert resp.status_code == 401

def test_login_correct_credentials():
    resp = requests.post(f"{BASE_URL}/auth/login", json={"email": "test3@test.com", "password": "testpass123"})
    assert resp.status_code == 200
    assert "access_token" in resp.json()

def test_sensor_reading_requires_auth():
    resp = requests.get(f"{BASE_URL}/sensor/readings")
    assert resp.status_code == 401

def test_sensor_reading_create_and_fetch(headers):
    payload = {
        "deviceId": "pytest-sensor",
        "soilMoisture": 50,
        "temperature": 25,
        "humidity": 60,
        "rainDetected": False
    }
    post_resp = requests.post(f"{BASE_URL}/sensor/readings", json=payload, headers=headers)
    assert post_resp.status_code in (200, 201)
    
    get_resp = requests.get(f"{BASE_URL}/sensor/readings", headers=headers)
    assert get_resp.status_code == 200
    readings = get_resp.json()
    assert len(readings) > 0
    assert readings[0]["deviceId"] == "pytest-sensor"

def test_yield_prediction_returns_valid_range(headers):
    resp = requests.get(f"{BASE_URL}/predict/yield", headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert "predictedYieldKgPerAcre" in data
    val = data["predictedYieldKgPerAcre"]
    assert 0 <= val <= 50000

def test_anomaly_check_returns_valid_status(headers):
    resp = requests.get(f"{BASE_URL}/predict/anomaly-check", headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] in ("Normal", "Anomalous")

def test_finance_calculation_math_consistent(headers):
    payload = {
        "seedCost": 1000,
        "fertilizerCost": 500,
        "laborCost": 200,
        "otherCosts": 100,
        "sellingPricePerKg": 10
    }
    resp = requests.post(f"{BASE_URL}/finance/calculate", json=payload, headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    
    expected_cost = sum(payload[k] for k in ["seedCost", "fertilizerCost", "laborCost", "otherCosts"])
    expected_revenue = data["totalYieldKg"] * payload["sellingPricePerKg"]
    
    # Allow small float differences
    assert abs(data["totalCost"] - expected_cost) < 0.01
    assert abs(data["revenue"] - expected_revenue) < 0.01
    assert abs(data["profit"] - (data["revenue"] - data["totalCost"])) < 0.01

def test_notification_create_and_mark_read(headers):
    payload = {
        "title": "Pytest Title",
        "message": "Pytest message",
        "type": "alert"
    }
    post_resp = requests.post(f"{BASE_URL}/notifications/", json=payload, headers=headers)
    assert post_resp.status_code in (200, 201)
    # The endpoint might return {"id": ...} or {"_id": ...} or the whole object.
    notif = post_resp.json()
    notif_id = notif.get("id") or notif.get("_id")
    
    # Mark read
    patch_resp = requests.patch(f"{BASE_URL}/notifications/{notif_id}/read", headers=headers)
    assert patch_resp.status_code == 200
    
    # Verify it is read
    get_resp = requests.get(f"{BASE_URL}/notifications/", headers=headers)
    assert get_resp.status_code == 200
    notifs = get_resp.json()
    target = next((n for n in notifs if n.get("id") == notif_id or n.get("_id") == notif_id), None)
    assert target is not None
    assert target["isRead"] is True
