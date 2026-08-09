from app.constants import PRECIO_ENTRADA
from app.services.entrada_service import listar_asistentes


def generar_reporte():
    asistentes = listar_asistentes()

    yape_plin = 0
    efectivo = 0
    cortesia = 0

    for asistente in asistentes:
        forma_pago = asistente["forma_pago"]

        if forma_pago == "YAPE / PLIN":
            yape_plin += 1

        elif forma_pago == "EFECTIVO":
            efectivo += 1

        elif forma_pago == "CORTESÍA":
            cortesia += 1

    pagadas = yape_plin + efectivo
    total_asistentes = pagadas + cortesia

    recaudado_yape_plin = yape_plin * PRECIO_ENTRADA
    recaudado_efectivo = efectivo * PRECIO_ENTRADA

    total_recaudado = (
        recaudado_yape_plin
        + recaudado_efectivo
    )

    return {
        "asistentes": asistentes,
        "resumen": {
            "yape_plin": yape_plin,
            "efectivo": efectivo,
            "cortesia": cortesia,
            "pagadas": pagadas,
            "total_asistentes": total_asistentes,
            "recaudado_yape_plin": recaudado_yape_plin,
            "recaudado_efectivo": recaudado_efectivo,
            "total_recaudado": total_recaudado,
            "precio_entrada": PRECIO_ENTRADA,
        },
    }