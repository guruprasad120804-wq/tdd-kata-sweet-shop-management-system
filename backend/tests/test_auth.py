from fastapi.testclient import TestClient
from app.main import app
import uuid

client = TestClient(app)


def test_register_and_login():
    email = f"test_{uuid.uuid4().hex}@example.com"
    password = "test1234"

    # Register
    res = client.post("/api/auth/register", json={
        "email": email,
        "password": password
    })
    assert res.status_code == 201

    # Login
    res = client.post("/api/auth/login", json={
        "email": email,
        "password": password
    })
    assert res.status_code == 200

    data = res.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
