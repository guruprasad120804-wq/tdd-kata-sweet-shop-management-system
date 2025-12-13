from pydantic import BaseModel, EmailStr, Field
from typing import Optional


# ---------- AUTH ----------
class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=4)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    email: EmailStr
    is_admin: bool


# ---------- SWEETS ----------
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
    amount: int = Field(gt=0)


class PurchaseRequest(BaseModel):
    amount: Optional[int] = Field(default=1, gt=0)
