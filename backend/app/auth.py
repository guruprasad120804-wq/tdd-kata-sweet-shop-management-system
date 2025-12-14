"""
Application entry point for the Sweet Shop API.

This module:
- Initializes the FastAPI application
- Configures CORS
- Creates database tables
- Registers API routers
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.auth import router as auth_router
from app.database import Base, engine
from app.sweets import router as sweets_router

# -------------------------------------------------------------------
# FastAPI application instance
# -------------------------------------------------------------------
app = FastAPI(title="Sweet Shop API")

# -------------------------------------------------------------------
# Database initialization
# -------------------------------------------------------------------
# Create all database tables on application startup.
# This is acceptable for small projects and demos.
Base.metadata.create_all(bind=engine)

# -------------------------------------------------------------------
# CORS configuration
# -------------------------------------------------------------------
# Allows the frontend (running on localhost) to communicate
# with the backend API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------------------------------------
# Router registration
# -------------------------------------------------------------------
app.include_router(auth_router)
app.include_router(sweets_router)

# -------------------------------------------------------------------
# Health check endpoint
# -------------------------------------------------------------------
@app.get("/")
def root():
    """
    Health check endpoint.

    Returns a simple message to confirm that the API is running.
    """
    return {"message": "Sweet Shop API running"}
