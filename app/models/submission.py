from sqlalchemy import  Text, ForeignKey, func, Integer, Float
from sqlalchemy.orm import  Mapped, mapped_column, relationship
from uuid import UUID
from datetime import datetime
from sqlalchemy import Enum as SAEnum
from .base import Base
from enum import Enum as PyEnum

class Status(str, PyEnum):
    IN_QUEUE = "In Queue"
    RUNNING = "Running"
    ACCEPTED = "Accepted"
    WRONG_ANSWER = "Wrong Answer"
    TIME_LIMIT_EXCEEDED = "Time Limit Exceeded"
    RUNTIME_ERROR = "Runtime Error"


class Submission(Base):
    __tablename__ = "submissions"

    id: Mapped[UUID] = mapped_column(primary_key=True)

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), index=True)
    problem_id: Mapped[UUID] = mapped_column(ForeignKey("problems.id"), index=True)
    language_id: Mapped[UUID] = mapped_column(ForeignKey("programming_languages.id"), index=True)
    code: Mapped[str] = mapped_column(Text())
    status: Mapped[Status] = mapped_column(SAEnum(Status, native_enum=False))
    execution_time: Mapped[float] = mapped_column(Float())
    execution_memory: Mapped[int] = mapped_column(Integer())
    error_message: Mapped[str] = mapped_column(Text())
    created_at:  Mapped[datetime] = mapped_column(server_default=func.now())

    user: Mapped["User"] = relationship(back_populates="submissions", lazy="selectin")
    problem: Mapped["Problem"] = relationship(back_populates="submissions", lazy="selectin")
    language: Mapped["Programming_language"] = relationship(back_populates="submissions", lazy="selectin")
