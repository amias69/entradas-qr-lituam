import qrcode
from qrcode.constants import ERROR_CORRECT_M


def generar_qr(token):
    qr = qrcode.QRCode(
        version=1,
        error_correction=ERROR_CORRECT_M,
        box_size=10,
        border=1,
    )

    qr.add_data(token)
    qr.make(fit=False)

    return qr.make_image(
        fill_color="black",
        back_color="white",
    ).convert("RGB")