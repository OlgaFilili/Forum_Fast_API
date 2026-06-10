from datetime import datetime

from sqlalchemy import Boolean, Integer, ForeignKey, func, SmallInteger, String, Text, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str]= mapped_column(String(50), unique=True, nullable=False)
    password: Mapped[str]= mapped_column(String(128), nullable=False)
    registered_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    banned_until: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    # Define a relationship to the Post model
    posts: Mapped[list["Post"]] = relationship(
        back_populates="author", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"Author(user_id={self.id!r}, username={self.username!r})"

class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    author_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())

    # Define a relationship to the User model
    author: Mapped[User] = relationship(
        back_populates="posts"
    )

    def __repr__(self) -> str:
        return f"Post(post_id={self.id!r}, text={self.text!r})"


class Vote(Base):
    __tablename__ = "votes"

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), primary_key=True)
    post_id: Mapped[int] = mapped_column(Integer, ForeignKey('posts.id'), primary_key=True)
    vote: Mapped[int] = mapped_column(SmallInteger, default=0)
