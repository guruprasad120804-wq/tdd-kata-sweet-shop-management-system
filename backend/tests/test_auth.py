from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_register_user_success():
    res = client.post("/api/auth/register", json={
        "email": "test@example.com",
        "password": "pass1234"
    })
    assert res.status_code == 201
    body = res.json()
    assert "id" in body
    assert body["email"] == "test@example.com"
