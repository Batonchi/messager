from fastapi import FastAPI, Request
from starlette.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.auth.router import router as auth_router



app = FastAPI()

templates = Jinja2Templates(directory='app/view')

app.include_router(auth_router)
app.mount('/static', StaticFiles(directory='app/view/static'))

@app.get('/')
def main_page(request: Request):
    return templates.TemplateResponse('main.html', {'request': request})