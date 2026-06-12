import jwt
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException, Response
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from config.config import SECRET_KEY
from database.db import get_session
from schemas import UserCreate, UserResponse
from repository import insert_user, select_user_by_username

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)

@router.post("/users", response_model=UserResponse)
async def create_user(user: UserCreate, async_session: AsyncSession = Depends(get_session)):
    hashed_password= hash_password(user.password)
    return insert_user(async_session, UserCreate(username=user.username, password=hashed_password))

@router.post("/login")
async def login(creds: UserCreate, response: Response, async_session: AsyncSession = Depends(get_session)):
    user= await select_user_by_username(async_session, creds.username)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    if not verify_password(creds.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    token= jwt.encode({ "user_id": user.id, "exp": datetime.now(timezone.utc) + timedelta(hours=1)}, SECRET_KEY, algorithm="HS256")
    response.set_cookie(key="token", value=token, httponly=True)
    return {"message": "logged in"}

@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie(key="token")
    return {"message": "logged out"}
