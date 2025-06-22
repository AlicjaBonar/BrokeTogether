from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.database.get_db import get_db
from app.services.balance_service import calculate_balances
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.services.group_service import get_one_group

router = APIRouter(prefix="/balances", tags=["Balances"])

templates = Jinja2Templates(directory="./app/templates")

@router.get("/group/{group_id}", response_class=HTMLResponse)
def get_group_balances(request: Request,group_id: int, db: Session = Depends(get_db)):
    try:
        balances = calculate_balances(group_id, db)
        group = get_one_group(db, group_id)
        return templates.TemplateResponse("group_balance.html", {"request": request, "group": group, "balances": balances})
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))