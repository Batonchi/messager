from fastapi import FastAPI
from starlette.staticfiles import StaticFiles
from app.auth.router import router as auth_router


app = FastAPI()

app.include_router(auth_router)
app.mount('/static', StaticFiles(directory='app/view/static'))