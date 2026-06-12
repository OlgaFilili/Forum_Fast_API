from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import User
from schemas import UserCreate, UserResponse


async def insert_user(session: AsyncSession, user_data: UserCreate) -> UserResponse:
    result = await session.execute(select(User).where(User.username == user_data.username))
    user = result.scalar_one_or_none()
    if user:
        raise ValueError("User already exists")
    new_user = User(
        username=user_data.username,
        password=user_data.password
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return UserResponse(user_id=new_user.id, registered_at=new_user.registered_at)

async def select_user_by_username(session: AsyncSession, username: str)-> User | None:
    result = await session.execute(select(User).where(User.username == username))
    user = result.scalar_one_or_none()
    return user
