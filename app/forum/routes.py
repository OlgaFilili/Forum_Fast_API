from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from database.db import get_session
from database.models import User
from app.forum.auth import get_current_user
from app.forum.repository import get_posts_by_user_id
from app.forum.schemas import PostsUserResponse

router = APIRouter(prefix="/forum", tags=["forum"])

@router.get("/my/posts", response_model=list[PostsUserResponse])
async def list_posts(current_user: User = Depends(get_current_user),
                     async_session: AsyncSession = Depends(get_session)) -> list[PostsUserResponse]:
    if not current_user:
        raise HTTPException(status_code=400, detail="User not found")
    posts = await get_posts_by_user_id(async_session, current_user.id)
    return posts
