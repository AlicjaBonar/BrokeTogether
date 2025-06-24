from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.schemas import GroupCreate, GroupRead
from app.database.get_db import get_db
from app.services.group_service import *
from fastapi import APIRouter, HTTPException, Depends, Request, Form
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database.get_db import get_db
from typing import List
import bcrypt
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.services.user_service import get_all_users_from_group, get_all_users, get_all_users_not_in_group
from app.services.expenses_service import get_expenses_from_group

router = APIRouter(prefix="/groups", tags=["Groups"])
templates = Jinja2Templates(directory="./app/templates")

@router.post("/", response_model=GroupRead)
def create_group_post(group: GroupCreate, db: Session = Depends(get_db)):
    return create_group(db, group)


@router.get("/", response_class=HTMLResponse)
def get_groups(request: Request, db: Session = Depends(get_db)):
    groups = get_all_groups(db)
    return templates.TemplateResponse("groups.html", {"request": request, "groups": groups})


@router.get("/{group_id}", response_class=HTMLResponse)
def get_group(request: Request, group_id: int, db: Session = Depends(get_db)):
    group = get_group_by_id(db, group_id)
    users = get_all_users_from_group(group_id, db)
    all_users = get_all_users_not_in_group(group_id=group_id, db=db)
    expenses = get_expenses_from_group(group_id, db)
    return templates.TemplateResponse("group_detail.html", {"request": request, "group": group, "users": users, "expenses": expenses, "all_users": all_users})


@router.put("/{group_id}", response_model=GroupRead)
def update_group_put(group_id: int, group_data: GroupCreate, db: Session = Depends(get_db)):
    return update_group(db, group_id, group_data)


@router.delete("/{group_id}")
def delete_group_del(group_id: int, db: Session = Depends(get_db)):
    return delete_group(db, group_id)

@router.post("/{group_id}/delete")
def delete_group_del_post(group_id: int, db: Session = Depends(get_db)):
    delete_group(db, group_id)
    return RedirectResponse(url="/groups", status_code=302)


