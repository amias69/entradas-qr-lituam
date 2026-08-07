from pwdlib import PasswordHash


password_hash = PasswordHash.recommended()


def generar_password_hash(password):
    return password_hash.hash(password)


def verificar_password(password, hash_guardado):
    return password_hash.verify(
        password,
        hash_guardado,
    )
