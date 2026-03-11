from fastapi.testclient import TestClient
from app.main import app
import json

client = TestClient(app)

def test_vitals():
    print("Testing /api/vitals/log...")
    try:
        response = client.post(
            "/api/vitals/log",
            json={
                "user_id": "test_user_123",
                "blood_pressure_systolic": 120,
                "blood_pressure_diastolic": 80,
                "heart_rate": 72,
                "glucose_level": 95.5
            }
        )
        print("Status Code:", response.status_code)
        print("Response JSON:", response.json())
    except Exception as e:
        print("Exception caught:", str(e))

if __name__ == "__main__":
    test_vitals()
