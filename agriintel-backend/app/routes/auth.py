from fastapi import APIRouter, HTTPException, status, Depends
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
from app.models.security_event import SecurityEventModel

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
        event = SecurityEventModel(email=user_credentials.email, success=False)
        await db.db["security_events"].insert_one(event.model_dump())
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if not verify_password(user_credentials.password, user["password"]):
        event = SecurityEventModel(email=user_credentials.email, success=False)
        await db.db["security_events"].insert_one(event.model_dump())
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user["_id"])}, expires_delta=access_token_expires
    )
    
    event = SecurityEventModel(email=user_credentials.email, success=True)
    await db.db["security_events"].insert_one(event.model_dump())
    
    return {"access_token": access_token, "token_type": "bearer"}
