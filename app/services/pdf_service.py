from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
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
        pagesize=A4,
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