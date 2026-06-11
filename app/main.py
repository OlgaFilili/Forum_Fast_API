from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.forum.routes import router
from app.forum.auth import router as auth_router
from database.db import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(auth_router)
app.include_router(router)
