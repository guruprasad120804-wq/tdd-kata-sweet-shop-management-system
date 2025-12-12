from fastapi import FastAPI
from app.auth import router as auth_router

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Sweet Shop API running"}

app.include_router(auth_router)
