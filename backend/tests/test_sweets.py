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


def test_search_sweets_by_name():
    # add a sweet
    client.post("/api/sweets", json={
        "name": "Jalebi",
        "category": "Indian",
        "price": 15.0,
        "quantity": 30
    })

    # search by name
    res = client.get("/api/sweets/search?name=Jale")

    assert res.status_code == 200
    data = res.json()
    assert len(data) >= 1
    assert data[0]["name"] == "Jalebi"


def test_update_sweet_success():
    # create sweet
    create_res = client.post("/api/sweets", json={
        "name": "Barfi",
        "category": "Indian",
        "price": 20.0,
        "quantity": 40
    })

    sweet_id = create_res.json()["id"]

    # update sweet
    update_res = client.put(f"/api/sweets/{sweet_id}", json={
        "name": "Kaju Barfi",
        "category": "Indian",
        "price": 25.0,
        "quantity": 35
    })

    assert update_res.status_code == 200
    body = update_res.json()
    assert body["name"] == "Kaju Barfi"
    assert body["price"] == 25.0
    assert body["quantity"] == 35
