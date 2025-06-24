# app/services/user_service.py

from sqlalchemy.orm import Session
from app.models import User
from app.schemas import UserCreate, UserUpdate
from fastapi import HTTPException
import bcrypt
from datetime import timedelta, datetime
from jose import jwt, JWTError
from app.models import Group

from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException

SECRET = "super-secret-key"  # We should change this to something secure
ALGORITHM = "HS256"

#manager = LoginManager(SECRET, token_url="/auth/token")

def hash_password(plain_password: str) -> str:
    return bcrypt.hashpw(plain_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

#@manager.user_loader
def load_user(username: str, db: Session):
    return db.query(User).filter(User.username == username).first()

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
    return db.get(User, user_id)


def update_user_in_db(db: Session, user_id: int, user_data: UserUpdate) -> User:
    user = db.get(User, user_id)
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
    user = db.get(User, user_id)
    if not user:
        return False
    db.delete(user)
    db.commit()
    return True


def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id}
    expires = datetime.now() + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET, algorithm=ALGORITHM)

def authenticate_user(username: str, password: str, db: Session) -> str:
    user = db.query(User).filter(User.username == username).first()
    print("Czy user znaleziony: ", user == None)
    if not user or not bcrypt.checkpw(password.encode(), user.hashed_password.encode()):
        raise InvalidCredentialsException
    return create_access_token(username=username, user_id=user.id, expires_delta=timedelta(seconds=50000))

def get_all_users_from_group(group_id: int, db: Session):
    group = db.get(Group, group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")

    return group.users

def get_all_users_not_in_group(group_id: int, db: Session):
    group = db.get(Group, group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")

    user_ids_in_group = [user.id for user in group.users]

    users_not_in_group = db.query(User).filter(User.id.notin_(user_ids_in_group)).all()

    return users_not_in_group
