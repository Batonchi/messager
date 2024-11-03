from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from app.auth.service import get_user_by_token
from app.users.service import UserService


router = APIRouter(
    prefix="/users", tags=['users']
)


templates = Jinja2Templates(directory='app/view')


@router.get("/profile")
async def profile(request: Request, user=Depends(get_user_by_token)):
    return templates.TemplateResponse("profile.html", {"request": request})

@router.get("/profile/{id}")
async def profile(request: Request, id: int, user=Depends(get_user_by_token)):
    return templates.TemplateResponse("no-personal-profile.html", {"request": request})


@router.get("/user")
async def user(request: Request, user=Depends(get_user_by_token)):
    return user


@router.get("/search")
async def search(request: Request, search_str: str):
    users = UserService.find_by_any(search_str)
    return users
