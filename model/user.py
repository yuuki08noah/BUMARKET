from datetime import datetime

from pydantic import BaseModel

class UserResponse(BaseModel):
    user_id: int
    username: str
    name: str
    is_admin: bool = False
    created_at: datetime

class UserAuthentication(BaseModel):
    username: str
    password: str

class UserCreation(BaseModel):
    username: str
    password: str
    name: str
    admin: bool