from fastapi import Depends, FastAPI

from app.routers import users_api

from .dependencies import get_query_token, get_token_header
from .internal import admin
from .routers import content_api, users_api

app = FastAPI(dependencies=[Depends(get_query_token)])


app.include_router(users_api.router)
app.include_router(content_api.router)
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_token_header)],
    responses={418: {"description": "I'm a teapot"}},
)


@app.get("/")
def welcome():
    return {"Hello": "There!"}

@app.get("/ping")
def pong():
    return {"ping": "pong!"}