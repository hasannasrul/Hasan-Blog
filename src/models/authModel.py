from typing import Optional, List
from pydantic import BaseModel, EmailStr

class UserJWT(BaseModel):
    sub: str
    exp: int
    iat: int
    roles: List[str]