
from pydantic import BaseModel
from typing import List, Optional

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from app.models import Expense
from app.schemas import ExpenseCreate, ExpenseRead, ExpenseUpdate
from app.database.get_db import get_db

# READ all from one group 
def get_expenses_from_group(group_id: int, db: Session):
    return db.query(Expense).filter(Expense.group_id == group_id).all()
