from fastapi import APIRouter
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import Sweet

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
