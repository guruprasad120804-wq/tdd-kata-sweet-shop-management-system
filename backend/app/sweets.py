"""
Sweet management endpoints for the Sweet Shop API.

This module contains all CRUD and inventory-related operations
for sweets, including:
- create
- list
- search
- update
- delete
- purchase
- restock

Access control:
- All endpoints require authentication
- Some endpoints require admin privileges
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth import get_current_admin, get_current_user
from app.database import get_db
from app.models import Sweet
from app.schemas import (
    PurchaseRequest,
    RestockRequest,
    SweetCreate,
    SweetUpdate,
)

router = APIRouter(prefix="/api/sweets", tags=["Sweets"])


# -------------------------------------------------------------------
# Helper utilities
# -------------------------------------------------------------------
def get_sweet_or_404(db: Session, sweet_id: int) -> Sweet:
    """
    Retrieve a sweet by ID or raise a 404 error.
    """
    sweet = db.query(Sweet).filter(Sweet.id == sweet_id).first()
    if not sweet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sweet not found",
        )
    return sweet


# -------------------------------------------------------------------
# Create
# -------------------------------------------------------------------
@router.post("", status_code=status.HTTP_201_CREATED)
def add_sweet(
    payload: SweetCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    """
    Create a new sweet item.

    Any authenticated user can create a sweet.
    (This can be restricted to admins if needed.)
    """
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


# -------------------------------------------------------------------
# Read
# -------------------------------------------------------------------
@router.get("")
def list_sweets(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    """
    Retrieve a list of all available sweets.
    """
    return db.query(Sweet).all()


@router.get("/search")
def search_sweets(
    name: str | None = None,
    category: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    """
    Search sweets by optional filters:
    - name
    - category
    - minimum price
    - maximum price
    """
    query = db.query(Sweet)

    if name:
        query = query.filter(Sweet.name.ilike(f"%{name}%"))
    if category:
        query = query.filter(Sweet.category.ilike(f"%{category}%"))
    if min_price is not None:
        query = query.filter(Sweet.price >= min_price)
    if max_price is not None:
        query = query.filter(Sweet.price <= max_price)

    return query.all()


# -------------------------------------------------------------------
# Update
# -------------------------------------------------------------------
@router.put("/{sweet_id}")
def update_sweet(
    sweet_id: int,
    payload: SweetUpdate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    """
    Update an existing sweet's details.
    """
    sweet = get_sweet_or_404(db, sweet_id)

    sweet.name = payload.name
    sweet.category = payload.category
    sweet.price = payload.price
    sweet.quantity = payload.quantity

    db.commit()
    db.refresh(sweet)

    return sweet


# -------------------------------------------------------------------
# Delete (Admin only)
# -------------------------------------------------------------------
@router.delete("/{sweet_id}")
def delete_sweet(
    sweet_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    """
    Delete a sweet item (admin only).
    """
    sweet = get_sweet_or_404(db, sweet_id)

    db.delete(sweet)
    db.commit()

    return {"detail": "Sweet deleted successfully"}


# -------------------------------------------------------------------
# Inventory operations
# -------------------------------------------------------------------
@router.post("/{sweet_id}/purchase")
def purchase_sweet(
    sweet_id: int,
    payload: PurchaseRequest = PurchaseRequest(),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    """
    Purchase a sweet, decreasing its stock quantity.
    """
    sweet = get_sweet_or_404(db, sweet_id)

    amount = payload.amount or 1
    if sweet.quantity < amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Not enough stock",
        )

    sweet.quantity -= amount
    db.commit()
    db.refresh(sweet)

    return {"id": sweet.id, "quantity": sweet.quantity}


@router.post("/{sweet_id}/restock")
def restock_sweet(
    sweet_id: int,
    payload: RestockRequest,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    """
    Restock a sweet, increasing its stock quantity (admin only).
    """
    sweet = get_sweet_or_404(db, sweet_id)

    sweet.quantity += payload.amount
    db.commit()
    db.refresh(sweet)

    return {"id": sweet.id, "quantity": sweet.quantity}
