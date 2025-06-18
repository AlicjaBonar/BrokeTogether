from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from app.models import User
from app.models import Group
from app.database.get_db import get_db
from pydantic import BaseModel

router = APIRouter(prefix="/user-groups", tags=["UserGroupAssociation"])

# --- Pydantic Schemas ---

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

# --- CRUD Endpoints ---

# Dodaj użytkownika do grupy
@router.post("/add", response_model=dict)
def add_user_to_group(data: UserGroupAddRequest, db: Session = Depends(get_db)):
    user = db.query(User).get(data.user_id)
    group = db.query(Group).get(data.group_id)

    if not user or not group:
        raise HTTPException(status_code=404, detail="User or Group not found")
    if group in user.groups:
        raise HTTPException(status_code=400, detail="User already in group")

    user.groups.append(group)
    db.commit()
    return {"detail": f"User {data.user_id} added to Group {data.group_id}"}


# Usuń użytkownika z grupy
@router.delete("/user/{user_id}/group/{group_id}")
def remove_user_from_group(user_id: int, group_id: int, db: Session = Depends(get_db)):
    user = db.query(User).get(user_id)
    group = db.query(Group).get(group_id)

    if not user or not group:
        raise HTTPException(status_code=404, detail="User or Group not found")
    if group not in user.groups:
        raise HTTPException(status_code=400, detail="User not in group")

    user.groups.remove(group)
    db.commit()
    return {"detail": f"User {user_id} removed from Group {group_id}"}


# Pobierz użytkowników w grupie
@router.get("/group/{group_id}/users", response_model=List[UserRead])
def get_users_in_group(group_id: int, db: Session = Depends(get_db)):
    group = db.query(Group).get(group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    return group.users


# Pobierz grupy użytkownika
@router.get("/user/{user_id}/groups", response_model=List[GroupRead])
def get_groups_of_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user.groups
