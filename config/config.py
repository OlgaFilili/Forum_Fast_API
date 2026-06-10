import os
from dotenv import load_dotenv

load_dotenv()

CONNECTION_STRING = (
    f"postgresql+asyncpg://{os.getenv('DB_USER')}:"
    f"{os.getenv('DB_PASSWORD')}@127.0.0.1:5432/"
    f"{os.getenv('DB_NAME')}"
)