from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle


def generar_pdf_entrada(imagen):
    buffer = BytesIO()

    imagen.convert("RGB").save(
        buffer,
        format="PDF",
        resolution=100.0,
    )

    buffer.seek(0)
    return buffer


def generar_pdf_asistentes(asistentes):
    buffer = BytesIO()

    documento = SimpleDocTemplate(
        buffer,
        pagesize=landscape(A4),
        leftMargin=8 * mm,
        rightMargin=8 * mm,
        topMargin=8 * mm,
        bottomMargin=8 * mm,
    )

    datos = [
        [
            "Nombre",
            "Teléfono",
            "Forma de pago",
            "Token",
            "Control",
        ]
    ]

    for asistente in asistentes:
        datos.append(
            [
                asistente["nombre"],
                asistente["telefono"] or "",
                asistente["forma_pago"],
                asistente["token"],
                "",
            ]
        )

    tabla = Table(
        datos,
        repeatRows=1,
        colWidths=[
            90 * mm,  # Nombre
            30 * mm,  # Teléfono
            35 * mm,  # Forma de pago
            65 * mm,  # Token
            45 * mm,  # Control
        ],
    )

    tabla.setStyle(
        TableStyle(
            [
                ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ALIGN", (-1, 1), (-1, -1), "CENTER"),
            ]
        )
    )

    documento.build([tabla])

    buffer.seek(0)
    return buffer