from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import User, Post
from app.forum.schemas import UserCreate, UserResponse, PostsUserResponse


async def insert_user(session: AsyncSession, user_data: UserCreate) -> UserResponse | None:
    result = await session.execute(select(User).where(User.username == user_data.username))
    user = result.scalar_one_or_none()
    if user:
        return None
    new_user = User(
        username=user_data.username,
        password=user_data.password
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return UserResponse(user_id=new_user.id, username=new_user.username, registered_at=new_user.registered_at)


async def select_user_by_username(session: AsyncSession, username: str) -> User | None:
    result = await session.execute(select(User).where(User.username == username))
    user = result.scalar_one_or_none()
    return user


async def select_user_by_id(session: AsyncSession, id: int) -> User | None:
    result = await session.execute(select(User).where(User.id == id))
    user = result.scalar_one_or_none()
    return user


async def get_posts_by_user_id(session: AsyncSession, user_id: int) -> list[PostsUserResponse]:
    result = await session.execute(select(Post).where(Post.author_id == user_id))
    posts = result.scalars().all()
    return [PostsUserResponse(post_id=post.id, text=post.text, created_at=post.created_at) for post in posts]
