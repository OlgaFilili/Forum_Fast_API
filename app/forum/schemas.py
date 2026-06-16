from datetime import datetime
from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    user_id: int
    username: str
    registered_at: datetime

class PostsUserResponse(BaseModel):
    post_id: int
    text: str
    created_at: datetime