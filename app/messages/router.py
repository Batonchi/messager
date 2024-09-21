from fastapi import APIRouter


router = APIRouter(
    prefix="/chat", tags=['chat']
)

@router.post('')
def chat():
    pass

@router.post('/messages/add')
def messages_add():
    pass


@router.post('/messages/delete')
def messages_delete():
    pass


@router.post('/messages/edit')
def messages_edit():
    pass