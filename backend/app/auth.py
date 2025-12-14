"""
Authentication and authorization logic for the Sweet Shop API.

This module handles:
- User registration and login
- Password hashing and verification
- JWT access token creation and validation
- Role-based access control (admin vs user)
"""

from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.schemas import LoginRequest, RegisterRequest, TokenResponse

# -------------------------------------------------------------------
# Router configuration
# -------------------------------------------------------------------
router = APIRouter(prefix="/api/auth", tags=["Auth"])

# -------------------------------------------------------------------
# Security configuration
# -------------------------------------------------------------------
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

# NOTE:
# For demo and kata purposes this is acceptable.
# In production, secrets must be stored in environment variables.
SECRET_KEY = "CHANGE_ME_TO_A_LONG_RANDOM_SECRET"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 1


# -------------------------------------------------------------------
# Password utilities
# -------------------------------------------------------------------
def hash_password(password: str) -> str:
    """Hash a plaintext password."""
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against its hash."""
    return pwd_context.verify(password, hashed_password)


# -------------------------------------------------------------------
# JWT utilities
# -------------------------------------------------------------------
def create_access_token(email: str, is_admin: bool) -> str:
    """
    Create a JWT access token.

    The token contains:
    - subject (user email)
    - admin flag
    - expiration time
    """
    expire = datetime.now(timezone.utc) + timedelta(
        hours=ACCESS_TOKEN_EXPIRE_HOURS
    )
    payload = {
        "sub": email,
        "is_admin": is_admin,
        "exp": expire,
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


# -------------------------------------------------------------------
# Auth endpoints
# -------------------------------------------------------------------
@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(
    payload: RegisterRequest,
    db: Session = Depends(get_db),
):
    """
    Register a new user.

    The first user in an empty database automatically becomes an admin.
    Subsequent users are created as normal users.
    """
    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists",
        )

    is_first_user = db.query(User).count() == 0

    user = User(
        email=payload.email,
        password=hash_password(payload.password),
        is_admin=is_first_user,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "id": user.id,
        "email": user.email,
        "is_admin": user.is_admin,
    }


@router.post("/login", response_model=TokenResponse)
def login(
    payload: LoginRequest,
    db: Session = Depends(get_db),
):
    """
    Authenticate a user and return a JWT access token.
    """
    user = db.query(User).filter(User.email == payload.email).first()

    if not user or not verify_password(payload.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    token = create_access_token(user.email, user.is_admin)

    return {
        "access_token": token,
        "token_type": "bearer",
        "email": user.email,
        "is_admin": user.is_admin,
    }


# -------------------------------------------------------------------
# Authorization dependencies
# -------------------------------------------------------------------
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    """
    Retrieve the currently authenticated user from the JWT token.
    """
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str | None = payload.get("sub")
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return user


def get_current_admin(
    user: User = Depends(get_current_user),
) -> User:
    """
    Ensure the current user has admin privileges.
    """
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    return user
