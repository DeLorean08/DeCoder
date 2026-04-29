from pydantic import BaseModel, EmailStr,  ConfigDict
from typing import Optional

class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserLogin(UserBase):
    password: str

class UserOut(UserBase):
    id: int
    is_active: bool
    model_config = ConfigDict(from_attributes=True, strict=True)

class UserUpdate(UserBase):
    name: Optional[str]
    password: Optional[str]