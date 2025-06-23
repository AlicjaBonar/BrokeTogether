from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models import Group
from app.schemas import GroupCreate


def create_group(db: Session, group_data: GroupCreate):
    existing = db.query(Group).filter(Group.name == group_data.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Group with this name already exists")

    new_group = Group(name=group_data.name)
    db.add(new_group)
    db.commit()
    db.refresh(new_group)
    return new_group


def get_all_groups(db: Session):
    return db.query(Group).all()

def get_one_group(db: Session, group_id: int):
    return db.get(Group, group_id)


def get_group_by_id(db: Session, group_id: int):
    group = db.get(Group, group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    return group


def update_group(db: Session, group_id: int, group_data: GroupCreate):
    group = db.get(Group, group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")

    group.name = group_data.name
    db.commit()
    db.refresh(group)
    return group


def delete_group(db: Session, group_id: int):
    group = db.get(Group, group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")

    db.delete(group)
    db.commit()
    return {"detail": "Group deleted"}
