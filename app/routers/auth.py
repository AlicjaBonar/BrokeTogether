from fastapi import APIRouter, HTTPException, Depends, Request, Form, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.models import User
from app.database.get_db import get_db
from app.schemas import UserCreate, UserRead, UserUpdate
from app.services.user_service import *
from typing import List, Annotated
import bcrypt
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi import Cookie
from jose import jwt, JWTError
from app.schemas import Token
import bcrypt

from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from passlib.context import CryptContext

ALGORITHM = "HS256"
SECRET = "super-secret-key"  # We should change this to something secure

#bcrypt_context = CryptContext(schemes=['bycrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')


router = APIRouter(prefix="/auth", tags=["Auth"])
templates = Jinja2Templates(directory="./app/templates")

"""async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    print("In get_current_user")
    try: 
        print("payload:", payload)
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user.")
        return {'username': username, 'id': user_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user.")
"""
async def get_current_user(token: str = Cookie(None)):
    if not token:
        raise HTTPException(status_code=401, detail="No token found in cookies")
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        username = payload.get("sub")
        user_id = payload.get("id")
        if username is None or user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return {"username": username, "id": user_id}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

# LOGIN
@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request, error: str | None = None):
    return templates.TemplateResponse("login.html", {"request": request, "error": error})


@router.post("/token", response_model=Token)
async def login_for_access_token(username: str = Form(), password: str = Form(), db=Depends(get_db)):
    token = authenticate_user(username, password, db)
    #return {"access_token": token, "token_type": "bearer"}
    response = RedirectResponse(url="/auth/", status_code=302)
    """response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=False,       # True w produkcji z HTTPS
        samesite="lax"      # lub 'none' dla różnych domen
    )"""
    response.set_cookie(key="user", value=username)
    return response

# HOME
@router.get("/", response_class=HTMLResponse)
def login_page(request: Request):
    user = request.cookies.get("user")
    print(user)
    return templates.TemplateResponse("index.html", {"request": request, "user": user})


