from fastapi import APIRouter
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import Sweet

from typing import Optional
from sqlalchemy import and_


router = APIRouter(prefix="/api/sweets", tags=["sweets"])


class SweetCreate(BaseModel):
    name: str
    category: str
    price: float
    quantity: int

class SweetUpdate(BaseModel):
    name: str
    category: str
    price: float
    quantity: int
    
class RestockRequest(BaseModel):
    amount: int



def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()


@router.post("", status_code=201)
def add_sweet(payload: SweetCreate):
    db = get_db()

    sweet = Sweet(
        name=payload.name,
        category=payload.category,
        price=payload.price,
        quantity=payload.quantity
    )

    db.add(sweet)
    db.commit()
    db.refresh(sweet)

    return {
        "id": sweet.id,
        "name": sweet.name,
        "category": sweet.category,
        "price": sweet.price,
        "quantity": sweet.quantity
    }


@router.get("")
def list_sweets():
    db = get_db()
    sweets = db.query(Sweet).all()

    return [
        {
            "id": s.id,
            "name": s.name,
            "category": s.category,
            "price": s.price,
            "quantity": s.quantity
        }
        for s in sweets
    ]


@router.get("/search")
def search_sweets(
    name: Optional[str] = None,
    category: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None
):
    db = get_db()

    query = db.query(Sweet)

    if name:
        query = query.filter(Sweet.name.ilike(f"%{name}%"))

    if category:
        query = query.filter(Sweet.category == category)

    if min_price is not None:
        query = query.filter(Sweet.price >= min_price)

    if max_price is not None:
        query = query.filter(Sweet.price <= max_price)

    sweets = query.all()

    return [
        {
            "id": s.id,
            "name": s.name,
            "category": s.category,
            "price": s.price,
            "quantity": s.quantity
        }
        for s in sweets
    ]


@router.put("/{sweet_id}")
def update_sweet(sweet_id: int, payload: SweetUpdate):
    db = get_db()

    sweet = db.query(Sweet).filter(Sweet.id == sweet_id).first()

    if not sweet:
        return {"detail": "Sweet not found"}

    sweet.name = payload.name
    sweet.category = payload.category
    sweet.price = payload.price
    sweet.quantity = payload.quantity

    db.commit()
    db.refresh(sweet)

    return {
        "id": sweet.id,
        "name": sweet.name,
        "category": sweet.category,
        "price": sweet.price,
        "quantity": sweet.quantity
    }

@router.delete("/{sweet_id}")
def delete_sweet(sweet_id: int):
    db = get_db()

    sweet = db.query(Sweet).filter(Sweet.id == sweet_id).first()

    if not sweet:
        return {"detail": "Sweet not found"}

    db.delete(sweet)
    db.commit()

    return {"detail": "Sweet deleted"}


@router.post("/{sweet_id}/purchase")
def purchase_sweet(sweet_id: int):
    db = get_db()

    sweet = db.query(Sweet).filter(Sweet.id == sweet_id).first()

    if not sweet:
        return {"detail": "Sweet not found"}

    if sweet.quantity <= 0:
        return {"detail": "Out of stock"}

    sweet.quantity -= 1
    db.commit()
    db.refresh(sweet)

    return {
        "id": sweet.id,
        "quantity": sweet.quantity
    }

@router.post("/{sweet_id}/restock")
def restock_sweet(sweet_id: int, payload: RestockRequest):
    db = get_db()

    sweet = db.query(Sweet).filter(Sweet.id == sweet_id).first()

    if not sweet:
        return {"detail": "Sweet not found"}

    if payload.amount <= 0:
        return {"detail": "Invalid restock amount"}

    sweet.quantity += payload.amount
    db.commit()
    db.refresh(sweet)

    return {
        "id": sweet.id,
        "quantity": sweet.quantity
    }
