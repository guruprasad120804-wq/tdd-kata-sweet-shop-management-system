# from fastapi.testclient import TestClient
# from app.main import app
# from app.database import SessionLocal
# from app.models import User

# client = TestClient(app)

# def get_admin_headers():
#     email = f"admin_{uuid.uuid4()}@example.com"
#     password = "admin123"

#     client.post("/api/auth/register", json={
#         "email": email,
#         "password": password
#     })

#     db = SessionLocal()
#     user = db.query(User).filter(User.email == email).first()  
#     user.is_admin = True
#     db.commit()
#     db.close()

#     res = client.post("/api/auth/login", json={
#         "email": email,
#         "password": password
#     })

#     token = res.json()["access_token"]
#     return {"Authorization": f"Bearer {token}"}


# def test_add_sweet_success():
#     res = client.post("/api/sweets", json={
#         "name": "Ladoo",
#         "category": "Indian",
#         "price": 10.5,
#         "quantity": 50
#     })

#     assert res.status_code == 201
#     body = res.json()
#     assert "id" in body
#     assert body["name"] == "Ladoo"

# def test_list_sweets():
#     res = client.get("/api/sweets")

#     assert res.status_code == 200
#     assert isinstance(res.json(), list)


# def test_search_sweets_by_name():
#     # add a sweet
#     client.post("/api/sweets", json={
#         "name": "Jalebi",
#         "category": "Indian",
#         "price": 15.0,
#         "quantity": 30
#     })

#     # search by name
#     res = client.get("/api/sweets/search?name=Jale")

#     assert res.status_code == 200
#     data = res.json()
#     assert len(data) >= 1
#     assert data[0]["name"] == "Jalebi"


# def test_update_sweet_success():
#     # create sweet
#     create_res = client.post("/api/sweets", json={
#         "name": "Barfi",
#         "category": "Indian",
#         "price": 20.0,
#         "quantity": 40
#     })

#     sweet_id = create_res.json()["id"]

#     # update sweet
#     update_res = client.put(f"/api/sweets/{sweet_id}", json={
#         "name": "Kaju Barfi",
#         "category": "Indian",
#         "price": 25.0,
#         "quantity": 35
#     })

#     assert update_res.status_code == 200
#     body = update_res.json()
#     assert body["name"] == "Kaju Barfi"
#     assert body["price"] == 25.0
#     assert body["quantity"] == 35


# def test_delete_sweet_success():
#     # create sweet
#     create_res = client.post("/api/sweets", json={
#         "name": "Rasgulla",
#         "category": "Indian",
#         "price": 12.0,
#         "quantity": 20
#     })

#     sweet_id = create_res.json()["id"]

#     # delete sweet
#     delete_res = client.delete(f"/api/sweets/{sweet_id}")

#     assert delete_res.status_code == 200
#     assert delete_res.json()["detail"] == "Sweet deleted"

#     # verify sweet is gone
#     list_res = client.get("/api/sweets")
#     sweets = list_res.json()
#     assert all(s["id"] != sweet_id for s in sweets)


# def test_purchase_sweet_success():
#     # create sweet
#     res = client.post("/api/sweets", json={
#         "name": "Peda",
#         "category": "Indian",
#         "price": 8.0,
#         "quantity": 5
#     })
#     sweet_id = res.json()["id"]

#     # purchase sweet
#     purchase_res = client.post(f"/api/sweets/{sweet_id}/purchase")

#     assert purchase_res.status_code == 200
#     body = purchase_res.json()
#     assert body["quantity"] == 4


# def test_restock_sweet_success():
#     # create sweet
#     res = client.post("/api/sweets", json={
#         "name": "Halwa",
#         "category": "Indian",
#         "price": 10.0,
#         "quantity": 3
#     })
#     sweet_id = res.json()["id"]

#     # restock sweet
#     restock_res = client.post(
#         f"/api/sweets/{sweet_id}/restock",
#         json={"amount": 5}
#     )

#     assert restock_res.status_code == 200
#     body = restock_res.json()
#     assert body["quantity"] == 8


# # #0----------------------
# from fastapi.testclient import TestClient
# from app.main import app

# client = TestClient(app)


# def get_token():
#     email = "admin2@example.com"
#     password = "admin123"

#     client.post("/api/auth/register", json={
#         "email": email,
#         "password": password
#     })

#     # make admin manually
#     from app.database import SessionLocal
#     from app.models import User

#     db = SessionLocal()
#     user = db.query(User).filter(User.email == email).first()
#     user.is_admin = True
#     db.commit()
#     db.close()

#     res = client.post("/api/auth/login", json={
#         "email": email,
#         "password": password
#     })
#     return res.json()["access_token"]


