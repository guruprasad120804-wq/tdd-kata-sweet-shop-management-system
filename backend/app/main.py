from fastapi import FastAPI
from app.auth import router as auth_router
from app.database import engine
from app import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Sweet Shop API running"}

app.include_router(auth_router)
