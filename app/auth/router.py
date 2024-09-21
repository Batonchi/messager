from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from datetime import date
from app.users.service import UserService
from app.users.model import Users


router = APIRouter()

templates = Jinja2Templates(directory='app/view')

@router.post('/registration')
def registration(first_name: str, last_name: str, email: str, birth_date: date, password: str):
    user = Users(first_name, last_name, email, birth_date, password)
    UserService.save(user)

@router.post('/login')
def login(email: str, password: str):
    return UserService.find_by_email_and_password(email, password)

@router.get('/registration')
def registration_page(request: Request):
    return templates.TemplateResponse('registration.html', {'request': request})

@router.get('/login')
def login_page(request: Request):
    return templates.TemplateResponse('login.html', {'request': request})
