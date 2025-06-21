from pydantic import BaseModel
from typing import List, Optional

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from app.models import Expense
from app.schemas import ExpenseCreate, ExpenseRead, ExpenseUpdate
from app.database.get_db import get_db

router = APIRouter(prefix="/expenses", tags=["Expenses"])

# CREATE
@router.post("/", response_model=ExpenseRead)
def create_expense(expense: ExpenseCreate, db: Session = Depends(get_db)):
    new_expense = Expense(**expense.model_dump())
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return new_expense

# READ all
@router.get("/all", response_model=List[ExpenseRead])
def get_expenses(db: Session = Depends(get_db)):
    return db.query(Expense).all()


# READ one
@router.get("/one/{expense_id}", response_model=ExpenseRead)
def get_expense(expense_id: int, db: Session = Depends(get_db)):
    expense = db.query(Expense).get(expense_id)
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense

# UPDATE
@router.put("/{expense_id}", response_model=ExpenseRead)
def update_expense(expense_id: int, expense_data: ExpenseUpdate, db: Session = Depends(get_db)):
        expense = db.query(Expense).get(expense_id)
        if not expense:
            raise HTTPException(status_code=404, detail="Expense not found")
        
        for key, value in expense_data.model_dump(exclude_unset=True).items():
            setattr(expense, key, value)
        
        db.commit()
        db.refresh(expense)
        return expense

# DELETE
@router.delete("/{expense_id}", response_model=ExpenseRead)
def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    expense = db.query(Expense).get(expense_id)
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    
    db.delete(expense)
    db.commit()
    return expense