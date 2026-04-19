from sqlalchemy import String, func
from sqlalchemy.orm import  Mapped, mapped_column, relationship
from uuid import UUID
from datetime import datetime
from typing import List
from .base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String())
    email: Mapped[str] = mapped_column(String(), unique=True)
    hashed_password: Mapped[str] = mapped_column(String())
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    submissions: Mapped[List["Submission"]] = relationship(back_populates="users", cascade="all, delete-orphan", lazy="selectin")
