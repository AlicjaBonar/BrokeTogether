from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.get_db import get_db
from app.services.balance_service import calculate_balances

router = APIRouter(prefix="/balances", tags=["Balances"])


@router.get("/group/{group_id}")
def get_group_balances(group_id: int, db: Session = Depends(get_db)):
    try:
        balances = calculate_balances(group_id, db)
        return balances
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
