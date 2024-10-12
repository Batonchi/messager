from fastapi import APIRouter, Request, Response
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from starlette.exceptions import HTTPException
from datetime import date
from app.users.service import UserService
from app.users.model import Users, UsersForm
from app.auth.service import create_token


router = APIRouter()

templates = Jinja2Templates(directory='app/view')


@router.post('/registration')
async def registration(user_form: UsersForm):
    user = Users(user_form.first_name, user_form.last_name, user_form.email, user_form.birth_date, user_form.password)
    try:
        UserService.save(user)
    except Exception as ex:
        print(ex)
        raise HTTPException(status_code=409)


@router.post('/login')
async def login(response: Response, email: str, password: str):
    user = UserService.find_by_email_and_password(email, password)
    if not user:
         raise HTTPException(status_code=409, detail="Пользователь не найден! Неверный логин или пароль!")
    token = create_token(email, password)
    response.set_cookie("token", token, httponly=True)
    return user.user_id


@router.get('/registration')
async def registration_page(request: Request):
    return templates.TemplateResponse('registration.html', {'request': request})


@router.get('/login')
async def login_page(request: Request):
    return templates.TemplateResponse('login.html', {'request': request})

