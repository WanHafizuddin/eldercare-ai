from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_check_symptoms():
    print("Sending POST request to /api/symptoms/check...")
    response = client.post(
        "/api/symptoms/check",
        json={
            "symptoms": "I have been feeling very dizzy and have a mild fever.",
            "age": 75,
            "pre_existing_conditions": "Hypertension"
        }
    )
    print("Status Code:", response.status_code)
    print("Response JSON:", response.json())

if __name__ == "__main__":
    test_check_symptoms()
