from fastapi import APIRouter, HTTPException
from fastapi import Depends
from fastapi.responses import StreamingResponse

from app.schemas.entrada import EntradaCreate, EntradaUpdate
from app.services.entrada_service import (
    anular_entrada,
    buscar_entradas,
    crear_entrada,
    editar_entrada,
    listar_asistentes,
    validar_entrada,
)
from app.services.pdf_service import generar_pdf_asistentes
from app.services.entrada_service import obtener_historial
from app.routes.auth import obtener_usuario_actual
from app.services.entrada_service import buscar_por_id


router = APIRouter(
    prefix="/api/entradas",
    tags=["entradas"],
)   

@router.post("")
def crear(
    datos: EntradaCreate,
    usuario=Depends(obtener_usuario_actual),
):
    entrada = crear_entrada(
        nombre=datos.nombre,
        telefono=datos.telefono,
        forma_pago=datos.forma_pago,
        generado_por=usuario["id"],
    )

    return dict(entrada)

@router.get("")
def buscar(
    q: str,
    usuario=Depends(obtener_usuario_actual),
):
    resultados = buscar_entradas(q)

    return [dict(entrada) for entrada in resultados]

@router.get("/{entrada_id}")
def obtener_entrada(
    entrada_id: int,
    usuario=Depends(obtener_usuario_actual),
):
    entrada = buscar_por_id(entrada_id)

    if entrada is None:
        raise HTTPException(
            status_code=404,
            detail="Entrada no encontrada",
        )

    return dict(entrada)

@router.put("/{entrada_id}")
def editar(
    entrada_id: int,
    datos: EntradaUpdate,
    usuario=Depends(obtener_usuario_actual),
):
    entrada = editar_entrada(
        entrada_id=entrada_id,
        nombre=datos.nombre,
        telefono=datos.telefono,
        forma_pago=datos.forma_pago,
        usuario_id=usuario["id"],
    )

    if entrada is None:
        raise HTTPException(
            status_code=404,
            detail="Entrada no encontrada",
        )

    return dict(entrada)

@router.post("/{entrada_id}/anular")
def anular(
    entrada_id: int,
    usuario=Depends(obtener_usuario_actual),
):
    entrada = anular_entrada(
        entrada_id=entrada_id,
        usuario_id=usuario["id"],
    )

    if entrada is None:
        raise HTTPException(
            status_code=400,
            detail="La entrada no existe o no puede ser anulada",
        )

    return dict(entrada)

@router.post("/{token}/validar")
def validar(
    token: str,
    usuario=Depends(obtener_usuario_actual),
):
    entrada = validar_entrada(
        token=token,
        usuario_id=usuario["id"],
    )

    if entrada is None:
        raise HTTPException(
            status_code=400,
            detail="Entrada inválida, usada o anulada",
        )

    return dict(entrada)

@router.get("/asistentes/lista")
def asistentes():
    resultados = listar_asistentes()

    return [dict(entrada) for entrada in resultados]

@router.get("/asistentes/pdf")
def descargar_lista_asistentes(
    usuario=Depends(obtener_usuario_actual),
):
    asistentes = listar_asistentes()

    pdf = generar_pdf_asistentes(asistentes)

    return StreamingResponse(
        pdf,
        media_type="application/pdf",
        headers={
            "Content-Disposition":
                'attachment; filename="lista-asistentes.pdf"'
        },
    )

@router.get("/{entrada_id}/historial")
def historial(
    entrada_id: int,
    usuario=Depends(obtener_usuario_actual),
):
    return [
        dict(registro)
        for registro in obtener_historial(entrada_id)
    ]