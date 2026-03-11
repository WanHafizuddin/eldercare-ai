from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_reminders():
    print("Testing /api/reminders/ ...")
    with TestClient(app) as client:
        # We need `with TestClient(app)` to trigger lifespan events in Starlette/FastAPI!
        response = client.post(
            "/api/reminders/",
            json={
                "user_email": "test@example.com",
                "medication_name": "Lisinopril",
                "time_to_take": "08:00"
            }
        )
        print("Status Code:", response.status_code)
        print("Response JSON:", response.json())
        
        get_response = client.get("/api/reminders/")
        print("GET Status Code:", get_response.status_code)
        print("All Reminders:", get_response.json())

if __name__ == "__main__":
    test_reminders()
