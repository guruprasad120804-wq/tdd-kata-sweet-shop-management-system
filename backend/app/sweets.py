from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Sweet
from app.schemas import SweetCreate, SweetUpdate, RestockRequest, PurchaseRequest
from app.auth import get_current_user, get_current_admin

router = APIRouter(prefix="/api/sweets", tags=["Sweets"])


# Protected: Add sweet (any logged-in user or admin — you can switch to admin-only if needed)
@router.post("", status_code=201)
def add_sweet(
    payload: SweetCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    sweet = Sweet(
        name=payload.name,
        category=payload.category,
        price=payload.price,
        quantity=payload.quantity,
    )
    db.add(sweet)
    db.commit()
    db.refresh(sweet)
    return sweet


# Protected: list sweets
@router.get("")
def list_sweets(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return db.query(Sweet).all()


# Protected: search by name/category/min_price/max_price
@router.get("/search")
def search_sweets(
    name: str | None = None,
    category: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    q = db.query(Sweet)

    if name:
        q = q.filter(Sweet.name.ilike(f"%{name}%"))
    if category:
        q = q.filter(Sweet.category.ilike(f"%{category}%"))
    if min_price is not None:
        q = q.filter(Sweet.price >= min_price)
    if max_price is not None:
        q = q.filter(Sweet.price <= max_price)

    return q.all()


# Protected: update sweet
@router.put("/{sweet_id}")
def update_sweet(
    sweet_id: int,
    payload: SweetUpdate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    sweet = db.query(Sweet).filter(Sweet.id == sweet_id).first()
    if not sweet:
        raise HTTPException(status_code=404, detail="Sweet not found")

    sweet.name = payload.name
    sweet.category = payload.category
    sweet.price = payload.price
    sweet.quantity = payload.quantity

    db.commit()
    db.refresh(sweet)
    return sweet


# Protected: delete sweet (ADMIN ONLY)
@router.delete("/{sweet_id}")
def delete_sweet(
    sweet_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    sweet = db.query(Sweet).filter(Sweet.id == sweet_id).first()
    if not sweet:
        raise HTTPException(status_code=404, detail="Sweet not found")

    db.delete(sweet)
    db.commit()
    return {"detail": "Sweet deleted"}


# Protected: purchase (decrease quantity) - any logged in user
@router.post("/{sweet_id}/purchase")
def purchase_sweet(
    sweet_id: int,
    payload: PurchaseRequest = PurchaseRequest(),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    sweet = db.query(Sweet).filter(Sweet.id == sweet_id).first()
    if not sweet:
        raise HTTPException(status_code=404, detail="Sweet not found")

    amount = payload.amount or 1
    if sweet.quantity < amount:
        raise HTTPException(status_code=400, detail="Not enough stock")

    sweet.quantity -= amount
    db.commit()
    db.refresh(sweet)
    return {"id": sweet.id, "quantity": sweet.quantity}


# Protected: restock (increase quantity) - ADMIN ONLY
@router.post("/{sweet_id}/restock")
def restock_sweet(
    sweet_id: int,
    payload: RestockRequest,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    sweet = db.query(Sweet).filter(Sweet.id == sweet_id).first()
    if not sweet:
        raise HTTPException(status_code=404, detail="Sweet not found")

    sweet.quantity += payload.amount
    db.commit()
    db.refresh(sweet)
    return {"id": sweet.id, "quantity": sweet.quantity}
