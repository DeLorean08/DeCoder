from sqlalchemy import String, Text, Integer, Boolean, ForeignKey
from sqlalchemy.orm import  Mapped, mapped_column, relationship
from uuid import UUID
from sqlalchemy import Enum as SAEnum
from typing import List
from enum import Enum as PyEnum
from .base import Base


class Difficult(str, PyEnum):
    EASY = "Easy"
    MEDIUM = "Medium"
    HARD= "Hard"


class Problem(Base):
    __tablename__ = "problems"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String())
    description: Mapped[str] = mapped_column(Text())
    starter_code: Mapped[str] = mapped_column(String())
    difficulty: Mapped[Difficult] = mapped_column(SAEnum(Difficult, native_enum=False))
    time_limit: Mapped[int] = mapped_column(Integer())
    memory_limit:  Mapped[int] = mapped_column(Integer())
    is_published: Mapped[bool] = mapped_column(Boolean())

    submissions: Mapped[List["Submission"]] = relationship(back_populates="problem", lazy="selectin")
    test_cases: Mapped[List["Test_case"]] = relationship(back_populates="problem", lazy="selectin")

class Test_case(Base):
    __tablename__ = "test_cases"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    problem_id: Mapped[UUID] = mapped_column(ForeignKey("problems.id"), index=True)
    input_file_path: Mapped[str] = mapped_column(String())
    expected_output_path: Mapped[str] = mapped_column(String())
    is_sample: Mapped[bool] = mapped_column(Boolean())

    problem: Mapped["Problem"] = relationship(back_populates="test_cases", lazy="selectin")
