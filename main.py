from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import RedirectResponse
from starlette.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.auth.router import router as auth_router
from app.users.router import router as user_router

from database import create_database

create_database()

app = FastAPI()
templates = Jinja2Templates(directory='app/view')

app.include_router(auth_router)
app.include_router(user_router)
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


