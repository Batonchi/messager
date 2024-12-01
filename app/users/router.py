import pickle


from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from app.auth.service import get_user_by_token
from app.users.service import UserService
from database import rcache


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
    if rcache.get(search_str):
        return pickle.loads(rcache.get(search_str))
    users = UserService.find_by_any(search_str)
    rcache.set(search_str, pickle.dumps(users))
    return users


@router.get('/friends')
async def friends(request: Request, user=Depends(get_user_by_token)):
    return templates.TemplateResponse("friends.html", {"request": request})


@router.post("/friend/add")
async def add_friend(request: Request, user=Depends(get_user_by_token)):
    pass


@router.post("/friend/remove")
async def remove_friend(request: Request, user=Depends(get_user_by_token)):
    pass


@router.post("/friend/list")
async def list_friends(request: Request, user=Depends(get_user_by_token)):
    pass



