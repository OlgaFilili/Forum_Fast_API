from fastapi import APIRouter, Depends, HTTPException
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from database.db import get_session
from schemas import UserCreate, UserResponse
from repository import insert_user

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

