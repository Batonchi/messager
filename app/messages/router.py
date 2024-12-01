from fastapi import APIRouter, Request, Depends
from app.messages.service import PrivateMessagesService
from app.auth.service import get_user_by_token


router = APIRouter(
    prefix="/chat", tags=['chat']
)


@router.get('')
async def chats_page(request: Request, user=Depends(get_user_by_token)):
    pass

@router.get('/get')
async def request(request: Request,  user2_id: int, user=Depends(get_user_by_token)):
    return PrivateMessagesService.find_chat(user.user_id, user2_id)


@router.post('/messages/add')
async def messages_add(request: Request, text_message: str, recipient_id: int, user=Depends(get_user_by_token)):
    PrivateMessagesService.save(user.user_id, recipient_id, text_message)


@router.delete('/messages/delete')
async def messages_delete():
    pass


@router.post('/messages/edit')
async def messages_edit():
    pass
