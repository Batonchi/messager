from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from starlette.exceptions import HTTPException
from datetime import date
from app.users.service import UserService
from app.users.model import Users, UsersForm


router = APIRouter()

templates = Jinja2Templates(directory='app/view')


@router.post('/registration')
def registration(user_form: UsersForm):
    user = Users(user_form.first_name, user_form.last_name, user_form.email, user_form.birth_date, user_form.password)
    try:
        UserService.save(user)
    except Exception as ex:
        print(ex)
        raise HTTPException(status_code=409)


@router.post('/login')
def login(email: str, password: str):
    return UserService.find_by_email_and_password(email, password)


@router.get('/registration')
def registration_page(request: Request):
    return templates.TemplateResponse('registration.html', {'request': request})


@router.get('/login')
def login_page(request: Request):
    return templates.TemplateResponse('login.html', {'request': request})

