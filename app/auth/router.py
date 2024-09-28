from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.response import RedirectResponse
from starlette.exeptions import HTTPExeption
from datetime import date
from app.users.service import UserService
from app.users.model import Users, UsersForm


router = APIRouter()

templates = Jinja2Templates(directory='app/view')


@router.post('/registration')
def registration(user_form: UsersForm):
    user = Users(UsersForm.first_name, UsersForm.last_name, UsersForm.email, UsersForm.birth_date, UsersForm.password)
    try:
        UserService.save(user)
    except Exception as ex:
        print(ex)
        raise HTTPExeption(status_code=409)
    return RedirectResponse(url='/login')


@router.post('/login')
def login(email: str, password: str):
    return UserService.find_by_email_and_password(email, password)


@router.get('/registration')
def registration_page(request: Request):
    return templates.TemplateResponse('registration.html', {'request': request})


@router.get('/login')
def login_page(request: Request):
    return templates.TemplateResponse('login.html', {'request': request})

