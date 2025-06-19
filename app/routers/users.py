from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.models import User
from app.database.get_db import get_db
from app.schemas import UserCreate, UserRead, UserUpdate
from app.services.user_service import *
from typing import List
import bcrypt

router = APIRouter(prefix="/users", tags=["Users"])

# CREATE
@router.post("/", response_model=UserRead)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user_in_db(user, db)


# READ all
@router.get("/", response_model=List[UserRead])
def get_users(db: Session = Depends(get_db)):
    return get_all_users(db)


# READ one
@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# UPDATE username or password
@router.put("/{user_id}", response_model=UserRead)
def update_user(user_id: int, user_data: UserUpdate, db: Session = Depends(get_db)):
    user = update_user_in_db(db, user_id, user_data)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# DELETE
@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    success = delete_user_from_db(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User deleted"}

