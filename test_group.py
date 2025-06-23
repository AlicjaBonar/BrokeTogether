import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models import Base, Group
from app.services.group_service import create_group, get_all_groups, get_one_group, get_group_by_id, update_group, delete_group
from app.schemas import GroupCreate
from fastapi import HTTPException

@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


def test_create_group(session):
    group_data = GroupCreate(name="TestGroup")
    group = create_group(session, group_data)
    assert group.name == "TestGroup"
    assert group.id is not None


def test_create_duplicate_group_raises(session):
    group_data = GroupCreate(name="TestGroup")
    create_group(session, group_data)
    with pytest.raises(HTTPException):
        create_group(session, group_data)


def test_get_all_groups(session):
    create_group(session, GroupCreate(name="G1"))
    create_group(session, GroupCreate(name="G2"))
    groups = get_all_groups(session)
    assert len(groups) == 2


def test_get_one_group(session):
    group = create_group(session, GroupCreate(name="SingleGroup"))
    got = get_one_group(session, group.id)
    assert got.id == group.id
    assert got.name == group.name


def test_get_group_by_id_not_found(session):
    with pytest.raises(HTTPException):
        get_group_by_id(session, 999)


def test_update_group(session):
    group = create_group(session, GroupCreate(name="OldName"))
    updated = update_group(session, group.id, GroupCreate(name="NewName"))
    assert updated.name == "NewName"


def test_update_group_not_found(session):
    with pytest.raises(HTTPException):
        update_group(session, 999, GroupCreate(name="NoGroup"))


def test_delete_group(session):
    group = create_group(session, GroupCreate(name="ToDelete"))
    result = delete_group(session, group.id)
    with pytest.raises(HTTPException):
        get_group_by_id(session, group.id)


def test_delete_group_not_found(session):
    with pytest.raises(HTTPException):
        delete_group(session, 999)
