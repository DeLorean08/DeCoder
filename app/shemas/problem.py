from pydantic import BaseModel, ConfigDict
from typing import Optional
from fastapi import Form

class ProblemBase(BaseModel):
    submission: str

    @classmethod
    def as_form(cls, submission: str = Form(...)):
        return cls(submission=submission)

# class UserCreate(UserBase):
#     password: str

#     @classmethod
#     def as_form(cls, name: str = Form(...),  email: EmailStr = Form(...), password: str = Form(...)):
#         return cls(name=name, email=email, password=password)