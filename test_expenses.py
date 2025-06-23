import pytest
from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.schemas import ExpenseCreate, ExpenseUpdate
from app.services.expenses_service import (
    create_expense_in_db,
    get_all_expenses,
    get_expense_by_id,
    update_expense_in_db,
    delete_expense_from_db,
    get_expenses_from_group
)
from app.models import Expense, Base

@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

@pytest.fixture
def expense_data():
    return ExpenseCreate(user_id=1, group_id=1, amount=100.0, description="Test Expense")

def test_create_and_get_expense(session, expense_data):
    expense = create_expense_in_db(expense_data, session)
    assert expense.amount == 100.0
    fetched = get_expense_by_id(expense.id, session)
    assert fetched.id == expense.id

def test_get_all_expenses(session):
    create_expense_in_db(ExpenseCreate(user_id=1, group_id=1, amount=10, description="Exp1"), session)
    create_expense_in_db(ExpenseCreate(user_id=1, group_id=1, amount=20, description="Exp2"), session)

    expenses = get_all_expenses(session)
    assert len(expenses) >= 2

def test_update_expense(session, expense_data):
    expense = create_expense_in_db(expense_data, session)
    update_data = ExpenseUpdate(amount=200, description="Updated Desc")

    updated = update_expense_in_db(expense.id, update_data, session)
    assert updated.amount == 200
    assert updated.description == "Updated Desc"

def test_delete_expense(session, expense_data):
    expense = create_expense_in_db(expense_data, session)
    deleted = delete_expense_from_db(expense.id, session)
    assert deleted.id == expense.id

    with pytest.raises(HTTPException):
        get_expense_by_id(expense.id, session)

def test_get_expenses_from_group(session):
    create_expense_in_db(ExpenseCreate(user_id=1, group_id=42, amount=50, description="G1"), session)
    create_expense_in_db(ExpenseCreate(user_id=2, group_id=42, amount=75, description="G2"), session)
    expenses = get_expenses_from_group(42, session)
    assert all(exp.group_id == 42 for exp in expenses)
