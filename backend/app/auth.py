from fastapi import APIRouter
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from jose import jwt
from datetime import datetime, timedelta

from app.database import SessionLocal
from app.models import User
from passlib.context import CryptContext

# ------------------------
# Router setup
# ------------------------
router = APIRouter(prefix="/api/auth", tags=["auth"])

# ------------------------
# JWT config
# ------------------------
SECRET_KEY = "super-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 1

# ------------------------
# Password hashing
# ------------------------
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ------------------------
# Pydantic schemas
# ------------------------
class RegisterRequest(BaseModel):
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


# ------------------------
# Helpers
# ------------------------
def get_db() -> Session:
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()


def create_access_token(email: str):
    expire = datetime.utcnow() + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    payload = {"sub": email, "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


# ------------------------
# Routes
# ------------------------
@router.post("/register", status_code=201)
def register_user(payload: RegisterRequest):
    db = get_db()

    # check if user already exists
    existing_user = db.query(User).filter(User.email == payload.email).first()
    if existing_user:
        return {"detail": "User already exists"}

    hashed_password = pwd_context.hash(payload.password)

    user = User(
        email=payload.email,
        password=hashed_password
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "id": user.id,
        "email": user.email
    }


@router.post("/login")
def login_user(payload: LoginRequest):
    db = get_db()

    user = db.query(User).filter(User.email == payload.email).first()

    if not user:
        return {"detail": "Invalid credentials"}

    if not pwd_context.verify(payload.password, user.password):
        return {"detail": "Invalid credentials"}

    access_token = create_access_token(user.email)

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
