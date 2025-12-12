# from fastapi import APIRouter
# from pydantic import BaseModel, EmailStr

# router = APIRouter(prefix="/api/auth", tags=["auth"])

# class RegisterRequest(BaseModel):
#     email: EmailStr
#     password: str

# _fake_users = []
# _next_id = 1

# @router.post("/register", status_code=201)
# def register_user(payload: RegisterRequest):
#     global _next_id
#     user = {
#         "id": _next_id,
#         "email": payload.email
#     }
#     _next_id += 1
#     _fake_users.append({
#         "id": user["id"],
#         "email": payload.email,
#         "password": payload.password
#     })
#     return user


from fastapi import APIRouter
from pydantic import BaseModel, EmailStr
from jose import jwt
from datetime import datetime, timedelta

router = APIRouter(prefix="/api/auth", tags=["auth"])

SECRET_KEY = "super-secret-key"
ALGORITHM = "HS256"

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
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


@router.post("/login")
def login_user(payload: LoginRequest):
    for user in _fake_users:
        if user["email"] == payload.email and user["password"] == payload.password:
            token = jwt.encode(
                {
                    "sub": user["email"],
                    "exp": datetime.utcnow() + timedelta(hours=1)
                },
                SECRET_KEY,
                algorithm=ALGORITHM
            )
            return {
                "access_token": token,
                "token_type": "bearer"
            }

    return {"detail": "Invalid credentials"}
