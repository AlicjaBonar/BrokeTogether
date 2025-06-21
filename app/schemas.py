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


class ExpenseCreate(BaseModel):
    user_id: int
    group_id: int
    amount: float
    description: str

class ExpenseRead(BaseModel):
    id: int
    user_id: int
    group_id: int
    amount: float
    description: Optional[str] = None

    class Config:
        orm_mode = True

class ExpenseUpdate(BaseModel):
    amount: Optional[float] = None
    description: Optional[str] = None

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    message: str
    user_id: int

class Token(BaseModel):
    access_token: str
    token_type: str


class GroupCreate(BaseModel):
    name: str


class GroupRead(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class UserRead(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True

class GroupRead(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class UserGroupAddRequest(BaseModel):
    user_id: int
    group_id: int