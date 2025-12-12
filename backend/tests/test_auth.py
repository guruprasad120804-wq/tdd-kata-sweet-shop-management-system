# from fastapi.testclient import TestClient
# from app.main import app

# client = TestClient(app)

# def test_register_user_success():
#     res = client.post("/api/auth/register", json={
#         "email": "testcl@example.com",
#         "password": "pass1234"
#     })
#     assert res.status_code == 201
#     body = res.json()
#     assert "id" in body
#     assert body["email"] == "test@example.com"

# def test_login_user_success():
#     # first register
#     client.post("/api/auth/register", json={
#         "email": "login@example.com",
#         "password": "pass1234"
#     })

#     # then login
#     res = client.post("/api/auth/login", json={
#         "email": "login@example.com",
#         "password": "pass1234"
#     })

#     assert res.status_code == 200
#     body = res.json()
#     assert "access_token" in body
#     assert body["token_type"] == "bearer"

from fastapi.testclient import TestClient
from app.main import app
import uuid

client = TestClient(app)


def test_register_user_success():
    email = f"{uuid.uuid4()}@example.com"

    res = client.post("/api/auth/register", json={
        "email": email,
        "password": "pass1234"
    })

    assert res.status_code == 201
    body = res.json()
    assert "id" in body
    assert body["email"] == email


def test_login_user_success():
    email = f"{uuid.uuid4()}@example.com"

    # register first
    client.post("/api/auth/register", json={
        "email": email,
        "password": "pass1234"
    })

    # then login
    res = client.post("/api/auth/login", json={
        "email": email,
        "password": "pass1234"
    })

    assert res.status_code == 200
    body = res.json()
    assert "access_token" in body
    assert body["token_type"] == "bearer"
