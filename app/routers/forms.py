from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.schemas import GroupCreate, UserCreate
from app.database.get_db import get_db
from app.services.group_service import *
from fastapi import APIRouter, HTTPException, Depends, Request, Form
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database.get_db import get_db
from typing import List
import bcrypt
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.services.user_service import create_user_in_db
from app.services.expenses_service import get_expenses_from_group

router = APIRouter(prefix="/forms", tags=["Forms"])
templates = Jinja2Templates(directory="./app/templates")

@router.get("/group", response_class=HTMLResponse)
def form_add_group_get(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("add_group.html", {"request": request})

@router.post("/group", response_class=HTMLResponse)
def form_add_group_post(
    request: Request,
    name: str = Form(...),
    db: Session = Depends(get_db)
):
    group = GroupCreate(
        name=name
    )
    create_group(db, group)
    return templates.TemplateResponse("add_another_group.html", {"request": request})

@router.get("/user", response_class=HTMLResponse)
def form_add_user_get(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("add_user.html", {"request": request})

@router.post("/user", response_class=HTMLResponse)
def form_add_user_post(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = UserCreate(
        username=username,
        password=password
    )
    create_user_in_db(user, db)
    return templates.TemplateResponse("add_another_user.html", {"request": request})
