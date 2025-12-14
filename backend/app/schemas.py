"""
Pydantic schemas (request/response models) for the Sweet Shop API.

These schemas define:
- What the API expects from clients (request bodies)
- What the API returns to clients (response bodies)

They help validate input, document endpoints in Swagger, and keep
business logic and persistence models separate.
"""

from typing import Optional

from pydantic import BaseModel, EmailStr, Field


# -------------------------------------------------------------------
# Auth schemas
# -------------------------------------------------------------------
class RegisterRequest(BaseModel):
    """Request body for registering a new user."""
    email: EmailStr
    password: str = Field(min_length=4, description="Minimum 4 characters")


class LoginRequest(BaseModel):
    """Request body for logging in an existing user."""
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """Response body returned after a successful login."""
    access_token: str
    token_type: str = "bearer"
    email: EmailStr
    is_admin: bool


# -------------------------------------------------------------------
# Sweet schemas
# -------------------------------------------------------------------
class SweetCreate(BaseModel):
    """Request body for creating a new sweet item."""
    name: str = Field(min_length=1)
    category: str = Field(min_length=1)
    price: float = Field(gt=0, description="Price must be greater than 0")
    quantity: int = Field(ge=0, description="Quantity cannot be negative")


class SweetUpdate(BaseModel):
    """Request body for updating an existing sweet item."""
    name: str = Field(min_length=1)
    category: str = Field(min_length=1)
    price: float = Field(gt=0, description="Price must be greater than 0")
    quantity: int = Field(ge=0, description="Quantity cannot be negative")


class RestockRequest(BaseModel):
    """Request body for restocking an existing sweet item."""
    amount: int = Field(gt=0, description="Amount must be greater than 0")


class PurchaseRequest(BaseModel):
    """
    Request body for purchasing a sweet item.

    If omitted, the API defaults to purchasing 1 unit.
    """
    amount: Optional[int] = Field(default=1, gt=0, description="Units to purchase")
