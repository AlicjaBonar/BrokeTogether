from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import sys
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker


DATABASE_NAME = "Broke"

app = FastAPI() 

from fastapi import FastAPI
from app.routers.users import router as users_router
from app.routers.groups import router as groups_router
from app.routers.user_group import router as user_group_router
from app.routers.expenses import router as expenses_router

app = FastAPI()

app.include_router(users_router)
app.include_router(groups_router)
app.include_router(user_group_router)
app.include_router(expenses_router)

"""
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python app.py <database_name>")
        sys.exit(1)

    db_name = sys.argv[1]
    engine = create_engine(f"sqlite:///{db_name}.db", echo=False)
    Session = sessionmaker(bind=engine, autoflush=False)
"""