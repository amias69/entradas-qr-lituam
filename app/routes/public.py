from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates   
from io import BytesIO
from fastapi.responses import StreamingResponse
from app.services.entrada_service import buscar_por_token
from app.services.imagen_service import generar_imagen_entrada
from app.services.pdf_service import generar_pdf_entrada

router = APIRouter(
    tags=["publico"],
)

templates = Jinja2Templates(
    directory="app/templates"
)


@router.get(
    "/e/{token}",
    response_class=HTMLResponse,
)
def ver_entrada(request: Request, token: str):
    entrada = buscar_por_token(token)

    if entrada is None:
        raise HTTPException(
            status_code=404,
            detail="Entrada no encontrada",
        )

    return templates.TemplateResponse(
        request=request,
        name="entrada_publica.html",
        context={
            "token": token,
            "nombre": entrada["nombre"],
            "estado": entrada["estado"],
        },
    )

@router.get("/e/{token}/imagen")
def obtener_imagen(token: str):
    entrada = buscar_por_token(token)

    if entrada is None:
        raise HTTPException(
            status_code=404,
            detail="Entrada no encontrada",
        )

    if entrada["estado"] == "ANULADA":
        raise HTTPException(
            status_code=404,
            detail="Entrada no disponible",
        )

    imagen = generar_imagen_entrada(token)

    buffer = BytesIO()

    imagen.save(
        buffer,
        format="JPEG",
        quality=95,
    )

    buffer.seek(0)

    return StreamingResponse(
        buffer,
        media_type="image/jpeg",
    )

@router.get("/e/{token}/pdf")
def descargar_pdf(token: str):
    entrada = buscar_por_token(token)

    if entrada is None:
        raise HTTPException(
            status_code=404,
            detail="Entrada no encontrada",
        )

    if entrada["estado"] == "ANULADA":
        raise HTTPException(
            status_code=404,
            detail="Entrada no disponible",
        )

    imagen = generar_imagen_entrada(token)
    pdf = generar_pdf_entrada(imagen)

    return StreamingResponse(
        pdf,
        media_type="application/pdf",
        headers={
            "Content-Disposition":
                f'attachment; filename="entrada-{token}.pdf"'
        },
    )
