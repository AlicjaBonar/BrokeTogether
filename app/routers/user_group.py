from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel


from app.schemas import *

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.schemas import GroupCreate, GroupRead
from app.database.get_db import get_db
from app.services.group_service import *
from fastapi import APIRouter, HTTPException, Depends, Request, Form
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from app.database.get_db import get_db
from typing import List
import bcrypt
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.services.user_service import get_all_users_from_group

from app.database.get_db import get_db
from app.models import User, Group
from app.services.user_group_service import (
    add_user_to_group,
    remove_user_from_group,
    get_users_in_group,
    get_groups_of_user
)

router = APIRouter(prefix="/user-groups", tags=["UserGroupAssociation"])
templates = Jinja2Templates(directory="./app/templates")

@router.post("/add", response_model=dict)
def api_add_user_to_group(data: UserGroupAddRequest, db: Session = Depends(get_db)):
    return add_user_to_group(db, data.user_id, data.group_id)

@router.post("/add-form", response_model=dict)
def api_add_user_to_group_form(user_id: int = Form(...), group_id: int = Form(...), db: Session = Depends(get_db)):
    user = add_user_to_group(db, user_id, group_id)
    return RedirectResponse(url=f"/groups/{group_id}", status_code=303)

@router.delete("/user/{user_id}/group/{group_id}", response_model=dict)
def api_remove_user_from_group(user_id: int, group_id: int, db: Session = Depends(get_db)):
    return remove_user_from_group(db, user_id, group_id)

@router.get("/group/{group_id}/users", response_model=List[UserRead])
def api_get_users_in_group(group_id: int, db: Session = Depends(get_db)):
    return get_users_in_group(db, group_id)

@router.get("/user/{user_id}/groups", response_model=List[GroupRead])
def api_get_groups_of_user(user_id: int, db: Session = Depends(get_db)):
    return get_groups_of_user(db, user_id)