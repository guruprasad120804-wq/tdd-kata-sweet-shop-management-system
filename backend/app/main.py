

# # {
# #   "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbkBleGFtcGxlLmNvbSIsImlzX2FkbWluIjp0cnVlLCJleHAiOjE3NjU1NjI1MTZ9.IWbzbQaJAZI-nesapytziKBaqF-hPn8aQIoF-qy6rGM",
# #   "token_type": "bearer"

# # -d '{"email":"admin@example.com","password":"pass1234"}'
# # uvicorn app.main:app --reload -----------> run backend
# #npm run dev ------------> run frontend
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.auth import router as auth_router
from app.sweets import router as sweets_router

app = FastAPI(title="Sweet Shop API")

# create tables
Base.metadata.create_all(bind=engine)

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(sweets_router)


@app.get("/")
def root():
    return {"message": "Sweet Shop API running"}
