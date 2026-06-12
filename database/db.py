from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from config.config import CONNECTION_STRING
from database.models import Base

engine = create_async_engine(CONNECTION_STRING, echo=True)
SessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)


async def get_session():
    async with SessionLocal() as session:
        yield session


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
