from fastapi import FastAPI
from app.auth import router as auth_router
from app.database import engine
from app import models
from app.sweets import router as sweets_router


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Sweet Shop API running"}

app.include_router(auth_router)
app.include_router(sweets_router)
