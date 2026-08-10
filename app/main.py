import os
from fastapi import FastAPI
from fastapi import Depends, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import (
    HTMLResponse,
    RedirectResponse,
    JSONResponse,
)
from fastapi.templating import Jinja2Templates

from app.db.init_db import init_db
from app.routes.entradas import router as entradas_router
from app.routes.public import router as public_router
from app.routes.auth import router as auth_router
from starlette.middleware.sessions import SessionMiddleware
from app.services.usuario_service import buscar_usuario_por_id
from app.routes.auth import obtener_usuario_actual
from app.services.reporte_service import generar_reporte
from starlette.exceptions import (
    HTTPException as StarletteHTTPException,
)


app = FastAPI()

SECRET_KEY = os.environ["SECRET_KEY"]

COOKIE_SECURE = (
    os.environ.get("COOKIE_SECURE", "false").lower()
    == "true"
)

app.add_middleware(
    SessionMiddleware,
    secret_key=SECRET_KEY,
    session_cookie="entradas_session",
    max_age=60 * 60 * 12,
    same_site="lax",
    https_only=COOKIE_SECURE,
)

app.include_router(auth_router)

app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static",
)

templates = Jinja2Templates(
    directory="app/templates",
)

@app.exception_handler(StarletteHTTPException)
async def manejar_error_http(
    request: Request,
    exc: StarletteHTTPException,
):
    ruta = request.url.path

    # Las APIs deben seguir respondiendo JSON.
    if ruta.startswith("/api/"):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "detail": exc.detail,
            },
            headers=exc.headers,
        )

    # Páginas web.
    if exc.status_code == 404:
        titulo = "Página no encontrada"
        mensaje = (
            "El contenido solicitado no existe "
            "o ya no está disponible."
        )

    elif exc.status_code in (401, 403):
        titulo = "Acceso restringido"
        mensaje = (
            "No tienes autorización para "
            "ver esta página."
        )

    else:
        titulo = "Contenido no disponible"
        mensaje = (
            "No es posible mostrar el "
            "contenido solicitado."
        )

    return templates.TemplateResponse(
        request=request,
        name="error.html",
        context={
            "titulo": titulo,
            "mensaje": mensaje,
        },
        status_code=exc.status_code,
    )


@app.get(
    "/",
    response_class=HTMLResponse,
)
def inicio(request: Request):
    usuario_id = request.session.get("usuario_id")

    if usuario_id is None:
        return RedirectResponse(
            url="/login",
            status_code=303,
        )

    usuario = buscar_usuario_por_id(usuario_id)

    if usuario is None or not usuario["activo"]:
        request.session.clear()

        return RedirectResponse(
            url="/login",
            status_code=303,
        )

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "usuario": usuario,
        },
    )

@app.on_event("startup")
def startup():
    init_db()

app.include_router(entradas_router)

app.include_router(public_router)

@app.get(
    "/generar",
    response_class=HTMLResponse,
)
def generar_pagina(
    request: Request,
    usuario=Depends(obtener_usuario_actual),
):
    return templates.TemplateResponse(
        request=request,
        name="generar.html",
        context={
            "usuario": usuario,
        },
    )

@app.get(
    "/consultar",
    response_class=HTMLResponse,
)
def consultar_pagina(
    request: Request,
    usuario=Depends(obtener_usuario_actual),
):
    return templates.TemplateResponse(
        request=request,
        name="consultar.html",
        context={
            "usuario": usuario,
        },
    )


@app.get(
    "/control-acceso",
    response_class=HTMLResponse,
)
def control_acceso_pagina(
    request: Request,
    usuario=Depends(obtener_usuario_actual),
):
    return templates.TemplateResponse(
        request=request,
        name="escanear.html",
        context={
            "usuario": usuario,
        },
    )

@app.get(
    "/reporte",
    response_class=HTMLResponse,
)
def reporte_pagina(
    request: Request,
    usuario=Depends(obtener_usuario_actual),
):
    reporte = generar_reporte()

    return templates.TemplateResponse(
        request=request,
        name="reporte.html",
        context={
            "usuario": usuario,
            "asistentes": reporte["asistentes"],
            "resumen": reporte["resumen"],
        },
    )
