from pydantic import BaseModel, EmailStr,  ConfigDict
from typing import Optional
from fastapi import Form

class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

    @classmethod
    def as_form(cls, name: str = Form(...),  email: EmailStr = Form(...), password: str = Form(...)):
        return cls(name=name, email=email, password=password)

class UserLogin(UserBase):
    name: Optional[str] = None
    password: str

    @classmethod
    def as_form(cls, email: EmailStr = Form(...), password: str = Form(...)):
        return cls(email=email, password=password)

class UserOut(UserBase):
    id: int
    is_active: bool
    model_config = ConfigDict(from_attributes=True, strict=True)

class UserUpdate(UserBase):
    name: Optional[str]
    password: Optional[str]