from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi import HTTPException


from app.services.usuario_service import (autenticar_usuario, buscar_usuario_por_id)

router = APIRouter(
    tags=["autenticacion"],
)

templates = Jinja2Templates(
    directory="app/templates",
)

def obtener_usuario_actual(request: Request):
    usuario_id = request.session.get("usuario_id")

    if usuario_id is None:
        raise HTTPException(
            status_code=401,
            detail="Autenticación requerida",
        )

    usuario = buscar_usuario_por_id(usuario_id)

    if usuario is None or not usuario["activo"]:
        request.session.clear()

        raise HTTPException(
            status_code=401,
            detail="Autenticación requerida",
        )

    return usuario


@router.get("/login")
def mostrar_login(request: Request):
    if request.session.get("usuario_id"):
        return RedirectResponse(
            url="/",
            status_code=303,
        )

    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={
            "error": None,
        },
    )


@router.post("/login")
def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
):
    usuario = autenticar_usuario(
        username=username,
        password=password,
    )

    if usuario is None:
        return templates.TemplateResponse(
            request=request,
            name="login.html",
            context={
                "error": "Usuario o contraseña incorrectos.",
            },
            status_code=401,
        )

    request.session.clear()
    request.session["usuario_id"] = usuario["id"]

    return RedirectResponse(
        url="/",
        status_code=303,
    )


@router.post("/logout")
def logout(request: Request):
    request.session.clear()

    return RedirectResponse(
        url="/login",
        status_code=303,
    )