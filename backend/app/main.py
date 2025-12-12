
# {
#   "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbkBleGFtcGxlLmNvbSIsImlzX2FkbWluIjp0cnVlLCJleHAiOjE3NjU1NjI1MTZ9.IWbzbQaJAZI-nesapytziKBaqF-hPn8aQIoF-qy6rGM",
#   "token_type": "bearer"
# }


from fastapi import FastAPI
from app.auth import router as auth_router
from app.database import engine
from app import models
from app.sweets import router as sweets_router
from fastapi.middleware.cors import CORSMiddleware



models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Sweet Shop API running"}

app.include_router(auth_router)
app.include_router(sweets_router)

