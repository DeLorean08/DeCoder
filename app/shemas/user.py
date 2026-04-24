from pydantic import BaseModel, EmailStr,  ConfigDict
from typing import Optional

class Userbase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(Userbase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(Userbase):
    id: int
    is_active: bool
    model_config = ConfigDict(from_attributes=True, strict=True)

class UserUpdate(BaseModel):
    name: Optional[str]
    password: Optional[str]