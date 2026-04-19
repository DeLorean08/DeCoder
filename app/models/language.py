from sqlalchemy import String, Boolean
from sqlalchemy.orm import  Mapped, mapped_column, relationship
from uuid import UUID
from typing import List
from .base import Base


class Programming_language(Base):
    __tablename__ = "programming_languages"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String())
    docker_image: Mapped[str] = mapped_column(String())
    is_active: Mapped[bool] = mapped_column(Boolean())

    submissions: Mapped[List["Submission"]] = relationship(back_populates="language", cascade="all, delete-orphan", lazy="selectin")