from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os

from app.routers.users import router as users_router
from app.routers.groups import router as groups_router
from app.routers.user_group import router as user_group_router
from app.routers.expenses import router as expenses_router
from app.routers.auth import router as auth_router
from app.routers.balances import router as balances_router
from app.routers.forms import router as forms_router

app = FastAPI()

# Static files (e.g. CSS)
app.mount("/static", StaticFiles(directory=os.path.join("app", "static")), name="static")

# Templates
templates = Jinja2Templates(directory="app/templates")

# Routers
app.include_router(users_router)
app.include_router(groups_router)
app.include_router(user_group_router)
app.include_router(expenses_router)
app.include_router(auth_router)
app.include_router(balances_router)
app.include_router(forms_router)

# Home route
@app.get("/", response_class=HTMLResponse)
async def read_home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

"""
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python app.py <database_name>")
        sys.exit(1)

    db_name = sys.argv[1]
    engine = create_engine(f"sqlite:///{db_name}.db", echo=False)
    Session = sessionmaker(bind=engine, autoflush=False)
"""