import pickle
import os


from fastapi import APIRouter, Request, Depends, UploadFile, WebSocket, WebSocketDisconnect
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import Optional
from app.auth.service import get_user_by_token
from app.users.service import UserService, FriendService, NotificationService, con_manager
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
    return templates.TemplateResponse("no-personal-profile.html", {"request": request, "current_user_id": user.user_id})


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
    return templates.TemplateResponse("friends.html", {"request": request, "current_user_id": user.user_id})


@router.websocket('/friend/add/{current_user_id}')
async def websocket_send_notification(web_soket: WebSocket, current_user_id: int, friend_id: int = None):
    await con_manager.connect(web_soket, user_id=current_user_id)
    try:
        while True:
            await web_soket.receive_text()
            NotificationService.save(friend_id, current_user_id)
            await con_manager.send_notification(current_user_id, friend_id)
    except WebSocketDisconnect:
        con_manager.disconnect(web_soket)


@router.post("/friend/accept")
async def accept_friend(request: Request, friend_id: int, user=Depends(get_user_by_token)):
    FriendService.save(user.user_id, friend_id)
    FriendService.save(friend_id, user.user_id)
    NotificationService.accept(user.user_id, friend_id)


@router.get("/check_friend")
async def check_friend(request: Request, friend_id: int, user=Depends(get_user_by_token)):
    return FriendService.check_friend(friend_id, user.user_id)


@router.get('/notification/list')
async def notification_list(request: Request, user=Depends(get_user_by_token)):
    return NotificationService.find_all(user.user_id)


@router.post("/friend/remove")
async def remove_friend(request: Request, user=Depends(get_user_by_token)):
    pass


@router.get("/friend/list")
async def list_friends(request: Request, user=Depends(get_user_by_token)):
    return FriendService.find_all(user.user_id)





