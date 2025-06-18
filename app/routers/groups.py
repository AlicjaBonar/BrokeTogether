from pydantic import BaseModel
from typing import List, Optional

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from app.models import Group
from app.database.get_db import get_db

router = APIRouter(prefix="/groups", tags=["Groups"])

class GroupCreate(BaseModel):
    name: str

class GroupRead(BaseModel):
    id: int
    name: str
    # opcjonalnie możesz dodać listę userów, np.:
    # users: Optional[List[int]] = []

    class Config:
        orm_mode = True


# CREATE
@router.post("/", response_model=GroupRead)
def create_group(group: GroupCreate, db: Session = Depends(get_db)):
    existing = db.query(Group).filter(Group.name == group.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Group with this name already exists")
    
    new_group = Group(name=group.name)
    db.add(new_group)
    db.commit()
    db.refresh(new_group)
    return new_group

# READ all
@router.get("/", response_model=List[GroupRead])
def get_groups(db: Session = Depends(get_db)):
    return db.query(Group).all()

# READ one
@router.get("/{group_id}", response_model=GroupRead)
def get_group(group_id: int, db: Session = Depends(get_db)):
    group = db.query(Group).get(group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    return group

# UPDATE
@router.put("/{group_id}", response_model=GroupRead)
def update_group(group_id: int, group_data: GroupCreate, db: Session = Depends(get_db)):
    group = db.query(Group).get(group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    
    group.name = group_data.name
    db.commit()
    db.refresh(group)
    return group

# DELETE
@router.delete("/{group_id}")
def delete_group(group_id: int, db: Session = Depends(get_db)):
    group = db.query(Group).get(group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    
    db.delete(group)
    db.commit()
    return {"detail": "Group deleted"}
