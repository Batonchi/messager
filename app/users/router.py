import pickle
import os


from fastapi import APIRouter, Request, Depends, UploadFile
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import Optional
from app.auth.service import get_user_by_token
from app.users.service import UserService, FriendService
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


@router.post('/update-data')
async def user_data(request: Request, user=Depends(get_user_by_token)):
    pass


@router.post('/update-avatar')
async def user_avatar(request: Request, photo_of_profile: UploadFile, user=Depends(get_user_by_token)):
    path = os.path.join('app/view/static/avatars/', f'{user.photo_of_profile}.png')
    with open(path, 'wb') as img:
        img.write(await photo_of_profile.read())
    

@router.get("/search")
async def search(request: Request, search_str: str, user=Depends(get_user_by_token)):
    # if rcache.get(search_str):
    #     return pickle.loads(rcache.get(search_str))
    users = UserService.find_by_any(search_str, user.user_id)
    # rcache.set(search_str, pickle.dumps(users))
    return users


@router.get('/friends')
async def friends(request: Request, user=Depends(get_user_by_token)):
    return templates.TemplateResponse("friends.html", {"request": request})


@router.post("/friend/add")
async def add_friend(request: Request, friend_id: int, user=Depends(get_user_by_token)):
    FriendService.save(user.id, friend_id)
    FriendService.save(friend_id, user.id)


@router.post("/friend/remove")
async def remove_friend(request: Request, user=Depends(get_user_by_token)):
    pass


@router.get("/friend/list")
async def list_friends(request: Request, user=Depends(get_user_by_token)):
    return FriendService.find_all(user.user_id)



