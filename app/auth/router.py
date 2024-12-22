import uuid
import os
import shutil
from fastapi import APIRouter, Request, Response, UploadFile, WebSocket, WebSocketDisconnect
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from typing import Optional
from starlette.exceptions import HTTPException
from datetime import date
from app.users.service import UserService
from app.users.model import Users
from app.auth.service import create_token, hash_password
from datetime import date


router = APIRouter()

templates = Jinja2Templates(directory='app/view')


@router.post('/registration')
async def registration(first_name: str, last_name: str, email: str, 
                       birth_date: date, password: str):
    photo_uuid = uuid.uuid4()
    print(photo_uuid)
    user = Users(first_name, last_name, email, birth_date,
                 photo_of_profile=photo_uuid,
                 password=hash_password(password))
    path = os.path.join('app/view/static/avatars/', f'{photo_uuid}.png')
    shutil.copy('app/view/static/avatars/default.png', path)
    try:
        UserService.save(user)
    except Exception as ex:
        print(ex)
        raise HTTPException(status_code=409)


@router.post('/login')
async def login(response: Response, email: str, password: str):
    user = UserService.find_by_email_and_password(email, hash_password(password))
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


@router.get('/logout')
async def logout_page(response: Response):
    response = RedirectResponse(url='/login')
    response.delete_cookie("token")
    return response

