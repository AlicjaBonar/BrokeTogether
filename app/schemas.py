from pydantic import BaseModel
from typing import Optional

# Pydantic Schemas
class UserCreate(BaseModel):
    username: str
    password: str

class UserRead(BaseModel):
    id: int
    username: str
    hashed_password: str

    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None