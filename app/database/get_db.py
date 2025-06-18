from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

DATABASE_URL = "sqlite:///Broke.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()  # otwieramy sesję
    try:
        yield db          # dajemy sesję endpointowi
    finally:
        db.close()       # na końcu zamykamy sesję