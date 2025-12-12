from fastapi import APIRouter
from pydantic import BaseModel, EmailStr

router = APIRouter(prefix="/api/auth", tags=["auth"])

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str

_fake_users = []
_next_id = 1

@router.post("/register", status_code=201)
def register_user(payload: RegisterRequest):
    global _next_id
    user = {
        "id": _next_id,
        "email": payload.email
    }
    _next_id += 1
    _fake_users.append({
        "id": user["id"],
        "email": payload.email,
        "password": payload.password
    })
    return user
