import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models import Base, User
from app.services.user_service import (
    create_user_in_db,
    get_all_users,
    get_user_by_id,
    update_user_in_db,
    delete_user_from_db,
)
from app.schemas import UserCreate, UserUpdate

@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

def test_create_user(session):
    # 1. Create user
    user_data = UserCreate(username="Ania", password="Ania123")

    # 2. Save user
    create_user_in_db(user_data, session)

    # 3. Check if they were added
    result = session.query(User).filter_by(username="Ania").first()
    assert result is not None
    assert result.username == "Ania"

def test_create_duplicate_user_raises(session):
    user_data = UserCreate(username="Ania", password="Ania123")
    create_user_in_db(user_data, session)
    with pytest.raises(Exception):
        create_user_in_db(user_data, session)  # powinno podnieść HTTPException

def test_get_all_users(session):
    user1 = create_user_in_db(UserCreate(username="Ala", password="ala123"), session)
    user2 = create_user_in_db(UserCreate(username="Ola", password="ola123"), session)
    users = get_all_users(session)
    assert len(users) == 2
    assert any(u.username == "Ala" for u in users)
    assert any(u.username == "Ola" for u in users)

def test_get_user_by_id(session):
    user = create_user_in_db(UserCreate(username="Ania", password="Ania123"), session)
    found = get_user_by_id(session, user.id)
    assert found is not None
    assert found.username == "Ania"

def test_update_user(session):
    user = create_user_in_db(UserCreate(username="Ania", password="Ania123"), session)
    old_hashed = user.hashed_password  # zapisz stary hash

    update_data = UserUpdate(username="Anka", password="NoweHaslo123")
    updated = update_user_in_db(session, user.id, update_data)

    assert updated.username == "Anka"
    assert updated.hashed_password != old_hashed 

def test_delete_user(session):
    user = create_user_in_db(UserCreate(username="Ania", password="Ania123"), session)
    deleted = delete_user_from_db(session, user.id)
    assert deleted is True
    missing = get_user_by_id(session, user.id)
    assert missing is None
