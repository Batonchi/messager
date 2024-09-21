from fastapi import APIRouter
from datetime import date
from app.users.service import UserService
from app.users.model import Users


router = APIRouter()

@router.post('/registration')
def register(first_name: str, last_name: str, email: str, birth_date: date, password: str):
    user = Users(first_name, last_name, email, birth_date, password)
    UserService.save(user)

@router.post('/login')
def login(email: str, password: str):
    return UserService.find_by_email_and_password(email, password)

