from fastapi import FastAPI
from fastapi import Request
from fastapi import Form
from fastapi import Depends

from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session

from app.database.db import engine
from app.database.db import Base

from app.database.deps import get_db

from app.models.user import User

from app.utils.security import (
    hash_password,
    verify_password
)

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static"
)

templates = Jinja2Templates(
    directory="app/templates"
)

@app.get("/", response_class=HTMLResponse)
def login_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="auth/login.html"
    )

@app.get("/register", response_class=HTMLResponse)
def register_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="auth/register.html"
    )

@app.post("/register")
def register_user(
    full_name: str = Form(...),
    email: str = Form(...),
    account_id: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):

    existing_user = db.query(User).filter(
        User.account_id == account_id
    ).first()

    if existing_user:

        return {
            "error": "Account ID already exists"
        }

    hashed_password = hash_password(password)

    new_user = User(
        full_name=full_name,
        email=email,
        account_id=account_id,
        password=hashed_password
    )

    db.add(new_user)

    db.commit()

    return RedirectResponse(
        url="/",
        status_code=303
    )

@app.post("/login")
def login_user(
    request: Request,
    account_id: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.account_id == account_id
    ).first()

    if not user:

        return {
            "error": "Invalid Account ID"
        }

    if not verify_password(
        password,
        user.password
    ):

        return {
            "error": "Invalid Password"
        }

    return templates.TemplateResponse(
        request=request,
        name="dashboard/dashboard.html",
        context={
            "request": request,
            "user": user
        }
    )

@app.get("/deposit", response_class=HTMLResponse)
def deposit_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="dashboard/deposit.html"
    )

@app.post("/deposit")
def deposit_money(
    request: Request,
    account_id: str = Form(...),
    amount: float = Form(...),
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.account_id == account_id
    ).first()

    if not user:

        return {
            "error": "User not found"
        }

    user.balance += amount

    db.commit()

    db.refresh(user)

    return templates.TemplateResponse(
        request=request,
        name="dashboard/dashboard.html",
        context={
            "request": request,
            "user": user
        }
    )