# def test_add_and_list_sweets():
#     token = get_token()

#     headers = {"Authorization": f"Bearer {token}"}

#     # Add sweet
#     res = client.post("/api/sweets", json={
#         "name": "Ladoo",
#         "category": "Indian",
#         "price": 10,
#         "quantity": 5
#     }, headers=headers)

#     assert res.status_code == 201

#     # List sweets
#     res = client.get("/api/sweets", headers=headers)
#     assert res.status_code == 200
#     assert len(res.json()) >= 1

import uuid
from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models import User

client = TestClient(app)

# ---------------------------
# Helper: get admin auth header
# ---------------------------
def get_admin_headers():
    email = f"admin_{uuid.uuid4()}@example.com"
    password = "admin123"

    # register user
    client.post("/api/auth/register", json={
        "email": email,
        "password": password
    })

    # promote to admin
    db = SessionLocal()
    user = db.query(User).filter(User.email == email).first()
    user.is_admin = True
    db.commit()
    db.close()

    # login
    res = client.post("/api/auth/login", json={
        "email": email,
        "password": password
    })

    token = res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


# ---------------------------
# SWEETS TESTS
# ---------------------------

def test_add_sweet_success():
    headers = get_admin_headers()

    res = client.post(
        "/api/sweets",
        json={
            "name": "Ladoo",
            "category": "Indian",
            "price": 10.5,
            "quantity": 50
        },
        headers=headers
    )

    assert res.status_code == 201
    body = res.json()
    assert "id" in body
    assert body["name"] == "Ladoo"


def test_list_sweets():
    headers = get_admin_headers()

    res = client.get("/api/sweets", headers=headers)

    assert res.status_code == 200
    assert isinstance(res.json(), list)


def test_search_sweets_by_name():
    headers = get_admin_headers()

    # create sweet
    client.post(
        "/api/sweets",
        json={
            "name": "Jalebi",
            "category": "Indian",
            "price": 15.0,
            "quantity": 30
        },
        headers=headers
    )

    # search
    res = client.get(
        "/api/sweets/search?name=Jale",
        headers=headers
    )

    assert res.status_code == 200
    data = res.json()
    assert len(data) >= 1
    assert any(s["name"] == "Jalebi" for s in data)


def test_update_sweet_success():
    headers = get_admin_headers()

    create_res = client.post(
        "/api/sweets",
        json={
            "name": "Barfi",
            "category": "Indian",
            "price": 20.0,
            "quantity": 40
        },
        headers=headers
    )

    sweet_id = create_res.json()["id"]

    update_res = client.put(
        f"/api/sweets/{sweet_id}",
        json={
            "name": "Kaju Barfi",
            "category": "Indian",
            "price": 25.0,
            "quantity": 35
        },
        headers=headers
    )

    assert update_res.status_code == 200
    body = update_res.json()
    assert body["name"] == "Kaju Barfi"
    assert body["price"] == 25.0
    assert body["quantity"] == 35


def test_delete_sweet_success():
    headers = get_admin_headers()

    create_res = client.post(
        "/api/sweets",
        json={
            "name": "Rasgulla",
            "category": "Indian",
            "price": 12.0,
            "quantity": 20
        },
        headers=headers
    )

    sweet_id = create_res.json()["id"]

    delete_res = client.delete(
        f"/api/sweets/{sweet_id}",
        headers=headers
    )

    assert delete_res.status_code == 200
    assert delete_res.json()["detail"] == "Sweet deleted"

    # verify deletion
    list_res = client.get("/api/sweets", headers=headers)
    sweets = list_res.json()
    assert all(s["id"] != sweet_id for s in sweets)


def test_purchase_sweet_success():
    headers = get_admin_headers()

    res = client.post(
        "/api/sweets",
        json={
            "name": "Peda",
            "category": "Indian",
            "price": 8.0,
            "quantity": 5
        },
        headers=headers
    )

    sweet_id = res.json()["id"]

    purchase_res = client.post(
        f"/api/sweets/{sweet_id}/purchase",
        headers=headers
    )

    assert purchase_res.status_code == 200
    body = purchase_res.json()
    assert body["quantity"] == 4


def test_restock_sweet_success():
    headers = get_admin_headers()

    res = client.post(
        "/api/sweets",
        json={
            "name": "Halwa",
            "category": "Indian",
            "price": 10.0,
            "quantity": 3
        },
        headers=headers
    )

    sweet_id = res.json()["id"]

    restock_res = client.post(
        f"/api/sweets/{sweet_id}/restock",
        json={"amount": 5},
        headers=headers
    )

    assert restock_res.status_code == 200
    body = restock_res.json()
    assert body["quantity"] == 8
