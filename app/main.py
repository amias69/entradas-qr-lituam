import os
from fastapi import FastAPI
from fastapi import Depends
from fastapi.staticfiles import StaticFiles

from app.db.init_db import init_db
from app.routes.entradas import router as entradas_router
from app.routes.public import router as public_router
from app.routes.auth import router as auth_router
from starlette.middleware.sessions import SessionMiddleware

from app.routes.auth import obtener_usuario_actual



app = FastAPI()

SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "clave-desarrollo-cambiar-en-produccion",
)

app.add_middleware(
    SessionMiddleware,
    secret_key=SECRET_KEY,
    session_cookie="entradas_session",
    max_age=60 * 60 * 12,
    same_site="lax",
    https_only=False,
)

app.include_router(auth_router)

app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static",
)

@app.get("/")
def root(
    usuario=Depends(obtener_usuario_actual),
):
    return {
        "status": "ok",
        "usuario": usuario["username"],
    }


@app.on_event("startup")
def startup():
    init_db()


app.include_router(entradas_router)


@app.get("/")
def root():
    return {"status": "ok"}


app.include_router(public_router)
