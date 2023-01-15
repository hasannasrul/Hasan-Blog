from typing import List
from datetime import datetime
from bson import ObjectId
from pydantic import BaseModel, validator, EmailStr

class User(BaseModel):
    username: str
    email: EmailStr
    password: str
    first_name: str = None
    last_name: str = None
    bio: str = None
    profile_picture: str = None
    date_joined: datetime
    last_login: datetime
    is_active: bool = True
    is_superuser: bool = False
    hashed_password: str
    salt: str
    role: str
