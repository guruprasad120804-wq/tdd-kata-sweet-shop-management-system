"""
Database configuration and session management.

This module is responsible for:
- Creating the SQLAlchemy database engine
- Providing a session factory
- Exposing a dependency (`get_db`) for request-scoped DB sessions

This follows the Single Responsibility Principle:
all database setup and lifecycle logic lives in one place.
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# -------------------------------------------------------------------
# Database path configuration
# -------------------------------------------------------------------
# Use an absolute path to avoid accidentally creating multiple SQLite
# databases depending on where the app is launched from.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'sweetshop.db')}"

# -------------------------------------------------------------------
# SQLAlchemy engine
# -------------------------------------------------------------------
# `check_same_thread=False` is required for SQLite when used with FastAPI
# because requests may be handled in different threads.
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

# -------------------------------------------------------------------
# Session factory
# -------------------------------------------------------------------
# Each request will get its own database session.
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# -------------------------------------------------------------------
# Base class for ORM models
# -------------------------------------------------------------------
# All SQLAlchemy models should inherit from this Base.
Base = declarative_base()

# -------------------------------------------------------------------
# Dependency: get_db
# -------------------------------------------------------------------
def get_db():
    """
    FastAPI dependency that provides a database session.

    Yields:
        Session: An active SQLAlchemy session.

    The session is automatically closed after the request is finished,
    ensuring proper cleanup and preventing connection leaks.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
