from fastapi import APIRouter, HTTPException, Depends, Request, Form
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.models import User
from app.database.get_db import get_db
from app.schemas import UserCreate, UserRead, UserUpdate
from app.services.user_service import *
from typing import List
import bcrypt
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi import Cookie
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from passlib.context import CryptContext

router = APIRouter(prefix="/auth0", tags=["Login"])
templates = Jinja2Templates(directory="./app/templates")

ALGORITHM = "HS256"
SECRET = "super-secret-key"  # We should change this to something secure

bcrypt_context = CryptContext(schemes=['bycrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

manager = LoginManager(SECRET, token_url="/auth/token")

def hash_password(plain_password: str) -> str:
    return bcrypt.hashpw(plain_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


def get_current_user(token: str = Cookie(None), db: Session = Depends(get_db)
):
    if token is None:
        raise HTTPException(status_code=401, detail="Missing token")

    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# HOME
@router.get("/", response_class=HTMLResponse)
def login_page(request: Request, user=Depends(get_current_user)):
    return templates.TemplateResponse("index.html", {"request": request, "user": user})


# LOGIN
@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request, error: str | None = None):
    return templates.TemplateResponse("login.html", {"request": request, "error": error})


@router.post("/token")
def login(username: str = Form(), password: str = Form(), db=Depends(get_db)):
    token = authenticate_user(username, password, db)
    redirect = RedirectResponse(url="/auth", status_code=303)
    redirect.set_cookie(
        key="access_token",
        value=token,
        httponly=True,         # prevents JS access (security)
        max_age=1800,          # expires in 30 mins
        samesite="lax",        # CSRF protection
        secure=False           # set to True in production with HTTPS
    )
    return redirect
    return {"access_token": token, "token_type": "bearer"}
    #return templates.TemplateResponse("login.html", {"request": request, "error": error_message})
