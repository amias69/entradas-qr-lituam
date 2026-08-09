from pathlib import Path

from PIL import Image

from app.services.qr_service import generar_qr


BASE_DIR = Path(__file__).resolve().parents[2]
PLANTILLA_PATH = BASE_DIR / "app" / "assets" / "entrada.png"

QR_X = 365
QR_Y = 755
QR_SIZE = 265


def generar_imagen_entrada(token):
    plantilla = Image.open(PLANTILLA_PATH).convert("RGB")

    qr = generar_qr(token)
    qr = qr.resize(
        (QR_SIZE, QR_SIZE),
        Image.Resampling.NEAREST,
    )

    plantilla.paste(
        qr,
        (QR_X, QR_Y),
    )

    return plantilla