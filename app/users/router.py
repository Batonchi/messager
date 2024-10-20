from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from app.auth.service import get_user_by_token
from app.users.service import UserService


router = APIRouter(
    prefix="/users", tags=['users']
)


templates = Jinja2Templates(directory='app/view')


@router.get("/profile")
async def profile(request: Request):
    user = get_user_by_token(request)
    if not user:
        return RedirectResponse("/login")
    return templates.TemplateResponse("profile.html", {"request": request})


@router.get("/user")
async def user(request: Request):
    user = get_user_by_token(request)
    return user


@router.get("/search")
async def search(request: Request, search_str: str):
    users = UserService.find_by_any(search_str)
    return users
