# app/services/user_service.py

from sqlalchemy.orm import Session
from app.models import User
from app.schemas import UserCreate, UserUpdate
from fastapi import HTTPException
import bcrypt

def hash_password(plain_password: str) -> str:
    return bcrypt.hashpw(plain_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def create_user_in_db(user_data: UserCreate, db: Session) -> User:
    existing = db.query(User).filter(User.username == user_data.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_pw = hash_password(user_data.password)
    new_user = User(username=user_data.username, hashed_password=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_all_users(db: Session):
    return db.query(User).all()

def get_user_by_id(db: Session, user_id: int) -> User | None:
    return db.query(User).get(user_id)


def update_user_in_db(db: Session, user_id: int, user_data: UserUpdate) -> User:
    user = db.query(User).get(user_id)
    if not user:
        return None

    if user_data.username:
        user.username = user_data.username
    if user_data.password:
        user.hashed_password = hash_password(user_data.password)
    db.commit()
    db.refresh(user)
    return user


def delete_user_from_db(db: Session, user_id: int) -> bool:
    user = db.query(User).get(user_id)
    if not user:
        return False
    db.delete(user)
    db.commit()
    return True
