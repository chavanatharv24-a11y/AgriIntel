import certifi
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import db
from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings
from app.routes import auth, sensors, recommendations, notifications, ai_assistant, predictions, finance, security, users
@asynccontextmanager
async def lifespan(app: FastAPI):
    db.client = AsyncIOMotorClient(settings.MONGO_URI, tlsCAFile=certifi.where())
    db.db = db.client[settings.MONGO_DB_NAME]
    # Create unique index for email
    await db.db["users"].create_index("email", unique=True)
    yield
    db.client.close()

from fastapi.staticfiles import StaticFiles

app = FastAPI(lifespan=lifespan, title="AgriIntel API")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=".*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(sensors.router)
app.include_router(recommendations.router)
app.include_router(notifications.router)
app.include_router(ai_assistant.router)
app.include_router(predictions.router)
app.include_router(finance.router)
app.include_router(security.router)
app.include_router(users.router)

@app.get("/")
async def root():
    return {"message": "Welcome to AgriIntel API"}
