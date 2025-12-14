"""
Database models for the Sweet Shop Management System.

This module defines the core domain entities that are persisted
in the database using SQLAlchemy ORM.
"""

from sqlalchemy import Column, Integer, String, Float, Boolean
from app.database import Base


class User(Base):
    """
    Represents an application user.

    Users can authenticate into the system and may optionally
    have administrative privileges.
    """

    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    email = Column(
        String,
        unique=True,
        index=True,
        nullable=False,
    )

    password = Column(
        String,
        nullable=False,
    )

    is_admin = Column(
        Boolean,
        default=False,
        nullable=False,
    )


class Sweet(Base):
    """
    Represents a sweet item available in the shop.

    Each sweet has:
    - a name
    - a category (e.g., Indian, Chocolate, Bakery)
    - a price
    - a quantity indicating current stock
    """

    __tablename__ = "sweets"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    name = Column(
        String,
        nullable=False,
    )

    category = Column(
        String,
        nullable=False,
    )

    price = Column(
        Float,
        nullable=False,
    )

    quantity = Column(
        Integer,
        nullable=False,
        default=0,
    )
