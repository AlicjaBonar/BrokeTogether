from sqlalchemy.orm import Session
from app.models import User, Group
from fastapi import HTTPException
from typing import List

def add_user_to_group(db: Session, user_id: int, group_id: int):
    user = db.query(User).get(user_id)
    group = db.query(Group).get(group_id)

    if not user or not group:
        raise HTTPException(status_code=404, detail="User or Group not found")
    if group in user.groups:
        raise HTTPException(status_code=400, detail="User already in group")

    user.groups.append(group)
    db.commit()
    return {"detail": f"User {user_id} added to Group {group_id}"}

def remove_user_from_group(db: Session, user_id: int, group_id: int):
    user = db.query(User).get(user_id)
    group = db.query(Group).get(group_id)

    if not user or not group:
        raise HTTPException(status_code=404, detail="User or Group not found")
    if group not in user.groups:
        raise HTTPException(status_code=400, detail="User not in group")

    user.groups.remove(group)
    db.commit()
    return {"detail": f"User {user_id} removed from Group {group_id}"}

def get_users_in_group(db: Session, group_id: int):
    group = db.query(Group).get(group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    return group.users

def get_groups_of_user(db: Session, user_id: int):
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user.groups
