
from pydantic import BaseModel
from typing import List, Optional

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from app.models import Expense
from app.schemas import ExpenseCreate, ExpenseRead, ExpenseUpdate
from app.database.get_db import get_db

from sqlalchemy.orm import Session
from app.models import Expense
from app.schemas import ExpenseCreate, ExpenseUpdate
from fastapi import HTTPException


def create_expense_in_db(expense_data: ExpenseCreate, db: Session) -> Expense:
    new_expense = Expense(**expense_data.model_dump())
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return new_expense


def get_all_expenses(db: Session) -> list[Expense]:
    return db.query(Expense).all()


def get_expense_by_id(expense_id: int, db: Session) -> Expense:
    expense = db.query(Expense).get(expense_id)
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense


def update_expense_in_db(expense_id: int, expense_data: ExpenseUpdate, db: Session) -> Expense:
    expense = db.query(Expense).get(expense_id)
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    for key, value in expense_data.model_dump(exclude_unset=True).items():
        setattr(expense, key, value)

    db.commit()
    db.refresh(expense)
    return expense


def delete_expense_from_db(expense_id: int, db: Session) -> Expense:
    expense = db.query(Expense).get(expense_id)
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    db.delete(expense)
    db.commit()
    return expense

# READ all from one group 
def get_expenses_from_group(group_id: int, db: Session):
    return db.query(Expense).filter(Expense.group_id == group_id).all()
