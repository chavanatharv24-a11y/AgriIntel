import os

base_dir = "c:/Users/athar/AgriIntel/agriintel-backend"

files = {
    ".env.example": """MONGO_URI=mongodb://localhost:27017
MONGO_DB_NAME=agriintel
JWT_SECRET=your_super_secret_jwt_key_here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
""",
    ".gitignore": """venv/
env/
.env
__pycache__/
*.pyc
.pytest_cache/
""",
    "requirements.txt": """fastapi
uvicorn
motor
pydantic>=2.0.0
pydantic-settings
passlib[bcrypt]
python-jose[cryptography]
python-multipart
""",
    "app/__init__.py": "",
    "app/main.py": """from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import db
from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings
from app.routes import auth, sensors

@asynccontextmanager
async def lifespan(app: FastAPI):
    db.client = AsyncIOMotorClient(settings.MONGO_URI)
    db.db = db.client[settings.MONGO_DB_NAME]
    # Create unique index for email
    await db.db["users"].create_index("email", unique=True)
    yield
    db.client.close()

app = FastAPI(lifespan=lifespan, title="AgriIntel API")

app.include_router(auth.router)
app.include_router(sensors.router)

@app.get("/")
async def root():
    return {"message": "Welcome to AgriIntel API"}
""",
    "app/config.py": """from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    MONGO_URI: str = "mongodb://localhost:27017"
    MONGO_DB_NAME: str = "agriintel"
    JWT_SECRET: str = "supersecretkey"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()
""",
    "app/database.py": """from motor.motor_asyncio import AsyncIOMotorClient

class Database:
    client: AsyncIOMotorClient = None
    db = None

db = Database()
""",
    "app/models/__init__.py": "",
    "app/models/user.py": """from pydantic import BaseModel, EmailStr, Field
from datetime import datetime, timezone
from typing import Optional

class UserModel(BaseModel):
    name: str
    age: int
    email: EmailStr
    password: str
    cropType: Optional[str] = None
    landSize: Optional[float] = None
    createdAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
""",
    "app/models/sensor_reading.py": """from pydantic import BaseModel, Field
from datetime import datetime, timezone

class SensorReadingModel(BaseModel):
    userId: str
    deviceId: str
    soilMoisture: float
    temperature: float
    humidity: float
    rainDetected: bool
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
""",
    "app/models/ai_recommendation.py": """from pydantic import BaseModel, Field
from datetime import datetime, timezone
from typing import Optional

class AIRecommendationModel(BaseModel):
    userId: str
    basedOnReadingId: Optional[str] = None
    recommendationText: str
    riskLevel: str
    createdAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
""",
    "app/schemas/__init__.py": "",
    "app/schemas/user.py": """from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    name: str
    age: int
    email: EmailStr
    password: str
    cropType: Optional[str] = None
    landSize: Optional[float] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    name: str
    age: int
    email: EmailStr
    cropType: Optional[str] = None
    landSize: Optional[float] = None
    createdAt: datetime
""",
    "app/schemas/sensor_reading.py": """from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SensorReadingCreate(BaseModel):
    deviceId: str
    soilMoisture: float
    temperature: float
    humidity: float
    rainDetected: bool

class SensorReadingResponse(SensorReadingCreate):
    id: str
    userId: str
    timestamp: datetime
""",
    "app/schemas/ai_recommendation.py": """from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AIRecommendationResponse(BaseModel):
    id: str
    userId: str
    basedOnReadingId: Optional[str] = None
    recommendationText: str
    riskLevel: str
    createdAt: datetime
""",
    "app/schemas/token.py": """from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str
""",
    "app/utils/__init__.py": "",
    "app/utils/security.py": """from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt
from passlib.context import CryptContext
from app.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt
""",
    "app/routes/__init__.py": "",
    "app/routes/auth.py": """from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from bson import ObjectId
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.schemas.token import Token
from app.utils.security import get_password_hash, verify_password, create_access_token
from app.database import db
from app.models.user import UserModel
from datetime import timedelta
from app.config import settings

router = APIRouter(prefix="/auth", tags=["auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = await db.db["users"].find_one({"_id": ObjectId(user_id)})
    if user is None:
        raise credentials_exception
    return user

@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(user: UserCreate):
    existing_user = await db.db["users"].find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = get_password_hash(user.password)
    user_model = UserModel(**user.model_dump(exclude={"password"}), password=hashed_password)
    user_dict = user_model.model_dump()
    
    result = await db.db["users"].insert_one(user_dict)
    
    return UserResponse(
        id=str(result.inserted_id),
        **user_dict
    )

@router.post("/login", response_model=Token)
async def login(user_credentials: UserLogin):
    user = await db.db["users"].find_one({"email": user_credentials.email})
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if not verify_password(user_credentials.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user["_id"])}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
""",
    "app/routes/sensors.py": """from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.schemas.sensor_reading import SensorReadingCreate, SensorReadingResponse
from app.routes.auth import get_current_user
from app.database import db
from app.models.sensor_reading import SensorReadingModel

router = APIRouter(prefix="/sensor", tags=["sensors"])

@router.post("/readings", response_model=SensorReadingResponse)
async def create_reading(reading: SensorReadingCreate, current_user: dict = Depends(get_current_user)):
    reading_model = SensorReadingModel(
        userId=str(current_user["_id"]),
        **reading.model_dump()
    )
    reading_dict = reading_model.model_dump()
    result = await db.db["sensor_readings"].insert_one(reading_dict)
    
    return SensorReadingResponse(
        id=str(result.inserted_id),
        **reading_dict
    )

@router.get("/readings", response_model=List[SensorReadingResponse])
async def get_readings(current_user: dict = Depends(get_current_user)):
    cursor = db.db["sensor_readings"].find({"userId": str(current_user["_id"])})
    readings = await cursor.to_list(length=100)
    
    response_list = []
    for r in readings:
        response_list.append(SensorReadingResponse(
            id=str(r["_id"]),
            **r
        ))
    return response_list
"""
}

for filepath, content in files.items():
    full_path = os.path.join(base_dir, filepath)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
