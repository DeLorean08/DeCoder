from pydantic import BaseModel, EmailStr,  ConfigDict
from typing import Optional

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData:
    pass
