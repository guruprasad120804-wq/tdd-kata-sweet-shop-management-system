from fastapi.testclient import TestClient
from app.main import app
import uuid

client = TestClient(app)


def test_add_sweet_success():
    res = client.post("/api/sweets", json={
        "name": "Ladoo",
        "category": "Indian",
        "price": 10.5,
        "quantity": 50
    })

    assert res.status_code == 201
    body = res.json()
    assert "id" in body
    assert body["name"] == "Ladoo"


def test_list_sweets():
    res = client.get("/api/sweets")

    assert res.status_code == 200
    assert isinstance(res.json(), list)
