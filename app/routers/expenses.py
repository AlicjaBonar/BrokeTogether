from fastapi import APIRouter, HTTPException, Depends, Request, Form
from sqlalchemy.orm import Session
from typing import List
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.schemas import ExpenseCreate, ExpenseRead, ExpenseUpdate
from app.database.get_db import get_db
from app.services.expenses_service import (
    create_expense_in_db,
    get_all_expenses,
    get_expense_by_id,
    update_expense_in_db,
    delete_expense_from_db
)
from app.services.group_service import get_one_group
from app.services.user_service import get_all_users_from_group

router = APIRouter(prefix="/expenses", tags=["Expenses"])
templates = Jinja2Templates(directory="./app/templates")

# CREATE
@router.post("/", response_model=ExpenseRead)
def create_expense(expense: ExpenseCreate, db: Session = Depends(get_db)):
    return create_expense_in_db(expense, db)

# READ all
@router.get("/all", response_model=List[ExpenseRead])
def read_all_expenses(db: Session = Depends(get_db)):
    return get_all_expenses(db)

# READ one
@router.get("/one/{expense_id}", response_model=ExpenseRead)
def read_expense(expense_id: int, db: Session = Depends(get_db)):
    return get_expense_by_id(expense_id, db)

# UPDATE
@router.put("/{expense_id}", response_model=ExpenseRead)
def update_expense(expense_id: int, expense_data: ExpenseUpdate, db: Session = Depends(get_db)):
    return update_expense_in_db(expense_id, expense_data, db)

# DELETE
@router.delete("/{expense_id}", response_model=ExpenseRead)
def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    return delete_expense_from_db(expense_id, db)

# FORM
@router.get("/add-form/{group_id}", response_class=HTMLResponse)
def show_add_form(request: Request, group_id: int, db: Session = Depends(get_db)):
    group = get_one_group(db, group_id)
    users = get_all_users_from_group(group_id=group_id, db=db)
    return templates.TemplateResponse("add_expense.html", {"request": request, "group": group, "users": users})

@router.post("/add-form", response_class=HTMLResponse)
def add_form(
    request: Request,
    user_id: int = Form(...),
    group_id: int = Form(...),
    amount: float = Form(...),
    description: str = Form(None),
    db: Session = Depends(get_db)
):
    expense = ExpenseCreate(
        user_id=user_id,
        group_id=group_id,
        amount=amount,
        description=description
    )
    create_expense_in_db(expense, db)
    group = get_one_group(db, group_id)
    return templates.TemplateResponse("add_another_expense.html", {"request": request, "group": group})
