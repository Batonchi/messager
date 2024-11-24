from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import RedirectResponse
from starlette.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.auth.router import router as auth_router
from app.users.router import router as user_router
from app.messages.router import router as messages_router
from database import create_database, rcache

create_database()

app = FastAPI()
templates = Jinja2Templates(directory='app/view')

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(messages_router)
app.mount('/static', StaticFiles(directory='app/view/static'))


@app.exception_handler(HTTPException)
async def exception_handler(request, exc):
    code = exc.__dict__['status_code']
    if code == 404:
        return RedirectResponse(url='/error')
    
    return RedirectResponse(url='/login')


@app.get('/')
def main_page(request: Request):
    return templates.TemplateResponse('main.html', {'request': request})


@app.get('/error')
def error(request: Request):
    return templates.TemplateResponse('error.html', {'request': request})


# alist = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
#
#
# @app.get('/test/{id}')
# def test(request: Request, id: int):
#     alist.append(id)
#     rcache.flushdb()
#
# @app.get('/test-list')
# def test_list(request: Request):
#     import json, time
#     global alist
#     if rcache.get('alist'):
#         return json.loads(rcache.get('alist'))
#     time.sleep(10)
#     rcache.set('alist', json.dumps(alist))
#     return alist

