from fastapi import APIRouter, Request, Depends, WebSocket, WebSocketDisconnect
from app.messages.service import PrivateMessagesService, con_manager
from app.auth.service import get_user_by_token
from fastapi.templating import Jinja2Templates


router = APIRouter(
    prefix="/chat", tags=['chat']
)


templates = Jinja2Templates(directory='app/view')


@router.get('')
async def chats_page(request: Request, user=Depends(get_user_by_token)):
    return templates.TemplateResponse("messages.html", {"request": request})


@router.get('/all')
async def get_all(user=Depends(get_user_by_token)):
    return PrivateMessagesService.get_all_chats(user.user_id)


@router.get('/get')
async def request(request: Request,  user2_id: int, user=Depends(get_user_by_token)):
    return PrivateMessagesService.find_chat(user.user_id, user2_id)


@router.websocket('/send/{recipient_id}')
async def websocket_send_message(websoket: WebSocket, recipient_id: int, user=Depends(get_user_by_token)):
    await con_manager.connect(websoket, user_id=user.user_id)
    try:
        while True:
            text_message = await websoket.receive_text()
            PrivateMessagesService.save(user.user_id, recipient_id, text_message)
            await con_manager.send_message(user.user_id, recipient_id)
    except WebSocketDisconnect:
        con_manager.disconnect(websoket)


@router.post('/messages/add')
async def messages_add(request: Request, text_message: str, recipient_id: int, user=Depends(get_user_by_token)):
    PrivateMessagesService.save(user.user_id, recipient_id, text_message)


@router.delete('/messages/delete')
async def messages_delete():
    pass


@router.post('/messages/edit')
async def messages_edit():
    pass
