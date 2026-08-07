import secrets


ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
TOKEN_LENGTH = 20


def generar_token():
    return "".join(
        secrets.choice(ALPHABET)
        for _ in range(TOKEN_LENGTH)
    )