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
