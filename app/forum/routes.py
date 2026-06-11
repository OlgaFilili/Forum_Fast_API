from fastapi import APIRouter
from database.db import get_session

router = APIRouter(prefix="/forum", tags=["forum"])


@router.get("/")
def home():
    return {"message": "Welcome to FastAPI Forum soon!"}





